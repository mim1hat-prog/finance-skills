"""Run the offline release gate; no provider calls, installs or remote writes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
import project_gates
import release
import check_git_identity

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-release", action="store_true", help="Also require current frozen release bytes and indexes to match")
    parser.add_argument("--private-policy", type=Path, help="Optional private JSON list of forbidden literals, outside the repository")
    parser.add_argument("--commit-export", type=Path, help="Also require public no-reply identities in GitHub commit JSON stored outside the project")
    args = parser.parse_args()
    try:
        private = ()
        if args.private_policy:
            path = args.private_policy.resolve()
            if path.is_relative_to(ROOT.resolve()):
                raise ValueError("Private publication policy must be outside the public repository")
            values = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
                raise ValueError("Private policy must be a list of nonempty strings")
            private = tuple(values)
        result = project_gates.validate(ROOT, private_literals=private)
        if args.commit_export:
            identity = check_git_identity.review_export(args.commit_export, project_root=ROOT)
            if not identity["ok"]:
                raise ValueError(f"Commit identity gate failed: {len(identity['findings'])} finding(s); no commit or publication was performed")
            result["commitIdentity"] = identity
        else:
            result["commitIdentity"] = {"status": "not-checked", "scope": "Artifact validation only; supply --commit-export before publication and verify history completeness separately"}
        suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
        tested = unittest.TextTestRunner(verbosity=1).run(suite)
        if not tested.wasSuccessful():
            raise ValueError("Unit tests failed; no release was created or published")
        result["tests"] = {"run": tested.testsRun, "skipped": len(tested.skipped),
                           "skipReasons": sorted({reason for _, reason in tested.skipped})}
        if args.require_release:
            result["currentRelease"] = release.run(ROOT, check=True)
        else:
            result["currentRelease"] = "not-required: run with --require-release after freezing"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(f"Release gate failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
