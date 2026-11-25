#!/usr/bin/env python3
"""Read upstream heads and primary docs; report review needs without changing pins."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.error
import urllib.request

from fetch_upstreams import (
    CheckedRedirects, DEFAULT_TIMEOUT, HASH_RE, PIN_RE, REPO_ROOT,
    SourceError, USER_AGENT, load_lock, validate_https_url,
)

REPORT_KIND = "finance-skills-upstream-review"
DOC_HOSTS = {
    "learn.microsoft.com", "support.microsoft.com", "support.google.com",
    "knowledge.workspace.google.com", "code.visualstudio.com",
    "duckdb.org", "www.duckdb.org", "docs.github.com",
    "www.agenorit.com.au",
}
MAX_RESPONSE_BYTES = 4 * 1024 * 1024


def read_url(url: str, *, hosts: set[str], timeout: float) -> tuple[bytes, dict]:
    validate_https_url(url, hosts)
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/html, text/plain"}
    )
    opener = urllib.request.build_opener(CheckedRedirects(hosts))
    with opener.open(request, timeout=timeout) as response:
        validate_https_url(response.geturl(), hosts)
        payload = response.read(MAX_RESPONSE_BYTES + 1)
        if len(payload) > MAX_RESPONSE_BYTES:
            raise SourceError("Response exceeds the review-size limit.")
        if not payload:
            raise SourceError("Source returned an empty response.")
        headers = response.headers
        metadata = {
            "httpStatus": response.status,
            "finalUrl": response.geturl(),
            "etag": headers.get("ETag"),
            "lastModified": headers.get("Last-Modified"),
            "contentType": headers.get("Content-Type", ""),
        }
        return payload, metadata


def error_detail(error: Exception) -> str:
    if isinstance(error, urllib.error.HTTPError):
        detail = f"HTTP {error.code}"
        headers = error.headers or {}
        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")
        retry = headers.get("Retry-After")
        if error.code in (403, 429) and remaining == "0":
            detail += "; GitHub API rate limit exhausted"
        if reset and reset.isdecimal():
            detail += f"; rate-limit reset Unix time {reset}"
        if retry and retry.isdecimal():
            detail += f"; retry after {retry} seconds"
        return detail
    return str(error)[:400]


def check_source(source: dict, *, timeout: float, reader=read_url) -> dict:
    result = {
        "id": source["id"],
        "repository": source["repository"],
        "reviewedCommit": source["commit"],
        "latestCommit": None,
    }
    url = f"https://api.github.com/repos/{source['repository']}/commits?per_page=1"
    try:
        body, _ = reader(url, hosts={"api.github.com"}, timeout=timeout)
        commits = json.loads(body)
        if not isinstance(commits, list) or not commits:
            raise SourceError("GitHub did not return a nonempty commit list.")
        latest = commits[0]
        sha = latest.get("sha", "")
        if not isinstance(sha, str) or not PIN_RE.fullmatch(sha):
            raise SourceError("GitHub did not return a valid full commit SHA.")
        result["latestCommit"] = sha
        result["latestCommitDate"] = latest.get("commit", {}).get("committer", {}).get("date")
        message = latest.get("commit", {}).get("message", "")
        result["latestCommitSummary"] = str(message).split("\n", 1)[0][:250]
        result["status"] = "unchanged" if sha == source["commit"] else "new_commit_requires_review"
        result["compatibilityVerified"] = False
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result.update(status="unavailable", error=error_detail(exc), compatibilityVerified=False)
    return result


def check_document(document: dict, *, timeout: float, reader=read_url) -> dict:
    result = {"id": document.get("id"), "url": document.get("url"), "semanticReviewPerformed": False}
    try:
        url = document["url"]
        baseline = document.get("contentSha256")
        if baseline is not None and (
            not isinstance(baseline, str) or not HASH_RE.fullmatch(baseline)
        ):
            raise SourceError("Document baseline must be null or a SHA-256.")
        body, metadata = reader(url, hosts=DOC_HOSTS, timeout=timeout)
        content_type = metadata.get("contentType", "").split(";", 1)[0].strip().lower()
        if content_type and not (
            content_type.startswith("text/") or content_type in {"application/xhtml+xml", "application/json"}
        ):
            raise SourceError("Documentation endpoint returned an unexpected content type.")
        digest = hashlib.sha256(body).hexdigest()
        if baseline is None:
            status = "reachable_unbaselined"
        else:
            status = "unchanged_bytes" if baseline == digest else "changed_bytes_requires_review"
        result.update(metadata, status=status, contentSha256=digest, responseBytes=len(body))
        result["interpretation"] = (
            "Reachability and byte comparison only; dynamic markup, redirects or sign-in pages "
            "do not establish a capability change. Review the primary documentation."
        )
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result.update(status="unavailable", error=error_detail(exc))
    return result


def collect_report(lock: dict, *, timeout: float = DEFAULT_TIMEOUT, reader=read_url) -> dict:
    sources = lock["sources"]
    documents = lock.get("documents", [])
    if not isinstance(documents, list):
        raise SourceError("documents must be a list.")
    with ThreadPoolExecutor(max_workers=4) as pool:
        source_futures = [
            pool.submit(check_source, source, timeout=timeout, reader=reader)
            for source in sources
        ]
        doc_futures = [
            pool.submit(check_document, document, timeout=timeout, reader=reader)
            for document in documents
        ]
        source_results = [future.result() for future in source_futures]
        doc_results = [future.result() for future in doc_futures]
    return {
        "schemaVersion": 1,
        "kind": REPORT_KIND,
        "checkedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lockReviewedOn": lock.get("reviewedOn"),
        "pinsChanged": False,
        "runtimeInstalled": False,
        "compatibilityReviewPerformed": False,
        "sources": source_results,
        "documents": doc_results,
        "summary": {
            "newCommits": sum(s["status"] == "new_commit_requires_review" for s in source_results),
            "unchangedCommits": sum(s["status"] == "unchanged" for s in source_results),
            "changedDocumentBytes": sum(d["status"] == "changed_bytes_requires_review" for d in doc_results),
            "unbaselinedDocuments": sum(d["status"] == "reachable_unbaselined" for d in doc_results),
            "unavailable": sum(r["status"] == "unavailable" for r in source_results + doc_results),
        },
        "nextStep": (
            "Review new commits and primary docs, inspect licences/dependencies, adapt relevant changes, "
            "run validation, then deliberately update the lock and generated packages. "
            "A newer commit is not verified compatibility. Existing account imports still require replacement or Refresh."
        ),
    }


def write_report(report: dict, output: Path, repo_root: Path = REPO_ROOT) -> None:
    output = output.expanduser().absolute()
    if output.is_symlink() or output.suffix.lower() != ".json":
        raise SourceError("Report output must be a regular JSON path, not a symlink.")
    resolved = output.resolve()
    try:
        relative = resolved.relative_to(repo_root.resolve())
    except ValueError:
        relative = None
    if relative is not None and (not relative.parts or relative.parts[0] != ".local"):
        raise SourceError("Write reports under ignored .local/ or outside the repository.")
    if output.exists():
        if not output.is_file():
            raise SourceError("Report output is not a regular file.")
        try:
            existing = json.loads(output.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise SourceError("Refusing to replace a file that is not a previous review report.") from exc
        if not isinstance(existing, dict) or existing.get("kind") != REPORT_KIND:
            raise SourceError("Refusing to replace a file that is not a previous review report.")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", prefix="review-", suffix=".json",
            dir=output.parent, delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(json.dumps(report, indent=2) + "\n")
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=REPO_ROOT / "upstream.lock.json")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / ".local" / "update-report.json")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args(argv)
    try:
        if not 0 < args.timeout <= 60:
            raise SourceError("--timeout must be above zero and at most 60 seconds.")
        lock = load_lock(args.lock)
        report = collect_report(lock, timeout=args.timeout)
        write_report(report, args.output)
        print(json.dumps({"report": str(args.output), **report["summary"], "pinsChanged": False}, indent=2))
        return 1 if report["summary"]["unavailable"] else 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"Update check unavailable: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
