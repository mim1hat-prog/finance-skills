"""Read-only local API over validated stored benchmarks; never fetch a provider per request."""
from __future__ import annotations

import argparse
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit

from benchmark_data import (BenchmarkError, DEFAULT_STORE, ROOT, SCHEMA_DIR, check_inventory, coverage, day, freshness, identifier, json_bytes,
                            load_catalog, load_snapshot, select_snapshot, snapshots, timestamp,
                            validate_named, utc_now)


def summary(snapshot: dict) -> dict:
    return {"id": snapshot["id"], "retrieved_at": snapshot["retrieved_at"], "data_class": snapshot["data_class"],
            "observation_count": len(snapshot["observations"])}


def latest_refresh(store: Path, adapter: str, *, as_of: str | None = None) -> dict | None:
    folder = store / "refresh-status"
    if not folder.exists():
        return None
    if folder.is_symlink():
        raise BenchmarkError("unsafe_storage", "Refresh status storage must not be linked.", 500)
    rows = []
    cutoff = timestamp(as_of) if as_of else None
    for path in folder.glob("*.json"):
        if path.is_symlink() or not path.is_file():
            raise BenchmarkError("unsafe_storage", "Refresh status entries must be regular files.", 500)
        row = json.loads(path.read_text(encoding="utf-8"))
        validate_named(row, "api", "RefreshStatus")
        if row["provider"] == adapter and (cutoff is None or timestamp(row["attempted_at"]) <= cutoff):
            rows.append(row)
    return max(rows, key=lambda r: timestamp(r["attempted_at"])) if rows else None


def problem(exc: BenchmarkError, path: str) -> tuple[int, dict, dict]:
    titles = {400: "Invalid benchmark request", 403: "Benchmark rights restriction", 404: "Benchmark not available",
              405: "Method not allowed", 409: "Benchmark configuration required", 413: "Request exceeds limits",
              500: "Benchmark integrity error", 502: "Public source failure", 503: "Benchmark source not ready"}
    body = {"type": "urn:finance-skills:problem:" + exc.code.replace("_", "-"),
            "title": titles.get(exc.status, "Benchmark request failed"), "status": exc.status,
            "detail": exc.detail, "instance": path, "code": exc.code}
    validate_named(body, "api", "Problem")
    headers = {"Content-Type": "application/problem+json; charset=utf-8", "Cache-Control": "no-store"}
    if exc.status == 405:
        headers["Allow"] = "GET"
    return exc.status, headers, body


def query_parameters(target: str) -> tuple[str, dict[str, str]]:
    if len(target) > 4096:
        raise BenchmarkError("request_too_long", "The request exceeds the supported URI length.", 413)
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or parsed.fragment:
        raise BenchmarkError("invalid_path", "Use an origin-relative API path without fragments.")
    path = unquote(parsed.path)
    if not path.startswith("/v1/") or ".." in path.split("/") or "\\" in path or any(ord(c) < 32 for c in path):
        raise BenchmarkError("invalid_path", "Use a documented API path.", 404)
    try:
        values = parse_qs(parsed.query, keep_blank_values=True, max_num_fields=12, strict_parsing=True)
    except ValueError:
        raise BenchmarkError("invalid_query", "Query parameters are malformed or exceed the supported limit.") from None
    if any(len(v) != 1 or v[0] == "" for v in values.values()):
        raise BenchmarkError("invalid_query", "Query parameters must be nonempty and cannot be repeated.")
    return path, {k: v[0] for k, v in values.items()}


def bounded_integer(value: str, name: str, lower: int, upper: int) -> int:
    if not re.fullmatch(r"0|[1-9][0-9]{0,5}", value) or not lower <= int(value) <= upper:
        raise BenchmarkError("invalid_pagination", f"{name} must be an integer from {lower} through {upper}.")
    return int(value)


def handle_request(method: str, target: str, store: Path = DEFAULT_STORE, *, now: str | None = None) -> tuple[int, dict, dict]:
    """Pure dispatcher used by the HTTP handler and contract tests. No provider/network calls."""
    path = "/v1/"
    try:
        path, query = query_parameters(target)
        if method != "GET":
            raise BenchmarkError("method_not_allowed", "This API exposes stored data through GET only.", 405)
        catalog = load_catalog(store)
        check_inventory(store)
        if path == "/v1/datasets":
            if query:
                raise BenchmarkError("unknown_parameter", "This endpoint has no query parameters.")
            saved = snapshots(store)
            if len(saved) > 500:
                raise BenchmarkError("snapshot_inventory_limit", "This local API inventory is limited to500 snapshots; archive and configure a bounded store.", 500)
            dataset = {"id": catalog["dataset_id"], "title": catalog["title"], "version": catalog["dataset_version"],
                       "stream": "public-benchmark", "series_count": len(catalog["series"]), "snapshot_count": len(saved),
                       "snapshots": [summary(s) for s in saved]}
            body, schema = {"data": [dataset], "count": 1}, "Datasets"
        elif path.startswith("/v1/snapshots/"):
            if query:
                raise BenchmarkError("unknown_parameter", "Snapshot retrieval uses only its immutable path identifier.")
            snapshot_id = identifier(path[len("/v1/snapshots/"):])
            body, schema = {"snapshot": load_snapshot(store, snapshot_id)}, "SnapshotResponse"
        elif path.startswith("/v1/series/"):
            parts = path[len("/v1/series/"):].split("/")
            series_id = identifier(parts[0])
            definition = next((s for s in catalog["series"] if s["id"] == series_id), None)
            if definition is None:
                raise BenchmarkError("series_not_found", "The series is not registered in this dataset.", 404)
            if len(parts) == 1:
                if query:
                    raise BenchmarkError("unknown_parameter", "Series metadata uses no query parameters; frozen metadata is returned with observations.")
                saved = [s for s in snapshots(store) if series_id in {v["id"] for v in s["series"]}]
                body, schema = {"dataset_id": catalog["dataset_id"], "series": definition,
                                "available_snapshots": [summary(s) for s in saved]}, "SeriesResponse"
            elif len(parts) == 2 and parts[1] == "observations":
                allowed = {"start", "end", "offset", "limit", "snapshot_id", "as_of", "data_class"}
                if set(query) - allowed:
                    raise BenchmarkError("unknown_parameter", "The request contains an unsupported query parameter.")
                if "start" not in query or "end" not in query:
                    raise BenchmarkError("date_range_required", "Both start and end dates are required for observation queries.")
                start, end = day(query["start"]), day(query["end"])
                if end < start or (end - start).days > 3660:
                    raise BenchmarkError("invalid_range", "Select an ordered date range of at most3660 days.")
                limit = bounded_integer(query.get("limit", "100"), "limit", 1, 500)
                offset = bounded_integer(query.get("offset", "0"), "offset", 0, 100000)
                try:
                    snapshot = select_snapshot(store, series_id, snapshot_id=query.get("snapshot_id"), as_of=query.get("as_of"), data_class=query.get("data_class", "public"))
                except BenchmarkError as exc:
                    if exc.code != "snapshot_not_found":
                        raise
                    if definition["rights"]["redistribution"] != "permitted":
                        raise BenchmarkError("redistribution_not_permitted", "This series is metadata-only until its reuse permission is resolved.", 403) from None
                    if definition["adapter_status"] in {"requires-configuration", "needs-source-validation"}:
                        raise BenchmarkError("source_not_ready", "Exact source/series configuration or native file validation is still required. No values were substituted.", 503) from None
                    raise
                frozen = next(s for s in snapshot["series"] if s["id"] == series_id)
                # Return complete observation periods inside the requested bounds; never prorate a monthly index.
                rows = [r for r in snapshot["observations"] if r["series_id"] == series_id and day(r["period_start"]) >= start and day(r["period_end"]) <= end]
                rows.sort(key=lambda r: r["observation_period"])
                page = rows[offset:offset + limit]
                body = {"dataset_id": snapshot["dataset_id"], "series": frozen, "snapshot_id": snapshot["id"],
                        "retrieved_at": snapshot["retrieved_at"], "data_class": snapshot["data_class"],
                        "vintage_status": "known-at-cutoff" if query.get("as_of") else "explicit-snapshot" if query.get("snapshot_id") else "latest-available",
                        "as_of": query.get("as_of"), "freshness": freshness(snapshot, frozen, now),
                        "refresh_status": latest_refresh(store, frozen["adapter"], as_of=query.get("as_of")), "data": page,
                        "pagination": {"offset": offset, "limit": limit, "total": len(rows), "next_offset": offset + limit if offset + limit < len(rows) else None},
                        "coverage": coverage([frozen], rows)[0]}
                schema = "ObservationsResponse"
            else:
                raise BenchmarkError("route_not_found", "This API route does not exist.", 404)
        else:
            raise BenchmarkError("route_not_found", "This API route does not exist.", 404)
        validate_named(body, "api", schema)
        return 200, {"Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store"}, body
    except BenchmarkError as exc:
        return problem(exc, path)
    except (OSError, ValueError, KeyError, TypeError, UnicodeError):
        return problem(BenchmarkError("dataset_integrity_failed", "Stored dataset or schema could not be validated. No provider call or fallback value was used.", 500), path)


def make_handler(store: Path):
    class Handler(BaseHTTPRequestHandler):
        server_version = "FinanceBenchmark/1.0"

        def dispatch(self):
            status, headers, body = handle_request(self.command, self.path, store)
            data = json_bytes(body)
            self.send_response(status)
            for key, value in headers.items():
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = dispatch

        def send_error(self, code, message=None, explain=None):
            status = 405 if code == 501 else code if 400 <= code <= 599 else 400
            error_code = "method_not_allowed" if status == 405 else "invalid_http_request"
            selected_status, headers, body = problem(BenchmarkError(error_code, "Use the documented read-only API request format.", status), "/v1/")
            data = json_bytes(body)
            self.send_response(selected_status)
            for key, value in headers.items():
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            if getattr(self, "command", None) != "HEAD":
                self.wfile.write(data)

        def log_message(self, format, *args):
            # No raw request URLs or query values in logs; no credentials are accepted by the API.
            return

    return Handler


def validate_openapi(store: Path = DEFAULT_STORE, openapi_path: Path | None = None) -> dict:
    """Check the project's documented routes/parameters/schema references against real dispatcher responses.

    This is a concrete contract gate, not a claim of general OpenAPI-validator conformance.
    """
    document = json.loads((openapi_path or ROOT / "api/openapi.yaml").read_text(encoding="utf-8"))
    expected = {"/v1/datasets": "Datasets", "/v1/series/{id}": "SeriesResponse",
                "/v1/series/{id}/observations": "ObservationsResponse", "/v1/snapshots/{id}": "SnapshotResponse"}
    if document.get("openapi") != "3.1.2" or set(document.get("paths", {})) != set(expected):
        raise BenchmarkError("api_contract_drift", "OpenAPI version or route inventory differs from the implemented contract.", 500)
    definitions = json.loads((SCHEMA_DIR / "benchmark-api.schema.json").read_text(encoding="utf-8"))["$defs"]
    components = document.get("components", {}).get("schemas", {})
    for name in {*expected.values(), "Problem"}:
        if name not in definitions or components.get(name) != {"$ref": "../schemas/benchmark-api.schema.json#/$defs/" + name}:
            raise BenchmarkError("api_contract_drift", "OpenAPI response schema reference differs from the runtime schema.", 500)
    for route, response in expected.items():
        methods = document["paths"][route]
        if set(methods) != {"get"}:
            raise BenchmarkError("api_contract_drift", "The API is GET-only.", 500)
        operation = methods["get"]
        if operation["responses"]["200"]["content"]["application/json"]["schema"] != {"$ref": "#/components/schemas/" + response}:
            raise BenchmarkError("api_contract_drift", "Documented success response differs from runtime.", 500)
        if operation["responses"]["default"]["content"]["application/problem+json"]["schema"] != {"$ref": "#/components/schemas/Problem"}:
            raise BenchmarkError("api_contract_drift", "Documented problem response differs from runtime.", 500)
        params = {p["name"]: p for p in operation.get("parameters", [])}
        required = {"id"} if "{id}" in route else set()
        if route.endswith("/observations"):
            required |= {"start", "end"}
            wanted = {"id", "start", "end", "limit", "offset", "snapshot_id", "as_of", "data_class"}
            if params.get("limit", {}).get("schema", {}).get("maximum") != 500 or params.get("offset", {}).get("schema", {}).get("maximum") != 100000:
                raise BenchmarkError("api_contract_drift", "Documented pagination bounds differ from runtime.", 500)
        else:
            wanted = required
        if set(params) != wanted or {name for name, p in params.items() if p.get("required")} != required:
            raise BenchmarkError("api_contract_drift", "Documented parameters differ from runtime.", 500)
    check_inventory(store)
    saved = snapshots(store)
    if not saved:
        raise BenchmarkError("api_contract_fixture_missing", "Contract execution needs a retained public or synthetic snapshot.", 500)
    sample = saved[-1]
    record = sample["observations"][0] if sample["observations"] else None
    if record is None:
        raise BenchmarkError("api_contract_fixture_missing", "Contract execution needs an observation.", 500)
    series_id = record["series_id"]
    targets = ["/v1/datasets", "/v1/series/" + series_id,
               "/v1/series/" + series_id + "/observations?start=" + record["period_start"] + "&end=" + record["period_end"] + "&snapshot_id=" + sample["id"] + "&data_class=" + sample["data_class"],
               "/v1/snapshots/" + sample["id"]]
    for route, target in zip(expected, targets):
        status, _, body = handle_request("GET", target, store)
        if status != 200:
            raise BenchmarkError("api_contract_execution_failed", "A documented route did not return a valid stored-data response.", 500)
        validate_named(body, "api", expected[route])
    status, _, error = handle_request("POST", "/v1/datasets", store)
    if status != 405:
        raise BenchmarkError("api_contract_execution_failed", "A write route was not rejected.", 500)
    validate_named(error, "api", "Problem")
    return {"openapi": document["openapi"], "routes": len(expected), "response_schemas_validated": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--check", action="store_true", help="Validate local catalogue and all snapshots without starting a server")
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.store)
        check_inventory(args.store)
        saved = snapshots(args.store)
        if args.check:
            contract = validate_openapi(args.store)
            print(json.dumps({"dataset": catalog["dataset_id"], "series": len(catalog["series"]), "validated_snapshots": len(saved), "api_contract": contract}))
            return 0
        if not 1 <= args.port <= 65535:
            raise BenchmarkError("invalid_port", "Port must be between1 and65535.")
        server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(args.store))
        print(f"Serving stored public benchmarks at http://127.0.0.1:{args.port}/v1/datasets; Ctrl+C stops the foreground server.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return 0
    except (BenchmarkError, OSError, ValueError, KeyError):
        print("Benchmark API could not validate its store or bind the local port. No public deployment or provider refresh was performed.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
