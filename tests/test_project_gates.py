"""Integration regressions for publication gates over actual generated artifacts."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build
import project_gates
import release
import research_registry


class ProjectGates(unittest.TestCase):
    def test_generated_skill_and_citation_drift_are_rejected_before_freeze(self):
        sources = release.collect_project(ROOT)
        for path in ("CITATION.cff", "editions/copilot/excel-agent-core/SKILL.md",
                     "metrics/summary.json", "site/index.html"):
            changed = dict(sources)
            changed[path] += b"\nUnreviewed generated change\n"
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "build drift"):
                project_gates.validate(ROOT, sources=changed, include_history=False)

    def test_unresolved_research_reference_prevents_release_gate(self):
        result = {"ok": False, "errors": ["missing-source: unresolved research ID"], "warnings": []}
        with mock.patch.object(research_registry, "validate", return_value=result):
            with self.assertRaisesRegex(ValueError, "unresolved research ID"):
                project_gates.validate(ROOT, include_history=False)

    def test_nested_release_and_private_marker_are_checked_without_writes(self):
        sources = release.collect_project(ROOT)
        marker = "independently-invented-publication-marker"
        sources["docs/invented-example.md"] = marker.encode()
        with self.assertRaisesRegex(ValueError, "private-review-marker"):
            project_gates.validate(ROOT, sources=sources, include_history=False, private_literals=(marker,))
        catalog = json.loads((ROOT / "catalog.json").read_text())
        changed = copy.deepcopy(catalog)
        changed["releasedOn"] = "2026-02-30"
        actual = Path.read_text
        def read(path, *args, **kwargs):
            return json.dumps(changed) if path == ROOT / "catalog.json" else actual(path, *args, **kwargs)
        with mock.patch.object(Path, "read_text", read), self.assertRaises(ValueError):
            build.generate(ROOT)


if __name__ == "__main__":
    unittest.main()
