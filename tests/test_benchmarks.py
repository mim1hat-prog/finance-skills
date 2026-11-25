"""Independent synthetic benchmark regressions; no provider requests or company data."""
from __future__ import annotations

import copy
import csv
from datetime import datetime
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import URLError
from urllib.parse import urlencode
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import benchmark_api as api
import benchmark_collect as collect
import benchmark_data as data


def invented_ecb_csv(periods=("2024-01-02", "2024-01-03")) -> bytes:
    """Provider-shaped, wholly invented numbers used only in temporary test stores."""
    output = io.StringIO()
    fields = ["KEY", "FREQ", "CURRENCY", "CURRENCY_DENOM", "EXR_TYPE", "EXR_SUFFIX", "TIME_PERIOD", "OBS_VALUE", "UNIT", "UNIT_MULT"]
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for period in periods:
        for currency, value in {"JPY": "150", "USD": "1.25", "CNY": "8", "THB": "40"}.items():
            writer.writerow(dict(zip(fields, [f"EXR.D.{currency}.EUR.SP00.A", "D", currency, "EUR", "SP00", "A", period, value, currency, "0"])))
    return output.getvalue().encode()


def invented_xlsx(rows: list[list[str]], sheet="Monthly Prices") -> bytes:
    """Construct a minimal workbook from scratch, with no copied binary/workbook metadata."""
    from xml.sax.saxutils import escape
    def col(n):
        result = ""
        while n:
            n, rem = divmod(n - 1, 26)
            result = chr(65 + rem) + result
        return result
    xml_rows = []
    for r, row in enumerate(rows, 1):
        cells = ''.join(f'<c r="{col(c)}{r}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>' for c, value in enumerate(row, 1))
        xml_rows.append(f'<row r="{r}">{cells}</row>')
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w") as out:
        out.writestr("xl/workbook.xml", '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="'+sheet+'" sheetId="1" r:id="rId1"/></sheets></workbook>')
        out.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
        out.writestr("xl/worksheets/sheet1.xml", '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+''.join(xml_rows)+'</sheetData></worksheet>')
    return target.getvalue()


class BenchmarkDatasetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.store = Path(self.temporary.name)
        self.catalog = data.load_catalog()
        (self.store / "catalog.json").write_bytes(data.json_bytes(self.catalog))
        data.write_inventory(self.store)
        self.ecb = next(s for s in self.catalog["series"] if s["id"] == "ecb-jpy-per-eur")

    def tearDown(self):
        self.temporary.cleanup()

    def snapshot(self, retrieved, value="150", period="2024-01-02"):
        row = data.observation(self.ecb, period, value, retrieved)
        snapshot = data.make_snapshot(self.catalog, [row], retrieved, data_class="public", series_ids=[self.ecb["id"]], capture_method="Wholly invented contract-test input, not an actual provider observation")
        data.store_snapshot(self.store, snapshot)
        return snapshot

    def assert_code(self, code, function, *args, **kwargs):
        with self.assertRaises(data.BenchmarkError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_after_cutoff_revision_never_uses_latest(self):
        earlier = self.snapshot("2024-02-01T09:00:00Z", "150")
        revised = self.snapshot("2024-03-01T09:00:00Z", "151")
        before = data.select_snapshot(self.store, self.ecb["id"], as_of="2024-02-15T00:00:00Z")
        self.assertEqual(before["id"], earlier["id"])
        self.assertEqual(before["observations"][0]["value"], "150")
        self.assertEqual(data.select_snapshot(self.store, self.ecb["id"])["id"], revised["id"])
        self.assert_code("as_of_unavailable", data.select_snapshot, self.store, self.ecb["id"], as_of="2024-01-31T23:59:59Z")
        self.assert_code("conflicting_vintage", data.select_snapshot, self.store, self.ecb["id"], snapshot_id=earlier["id"], as_of="2024-02-15T00:00:00Z")

    def test_retrieval_time_follows_completed_fetch_or_import_not_request_start(self):
        started, completed, receipt = "2024-02-01T09:00:00Z", "2024-02-01T09:01:00Z", "2024-02-01T09:02:00Z"
        imported = self.store / "invented-provider.csv"
        imported.write_bytes(invented_ecb_csv())
        for mode in ("fetch", "import"):
            with self.subTest(mode=mode), patch("benchmark_collect.utc_now", side_effect=[started, completed, receipt]):
                saved = collect.collect(self.store, "ecb", "2024-01-01", "2024-01-31",
                                        input_file=imported if mode == "import" else None,
                                        fetch=lambda *a, **k: invented_ecb_csv())
            self.assertEqual(saved["retrieved_at"], completed)
            self.assertTrue(all(r["retrieved_at"] == completed for r in saved["observations"]))
            self.assert_code("as_of_unavailable", data.select_snapshot, self.store, self.ecb["id"], as_of="2024-02-01T09:00:30Z")
            self.assertEqual(api.latest_refresh(self.store, "ecb")["attempted_at"], receipt)
            self.assertIsNone(api.latest_refresh(self.store, "ecb", as_of="2024-02-01T09:01:30Z"))
        with patch("benchmark_collect.utc_now", side_effect=["2024-02-02T09:00:00Z", "2024-02-02T09:01:00Z"]):
            self.assert_code("upstream_fetch_failed", collect.collect, self.store, "ecb", "2024-01-01", "2024-01-31",
                             fetch=lambda *a, **k: (_ for _ in ()).throw(data.BenchmarkError("upstream_fetch_failed", "Invented bounded failure.", 502)))
        self.assertEqual(api.latest_refresh(self.store, "ecb")["attempted_at"], "2024-02-02T09:01:00Z")

    def test_as_of_response_excludes_refresh_results_after_cutoff(self):
        saved = self.snapshot("2024-02-01T09:00:00Z")
        collect.record_attempt(self.store, "ecb", "2024-03-01T09:00:00Z", "fetch-failed", "upstream-fetch-failed", None)
        uri = "/v1/series/ecb-jpy-per-eur/observations?start=2024-01-01&end=2024-01-31&as_of=2024-02-15T00:00:00Z"
        status, _, body = api.handle_request("GET", uri, self.store)
        self.assertEqual(status, 200)
        self.assertEqual(body["vintage_status"], "known-at-cutoff")
        self.assertIsNone(body["refresh_status"])
        collect.record_attempt(self.store, "ecb", "2024-02-01T09:01:00Z", "succeeded", "refresh-complete", saved["id"])
        status, _, body = api.handle_request("GET", uri, self.store)
        self.assertEqual(status, 200)
        self.assertEqual(body["refresh_status"]["status"], "succeeded")
        self.assertEqual(body["refresh_status"]["attempted_at"], "2024-02-01T09:01:00Z")
        self.assertEqual(api.latest_refresh(self.store, "ecb")["status"], "fetch-failed")

    def test_as_of_rejects_invalid_timestamps_before_snapshot_selection(self):
        saved = self.snapshot("2024-02-01T09:00:00Z")
        invalid = ("2024-02-15T00:00:00+00:99", "2024-01-31T00:00:00+00:99",
                   "2024-02-15T00:00:00+24:00", "2024-02-15 00:00:00Z",
                   "20240215T000000Z", "2024-02-30T00:00:00Z",
                   "0001-01-01T00:00:00+01:00", "9999-12-31T23:59:59-01:00")
        for value in invalid:
            with self.subTest(as_of=value):
                self.assert_code("invalid_timestamp", data.timestamp, value)
                query = urlencode({"start": "2024-01-01", "end": "2024-01-31", "as_of": value})
                status, headers, body = api.handle_request("GET", "/v1/series/ecb-jpy-per-eur/observations?" + query, self.store)
                self.assertEqual((status, body["code"]), (400, "invalid_timestamp"))
                self.assertTrue(headers["Content-Type"].startswith("application/problem+json"))
        equivalent = "2024-02-01T18:00:00+09:00"
        self.assertEqual(data.timestamp(equivalent), data.timestamp(saved["retrieved_at"]))
        query = urlencode({"start": "2024-01-01", "end": "2024-01-31", "as_of": equivalent})
        status, _, body = api.handle_request("GET", "/v1/series/ecb-jpy-per-eur/observations?" + query, self.store)
        self.assertEqual((status, body["snapshot_id"]), (200, saved["id"]))

    def test_snapshot_and_csv_integrity_and_no_overwrite(self):
        snapshot = self.snapshot("2024-02-01T09:00:00Z")
        folder = self.store / "snapshots" / snapshot["id"]
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in folder.iterdir()}
        data.store_snapshot(self.store, snapshot)
        self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in folder.iterdir()})
        changed = copy.deepcopy(snapshot)
        changed["observations"][0]["value"] = "999"
        self.assert_code("immutable_snapshot_conflict", data.store_snapshot, self.store, changed)
        (folder / "observations.csv").write_bytes(b"corrupt\n")
        self.assert_code("snapshot_integrity_failed", data.load_snapshot, self.store, snapshot["id"])

    def test_outage_preserves_last_good_and_redacts_credentials(self):
        good = collect.collect(self.store, "ecb", "2024-01-01", "2024-01-31", fetch=lambda *a, **k: invented_ecb_csv(), now="2024-02-01T09:00:00Z")
        before = {str(p.relative_to(self.store)): p.read_bytes() for p in (self.store / "snapshots").rglob("*") if p.is_file()}
        secret = "inventedCredentialForTestOnly"
        with patch("benchmark_collect.build_opener") as opener:
            opener.return_value.open.side_effect = URLError("provider URL " + "app" + "Id=" + secret)
            self.assert_code("upstream_fetch_failed", collect.collect, self.store, "ecb", "2024-01-01", "2024-01-31", now="2024-02-02T09:00:00Z")
        self.assertEqual(before, {str(p.relative_to(self.store)): p.read_bytes() for p in (self.store / "snapshots").rglob("*") if p.is_file()})
        self.assertEqual(data.select_snapshot(self.store, self.ecb["id"])["id"], good["id"])
        failure = api.latest_refresh(self.store, "ecb")
        self.assertEqual(failure["status"], "fetch-failed")
        self.assertNotIn(secret.encode(), b"".join(p.read_bytes() for p in self.store.rglob("*") if p.is_file()))

    def test_partial_month_and_rebase_reject_changes(self):
        fixture = data.load_catalog(ROOT / "benchmarks/fixtures")["series"][0]
        prior = data.observation(fixture, "2024-01", "100", "2024-04-01T00:00:00Z", origin="synthetic", status="synthetic")
        current = data.observation(fixture, "2024-02", "110", "2024-04-01T00:00:00Z", origin="synthetic", status="synthetic")
        self.assertEqual(data.percentage_change(current, prior), "10.0")
        current["period_completeness"] = "partial"
        self.assert_code("partial_period", data.percentage_change, current, prior)
        current["period_completeness"] = "complete"
        current["index_base"] = "invented2025=100"
        self.assert_code("incomparable_observations", data.percentage_change, current, prior)
        fixture_catalog = data.load_catalog(ROOT / "benchmarks/fixtures")
        incomplete = data.observation(fixture, "2024-02", "105", "2024-02-15T00:00:00Z", origin="synthetic", status="synthetic")
        self.assert_code("future_observation_period", data.make_snapshot, fixture_catalog, [incomplete], "2024-02-15T00:00:00Z", data_class="synthetic", series_ids=[fixture["id"]], capture_method="invented fixture")
        partial = data.observation(fixture, "2024-02", "105", "2024-02-15T00:00:00Z", origin="synthetic", status="synthetic", completeness="partial", observed_through="2024-02-15")
        valid = data.make_snapshot(fixture_catalog, [partial], "2024-02-15T00:00:00Z", data_class="synthetic", series_ids=[fixture["id"]], capture_method="invented fixture")
        self.assertEqual(valid["observations"][0]["period_end"], "2024-02-15")

    def test_reversed_fx_quote_is_rejected(self):
        rows = collect.parse_ecb(invented_ecb_csv(), collect.selected(self.catalog, "ecb"), "2024-02-01T00:00:00Z", "https://data.ecb.europa.eu/", "2024-01-01", "2024-01-31")
        crosses = collect.derive_ecb_crosses(self.catalog, rows, "2024-02-01T00:00:00Z")
        self.assertEqual(next(r for r in crosses if r["series_id"] == "project-jpy-per-usd")["value"], "120")
        wrong = invented_ecb_csv().replace(b",EUR,SP00", b",JPY,SP00")
        self.assert_code("fx_quote_mismatch", collect.parse_ecb, wrong, collect.selected(self.catalog, "ecb"), "2024-02-01T00:00:00Z", "https://data.ecb.europa.eu/", "2024-01-01", "2024-01-31")
        rows[0]["value"] = "0"
        self.assert_code("invalid_fx_rate", collect.derive_ecb_crosses, self.catalog, rows, "2024-02-01T00:00:00Z")

    def test_derived_inputs_and_formula_are_independently_verified(self):
        snapshot = collect.collect(self.store, "ecb", "2024-01-01", "2024-01-31", fetch=lambda *a, **k: invented_ecb_csv(), now="2024-02-01T09:00:00Z")
        derived = next(r for r in snapshot["observations"] if r["origin"] == "derived")
        self.assertTrue(all(r["snapshot_id"] == snapshot["id"] for r in derived["inputs"]))
        changed = copy.deepcopy(snapshot)
        next(r for r in changed["observations"] if r["origin"] == "derived")["value"] = "123"
        self.assert_code("invalid_derivation", data.validate_snapshot, changed)
        changed = copy.deepcopy(snapshot)
        next(r for r in changed["observations"] if r["origin"] == "derived")["inputs"][0]["snapshot_id"] = "not-this-snapshot"
        self.assert_code("missing_derivation", data.validate_snapshot, changed)

    def test_public_origin_cannot_bypass_frozen_series_kind(self):
        saved = collect.collect(self.store, "ecb", "2024-01-01", "2024-01-31", fetch=lambda *a, **k: invented_ecb_csv(), now="2024-02-01T09:00:00Z")
        changed = copy.deepcopy(saved)
        derived = next(r for r in changed["observations"] if r["origin"] == "derived")
        derived.update(origin="original", value="999", inputs=[], transformation=None)
        self.assert_code("invalid_derivation", data.validate_snapshot, changed)
        changed = copy.deepcopy(saved)
        next(r for r in changed["observations"] if r["origin"] == "original")["origin"] = "derived"
        self.assert_code("invalid_derivation", data.validate_snapshot, changed)

    def test_credential_metadata_is_rejected(self):
        snapshot = self.snapshot("2024-02-01T09:00:00Z")
        changed = copy.deepcopy(snapshot)
        changed["observations"][0]["source_url"] += "?" + "app" + "Id=" + "invented-only"
        self.assert_code("unsafe_metadata", data.validate_snapshot, changed)
        self.assert_code("unsafe_metadata", data.reject_secrets, {"api" + "_key": "invented-only"})
        self.assert_code("unsafe_metadata", data.safe_public_url, "https://" + "10.0.0.1" + "/source")
        status, _, body = api.handle_request("GET", "/v1/datasets?" + "app" + "Id=never-copy-this", self.store)
        self.assertEqual(status, 400)
        self.assertNotIn("never-copy-this", json.dumps(body))

    def test_rights_gate_blocks_before_fetch(self):
        with patch("benchmark_collect.fetch_bytes") as fetch:
            self.assert_code("redistribution_not_permitted", collect.collect, self.store, "boj", "2024-01-01", "2024-02-29", fetch=fetch, now="2024-03-01T00:00:00Z")
            fetch.assert_not_called()
        self.assertEqual(data.snapshots(self.store), [])
        status, _, body = api.handle_request("GET", "/v1/series/boj-domestic-producer-price/observations?start=2024-01-01&end=2024-02-29", self.store)
        self.assertEqual((status, body["code"]), (403, "redistribution_not_permitted"))

    def test_empty_result_is_not_failed_fetch_or_zero(self):
        good = collect.collect(self.store, "ecb", "2024-01-01", "2024-01-31", fetch=lambda *a, **k: invented_ecb_csv(), now="2024-02-01T00:00:00Z")
        self.assert_code("no_observations", collect.collect, self.store, "ecb", "2024-02-01", "2024-02-29", fetch=lambda *a, **k: invented_ecb_csv(), now="2024-03-01T00:00:00Z")
        self.assertEqual(data.select_snapshot(self.store, self.ecb["id"])["id"], good["id"])
        status, _, result = api.handle_request("GET", "/v1/series/ecb-jpy-per-eur/observations?start=2024-02-01&end=2024-02-29", self.store)
        self.assertEqual(status, 200)
        self.assertEqual(result["data"], [])
        self.assertEqual(result["coverage"]["status"], "no-observations")
        self.assertEqual(result["refresh_status"]["code"], "no-observations")

    def test_api_contract_pagination_errors_and_no_provider_calls(self):
        saved = collect.collect(self.store, "ecb", "2024-01-01", "2024-01-31", fetch=lambda *a, **k: invented_ecb_csv(), now="2024-02-01T09:00:00Z")
        uri = "/v1/series/ecb-jpy-per-eur/observations?start=2024-01-01&end=2024-01-31&limit=1"
        with patch("benchmark_collect.fetch_bytes", side_effect=AssertionError("API must not refresh")):
            status, headers, body = api.handle_request("GET", uri, self.store, now="2024-03-01T00:00:00Z")
            self.assertEqual(status, 200)
            data.validate_named(body, "api", "ObservationsResponse")
            self.assertEqual(body["pagination"], {"offset": 0, "limit": 1, "total": 2, "next_offset": 1})
            self.assertEqual(body["freshness"]["status"], "stale")
            self.assertEqual(body["snapshot_id"], saved["id"])
            self.assertEqual(api.handle_request("GET", uri + "&offset=1", self.store)[2]["pagination"]["next_offset"], None)
        bad_requests = [("POST", "/v1/datasets", 405), ("GET", uri + "&limit=2", 400),
                        ("GET", uri.replace("limit=1", "limit=501"), 400), ("GET", uri.replace("2024-01-31", "2036-01-31"), 400),
                        ("GET", "/v1/series/ecb-jpy-per-eur/observations", 400), ("GET", "/v1/snapshots/..", 404)]
        for method, request, expected in bad_requests:
            status, headers, body = api.handle_request(method, request, self.store)
            self.assertEqual(status, expected)
            self.assertTrue(headers["Content-Type"].startswith("application/problem+json"))
            data.validate_named(body, "api", "Problem")

    def test_all_registered_openapi_routes_match_schema(self):
        summary = api.validate_openapi(ROOT / "benchmarks")
        self.assertEqual(summary["routes"], 4)
        self.assertEqual(summary["openapi"], "3.1.2")
        data.check_inventory(ROOT / "benchmarks")
        actual = data.snapshots(ROOT / "benchmarks")
        self.assertEqual({s["data_class"] for s in actual}, {"public"})
        self.assertTrue(all(s["knowledge_basis"] == "retrieval-time" for s in actual))

    def test_synthetic_fixture_never_fills_public_gap(self):
        store = ROOT / "benchmarks/fixtures"
        first = data.select_snapshot(store, "demo-monthly-index", data_class="synthetic", as_of="2024-03-15T00:00:00Z")
        last = data.select_snapshot(store, "demo-monthly-index", data_class="synthetic")
        self.assertNotEqual(first["id"], last["id"])
        self.assertEqual(first["observations"][0]["value"], "100.0")
        self.assertEqual(last["observations"][0]["value"], "99.0")
        self.assert_code("snapshot_not_found", data.select_snapshot, store, "demo-monthly-index")
        status, _, body = api.handle_request("GET", "/v1/series/demo-monthly-index/observations?start=2024-02-01&end=2024-02-15&data_class=synthetic", store)
        self.assertEqual((status, body["data"]), (200, []))

    def test_worldbank_units_dates_and_selected_values(self):
        definitions = collect.selected(self.catalog, "worldbank")
        headers = ["", "Aluminum", "Copper", "Crude oil, Brent", "Liquefied natural gas, Japan"]
        rows = [["World Bank shaped synthetic fixture"], ["Updated on March 04, 2024"], headers,
                ["", "($/mt)", "($/mt)", "($/bbl)", "($/mmbtu)"], ["2024M02", "100", "200", "30", "4"]]
        parsed = collect.parse_worldbank(invented_xlsx(rows), definitions, "2024-03-05T00:00:00Z", "https://www.worldbank.org/", "2024-02-01", "2024-02-29")
        self.assertEqual(len(parsed), 4)
        self.assertTrue(all(r["currency"] == "USD" and r["release_date"] == "2024-03-04" and r["release_at"] is None for r in parsed))
        rows[3][1] = "(JPY/kg)"
        self.assert_code("unit_mismatch", collect.parse_worldbank, invented_xlsx(rows), definitions, "2024-03-05T00:00:00Z", "https://www.worldbank.org/", "2024-02-01", "2024-02-29")

    def test_configured_meti_and_boj_parsers_without_live_claim(self):
        definition = copy.deepcopy(next(s for s in self.catalog["series"] if s["id"] == "meti-transport-production-original"))
        definition["provider_series_id"] = "invented-code"
        config = {"worksheet": "Original", "header_row": 1, "code_column": 0, "label_column": 1,
                  "series_labels": {definition["id"]: "Invented transport fixture"}, "base_marker": "2020=100"}
        xlsx = invented_xlsx([["2020=100"], ["Code", "Industry", "2024-01", "2024-02"], ["invented-code", "Invented transport fixture", "100", "102"]], "Original")
        rows = collect.parse_meti(xlsx, [definition], "2024-03-01T00:00:00Z", "https://www.meti.go.jp/", "2024-01-01", "2024-02-29", config)
        self.assertEqual([r["value"] for r in rows], ["100", "102"])
        config["base_marker"] = "2025=100"
        self.assert_code("index_rebase", collect.parse_meti, xlsx, [definition], "2024-03-01T00:00:00Z", "https://www.meti.go.jp/", "2024-01-01", "2024-02-29", config)
        boj = collect.selected(self.catalog, "boj")
        raw = ("Series Code," + ",".join(s["provider_series_id"] for s in boj) + "\n2024/01,100,200\n").encode()
        rows = collect.parse_boj(raw, boj, "2024-03-01T00:00:00Z", "https://www.stat-search.boj.or.jp/", "2024-01-01", "2024-01-31")
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(s["adapter_status"] == "rights-gated" for s in boj))

    def test_estat_requires_complete_reviewed_classifications(self):
        definition = copy.deepcopy(next(s for s in self.catalog["series"] if s["id"] == "mhlw-hours-candidate"))
        definition.update(unit="invented hours", provider_series_id="invented-series")
        config = {"series": {definition["id"]: {"filters": {"cat01": "invented-class"}, "unit": "invented hours"}}}
        response = {"GET_STATS_DATA": {"RESULT": {"STATUS": 0}, "STATISTICAL_DATA": {"RESULT_INF": {"TOTAL_NUMBER": 1, "FROM_NUMBER": 1, "TO_NUMBER": 1}, "DATA_INF": {"VALUE": [{"@cat01": "invented-class", "@time": "2024000100", "@unit": "invented hours", "$": "10"}]}}}}
        rows = collect.parse_estat(json.dumps(response).encode(), [definition], "2024-03-01T00:00:00Z", "https://api.e-stat.go.jp/", "2024-01-01", "2024-01-31", config)
        self.assertEqual(rows[0]["value"], "10")
        response["GET_STATS_DATA"]["STATISTICAL_DATA"]["RESULT_INF"]["TOTAL_NUMBER"] = 2
        self.assert_code("upstream_pagination_required", collect.parse_estat, json.dumps(response).encode(), [definition], "2024-03-01T00:00:00Z", "https://api.e-stat.go.jp/", "2024-01-01", "2024-01-31", config)

    def test_real_local_http_serves_only_validated_gets(self):
        self.snapshot("2024-02-01T00:00:00Z")
        server = ThreadingHTTPServer(("127.0.0.1", 0), api.make_handler(self.store))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            connection = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
            connection.request("GET", "/v1/datasets")
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            data.validate_named(json.loads(response.read()), "api", "Datasets")
            connection.close()
            connection = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
            connection.request("POST", "/v1/datasets")
            response = connection.getresponse()
            self.assertEqual(response.status, 405)
            self.assertTrue(response.getheader("Content-Type").startswith("application/problem+json"))
            data.validate_named(json.loads(response.read()), "api", "Problem")
            connection.close()
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
