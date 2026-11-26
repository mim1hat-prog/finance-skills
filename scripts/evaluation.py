"""Offline public development kit and manual matched-run bookkeeping; no model calls."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("baseline", "suite")
STATUSES = ("not-run", "completed", "failed", "refused", "interrupted", "unavailable")
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)\Z")
LIMITATION = ("Manual records are declarations, not proof of native execution. "
              "Public answer keys make these development cases, not a held-out efficacy study.")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_json(data: str):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result
    def constant(value):
        raise ValueError("Nonfinite JSON number")
    return json.loads(data, object_pairs_hook=pairs, parse_float=Decimal, parse_constant=constant)


def shape(value, fields, label):
    require(isinstance(value, dict) and set(value) == set(fields), f"Invalid {label} fields")


def finite(value):
    if isinstance(value, dict):
        for item in value.values():
            finite(item)
    elif isinstance(value, list):
        for item in value:
            finite(item)
    elif type(value) in (float, Decimal):
        require(Decimal(str(value)).is_finite(), "Nonfinite number")
    else:
        require(value is None or type(value) in (str, int, bool), "Unsupported JSON value")


def load_kit(root: Path = ROOT):
    folder = root / "evaluations"
    require(folder.is_dir() and not folder.is_symlink(), "Missing or linked evaluation kit")
    manifest_path = folder / "cases.json"
    require(manifest_path.is_file() and not manifest_path.is_symlink(), "Missing kit manifest")
    raw = manifest_path.read_bytes()
    manifest = strict_json(raw.decode("utf-8"))
    shape(manifest, ("schemaVersion", "caseSetVersion", "kind", "status", "cases"), "kit")
    require(type(manifest["schemaVersion"]) is int and manifest["schemaVersion"] == 1,
            "Unsupported evaluation schema")
    require(manifest["kind"] == "public-development-kit" and manifest["status"] == "prepared-unrun",
            "Unsupported evaluation scope")
    require(isinstance(manifest["caseSetVersion"], str) and VERSION.fullmatch(manifest["caseSetVersion"]),
            "Invalid case-set version")
    require(isinstance(manifest["cases"], list) and len(manifest["cases"]) == 4, "Expected four cases")
    cases, allowed = {}, {"cases.json", "README.md"}
    for case in manifest["cases"]:
        shape(case, ("id", "title", "family", "prompt", "answer"), "case")
        name = case["id"]
        require(isinstance(name, str) and ID.fullmatch(name) and name not in cases, "Invalid case ID")
        require(all(isinstance(case[key], str) and case[key].strip() for key in ("title", "family")),
                "Missing case description")
        for kind, extension in (("prompt", "md"), ("answer", "json")):
            record = case[kind]
            shape(record, ("path", "sha256"), "fixture")
            expected_path = f"{kind}s/{name}.{extension}"
            require(record["path"] == expected_path and isinstance(record["sha256"], str)
                    and SHA.fullmatch(record["sha256"]), "Invalid fixture identity")
            path = folder / expected_path
            require(not path.parent.is_symlink() and not path.is_symlink() and path.is_file(),
                    "Missing or linked fixture")
            contents = path.read_bytes()
            require(digest(contents) == record["sha256"], f"Fixture digest mismatch: {name}/{kind}")
            require(bool(contents.decode("utf-8").strip()), "Empty fixture")
            allowed.add(expected_path)
        answer = strict_json((folder / case["answer"]["path"]).read_text(encoding="utf-8"))
        require(isinstance(answer, dict) and bool(answer), "Answer key must be an object")
        finite(answer)
        cases[name] = {**case, "expected": answer}
    for path in folder.rglob("*"):
        require(not path.is_symlink(), "Linked evaluation entry")
        if not path.is_dir():
            require(path.is_file() and path.relative_to(folder).as_posix() in allowed,
                    "Unexpected evaluation file; keep run records outside the public kit")
    return digest(raw), manifest["caseSetVersion"], cases


def validate_kit(root: Path = ROOT) -> dict:
    kit_hash, case_version, cases = load_kit(root)
    return {"status": "prepared-unrun", "kitSha256": kit_hash, "caseSetVersion": case_version,
            "uniqueCases": len(cases),
            "fixtureFiles": 2 * len(cases), "nativeRunRecords": 0, "scope": LIMITATION}


def schedule(cases, repetitions: int, seed: int) -> list[dict]:
    require(type(repetitions) is int and 1 <= repetitions <= 100, "Repetitions must be 1..100")
    require(type(seed) is int and 0 <= seed <= 2**32 - 1, "Seed must be a 32-bit nonnegative integer")
    blocks = [(case, repeat) for case in sorted(cases) for repeat in range(1, repetitions + 1)]
    blocks.sort(key=lambda item: digest(f"{seed}|{item[0]}|{item[1]}".encode()))
    offset = int(digest(str(seed).encode()), 16) % 2
    runs = []
    for position, (case, repeat) in enumerate(blocks):
        order = CONDITIONS if (position + offset) % 2 == 0 else CONDITIONS[::-1]
        for condition in order:
            runs.append({"id": f"{case}:{repeat}:{condition}", "case": case,
                         "repeat": repeat, "condition": condition})
    return runs


def environment_check(environment):
    shape(environment, ("hostSurface", "model", "toolSettings", "packageVersion", "packageSha256"), "environment")
    require(all(isinstance(v, str) and 1 <= len(v.strip()) <= 1000 for v in environment.values()),
            "Environment values must be nonempty strings; use unknown explicitly")
    require(environment["packageSha256"] == "unknown" or SHA.fullmatch(environment["packageSha256"]),
            "Package SHA-256 must be lowercase hex or unknown")
    require(environment["packageVersion"] == "unknown" or VERSION.fullmatch(environment["packageVersion"]),
            "Package version must be stable MAJOR.MINOR.PATCH or unknown")


def timestamp_check(value):
    require(isinstance(value, str) and TIMESTAMP.fullmatch(value),
            "Attempted run needs a timezone-aware executedAt timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(parsed.utcoffset() is not None, "executedAt needs a timezone")
    except ValueError as error:
        raise ValueError("Invalid executedAt calendar date/time") from error


def init_plan(root: Path, environment: dict, repetitions: int, seed: int) -> dict:
    kit_hash, case_version, cases = load_kit(root)
    environment_check(environment)
    runs = [{**row, "status": "not-run", "executedAt": None, "response": None, "evidence": "unknown"}
            for row in schedule(cases, repetitions, seed)]
    return {"schemaVersion": 1, "kitSha256": kit_hash, "caseSetVersion": case_version,
            "environment": dict(environment),
            "repetitions": repetitions, "seed": seed, "runs": runs}


def differences(expected, actual, path="$", depth=0) -> list[str]:
    require(depth < 100, "Response nesting limit exceeded")
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(expected) != set(actual):
            return [path + ": object fields"]
        return [error for key in sorted(expected)
                for error in differences(expected[key], actual[key], path + "/" + key, depth + 1)]
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            return [path + ": array length"]
        return [error for i, value in enumerate(expected)
                for error in differences(value, actual[i], path + f"/{i}", depth + 1)]
    if type(expected) in (int, float, Decimal):
        equal = type(actual) in (int, float, Decimal) and Decimal(str(expected)) == Decimal(str(actual))
    else:
        equal = type(expected) is type(actual) and expected == actual
    return [] if equal else [path + ": value or type"]


def summarize(root: Path, plan: dict) -> dict:
    finite(plan)
    shape(plan, ("schemaVersion", "kitSha256", "caseSetVersion", "environment", "repetitions", "seed", "runs"), "plan")
    require(type(plan["schemaVersion"]) is int and plan["schemaVersion"] == 1, "Unsupported plan schema")
    kit_hash, case_version, cases = load_kit(root)
    require(plan["kitSha256"] == kit_hash, "Plan uses a different kit manifest")
    require(plan["caseSetVersion"] == case_version, "Plan uses a different case-set version")
    environment_check(plan["environment"])
    expected = schedule(cases, plan["repetitions"], plan["seed"])
    require(isinstance(plan["runs"], list) and len(plan["runs"]) == len(expected),
            "Missing or extra scheduled runs")
    graded, identities = [], set()
    for row, scheduled in zip(plan["runs"], expected):
        shape(row, ("id", "case", "repeat", "condition", "status", "executedAt", "response", "evidence"), "run")
        require(isinstance(row["id"], str) and row["id"] not in identities, "Duplicate run identity")
        identities.add(row["id"])
        require(type(row["repeat"]) is int and all(row[k] == v for k, v in scheduled.items()),
                "Run identity/order differs from the predetermined schedule")
        require(row["status"] in STATUSES and isinstance(row["evidence"], str)
                and bool(row["evidence"].strip()), "Invalid run status or evidence locator")
        if row["status"] == "not-run":
            require(row["executedAt"] is None, "Not-run records must retain null executedAt")
        else:
            timestamp_check(row["executedAt"])
        require(row["status"] == "completed" or row["response"] is None,
                "Only completed runs may contain a response")
        errors = differences(cases[row["case"]]["expected"], row["response"]) if row["status"] == "completed" else []
        graded.append({**scheduled, "status": row["status"], "executedAt": row["executedAt"],
                       "passed": row["status"] == "completed" and not errors, "errors": errors})
    def counts(rows):
        statuses = Counter(row["status"] for row in rows)
        passed = sum(row["passed"] for row in rows)
        return {"scheduled": len(rows), "attempted": len(rows) - statuses["not-run"],
                "completed": statuses["completed"], "passed": passed,
                "completedIncorrect": statuses["completed"] - passed,
                "statusCounts": {status: statuses[status] for status in STATUSES}}
    per_case, paired = {}, Counter()
    for case in sorted(cases):
        rows = [row for row in graded if row["case"] == case]
        per_case[case] = {condition: counts([r for r in rows if r["condition"] == condition])
                          for condition in CONDITIONS}
        pairs = Counter()
        for repeat in range(1, plan["repetitions"] + 1):
            pair = {r["condition"]: r for r in rows if r["repeat"] == repeat}
            if any(r["status"] != "completed" for r in pair.values()):
                outcome = "incomplete"
            else:
                outcome = {(True, True): "bothPassed", (True, False): "baselineOnlyPassed",
                           (False, True): "suiteOnlyPassed", (False, False): "neitherPassed"}[
                               tuple(pair[c]["passed"] for c in CONDITIONS)]
            pairs[outcome] += 1
        names = ("bothPassed", "baselineOnlyPassed", "suiteOnlyPassed", "neitherPassed", "incomplete")
        per_case[case]["pairedOutcomes"] = {name: pairs[name] for name in names}
        paired.update(pairs)
    return {"schemaVersion": 1, "kitSha256": kit_hash, "caseSetVersion": case_version,
            "environment": plan["environment"],
            "uniqueCases": len(cases), "repetitionsPerCaseCondition": plan["repetitions"],
            "totals": counts(graded), "perCondition": {c: counts([r for r in graded if r["condition"] == c]) for c in CONDITIONS},
            "perCase": per_case, "pairedOutcomes": {name: paired[name] for name in names},
            "runs": graded, "limitations": LIMITATION}


def write_new(path: Path, result: dict, root: Path = ROOT):
    target = path.resolve()
    project = root.resolve()
    require(not target.is_relative_to(project) or target.is_relative_to(project / ".local"),
            "Keep evaluation run records outside the public project or under .local")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, ensure_ascii=False, indent=2, allow_nan=False)
        output.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate-kit")
    initialize = commands.add_parser("init-plan")
    initialize.add_argument("--output", type=Path, required=True)
    initialize.add_argument("--host-surface", required=True)
    initialize.add_argument("--model", default="unknown")
    initialize.add_argument("--tool-settings", default="unknown")
    initialize.add_argument("--package-version", default="unknown")
    initialize.add_argument("--package-sha256", default="unknown")
    initialize.add_argument("--repetitions", type=int, default=3)
    initialize.add_argument("--seed", type=int, default=0)
    summary = commands.add_parser("summarize")
    summary.add_argument("plan", type=Path)
    summary.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate-kit":
            result = validate_kit()
        elif args.command == "init-plan":
            result = init_plan(ROOT, {"hostSurface": args.host_surface, "model": args.model,
                                     "toolSettings": args.tool_settings, "packageVersion": args.package_version,
                                     "packageSha256": args.package_sha256},
                               args.repetitions, args.seed)
            write_new(args.output, result)
            result = {"status": "prepared-unrun", "scheduled": len(result["runs"])}
        else:
            result = summarize(ROOT, strict_json(args.plan.read_text(encoding="utf-8")))
            if args.output:
                write_new(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print(f"Evaluation check failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
