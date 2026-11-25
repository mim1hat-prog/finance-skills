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


def scan_inventory(files: dict[str, bytes], *, private_literals: tuple[str, ...] = (), exceptions: tuple[dict, ...] = (), max_expanded_bytes: int = 200_000_000) -> dict:
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
        if counters["files"] > 25000 or counters["expandedBytes"] > max_expanded_bytes:
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
            if depth >= 5:
                finding(path, "archive-depth-limit")
                return
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    members = archive.infolist()
                    if len(members) > 5000 or sum(x.file_size for x in members) + counters["expandedBytes"] > max_expanded_bytes:
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
    return {"ok": not findings, **counters, "findings": findings, "reviewedSyntheticExceptionsUsed": len(exceptions_used),
            "limit": "Heuristics plus an explicit public inventory; does not establish source authenticity, licensing or publication approval."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", action="store_true", help="Inspect every frozen release as well as current public sources")
    parser.add_argument("--private-policy", type=Path, help="Optional private JSON list of forbidden literals, outside the repository; values are never printed")
    args = parser.parse_args()
    try:
        import release
        files = release.collect_project(ROOT)
        policy = json.loads((ROOT / "tools/publication-policy.json").read_text(encoding="utf-8"))
        if args.history:
            for p in (ROOT / "releases").rglob("*"):
                if p.is_symlink():
                    raise ValueError("Linked release entry refused")
                if p.is_file():
                    files[p.relative_to(ROOT).as_posix()] = p.read_bytes()
        private = ()
        if args.private_policy:
            private_path = args.private_policy.resolve()
            if private_path.is_relative_to(ROOT.resolve()):
                raise ValueError("Private publication policy must be outside the public repository")
            values = json.loads(private_path.read_text(encoding="utf-8"))
            if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
                raise ValueError("Private policy must be a nonempty-string list")
            private = tuple(values)
        result = scan_inventory(files, private_literals=private, exceptions=tuple(policy["reviewedSyntheticTests"]))
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    except (OSError, ValueError) as exc:
        print(f"Publication check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
