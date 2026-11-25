#!/usr/bin/env python3
"""Acquire reviewed upstream source archives. Never install or execute them."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPO_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "dot-finance-skills-source-review/1.0"
REQUESTED_TOOLS = ("hallmark", "anthropic-skills", "claude-mem", "hyperframes")
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024
MAX_EXPANDED_BYTES = 1024 * 1024 * 1024
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_FILES = 50000
DEFAULT_TIMEOUT = 20
PIN_RE = re.compile(r"^[0-9a-f]{40}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
WINDOWS_RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9¹²³]|LPT[1-9¹²³])(?:\.|$)", re.I)


class SourceError(ValueError):
    """An acquisition cannot proceed without changing its declared contract."""


def load_lock(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schemaVersion") != 1 or not isinstance(data.get("sources"), list):
        raise SourceError("Unsupported upstream lock schema.")
    ids = set()
    for source in data["sources"]:
        if not isinstance(source, dict):
            raise SourceError("Each source must be an object.")
        name = source.get("id", "")
        repo = source.get("repository", "")
        commit = source.get("commit", "")
        checksum = source.get("archiveSha256")
        if not isinstance(name, str) or not ID_RE.fullmatch(name) or name in ids:
            raise SourceError("Every source needs a unique, lowercase tool id.")
        if not isinstance(repo, str) or not REPO_RE.fullmatch(repo):
            raise SourceError("Repository must be an owner/name identifier.")
        if any(part in {".", ".."} for part in repo.split("/")):
            raise SourceError("Repository cannot contain relative path components.")
        if not isinstance(commit, str) or not PIN_RE.fullmatch(commit):
            raise SourceError("Each source must pin a full, lowercase Git commit SHA.")
        if checksum is not None and (
            not isinstance(checksum, str) or not HASH_RE.fullmatch(checksum)
        ):
            raise SourceError("archiveSha256 must be null or a lowercase SHA-256.")
        ids.add(name)
    return data


def validate_https_url(url: str, hosts: set[str]) -> None:
    parts = urllib.parse.urlsplit(url)
    try:
        port = parts.port
    except ValueError as exc:
        raise SourceError("Invalid URL port.") from exc
    if (
        parts.scheme != "https"
        or parts.hostname not in hosts
        or port not in (None, 443)
        or parts.username is not None
        or parts.password is not None
        or parts.fragment
    ):
        raise SourceError("Only HTTPS URLs on the reviewed source hosts are allowed.")


class CheckedRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, hosts: set[str]) -> None:
        super().__init__()
        self.hosts = hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_https_url(newurl, self.hosts)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_archive(
    url: str, output: Path, *, timeout: float = DEFAULT_TIMEOUT,
    max_bytes: int = MAX_ARCHIVE_BYTES,
) -> str:
    hosts = {"codeload.github.com"}
    validate_https_url(url, hosts)
    opener = urllib.request.build_opener(CheckedRedirects(hosts))
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/zip"}
    )
    digest = hashlib.sha256()
    total = 0
    with opener.open(request, timeout=timeout) as response:
        validate_https_url(response.geturl(), hosts)
        declared = response.headers.get("Content-Length")
        if declared and declared.isdecimal() and int(declared) > max_bytes:
            raise SourceError("Archive exceeds the download limit.")
        with output.open("xb") as handle:
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > max_bytes:
                    raise SourceError("Archive exceeds the download limit.")
                digest.update(chunk)
                handle.write(chunk)
    if total == 0:
        raise SourceError("The downloaded archive is empty.")
    return digest.hexdigest()


def safe_member_parts(name: str) -> tuple[str, ...]:
    if not name or "\\" in name or any(ord(c) < 32 for c in name):
        raise SourceError("Archive contains an unsafe path.")
    path = PurePosixPath(name)
    raw_parts = name.rstrip("/").split("/")
    if path.is_absolute() or any(p in {"", ".", ".."} for p in raw_parts):
        raise SourceError("Archive contains an absolute or relative traversal path.")
    for part in raw_parts:
        if any(c in part for c in '<>:"|?*') or part.endswith((" ", ".")) or WINDOWS_RESERVED.match(part):
            raise SourceError("Archive contains a path unsafe on Windows.")
        if part.casefold() == ".git":
            raise SourceError("Archive must not write Git metadata.")
    return tuple(raw_parts)


def validate_archive(
    archive: zipfile.ZipFile, expected_root: str, *,
    max_expanded_bytes: int = MAX_EXPANDED_BYTES,
    max_file_bytes: int = MAX_FILE_BYTES, max_files: int = MAX_FILES,
    archive_only: bool = False,
) -> list[tuple[zipfile.ZipInfo, tuple[str, ...]]]:
    entries = archive.infolist()
    if not entries or len(entries) > max_files:
        raise SourceError("Archive is empty or contains too many entries.")
    seen = set()
    files = set()
    validated = []
    total = 0
    for info in entries:
        # orig_filename preserves a NUL that ZipInfo.filename can otherwise trim.
        parts = safe_member_parts(info.orig_filename)
        if parts[0] != expected_root:
            raise SourceError("Archive root does not match the pinned repository commit.")
        key = "/".join(parts).casefold()
        if key in seen:
            raise SourceError("Archive contains duplicate or case-colliding paths.")
        seen.add(key)
        mode = info.external_attr >> 16
        kind = stat.S_IFMT(mode)
        allowed_kinds = (0, stat.S_IFREG, stat.S_IFDIR, stat.S_IFLNK) if archive_only else (0, stat.S_IFREG, stat.S_IFDIR)
        if kind not in allowed_kinds:
            raise SourceError("Archive contains a symlink or special file.")
        if info.flag_bits & 1:
            raise SourceError("Encrypted archive entries are not supported.")
        if kind == stat.S_IFDIR and not info.is_dir():
            raise SourceError("Archive directory attributes disagree with its path.")
        if info.is_dir() and kind == stat.S_IFREG:
            raise SourceError("Archive file attributes disagree with its path.")
        if info.file_size > max_file_bytes:
            raise SourceError("An archive entry exceeds the file-size limit.")
        if info.file_size > 1024 * 1024 and info.file_size > max(1, info.compress_size) * 1000:
            raise SourceError("Archive contains an excessive compression ratio.")
        total += info.file_size
        if total > max_expanded_bytes:
            raise SourceError("Archive exceeds the expanded-size limit.")
        if not info.is_dir():
            if len(parts) == 1:
                raise SourceError("The pinned archive root must be a directory.")
            files.add(key)
        validated.append((info, parts[1:]))
    for key in seen:
        parts = key.split("/")
        if any("/".join(parts[:i]) in files for i in range(1, len(parts))):
            raise SourceError("An archive file conflicts with a parent directory.")
    if not files:
        raise SourceError("Archive contains no source files.")
    return validated


def choose_destination(destination: Path, repo_root: Path = REPO_ROOT) -> Path:
    destination = destination.expanduser().absolute()
    if destination.is_symlink():
        raise SourceError("Destination must not be a symbolic link.")
    resolved = destination.resolve()
    try:
        relative = resolved.relative_to(repo_root.resolve())
    except ValueError:
        return resolved
    if not relative.parts or relative.parts[0] != "upstream-sources":
        raise SourceError(
            "Inside the repository, use only ignored upstream-sources/; "
            "otherwise choose a destination outside the repository."
        )
    return resolved


def source_target(source: dict, destination: Path) -> Path:
    return destination / (source["id"] + "-" + source["commit"][:12])


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def acquire_source(
    source: dict, destination: Path, *, timeout: float = DEFAULT_TIMEOUT,
    archive_only: bool = False, download_fn=None,
) -> dict:
    target = source_target(source, destination)
    if target.exists() or target.is_symlink():
        raise SourceError(f"Refusing to overwrite existing source target: {target.name}")
    destination.mkdir(parents=True, exist_ok=True)
    repository = source["repository"]
    commit = source["commit"]
    url = f"https://codeload.github.com/{repository}/zip/{commit}"
    expected_root = repository.split("/")[1] + "-" + commit
    downloader = download_fn or download_archive
    target_created = False
    with tempfile.TemporaryDirectory(prefix="finance-source-", dir=destination) as tmp:
        archive_path = Path(tmp) / "source.zip"
        digest = downloader(url, archive_path, timeout=timeout)
        # Re-read bytes: the receipt must describe the archive that is extracted.
        actual = file_sha256(archive_path)
        if digest != actual:
            raise SourceError("Download receipt does not match the archive bytes.")
        expected = source.get("archiveSha256")
        if expected is not None and actual != expected:
            raise SourceError("Archive SHA-256 differs from the reviewed lock.")
        try:
            with zipfile.ZipFile(archive_path) as archive:
                entries = validate_archive(archive, expected_root, archive_only=archive_only)
                # Exclusive creation prevents replacing a pre-existing directory.
                target.mkdir(exist_ok=False)
                target_created = True
                if archive_only:
                    with archive_path.open("rb") as incoming, (target / "source.zip").open("xb") as outgoing:
                        shutil.copyfileobj(incoming, outgoing, length=1024 * 1024)
                else:
                    source_dir = target / "source"
                    source_dir.mkdir()
                    for info, parts in entries:
                        if not parts:
                            continue
                        path = source_dir.joinpath(*parts)
                        if info.is_dir():
                            path.mkdir(parents=True, exist_ok=True)
                        else:
                            path.parent.mkdir(parents=True, exist_ok=True)
                            with archive.open(info) as incoming, path.open("xb") as outgoing:
                                shutil.copyfileobj(incoming, outgoing, length=1024 * 1024)
                            if path.stat().st_size != info.file_size:
                                raise SourceError("Extracted file size differs from its archive.")
                receipt = {
                    "schemaVersion": 1,
                    "kind": "finance-skills-source-acquisition",
                    "id": source["id"],
                    "repository": repository,
                    "commit": commit,
                    "archiveUrl": url,
                    "archiveSha256": actual,
                    "integrity": "matched_reviewed_checksum" if expected else "checksum_recorded_unbaselined",
                    "stage": "source_archive_saved" if archive_only else "source_prepared",
                    "runtimeInstalled": False,
                    "upstreamCodeExecuted": False,
                    "workPcHostActivated": False,
                    "sourceDirectory": None if archive_only else "source",
                    "archiveFile": "source.zip" if archive_only else None,
                    "unextractedSymlinkEntries": sum(
                        stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK
                        for info, _ in entries
                    ) if archive_only else 0,
                }
                (target / "SOURCE-RECEIPT.json").write_text(
                    json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
                )
                return receipt
        except Exception:
            if target_created:
                shutil.rmtree(target)
            raise


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=REPO_ROOT / "upstream.lock.json")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--tool", action="append", help="Tool id; repeat for several sources.")
    selection.add_argument("--all", action="store_true", help="Fetch the four explicitly requested sources.")
    parser.add_argument(
        "--destination", type=Path, default=REPO_ROOT / "upstream-sources",
        help="Source destination. Default: ignored upstream-sources/ in this repository.",
    )
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--archive-only", action="store_true",
        help="Keep original ZIP and receipt; never extract any entry. Useful for sources containing symlinks.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        if not 0 < args.timeout <= 60:
            raise SourceError("--timeout must be above zero and at most 60 seconds.")
        lock = load_lock(args.lock)
        sources = {source["id"]: source for source in lock["sources"]}
        selected = list(REQUESTED_TOOLS) if args.all else list(dict.fromkeys(args.tool))
        unknown = set(selected) - sources.keys()
        if unknown:
            raise SourceError("Unknown source ids: " + ", ".join(sorted(unknown)))
        destination = choose_destination(args.destination)
        for name in selected:
            target = source_target(sources[name], destination)
            if target.exists() or target.is_symlink():
                raise SourceError(f"Refusing to overwrite existing source target: {target.name}")
        results = []
        for name in selected:
            try:
                receipt = acquire_source(
                    sources[name], destination, timeout=args.timeout,
                    archive_only=args.archive_only,
                )
                results.append(receipt)
            except (OSError, SourceError, zipfile.BadZipFile, urllib.error.URLError) as exc:
                results.append({"id": name, "stage": "unavailable", "error": str(exc)})
        print(json.dumps({
            "destination": str(destination), "sources": results,
            "runtimeInstalled": False,
            "note": "Source acquisition only. Review and activate a supported host separately.",
        }, indent=2))
        return 1 if any(result["stage"] == "unavailable" for result in results) else 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"Source acquisition stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
