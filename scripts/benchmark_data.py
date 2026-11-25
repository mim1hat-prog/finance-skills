"""Validated, immutable public benchmark snapshots. Python standard library only."""
from __future__ import annotations

import calendar
import csv
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import ipaddress
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import parse_qsl, urlsplit

from schema_validation import validate as shared_validate, SchemaValidationError, UnsupportedSchemaError

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORE = ROOT / "benchmarks"
SCHEMA_DIR = ROOT / "schemas"
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9.-]{0,119}\Z")
SECRET_NAMES = re.compile(r"(?:app_?id|application_?id|api_?key|access_?token|key|token|authorization|password|secret|credential)", re.I)
DECIMAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z")


class BenchmarkError(ValueError):
    def __init__(self, code: str, detail: str, status: int = 400):
        super().__init__(detail)
        self.code, self.detail, self.status = code, detail, status


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def timestamp(value: str) -> datetime:
    try:
        shared_validate(value, {"type": "string", "format": "date-time"})
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.astimezone(timezone.utc)
    except (ValueError, TypeError, AttributeError, OverflowError) as exc:
        raise BenchmarkError("invalid_timestamp", "Use a valid RFC 3339 timestamp with an explicit timezone.") from exc


def day(value: str) -> date:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise BenchmarkError("invalid_date", "Use an ISO calendar date YYYY-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise BenchmarkError("invalid_date", "The calendar date is invalid.") from exc


def identifier(value: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise BenchmarkError("invalid_identifier", "Use a bounded lowercase dataset, series or snapshot identifier.")
    return value


def number(value: str) -> Decimal:
    if not isinstance(value, str) or not DECIMAL.fullmatch(value) or len(value) > 80:
        raise BenchmarkError("invalid_value", "Observation values must be finite bounded decimal strings.")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise BenchmarkError("invalid_value", "Observation value is not a finite decimal.") from exc
    if not result.is_finite():
        raise BenchmarkError("invalid_value", "Observation value is not finite.")
    return result


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_public_url(value: str) -> None:
    try:
        parts = urlsplit(value)
        query = parse_qsl(parts.query, keep_blank_values=True)
    except ValueError as exc:
        raise BenchmarkError("unsafe_metadata", "Source URL is malformed.") from exc
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.fragment:
        raise BenchmarkError("unsafe_metadata", "Source URLs must be public HTTPS URLs without credentials or fragments.")
    if any(SECRET_NAMES.fullmatch(key) for key, _ in query):
        raise BenchmarkError("unsafe_metadata", "Credential parameters must never be stored in source URLs.")
    host = parts.hostname.lower()
    try:
        private_address = not ipaddress.ip_address(host).is_global
    except ValueError:
        private_address = False
    if private_address or host in {"localhost", "teams.microsoft.com", "outlook.office.com", "outlook.office365.com"} or host.endswith((".local", ".internal", ".corp", ".sharepoint.com", ".onmicrosoft.com")):
        raise BenchmarkError("unsafe_metadata", "A public benchmark cannot contain an internal source URL.")


def reject_secrets(value) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if SECRET_NAMES.fullmatch(key):
                raise BenchmarkError("unsafe_metadata", "Credential fields cannot be saved in the public dataset.")
            reject_secrets(item)
    elif isinstance(value, list):
        for item in value:
            reject_secrets(item)
    elif isinstance(value, str):
        if "-----BEGIN " in value and "PRIVATE KEY-----" in value:
            raise BenchmarkError("unsafe_metadata", "A private key cannot be saved in a benchmark dataset.")
        if value.startswith(("https://", "http://")):
            safe_public_url(value)


def schema_validate(value, schema: dict, root_schema: dict | None = None) -> None:
    """Use the shared, fail-closed project subset validator for data and API schemas."""
    try:
        shared_validate(value, schema, root_schema)
    except UnsupportedSchemaError as exc:
        raise BenchmarkError("invalid_schema", str(exc), 500) from exc
    except SchemaValidationError as exc:
        raise BenchmarkError("schema_validation_failed", str(exc)) from exc


def validate_named(value, name: str, definition: str | None = None) -> None:
    schema = json.loads((SCHEMA_DIR / f"benchmark-{name}.schema.json").read_text(encoding="utf-8"))
    schema_validate(value, schema["$defs"][definition] if definition else schema, schema)


def load_catalog(store: Path = DEFAULT_STORE) -> dict:
    if store.is_symlink() or (store / "catalog.json").is_symlink():
        raise BenchmarkError("unsafe_storage", "Catalogue storage must not be a symlink.")
    catalog = json.loads((store / "catalog.json").read_text(encoding="utf-8"))
    validate_named(catalog, "catalog")
    reject_secrets(catalog)
    ids = [s["id"] for s in catalog["series"]]
    if len(ids) != len(set(ids)):
        raise BenchmarkError("invalid_catalog", "Series identifiers must be unique.")
    return catalog


def period_bounds(period: str, frequency: str) -> tuple[str, str]:
    if frequency == "daily":
        value = day(period)
        return value.isoformat(), value.isoformat()
    if frequency != "monthly" or not re.fullmatch(r"\d{4}-\d{2}", period):
        raise BenchmarkError("invalid_period", "The period does not match the series frequency.")
    value = day(period + "-01")
    return value.isoformat(), value.replace(day=calendar.monthrange(value.year, value.month)[1]).isoformat()


def observation(series: dict, period: str, value: str, retrieved_at: str, *, release_at: str | None = None, release_date: str | None = None,
                source_url: str | None = None, origin: str = "original", completeness: str = "complete",
                status: str = "published", inputs: list | None = None, transformation: dict | None = None, observed_through: str | None = None) -> dict:
    number(value)
    start, end = period_bounds(period, series["frequency"])
    if observed_through is not None:
        if completeness != "partial" or not day(start) <= day(observed_through) <= day(end):
            raise BenchmarkError("invalid_period", "An explicit observed-through date requires a partial period within its calendar bounds.")
        end = observed_through
    return {"series_id": series["id"], "provider": series["provider"], "provider_series_id": series["provider_series_id"],
            "source_id": series["source_id"], "source_url": source_url or series["source_url"],
            "observation_period": period, "period_start": start, "period_end": end, "value": value,
            "unit": series["unit"], "geography": series["geography"], "currency": series["currency"],
            "index_base": series["index_base"], "frequency": series["frequency"], "seasonal_adjustment": series["seasonal_adjustment"],
            "release_date": release_date, "release_at": release_at, "retrieved_at": retrieved_at, "snapshot_id": "pending",
            "origin": origin, "period_completeness": completeness, "observation_status": status,
            "inputs": inputs or [], "transformation": transformation}


def validate_snapshot(snapshot: dict) -> None:
    validate_named(snapshot, "snapshot")
    reject_secrets(snapshot)
    series = {s["id"]: s for s in snapshot["series"]}
    if len(series) != len(snapshot["series"]):
        raise BenchmarkError("invalid_snapshot", "Snapshot series must be unique.")
    seen = set()
    retrieved = timestamp(snapshot["retrieved_at"])
    for row in snapshot["observations"]:
        if row["series_id"] not in series or row["snapshot_id"] != snapshot["id"]:
            raise BenchmarkError("invalid_snapshot", "Observation points outside its snapshot or series inventory.")
        definition = series[row["series_id"]]
        if snapshot["data_class"] == "public" and definition["rights"]["redistribution"] != "permitted":
            raise BenchmarkError("redistribution_not_permitted", "This series cannot be mirrored in a public snapshot.", 403)
        if snapshot["data_class"] == "synthetic" and row["origin"] != "synthetic":
            raise BenchmarkError("invalid_snapshot", "Synthetic snapshots must label every observation synthetic.")
        if snapshot["data_class"] == "public" and row["origin"] == "synthetic":
            raise BenchmarkError("invalid_snapshot", "Synthetic values cannot be mixed into a public snapshot.")
        if snapshot["data_class"] == "public" and row["origin"] != definition["series_kind"]:
            raise BenchmarkError("invalid_derivation", "A public observation's origin must match its frozen original or derived series definition.")
        for key in ("provider", "provider_series_id", "source_id", "unit", "geography", "currency", "index_base", "frequency", "seasonal_adjustment"):
            if row[key] != definition[key]:
                raise BenchmarkError("metadata_mismatch", "Observation metadata differs from its frozen series definition.")
        expected_start, expected_end = period_bounds(row["observation_period"], row["frequency"])
        if row["period_start"] != expected_start or not day(expected_start) <= day(row["period_end"]) <= day(expected_end):
            raise BenchmarkError("invalid_period", "Observation period boundaries are inconsistent.")
        if row["period_completeness"] == "complete" and row["period_end"] != expected_end:
            raise BenchmarkError("partial_period", "An incomplete calendar window cannot be labeled a complete observation period.")
        if day(row["period_end"]) > timestamp(row["retrieved_at"]).date():
            raise BenchmarkError("future_observation_period", "An observation window cannot extend beyond its observed retrieval date.")
        if timestamp(row["retrieved_at"]) > retrieved:
            raise BenchmarkError("invalid_snapshot", "Observation retrieval cannot follow snapshot retrieval.")
        if row["release_date"] and day(row["release_date"]) > timestamp(row["retrieved_at"]).date():
            raise BenchmarkError("invalid_snapshot", "Release date cannot follow retrieval.")
        if row["release_at"] and row["release_date"] and timestamp(row["release_at"]).date() != day(row["release_date"]):
            raise BenchmarkError("invalid_snapshot", "Release date and timestamp conflict.")
        if row["release_at"] and timestamp(row["release_at"]) > timestamp(row["retrieved_at"]):
            raise BenchmarkError("invalid_snapshot", "A release cannot be asserted after its retrieval.")
        number(row["value"])
        key = (row["series_id"], row["observation_period"])
        if key in seen:
            raise BenchmarkError("duplicate_observation", "A snapshot cannot contain duplicate series-period observations.")
        seen.add(key)
        if row["origin"] == "derived" and (not row["transformation"] or not row["inputs"]):
            raise BenchmarkError("missing_derivation", "Derived values need input references and a versioned formula.")
        if row["origin"] == "original" and (row["transformation"] is not None or row["inputs"]):
            raise BenchmarkError("invalid_derivation", "Original observations cannot claim a project transformation.")
    by_key = {(r["series_id"], r["observation_period"]): r for r in snapshot["observations"]}
    for row in snapshot["observations"]:
        if row["origin"] != "derived":
            continue
        refs = row["inputs"]
        if any(ref["snapshot_id"] != snapshot["id"] or (ref["series_id"], ref["observation_period"]) not in by_key for ref in refs):
            raise BenchmarkError("missing_derivation", "Every derived input must resolve inside the same retained snapshot.")
        if row["transformation"]["id"] != "ecb-jpy-cross" or row["transformation"]["version"] != "1.0.0" or len(refs) != 2:
            raise BenchmarkError("unsupported_derivation", "The derived observation needs a supported versioned transformation.")
        first, second = [by_key[(ref["series_id"], ref["observation_period"])] for ref in refs]
        definition = series[row["series_id"]]
        expected_denominator = definition["base_currency"] + " per EUR"
        if (first["unit"] != "JPY per EUR" or second["unit"] != expected_denominator
                or first["observation_period"] != row["observation_period"] or second["observation_period"] != row["observation_period"]
                or first["origin"] != "original" or second["origin"] != "original"
                or first["period_completeness"] != "complete" or second["period_completeness"] != "complete"
                or number(second["value"]) <= 0 or number(first["value"]) <= 0):
            raise BenchmarkError("invalid_derivation", "Cross-rate inputs have incompatible period, quote or value semantics.")
        with localcontext() as context:
            context.prec = 40
            expected_value = number(first["value"]) / number(second["value"])
        if number(row["value"]) != expected_value:
            raise BenchmarkError("invalid_derivation", "The derived value does not match its retained inputs and transformation.")
    expected = coverage(snapshot["series"], snapshot["observations"])
    if expected != snapshot["coverage"]:
        raise BenchmarkError("invalid_coverage", "Snapshot coverage must match its actual observations.")


def coverage(series: list[dict], rows: list[dict]) -> list[dict]:
    output = []
    for item in sorted(series, key=lambda s: s["id"]):
        periods = sorted(r["observation_period"] for r in rows if r["series_id"] == item["id"])
        output.append({"series_id": item["id"], "status": "available" if periods else "no-observations",
                       "count": len(periods), "first_period": periods[0] if periods else None,
                       "last_period": periods[-1] if periods else None})
    return output


def make_snapshot(catalog: dict, rows: list[dict], retrieved_at: str, *, data_class: str, series_ids: list[str], capture_method: str) -> dict:
    timestamp(retrieved_at)
    selected = [s for s in catalog["series"] if s["id"] in set(series_ids)]
    if len(selected) != len(set(series_ids)):
        raise BenchmarkError("unknown_series", "Requested series is absent from the catalogue.")
    rows = json.loads(json.dumps(rows))
    base = {"schema_version": "1.0", "dataset_id": catalog["dataset_id"], "dataset_version": catalog["dataset_version"],
            "retrieved_at": retrieved_at, "data_class": data_class, "knowledge_basis": "retrieval-time",
            "capture_method": capture_method, "series": selected,
            "observations": sorted(rows, key=lambda r: (r["series_id"], r["observation_period"])),
            "coverage": coverage(selected, rows)}
    snapshot_id = timestamp(retrieved_at).strftime("%Y%m%dT%H%M%SZ").lower() + "-" + digest(json_bytes(base))[:16]
    base["id"] = snapshot_id
    for row in base["observations"]:
        row["snapshot_id"] = snapshot_id
        for ref in row["inputs"]:
            if ref.get("snapshot_id") == "pending":
                ref["snapshot_id"] = snapshot_id
    validate_snapshot(base)
    return base


def csv_bytes(snapshot: dict) -> bytes:
    columns = sorted(snapshot["observations"][0]) if snapshot["observations"] else ["series_id", "observation_period", "value"]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in snapshot["observations"]:
        writer.writerow({k: json.dumps(v, sort_keys=True, separators=(",", ":")) if isinstance(v, (dict, list)) else v for k, v in row.items()})
    return stream.getvalue().encode("utf-8")


def store_snapshot(store: Path, snapshot: dict) -> Path:
    validate_snapshot(snapshot)
    parent = store / "snapshots"
    if store.is_symlink() or parent.is_symlink():
        raise BenchmarkError("unsafe_storage", "Snapshot storage must not be a symlink.")
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / identifier(snapshot["id"])
    files = {"snapshot.json": json_bytes(snapshot), "observations.csv": csv_bytes(snapshot)}
    files["manifest.json"] = json_bytes({"schema_version": "1.0", "snapshot_id": snapshot["id"], "data_class": snapshot["data_class"],
                                       "files": [{"path": name, "bytes": len(data), "sha256": digest(data)} for name, data in sorted(files.items())]})
    if target.exists() or target.is_symlink():
        if target.is_symlink() or not target.is_dir() or {p.name for p in target.iterdir()} != set(files):
            raise BenchmarkError("immutable_snapshot_conflict", "Existing snapshot inventory differs; preserve it.", 409)
        if any((target / name).is_symlink() or (target / name).read_bytes() != data for name, data in files.items()):
            raise BenchmarkError("immutable_snapshot_conflict", "Existing snapshot bytes differ; preserve it.", 409)
        write_inventory(store)
        return target
    stage = Path(tempfile.mkdtemp(prefix=".snapshot-", dir=parent))
    try:
        for name, data in files.items():
            (stage / name).write_bytes(data)
        if target.exists() or target.is_symlink():
            raise BenchmarkError("immutable_snapshot_conflict", "Snapshot appeared while writing; preserve it.", 409)
        stage.rename(target)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    write_inventory(store)
    return target


def load_snapshot(store: Path, snapshot_id: str) -> dict:
    if store.is_symlink() or (store / "snapshots").is_symlink():
        raise BenchmarkError("unsafe_storage", "Snapshot storage must not be a symlink.")
    folder = store / "snapshots" / identifier(snapshot_id)
    if folder.is_symlink() or not folder.is_dir():
        raise BenchmarkError("snapshot_not_found", "Snapshot was not found.", 404)
    if {p.name for p in folder.iterdir()} != {"manifest.json", "snapshot.json", "observations.csv"}:
        raise BenchmarkError("snapshot_integrity_failed", "Snapshot inventory changed.", 500)
    for file in folder.iterdir():
        if file.is_symlink() or not file.is_file():
            raise BenchmarkError("snapshot_integrity_failed", "Snapshot files must be unlinked regular files.", 500)
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "1.0" or manifest.get("snapshot_id") != snapshot_id:
        raise BenchmarkError("snapshot_integrity_failed", "Snapshot manifest identity differs.", 500)
    records = manifest.get("files", [])
    if len(records) != 2 or {r.get("path") for r in records} != {"snapshot.json", "observations.csv"}:
        raise BenchmarkError("snapshot_integrity_failed", "Snapshot manifest inventory differs.", 500)
    for row in records:
        data = (folder / row["path"]).read_bytes()
        if len(data) != row.get("bytes") or digest(data) != row.get("sha256"):
            raise BenchmarkError("snapshot_integrity_failed", "Snapshot checksum differs.", 500)
    snapshot = json.loads((folder / "snapshot.json").read_text(encoding="utf-8"))
    validate_snapshot(snapshot)
    if snapshot["id"] != snapshot_id or manifest.get("data_class") != snapshot["data_class"] or csv_bytes(snapshot) != (folder / "observations.csv").read_bytes():
        raise BenchmarkError("snapshot_integrity_failed", "Snapshot identity or CSV representation differs.", 500)
    return snapshot


def snapshots(store: Path) -> list[dict]:
    folder = store / "snapshots"
    if not folder.exists():
        return []
    if folder.is_symlink():
        raise BenchmarkError("unsafe_storage", "Snapshot storage must not be a symlink.", 500)
    result = []
    for path in sorted(folder.iterdir()):
        if path.name.startswith("."):
            continue
        result.append(load_snapshot(store, path.name))
    return sorted(result, key=lambda s: (timestamp(s["retrieved_at"]), s["id"]))


def dataset_inventory(store: Path) -> dict:
    catalog = load_catalog(store)
    saved = snapshots(store)
    if any(s["dataset_id"] != catalog["dataset_id"] for s in saved):
        raise BenchmarkError("dataset_identity_mismatch", "A snapshot belongs to a different dataset.", 500)
    return {"schema_version": "1.0", "dataset_id": catalog["dataset_id"], "dataset_version": catalog["dataset_version"],
            "stream": "public-benchmark", "catalog_path": "catalog.json", "catalog_sha256": digest((store / "catalog.json").read_bytes()),
            "snapshot_layout": "snapshots/{id}/{snapshot.json,observations.csv,manifest.json}",
            "snapshots": [{"id": s["id"], "data_class": s["data_class"], "retrieved_at": s["retrieved_at"],
                           "manifest_sha256": digest((store / "snapshots" / s["id"] / "manifest.json").read_bytes())} for s in saved]}


def write_inventory(store: Path) -> None:
    data = json_bytes(dataset_inventory(store))
    target = store / "manifest.json"
    if target.is_symlink():
        raise BenchmarkError("unsafe_storage", "Dataset manifest must not be a symlink.")
    if target.exists() and target.read_bytes() == data:
        return
    descriptor, temporary = tempfile.mkstemp(prefix=".inventory-", dir=store)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def check_inventory(store: Path) -> None:
    target = store / "manifest.json"
    if target.is_symlink() or not target.is_file() or target.read_bytes() != json_bytes(dataset_inventory(store)):
        raise BenchmarkError("dataset_integrity_failed", "Dataset catalogue/snapshot manifest differs; review and rebuild the inventory.", 500)


def select_snapshot(store: Path, series_id: str | None = None, *, snapshot_id: str | None = None,
                    as_of: str | None = None, data_class: str = "public") -> dict:
    if snapshot_id and as_of:
        raise BenchmarkError("conflicting_vintage", "Choose snapshot_id or as_of, not both.")
    if data_class not in {"public", "synthetic"}:
        raise BenchmarkError("invalid_data_class", "Choose public or synthetic data explicitly.")
    candidates = [load_snapshot(store, snapshot_id)] if snapshot_id else snapshots(store)
    candidates = [s for s in candidates if s["data_class"] == data_class and (series_id is None or series_id in {r["id"] for r in s["series"]})]
    if as_of:
        cutoff = timestamp(as_of)
        candidates = [s for s in candidates if timestamp(s["retrieved_at"]) <= cutoff]
    if not candidates:
        if as_of:
            raise BenchmarkError("as_of_unavailable", "No retained snapshot establishes what was available by that cutoff. Latest data was not substituted.", 404)
        raise BenchmarkError("snapshot_not_found", "No validated snapshot matches the requested series and data class.", 404)
    return max(candidates, key=lambda s: (timestamp(s["retrieved_at"]), s["id"]))


def freshness(snapshot: dict, series: dict, now: str | None = None) -> dict:
    at = timestamp(now or utc_now())
    rows = [r for r in snapshot["observations"] if r["series_id"] == series["id"]]
    if not rows:
        return {"status": "no-observations", "observation_age_days": None, "retrieval_age_days": max(0, (at - timestamp(snapshot["retrieved_at"])).days), "max_age_days": series["freshness_days"]}
    last = max(day(r["period_end"]) for r in rows)
    age = max(0, (at.date() - last).days)
    return {"status": "stale" if age > series["freshness_days"] else "within-policy", "observation_age_days": age,
            "retrieval_age_days": max(0, (at - timestamp(snapshot["retrieved_at"])).days), "max_age_days": series["freshness_days"]}


def percentage_change(current: dict, prior: dict) -> str:
    for field in ("series_id", "unit", "currency", "index_base", "frequency", "seasonal_adjustment"):
        if current[field] != prior[field]:
            raise BenchmarkError("incomparable_observations", "Changes require the same series definition, units, base and adjustment.")
    if current["period_completeness"] != "complete" or prior["period_completeness"] != "complete":
        raise BenchmarkError("partial_period", "A partial or unknown period cannot be treated as a complete comparison period.")
    if day(current["period_start"]) <= day(prior["period_start"]):
        raise BenchmarkError("invalid_comparison", "Current period must follow the prior period.")
    denominator = number(prior["value"])
    if denominator == 0:
        raise BenchmarkError("zero_denominator", "Percentage change cannot use a zero prior value.")
    with localcontext() as context:
        context.prec = 50
        return format((number(current["value"]) / denominator - 1) * 100, "f")
