"""Read-only checks over supplied workflow snapshots and evidence.

No live connector, refresh, write, approval or submission is performed. Decimal
inputs are strings in the same supported 28-digit range as finance_tools.
Declared scale/sign normalize amounts to base currency units; raw amounts stay
in diagnostics. No FX, grain, source authority or missing input is inferred.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime
from decimal import Decimal, DecimalException
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from finance_tools import exact, number
from schema_validation import validate


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NAMES = {f"workflow-{name}.schema.json" for name in ("context", "artifact", "request", "result")}
MOVEMENTS = ("opening", "additions", "releases", "utilization", "other")
STAGES = ("overview", "detail", "upload", "readback")


def _no_constant(value):
    raise ValueError("Non-finite JSON numbers are not accepted")


def _no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON property name")
        result[key] = value
    return result


def read_json(path: Path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("Input must be a regular file")
    if path.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("Snapshot exceeds the supported 20 MiB JSON input limit")
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_no_constant, object_pairs_hook=_no_duplicates)


def _schema(name):
    if name not in SCHEMA_NAMES:
        raise ValueError("Only the repository's local workflow schemas may be resolved")
    return read_json(ROOT / "schemas" / name)


def validate_contract(instance, name):
    filename = name if name in SCHEMA_NAMES else f"workflow-{name}.schema.json"
    validate(instance, _schema(filename), resolver=_schema)


def _time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _issue(code, detail, location=None):
    result = {"code": code, "detail": detail}
    if location is not None:
        result["location"] = location
    return result


def _context(context, stream):
    issues = []
    if context["stream"] != stream:
        issues.append(_issue("wrong_data_stream", f"This operation requires {stream}; another stream cannot replace it."))
    if _time(context["sourceSnapshot"]["asOf"]) > _time(context["cutoff"]):
        issues.append(_issue("snapshot_after_cutoff", "The supplied source snapshot was not established by the requested cutoff."))
    if number(context["unitScale"], "unitScale") <= 0:
        raise ValueError("unitScale must be strictly positive")
    return issues


def _compare(left, right):
    issues = []
    for field in ("workflow", "period", "scenario", "version", "basis", "currency"):
        if left[field] != right[field]:
            issues.append(_issue("context_mismatch", f"The compared contexts differ in {field}.", field))
    if set(left["entities"]) != set(right["entities"]):
        issues.append(_issue("context_mismatch", "The compared entity scopes differ.", "entities"))
    if _time(left["cutoff"]) != _time(right["cutoff"]):
        issues.append(_issue("context_mismatch", "The compared cutoffs differ.", "cutoff"))
    return issues


def _tolerance(config, contexts):
    amount = number(config["amount"], "tolerance amount")
    if amount < 0:
        raise ValueError("Tolerance cannot be negative")
    start, end = date.fromisoformat(config["effectiveFrom"]), date.fromisoformat(config["effectiveTo"])
    if start > end:
        raise ValueError("Tolerance validity dates are reversed")
    issues = []
    if any(not start <= _time(c["cutoff"]).date() <= end for c in contexts):
        issues.append(_issue("tolerance_not_effective", "The versioned tolerance is not effective at every compared cutoff."))
    return amount, issues


def _amount(raw, context):
    return number(raw, "amount") * number(context["unitScale"], "unitScale") * context["signMultiplier"]


def _evidence(contexts):
    records = []
    for context in contexts:
        source = context["sourceSnapshot"]
        record = {"snapshotId": source["id"], "version": source["version"], "locator": source["locator"]}
        if record not in records:
            records.append(record)
    return records


def _result(operation, status, answer, issues, contexts, metrics=None, details=None, next_action=None):
    result = {"schemaVersion": 1, "operation": operation, "evidenceStatus": status,
              "actionState": "not-executed", "submissionState": "not-established",
              "scope": "supplied-snapshots-and-evidence", "answer": answer,
              "issues": issues, "evidence": _evidence(contexts), "metrics": metrics or {},
              "details": details or [], "nextAction": next_action or
              ("Resolve the listed evidence or compatibility gaps before relying on this result." if issues else
               "Review the result in the approved workflow; this helper performs no external action.")}
    validate_contract(result, "result")
    return result


def _provision(request):
    stages = request["stages"]
    names = [s["name"] for s in stages]
    if len(set(names)) != len(names) or names != sorted(names, key=STAGES.index):
        raise ValueError("Provision stages must be unique and ordered overview, detail, upload, readback")
    contexts = [s["context"] for s in stages]
    issues = [issue for context in contexts for issue in _context(context, "approved_internal_figures")]
    for context in contexts:
        if context["version"] != request["requiredVersion"]:
            issues.append(_issue("requested_version_unavailable", "A supplied stage is not the requested frozen scenario version."))
    for context in contexts[1:]:
        issues.extend(_compare(contexts[0], context))
    tolerance, tolerance_issues = _tolerance(request["tolerance"], contexts)
    issues.extend(tolerance_issues)
    if issues:
        return _result("provision", "blocked", "The stages are not comparable at the requested scope and version.", issues, contexts)
    normalized = {}
    balances = []
    for stage in stages:
        amounts = {key: _amount(value, stage["context"]) for key, value in stage["movements"].items()}
        normalized[stage["name"]] = amounts
        residual = amounts["closing"] - sum((amounts[key] for key in MOVEMENTS), Decimal(0))
        balances.append({"stage": stage["name"], "rawClosing": stage["movements"]["closing"],
                         "normalizedClosing": str(amounts["closing"]), "closingResidual": str(residual)})
        if abs(residual) > tolerance:
            issues.append(_issue("stage_balance_residual", "Opening and signed movements do not reconcile to closing.", stage["name"]))
    pairs = set(zip(names, names[1:]))
    explained = defaultdict(lambda: Decimal(0))
    explanation_refs = defaultdict(list)
    source_counts = Counter((item["fromStage"], item["toStage"], item["movement"], item["evidenceRef"].strip())
                            for item in request["explanations"])
    component_counts = Counter((item["fromStage"], item["toStage"], item["componentId"].strip())
                               for item in request["explanations"] if "componentId" in item)
    duplicated_sources = {key for key, count in source_counts.items() if count > 1}
    duplicated_components = {key for key, count in component_counts.items() if count > 1}
    if duplicated_sources or duplicated_components:
        issues.append(_issue("duplicate_explanation", "Explanation components or source locators overlap. Duplicate groups are excluded rather than counted twice; supply distinct component IDs and precise non-overlapping evidence locators."))
    for item in request["explanations"]:
        pair = (item["fromStage"], item["toStage"])
        if pair not in pairs:
            raise ValueError("An explanation must name an adjacent supplied stage pair")
        source_key = (*pair, item["movement"], item["evidenceRef"].strip())
        component_key = (*pair, item["componentId"].strip()) if "componentId" in item else None
        if source_key in duplicated_sources or component_key in duplicated_components:
            continue
        key = (*pair, item["movement"])
        explained[key] += number(item["amount"], "explanation amount in normalized base currency units")
        explanation_refs[key].append(item["evidenceRef"])
    details, comparisons = [], []
    any_difference = False
    for left, right in zip(stages, stages[1:]):
        a, b = normalized[left["name"]], normalized[right["name"]]
        residual_sum, gross_residual = Decimal(0), Decimal(0)
        for movement in MOVEMENTS:
            key = (left["name"], right["name"], movement)
            delta = b[movement] - a[movement]
            residual = delta - explained[key]
            any_difference |= abs(delta) > tolerance
            residual_sum += residual
            gross_residual += abs(residual)
            details.append({"fromStage": left["name"], "toStage": right["name"], "movement": movement,
                            "rawFrom": left["movements"][movement], "rawTo": right["movements"][movement],
                            "normalizedFrom": str(a[movement]), "normalizedTo": str(b[movement]),
                            "difference": str(delta), "explained": str(explained[key]), "residual": str(residual),
                            "withinTolerance": abs(residual) <= tolerance, "explanationReferences": explanation_refs[key]})
            if abs(residual) > tolerance:
                issues.append(_issue("unexplained_movement", "A movement difference remains unexplained at source precision.", "/".join(key)))
        closing_difference = b["closing"] - a["closing"]
        any_difference |= abs(closing_difference) > tolerance
        if abs(residual_sum) > tolerance or gross_residual > tolerance:
            issues.append(_issue("unexplained_total", "The net or gross unexplained bridge residual exceeds the declared tolerance.", left["name"] + "/" + right["name"]))
        comparisons.append({"fromStage": left["name"], "toStage": right["name"],
                            "closingDifference": str(closing_difference),
                            "unexplainedNetResidual": str(residual_sum), "unexplainedGrossResidual": str(gross_residual)})
    status = "blocked" if issues else "validated" if any_difference else "reconciled"
    answer = ("Movement differences remain open; additions and utilization were checked separately." if issues else
              "The supplied difference bridge is fully allocated; the compared snapshot values still differ." if any_difference else
              "Supplied stages reconcile at the declared component grain and tolerance.")
    return _result("provision", status, answer, issues, contexts,
                   {"tolerance": dict(request["tolerance"]), "normalization": "raw * declared unitScale * declared signMultiplier",
                    "stageBalances": balances, "comparisons": comparisons}, details)


def _rows(artifact, label):
    names = [column["name"] for column in artifact["columns"]]
    keys = artifact["keyColumns"]
    issues = []
    if len(set(names)) != len(names) or not set(keys) <= set(names):
        issues.append(_issue("invalid_column_contract", "Column names must be unique and contain every business key.", label))
    records = {}
    for index, row in enumerate(artifact["rows"]):
        location = f"{label}/rows/{index}"
        if set(row) != set(names):
            issues.append(_issue("row_schema_mismatch", "A row does not match the declared complete column set.", location))
        for column in artifact["columns"]:
            value = row.get(column["name"])
            if value is None:
                continue
            valid = True
            try:
                if column["type"] in {"decimal", "integer"}:
                    parsed = number(value, "typed cell")
                    valid = column["type"] != "integer" or parsed == parsed.to_integral_value()
                elif column["type"] == "date":
                    valid = date.fromisoformat(value).isoformat() == value
                elif column["type"] == "boolean":
                    valid = value in {"true", "false"}
            except ValueError:
                valid = False
            if not valid:
                issues.append(_issue("cell_type_mismatch", "A stored cell does not satisfy its declared normalized type.", location + "/" + column["name"]))
        if any(not row.get(key) or not row[key].strip() for key in keys):
            issues.append(_issue("missing_business_key", "A business key is blank or absent.", location))
            continue
        key = tuple(row[column] for column in keys)
        if key in records:
            issues.append(_issue("duplicate_business_key", "A repeated business key could multiply records; no row was selected as authoritative.", location))
            continue
        records[key] = row
    return records, issues


def _artifact(request):
    baseline, candidate = request["baseline"], request["candidate"]
    contexts = [baseline["context"], candidate["context"]]
    issues = [issue for context in contexts for issue in _context(context, "approved_internal_figures")]
    issues.extend(_compare(*contexts))
    if (number(contexts[0]["unitScale"], "baseline unitScale") != number(contexts[1]["unitScale"], "candidate unitScale")
            or contexts[0]["signMultiplier"] != contexts[1]["signMultiplier"]):
        issues.append(_issue("artifact_semantic_context_changed", "The artifact's scale or sign convention changed; identical protected raw records would no longer have the same meaning."))
    for field in ("columns", "keyColumns", "formulas", "loadTargets", "dependencies"):
        if baseline[field] != candidate[field]:
            issues.append(_issue("artifact_contract_changed", f"The existing {field} contract changed.", field))
    original, original_issues = _rows(baseline, "baseline")
    revised, revised_issues = _rows(candidate, "candidate")
    issues.extend(original_issues + revised_issues)
    width = len(baseline["keyColumns"])
    if any(len(key) != width for key in request["protectedKeys"] + request["scopeKeys"]):
        raise ValueError("Protected and scoped key tuples must match the ordered business-key width")
    protected, scope = map(lambda keys: {tuple(key) for key in keys}, (request["protectedKeys"], request["scopeKeys"]))
    if protected & scope:
        raise ValueError("Protected keys cannot also be authorized change keys")
    if request["changeMode"] == "append" and scope:
        raise ValueError("Append mode preserves every existing row and requires empty scopeKeys")
    details = []
    for key in sorted(original.keys() | revised.keys() | protected):
        before, after = original.get(key), revised.get(key)
        if key in protected and before is None:
            issues.append(_issue("protected_baseline_missing", "The protected key is missing from the accepted baseline."))
        changed = before != after
        allowed = key not in protected and (before is None if request["changeMode"] == "append" else key in scope)
        if changed:
            details.append({"key": list(key), "change": "added" if before is None else "removed" if after is None else "changed",
                            "withinRequestedScope": allowed, "protected": key in protected})
            if not allowed:
                issues.append(_issue("protected_output_regression" if key in protected else "out_of_scope_change",
                                     "An existing row was changed or removed outside the permitted scope, or an addition is outside replacement scope."))
    unverified = False
    refresh = request["refresh"]
    if refresh["status"] == "failed":
        issues.append(_issue("native_refresh_failed", "The supplied native refresh evidence reports failure."))
    elif refresh["status"] == "not-run" or not refresh["locator"].strip():
        unverified = True
        issues.append(_issue("native_refresh_unverified", "Native refresh was not evidenced; static compatibility is not a completed refresh."))
    for check in request["downstreamChecks"]:
        if check["status"] == "failed":
            issues.append(_issue("downstream_regression", "A required downstream check failed.", check["name"]))
        elif check["status"] == "not-run" or not check["locator"].strip():
            unverified = True
            issues.append(_issue("downstream_unverified", "A required downstream check has no successful evidence.", check["name"]))
    only_unverified = all(issue["code"] in {"native_refresh_unverified", "downstream_unverified"} for issue in issues)
    status = "unverified" if unverified and only_unverified else "blocked" if issues else "validated"
    return _result("artifact", status, "Existing workbook/query contracts pass the supplied checks." if not issues else
                   "Replacement is not established: preserve the accepted artifact while the listed checks remain open.",
                   issues, contexts, {"baselineRows": len(baseline["rows"]), "candidateRows": len(candidate["rows"]),
                                      "protectedKeys": len(protected), "changeMode": request["changeMode"],
                                      "contractCompatible": not any(i["code"] not in {"native_refresh_unverified", "downstream_unverified"} for i in issues),
                                      "replacementPerformed": False}, details)


def _coordinates(target, label):
    rows, issues = {}, []
    for index, row in enumerate(target["rows"]):
        key = tuple(row["members"])
        if len(key) != len(target["dimensions"]):
            issues.append(_issue("coordinate_width", "Member tuple does not match the ordered dimensions.", f"{label}/{index}"))
        if key in rows:
            issues.append(_issue("duplicate_coordinate", "Duplicate intersections cannot be silently aggregated.", f"{label}/{index}"))
        elif row["value"] is None:
            issues.append(_issue("blank_value_unverified", "A blank readback value is not evidence of zero activity.", f"{label}/{index}"))
        else:
            rows[key] = (row["value"], _amount(row["value"], target["context"]))
    return rows, issues


def _readback(request):
    expected, observed, read = request["expected"], request["observed"], request["read"]
    contexts = [expected["context"], observed["context"]]
    issues = [issue for context in contexts for issue in _context(context, "approved_internal_figures")]
    issues.extend(_compare(*contexts))
    for field in ("model", "dimensions"):
        if expected[field] != observed[field]:
            issues.append(_issue("reporting_target_mismatch", f"The reporting {field} differs; coordinate values cannot be treated as the same target."))
    if not expected["rows"]:
        issues.append(_issue("expected_population_missing", "An empty expected payload does not establish zero activity; supply the intended coordinates or explicit zero-valued intersections."))
    tolerance, more = _tolerance(request["tolerance"], contexts)
    issues.extend(more)
    if read["state"] != "live" or not read["knownGoodRead"] or not read["independent"] or read["errorSuppressed"] or not read["locator"].strip():
        issues.append(_issue("read_failed" if read["state"] == "failed" or read["errorSuppressed"] else "read_unverified",
                             "A live independent read with a known-good connection and unsuppressed result is required; cached or blank inspection is not readback verification."))
    if _time(read["readAt"]) < _time(observed["context"]["sourceSnapshot"]["asOf"]):
        issues.append(_issue("read_time_conflict", "The read is timestamped before its supplied source observation."))
    if issues:
        status = "unverified" if all(i["code"] == "read_unverified" for i in issues) else "blocked"
        return _result("readback", status, "The reporting readback is failed or unverified; no zero-activity conclusion is supported.", issues, contexts)
    left, a_issues = _coordinates(expected, "expected")
    right, b_issues = _coordinates(observed, "observed")
    issues.extend(a_issues + b_issues)
    details, gross, net = [], Decimal(0), Decimal(0)
    for key in sorted(left.keys() | right.keys()):
        a, b = left.get(key), right.get(key)
        delta = (b[1] if b else Decimal(0)) - (a[1] if a else Decimal(0))
        net += delta
        gross += abs(delta)
        matched = a is not None and b is not None and abs(delta) <= tolerance
        details.append({"members": list(key), "rawExpected": a[0] if a else None, "rawObserved": b[0] if b else None,
                        "normalizedExpected": str(a[1]) if a else None, "normalizedObserved": str(b[1]) if b else None,
                        "difference": str(delta), "matched": matched, "missingSide": "expected" if a is None else "observed" if b is None else None})
        if not matched:
            issues.append(_issue("coordinate_difference", "An intersection is missing or differs beyond the declared tolerance."))
    if abs(net) > tolerance or gross > tolerance:
        issues.append(_issue("readback_total_difference", "The net or gross coordinate difference exceeds the declared tolerance."))
    return _result("readback", "blocked" if issues else "reconciled",
                   "Readback fails at the agreed coordinate grain." if issues else "The supplied independent readback matches at every agreed intersection.",
                   issues, contexts, {"netDifference": str(net), "grossAbsoluteDifference": str(gross),
                                      "expectedCoordinates": len(left), "observedCoordinates": len(right),
                                      "tolerance": dict(request["tolerance"]), "zeroUsedOnlyForMissingSideBridge": True}, details)


def _mapping(request):
    context = request["context"]
    issues = _context(context, "approved_internal_figures")
    if issues:
        return _result("mapping", "blocked", "An eligible internal source at the requested cutoff is required.", issues, [context])
    cutoff = _time(context["cutoff"]).date()
    by_key = defaultdict(list)
    for index, rule in enumerate(request["rules"]):
        start, end = date.fromisoformat(rule["validFrom"]), date.fromisoformat(rule["validTo"])
        if start > end:
            raise ValueError("Mapping validity dates are reversed")
        by_key[rule["key"]].append((rule, start <= cutoff <= end, index))
    details = []
    for key in request["keys"]:
        rules = by_key[key]
        active = [r for r, current, _ in rules if current]
        status, fields = "matched", None
        if not rules:
            status = "mapping_missing"
        elif not active:
            status = "mapping_not_effective"
        elif len(active) != 1:
            status = "ambiguous_mapping"
        elif not active[0]["approvalRef"].strip():
            status = "mapping_not_approved"
        elif any(not active[0]["fields"].get(field, "").strip() for field in request["requiredFields"]):
            status = "mapping_incomplete"
        else:
            fields = dict(active[0]["fields"])
        details.append({"key": key, "status": status, "fields": fields})
        if status != "matched":
            issues.append(_issue(status, "Keep this key unresolved and review the approved source or master; no rule was guessed or written."))
    return _result("mapping", "blocked" if issues else "validated", "Mapping requirements are unresolved." if issues else
                   "Each required key has one effective, complete rule with supplied approval evidence.", issues, [context],
                   {"keyCount": len(request["keys"]), "statuses": dict(Counter(d["status"] for d in details)), "masterModified": False}, details)


def _granularity(request):
    context = request["context"]
    issues = _context(context, "approved_internal_figures")
    missing = sorted(set(request["requiredDimensions"]) - set(request["availableDimensions"]))
    if missing:
        issues.append(_issue("required_granularity_missing", "The source lacks required dimensions. Obtain an approved extract at that grain; totals or public benchmarks cannot reconstruct the split."))
    return _result("granularity", "blocked" if issues else "validated", "The requested split is unavailable at the supplied grain." if issues else
                   "The supplied source declares every required dimension; record-level checks remain separate.", issues, [context],
                   {"measure": request["measure"], "missingDimensions": missing, "inferredValues": False})


def _cases(request):
    context = request["context"]
    issues = _context(context, "internal_workflow_status")
    if issues:
        return _result("case-status", "blocked", "Internal workflow evidence at the requested cutoff is required.", issues, [context])
    details = []
    counts = Counter((item["scope"], item["ownerRole"]) for item in request["cases"])
    if any(count > 1 for count in counts.values()):
        issues.append(_issue("duplicate_case_scope", "The same owner and scope has multiple status records; resolve the authoritative confirmation."))
    for item in request["cases"]:
        status = item["status"]
        if status in {"not-requested", "awaiting-confirmation"}:
            issues.append(_issue(status.replace("-", "_"), "No confirmed zero is established for this owner and scope.", item["scope"]))
        elif not item.get("confirmedAt") or not item.get("evidenceRef"):
            issues.append(_issue("confirmation_evidence_missing", "Confirmed status needs a confirmation date and evidence locator.", item["scope"]))
        elif _time(item["confirmedAt"]) > _time(context["cutoff"]):
            issues.append(_issue("confirmation_after_cutoff", "A later confirmation does not establish status at the requested cutoff.", item["scope"]))
        if status == "confirmed-none" and item.get("caseCount") != 0:
            issues.append(_issue("confirmed_none_count_conflict", "A confirmed-none record must explicitly state zero cases.", item["scope"]))
        if status == "cases-received" and item.get("caseCount", 0) < 1:
            issues.append(_issue("received_cases_count_missing", "Cases-received requires a positive explicit case count.", item["scope"]))
        details.append(dict(item))
    return _result("case-status", "blocked" if issues else "validated", "Case coverage has unconfirmed scopes." if issues else
                   "Each supplied scope has explicit dated case confirmation; no provision amount is inferred.", issues, [context],
                   {"scopeCount": len(details), "statuses": dict(Counter(d["status"] for d in details))}, details)


def payload_sha256(payload):
    """Binding uses UTF-8 JSON, sorted object keys, compact separators, no NaN."""
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _allocation(request):
    context, configuration, approval, prior = (request[k] for k in ("context", "configuration", "approval", "priorRun"))
    issues = _context(context, "internal_workflow_status")
    cutoff = _time(context["cutoff"])
    start, end = date.fromisoformat(configuration["validFrom"]), date.fromisoformat(configuration["validTo"])
    if start > end:
        raise ValueError("Allocation configuration validity dates are reversed")
    if not start <= cutoff.date() <= end:
        issues.append(_issue("configuration_not_effective", "The approved configuration is not effective at the requested cutoff."))
    if configuration["lockState"] != "unlocked":
        issues.append(_issue("sender_locked_or_unknown", "Preserve the approved sender; do not substitute a master or bypass the lock."))
    for field in ("membershipEvidence", "permissionEvidence"):
        if not configuration[field].strip():
            issues.append(_issue("configuration_evidence_missing", "Membership and permission each need evidence.", field))
    members = [r["member"] for r in configuration["receivers"]]
    weights = [number(r["weight"], "receiver weight") for r in configuration["receivers"]]
    if len(set(members)) != len(members) or any(weight < 0 for weight in weights) or sum(weights, Decimal(0)) != 1:
        issues.append(_issue("receiver_weights_invalid", "Receiver members must be unique and nonnegative fractional weights must total exactly one; no normalization is applied."))
    payload = request["payload"]
    number(payload["amount"], "allocation payload amount")
    payload_members = [receiver["member"] for receiver in payload["receivers"]]
    payload_weights = [number(receiver["weight"], "payload receiver weight") for receiver in payload["receivers"]]
    if (len(set(payload_members)) != len(payload_members) or any(weight < 0 for weight in payload_weights)
            or sum(payload_weights, Decimal(0)) != 1):
        issues.append(_issue("payload_receiver_weights_invalid", "Payload receivers must be unique and nonnegative fractional weights must total exactly one."))
    if (payload["sender"] != configuration["sender"] or payload["configurationVersion"] != configuration["version"]
            or dict(zip(payload_members, payload_weights)) != dict(zip(members, weights))):
        issues.append(_issue("payload_configuration_mismatch", "The actual payload sender, configuration version, receiver membership and weights must match the checked configuration exactly."))
    digest = payload_sha256(request["payload"])
    if approval["target"] != request["target"] or approval["payloadSha256"] != digest or not approval["evidenceRef"].strip() or _time(approval["expiresAt"]) < cutoff:
        issues.append(_issue("approval_binding_invalid", "Approval must cover this exact target and canonical payload, have an evidence locator and remain effective at the cutoff."))
    if prior["status"] != "confirmed-not-executed" or not prior["evidenceRef"].strip():
        issues.append(_issue("duplicate_run_risk", "Verify prior execution independently; an unknown or executed run cannot be retried."))
    if prior["target"] != request["target"] or prior["payloadSha256"] != digest:
        issues.append(_issue("prior_run_binding_invalid", "Prior-run evidence must identify this exact target and canonical payload; evidence for another target or payload cannot clear a retry."))
    if _time(prior["checkedAt"]) > cutoff:
        issues.append(_issue("prior_status_after_cutoff", "Prior-run status was checked after the requested cutoff."))
    if "lastAttempt" in request and _time(prior["checkedAt"]) <= _time(request["lastAttempt"]["at"]):
        issues.append(_issue("timeout_readback_required", "A timed-out write requires a later independent status check before any retry can be considered."))
    return _result("allocation-preflight", "blocked" if issues else "validated", "Allocation preflight is blocked; no execution or retry is performed." if issues else
                   "The supplied preflight checks pass; this helper grants no execution permission and performs no write.",
                   issues, [context], {"payloadSha256": digest, "configurationVersion": configuration["version"],
                                      "receiverWeightTotal": str(sum(weights, Decimal(0))), "retryPerformed": False})


OPERATIONS = {"provision": _provision, "artifact": _artifact, "readback": _readback,
              "mapping": _mapping, "granularity": _granularity, "case-status": _cases,
              "allocation-preflight": _allocation}


@exact
def check(request):
    """Validate a request and return separate evidence/action state, without mutation."""
    validate_contract(request, "request")
    return OPERATIONS[request["operation"]](request)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check_parser = sub.add_parser("check", help="Check supplied snapshots; print JSON, never write a workbook")
    check_parser.add_argument("file", type=Path)
    validate_parser = sub.add_parser("validate", help="Validate one local workflow JSON contract")
    validate_parser.add_argument("--schema", choices=("context", "artifact", "request", "result"), required=True)
    validate_parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        data = read_json(args.file)
        if args.command == "validate":
            validate_contract(data, args.schema)
            print(json.dumps({"schema": args.schema, "status": "valid"}))
            return 0
        result = check(data)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 2 if result["evidenceStatus"] in {"blocked", "unverified"} else 0
    except (ValueError, OSError, UnicodeError, DecimalException) as exc:
        print(f"Workflow check stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
