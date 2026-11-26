"""Integrity, grading and reporting checks over invented evaluation records."""
from __future__ import annotations

import copy
from decimal import Decimal
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import evaluation
import release


class EvaluationKit(unittest.TestCase):
    def setUp(self):
        self.environment = {"hostSurface": "invented-test-host", "model": "unknown",
                            "toolSettings": "synthetic unit records only", "packageVersion": "unknown",
                            "packageSha256": "unknown"}
        self.plan = evaluation.init_plan(ROOT, self.environment, repetitions=2, seed=31)
        self.kit_hash, self.case_version, self.cases = evaluation.load_kit(ROOT)

    def test_fixture_integrity_release_inclusion_and_independent_arithmetic(self):
        self.assertEqual(evaluation.validate_kit(ROOT)["uniqueCases"], 5)
        files = release.collect_project(ROOT)
        self.assertIn("evaluations/cases.json", files)
        self.assertTrue(all("evaluations/" + case[kind]["path"] in files
                            for case in self.cases.values() for kind in ("prompt", "answer")))
        rec = self.cases["reconciliation"]["expected"]
        earlier = sum(map(Decimal, ("150.25", "40.50", "-10.75")))
        later = sum(map(Decimal, ("157.75", "38.25", "-4")))
        self.assertEqual((rec["earlier_total"], rec["later_total"], rec["change"]),
                         (earlier, later, later - earlier))
        bridge = self.cases["quantity-price-fx"]["expected"]
        stages = [Decimal(80)*Decimal("12.5")*142, Decimal(92)*Decimal("12.5")*142,
                  Decimal(92)*Decimal("13.25")*142, Decimal(92)*Decimal("13.25")*139]
        self.assertEqual([bridge[k] for k in ("quantity_effect_jpy", "price_effect_jpy", "fx_effect_jpy")],
                         [stages[i+1]-stages[i] for i in range(3)])
        self.assertEqual(bridge["actual_jpy"] - bridge["plan_jpy"], sum(stages[i+1]-stages[i] for i in range(3)))

    def test_schedule_reproducible_counterbalanced_and_initially_unrun(self):
        self.assertEqual(self.plan, evaluation.init_plan(ROOT, self.environment, 2, 31))
        changed = evaluation.init_plan(ROOT, self.environment, 2, 32)
        self.assertNotEqual([r["id"] for r in self.plan["runs"]], [r["id"] for r in changed["runs"]])
        firsts = [r["condition"] for r in self.plan["runs"][::2]]
        self.assertEqual(firsts.count("baseline"), firsts.count("suite"))
        result = evaluation.summarize(ROOT, self.plan)
        self.assertEqual(result["totals"]["scheduled"], 20)
        self.assertEqual(result["totals"]["passed"], 0)
        self.assertEqual(result["totals"]["attempted"], 0)
        self.assertEqual(result["uniqueCases"], 5)
        self.assertEqual(result["pairedOutcomes"]["incomplete"], 10)

    def test_wrong_values_signs_types_and_missing_answers_cannot_pass(self):
        for name, key, bad in (("reconciliation", "change", True),
                               ("reconciliation", "added_effect", 4),
                               ("quantity-price-fx", "fx_quote", "USD per JPY"),
                               ("quantity-price-fx", "price_effect_jpy", "9798"),
                               ("ambiguous-mapping", "unresolved_total", 0),
                               ("cutoff-and-missing-input", "internal_forecast", 104),
                               ("cutoff-and-missing-input", "public_backfill", 0),
                               ("early-stop-and-source-coverage", "september_benchmark", 81),
                               ("early-stop-and-source-coverage", "total_pc", 35),
                               ("early-stop-and-source-coverage", "recalculation_verified", True)):
            answer = copy.deepcopy(self.cases[name]["expected"])
            answer[key] = bad
            with self.subTest(name=name, key=key):
                self.assertTrue(evaluation.differences(self.cases[name]["expected"], answer))
        row = self.plan["runs"][0]
        row["status"] = "completed"
        row["executedAt"] = "2024-05-06T14:30:00+09:00"
        self.assertEqual(evaluation.summarize(ROOT, self.plan)["totals"]["completedIncorrect"], 1)

    def test_status_denominators_and_paired_outcomes(self):
        for condition in evaluation.CONDITIONS:
            row = next(r for r in self.plan["runs"] if r["case"] == "reconciliation"
                       and r["repeat"] == 1 and r["condition"] == condition)
            row["status"] = "completed"
            row["executedAt"] = "2024-05-06T05:30:00Z"
            row["response"] = copy.deepcopy(self.cases[row["case"]]["expected"])
            if condition == "baseline":
                row["response"]["change"] = 13
        unused = [r for r in self.plan["runs"] if r["status"] == "not-run"]
        for row, status in zip(unused, ("failed", "refused", "interrupted", "unavailable")):
            row["status"] = status
            row["executedAt"] = "2024-05-06T05:31:00Z"
        result = evaluation.summarize(ROOT, self.plan)
        self.assertEqual(result, evaluation.summarize(ROOT, self.plan))
        self.assertEqual(result["totals"]["attempted"], 6)
        self.assertEqual(result["totals"]["completed"], 2)
        self.assertEqual(result["totals"]["passed"], 1)
        self.assertEqual(result["pairedOutcomes"]["suiteOnlyPassed"], 1)
        self.assertEqual(result["pairedOutcomes"]["incomplete"], 9)
        self.assertEqual(result["perCase"]["reconciliation"]["suite"]["passed"], 1)

    def test_case_and_package_versions_explicit_and_bound(self):
        self.assertEqual(self.plan["caseSetVersion"], "1.1.0")
        self.assertEqual(evaluation.summarize(ROOT, self.plan)["caseSetVersion"], "1.1.0")
        environment = {**self.environment, "packageVersion": "1.5.0"}
        older = evaluation.init_plan(ROOT, environment, 2, 31)
        self.assertEqual(evaluation.summarize(ROOT, older)["environment"]["packageVersion"], "1.5.0")
        for version in ("", "v1.5.0", "1.05.0", True):
            with self.subTest(version=version), self.assertRaises(ValueError):
                evaluation.init_plan(ROOT, {**self.environment, "packageVersion": version}, 2, 31)
        self.plan["caseSetVersion"] = "1.0.1"
        with self.assertRaisesRegex(ValueError, "different case-set"):
            evaluation.summarize(ROOT, self.plan)

    def test_attempt_timestamps_required_calendar_valid_and_timezone_aware(self):
        row = self.plan["runs"][0]
        row["executedAt"] = "2024-05-06T14:30:00+09:00"
        with self.assertRaisesRegex(ValueError, "Not-run"):
            evaluation.summarize(ROOT, self.plan)
        for status in evaluation.STATUSES[1:]:
            row["status"] = status
            row["executedAt"] = None
            with self.subTest(status=status), self.assertRaises(ValueError):
                evaluation.summarize(ROOT, self.plan)
        for timestamp in ("2024-02-30T09:00:00Z", "2024-05-06T14:30:00", "2024-05-06",
                          "2024-05-06T24:00:00Z", "2024-05-06T14:30:00+25:00", True):
            row["executedAt"] = timestamp
            with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                evaluation.summarize(ROOT, self.plan)
        for timestamp in ("2024-02-29T09:00:00Z", "2024-05-06T14:30:00.123456+09:00"):
            row["executedAt"] = timestamp
            result = evaluation.summarize(ROOT, self.plan)
            self.assertEqual(result["runs"][0]["executedAt"], timestamp)

    def test_missing_duplicate_reordered_and_modified_schedule_rejected(self):
        for change in (lambda p: p["runs"].pop(),
                       lambda p: p["runs"].__setitem__(1, copy.deepcopy(p["runs"][0])),
                       lambda p: p["runs"].reverse(),
                       lambda p: p["runs"][0].__setitem__("repeat", True),
                       lambda p: p.__setitem__("seed", True),
                       lambda p: p["runs"][0].__setitem__("status", "passed"),
                       lambda p: p["runs"][0].__setitem__("response", {})):
            plan = copy.deepcopy(self.plan)
            change(plan)
            with self.assertRaises(ValueError):
                evaluation.summarize(ROOT, plan)

    def test_tampered_fixtures_and_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "evaluations", root / "evaluations")
            prompt = root / "evaluations/prompts/reconciliation.md"
            prompt.write_text(prompt.read_text() + "\nChanged prompt.\n")
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                evaluation.validate_kit(root)
            manifest = root / "evaluations/cases.json"
            values = json.loads(manifest.read_text())
            for case in values["cases"]:
                if case["id"] == "reconciliation":
                    case["prompt"]["sha256"] = evaluation.digest(prompt.read_bytes())
            manifest.write_text(json.dumps(values))
            with self.assertRaisesRegex(ValueError, "different kit"):
                evaluation.summarize(root, self.plan)

    def test_strict_json_and_nonfinite_records_rejected(self):
        for raw in ('{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}', '{"x":1,"x":2}'):
            with self.assertRaises(ValueError):
                evaluation.strict_json(raw)
        for invalid in (float("nan"), float("inf"), Decimal("NaN")):
            plan = copy.deepcopy(self.plan)
            plan["runs"][0]["response"] = {"x": invalid}
            with self.assertRaises(ValueError):
                evaluation.summarize(ROOT, plan)
        self.assertTrue(evaluation.differences({"value": Decimal("0.1")}, {"value": "0.1"}))
        self.assertFalse(evaluation.differences({"value": Decimal("0.1")}, {"value": Decimal("0.10")}))

    def test_public_output_and_overwrite_refused_cli_smoke(self):
        with self.assertRaisesRegex(ValueError, "outside the public"):
            evaluation.write_new(ROOT / "evaluations/result.json", self.plan)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "plan.json"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluation.py"), "init-plan",
                                     "--output", str(target), "--host-surface", "invented-test-host",
                                     "--repetitions", "1", "--seed", "4"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["scheduled"], 10)
            summary = subprocess.run([sys.executable, str(ROOT / "scripts/evaluation.py"), "summarize", str(target)],
                                     capture_output=True, text=True)
            self.assertEqual(summary.returncode, 0, summary.stderr)
            self.assertEqual(json.loads(summary.stdout)["totals"]["passed"], 0)
            with self.assertRaises(FileExistsError):
                evaluation.write_new(target, self.plan)


if __name__ == "__main__":
    unittest.main()
