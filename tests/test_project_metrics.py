"""Descriptive inventory regressions; no network, credentials or employer data."""
from __future__ import annotations

import copy
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import benchmark_data as data
import project_metrics as metrics


class ProjectMetricsTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "catalog.json").read_text())
        self.tools = json.loads((ROOT / "tools/catalog.json").read_text())
        self.registry = json.loads((ROOT / "research/sources.json").read_text())
        self.dataset = data.load_catalog(ROOT / "benchmarks")

    def describe(self, saved=(), **overrides):
        values = {"catalog": self.catalog, "tools": self.tools, "registry": self.registry,
                  "dataset": self.dataset, "saved": list(saved)}
        values.update(overrides)
        return metrics.describe(**values)

    def snapshot(self, retrieved: str, value="150", *, empty=False, synthetic=False):
        # Wholly invented provider-shaped data, confined to this unit test.
        series = self.dataset["series"][0]
        row = data.observation(series, "2024-01-02", value, retrieved,
                               origin="synthetic" if synthetic else "original")
        return data.make_snapshot(self.dataset, [] if empty else [row], retrieved,
                                  data_class="synthetic" if synthetic else "public",
                                  series_ids=[series["id"]],
                                  capture_method="Wholly invented test input; not a provider observation")

    def test_generated_metrics_are_exact_deterministic_and_traceable(self):
        generated = metrics.generate(ROOT)
        self.assertEqual(generated, metrics.generate(ROOT))
        summary = json.loads(generated[Path("metrics/summary.json")])
        self.assertEqual(summary["projectVersion"], self.catalog["version"])
        self.assertEqual(summary["skills"]["count"], len(self.catalog["skills"]))
        expected_links = [s["name"] for s in self.catalog["skills"] if s["contract"]["validation"]["workflowTests"]]
        self.assertEqual(summary["skills"]["withDeclaredWorkflowTests"], sorted(expected_links))
        self.assertEqual(summary["skills"]["declaredWorkflowTestLinks"]["numerator"], len(expected_links))
        expected_active = sum(s.get("integrationStatus", "active") == "active" for s in self.registry["sources"])
        self.assertEqual(summary["research"]["active"], expected_active)
        self.assertEqual(summary["research"]["registered"], len(self.registry["sources"]))
        for source in summary["inputs"]:
            self.assertEqual(source["sha256"], hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest())
            self.assertNotIn("/fixtures/", source["path"])
        figure = ET.fromstring(generated[Path("assets/coverage.svg")])
        self.assertEqual(figure.get("role"), "img")
        self.assertTrue(figure.find("{http://www.w3.org/2000/svg}title").text)
        self.assertIn("not model accuracy", figure.find("{http://www.w3.org/2000/svg}desc").text)
        self.assertIn("not a full-workflow pass", " ".join(summary["limits"]))

    def test_vintages_do_not_inflate_counts_and_synthetic_is_excluded(self):
        first = self.snapshot("2024-02-01T09:00:00Z")
        revised = self.snapshot("2024-03-01T09:00:00Z", "151")
        synthetic = self.snapshot("2024-04-01T09:00:00Z", "999", synthetic=True)
        summary = self.describe([first, revised, synthetic])["benchmarks"]
        self.assertEqual(summary["retainedPublicSnapshots"], 2)
        self.assertEqual(summary["excludedSyntheticSnapshotsInPublicStore"], 1)
        self.assertEqual(summary["selectedObservationRows"], 1)
        self.assertEqual(summary["originalObservationRows"], 1)
        self.assertEqual(summary["derivedObservationRows"], 0)
        selected = next(s for s in summary["series"] if s["id"] == self.dataset["series"][0]["id"])
        self.assertEqual(selected["selectedSnapshotId"], revised["id"])
        self.assertEqual(summary["observedSeries"], metrics.proportion(1, len(self.dataset["series"])))

    def test_homepage_text_updates_from_counts_without_changing_surrounding_content(self):
        before = "# Invented homepage\n\n<!-- project-coverage-summary:start -->\nstale counts\n<!-- project-coverage-summary:end -->\n\nKeep this link.\n"
        summary = self.describe()
        summary["skills"]["count"] = 2
        summary["skills"]["declaredWorkflowTestLinks"] = metrics.proportion(1, 2)
        summary["skills"]["nativeExecutionEvidence"] = metrics.proportion(0, 2)
        summary["benchmarks"]["observedSeries"] = metrics.proportion(0, 3)
        result = metrics.update_readme(before, summary).decode()
        self.assertTrue(result.startswith("# Invented homepage\n\n"))
        self.assertTrue(result.endswith("\n\nKeep this link.\n"))
        self.assertIn("**2 skills**", result)
        self.assertIn("**1/2** with workflow-test links", result)
        self.assertIn("**0/2** with native execution evidence", result)
        self.assertIn("**0/3** configured benchmark series", result)
        self.assertNotIn("stale counts", result)
        for malformed in (before.replace(":start", ":missing"),
                          before + "<!-- project-coverage-summary:end -->",
                          "<!-- project-coverage-summary:end --><!-- project-coverage-summary:start -->"):
            with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                metrics.update_readme(malformed, summary)

    def test_empty_new_vintage_does_not_backfill_or_claim_complete_coverage(self):
        first = self.snapshot("2024-02-01T09:00:00Z")
        empty = self.snapshot("2024-03-01T09:00:00Z", empty=True)
        summary = self.describe([first, empty])["benchmarks"]
        self.assertEqual(summary["observedSeries"]["numerator"], 0)
        self.assertEqual(summary["selectedObservationRows"], 0)
        self.assertEqual(metrics.proportion(0, 0), {"numerator": 0, "denominator": 0, "percent": None})
        with self.assertRaises(ValueError):
            metrics.proportion(1, 0)

    def test_missing_inactive_and_unmapped_sources_do_not_count_as_support(self):
        for case in ("missing", "candidate", "no-use"):
            with self.subTest(case=case):
                registry = copy.deepcopy(self.registry)
                ref = self.catalog["skills"][0]["researchIds"][0]
                source = next(s for s in registry["sources"] if s["id"] == ref)
                if case == "missing":
                    registry["sources"].remove(source)
                elif case == "candidate":
                    source["integrationStatus"] = "candidate"
                else:
                    source["uses"] = []
                with self.assertRaises(ValueError):
                    self.describe(registry=registry)

    def test_metadata_change_and_unsupported_native_claim_fail_closed(self):
        snapshot = self.snapshot("2024-02-01T09:00:00Z")
        dataset = copy.deepcopy(self.dataset)
        dataset["series"][0]["index_base"] = "different-base"
        with self.assertRaisesRegex(ValueError, "metadata differ"):
            self.describe([snapshot], dataset=dataset)
        catalog = copy.deepcopy(self.catalog)
        catalog["skills"][0]["contract"]["validation"]["nativeStatus"] = "validated"
        with self.assertRaisesRegex(ValueError, "supported validation record"):
            self.describe(catalog=catalog)

    def test_check_is_read_only_and_rejects_stale_generated_bytes(self):
        outputs = metrics.generate(ROOT)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, content in outputs.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes(content)
            before = {p: (root / p).stat().st_mtime_ns for p in outputs}
            with patch.object(metrics, "ROOT", root), patch.object(metrics, "generate", return_value=outputs):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(metrics.main(["--check"]), 0)
                self.assertEqual(before, {p: (root / p).stat().st_mtime_ns for p in outputs})
                path = root / "metrics/summary.json"
                path.write_bytes(b"stale\n")
                error = io.StringIO()
                with redirect_stderr(error), redirect_stdout(io.StringIO()):
                    self.assertEqual(metrics.main(["--check"]), 1)
                self.assertIn("Stale metrics output", error.getvalue())
                self.assertEqual(path.read_bytes(), b"stale\n")


if __name__ == "__main__":
    unittest.main()
