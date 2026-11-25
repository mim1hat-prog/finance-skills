"""Offline source, generated-artifact, evidence, dataset and publication gates."""
from __future__ import annotations

import json
from pathlib import Path

import benchmark_api
import benchmark_data
import check_publication
import research_registry


def validate(root: Path, *, sources: dict[str, bytes] | None = None,
             include_history: bool = True, private_literals: tuple[str, ...] = ()) -> dict:
    # Local import keeps release.prepare -> gates -> release free of import-time work.
    import release

    files = dict(sources if sources is not None else release.collect_project(root))
    release.verify_build(root, files)
    registry = research_registry.validate(root, check_generated=True)
    if not registry["ok"]:
        raise ValueError("Research gate failed: " + "; ".join(registry["errors"]))
    store = root / "benchmarks"
    benchmark_data.check_inventory(store)
    benchmark_data.check_inventory(store / "fixtures")
    contract = benchmark_api.validate_openapi(store, root / "api/openapi.yaml")
    fixtures = benchmark_api.validate_openapi(store / "fixtures", root / "api/openapi.yaml")
    versions = []
    if include_history and (root / "releases").exists():
        versions = release.existing_versions(root / "releases")
        for path in (root / "releases").rglob("*"):
            if path.is_symlink():
                raise ValueError("Linked release entry refused")
            if path.is_file():
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    policy = json.loads((root / "tools/publication-policy.json").read_text(encoding="utf-8"))
    if set(policy) != {"schemaVersion", "reviewedOn", "reviewedSyntheticTests"} or policy["schemaVersion"] != 1:
        raise ValueError("Unsupported publication policy")
    scan = check_publication.scan_inventory(files, private_literals=private_literals,
                                           exceptions=tuple(policy["reviewedSyntheticTests"]))
    if not scan["ok"]:
        raise ValueError("Publication gate failed: " + "; ".join(
            f"{finding['path']}: {finding['code']}" for finding in scan["findings"]))
    return {"ok": True, "generatedArtifacts": "exact", "research": registry,
            "publicDataset": {"snapshots": len(benchmark_data.snapshots(store)), "contract": contract},
            "syntheticDataset": {"snapshots": len(benchmark_data.snapshots(store / 'fixtures')), "contract": fixtures},
            "verifiedPriorVersions": [v["version"] for v in versions], "publication": scan}
