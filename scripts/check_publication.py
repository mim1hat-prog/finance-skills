"""Read-only leakage checks for public source inventories and nested release ZIPs."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from urllib.parse import parse_qsl, urlsplit
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BLOCKED_PARTS = {"private", "work-data", "outputs", "credentials", "secrets", ".git", ".venv", "__pycache__"}
BLOCKED_EXTENSIONS = {".xlsx", ".xlsm", ".xlsb", ".xls", ".docx", ".pptx", ".pbix", ".pbit", ".one", ".msg", ".eml", ".pst", ".pdf", ".sqlite", ".db"}
URL = re.compile(r"https?://[^\s<>\"'`\]\)]+", re.I)
SECRET_KEYS = {"apikey", "appid", "accesstoken", "refreshtoken", "clientsecret", "password", "authorization", "credential"}
MAX_EXPANDED_BYTES = 200_000_000
MAX_FILES = 25_000
MAX_ARCHIVE_MEMBERS = 5_000
MAX_ARCHIVE_DEPTH = 5
LIMIT_NOTE = "Heuristics plus an explicit public inventory; does not establish source authenticity, licensing or publication approval."


def _scan_inventory(files: dict[str, bytes], *, private_literals: tuple[str, ...] = (), exceptions: tuple[dict, ...] = (), max_expanded_bytes: int = MAX_EXPANDED_BYTES) -> tuple[dict, set]:
    """Inspect bytes without extraction/network; a pass is not publication approval."""
    findings: list[dict] = []
    counters = {"files": 0, "expandedBytes": 0, "archives": 0}
    reviewed = set()
    for record in exceptions:
        if (set(record) != {"path", "sha256", "code", "reason"}
                or record["code"] != "credential-in-url"
                or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"])
                or not record["path"].startswith("tests/") or not record["reason"].strip()):
            raise ValueError("Invalid reviewed synthetic-test exception")
        reviewed.add((record["path"], record["sha256"], record["code"]))
    inspected_hashes = {}
    exceptions_used = set()

    def finding(path: str, code: str) -> None:
        key = (path.rsplit("!/", 1)[-1], inspected_hashes.get(path), code)
        if key in reviewed:
            exceptions_used.add(key)
            return
        record = {"path": path, "code": code}
        if record not in findings:
            findings.append(record)

    def json_secrets(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                normalized = re.sub(r"[^a-z]", "", str(key).lower())
                if normalized in SECRET_KEYS and isinstance(child, str) and child.strip():
                    finding(path, "credential-value-in-json")
                json_secrets(child, path)
        elif isinstance(value, list):
            for child in value:
                json_secrets(child, path)

    def inspect(path: str, data: bytes, depth: int) -> None:
        inspected_hashes[path] = hashlib.sha256(data).hexdigest()
        counters["files"] += 1
        counters["expandedBytes"] += len(data)
        if counters["files"] > MAX_FILES or counters["expandedBytes"] > max_expanded_bytes:
            raise ValueError("Publication inspection limit exceeded; split and review explicitly")
        inner = path.rsplit("!/", 1)[-1]
        parts = PurePosixPath(inner).parts
        if (not parts or inner.startswith(("/", "\\")) or "\\" in inner
                or any(p in {"..", "."} for p in parts)):
            finding(path, "unsafe-package-path")
        if any(p.lower() in BLOCKED_PARTS or p.lower() == ".env" or p.lower().startswith(".env.") for p in parts):
            finding(path, "private-or-runtime-path")
        suffix = PurePosixPath(inner).suffix.lower()
        if suffix in BLOCKED_EXTENSIONS:
            finding(path, "opaque-office-data-or-document")
            return
        if suffix == ".zip":
            counters["archives"] += 1
            if depth >= MAX_ARCHIVE_DEPTH:
                finding(path, "archive-depth-limit")
                return
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    members = archive.infolist()
                    if len(members) > MAX_ARCHIVE_MEMBERS or sum(x.file_size for x in members) + counters["expandedBytes"] > max_expanded_bytes:
                        finding(path, "archive-expansion-limit")
                        return
                    seen = set()
                    for info in members:
                        if info.filename.casefold() in seen:
                            finding(path, "duplicate-archive-path")
                        seen.add(info.filename.casefold())
                        member = path + "!/" + info.filename
                        if info.flag_bits & 1 or stat.S_ISLNK(info.external_attr >> 16):
                            finding(member, "encrypted-or-linked-archive-member")
                            continue
                        if not info.is_dir():
                            inspect(member, archive.read(info), depth + 1)
            except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError):
                finding(path, "unreadable-archive")
            return
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            finding(path, "unreviewed-binary-artifact")
            return
        if any(value and value.casefold() in text.casefold() for value in private_literals):
            finding(path, "private-review-marker")
        if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", text):
            finding(path, "private-key-material")
        if re.search(r"authorization\s*:\s*(?:bearer|basic)\s+[A-Za-z0-9+/=_-]{16,}", text, re.I):
            finding(path, "authorization-value")
        for match in URL.finditer(text):
            try:
                parsed = urlsplit(match.group())
                host = (parsed.hostname or "").lower()
                if (host.endswith((".sharepoint.com", ".onmicrosoft.com", ".corp", ".internal"))
                        or (host == "teams.microsoft.com" and parsed.path.startswith("/l/"))
                        or (host in {"outlook.office.com", "outlook.office365.com"} and parsed.path.startswith(("/mail/", "/calendar/")))):
                    finding(path, "private-enterprise-link")
                if parsed.username or parsed.password:
                    finding(path, "credential-in-url")
                if any(re.sub(r"[^a-z]", "", key.lower()) in SECRET_KEYS for key, _ in parse_qsl(parsed.query)):
                    finding(path, "credential-query-parameter")
            except ValueError:
                finding(path, "malformed-source-url")
        if suffix in {".json", ".yaml", ".yml"}:
            try:
                json_secrets(json.loads(text), path)
            except json.JSONDecodeError:
                pass  # YAML source is also covered by text/URL checks; schema validation is a separate gate.

    for path, data in sorted(files.items()):
        inspect(path, data, 0)
    return ({"ok": not findings, **counters, "findings": findings, "reviewedSyntheticExceptionsUsed": len(exceptions_used),
             "limit": LIMIT_NOTE}, exceptions_used)


def scan_inventory(files: dict[str, bytes], *, private_literals: tuple[str, ...] = (),
                   exceptions: tuple[dict, ...] = (), max_expanded_bytes: int = MAX_EXPANDED_BYTES) -> dict:
    """Inspect one bounded inventory, retaining the original single-batch contract."""
    return _scan_inventory(files, private_literals=private_literals, exceptions=exceptions,
                           max_expanded_bytes=max_expanded_bytes)[0]


def _verified_release_files(root: Path, manifest: dict) -> dict[str, bytes]:
    """Read one verified snapshot and reject changes after its integrity check."""
    import release

    version = manifest["version"]
    release.version_key(version)
    folder = root / "releases" / f"v{version}"
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Linked or missing frozen release directory refused")
    names = {row["path"] for row in manifest["files"]} | {"manifest.json", "SHA256SUMS.txt"}
    if {path.name for path in folder.iterdir()} != names:
        raise ValueError(f"Frozen release inventory changed before inspection: v{version}")
    files = {name: release.read_regular(folder / name) for name in sorted(names)}
    if json.loads(files["manifest.json"]) != manifest:
        raise ValueError(f"Frozen release manifest changed before inspection: v{version}")
    for row in manifest["files"]:
        if release.file_record(row["path"], files[row["path"]]) != {
                key: row[key] for key in ("path", "bytes", "sha256")}:
            raise ValueError(f"Frozen release bytes changed before inspection: v{version}")
    if release.sums({name: content for name, content in files.items() if name != "SHA256SUMS.txt"}) != files["SHA256SUMS.txt"]:
        raise ValueError(f"Frozen release checksum list changed before inspection: v{version}")
    return {f"releases/v{version}/{name}": content for name, content in files.items()}


def scan_project(root: Path, *, sources: dict[str, bytes] | None = None,
                 include_history: bool = False, private_literals: tuple[str, ...] = (),
                 exceptions: tuple[dict, ...] = (), max_expanded_bytes: int = MAX_EXPANDED_BYTES) -> dict:
    """Scan current sources/index together, then each integrity-verified release.

    A version gets its own budget only after the existing immutable-release verifier
    accepts its exact directory and inventory. Arbitrary path prefixes cannot make
    new batches. Every batch keeps the same file, expansion and nesting ceilings.
    """
    import release

    current = dict(sources if sources is not None else release.collect_project(root))
    if not include_history:
        return scan_inventory(current, private_literals=private_literals, exceptions=exceptions,
                              max_expanded_bytes=max_expanded_bytes)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Publication project root must be a regular directory")
    for path in current:
        release.safe_path(path)
        if path.split("/", 1)[0].casefold() == "releases":
            raise ValueError("Supply current sources separately; release paths must come from verified snapshots")
    folder = root / "releases"
    if folder.is_symlink():
        raise ValueError("Linked releases directory refused")
    manifests = release.existing_versions(folder) if folder.exists() else []
    for name in ("README.md", "latest.json"):
        path = folder / name
        if path.exists() or path.is_symlink():
            current[f"releases/{name}"] = release.read_regular(path)

    batches = []
    assigned = set()
    used_exceptions = set()

    def inspect_batch(batch_id: str, kind: str, files: dict[str, bytes], version: str | None = None) -> None:
        if assigned.intersection(files):
            raise ValueError("Publication batch inventories overlap")
        assigned.update(files)
        try:
            checked, used = _scan_inventory(files, private_literals=private_literals, exceptions=exceptions,
                                            max_expanded_bytes=max_expanded_bytes)
        except ValueError as exc:
            raise ValueError(f"Publication batch {batch_id}: {exc}") from exc
        used_exceptions.update(used)
        inventory = [{"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                     for path, data in sorted(files.items())]
        inventory_hash = hashlib.sha256(json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        batches.append({"id": batch_id, "kind": kind, **({"version": version} if version is not None else {}),
                        "topLevelFiles": len(files), "inventorySha256": inventory_hash,
                        **{key: value for key, value in checked.items() if key != "limit"}})

    inspect_batch("current-project", "current-project-and-release-index", current)
    for manifest in manifests:
        version = manifest["version"]
        inspect_batch(f"release-v{version}", "verified-frozen-release",
                      _verified_release_files(root, manifest), version)
    findings = [finding for batch in batches for finding in batch["findings"]]
    return {"ok": not findings, "strategy": "current-project-and-each-verified-release",
            "batchCount": len(batches), "topLevelFiles": len(assigned),
            "perBatchLimits": {"maxExpandedBytes": max_expanded_bytes, "maxFiles": MAX_FILES,
                               "maxArchiveMembers": MAX_ARCHIVE_MEMBERS, "maxArchiveDepth": MAX_ARCHIVE_DEPTH},
            **{key: sum(batch[key] for batch in batches) for key in ("files", "expandedBytes", "archives")},
            "findings": findings, "reviewedSyntheticExceptionsUsed": len(used_exceptions),
            "verifiedReleaseVersions": [manifest["version"] for manifest in manifests],
            "batches": batches, "limit": LIMIT_NOTE}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", action="store_true", help="Inspect every frozen release as well as current public sources")
    parser.add_argument("--private-policy", type=Path, help="Optional private JSON list of forbidden literals, outside the repository; values are never printed")
    args = parser.parse_args()
    try:
        import release
        files = release.collect_project(ROOT)
        policy = json.loads((ROOT / "tools/publication-policy.json").read_text(encoding="utf-8"))
        private = ()
        if args.private_policy:
            private_path = args.private_policy.resolve()
            if private_path.is_relative_to(ROOT.resolve()):
                raise ValueError("Private publication policy must be outside the public repository")
            values = json.loads(private_path.read_text(encoding="utf-8"))
            if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
                raise ValueError("Private policy must be a nonempty-string list")
            private = tuple(values)
        result = scan_project(ROOT, sources=files, include_history=args.history,
                              private_literals=private, exceptions=tuple(policy["reviewedSyntheticTests"]))
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    except (OSError, ValueError) as exc:
        print(f"Publication check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
