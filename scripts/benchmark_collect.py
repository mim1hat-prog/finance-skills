"""Explicit public-only benchmark refresh/import. No background runner or company connections."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from xml.etree import ElementTree as ET
import zipfile

from benchmark_data import (BenchmarkError, DEFAULT_STORE, coverage, day, digest, identifier, json_bytes,
                            load_catalog, make_snapshot, number, observation, reject_secrets,
                            safe_public_url, store_snapshot, timestamp, utc_now, validate_named)

MAX_DOWNLOAD = 8_000_000
MAX_XLSX_EXPANDED = 40_000_000
HOSTS = {"ecb": {"data-api.ecb.europa.eu"}, "worldbank": {"thedocs.worldbank.org"},
         "boj": {"www.stat-search.boj.or.jp"}, "meti": {"www.meti.go.jp"}, "estat": {"api.e-stat.go.jp"}}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
MISSING = {"", "...", "…", "NA", "N/A", ":", "-"}


class PublicRedirects(HTTPRedirectHandler):
    def __init__(self, allowed):
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urlsplit(newurl)
        if parsed.scheme != "https" or parsed.hostname not in self.allowed or parsed.username or parsed.password:
            raise BenchmarkError("redirect_not_allowed", "The provider redirected outside its approved public host.", 502)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_bytes(url: str, adapter: str, *, allow_credential_query: bool = False) -> bytes:
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in HOSTS[adapter] or parts.username or parts.password:
        raise BenchmarkError("source_not_allowed", "The source is not an approved public provider endpoint.")
    if not allow_credential_query:
        safe_public_url(url)
    try:
        opener = build_opener(PublicRedirects(HOSTS[adapter]))
        with opener.open(Request(url, headers={"User-Agent": "finance-skills-public-benchmarks/1.0", "Accept": "*/*"}), timeout=25) as response:
            data = response.read(MAX_DOWNLOAD + 1)
    except BenchmarkError:
        raise
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        # Exception strings can contain a credentialed request URL. Never persist them.
        raise BenchmarkError("upstream_fetch_failed", "The public provider request failed; the last good snapshot is retained.", 502) from None
    if len(data) > MAX_DOWNLOAD:
        raise BenchmarkError("upstream_too_large", "The provider response exceeds the configured download bound.", 502)
    if not data:
        raise BenchmarkError("upstream_empty_response", "The provider returned an empty response; this is not zero activity.", 502)
    return data


def selected(catalog: dict, adapter: str) -> list[dict]:
    return [s for s in catalog["series"] if s["adapter"] == adapter and s["series_kind"] == "original"]


def permitted(series: list[dict]) -> None:
    if not series:
        raise BenchmarkError("unknown_adapter", "No series are configured for this adapter.")
    if any(s["rights"]["redistribution"] != "permitted" for s in series):
        raise BenchmarkError("redistribution_not_permitted", "The selected series require a rights review or permission before mirroring.", 403)
    if any(s["adapter_status"] in {"requires-configuration", "needs-source-validation"} or not s["provider_series_id"] for s in series):
        raise BenchmarkError("configuration_required", "Verify the exact source file/table, series, units and classification before collecting this provider.", 409)


def within(period: str, start: str, end: str) -> bool:
    point = day(period if len(period) == 10 else period + "-01")
    return day(start).replace(day=1) <= point <= day(end) if len(period) == 7 else day(start) <= point <= day(end)


def parse_ecb(data: bytes, series: list[dict], retrieved_at: str, source_url: str, start: str, end: str) -> list[dict]:
    try:
        reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    except UnicodeError as exc:
        raise BenchmarkError("source_format_changed", "ECB response is not UTF-8 CSV.", 502) from exc
    required = {"KEY", "FREQ", "CURRENCY", "CURRENCY_DENOM", "EXR_TYPE", "EXR_SUFFIX", "TIME_PERIOD", "OBS_VALUE", "UNIT", "UNIT_MULT"}
    if not required <= set(reader.fieldnames or []) or len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise BenchmarkError("source_format_changed", "ECB CSV is missing its declared series or value columns.", 502)
    mapping = {s["provider_series_id"]: s for s in series}
    result = []
    for row in reader:
        if None in row or any(v is None for v in row.values()):
            raise BenchmarkError("source_format_changed", "ECB CSV record width differs from the header.", 502)
        definition = mapping.get(row.get("KEY"))
        if definition is None:
            raise BenchmarkError("unexpected_series", "ECB returned a series outside the requested inventory.", 502)
        if any(row.get(k) != v for k, v in {"FREQ": "D", "CURRENCY_DENOM": "EUR", "EXR_TYPE": "SP00", "EXR_SUFFIX": "A", "UNIT_MULT": "0", "CURRENCY": definition["quote_currency"], "UNIT": definition["quote_currency"]}.items()):
            raise BenchmarkError("fx_quote_mismatch", "ECB quote direction, currency or multiplier differs from the declared series.", 502)
        if definition["base_currency"] != "EUR" or definition["unit"] != definition["quote_currency"] + " per EUR":
            raise BenchmarkError("fx_quote_mismatch", "The local series definition reverses or mislabels the provider quote.")
        if row["OBS_VALUE"] in MISSING:
            continue
        if within(row["TIME_PERIOD"], start, end):
            if number(row["OBS_VALUE"]) <= 0:
                raise BenchmarkError("invalid_fx_rate", "A reference FX quote must be positive.", 502)
            status = "provisional" if row.get("OBS_STATUS") == "P" else "published"
            result.append(observation(definition, row["TIME_PERIOD"], row["OBS_VALUE"], retrieved_at, source_url=source_url, status=status))
    return result


def derive_ecb_crosses(catalog: dict, rows: list[dict], retrieved_at: str) -> list[dict]:
    definitions = {s["id"]: s for s in catalog["series"]}
    by_key = {(r["series_id"], r["observation_period"]): r for r in rows}
    output = []
    for numerator in rows:
        if numerator["series_id"] != "ecb-jpy-per-eur":
            continue
        for ccy in ("usd", "cny", "thb"):
            denominator = by_key.get(("ecb-" + ccy + "-per-eur", numerator["observation_period"]))
            if denominator is None:
                continue  # No interpolation, carry-forward or substitute quote.
            if numerator["period_completeness"] != "complete" or denominator["period_completeness"] != "complete":
                raise BenchmarkError("partial_period", "Cross-rate inputs must cover the same complete observation date.")
            if numerator["unit"] != "JPY per EUR" or denominator["unit"] != ccy.upper() + " per EUR":
                raise BenchmarkError("fx_quote_mismatch", "Cross-rate inputs have incompatible quote directions.")
            if number(numerator["value"]) <= 0 or number(denominator["value"]) <= 0:
                raise BenchmarkError("invalid_fx_rate", "Cross-rate inputs must be positive.")
            with localcontext() as ctx:
                ctx.prec = 40
                value = format(number(numerator["value"]) / number(denominator["value"]), "f")
            definition = definitions["project-jpy-per-" + ccy]
            refs = [{"series_id": r["series_id"], "observation_period": r["observation_period"], "snapshot_id": r["snapshot_id"]} for r in (numerator, denominator)]
            output.append(observation(definition, numerator["observation_period"], value, retrieved_at,
                                      origin="derived", inputs=refs,
                                      transformation={"id": "ecb-jpy-cross", "version": "1.0.0",
                                                      "formula": "JPY per EUR divided by " + ccy.upper() + " per EUR; 40-digit Decimal precision"}))
    return output


def read_xlsx(data: bytes, sheet_name: str) -> list[list[str]]:
    """Read stored XML values only; no macros, formulas, external links or Excel execution."""
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise BenchmarkError("source_format_changed", "Expected a valid XLSX file.", 502) from exc
    with archive:
        members = archive.infolist()
        if len(members) > 3000 or sum(i.file_size for i in members) > MAX_XLSX_EXPANDED or any(i.flag_bits & 1 for i in members):
            raise BenchmarkError("source_too_large", "Workbook exceeds the bounded readable XML inventory.", 502)
        def xml(name):
            payload = archive.read(name)
            if b"<!DOCTYPE" in payload or b"<!ENTITY" in payload:
                raise BenchmarkError("unsafe_workbook_xml", "XML entity definitions are not supported.", 502)
            return ET.fromstring(payload)
        try:
            workbook = xml("xl/workbook.xml")
            links = {e.attrib["Id"]: e.attrib["Target"] for e in xml("xl/_rels/workbook.xml.rels")}
            sheet = next((e for e in workbook.findall("m:sheets/m:sheet", NS) if e.attrib.get("name") == sheet_name), None)
            if sheet is None:
                raise BenchmarkError("source_format_changed", "Expected worksheet was not found.", 502)
            target = links[sheet.attrib["{" + NS["r"] + "}id"]]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            if ".." in target.split("/") or "\\" in target or not target.startswith("xl/"):
                raise BenchmarkError("unsafe_workbook_xml", "Worksheet target is outside the workbook XML scope.", 502)
            strings = []
            if "xl/sharedStrings.xml" in archive.namelist():
                strings = ["".join(t.text or "" for t in item.iter("{" + NS["m"] + "}t")) for item in xml("xl/sharedStrings.xml")]
            rows = []
            for row in xml(target).findall("m:sheetData/m:row", NS):
                cells = {}
                for cell in row.findall("m:c", NS):
                    has_formula = cell.find("m:f", NS) is not None
                    match = re.fullmatch(r"([A-Z]+)[1-9][0-9]*", cell.attrib.get("r", ""))
                    if not match:
                        raise BenchmarkError("source_format_changed", "Worksheet cell address is invalid.", 502)
                    col = 0
                    for char in match[1]:
                        col = col * 26 + ord(char) - 64
                    if col > 500:
                        raise BenchmarkError("source_too_large", "Workbook has too many columns.", 502)
                    value = cell.findtext("m:v", "", NS)
                    kind = cell.attrib.get("t")
                    if kind == "s":
                        value = strings[int(value)]
                    elif kind == "inlineStr":
                        value = "".join(t.text or "" for t in cell.iter("{" + NS["m"] + "}t"))
                    elif kind == "e":
                        value = "!STORED-CELL-ERROR!"
                    if has_formula:
                        value = "!UNVERIFIED-FORMULA-CACHE!"
                    cells[col - 1] = value
                rows.append([cells.get(i, "") for i in range(max(cells, default=-1) + 1)])
                if len(rows) > 10000:
                    raise BenchmarkError("source_too_large", "Workbook has too many rows.", 502)
            return rows
        except (KeyError, ValueError, ET.ParseError, IndexError) as exc:
            if isinstance(exc, BenchmarkError):
                raise
            raise BenchmarkError("source_format_changed", "Workbook XML structure is not supported.", 502) from None


def source_decimal(value: str) -> str:
    try:
        converted = Decimal(value)
    except (InvalidOperation, ValueError):
        raise BenchmarkError("source_value_error", "A published numeric cell could not be parsed.", 502) from None
    if not converted.is_finite():
        raise BenchmarkError("source_value_error", "Published values must be finite.", 502)
    result = format(converted, "f")
    number(result)
    return result


def parse_worldbank(data: bytes, series: list[dict], retrieved_at: str, source_url: str, start: str, end: str) -> list[dict]:
    table = read_xlsx(data, "Monthly Prices")
    expected_units = {"USD per metric tonne": "($/mt)", "USD per barrel": "($/bbl)", "USD per million Btu": "($/mmbtu)"}
    matches = [i for i, row in enumerate(table[:20]) if all(s["provider_series_id"] in row for s in series)]
    if len(matches) != 1 or matches[0] + 1 >= len(table):
        raise BenchmarkError("source_format_changed", "Pink Sheet column headings are missing or ambiguous.", 502)
    header = table[matches[0]]
    units = table[matches[0] + 1]
    columns = {}
    for s in series:
        if header.count(s["provider_series_id"]) != 1:
            raise BenchmarkError("source_format_changed", "Pink Sheet series heading is duplicated.", 502)
        col = header.index(s["provider_series_id"])
        if col >= len(units) or units[col].strip() != expected_units.get(s["unit"]) or s["currency"] != "USD":
            raise BenchmarkError("unit_mismatch", "Pink Sheet unit or currency differs from the declared series.", 502)
        columns[s["id"]] = col
    release_date = None
    for row in table[:matches[0]]:
        if row and row[0].startswith("Updated on "):
            try:
                release_date = datetime.strptime(row[0][11:].strip(), "%B %d, %Y").date().isoformat()
            except ValueError:
                raise BenchmarkError("source_format_changed", "Pink Sheet update date format changed.", 502) from None
    result = []
    for row in table[matches[0] + 2:]:
        if not row or not re.fullmatch(r"\d{4}M\d{2}", row[0]):
            continue
        period = row[0].replace("M", "-")
        if not within(period, start, end):
            continue
        for s in series:
            col = columns[s["id"]]
            value = row[col].strip() if col < len(row) else ""
            if value in MISSING:
                continue
            result.append(observation(s, period, source_decimal(value), retrieved_at, release_date=release_date, source_url=source_url))
    return result


def parse_boj(data: bytes, series: list[dict], retrieved_at: str, source_url: str, start: str, end: str) -> list[dict]:
    """Configured BOJ column layout; rights gate is enforced before acquisition/storage."""
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError:
        text = data.decode("cp932")
    table = list(csv.reader(io.StringIO(text)))
    keys = [s["provider_series_id"].split("'", 1)[-1] for s in series]
    headers = [i for i, row in enumerate(table) if all(any(cell.split("'", 1)[-1] == key for cell in row) for key in keys)]
    if len(headers) != 1:
        raise BenchmarkError("source_format_changed", "BOJ series-code header is missing or ambiguous.", 502)
    header = table[headers[0]]
    columns = {s["id"]: next(i for i, cell in enumerate(header) if cell.split("'", 1)[-1] == key) for s, key in zip(series, keys)}
    result = []
    for row in table[headers[0] + 1:]:
        if not row or not re.fullmatch(r"\d{4}[/-]\d{2}", row[0]):
            continue
        period = row[0].replace("/", "-")
        if not within(period, start, end):
            continue
        for s in series:
            col = columns[s["id"]]
            value = row[col].strip() if col < len(row) else ""
            if value not in MISSING:
                result.append(observation(s, period, source_decimal(value), retrieved_at, source_url=source_url))
    return result


def parse_meti(data: bytes, series: list[dict], retrieved_at: str, source_url: str, start: str, end: str, config: dict) -> list[dict]:
    """Use an explicitly verified METI workbook layout; no guessed row codes or URLs."""
    if set(config) != {"worksheet", "header_row", "code_column", "label_column", "series_labels", "base_marker"}:
        raise BenchmarkError("configuration_required", "METI import needs the exact worksheet/header/code/label/base configuration.")
    table = read_xlsx(data, config["worksheet"])
    index = config["header_row"]
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < min(100, len(table)):
        raise BenchmarkError("configuration_required", "METI header_row must be an observed zero-based row index.")
    if not config["base_marker"] or not any(config["base_marker"] in cell for row in table[:index + 1] for cell in row):
        raise BenchmarkError("index_rebase", "The configured index-base marker is not present; review the provider revision.", 502)
    headers = table[index]
    period_columns = {}
    for i, value in enumerate(headers):
        if re.fullmatch(r"\d{4}[-/]\d{2}", value):
            period_columns[i] = value.replace("/", "-")
        elif re.fullmatch(r"\d{6}", value):
            period_columns[i] = value[:4] + "-" + value[4:]
    if not period_columns:
        raise BenchmarkError("source_format_changed", "METI monthly period columns were not found.", 502)
    result = []
    for s in series:
        code_col, label_col = config["code_column"], config["label_column"]
        if any(not isinstance(v, int) or isinstance(v, bool) or not 0 <= v < 500 for v in (code_col, label_col)):
            raise BenchmarkError("configuration_required", "METI code and label columns must be explicit zero-based indices.")
        matching = [r for r in table[index + 1:] if code_col < len(r) and r[code_col] == s["provider_series_id"]]
        if len(matching) != 1:
            raise BenchmarkError("source_format_changed", "METI configured row code is missing or duplicated.", 502)
        row = matching[0]
        if label_col >= len(row) or row[label_col] != config["series_labels"].get(s["id"]):
            raise BenchmarkError("source_format_changed", "METI industry label does not match its verified row code.", 502)
        if s["index_base"] != config["base_marker"]:
            raise BenchmarkError("index_rebase", "METI base marker differs from the series definition.", 502)
        for col, period in period_columns.items():
            value = row[col].strip() if col < len(row) else ""
            if value not in MISSING and within(period, start, end):
                result.append(observation(s, period, source_decimal(value), retrieved_at, source_url=source_url))
    return result


def parse_estat(data: bytes, series: list[dict], retrieved_at: str, source_url: str, start: str, end: str, config: dict) -> list[dict]:
    document = json.loads(data)
    root = document.get("GET_STATS_DATA", {})
    if str(root.get("RESULT", {}).get("STATUS")) != "0":
        raise BenchmarkError("upstream_fetch_failed", "e-Stat did not report a successful statistics response.", 502)
    statistical = root.get("STATISTICAL_DATA", {})
    values = statistical.get("DATA_INF", {}).get("VALUE", [])
    values = values if isinstance(values, list) else [values]
    counts = statistical.get("RESULT_INF", {})
    if counts.get("TOTAL_NUMBER") != len(values) or counts.get("FROM_NUMBER") != (1 if values else 0) or counts.get("TO_NUMBER") != len(values):
        raise BenchmarkError("upstream_pagination_required", "The configured e-Stat response is incomplete or lacks reviewed pagination counts; no partial snapshot was saved.", 502)
    result = []
    for s in series:
        setting = config.get("series", {}).get(s["id"])
        if not setting or set(setting) != {"filters", "unit"} or not setting["filters"]:
            raise BenchmarkError("configuration_required", "e-Stat requires exact reviewed classification filters and unit for every series.")
        for value in values:
            if any(value.get("@" + key) != expected for key, expected in setting["filters"].items()):
                continue
            raw_time = value.get("@time", "")
            if not re.fullmatch(r"\d{10}", raw_time) or raw_time[4:6] != "00":
                raise BenchmarkError("source_format_changed", "e-Stat monthly time classification must be reviewed before conversion.", 502)
            period = raw_time[:4] + "-" + raw_time[6:8]
            if raw_time[8:] != "00" or not within(period, start, end):
                continue
            if value.get("@unit") != setting["unit"] or s["unit"] != setting["unit"]:
                raise BenchmarkError("unit_mismatch", "e-Stat observation unit differs from the configured series.", 502)
            raw = value.get("$", "")
            if raw not in MISSING:
                result.append(observation(s, period, source_decimal(raw), retrieved_at, source_url=source_url))
    return result


def record_attempt(store: Path, adapter: str, attempted_at: str, status: str, code: str, snapshot_id: str | None) -> None:
    record = {"provider": adapter, "attempted_at": attempted_at, "status": status, "code": code, "snapshot_id": snapshot_id}
    validate_named(record, "api", "RefreshStatus")
    reject_secrets(record)
    folder = store / "refresh-status"
    if store.is_symlink() or folder.is_symlink():
        raise BenchmarkError("unsafe_storage", "Refresh status directory must not be a symlink.")
    folder.mkdir(parents=True, exist_ok=True)
    data = json_bytes(record)
    target = folder / (timestamp(attempted_at).strftime("%Y%m%dT%H%M%SZ").lower() + "-" + digest(data)[:16] + ".json")
    if target.is_symlink():
        raise BenchmarkError("unsafe_storage", "Refresh status file must not be a symlink.")
    if target.exists():
        if target.read_bytes() != data:
            raise BenchmarkError("immutable_status_conflict", "Existing refresh receipt differs; preserve it.", 409)
    else:
        with target.open("xb") as stream:
            stream.write(data)


def collect(store: Path, adapter: str, start: str, end: str, *, input_file: Path | None = None,
            config: dict | None = None, series_ids: list[str] | None = None, fetch=fetch_bytes, now: str | None = None) -> dict:
    if adapter not in HOSTS:
        raise BenchmarkError("unknown_adapter", "Select a registered public provider.")
    if day(end) < day(start) or (day(end) - day(start)).days > 3660:
        raise BenchmarkError("invalid_range", "Select an ordered date range of at most 3660 days.")
    at = now or utc_now()
    snapshot = None
    try:
        catalog = load_catalog(store)
        definitions = selected(catalog, adapter)
        if series_ids is not None:
            if not series_ids or len(set(series_ids)) != len(series_ids) or set(series_ids) - {s["id"] for s in definitions}:
                raise BenchmarkError("unknown_series", "Select registered original series belonging to this adapter.")
            definitions = [s for s in definitions if s["id"] in series_ids]
        permitted(definitions)
        source = definitions[0]["download_url"]
        if any(s["download_url"] != source for s in definitions):
            raise BenchmarkError("configuration_required", "This adapter needs one verified source file per invocation.")
        if adapter == "ecb":
            quotes = sorted({s["quote_currency"] for s in definitions})
            if not set(quotes) <= {"JPY", "USD", "CNY", "THB"}:
                raise BenchmarkError("configuration_required", "Only the reviewed ECB currency inventory is supported.")
            source = "https://data-api.ecb.europa.eu/service/data/EXR/D." + "+".join(quotes) + ".EUR.SP00.A?" + urlencode({"startPeriod": start, "endPeriod": end, "format": "csvdata"})
        request_url = source
        if adapter == "estat":
            if not config or not re.fullmatch(r"[0-9]{5,20}", str(config.get("stats_data_id", ""))):
                raise BenchmarkError("configuration_required", "Configure a verified e-Stat statistics table ID and exact classification filters.")
            if not input_file:
                application_id = os.environ.get("ESTAT_APP_ID")
                if not application_id:
                    raise BenchmarkError("configuration_required", "Set ESTAT_APP_ID in the local environment; do not save it in files or URLs.")
                source = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?" + urlencode({"statsDataId": config["stats_data_id"], "metaGetFlg": "Y", "cntGetFlg": "N", "limit": "100000"})
                request_url = source + "&" + urlencode({"appId": application_id})
        if input_file:
            if input_file.is_symlink() or not input_file.is_file() or input_file.stat().st_size > MAX_DOWNLOAD:
                raise BenchmarkError("invalid_input_file", "Use a bounded regular provider file.")
            data = input_file.read_bytes()
        else:
            data = fetch(request_url, adapter, allow_credential_query=adapter == "estat")
        # A request start is not evidence that its returned bytes were known then.
        # The explicit now override is only for deterministic local tests/imports.
        retrieved_at = now or utc_now()
        if timestamp(retrieved_at) < timestamp(at):
            raise BenchmarkError("clock_regression", "The completion clock precedes the request clock; no historical availability can be asserted.")
        if adapter == "ecb":
            rows = parse_ecb(data, definitions, retrieved_at, source, start, end)
            rows += derive_ecb_crosses(catalog, rows, retrieved_at)
        elif adapter == "worldbank":
            rows = parse_worldbank(data, definitions, retrieved_at, source, start, end)
        elif adapter == "boj":
            rows = parse_boj(data, definitions, retrieved_at, source, start, end)
        elif adapter == "meti":
            rows = parse_meti(data, definitions, retrieved_at, source, start, end, config or {})
        else:
            rows = parse_estat(data, definitions, retrieved_at, source, start, end, config or {})
        if not rows:
            raise BenchmarkError("no_observations", "The successful provider response contained no selected observations; the last good snapshot is retained.", 404)
        inventory = [s["id"] for s in definitions]
        inventory += sorted({r["series_id"] for r in rows} - set(inventory))
        if any(not any(r["series_id"] == s["id"] for r in rows) for s in definitions):
            raise BenchmarkError("incomplete_provider_coverage", "One or more requested series have no observations; the last good snapshot is retained.", 502)
        snapshot = make_snapshot(catalog, rows, retrieved_at, data_class="public", series_ids=inventory,
                                 capture_method=("Explicit imported provider file" if input_file else "Explicit provider HTTPS request") + "; adapter=" + adapter + "; source-sha256=" + digest(data))
        store_snapshot(store, snapshot)
        record_attempt(store, adapter, now or utc_now(), "succeeded", "refresh-complete", snapshot["id"])
        return snapshot
    except BenchmarkError as exc:
        status = "rights-blocked" if exc.code == "redistribution_not_permitted" else "configuration-required" if exc.code == "configuration_required" else "fetch-failed" if exc.code.startswith("upstream_") else "validation-failed"
        record_attempt(store, adapter, now or utc_now(), status, exc.code.replace("_", "-"), None)
        raise
    except (OSError, ValueError, KeyError, TypeError, UnicodeError):
        record_attempt(store, adapter, now or utc_now(), "validation-failed", "source-validation-failed", None)
        raise BenchmarkError("source_validation_failed", "The provider response or local snapshot could not be validated; no fallback value was supplied.", 502) from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE)
    parser.add_argument("--adapter", choices=sorted(HOSTS), required=True)
    parser.add_argument("--start", required=True, help="First observation date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Last observation date YYYY-MM-DD")
    parser.add_argument("--series", nargs="+", help="Optional exact original series IDs; use separate requests for distinct source files")
    parser.add_argument("--input", type=Path, help="Import an official provider file; still enforce source/rights metadata")
    parser.add_argument("--config", type=Path, help="Reviewed public METI/e-Stat layout/classification JSON; never credentials")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8")) if args.config else None
        if config is not None:
            reject_secrets(config)
        snapshot = collect(args.store, args.adapter, args.start, args.end, input_file=args.input, config=config, series_ids=args.series)
        print(json.dumps({"snapshot_id": snapshot["id"], "observations": len(snapshot["observations"]), "data_class": snapshot["data_class"]}))
        return 0
    except BenchmarkError as exc:
        print(json.dumps({"code": exc.code, "detail": exc.detail}), file=sys.stderr)
        return 1
    except (OSError, ValueError, UnicodeError):
        print(json.dumps({"code": "invalid_local_input", "detail": "A local public dataset or configuration file could not be read or validated."}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
