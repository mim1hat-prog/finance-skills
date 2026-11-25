from copy import deepcopy
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
import workflow_controls as controls
from schema_validation import validate, SchemaValidationError, UnsupportedSchemaError


def fixture(name):
    return json.loads((ROOT / "examples/workflows" / (name + ".json")).read_text())


def codes(result):
    return {issue["code"] for issue in result["issues"]}


def context(stream="approved_internal_figures"):
    value = fixture("provision-residual")["stages"][0]["context"]
    value["stream"] = stream
    return value


class SchemaSubsetTests(unittest.TestCase):
    def test_enforced_keywords_refs_formats_and_unknown_keyword_fail_closed(self):
        schema = {"type": "object", "$defs": {"id": {"type": "string", "minLength": 2, "maxLength": 3, "pattern": "^[a-z]+$"}},
                  "properties": {"id": {"$ref": "#/$defs/id"}, "count": {"type": "integer", "minimum": 1, "exclusiveMaximum": 3}},
                  "required": ["id", "count"], "additionalProperties": False}
        validate({"id": "ab", "count": 1}, schema)
        for invalid in ({"id": "ab"}, {"id": "A", "count": 1}, {"id": "abcd", "count": 1},
                        {"id": "ab", "count": True}, {"id": "ab", "count": 3}, {"id": "ab", "count": 1, "extra": 0}):
            with self.subTest(invalid=invalid), self.assertRaises(SchemaValidationError):
                validate(invalid, schema)
        for schema in ({"not": {}}, {"oneOf": [{"const": 1}, {"type": "string", "unimplemented": True}]}, {"format": "email"}):
            with self.assertRaises(UnsupportedSchemaError):
                validate(1, schema)
        validate("about:blank", {"type": "string", "format": "uri"})
        validate("2032-02-29T23:00:00+02:00", {"format": "date-time"})
        for value, kind in [("2031-02-29", "date"), ("2032-04-30T12:00:00", "date-time"),
                            ("2032-04-30T18:00:00+00:99", "date-time"), ("2032-04-30T18:00:00+23:99", "date-time"),
                            ("2032-04-30T18:00:00+24:00", "date-time"), ("relative/path", "uri")]:
            with self.assertRaises(SchemaValidationError):
                validate(value, {"format": kind})
        validate("ok", {"$ref": "local.json#/$defs/text"}, resolver=lambda name: {"$defs": {"text": {"const": "ok"}}})
        with self.assertRaises(UnsupportedSchemaError):
            validate(1, {"$ref": "unavailable.json"})

    def test_json_type_equality_uniqueness_boolean_and_nonfinite_values(self):
        validate([True, 1], {"type": "array", "uniqueItems": True, "minItems": 2, "maxItems": 2})
        for value, schema in [([1, 1.0], {"uniqueItems": True}),
                              ([{"x": [1]}, {"x": [1.0]}], {"uniqueItems": True}),
                              (True, {"const": 1}), (False, {"enum": [0]}),
                              (float("nan"), {}), ([], {"minItems": 1}), ([1, 2], {"maxItems": 1})]:
            with self.subTest(value=value), self.assertRaises(SchemaValidationError):
                validate(value, schema)


class WorkflowControlsTests(unittest.TestCase):
    def assert_read_only_state(self, result):
        self.assertEqual(result["actionState"], "not-executed")
        self.assertEqual(result["submissionState"], "not-established")
        controls.validate_contract(result, "result")

    def test_partial_provision_explanation_retains_component_and_total_residual(self):
        request = fixture("provision-residual")
        before = deepcopy(request)
        result = controls.check(request)
        self.assertEqual(request, before)
        self.assertEqual(result["evidenceStatus"], "blocked")
        compared = result["details"][:5]
        self.assertEqual(next(x for x in compared if x["movement"] == "additions")["residual"], "0")
        self.assertEqual(next(x for x in compared if x["movement"] == "utilization")["residual"], "-1")
        self.assertEqual(result["metrics"]["comparisons"][0]["closingDifference"], "2")
        self.assertEqual(result["metrics"]["comparisons"][0]["unexplainedNetResidual"], "-1")
        self.assertIn("unexplained_movement", codes(result))
        self.assert_read_only_state(result)

    def test_explained_difference_is_not_equal_snapshots_and_latest_cannot_replace_requested_version(self):
        request = fixture("provision-residual")
        request["explanations"][1]["amount"] = "-3"
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "validated")
        self.assertIn("values still differ", result["answer"])
        request["stages"][1]["context"]["version"] = "scenario-f2"
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "blocked")
        self.assertIn("requested_version_unavailable", codes(result))
        self.assertEqual(result["details"], [])

    def test_overlapping_explanations_are_excluded_instead_of_counted_twice(self):
        request = fixture("provision-residual")
        request["stages"] = request["stages"][:2]
        first = {"fromStage": "overview", "toStage": "detail", "movement": "additions",
                 "amount": "2.5", "evidenceRef": "urn:synthetic:one-driver"}
        second = {"fromStage": "overview", "toStage": "detail", "movement": "utilization",
                  "amount": "-3", "evidenceRef": "urn:synthetic:second-driver"}
        request["explanations"] = [first, deepcopy(first), second]
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "blocked")
        self.assertIn("duplicate_explanation", codes(result))
        addition = next(item for item in result["details"] if item["movement"] == "additions")
        self.assertEqual(addition["explained"], "0")
        self.assertEqual(addition["residual"], "5")
        request["explanations"] = [first, second]
        result = controls.check(request)
        addition = next(item for item in result["details"] if item["movement"] == "additions")
        self.assertEqual(addition["residual"], "2.5")
        first["amount"] = "5"
        first["componentId"] = second["componentId"] = "same-component"
        self.assertIn("duplicate_explanation", codes(controls.check(request)))

    def test_whitespace_only_evidence_owners_and_coordinate_identifiers_are_rejected(self):
        request = fixture("provision-residual")
        request["explanations"][1]["amount"] = "-3"
        request["explanations"][0]["evidenceRef"] = "   "
        with self.assertRaises(SchemaValidationError):
            controls.check(request)
        case = {"scope": "sample-region", "ownerRole": "case-owner", "status": "confirmed-none",
                "caseCount": 0, "confirmedAt": "2032-04-30T09:00:00Z", "evidenceRef": "urn:synthetic:confirmation"}
        for field in ("scope", "ownerRole", "evidenceRef"):
            item = deepcopy(case)
            item[field] = " \t "
            with self.subTest(field=field), self.assertRaises(SchemaValidationError):
                controls.check({"schemaVersion": 1, "operation": "case-status", "context": context("internal_workflow_status"), "cases": [item]})
        for field in ("member", "dimension", "model"):
            request = fixture("readback-intersections")
            request["observed"]["rows"] = deepcopy(request["expected"]["rows"])
            for target in (request["expected"], request["observed"]):
                if field == "member":
                    target["rows"][0]["members"][0] = " "
                elif field == "dimension":
                    target["dimensions"][0] = " "
                else:
                    target["model"] = " "
            with self.subTest(field=field), self.assertRaises(SchemaValidationError):
                controls.check(request)

    def test_declared_scale_sign_and_source_precision_preserve_raw_values(self):
        request = fixture("provision-residual")
        request["stages"] = request["stages"][:2]
        request["explanations"] = []
        left, right = request["stages"]
        left["context"]["unitScale"] = "1000"
        left["movements"] = {"opening": "1.2300", "additions": "0.0101", "releases": "-0.0030",
                             "utilization": "-0.0200", "other": "0.0002", "closing": "1.2173"}
        right["context"]["signMultiplier"] = -1
        right["movements"] = {key: str(-Decimal(value) * 1000) for key, value in left["movements"].items()}
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "reconciled")
        self.assertEqual(result["details"][0]["rawFrom"], "1.2300")
        self.assertEqual(Decimal(result["details"][0]["normalizedFrom"]), Decimal("1230"))
        self.assertTrue(all(Decimal(x["residual"]) == 0 for x in result["details"]))
        self.assert_read_only_state(result)

    def test_net_zero_does_not_hide_gross_unexplained_components_or_detail_rounding(self):
        request = fixture("provision-residual")
        request["stages"] = request["stages"][:2]
        request["explanations"] = []
        request["tolerance"]["amount"] = "1"
        request["stages"][1]["movements"] = deepcopy(request["stages"][0]["movements"])
        request["stages"][1]["movements"]["additions"] = "24.7"
        request["stages"][1]["movements"]["utilization"] = "-12.7"
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "blocked")
        self.assertEqual(Decimal(result["metrics"]["comparisons"][0]["unexplainedNetResidual"]), 0)
        self.assertEqual(Decimal(result["metrics"]["comparisons"][0]["unexplainedGrossResidual"]), Decimal("1.4"))
        self.assertIn("unexplained_total", codes(result))

    def test_context_tolerance_and_decimal_boundaries_are_explicit(self):
        request = fixture("provision-residual")
        request["tolerance"]["effectiveTo"] = "2032-03-31"
        self.assertIn("tolerance_not_effective", codes(controls.check(request)))
        request = fixture("provision-residual")
        request["stages"][1]["context"]["sourceSnapshot"]["asOf"] = "2032-05-01T10:00:00Z"
        self.assertIn("snapshot_after_cutoff", codes(controls.check(request)))
        for value in ("NaN", "1e29", "12345678901234567890123456789"):
            request = fixture("provision-residual")
            request["stages"][0]["movements"]["opening"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                controls.check(request)
        request = fixture("provision-residual")
        request["tolerance"]["amount"] = "-1"
        with self.assertRaises(ValueError):
            controls.check(request)

    def test_successful_refresh_cannot_hide_protected_population_or_schema_regression(self):
        request = fixture("workforce-regression")
        before = deepcopy(request)
        result = controls.check(request)
        self.assertEqual(request, before)
        self.assertEqual(result["evidenceStatus"], "blocked")
        self.assertIn("protected_output_regression", codes(result))
        self.assertIn("artifact_contract_changed", codes(result))
        self.assertFalse(result["metrics"]["contractCompatible"])
        self.assertFalse(result["metrics"]["replacementPerformed"])
        self.assert_read_only_state(result)

    def compatible_artifact(self):
        request = fixture("workforce-regression")
        request["candidate"] = deepcopy(request["baseline"])
        request["candidate"]["context"]["sourceSnapshot"]["id"] = "synthetic-candidate"
        return request

    def test_scoped_replacement_and_append_preserve_history_with_native_checks_separate(self):
        request = self.compatible_artifact()
        request["candidate"]["rows"].append({"period": "2032-04", "person": "sample-c", "scenario": "actual", "hours": "100", "amount": "2800"})
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "validated")
        request["refresh"] = {"status": "not-run", "locator": ""}
        self.assertEqual(controls.check(request)["evidenceStatus"], "unverified")
        request = self.compatible_artifact()
        request["changeMode"] = "replace-scoped"
        request["scopeKeys"] = [["2032-04", "sample-b", "actual"]]
        request["candidate"]["rows"][2]["amount"] = "3750"
        self.assertEqual(controls.check(request)["evidenceStatus"], "validated")
        request["candidate"]["rows"][1]["amount"] = "3400"
        self.assertIn("protected_output_regression", codes(controls.check(request)))

    def test_duplicate_business_keys_and_typed_cells_fail_even_if_refresh_succeeded(self):
        request = self.compatible_artifact()
        request["candidate"]["rows"].append(deepcopy(request["candidate"]["rows"][0]))
        self.assertIn("duplicate_business_key", codes(controls.check(request)))
        request = self.compatible_artifact()
        request["candidate"]["rows"][0]["hours"] = "not-numeric"
        self.assertIn("cell_type_mismatch", codes(controls.check(request)))

    def test_artifact_raw_records_cannot_change_scale_sign_or_use_blank_business_keys(self):
        for field, value in (("unitScale", "1000"), ("signMultiplier", -1)):
            request = self.compatible_artifact()
            request["candidate"]["context"][field] = value
            result = controls.check(request)
            self.assertEqual(result["evidenceStatus"], "blocked")
            self.assertFalse(result["metrics"]["contractCompatible"])
            self.assertIn("artifact_semantic_context_changed", codes(result))
        request = self.compatible_artifact()
        request["candidate"]["context"]["unitScale"] = "1.000"
        self.assertEqual(controls.check(request)["evidenceStatus"], "validated")
        for artifact in (request["baseline"], request["candidate"]):
            artifact["rows"][0]["person"] = " "
        self.assertIn("missing_business_key", codes(controls.check(request)))

    def test_missing_ambiguous_future_unapproved_and_incomplete_mappings_are_not_guessed(self):
        rule = {"key": "complete", "fields": {"department": "sample-dept", "location": "sample-site"},
                "validFrom": "2032-01-01", "validTo": "2032-12-31", "approvalRef": "urn:synthetic:approved-rule"}
        request = {"schemaVersion": 1, "operation": "mapping", "context": context(),
                   "keys": ["complete", "missing", "future", "duplicate", "incomplete", "unapproved"],
                   "requiredFields": ["department", "location"], "rules": [rule]}
        request["rules"] += [dict(deepcopy(rule), key="future", validFrom="2033-01-01", validTo="2033-12-31"),
                              dict(deepcopy(rule), key="duplicate"), dict(deepcopy(rule), key="duplicate"),
                              dict(deepcopy(rule), key="incomplete", fields={"department": "sample-dept"}),
                              dict(deepcopy(rule), key="unapproved", approvalRef="")]
        before = deepcopy(request)
        result = controls.check(request)
        self.assertEqual(request, before)
        self.assertEqual([x["status"] for x in result["details"]],
                         ["matched", "mapping_missing", "mapping_not_effective", "ambiguous_mapping", "mapping_incomplete", "mapping_not_approved"])
        self.assertTrue(all(x["fields"] is None for x in result["details"][1:]))
        self.assertFalse(result["metrics"]["masterModified"])

    def test_readback_checks_target_intersections_not_only_grand_total(self):
        request = fixture("readback-intersections")
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "blocked")
        self.assertEqual(result["metrics"]["netDifference"], "0")
        self.assertEqual(result["metrics"]["grossAbsoluteDifference"], "30")
        self.assertEqual(sum(x["matched"] for x in result["details"]), 0)
        request["observed"]["rows"] = deepcopy(request["expected"]["rows"])
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "reconciled")
        self.assert_read_only_state(result)
        request["observed"]["dimensions"].reverse()
        self.assertIn("reporting_target_mismatch", codes(controls.check(request)))

    def test_failed_cached_blank_or_empty_reads_never_become_zero_activity(self):
        request = fixture("readback-intersections")
        request["read"]["state"] = "failed"
        request["read"]["errorSuppressed"] = True
        request["observed"]["rows"] = []
        result = controls.check(request)
        self.assertIn("read_failed", codes(result))
        self.assertEqual(result["metrics"], {})
        request["read"]["state"] = "cached"
        request["read"]["errorSuppressed"] = False
        self.assertEqual(controls.check(request)["evidenceStatus"], "unverified")
        request = fixture("readback-intersections")
        request["observed"]["rows"][0]["value"] = None
        result = controls.check(request)
        self.assertIn("blank_value_unverified", codes(result))
        self.assertEqual(result["evidenceStatus"], "blocked")
        request["expected"]["rows"] = []
        request["observed"]["rows"] = []
        self.assertIn("expected_population_missing", codes(controls.check(request)))

    def test_granularity_and_three_streams_do_not_backfill_internal_inputs(self):
        request = {"schemaVersion": 1, "operation": "granularity", "context": context(), "measure": "personnel-cost",
                   "availableDimensions": ["cost_center"], "requiredDimensions": ["cost_center", "job_rank"]}
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "blocked")
        self.assertEqual(result["metrics"]["missingDimensions"], ["job_rank"])
        self.assertFalse(result["metrics"]["inferredValues"])
        request["availableDimensions"].append("job_rank")
        request["context"]["stream"] = "public_benchmarks"
        self.assertIn("wrong_data_stream", codes(controls.check(request)))
        provision = fixture("provision-residual")
        provision["stages"][0]["context"]["stream"] = "internal_workflow_status"
        result = controls.check(provision)
        self.assertIn("wrong_data_stream", codes(result))
        self.assertEqual(result["details"], [])

    def test_case_coverage_requires_owner_scope_and_dated_explicit_zero_confirmation(self):
        request = {"schemaVersion": 1, "operation": "case-status", "context": context("internal_workflow_status"),
                   "cases": [{"scope": "sample-region-a", "ownerRole": "case-owner", "status": "not-requested"},
                             {"scope": "sample-region-b", "ownerRole": "case-owner", "status": "awaiting-confirmation"}]}
        result = controls.check(request)
        self.assertEqual(codes(result), {"not_requested", "awaiting_confirmation"})
        for item in request["cases"]:
            item.update(status="confirmed-none", caseCount=0, confirmedAt="2032-04-30T09:00:00Z", evidenceRef="urn:synthetic:confirmation")
        self.assertEqual(controls.check(request)["evidenceStatus"], "validated")
        request["cases"][0].pop("confirmedAt")
        self.assertIn("confirmation_evidence_missing", codes(controls.check(request)))
        request["cases"][0]["confirmedAt"] = "2032-05-01T09:00:00Z"
        self.assertIn("confirmation_after_cutoff", codes(controls.check(request)))

    def allocation(self):
        payload = {"sender": "sample-sender", "amount": "12", "configurationVersion": "sample-config-1",
                   "receivers": [{"member": "sample-a", "weight": "0.6"}, {"member": "sample-b", "weight": "0.4"}]}
        return {"schemaVersion": 1, "operation": "allocation-preflight", "context": context("internal_workflow_status"),
                "target": "synthetic-model/forecast/scope-a", "payload": payload,
                "approval": {"target": "synthetic-model/forecast/scope-a", "payloadSha256": controls.payload_sha256(payload),
                             "expiresAt": "2032-04-30T19:00:00Z", "evidenceRef": "urn:synthetic:approval"},
                "configuration": {"version": "sample-config-1", "sender": "sample-sender", "validFrom": "2032-01-01", "validTo": "2032-12-31",
                                  "membershipEvidence": "urn:synthetic:membership", "permissionEvidence": "urn:synthetic:permissions",
                                  "lockState": "unlocked", "receivers": [{"member": "sample-a", "weight": "0.6"}, {"member": "sample-b", "weight": "0.4"}]},
                "priorRun": {"status": "confirmed-not-executed", "checkedAt": "2032-04-30T17:00:00Z", "evidenceRef": "urn:synthetic:status-read",
                             "target": "synthetic-model/forecast/scope-a", "payloadSha256": controls.payload_sha256(payload)}}

    def test_allocation_locks_duplicate_run_risk_timeout_and_exact_binding_block_execution(self):
        request = self.allocation()
        before = deepcopy(request)
        result = controls.check(request)
        self.assertEqual(result["evidenceStatus"], "validated")
        self.assertEqual(request, before)
        self.assert_read_only_state(result)
        request["configuration"]["lockState"] = "locked"
        request["priorRun"]["status"] = "unknown"
        result = controls.check(request)
        self.assertIn("sender_locked_or_unknown", codes(result))
        self.assertIn("duplicate_run_risk", codes(result))
        request = self.allocation()
        request["lastAttempt"] = {"outcome": "timed-out", "at": "2032-04-30T17:05:00Z"}
        self.assertIn("timeout_readback_required", codes(controls.check(request)))
        request = self.allocation()
        request["payload"]["amount"] = "13"
        self.assertIn("approval_binding_invalid", codes(controls.check(request)))
        request = self.allocation()
        request["configuration"]["receivers"][0]["weight"] = "0.5"
        self.assertIn("receiver_weights_invalid", codes(controls.check(request)))

    def test_allocation_payload_configuration_and_prior_evidence_must_identify_same_action(self):
        request = self.allocation()
        request["configuration"]["receivers"] = [{"member": "different-sample-receiver", "weight": "1"}]
        self.assertIn("payload_configuration_mismatch", codes(controls.check(request)))
        request = self.allocation()
        request["configuration"]["receivers"][0]["weight"] = "0.7"
        request["configuration"]["receivers"][1]["weight"] = "0.3"
        self.assertIn("payload_configuration_mismatch", codes(controls.check(request)))
        for field, value in (("sender", "different-sample-sender"), ("version", "sample-config-2")):
            request = self.allocation()
            request["configuration"][field] = value
            self.assertIn("payload_configuration_mismatch", codes(controls.check(request)))
        request = self.allocation()
        request["target"] = request["approval"]["target"] = "synthetic-model/forecast/other-scope"
        self.assertIn("prior_run_binding_invalid", codes(controls.check(request)))
        request = self.allocation()
        request["payload"]["amount"] = "13"
        request["approval"]["payloadSha256"] = controls.payload_sha256(request["payload"])
        self.assertIn("prior_run_binding_invalid", codes(controls.check(request)))

    def test_cli_contract_exit_codes_and_input_files_remain_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "schemas").mkdir()
            for name in ("workflow_controls.py", "schema_validation.py", "finance_tools.py"):
                shutil.copyfile(ROOT / "scripts" / name, root / "scripts" / name)
            for file in (ROOT / "schemas").glob("workflow-*.schema.json"):
                shutil.copyfile(file, root / "schemas" / file.name)
            path = root / "request.json"
            path.write_text(json.dumps(fixture("provision-residual")))
            before = {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file()}
            run = subprocess.run([sys.executable, "-E", str(root / "scripts/workflow_controls.py"), "check", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2, run.stderr)
            self.assertEqual(json.loads(run.stdout)["evidenceStatus"], "blocked")
            after = {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            run = subprocess.run([sys.executable, "-E", str(root / "scripts/workflow_controls.py"), "validate", "--schema", "request", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            path.write_text('{"schemaVersion":1,"schemaVersion":2}')
            run = subprocess.run([sys.executable, "-E", str(root / "scripts/workflow_controls.py"), "check", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertIn("Duplicate JSON", run.stderr)


if __name__ == "__main__":
    unittest.main()
