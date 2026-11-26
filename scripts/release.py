"""Freeze deterministic repository-hosted downloads; no network or GitHub Release API."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

# A clean --check must not create build.pyc in the checkout.
sys.dont_write_bytecode = True
import build

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
REPOSITORY = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)\Z")
ROOT_FILES = {
    ".gitattributes", ".gitignore", "AGENTS.md", "CHANGELOG.md", "DESIGN.md",
    "LICENSE", "NOTICE", "PRODUCT.md", "README.md", "SKILLS.md", "TOOLS.md", "catalog.json",
    "CITATION.cff", "CONTRIBUTING.md", "SECURITY.md",
    "SUPPORT.md", "CODE_OF_CONDUCT.md",
    ".github/ISSUE_TEMPLATE/bug_report.md", ".github/ISSUE_TEMPLATE/skill_request.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "upstream.lock.json", "requirements.txt", "requirements-duckdb.txt", "requirements-xlsx.txt",
}
DIRECTORIES = {
    "api": {".yaml", ".yml", ".json", ".md"},
    "benchmarks": {".json", ".csv", ".md", ".txt"},
    "research": {".json", ".yaml", ".yml", ".md", ".txt"},
    "metrics": {".json", ".md"},
    "schemas": {".json"}, "tools": {".json", ".md"},
    "adapters": {".md"}, "assets": {".svg", ".png", ".jpg", ".jpeg", ".webp", ".txt", ".md"},
    "branding": {".css", ".json", ".svg", ".png", ".md", ".txt", ""},
    "docs": {".md", ".txt", ".json", ".svg", ".png"}, "editions": {".md", ".txt"},
    "examples": {".csv", ".json", ".md", ".txt", ".sql", ".py"},
    "evaluations": {".json", ".md"},
    "packages": {".zip", ".json"}, "profiles": {".txt", ".md", ".json"},
    "release-notes": {".md"}, "requirements": {".txt", ".lock", ".toml"},
    "scripts": {".py", ".ps1", ".cmd", ".bat", ".sh", ".mjs", ".js", ".json"},
    "site": {".html", ".css", ".js", ".svg", ".json"}, "skills": {".md"},
    "tests": {".py", ".json", ".csv", ".txt", ".md", ".zip"},
}
EXCLUDED_PARTS = {
    "__pycache__", "node_modules", "venv", "private", "work-data", "outputs",
    "upstream-sources", "runtime", "tmp", "temp", "dist", "build", "coverage", "releases",
}
REQUIRED = {"README.md", "AGENTS.md", "LICENSE", "catalog.json", "docs/RELEASES.md",
            "scripts/build.py", "scripts/release.py"}
VARIANTS_BY_SCHEMA = {
    1: ("copilot", "gemini", "all", "full"),
    2: ("copilot", "gemini", "all", "markdown", "full"),
    3: ("copilot-suite", "gemini-suite", "copilot", "gemini", "all", "markdown", "full"),
    4: ("excel-onedrive", "copilot-suite", "gemini-suite", "copilot", "gemini", "all", "markdown", "full"),
}
BUNDLE_PATHS = {
    "copilot": "packages/bundles/finance-skills-copilot.zip",
    "gemini": "packages/bundles/finance-skills-gemini.zip",
    "all": "packages/bundles/finance-skills-all.zip",
    "markdown": "packages/markdown/finance-skills-markdown.zip",
    "copilot-suite": "packages/suites/finance-suite-copilot.zip",
    "gemini-suite": "packages/suites/finance-suite-gemini.zip",
    "excel-onedrive": "packages/excel/finance-suite-onedrive.zip",
}
LOCK_NAME = ".release.lock"


class ReleaseError(ValueError):
    """A release cannot be generated or verified without changing its contract."""


def version_key(value: str) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(value) if isinstance(value, str) else None
    if not match:
        raise ReleaseError("Use a stable SemVer such as 1.1.0, without a v prefix or leading zeroes")
    return tuple(map(int, match.groups()))


def safe_path(name: str) -> str:
    """Reject paths that extract ambiguously or escape a Windows project directory."""
    if not isinstance(name, str) or not name or "\\" in name:
        raise ReleaseError(f"Unsafe archive path: {name!r}")
    for part in name.split("/"):
        stem = part.split(".", 1)[0].upper()
        if (not part or part in {".", ".."} or part.endswith((".", " "))
                or re.search(r'[<>:"|?*\x00-\x1f]', part)
                or stem in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
                or re.fullmatch(r"(?:COM|LPT)[1-9]", stem)):
            raise ReleaseError(f"Unsafe archive path: {name!r}")
    return name


def read_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ReleaseError(f"Expected a regular file, not a symlink: {path.name}")
    return path.read_bytes()


def public_path(name: str) -> bool:
    parts = safe_path(name).split("/")
    if name in ROOT_FILES:
        return True
    if len(parts) == 1:
        return False
    return (parts[0] in DIRECTORIES and Path(parts[-1]).suffix.lower() in DIRECTORIES[parts[0]]
            and all(not p.startswith(".") and p.casefold() not in EXCLUDED_PARTS for p in parts[1:]))


def collect_project(root: Path) -> dict[str, bytes]:
    """Only explicit public project roots/file types are eligible for the full ZIP."""
    if root.is_symlink() or not root.is_dir():
        raise ReleaseError("Project root must be a regular directory")
    files: dict[str, bytes] = {}
    seen: set[str] = set()

    def add(path: Path) -> None:
        if any(parent.is_symlink() for parent in path.parents if parent != root.parent):
            raise ReleaseError("Linked parent in explicit public files")
        name = safe_path(path.relative_to(root).as_posix())
        if name.casefold() in seen:
            raise ReleaseError(f"Windows case collision: {name}")
        seen.add(name.casefold())
        files[name] = read_regular(path)

    def walk(folder: Path, extensions: set[str]) -> None:
        if folder.is_symlink() or not folder.is_dir():
            raise ReleaseError(f"Expected an unlinked project directory: {folder.name}")
        for path in sorted(folder.iterdir()):
            if path.is_symlink():
                raise ReleaseError(f"Symlink in project sources: {path.relative_to(root)}")
            if (path.name.startswith(".") or path.name.casefold() in EXCLUDED_PARTS
                    or path.name.casefold() == "thumbs.db"):
                continue
            if path.is_dir():
                walk(path, extensions)
            elif not path.is_file():
                raise ReleaseError(f"Non-regular project entry: {path.relative_to(root)}")
            elif path.suffix.lower() in extensions:
                add(path)

    for name in sorted(ROOT_FILES):
        path = root / name
        if path.exists() or path.is_symlink():
            add(path)
    for name, extensions in sorted(DIRECTORIES.items()):
        path = root / name
        if path.exists() or path.is_symlink():
            walk(path, extensions)
    missing = REQUIRED - files.keys()
    if missing:
        raise ReleaseError("Missing release project files: " + ", ".join(sorted(missing)))
    return dict(sorted(files.items()))


def verify_build(root: Path, sources: dict[str, bytes]) -> None:
    expected = build.generate(root)
    expected_names = {path.as_posix() for path in expected}
    actual_names = set()
    for name in ("editions", "packages", "profiles"):
        folder = root / name
        if folder.is_symlink():
            raise ReleaseError(f"Symlink in generated outputs: {name}")
        for path in folder.rglob("*"):
            if path.is_symlink():
                raise ReleaseError(f"Symlink in generated outputs: {path.relative_to(root)}")
            if path.is_file():
                actual_names.add(path.relative_to(root).as_posix())
    unexpected = actual_names - expected_names
    stale = [path.as_posix() for path, content in expected.items()
             if sources.get(path.as_posix()) != content]
    if unexpected or stale:
        raise ReleaseError("Current build drift; run scripts/build.py and review outputs. "
                           f"Unexpected: {sorted(unexpected)}; stale: {sorted(stale)}")


def file_record(name: str, data: bytes) -> dict:
    return {"path": safe_path(name), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def sums(files: dict[str, bytes]) -> bytes:
    return "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n"
                   for name, data in sorted(files.items())).encode("utf-8")


def embedded_notes(notes: str, version: str) -> str:
    lines = notes.removeprefix(f"# Finance skills v{version}\n").strip().splitlines()
    output, fence = [], None
    for line in lines:
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        elif fence is None:
            line = re.sub(r"^(#{1,5}) ", r"#\1 ", line)
        output.append(line)
    return "\n".join(output)


def prepare(root: Path, download_ref: str = "main") -> tuple[dict, dict[str, bytes], dict[str, bytes]]:
    sources = collect_project(root)
    catalog = json.loads(sources["catalog.json"])
    if not isinstance(catalog, dict):
        raise ReleaseError("Catalogue must be a JSON object")
    markdown_version = catalog.get("markdownBundleVersion")
    if markdown_version is not None and (type(markdown_version) is not int or markdown_version != 1):
        raise ReleaseError("Unsupported Markdown bundle version")
    suite_version = catalog.get("suitePackageVersion")
    if "suitePackageVersion" in catalog:
        if type(suite_version) is not int or suite_version not in (1, 2):
            raise ReleaseError("Unsupported suite package version")
        if type(markdown_version) is not int or markdown_version != 1:
            raise ReleaseError("Suite packages require Markdown bundle version 1")
    excel_folder_version = catalog.get("excelFolderBundleVersion")
    if "excelFolderBundleVersion" in catalog:
        if type(excel_folder_version) is not int or excel_folder_version != 1:
            raise ReleaseError("Unsupported Excel folder bundle version")
        if suite_version != 2:
            raise ReleaseError("Excel folder bundle requires grouped suite package version 2")
    schema_version = 2 if markdown_version == 1 else 1
    if suite_version in (1, 2):
        schema_version = 3
    if excel_folder_version == 1:
        schema_version = 4
    variants = VARIANTS_BY_SCHEMA[schema_version]
    version = catalog.get("version")
    version_key(version)
    repo_value = catalog.get("repoUrl")
    repo = repo_value.rstrip("/") if isinstance(repo_value, str) else ""
    match = REPOSITORY.fullmatch(repo)
    if not match or match[1] in {".", ".."} or match[2] in {".", ".."}:
        raise ReleaseError("Catalogue repoUrl must identify one HTTPS GitHub repository")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", download_ref) or ".." in download_ref:
        raise ReleaseError("Download ref must be a single branch/tag name or commit, such as main")
    notes_path = f"release-notes/v{version}.md"
    if notes_path not in sources or not sources[notes_path].strip():
        raise ReleaseError(f"Missing non-empty release notes: {notes_path}")
    notes = sources[notes_path].decode("utf-8")
    notes_body = embedded_notes(notes, version)
    verify_build(root, sources)
    if catalog.get("workflowContractsVersion") is not None:
        import project_gates
        project_gates.validate(root, sources=sources)
    if collect_project(root) != sources:
        raise ReleaseError("Project changed while preparing the release; retry after edits finish")
    prefix = f"finance-skills-v{version}"
    raw = f"https://raw.githubusercontent.com/{match[1]}/{match[2]}/{download_ref}/releases/v{version}"
    files = {f"{prefix}-{variant}.zip": sources[BUNDLE_PATHS[variant]]
             for variant in variants if variant != "full"}
    files[f"{prefix}-full.zip"] = build.archive_files(sources)
    labels = {"copilot": "Copilot skills", "gemini": "Gemini skills", "all": "Both editions",
              "markdown": "Copy-and-paste Markdown only",
              "copilot-suite": "Copilot complete suite — upload unchanged: one skill, all workflows",
              "gemini-suite": "Gemini complete suite — upload unchanged: one skill, all workflows",
              "excel-onedrive": "Copilot in Excel — extract, then Upload Folder to OneDrive",
              "full": "Full project, tools and documentation"}
    if schema_version >= 3:
        labels.update(copilot="Individual Copilot packages — extract first",
                      gemini="Individual Gemini packages — extract first",
                      all="Both individual editions — extract first")
    lines = [f"# Finance skills v{version}", "", "## Downloads", "",
             "These are the frozen repository-hosted files. GitHub Release assets are published and verified separately.", "",
             "| Download | File |", "| --- | --- |"]
    lines += [f"| {labels[v]} | [{prefix}-{v}.zip]({raw}/{prefix}-{v}.zip) |" for v in variants]
    if schema_version == 4:
        lines += ["", "For Copilot in Excel, extract the Excel OneDrive ZIP first, then upload the inner "
                  "finance-suite folder using Upload Folder in the OneDrive skills location opened by Excel. "
                  "The folder contains SKILL.md and all references. Select Refresh in Excel, then invoke "
                  "@finance-suite. Do not upload this folder-transport ZIP through a native ZIP-import screen. "
                  "Native account activation and task execution remain unverified."]
    if schema_version >= 3:
        lead = ("For hosts with native ZIP import, upload the complete Copilot or Gemini suite ZIP unchanged. "
                if schema_version == 4 else
                "For one import, upload the complete Copilot or Gemini suite ZIP unchanged. ")
        lines += ["", lead +
                  f"Each registers one finance-suite skill containing {len(catalog['skills'])} workflow references. "
                  "It does not register the workflows as separate native skills. "
                  "Keep the reference files with SKILL.md when replacing the suite."]
        if suite_version == 2:
            suite_manifest = json.loads(sources["packages/suites/manifest.json"])
            companion_counts = {p["companionFileCount"] for p in suite_manifest["packages"]}
            if len(companion_counts) != 1:
                raise ReleaseError("Grouped suite companion counts differ between editions")
            lines += ["", f"The complete workflows are grouped into {companion_counts.pop()} Markdown companion files, "
                      "within the project's 20-companion portability ceiling. All workflow procedures remain complete. "
                      "The earlier v1.5.0 suite has 29 companion files and exceeds Cowork's documented 20-companion limit. "
                      "Use the current package; host acceptance and tenant permissions remain separate checks."]
    if schema_version >= 2:
        lines += ["", "For copy and paste, extract the Markdown-only ZIP, open START-HERE.md, "
                  "then copy the relevant Copilot or Gemini file. Every file in that ZIP is Markdown."]
    lines += ["", "Extract a transport bundle before importing individual native skill ZIPs. "
              "The full project archive contains source, tools and documentation; it is not a native skill import.",
              "", f"[SHA-256 checksums]({raw}/SHA256SUMS.txt) · [Release manifest]({raw}/manifest.json)",
              "", "## Release notes", "", notes_body, ""]
    files["README.md"] = "\n".join(lines).encode("utf-8")
    manifest = {
        "schemaVersion": schema_version, "kind": "repository-hosted-release", "version": version,
        "repository": repo, "downloadRef": download_ref, "reviewedOn": catalog["reviewedOn"],
        "skillCount": len(catalog["skills"]), "notes": file_record(notes_path, sources[notes_path]),
        "files": [dict(file_record(name, content), downloadUrl=f"{raw}/{name}")
                  for name, content in sorted(files.items())],
        "projectFiles": [file_record(name, content) for name, content in sources.items()],
    }
    files["manifest.json"] = build.json_bytes(manifest)
    files["SHA256SUMS.txt"] = sums(files)
    return manifest, files, sources


def verify_frozen(directory: Path) -> dict:
    if directory.is_symlink() or not directory.is_dir() or not directory.name.startswith("v"):
        raise ReleaseError("Release snapshot must be a regular version directory")
    version = directory.name[1:]
    version_key(version)
    manifest_bytes = read_regular(directory / "manifest.json")
    manifest = json.loads(manifest_bytes)
    if not isinstance(manifest, dict):
        raise ReleaseError(f"Invalid release manifest for {directory.name}")
    schema_version = manifest.get("schemaVersion")
    if (type(schema_version) is not int or schema_version not in VARIANTS_BY_SCHEMA
            or manifest.get("kind") != "repository-hosted-release" or manifest.get("version") != version):
        raise ReleaseError(f"Invalid release manifest for {directory.name}")
    names = {f"finance-skills-v{version}-{v}.zip" for v in VARIANTS_BY_SCHEMA[schema_version]} | {"README.md"}
    all_names = names | {"manifest.json", "SHA256SUMS.txt"}
    if {p.name for p in directory.iterdir()} != all_names:
        raise ReleaseError(f"Unexpected or missing files in frozen {directory.name}")
    files = {name: read_regular(directory / name) for name in sorted(all_names)}
    if files["manifest.json"] != manifest_bytes:
        raise ReleaseError(f"Release manifest changed while verifying {directory.name}")
    repo = manifest.get("repository")
    ref = manifest.get("downloadRef")
    if (not isinstance(repo, str) or not REPOSITORY.fullmatch(repo) or not isinstance(ref, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", ref) or ".." in ref):
        raise ReleaseError(f"Invalid download location in {directory.name}")
    match = REPOSITORY.fullmatch(repo)
    raw = f"https://raw.githubusercontent.com/{match[1]}/{match[2]}/{ref}/releases/v{version}"
    records = manifest.get("files", [])
    if (not isinstance(records, list) or len(records) != len(names)
            or any(not isinstance(r, dict) or not isinstance(r.get("path"), str) for r in records)
            or {r.get("path") for r in records} != names):
        raise ReleaseError(f"Invalid release file inventory for {directory.name}")
    for record in records:
        if (type(record.get("bytes")) is not int or record.get("downloadUrl") != f"{raw}/{record['path']}"
                or file_record(record["path"], files[record["path"]]) != {k: record.get(k) for k in ("path", "bytes", "sha256")}):
            raise ReleaseError(f"Frozen release checksum mismatch: {directory.name}/{record['path']}")
    if sums({k: v for k, v in files.items() if k != "SHA256SUMS.txt"}) != files["SHA256SUMS.txt"]:
        raise ReleaseError(f"Frozen checksum list mismatch: {directory.name}")
    project = manifest.get("projectFiles", [])
    if (not isinstance(project, list) or not project
            or any(not isinstance(r, dict) or not isinstance(r.get("path"), str) for r in project)):
        raise ReleaseError(f"Missing full-project inventory: {directory.name}")
    with zipfile.ZipFile(io.BytesIO(files[f"finance-skills-v{version}-full.zip"])) as archive:
        paths = [safe_path(r["path"]) for r in project]
        if (any(not public_path(p) for p in paths) or len(paths) != len(set(p.casefold() for p in paths))
                or archive.namelist() != sorted(paths)):
            raise ReleaseError(f"Full-project path inventory mismatch: {directory.name}")
        for record in project:
            if type(record.get("bytes")) is not int or file_record(record["path"], archive.read(record["path"])) != record:
                raise ReleaseError(f"Full-project content mismatch: {directory.name}/{record['path']}")
        if schema_version >= 3:
            for variant in ("copilot-suite", "gemini-suite"):
                source_path = BUNDLE_PATHS[variant]
                if (source_path not in paths
                        or archive.read(source_path) != files[f"finance-skills-v{version}-{variant}.zip"]):
                    raise ReleaseError(f"Frozen suite package differs from full-project source: {directory.name}/{variant}")
        if schema_version == 4:
            verify_excel_folder(files[f"finance-skills-v{version}-excel-onedrive.zip"], archive,
                                paths, version, directory.name)
    return manifest


def verify_excel_folder(payload: bytes, project: zipfile.ZipFile, paths: list[str],
                        version: str, label: str) -> None:
    """Independently verify the folder transport and its external inventory."""
    source_path = BUNDLE_PATHS["excel-onedrive"]
    metadata_path = "packages/excel/manifest.json"
    suite_path = BUNDLE_PATHS["copilot-suite"]
    source_folder = "editions/copilot-suite/finance-suite"
    if any(path not in paths for path in (source_path, metadata_path, suite_path)):
        raise ReleaseError(f"Missing Excel folder source or inventory: {label}")
    if project.read(source_path) != payload:
        raise ReleaseError(f"Frozen Excel folder differs from full-project source: {label}")
    suite_payload = project.read(suite_path)
    with zipfile.ZipFile(io.BytesIO(suite_payload)) as suite:
        if len(suite.namelist()) != len(set(suite.namelist())):
            raise ReleaseError(f"Duplicate source suite resource: {label}")
        members = {name: suite.read(name) for name in suite.namelist()}
    try:
        build.validate_portable_suite_members(members, suite_payload)
    except ValueError as exc:
        raise ReleaseError(f"Invalid Excel source suite: {label}: {exc}") from exc
    expected = {f"finance-suite/{name}": content for name, content in members.items()}
    with zipfile.ZipFile(io.BytesIO(payload)) as folder:
        if folder.namelist() != sorted(expected):
            raise ReleaseError(f"Excel folder must contain exactly the finance-suite folder: {label}")
        for name, content in expected.items():
            if folder.read(name) != content:
                raise ReleaseError(f"Excel folder differs from the complete Copilot suite: {label}/{name}")
    metadata = json.loads(project.read(metadata_path))
    expected_files = [{**file_record(name, content),
                       "sourcePath": f"{source_folder}/{name.removeprefix('finance-suite/')}"}
                      for name, content in sorted(expected.items())]
    required_metadata = {
        "schemaVersion": 1, "kind": "excel-onedrive-folder-package", "version": version,
        "edition": "copilot", "skillName": "finance-suite", "folderName": "finance-suite",
        "path": source_path, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
        "sourceSuitePath": suite_path, "sourceSuiteSha256": hashlib.sha256(suite_payload).hexdigest(),
        "sourceExpandedPath": source_folder, "fileCount": len(expected),
        "installationMode": "extract-then-upload-folder", "registrationCount": 1,
        "nativeStatus": "not-validated", "files": expected_files,
    }
    if (not isinstance(metadata, dict)
            or any(metadata.get(key) != value for key, value in required_metadata.items())
            or any(type(metadata.get(key)) is not int
                   for key in ("schemaVersion", "bytes", "fileCount", "registrationCount"))):
        raise ReleaseError(f"Invalid Excel folder inventory: {label}")
    for record in expected_files:
        if record["sourcePath"] not in paths or project.read(record["sourcePath"]) != expected[record["path"]]:
            raise ReleaseError(f"Excel folder differs from expanded source: {label}/{record['path']}")


def existing_versions(folder: Path, *, locked: bool = False) -> list[dict]:
    if folder.is_symlink() or not folder.is_dir():
        raise ReleaseError("Releases must be a regular directory")
    manifests = []
    for path in sorted(folder.iterdir()):
        if locked and path.name == LOCK_NAME:
            continue
        if path.name in {"README.md", "latest.json"}:
            read_regular(path)
        elif path.name.startswith("v") and path.is_dir() and not path.is_symlink():
            manifests.append(verify_frozen(path))
        else:
            raise ReleaseError(f"Unexpected release entry; preserve and review it: {path.name}")
    return sorted(manifests, key=lambda m: version_key(m["version"]), reverse=True)


def index_files(manifests: list[dict]) -> dict[str, bytes]:
    ordered = sorted(manifests, key=lambda m: version_key(m["version"]), reverse=True)
    if not ordered:
        raise ReleaseError("No frozen releases to index")
    latest = ordered[0]
    index = {
        "schemaVersion": 1, "kind": "repository-hosted-release-index", "version": latest["version"],
        "path": f"releases/v{latest['version']}", "repository": latest["repository"],
        "downloads": [dict(record, path=f"releases/v{latest['version']}/{record['path']}")
                      for record in latest["files"] if record["path"].endswith(".zip")],
        "manifestPath": f"releases/v{latest['version']}/manifest.json",
        "checksumsPath": f"releases/v{latest['version']}/SHA256SUMS.txt",
    }
    lines = ["# Finance skills releases", "", f"Latest stable version: **{latest['version']}**.", "",
             "Download a versioned file from its release page. Extract transport bundles before importing "
             "individual native skill ZIPs. These files are hosted in the repository; no GitHub Release object is implied.",
             "", "| Version | Downloads and notes |", "| --- | --- |"]
    lines += [f"| {m['version']} | [v{m['version']}](v{m['version']}/README.md) |" for m in ordered]
    lines += ["", "[Machine-readable latest release](latest.json)", ""]
    return {"README.md": "\n".join(lines).encode("utf-8"), "latest.json": build.json_bytes(index)}


@contextmanager
def release_lock(folder: Path):
    lock = folder / LOCK_NAME
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ReleaseError("Another release operation holds .release.lock; preserve it until that operation finishes") from exc
    os.close(descriptor)
    try:
        yield
    finally:
        lock.unlink()


def write_indexes(folder: Path, outputs: dict[str, bytes]) -> list[str]:
    changed = []
    for name, data in outputs.items():
        target = folder / name
        if target.is_symlink():
            raise ReleaseError(f"Symlink in release index: {name}")
        if target.exists() and read_regular(target) == data:
            continue
        descriptor, temporary = tempfile.mkstemp(prefix=".index-", dir=folder)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        changed.append(name)
    return changed


def run(root: Path, *, check: bool = False, download_ref: str = "main") -> dict:
    manifest, expected, sources = prepare(root, download_ref)
    folder = root / "releases"
    target = folder / f"v{manifest['version']}"
    if folder.is_symlink():
        raise ReleaseError("Symlink at releases directory")
    if check:
        manifests = existing_versions(folder)
        if not target.is_dir():
            raise ReleaseError(f"Release v{manifest['version']} has not been frozen")
        if any(read_regular(target / name) != data for name, data in expected.items()):
            raise ReleaseError("Current source differs from the frozen version; use a new version")
        for name, data in index_files(manifests).items():
            if not (folder / name).is_file() or read_regular(folder / name) != data:
                raise ReleaseError(f"Release index drift: {name}")
        return {"version": manifest["version"], "status": "verified", "indexesChanged": []}
    folder.mkdir(exist_ok=True)
    with release_lock(folder):
        manifests = existing_versions(folder, locked=True)
        created = not target.exists()
        if not created and any(read_regular(target / name) != data for name, data in expected.items()):
            raise ReleaseError("Refusing to change an existing version; bump catalog.json and add new release notes")
        if created:
            temporary = Path(tempfile.mkdtemp(prefix=f".v{manifest['version']}-", dir=folder))
            try:
                for name, data in expected.items():
                    (temporary / name).write_bytes(data)
                if collect_project(root) != sources:
                    raise ReleaseError("Project changed while freezing the release; no version was published")
                if target.exists() or target.is_symlink():
                    raise ReleaseError("Version appeared during release; refusing to replace it")
                temporary.rename(target)
            finally:
                if temporary.exists():
                    shutil.rmtree(temporary)
            manifests.append(verify_frozen(target))
        changed = write_indexes(folder, index_files(manifests))
    return {"version": manifest["version"], "status": "created" if created else "unchanged", "indexesChanged": changed}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify current/frozen bytes and indexes without writing")
    parser.add_argument("--ref", default="main", help="GitHub branch/tag/commit used by raw download links (default: main)")
    args = parser.parse_args()
    try:
        result = run(ROOT, check=args.check, download_ref=args.ref)
        print(f"Release v{result['version']}: {result['status']}; repository-hosted downloads.")
        return 0
    except (ValueError, OSError, UnicodeError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(f"Release failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
