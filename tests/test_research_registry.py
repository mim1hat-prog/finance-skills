"""Research release gates, with independently invented sources and notices."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import research_registry as registry


class ResearchRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "research").mkdir()
        (self.root / "skills/example-skill").mkdir(parents=True)
        (self.root / "skills/example-skill/SKILL.md").write_text("# Invented example\n")
        (self.root / "tests").mkdir()
        (self.root / "tests/test_example.py").write_text(
            "class ExampleTests:\n    def test_evidence(self):\n        pass\n")
        self.catalog = {"skills": [{"name": "example-skill", "researchIds": ["invented-source"]}]}
        self.source = {
            "id": "invented-source", "type": "empirical-research",
            "title": "Invented source used only by tests", "publisher": "Example publisher",
            "authors": ["Example research group"], "year": 2025,
            "url": "https://example.org/research", "doi": "10.0000/example-test",
            "edition": "Synthetic version 1", "accessedOn": "2026-11-25",
            "lastReviewedOn": "2026-11-25", "maintainerRole": "Research maintainer",
            "reviewStatus": "reviewed", "reviewNotes": "Synthetic source; not real evidence.",
            "license": {
                "name": "Synthetic test permission", "termsUrl": "https://example.org/terms",
                "attribution": "Invented source", "rawRedistribution": "allowed-with-conditions",
                "derivedRedistribution": "allowed-with-conditions", "checkedOn": "2026-11-25",
                "notes": "No upstream content is present."
            },
            "uses": [{"skills": ["example-skill"], "paths": ["skills/example-skill/SKILL.md"],
                      "section": "Synthetic section", "purpose": "Exercise reference resolution.",
                      "limits": "Not a production method.", "distribution": "metadata-only",
                      "tests": ["tests/test_example.py::ExampleTests.test_evidence"]}],
            "updates": []
        }
        self.write()

    def write(self, regenerate=True):
        (self.root / "catalog.json").write_text(json.dumps(self.catalog))
        (self.root / registry.REGISTRY).write_text(json.dumps({"schemaVersion": 1, "sources": [self.source]}))
        if regenerate:
            for path, content in registry.generate(self.root).items():
                (self.root / path).write_bytes(content)

    def report(self):
        self.write()
        return registry.validate(self.root)

    def assert_error(self, phrase):
        result = self.report()
        self.assertFalse(result["ok"])
        self.assertTrue(any(phrase in e for e in result["errors"]), result)

    def test_valid_registry_is_deterministic_and_read_only(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertTrue(registry.validate(self.root)["ok"])
        self.assertEqual(registry.generate(self.root), registry.generate(self.root))
        after = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_unknown_research_id_blocks_release(self):
        self.catalog["skills"][0]["researchIds"] = ["nonexistent-source"]
        self.assert_error("unknown research ID")

    def test_retracted_source_blocks_release(self):
        self.source["reviewStatus"] = "retracted"
        self.source["updates"] = [{"kind": "retraction", "url": "https://example.org/retraction",
                                  "reviewedOn": "2026-11-25", "assessment": "Synthetic notice.",
                                  "disposition": "reviewed-no-method-change"}]
        self.assert_error("referenced source is retracted")

    def test_unresolved_correction_blocks_release(self):
        self.source["updates"] = [{"kind": "correction", "url": "https://example.org/correction",
                                  "detectedOn": "2026-11-25", "reviewedOn": None, "assessment": "Review not finished.",
                                  "disposition": "needs-review"}]
        self.assert_error("affected-method review")

    def test_unresolved_candidate_cannot_be_cited_as_active_support(self):
        self.source["integrationStatus"] = "candidate"
        self.source["candidateReason"] = "Correction was detected but not read."
        self.source["reviewStatus"] = "needs-review"
        self.source["uses"] = []
        self.assert_error("candidate source")

    def test_unresolved_candidate_visible_without_active_use(self):
        candidate = copy.deepcopy(self.source)
        candidate["id"] = "candidate-source"
        candidate["integrationStatus"] = "candidate"
        candidate["candidateReason"] = "Correction was detected but not read."
        candidate["reviewStatus"] = "needs-review"
        candidate["uses"] = []
        candidate["updates"] = [{"kind": "correction", "url": "https://example.org/correction",
                                 "detectedOn": "2026-11-25", "reviewedOn": None,
                                 "assessment": "Content unavailable; excluded from method support.",
                                 "disposition": "needs-review"}]
        (self.root / registry.REGISTRY).write_text(json.dumps({"schemaVersion": 1, "sources": [self.source, candidate]}))
        for path, content in registry.generate(self.root).items():
            (self.root / path).write_bytes(content)
        report = registry.validate(self.root)
        self.assertTrue(report["ok"], report)
        self.assertIn("Candidate; no active use", (self.root / registry.GENERATED).read_text())

    def test_reviewed_link_correction_can_preserve_method(self):
        self.source["updates"] = [{"kind": "addendum", "url": "https://example.org/addendum",
                                  "reviewedOn": "2026-11-25", "assessment": "Link changed; method unchanged.",
                                  "disposition": "reviewed-no-method-change"}]
        self.assertTrue(self.report()["ok"])

    def test_superseded_source_blocks_release(self):
        self.source["reviewStatus"] = "superseded"
        self.assert_error("referenced source is superseded")

    def test_unimplemented_path_is_not_integrated(self):
        self.source["uses"][0]["paths"].append("scripts/not-implemented.py")
        self.assert_error("missing target")

    def test_unknown_test_symbol_blocks_release(self):
        self.source["uses"][0]["tests"] = ["tests/test_example.py::ExampleTests.not_a_test"]
        self.assert_error("unresolved test")

    def test_source_must_name_exact_skill_use(self):
        self.source["uses"][0]["skills"] = []
        self.assert_error("no matching use for this skill")

    def test_secret_in_url_blocks_release(self):
        self.source["url"] = "https://example.org/api?" + "appId" + "=" + "synthetic-forbidden-value"
        self.assert_error("without credentials")

    def test_missing_rights_block_values_but_allow_metadata(self):
        self.source["license"]["rawRedistribution"] = "unknown"
        self.source["license"]["derivedRedistribution"] = "unknown"
        self.assertTrue(self.report()["ok"])
        self.source["uses"][0]["distribution"] = "data-values"
        self.assert_error("unresolved redistribution rights")

    def test_generated_readme_is_checked(self):
        (self.root / registry.GENERATED).write_text("stale generated file\n")
        result = registry.validate(self.root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("Generated artifact differs" in e for e in result["errors"]))

    def test_benchmark_research_id_resolves(self):
        (self.root / "benchmarks").mkdir()
        (self.root / "benchmarks/catalog.json").write_text(json.dumps({"research_ids": ["not-found"]}))
        self.assert_error("benchmarks/catalog.json: unknown research ID")

    def test_catalog_cannot_override_source_redistribution_limit(self):
        self.source["license"]["rawRedistribution"] = "permission-required"
        (self.root / "benchmarks").mkdir()
        (self.root / "benchmarks/catalog.json").write_text(json.dumps({"series": [{
            "id": "example-series", "source_id": "invented-source", "series_kind": "original",
            "rights": {"redistribution": "permitted"}}]}))
        self.assert_error("redistribution conflicts with source")

    def test_path_cannot_escape_repository(self):
        self.source["uses"][0]["paths"].append("../outside.txt")
        self.assert_error("inside the repository")

    def test_changed_upstream_pin_requires_new_research_review(self):
        self.source["id"] = "upstream-example"
        self.source["url"] = "https://github.com/example/project/tree/old-pin"
        self.catalog["skills"][0]["researchIds"] = ["upstream-example"]
        (self.root / "upstream.lock.json").write_text(json.dumps({"sources": [{
            "id": "example", "repository": "example/project", "commit": "new-pin",
            "appliedSkills": ["example-skill"]}]}))
        self.assert_error("pinned upstream changed")

    def test_crossref_notice_requires_review_without_mutation(self):
        before = copy.deepcopy(self.source)
        response = {"message": {"DOI": self.source["doi"], "updated-by": [{"DOI": "10.0000/test-notice", "type": "retraction"}]}}
        result = registry.inspect_crossref(self.source, lambda url: response)
        self.assertEqual(result["status"], "review-required")
        self.assertEqual(result["updates"][0]["type"], "retraction")
        self.assertEqual(self.source, before)
        self.assertFalse(result["mutated"])

    def test_update_failure_is_unknown(self):
        def failed(url):
            raise OSError("Synthetic unavailable upstream; never serialize this exception text")
        result = registry.inspect_crossref(self.source, failed)
        self.assertEqual(result["status"], "unavailable")
        self.assertNotIn("Synthetic unavailable", json.dumps(result))
        self.assertEqual(self.source["reviewStatus"], "reviewed")

    def test_recorded_addendum_does_not_approve_a_new_notice(self):
        self.source["updates"] = [{"kind": "addendum", "doi": "10.0000/known",
                                  "url": "https://doi.org/10.0000/known", "reviewedOn": "2026-11-25",
                                  "assessment": "Synthetic link correction.",
                                  "disposition": "reviewed-no-method-change"}]
        payload = {"message": {"DOI": self.source["doi"], "updated-by": [
            {"DOI": "10.0000/known", "type": "addendum"}]}}
        known = registry.inspect_crossref(self.source, lambda url: payload)
        self.assertEqual(known["status"], "recorded-updates")
        payload["message"]["updated-by"].append({"DOI": "10.0000/new-notice", "type": "correction"})
        changed = registry.inspect_crossref(self.source, lambda url: payload)
        self.assertEqual(changed["status"], "review-required")
        self.assertFalse(changed["mutated"])

    def test_empty_update_response_does_not_establish_no_retraction(self):
        result = registry.inspect_crossref(self.source, lambda url: {"message": {"DOI": self.source["doi"]}})
        self.assertEqual(result["status"], "no-update-reported")
        self.assertIn("publisher review is still required", result["detail"])

    def test_malformed_update_response_is_unknown(self):
        result = registry.inspect_crossref(self.source, lambda url: {"message": {}})
        self.assertEqual(result["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
