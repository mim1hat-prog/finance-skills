import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import catalog_contracts


class RoutingContracts(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "tools").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "tests/test_sample.py").write_text("class Cases:\n    def test_rule(self):\n        pass\n")
        self.catalog = {"version": "1.2.0", "skills": [{"name": "sample", "title": "Sample workflow", "researchIds": ["sample-source"], "contract": {
            "triggers": ["inspect a sample"], "requiredInputs": ["approved sample"], "outputs": ["scoped result"],
            "modes": ["inspect", "validate"], "conditionalModes": [], "sharedProcedure": "workflow-controls-v1",
            "optionalCapabilities": ["local-calculation"], "validation": {"nativeStatus": "not-validated",
            "packageTests": ["tests/test_sample.py::Cases.test_rule"], "workflowTests": []}}}]}
        self.tools = {"schemaVersion": 1, "reviewedOn": "2026-11-25", "availabilityNotes": {"confirm-at-work": "Check the actual environment."}, "tools": [{
            "id": "sample-tool", "name": "Sample tool", "group": "Optional", "priority": "P1", "availability": "confirm-at-work",
            "repositorySupport": "instructions-and-export-checks", "financeUse": "Sample inspection", "actions": ["Inspect supplied data"],
            "requiredEvidence": ["Input scope"], "skillIds": ["sample"], "researchIds": []}]}
        self.write_tools()

    def write_tools(self):
        (self.root / "tools/catalog.json").write_text(json.dumps(self.tools))

    def test_unknown_tool_routing_or_unsupported_availability_fails(self):
        self.tools["tools"][0]["skillIds"] = ["nonexistent"]
        self.write_tools()
        with self.assertRaisesRegex(ValueError, "unknown workflow"):
            catalog_contracts.generate(self.root, self.catalog)
        self.tools["tools"][0]["skillIds"] = ["sample"]
        self.tools["tools"][0]["availability"] = "automatically-installed"
        self.write_tools()
        with self.assertRaisesRegex(ValueError, "invalid support"):
            catalog_contracts.generate(self.root, self.catalog)

    def test_removed_test_symbol_and_unsupported_native_claim_fail(self):
        contract = self.catalog["skills"][0]["contract"]
        contract["validation"]["workflowTests"] = ["tests/test_sample.py::Cases.test_missing"]
        with self.assertRaisesRegex(ValueError, "Missing test symbol"):
            catalog_contracts.generate(self.root, self.catalog)
        contract["validation"]["workflowTests"] = []
        contract["validation"]["nativeStatus"] = "production-ready"
        with self.assertRaisesRegex(ValueError, "native validation"):
            catalog_contracts.generate(self.root, self.catalog)

    def test_generated_catalogues_distinguish_package_only_from_native_and_do_not_write(self):
        before = copy.deepcopy(self.catalog)
        files = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        outputs = catalog_contracts.generate(self.root, self.catalog)
        self.assertEqual(self.catalog, before)
        self.assertEqual(files, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertIn(b"No automated end-to-end workflow coverage claimed", outputs[Path("docs/SKILL-CONTRACTS.md")])
        self.assertIn(b"does not install", outputs[Path("TOOLS.md")])


if __name__ == "__main__":
    unittest.main()
