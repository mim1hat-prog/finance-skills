"""Generate descriptive repository coverage from validated local sources, offline."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, timezone
import hashlib
from html import escape
import json
from pathlib import Path
import re
import sys
from textwrap import wrap

import benchmark_data
import catalog_contracts
import research_registry

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = (Path("metrics/summary.json"), Path("metrics/README.md"), Path("assets/coverage.svg"))


def proportion(numerator: int, denominator: int) -> dict:
    """An empty population is undefined, not zero or complete coverage."""
    if not 0 <= numerator <= denominator:
        raise ValueError("Coverage numerator must be within its denominator")
    return {"numerator": numerator, "denominator": denominator,
            "percent": round(100 * numerator / denominator, 1) if denominator else None}


def distribution(values) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def describe(catalog: dict, tools: dict, registry: dict, dataset: dict, saved: list[dict]) -> dict:
    """Count validated inputs. A newer vintage replaces, rather than adds to, a series count."""
    skills = catalog["skills"]
    names = {s["name"] for s in skills}
    if len(names) != len(skills):
        raise ValueError("Duplicate skill identity in metrics input")
    sources = {s["id"]: s for s in registry["sources"]}
    if len(sources) != len(registry["sources"]):
        raise ValueError("Duplicate research identity in metrics input")
    active = {sid for sid, source in sources.items()
              if source.get("integrationStatus", "active") == "active"}
    mapped = set()
    for skill in skills:
        refs = skill.get("researchIds", [])
        for ref in refs:
            if ref not in sources:
                raise ValueError(f"Unknown research reference: {ref}")
            if ref not in active:
                raise ValueError(f"Inactive source cannot count as skill support: {ref}")
            if not any(skill["name"] in use.get("skills", []) for use in sources[ref]["uses"]):
                raise ValueError(f"Missing source-to-skill use: {ref}")
        if refs:
            mapped.add(skill["name"])
    tests = {s["name"]: s.get("contract", {}).get("validation", {}) for s in skills}
    package_linked = sorted(name for name, row in tests.items() if row.get("packageTests"))
    workflow_linked = sorted(name for name, row in tests.items() if row.get("workflowTests"))
    native_status = distribution(row.get("nativeStatus", "not-recorded") for row in tests.values())
    # The public contract validator currently permits only not-validated. Do not
    # invent a native pass from a nonempty status string or from a local test.
    if any(status != "not-validated" for status in native_status):
        raise ValueError("Native evidence requires a supported validation record before it can be counted")
    native_count = sum(row.get("nativeStatus") == "validated" for row in tests.values())
    for tool in tools["tools"]:
        if set(tool["skillIds"]) - names:
            raise ValueError("Tool points to an unknown skill")
    public = [s for s in saved if s["data_class"] == "public"]
    records = []
    for series in sorted(dataset["series"], key=lambda row: row["id"]):
        candidates = [s for s in public if series["id"] in {r["id"] for r in s["series"]}]
        selected = max(candidates, key=lambda s: (benchmark_data.timestamp(s["retrieved_at"]), s["id"])) if candidates else None
        if selected:
            frozen = next(row for row in selected["series"] if row["id"] == series["id"])
            if any(frozen[key] != series[key] for key in ("series_kind", "unit", "frequency", "index_base",
                                                         "seasonal_adjustment", "provider", "provider_series_id",
                                                         "source_id", "geography", "currency")):
                raise ValueError("Current and selected snapshot metadata differ; review the coverage definition")
        rows = [r for r in selected["observations"] if r["series_id"] == series["id"]] if selected else []
        if any(r["origin"] == "synthetic" for r in rows):
            raise ValueError("Synthetic row inside a public snapshot")
        kinds = {r["origin"] for r in rows}
        if kinds - {series["series_kind"]}:
            raise ValueError("Current and selected snapshot series kinds differ; review the coverage definition")
        periods = sorted(r["observation_period"] for r in rows)
        records.append({
            "id": series["id"], "sourceId": series["source_id"],
            "adapter": series["adapter"], "adapterStatus": series["adapter_status"],
            "kind": series["series_kind"], "frequency": series["frequency"], "unit": series["unit"],
            "redistribution": series["rights"]["redistribution"],
            "observations": len(rows), "firstPeriod": periods[0] if periods else None,
            "lastPeriod": periods[-1] if periods else None,
            "selectedSnapshotId": selected["id"] if selected else None,
            "retrievedAt": selected["retrieved_at"] if selected else None,
            "status": "observed" if rows else "no-retained-public-observations",
        })
    observed = [row for row in records if row["observations"]]
    row_counts = {kind: sum(row["observations"] for row in records if row["kind"] == kind)
                  for kind in ("original", "derived")}
    snapshots = [{"id": s["id"], "retrievedAt": s["retrieved_at"],
                  "rowsAcrossAllSeriesInThisVintage": len(s["observations"])}
                 for s in sorted(public, key=lambda s: (benchmark_data.timestamp(s["retrieved_at"]), s["id"]))]
    return {
        "schemaVersion": 1, "measurementType": "descriptive-repository-inventory",
        "projectVersion": catalog["version"], "releaseDate": catalog["releasedOn"],
        "sourceReviewDates": {"skills": catalog["reviewedOn"], "tools": tools["reviewedOn"],
                              "research": registry["reviewedOn"]},
        "skills": {
            "count": len(skills), "categories": distribution(s["category"] for s in skills),
            "groups": distribution(s["group"] for s in skills),
            "declaredContracts": proportion(sum(bool(s.get("contract")) for s in skills), len(skills)),
            "activeSourceMappings": proportion(len(mapped), len(skills)),
            "declaredPackageTestLinks": proportion(len(package_linked), len(skills)),
            "declaredWorkflowTestLinks": proportion(len(workflow_linked), len(skills)),
            "nativeExecutionEvidence": proportion(native_count, len(skills)),
            "nativeStatus": native_status,
            "withDeclaredWorkflowTests": workflow_linked,
            "withoutDeclaredWorkflowTests": sorted(names - set(workflow_linked)),
        },
        "research": {
            "registered": len(sources), "active": len(active), "candidates": len(sources) - len(active),
            "reviewStatus": distribution(s["reviewStatus"] for s in sources.values()),
            "activeSourceTypes": distribution(sources[sid]["type"] for sid in active),
            "candidateIds": sorted(set(sources) - active),
            "limit": "A source mapping records a stated use; it is not independent empirical validation of a skill.",
        },
        "tools": {"registered": len(tools["tools"]),
                  "availability": distribution(t["availability"] for t in tools["tools"]),
                  "limit": "Inventory entries do not establish installation, permission or native integration."},
        "benchmarks": {
            "datasetId": dataset["dataset_id"], "datasetVersion": dataset["dataset_version"],
            "configuredSeries": len(records), "observedSeries": proportion(len(observed), len(records)),
            "retainedPublicSnapshots": len(public), "originalObservationRows": row_counts["original"],
            "derivedObservationRows": row_counts["derived"], "selectedObservationRows": sum(row_counts.values()),
            "adapterStatus": distribution(row["adapterStatus"] for row in records),
            "observedAdapters": sorted({row["adapter"] for row in observed}),
            "series": records, "publicSnapshots": snapshots,
            "excludedSyntheticSnapshotsInPublicStore": len(saved) - len(public),
            "selectionRule": "For each currently configured series, use its latest retained public snapshot by retrieval timestamp, then snapshot ID. Count that snapshot's rows once. A later empty snapshot is not backfilled from an older one.",
            "exclusions": "Synthetic fixtures, retired series outside the current catalogue, and earlier vintages of a selected series are excluded from observation totals. Public snapshot retention counts still include older public vintages.",
        },
        "limits": [
            "These are descriptive counts, not model accuracy, task success, statistical confidence or native account validation.",
            "A linked local test is a declared test reference, not a full-workflow pass or an execution receipt; this generator does not run tests.",
            "Repository skill categories are editorial classifications, not a representative sample of all finance tasks.",
            "Observed-series coverage is availability within this project's configured catalogue, not coverage of all public finance data or of a company's inputs.",
            "Daily and monthly observations count retained rows; they are not comparable sample sizes. Financial values with different units are never pooled.",
            "Stored retrieval timestamps and observation periods are not a live refresh, freshness guarantee or evidence of what was known before those snapshots were captured.",
        ],
    }


def ratio_text(value: dict) -> str:
    pct = "undefined" if value["percent"] is None else f"{value['percent']:g}%"
    return f"{value['numerator']} / {value['denominator']} ({pct})"


def retained_context(summary: dict) -> list[dict]:
    """Describe stored date evidence without treating a build as a provider fetch."""
    grouped: dict[tuple[str, str, str], list[dict]] = {}
    for row in summary["benchmarks"]["series"]:
        if row["observations"]:
            grouped.setdefault((row["sourceId"], row["adapter"], row["frequency"]), []).append(row)
    context = []
    for (source, adapter, frequency), rows in sorted(grouped.items()):
        ends = sorted(row["lastPeriod"] for row in rows)
        retrieved = sorted(benchmark_data.timestamp(row["retrievedAt"]).astimezone(timezone.utc)
                           for row in rows)
        stamps = [value.isoformat().replace("+00:00", "Z") for value in (retrieved[0], retrieved[-1])]
        context.append({
            "sourceId": source, "adapter": adapter, "frequency": frequency,
            "latestPeriods": ends[0] if ends[0] == ends[-1] else f"{ends[0]} to {ends[-1]} (varies by series)",
            "retrievedAt": stamps[0] if stamps[0] == stamps[-1] else f"{stamps[0]} to {stamps[-1]}",
        })
    return context


def update_readme(text: str, summary: dict) -> bytes:
    """Regenerate the homepage graph, text equivalent and actual retained-data dates."""
    start = "<!-- project-coverage-summary:start -->"
    end = "<!-- project-coverage-summary:end -->"
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError("Expected one ordered homepage coverage summary block")
    quick_start = re.search(r"^##\s+Quick start\s*$", text, re.MULTILINE)
    if quick_start and text.index(end) > quick_start.start():
        raise ValueError("Homepage coverage block must precede Quick start")
    skills, data = summary["skills"], summary["benchmarks"]
    workflow = skills["declaredWorkflowTestLinks"]
    native = skills["nativeExecutionEvidence"]
    observed = data["observedSeries"]
    sentence = (
        f"**{skills['count']} skills** · "
        f"**{workflow['numerator']}/{workflow['denominator']}** with workflow-test links · "
        f"**{native['numerator']}/{native['denominator']}** with native execution evidence · "
        f"**{observed['numerator']}/{observed['denominator']}** configured benchmark series with observations."
    )
    content = [
        "[![Descriptive coverage of skill evidence and public benchmark data, showing numerators, denominators and retained observation dates](assets/coverage.svg)](metrics/README.md)",
        "", sentence, "",
        f"Repository measurements: **v{summary['projectVersion']}**, release **{summary['releaseDate']}**. "
        "The release date is not a provider retrieval date.", "",
    ]
    context = retained_context(summary)
    for source in context:
        content.append(
            f"- **`{source['sourceId']}` ({source['frequency']}):** latest retained observation period per series "
            f"**{source['latestPeriods']}**; retrieval timestamp (UTC) **{source['retrievedAt']}**."
        )
    if not context:
        content.append("No public observations are retained; no provider retrieval date is inferred.")
    content += ["", "Dates describe retained snapshots. Rebuilding these graphs does not fetch providers or establish current market-data freshness."]
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return (before + start + "\n" + "\n".join(content) + "\n" + end + after).encode("utf-8")


def markdown(summary: dict) -> bytes:
    skills, research, data = summary["skills"], summary["research"], summary["benchmarks"]
    lines = ["# Repository coverage and public-data inventory", "",
             f"Version **{summary['projectVersion']}** · release date **{summary['releaseDate']}** · generated offline from the committed sources.", "",
             "These descriptive counts make implemented scope and remaining gaps visible. They do not measure model accuracy, task success or effectiveness in a work account.", "",
             "![Repository evidence links and retained public benchmark coverage](../assets/coverage.svg)", "",
             "[Machine-readable measurements](summary.json) · [Generator](../scripts/project_metrics.py) · [Validation record](../docs/VALIDATION.md)", "",
             "## Skill coverage", "",
             "The denominator is the complete canonical skill catalogue, including the Excel agent defaults. A test link means the named test exists; it does not mean a model completed that workflow.", "",
             "| Measurement | Numerator / denominator | Definition |", "| --- | --- | --- |",
             f"| Declared workflow contracts | {ratio_text(skills['declaredContracts'])} | Skills with structured inputs, outputs and execution conditions |",
             f"| Active source mappings | {ratio_text(skills['activeSourceMappings'])} | Skills linked to an active registry source with a matching stated use |",
             f"| Declared package-test links | {ratio_text(skills['declaredPackageTestLinks'])} | Skills naming at least one resolvable local package test |",
             f"| Declared workflow-test links | {ratio_text(skills['declaredWorkflowTestLinks'])} | Skills naming at least one resolvable local workflow test; full task coverage is not implied |",
             f"| Native execution evidence | {ratio_text(skills['nativeExecutionEvidence'])} | Skills with an accepted native-account validation record; currently none is supported by the public contract |", "",
             "### Scope by task category", "",
             "Categories are the project's editorial grouping, not an external financial taxonomy or a completeness score.", "",
             "| Category | Skills |", "| --- | ---: |"]
    lines += [f"| {name} | {count} |" for name, count in skills["categories"].items()]
    lines += ["", "### Explicit gaps", "",
              "Skills without a declared workflow-test link: " + (", ".join(f"`{name}`" for name in skills["withoutDeclaredWorkflowTests"]) or "none") + ".", "",
              "All host workflows still require a representative check in the actual approved Copilot/Gemini account. Local package and helper checks cannot establish host activation, tool access or answer quality.", "",
              "## Research and tool inventory", "",
              f"The registry has **{research['registered']} records: {research['active']} active and {research['candidates']} candidate**. Candidates are excluded from active skill support. Active records can be standards, provider documentation, software references or project design decisions; this total is not a count of peer-reviewed experiments.", "",
              "| Source review status | Records |", "| --- | ---: |"]
    lines += [f"| {name} | {count} |" for name, count in research["reviewStatus"].items()]
    lines += ["", f"The tool catalogue contains **{summary['tools']['registered']} capabilities/products**. Availability labels remain separate from installation or integration evidence.", "",
              "| Tool availability label | Entries |", "| --- | ---: |"]
    lines += [f"| {name} | {count} |" for name, count in summary["tools"]["availability"].items()]
    lines += ["", "[Exact source uses and limitations](../research/README.md) · [Tool availability definitions](../TOOLS.md)", "",
              "## Retained public benchmark data", "",
              f"**{ratio_text(data['observedSeries'])} configured series** have observations in their latest retained public snapshot. "
              f"Across those selected series there are **{data['originalObservationRows']} original rows** and **{data['derivedObservationRows']} separately derived rows**. "
              f"The store retains **{data['retainedPublicSnapshots']} public snapshots**. Synthetic fixtures do not contribute to these totals.", "",
              "Each series is counted from its own latest retained public snapshot. Repeated historical rows in later vintages do not inflate the total. The table reports row availability and stored period ranges, not completeness against an official trading/release calendar.", "",
              "| Series | Kind | Rows | Stored periods | Unit |", "| --- | --- | ---: | --- | --- |"]
    for row in data["series"]:
        if row["observations"]:
            lines.append(f"| `{row['id']}` | {row['kind']} | {row['observations']} | {row['firstPeriod']} to {row['lastPeriod']} | {row['unit']} |")
    if not any(row["observations"] for row in data["series"]):
        lines += ["| No retained public observations | — | 0 | — | — |"]
    lines += ["", "### Configured series without retained observations", "",
              "These remain visible in the denominator. A configured adapter or public URL is not a supported observation feed.", "",
              "| Series | Adapter state | Redistribution |", "| --- | --- | --- |"]
    missing = [row for row in data["series"] if not row["observations"]]
    lines += [f"| `{row['id']}` | {row['adapterStatus']} | {row['redistribution']} |" for row in missing]
    if not missing:
        lines += ["| None | — | — |"]
    lines += ["", "### Retained acquisition evidence", "",
              "| Public snapshot | Retrieval timestamp | Rows in that vintage |", "| --- | --- | ---: |"]
    lines += [f"| [{s['id']}](../benchmarks/snapshots/{s['id']}/snapshot.json) | {s['retrievedAt']} | {s['rowsAcrossAllSeriesInThisVintage']} |" for s in data["publicSnapshots"]]
    if not data["publicSnapshots"]:
        lines += ["| None | — | 0 |"]
    lines += ["", "Snapshot rows are shown separately for retention evidence; do not sum overlapping vintages as additional observations. "
              "A retrieval timestamp establishes the stored acquisition, not a claim that the provider has been checked again today. "
              "See [dataset methods and rights](../benchmarks/README.md) and the [data dictionary](../benchmarks/DATA_DICTIONARY.md).", "",
              "## Reproduce the measurements", "",
              "```powershell", "py -3 scripts\\project_metrics.py", "py -3 scripts\\project_metrics.py --check", "```", "",
              "The generator validates workflow/tool references, source-to-skill mappings and the public dataset inventory before counting. "
              "It reads `catalog.json`, `tools/catalog.json`, `research/sources.json`, `benchmarks/catalog.json` and the validated public snapshot files. "
              "The JSON output records their SHA-256 hashes. It performs no network calls, does not execute tests and does not inspect private workbooks or work accounts.", "",
              "For every ratio, percentage = numerator ÷ denominator × 100, rounded to one decimal place. An empty denominator is undefined. "
              "The SVG is generated from the same summary as this page, with labeled counts and denominators. No confidence interval or significance test is appropriate for this complete, deterministic repository inventory.", "",
              "### Interpretation limits", ""]
    lines += [f"- {value}" for value in summary["limits"]]
    return ("\n".join(lines) + "\n").encode("utf-8")


def figure(summary: dict) -> bytes:
    skills, data = summary["skills"], summary["benchmarks"]
    scale = 358
    footer: list[tuple[int, str, int, str]] = []
    y = 614
    def footer_text(value: str, size: int = 15, weight: str = "400") -> None:
        nonlocal y
        for line in wrap(value, width=112 if size <= 15 else 100):
            footer.append((y, line, size, weight))
            y += 23
    footer_text("C. Retained data context", 19, "650")
    footer_text("Latest endpoints across selected series; the release date above is not a provider retrieval date.")
    y += 7
    context = retained_context(summary)
    for source in context:
        footer_text(f"{source['sourceId']} ({source['frequency']}): latest per-series period {source['latestPeriods']}", 15, "600")
        footer_text(f"Retrieved (UTC): {source['retrievedAt']}", 14)
        y += 7
    if not context:
        footer_text("No retained public observations; no provider retrieval date is inferred.")
        y += 7
    footer_text("Counts show scope and gaps, not model accuracy, native task success or a live provider refresh.", 16, "650")
    footer_text("Methods, denominators and source hashes: metrics/README.md · Reproduce: python scripts/project_metrics.py", 14)
    height = y + 22
    a = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
         '<title id="title">Finance skills: repository coverage and retained public data</title>',
         '<desc id="desc">' + escape(
             f"Descriptive inventory for version {summary['projectVersion']}. "
             f"Workflow test links {ratio_text(skills['declaredWorkflowTestLinks'])}; native execution evidence {ratio_text(skills['nativeExecutionEvidence'])}. "
             f"Observed benchmark series {ratio_text(data['observedSeries'])}; {data['originalObservationRows']} original and {data['derivedObservationRows']} derived rows. "
             "Counts describe repository evidence, not model accuracy or production readiness.") + '</desc>',
         f'<rect width="1200" height="{height}" fill="#FAF8F4"/>',
         '<g font-family="system-ui, -apple-system, Segoe UI, sans-serif" fill="#242622">',
         '<text x="48" y="55" font-size="30" font-weight="650">Repository coverage</text>',
         '<circle cx="1140" cy="45" r="12" fill="#31573f"/>',
         f'<text x="48" y="88" font-size="16" fill="#60645C">Descriptive inventory · v{escape(summary["projectVersion"])} · release {escape(summary["releaseDate"])}</text>',
         '<path d="M48 113H1152 M624 146V550 M48 582H1152" stroke="#DADDD5" fill="none"/>',
         f'<text x="48" y="154" font-size="19" font-weight="650">A. Skill evidence links (n = {skills["count"]})</text>',
         '<text x="660" y="154" font-size="19" font-weight="650">B. Retained public benchmark data</text>']
    labels = [("Declared contracts", "declaredContracts"), ("Active source mappings", "activeSourceMappings"),
              ("Package-test links", "declaredPackageTestLinks"), ("Workflow-test links", "declaredWorkflowTestLinks"),
              ("Native execution evidence", "nativeExecutionEvidence")]
    for index, (label, key) in enumerate(labels):
        y = 198 + index * 70
        value = skills[key]
        width = scale * (value["numerator"] / value["denominator"]) if value["denominator"] else 0
        a += [f'<text x="48" y="{y}" font-size="16">{label}</text>',
              f'<rect x="48" y="{y+13}" width="{scale}" height="12" fill="#DADDD5"/>',
              f'<rect x="48" y="{y+13}" width="{width:.2f}" height="12" fill="#31573f"/>',
              f'<text x="426" y="{y+25}" font-size="15" font-variant-numeric="tabular-nums">{escape(ratio_text(value))}</text>']
    observed = data["observedSeries"]
    fraction = observed["numerator"] / observed["denominator"] if observed["denominator"] else 0
    a += ['<text x="660" y="198" font-size="16">Configured series with observations</text>',
          f'<text x="660" y="235" font-size="28" font-weight="650">{escape(ratio_text(observed))}</text>',
          '<rect x="660" y="254" width="492" height="12" fill="#DADDD5"/>',
          f'<rect x="660" y="254" width="{492*fraction:.2f}" height="12" fill="#31573f"/>',
          f'<text x="660" y="310" font-size="16">Original source rows</text><text x="1152" y="310" text-anchor="end" font-size="23" font-weight="650">{data["originalObservationRows"]}</text>',
          f'<text x="660" y="349" font-size="16">Derived rows</text><text x="1152" y="349" text-anchor="end" font-size="23" font-weight="650">{data["derivedObservationRows"]}</text>',
          f'<text x="660" y="388" font-size="16">Retained public snapshots</text><text x="1152" y="388" text-anchor="end" font-size="23" font-weight="650">{data["retainedPublicSnapshots"]}</text>',
          f'<text x="660" y="436" font-size="15" fill="#60645C">{observed["denominator"]-observed["numerator"]} configured series have no retained public observations.</text>',
          '<text x="660" y="466" font-size="15" fill="#60645C">Latest retained snapshot per series; vintages are not added.</text>',
          '<text x="660" y="496" font-size="15" fill="#60645C">Synthetic fixtures are excluded from public-data counts.</text>',
          '<text x="660" y="526" font-size="15" fill="#60645C">Daily and monthly row counts are not sample-size claims.</text>']
    a += [f'<text x="48" y="{baseline}" font-size="{size}" font-weight="{weight}" fill="#60645C">{escape(line)}</text>'
          for baseline, line, size, weight in footer]
    a += ['</g>', '</svg>', '']
    return "\n".join(a).encode("utf-8")


def generate(root: Path, catalog: dict | None = None) -> dict[Path, bytes]:
    root = Path(root)
    canonical = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if catalog is not None and catalog != canonical:
        raise ValueError("Metrics catalogue differs from its authoritative source file")
    catalog = canonical
    date.fromisoformat(catalog["releasedOn"])
    tools = catalog_contracts.validate(root, catalog)
    checked = research_registry.validate(root, check_generated=False)
    if not checked["ok"]:
        raise ValueError("Metrics research references failed: " + "; ".join(checked["errors"]))
    registry = json.loads((root / "research/sources.json").read_text(encoding="utf-8"))
    store = root / "benchmarks"
    benchmark_data.check_inventory(store)
    dataset = benchmark_data.load_catalog(store)
    saved = benchmark_data.snapshots(store)
    summary = describe(catalog, tools, registry, dataset, saved)
    paths = ["catalog.json", "tools/catalog.json", "research/sources.json", "benchmarks/catalog.json", "benchmarks/manifest.json"]
    paths += [f"benchmarks/snapshots/{snapshot['id']}/{name}" for snapshot in saved
              if snapshot["data_class"] == "public" for name in ("manifest.json", "observations.csv", "snapshot.json")]
    summary["inputs"] = [{"path": name, "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest()}
                         for name in sorted(paths)]
    return {OUTPUTS[0]: (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
            OUTPUTS[1]: markdown(summary), OUTPUTS[2]: figure(summary),
            Path("README.md"): update_readme((root / "README.md").read_text(encoding="utf-8"), summary)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check exact generated bytes without writing")
    args = parser.parse_args(argv)
    try:
        outputs = generate(ROOT)
        for relative, content in outputs.items():
            path = ROOT / relative
            if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != ROOT.parent):
                raise ValueError(f"Linked metrics output refused: {relative}")
            if args.check:
                if not path.is_file() or path.read_bytes() != content:
                    raise ValueError(f"Stale metrics output: {relative}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        print(f"{'Verified' if args.check else 'Generated'} {len(outputs)} descriptive coverage artifacts; no performance claim.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Metrics failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
