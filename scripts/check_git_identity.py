"""Read-only public commit-identity guard; never prints names, addresses or messages.

Review a GitHub /commits JSON array, one /commits/{sha} response, or one
/git/commits/{sha} response exported outside the project. Alternatively inspect
every commit reachable from local Git refs, failing if ancestry is incomplete.
This checks public no-reply address form, not identity ownership or file content.
It does not contact GitHub, change settings, create commits or rewrite history.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
COMMIT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
PUBLIC_NOREPLY = re.compile(
    r"(?:[a-z0-9][a-z0-9._+\-\[\]]*@users\.noreply\.github\.com|noreply@github\.com)\Z",
    re.I,
)


class IdentityCheckError(ValueError):
    """An error code safe to return without echoing the supplied evidence."""


def review_records(value: object, *, source: str = "provided-export") -> dict:
    rows = value if isinstance(value, list) else [value]
    if not rows:
        raise IdentityCheckError("empty-commit-export")
    findings, seen, identities = [], set(), 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get("sha"), str) or not COMMIT_ID.fullmatch(row["sha"]):
            findings.append({"record": index, "code": "invalid-commit-record"})
            continue
        commit = row["sha"]
        if commit in seen:
            findings.append({"commit": commit, "code": "duplicate-commit-record"})
            continue
        seen.add(commit)
        # REST /commits nests the Git identities under commit. Git-data responses
        # put them at the root. Top-level REST author/committer are user profiles.
        metadata = row.get("commit", row)
        for role in ("author", "committer"):
            identities += 1
            person = metadata.get(role) if isinstance(metadata, dict) else None
            address = person.get("email") if isinstance(person, dict) else None
            if not isinstance(address, str) or not address:
                code = "missing-or-invalid-identity"
            elif not PUBLIC_NOREPLY.fullmatch(address):
                code = "non-public-noreply-identity"
            else:
                continue
            findings.append({"commit": commit, "role": role, "code": code})
    return {
        "ok": not findings,
        "source": source,
        "commitCount": len(seen),
        "identityCount": identities,
        "findings": findings,
        "historyCompleteness": ("all-local-refs-traversed" if source == "local-git-history"
                                else "not-established-by-export"),
        "limit": "Address form only; does not establish ownership, remote-history completeness or file-content safety.",
    }


def review_export(path: Path, *, project_root: Path) -> dict:
    try:
        if path.is_symlink():
            raise IdentityCheckError("linked-export-refused")
        resolved = path.resolve()
        if resolved.is_relative_to(project_root.resolve()):
            raise IdentityCheckError("export-must-remain-outside-project")
        if not path.is_file() or path.stat().st_size > 20_000_000:
            raise IdentityCheckError("export-unavailable-or-too-large")
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise IdentityCheckError("unreadable-commit-export") from None
    return review_records(value)


def _git(root: Path, *args: str) -> bytes:
    try:
        # Explicit Git options fail safely on versions that lack them. Missing
        # objects must never trigger a promisor fetch, and replacement refs must
        # not substitute different identities for the requested object.
        result = subprocess.run(["git", "--no-lazy-fetch", "--no-replace-objects", "-C", str(root), *args],
                                capture_output=True, check=False)
    except OSError:
        raise IdentityCheckError("git-unavailable") from None
    if result.returncode:
        # Do not print Git stderr: it can contain identities, messages or paths.
        raise IdentityCheckError("incomplete-or-unreadable-git-history")
    return result.stdout


def review_local_history(root: Path) -> dict:
    if _git(root, "rev-parse", "--is-shallow-repository").strip() != b"false":
        raise IdentityCheckError("incomplete-shallow-git-history")
    raw_ids = _git(root, "rev-list", "--all")
    try:
        ids = raw_ids.decode("ascii").splitlines()
    except UnicodeError:
        raise IdentityCheckError("invalid-local-commit-list") from None
    if not ids or any(not COMMIT_ID.fullmatch(sha) for sha in ids):
        raise IdentityCheckError("empty-or-invalid-local-commit-list")
    rows = []
    known_ids = set(ids)
    for sha in ids:
        header = _git(root, "cat-file", "commit", sha).split(b"\n\n", 1)[0]
        try:
            lines = header.decode("utf-8").splitlines()
        except UnicodeError:
            raise IdentityCheckError("unreadable-local-commit-metadata") from None
        parents = [line.removeprefix("parent ") for line in lines if line.startswith("parent ")]
        if any(parent not in known_ids for parent in parents):
            raise IdentityCheckError("incomplete-or-rewritten-git-history")
        row = {"sha": sha}
        for role in ("author", "committer"):
            candidates = [line for line in lines if line.startswith(role + " ")]
            match = (re.fullmatch(role + r" .* <([^<>\r\n]*)> -?\d+ [+-]\d{4}", candidates[0])
                     if len(candidates) == 1 else None)
            row[role] = {"email": match[1] if match else None}
        rows.append(row)
    return review_records(rows, source="local-git-history")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--export", type=Path, help="GitHub commit JSON saved outside the project; never commit this evidence")
    mode.add_argument("--local-history", action="store_true", help="Inspect all local refs; incomplete ancestry fails")
    args = parser.parse_args(argv)
    try:
        result = review_export(args.export, project_root=ROOT) if args.export else review_local_history(ROOT)
    except IdentityCheckError as exc:
        result = {"ok": False, "code": str(exc), "commitCount": 0, "identityCount": 0, "findings": []}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
