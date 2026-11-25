#!/usr/bin/env python3
"""Build and check the project research registry; network access is opt-in.

The registry records limited, concrete uses of evidence. A resolved source ID is
not a claim that a method is suitable for every dataset, nor a conformance badge.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Callable
from urllib.parse import parse_qsl, quote, urlsplit
from urllib.request import Request, urlopen


REGISTRY = Path("research/sources.json")
GENERATED = Path("research/README.md")
ID = re.compile(r"[a-z0-9]+(?:[-.][a-z0-9]+)*\Z")
GOOD_REVIEWS = {"reviewed", "reviewed-with-limitations", "carried-forward"}
BLOCKED_REVIEWS = {"unreviewed", "needs-review", "retracted", "superseded"}
SOURCE_TYPES = {"normative-standard", "empirical-research", "method-guide",
                "provider-documentation", "data-license", "software-reference",
                "project-design", "metadata-guidance"}
RIGHTS = {"allowed-with-conditions", "permission-required", "unknown", "not-applicable"}
SECRET_KEYS = {"appid", "apikey", "api_key", "api-key", "access_token", "token",
               "key", "secret", "password", "authorization", "client_secret"}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("expected a nonempty repository-relative POSIX path")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError("path must remain inside the repository")
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("path escapes repository through a link")
    return resolved


def _date(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    p = urlsplit(value)
    return (p.scheme == "https" and bool(p.netloc) and not p.username and not p.password
            and not any(k.lower() in SECRET_KEYS for k, _ in parse_qsl(p.query)))


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def _research_refs(value: Any):
    """Read explicitly declared IDs; prose is not treated as an API contract."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"researchIds", "research_ids"}:
                if isinstance(item, list):
                    yield from item
                else:
                    yield None
            elif key == "source_id":
                yield item
            else:
                yield from _research_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from _research_refs(item)


def _test_exists(root: Path, test_id: str) -> bool:
    filename, sep, symbol = test_id.partition("::")
    if not sep or not symbol:
        return False
    path = _path(root, filename)
    if not path.is_file() or path.suffix != ".py":
        return False
    tree = ast.parse(path.read_text(encoding="utf-8"))
    nodes = tree.body
    for part in symbol.split("."):
        node = next((n for n in nodes if isinstance(n, (ast.ClassDef, ast.FunctionDef,
                    ast.AsyncFunctionDef)) and n.name == part), None)
        if node is None:
            return False
        nodes = node.body
    return True


def validate(root: Path, *, check_generated: bool = True) -> dict[str, Any]:
    """Return a deterministic validation report; perform no network calls or writes."""
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    result = {"ok": False, "errors": errors, "warnings": warnings,
              "sourceCount": 0, "skillCount": 0}
    try:
        registry = _load(root / REGISTRY)
        catalog = _load(root / "catalog.json")
    except (OSError, ValueError) as exc:
        errors.append(f"Cannot load registry/catalog: {exc}")
        return result
    if not isinstance(registry, dict) or registry.get("schemaVersion") != 1:
        errors.append("research/sources.json: unsupported schemaVersion")
        return result
    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("research/sources.json: sources must be a nonempty list")
        return result
    rows = catalog.get("skills", []) if isinstance(catalog, dict) else []
    skill_names = {r.get("name") for r in rows if isinstance(r, dict)}
    result["sourceCount"], result["skillCount"] = len(sources), len(skill_names)
    by_id: dict[str, dict] = {}
    declared: dict[str, set[str]] = {name: set() for name in skill_names}
    upstreams = {}
    if any(isinstance(s, dict) and str(s.get("id", "")).startswith("upstream-") for s in sources):
        try:
            upstreams = {s["id"]: s for s in _load(root / "upstream.lock.json")["sources"]}
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"Cannot resolve pinned upstream research records: {exc}")
    for s in sources:
        if not isinstance(s, dict):
            errors.append("Source entry must be an object")
            continue
        sid = s.get("id")
        if not isinstance(sid, str) or not ID.fullmatch(sid):
            errors.append(f"Invalid source ID: {sid!r}")
            continue
        if sid in by_id:
            errors.append(f"Duplicate source ID: {sid}")
            continue
        by_id[sid] = s
        if sid.startswith("upstream-"):
            pinned = upstreams.get(sid.removeprefix("upstream-"))
            expected = (f"https://github.com/{pinned['repository']}/tree/{pinned['commit']}"
                        if pinned else None)
            if s.get("url") != expected:
                errors.append(f"{sid}: pinned upstream changed or is missing; review the source before release")
            mapped = {name for use in s.get("uses", []) for name in use.get("skills", [])}
            if pinned and mapped != set(pinned.get("appliedSkills", [])):
                errors.append(f"{sid}: affected skills differ from the pinned upstream review")
        for field in ("title", "publisher", "edition", "maintainerRole", "reviewNotes"):
            if not isinstance(s.get(field), str) or not s[field].strip():
                errors.append(f"{sid}: missing {field}")
        if s.get("type") not in SOURCE_TYPES:
            errors.append(f"{sid}: unknown source type")
        if not isinstance(s.get("authors"), list) or not s["authors"]:
            errors.append(f"{sid}: authors must identify author(s) or institutional publisher")
        if s.get("year") is not None and (not isinstance(s["year"], int) or not 1900 <= s["year"] <= 2100):
            errors.append(f"{sid}: year must be a publication year or null")
        for field in ("accessedOn", "lastReviewedOn"):
            if not _date(s.get(field)):
                errors.append(f"{sid}: invalid {field}")
        if not _url(s.get("url")):
            errors.append(f"{sid}: canonical URL must be public HTTPS without credentials")
        review = s.get("reviewStatus")
        if review not in GOOD_REVIEWS | BLOCKED_REVIEWS:
            errors.append(f"{sid}: unknown reviewStatus")
        integration = s.get("integrationStatus", "active")
        if integration not in {"active", "candidate"}:
            errors.append(f"{sid}: unknown integrationStatus")
        if integration == "candidate" and not s.get("candidateReason"):
            errors.append(f"{sid}: candidate requires a visible reason for exclusion")
        license_ = s.get("license", {})
        for field in ("name", "attribution", "notes"):
            if not isinstance(license_.get(field), str) or not license_[field].strip():
                errors.append(f"{sid}: license.{field} required")
        if not _url(license_.get("termsUrl")) or not _date(license_.get("checkedOn")):
            errors.append(f"{sid}: licence needs termsUrl and checkedOn")
        for field in ("rawRedistribution", "derivedRedistribution"):
            if license_.get(field) not in RIGHTS:
                errors.append(f"{sid}: license.{field} must be an explicit rights decision")
        updates = s.get("updates")
        if not isinstance(updates, list):
            errors.append(f"{sid}: updates must be a list, including [] when none were found")
            updates = []
        for update in updates:
            if not isinstance(update, dict) or not _url(update.get("url")):
                errors.append(f"{sid}: update needs a public notice URL")
                continue
            if update.get("kind") not in {"correction", "addendum", "retraction", "supersession", "expression-of-concern"}:
                errors.append(f"{sid}: unknown update kind")
            if not update.get("assessment"):
                errors.append(f"{sid}: update requires an impact assessment or explicit unresolved gap")
            if update.get("disposition") == "reviewed-no-method-change":
                if not _date(update.get("reviewedOn")):
                    errors.append(f"{sid}: reviewed update requires its actual review date")
            elif update.get("disposition") == "needs-review":
                if not _date(update.get("detectedOn")):
                    errors.append(f"{sid}: unresolved update requires detection date")
            else:
                errors.append(f"{sid}: unknown update disposition")
        uses = s.get("uses")
        if not isinstance(uses, list) or (not uses and integration == "active"):
            errors.append(f"{sid}: no concrete use; do not label an unused bibliography entry integrated")
            uses = []
        if integration == "candidate":
            if uses:
                errors.append(f"{sid}: candidate cannot declare active skill or implementation uses")
            warnings.append(f"{sid}: candidate excluded from active method support: {s.get('candidateReason', '')}")
        for index, use in enumerate(uses):
            label = f"{sid}.uses[{index}]"
            if not isinstance(use, dict):
                errors.append(f"{label}: use must be an object")
                continue
            for field in ("section", "purpose", "limits"):
                if not isinstance(use.get(field), str) or not use[field].strip():
                    errors.append(f"{label}: missing {field}")
            paths = use.get("paths", [])
            if not isinstance(paths, list) or not paths:
                errors.append(f"{label}: exact affected paths required")
                paths = []
            for value in paths:
                try:
                    if not _path(root, value).is_file():
                        errors.append(f"{label}: missing target {value}")
                except ValueError as exc:
                    errors.append(f"{label}: {exc}")
            for name in use.get("skills", []):
                if name not in skill_names:
                    errors.append(f"{label}: unknown skill {name}")
                else:
                    declared[name].add(sid)
                    if f"skills/{name}/SKILL.md" not in paths:
                        errors.append(f"{label}: named skill needs its exact SKILL.md path")
            for test in use.get("tests", []):
                try:
                    if not _test_exists(root, test):
                        errors.append(f"{label}: unresolved test {test}")
                except (OSError, ValueError, SyntaxError) as exc:
                    errors.append(f"{label}: invalid test {test}: {exc}")
            if use.get("distribution", "metadata-only") == "data-values":
                if any(license_.get(field) != "allowed-with-conditions" for field in ("rawRedistribution", "derivedRedistribution")):
                    errors.append(f"{label}: data-values use has unresolved redistribution rights")
        if integration == "active" and uses and review not in GOOD_REVIEWS:
            errors.append(f"{sid}: referenced source is {review}; review affected skills before release")
        for update in updates:
            if not isinstance(update, dict):
                continue
            if integration == "active" and (update.get("kind") == "retraction" or update.get("disposition") != "reviewed-no-method-change"):
                errors.append(f"{sid}: update requires affected-method review before release")
        if license_.get("rawRedistribution") in {"permission-required", "unknown"}:
            warnings.append(f"{sid}: metadata/original summaries only; upstream redistribution is {license_.get('rawRedistribution')}")
        for text in _walk_strings(s):
            for url in re.findall(r"https?://[^\s<>\"`]+", text):
                if not _url(url):
                    errors.append(f"{sid}: unsafe/non-HTTPS or credential-bearing source URL")
    for row in rows:
        name = row.get("name")
        refs = row.get("researchIds")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{name}: catalog researchIds must name concrete supporting sources")
            continue
        if len(set(refs)) != len(refs):
            errors.append(f"{name}: duplicate research IDs")
        for sid in refs:
            if sid not in by_id:
                errors.append(f"{name}: unknown research ID {sid}")
            elif by_id[sid].get("integrationStatus", "active") != "active":
                errors.append(f"{name}: candidate source {sid} cannot support an active skill")
            elif sid not in declared.get(name, set()):
                errors.append(f"{name}: {sid} has no matching use for this skill")
        if set(refs) != declared.get(name, set()):
            errors.append(f"{name}: catalog researchIds differ from registry use mappings")
    # Benchmark records declare source IDs too. They may use standards that have
    # no direct skill mapping, but the exact registry ID must still resolve.
    for relative_catalog in ("benchmarks/catalog.json", "tools/catalog.json"):
        linked_catalog = root / relative_catalog
        if not linked_catalog.exists():
            continue
        try:
            linked_data = _load(linked_catalog)
            for sid in _research_refs(linked_data):
                if sid not in by_id:
                    errors.append(f"{relative_catalog}: unknown research ID {sid}")
                elif by_id[sid].get("integrationStatus", "active") != "active":
                    errors.append(f"{relative_catalog}: candidate source {sid} cannot support active integration")
            if relative_catalog == "benchmarks/catalog.json":
                for series in linked_data.get("series", []):
                    source = by_id.get(series.get("source_id"))
                    if not source or series.get("rights", {}).get("redistribution") != "permitted":
                        continue
                    field = "derivedRedistribution" if series.get("series_kind") == "derived" else "rawRedistribution"
                    if source.get("license", {}).get(field) != "allowed-with-conditions":
                        errors.append(f"{relative_catalog}: {series.get('id')} redistribution conflicts with source {source['id']}")
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"Cannot validate {relative_catalog} research IDs: {exc}")
    if check_generated:
        try:
            for path, expected in generate(root).items():
                if not (root / path).is_file() or (root / path).read_bytes() != expected:
                    errors.append(f"Generated artifact differs: {path}; run scripts/research_registry.py")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"Cannot generate research README: {exc}")
    result["ok"] = not errors
    return result


def generate(root: Path) -> dict[Path, bytes]:
    """Return generated artifacts without mutating the repository."""
    registry = _load(Path(root) / REGISTRY)
    sources = sorted(registry["sources"], key=lambda s: s["id"])
    lines = ["# Research and source registry", "",
             "Generated from `research/sources.json`. Edit the registry, then run "
             "`python scripts/research_registry.py`.", "",
             "Each entry identifies the exact skill, implementation decision or test it supports. "
             "A method reference is not proof of performance on a particular dataset. "
             "Normative standards, empirical research, provider documentation, software inspiration "
             "and project design choices are labeled separately.", "",
             "This project uses a lightweight catalog informed by FAIR and DCAT. It does not claim "
             "full FAIR certification, DCAT conformance or registration of dataset DOIs.", "",
             "## Maintenance", "",
             "`python scripts/research_registry.py --check` validates IDs, exact use paths, declared "
             "test symbols, review states, rights decisions, pinned upstream consistency and this generated page without network "
             "access. Catalog `researchIds` must agree with the uses below.", "",
             "`python scripts/research_registry.py --check-updates` is an optional read-only network "
             "review. It reads DOI metadata from Crossref and identifies publisher review links; failures remain "
             "unknown. No result automatically approves a source, updates a skill, refreshes an imported "
             "host or establishes that a paper has never been corrected or retracted.", "",
             "The research maintainer reviews publisher notices, editions and licence terms. Record "
             "a correction, supersession, expression of concern or retraction with its affected uses. "
             "Unresolved notices and referenced retractions block release. A candidate is visible "
             "in this registry but cannot support an active skill or implementation. A reviewed link-only "
             "correction may retain the method with a written impact assessment. No upstream PDFs "
             "or full papers are included. Software licensing does not relicense upstream data.", "",
             "## Source map", "",
             "| ID | Evidence type | Review | Exact skills |", "| --- | --- | --- | --- |"]
    for s in sources:
        names = sorted({name for use in s["uses"] for name in use.get("skills", [])})
        anchor = s["id"].replace(".", "")
        empty_label = "Candidate; no active use" if s.get("integrationStatus") == "candidate" else "Implementation / registry"
        lines.append(f"| [`{s['id']}`](#{anchor}) | {s['type']} | {s['reviewStatus']} | "
                     + (", ".join(f"`{n}`" for n in names) or empty_label) + " |")
    for s in sources:
        license_ = s["license"]
        lines += ["", f"## {s['id']}", "", f"**[{s['title']}]({s['url']})**", "",
                  f"{s['publisher']}; {', '.join(s['authors'])}. "
                  f"Year: {s['year'] if s['year'] is not None else 'living documentation'}. "
                  f"Edition: {s['edition']}.", "",
                  f"Type: `{s['type']}`. Review: `{s['reviewStatus']}`. "
                  f"Accessed: {s['accessedOn']}; last reviewed: {s['lastReviewedOn']}. "
                  f"Maintainer: {s['maintainerRole']}.", "", s["reviewNotes"], ""]
        if s.get("integrationStatus") == "candidate":
            lines += [f"**Candidate only — no active method support:** {s['candidateReason']}", ""]
            if s.get("affectedSkills"):
                lines += ["Skills to reconsider after review: " + ", ".join(f"`{name}`" for name in s["affectedSkills"]) + ".", ""]
        if s.get("doi"):
            lines += [f"DOI: [{s['doi']}](https://doi.org/{s['doi']}).", ""]
        if s.get("relatedUrls"):
            lines += ["Related primary sources: " + "; ".join(f"[{url}]({url})" for url in s["relatedUrls"]) + ".", ""]
        lines += [f"Rights: [{license_['name']}]({license_['termsUrl']}); checked {license_['checkedOn']}. "
                  f"Raw redistribution: `{license_['rawRedistribution']}`; derived redistribution: "
                  f"`{license_['derivedRedistribution']}`.", "", f"Attribution: {license_['attribution']}", "",
                  license_["notes"], ""]
        for use in s["uses"]:
            lines += [f"- **Use:** {use['purpose']}", f"  **Supporting section:** {use['section']}",
                      f"  **Limits:** {use['limits']}",
                      "  **Paths:** " + ", ".join(f"[`{p}`](../{p})" for p in use["paths"])]
            if use.get("tests"):
                lines.append("  **Tests:** " + ", ".join(f"`{t}`" for t in use["tests"]))
        for notice in s.get("updates", []):
            review_date = (f"reviewed {notice['reviewedOn']}" if notice.get("reviewedOn")
                           else f"detected {notice.get('detectedOn', 'unknown')}; review incomplete")
            lines += ["", f"**Recorded {notice['kind']}:** [{notice['url']}]({notice['url']}); "
                      f"{review_date}. {notice['assessment']} "
                      f"Disposition: `{notice['disposition']}`."]
    return {GENERATED: ("\n".join(lines).rstrip() + "\n").encode("utf-8")}


def _fetch(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "finance-skills-research-review/1.0",
                                   "Accept": "application/json"})
    with urlopen(request, timeout=15) as response:
        body = response.read(2_000_001)
        if len(body) > 2_000_000:
            raise ValueError("response exceeds review limit")
    return json.loads(body)


def inspect_crossref(source: dict, fetcher: Callable[[str], dict] = _fetch) -> dict:
    """Return observations only. An empty Crossref result is not a clean bill of health."""
    observation = {"id": source["id"], "publisherUrl": source["url"], "mutated": False}
    if not source.get("doi"):
        return {**observation, "status": "publisher-review-required",
                "detail": "No DOI; review the publisher edition, errata and terms manually."}
    url = "https://api.crossref.org/works/" + quote(source["doi"], safe="")
    try:
        message = fetcher(url).get("message", {})
        if not isinstance(message, dict) or str(message.get("DOI", "")).lower() != source["doi"].lower():
            raise ValueError("Crossref response does not identify the requested work")
        updates = []
        for field in ("updated-by", "update-to"):
            for update in message.get(field, []) or []:
                if isinstance(update, dict):
                    updates.append({key: update.get(key) for key in ("DOI", "type", "label", "source")
                                    if update.get(key) is not None})
        relations = {key: value for key, value in message.get("relation", {}).items()
                     if any(token in key for token in ("update", "replace", "version", "retract", "correct"))}
        if updates or relations:
            recorded = {str(n.get("doi", "")).lower(): n for n in source.get("updates", []) if n.get("doi")}
            all_reviewed = bool(updates) and not relations
            for update in updates:
                prior = recorded.get(str(update.get("DOI", "")).lower(), {})
                update["recordedDisposition"] = prior.get("disposition", "not-recorded")
                kind = {"erratum": "correction"}.get(update.get("type"), update.get("type"))
                approved = (prior.get("disposition") == "reviewed-no-method-change"
                            and prior.get("kind") == kind and _date(prior.get("reviewedOn"))
                            and kind != "retraction")
                all_reviewed = all_reviewed and approved
            return {**observation, "status": "recorded-updates" if all_reviewed else "review-required",
                    "updates": updates, "relations": relations,
                    "detail": ("Returned notices match recorded assessments; this is not a complete publisher integrity review."
                               if all_reviewed else "Compare publisher notices with recorded assessments before release.")}
        return {**observation, "status": "no-update-reported",
                "detail": "Crossref returned no update relation; publisher review is still required."}
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        # Avoid exception text: URLs/headers from third-party clients can contain credentials.
        return {**observation, "status": "unavailable", "errorType": type(exc).__name__,
                "detail": "Update state is unknown; no review or method was changed."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--check", action="store_true")
    actions.add_argument("--check-updates", action="store_true")
    args = parser.parse_args(argv)
    if args.check_updates:
        registry = _load(args.root / REGISTRY)
        print(json.dumps({"readOnly": True, "observations": [inspect_crossref(s) for s in registry["sources"]]}, indent=2))
        return 0
    report = validate(args.root, check_generated=args.check)
    if not report["ok"]:
        print(json.dumps(report, indent=2))
        return 1
    if not args.check:
        for path, content in generate(args.root).items():
            (args.root / path).parent.mkdir(parents=True, exist_ok=True)
            (args.root / path).write_bytes(content)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
