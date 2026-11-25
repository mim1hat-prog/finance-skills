"""Build portable finance skill editions using only the Python standard library."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EDITIONS = ("copilot", "gemini")
EXCEL_PROFILE = Path("profiles/excel-agent-instructions.txt")
BUNDLE_EDITIONS = {
    "finance-skills-copilot": ("copilot",),
    "finance-skills-gemini": ("gemini",),
    "finance-skills-all": EDITIONS,
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_skill(data: bytes, name: str) -> tuple[str, str, str]:
    text = data.decode("utf-8")
    if text.startswith("\ufeff") or "\r" in text:
        raise ValueError(f"{name}: use UTF-8 without BOM and LF line endings")
    match = re.fullmatch(r'---\nname: ([^\n]+)\ndescription: ("[^\n]+")\n---\n(.*)', text, re.S)
    if not match or match[1] != name or len(name) > 64 or not NAME.fullmatch(name):
        raise ValueError(f"{name}: invalid name or frontmatter")
    description = json.loads(match[2])
    body = match[3].strip()
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        raise ValueError(f"{name}: invalid description")
    if not body.startswith("# ") or len(body.splitlines()) >= 500:
        raise ValueError(f"{name}: body needs a heading and fewer than 500 lines")
    if len(text) >= 20000:
        raise ValueError(f"{name}: exceeds portable 20,000-character ceiling")
    for link in re.findall(r'\]\(([^)]+)\)', body):
        if not link.startswith(("https://", "#")):
            raise ValueError(f"{name}: unresolved local resource: {link}")
    front = text[: text.index("\n---\n", 4) + 5]
    return front, description, body


def archive_files(files: dict[str, bytes]) -> bytes:
    """Return a stable ZIP whose entries and metadata do not depend on the host."""
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for name in sorted(files):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(entry, files[name], compresslevel=9)
    return target.getvalue()


def archive(data: bytes) -> bytes:
    """The individual native-import contract remains one root SKILL.md."""
    return archive_files({"SKILL.md": data})


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def bundle_start_here(catalog: dict, editions: tuple[str, ...]) -> bytes:
    if not isinstance(catalog.get("repoUrl"), str):
        raise ValueError("Catalogue repoUrl must be an HTTPS GitHub repository URL")
    repo_url = catalog["repoUrl"].rstrip("/")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo_url):
        raise ValueError("Catalogue repoUrl must be an HTTPS GitHub repository URL")
    guide_root = repo_url + "/blob/main/docs"
    count = len(catalog["skills"])
    selected = " and ".join("Microsoft 365 Copilot" if e == "copilot" else "Gemini" for e in editions)
    lines = [
        "# Start here",
        "",
        f"Finance skills {catalog['version']} · reviewed {catalog['reviewedOn']}",
        "",
        f"This download contains {count} finance skills for {selected}, with "
        f"{count * len(editions)} individual native-import packages.",
        "",
        "## Extract and choose",
        "",
        "1. In Windows File Explorer, extract this outer ZIP to a folder.",
        "2. Read the selected assistant's guide below.",
        "3. Import the individual skill ZIPs you need. Each contains one root SKILL.md.",
        "",
    ]
    if "copilot" in editions:
        lines += [
            f"**Copilot:** [setup guide]({guide_root}/COPILOT.md). "
            "Select individual files under packages/copilot/ for a supported Chat or Agent Builder import. "
            "For an Excel or PowerPoint folder workflow, copy selected matching-name folders from "
            "editions/copilot/ into the location opened by the app, then follow its sync and Refresh steps.",
            "",
        ]
    if "gemini" in editions:
        lines += [
            f"**Gemini:** [setup guide]({guide_root}/GEMINI.md). "
            "Import individual files under packages/gemini/ into native Skills. "
            "If your account uses the Gem fallback, the corresponding editions/gemini-gems/ text "
            "goes in Instructions; follow the guide for that account.",
            "",
        ]
    lines += [
        "## Excel agent instructions",
        "",
        "profiles/excel-agent-instructions.txt is the plain-text body of the canonical "
        "excel-agent-core skill. Copy it into an available Excel agent's instruction field "
        "when that setup accepts text, or use the individual skill package through a supported import.",
        "",
        "## Verify and update",
        "",
        "manifest.json lists the exact path, size and SHA-256 of every other file in this bundle. "
        "The manifests under packages/ describe the individual native skill packages.",
        "",
        "This outer ZIP is a download-and-transport bundle. Native imports still happen one skill "
        "at a time; extracting or copying files does not prove automatic activation. "
        "Use the host's replacement or Refresh flow for later updates and verify a representative task.",
        "",
        f"[Windows guide]({guide_root}/WINDOWS.md) · [Update guide]({guide_root}/UPDATES.md)",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def add_transport_bundles(outputs: dict[Path, bytes], catalog: dict) -> None:
    """Select only explicit native outputs; a transport ZIP never contains another bundle."""
    records = []
    names = [row["name"] for row in catalog["skills"]]
    for bundle_name, editions in BUNDLE_EDITIONS.items():
        selected = {
            EXCEL_PROFILE.as_posix(): outputs[EXCEL_PROFILE],
            "START-HERE.md": bundle_start_here(catalog, editions),
        }
        for edition in editions:
            paths = [Path("packages") / edition / "manifest.json"]
            for name in names:
                paths += [
                    Path("editions") / edition / name / "SKILL.md",
                    Path("packages") / edition / f"{name}.zip",
                ]
                if edition == "gemini":
                    paths.append(Path("editions/gemini-gems") / f"{name}.txt")
            selected.update({path.as_posix(): outputs[path] for path in paths})
        bundle_manifest = {
            "schemaVersion": 1,
            "kind": "transport-bundle",
            "version": catalog["version"],
            "reviewedOn": catalog["reviewedOn"],
            "editions": list(editions),
            "skillCount": len(names),
            "packageCount": len(names) * len(editions),
            "import": "Extract first, then import individual root-SKILL.md packages or follow the host folder guide.",
            "files": [
                {"path": path, "sha256": sha(data), "bytes": len(data)}
                for path, data in sorted(selected.items())
            ],
        }
        selected["manifest.json"] = json_bytes(bundle_manifest)
        packed = archive_files(selected)
        path = Path("packages/bundles") / f"{bundle_name}.zip"
        outputs[path] = packed
        records.append({
            "name": bundle_name,
            "path": path.as_posix(),
            "editions": list(editions),
            "skillCount": len(names),
            "packageCount": len(names) * len(editions),
            "fileCount": len(selected),
            "sha256": sha(packed),
            "bytes": len(packed),
        })
    outputs[Path("packages/bundles/manifest.json")] = json_bytes({
        "schemaVersion": 1,
        "kind": "transport-bundle-index",
        "version": catalog["version"],
        "reviewedOn": catalog["reviewedOn"],
        "import": "Extract the outer archive; native imports remain individual skills.",
        "bundles": records,
    })


def generate(root: Path) -> dict[Path, bytes]:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if catalog.get("schemaVersion") != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", catalog["version"]):
        raise ValueError("Unsupported catalogue schema or version")
    names = [s["name"] for s in catalog["skills"]]
    if not names or len(names) != len(set(names)):
        raise ValueError("Empty catalogue or duplicate names")
    if "excel-agent-core" not in names:
        raise ValueError("The catalogue must include excel-agent-core for the Excel instructions profile")
    found = {p.name for p in (root / "skills").iterdir()}
    if found != set(names):
        raise ValueError(f"Catalogue/source mismatch: {sorted(found ^ set(names))}")
    groups: dict[str, int] = {}
    for row in catalog["skills"]:
        for key in ("name", "title", "summary", "category", "group", "prompt"):
            if not isinstance(row.get(key), str) or not row[key]:
                raise ValueError(f"Missing catalogue field {key}")
        groups[row["group"]] = groups.get(row["group"], 0) + 1
    if any(n > 8 for n in groups.values()):
        raise ValueError("Each suggested Agent Builder group must contain at most eight skills")
    outputs: dict[Path, bytes] = {}
    entries = []
    for row in catalog["skills"]:
        name = row["name"]
        folder = root / "skills" / name
        if folder.is_symlink() or not folder.is_dir() or {p.name for p in folder.iterdir()} != {"SKILL.md"}:
            raise ValueError(f"{name}: source must contain only SKILL.md")
        source_path = folder / "SKILL.md"
        if source_path.is_symlink() or not source_path.is_file():
            raise ValueError(f"{name}: source must be a regular file")
        source = source_path.read_bytes()
        front, _, body = parse_skill(source, name)
        if name == "excel-agent-core":
            outputs[EXCEL_PROFILE] = (body + "\n").encode("utf-8")
        title, rest = body.split("\n", 1)
        for edition in EDITIONS:
            adapter = (root / "adapters" / f"{edition}.md").read_text(encoding="utf-8").strip()
            rendered_body = f"{title}\n\n{adapter}\n\n{rest.strip()}\n\n## Edition record\n\nFinance skills {catalog['version']}; {edition} edition; source review {catalog['reviewedOn']}. This date records the package review, not the freshness of a user's business data.\n"
            rendered = (front + "\n" + rendered_body).encode("utf-8")
            parse_skill(rendered, name)
            packed = archive(rendered)
            outputs[Path("editions") / edition / name / "SKILL.md"] = rendered
            outputs[Path("packages") / edition / f"{name}.zip"] = packed
            entries.append({"name": name, "edition": edition, "group": row["group"],
                            "sourceSha256": sha(source), "skillSha256": sha(rendered),
                            "packageSha256": sha(packed), "skillBytes": len(rendered),
                            "packageBytes": len(packed), "path": f"packages/{edition}/{name}.zip"})
            if edition == "gemini":
                outputs[Path("editions/gemini-gems") / f"{name}.txt"] = rendered_body.encode("utf-8")
    manifest = {"schemaVersion": 1, "version": catalog["version"], "reviewedOn": catalog["reviewedOn"],
                "profile": "standalone-text", "import": "one ZIP per skill; root SKILL.md", "skills": entries}
    outputs[Path("packages/manifest.json")] = json_bytes(manifest)
    for edition in EDITIONS:
        selected = dict(manifest, skills=[e for e in entries if e["edition"] == edition])
        outputs[Path("packages") / edition / "manifest.json"] = json_bytes(selected)
    add_transport_bundles(outputs, catalog)
    site_data = dict(catalog, counts={"skills": len(names)})
    outputs[Path("site/catalog-data.js")] = ("// Generated by scripts/build.py.\nwindow.FINANCE_SKILLS = " + json.dumps(site_data, ensure_ascii=False, indent=2).replace("<", "\\u003c") + ";\n").encode()
    index = ["# Skills", "", f"{len(names)} skills · version {catalog['version']} · reviewed {catalog['reviewedOn']}", "",
             "Choose one edition. Import each skill separately. Suggested Agent Builder groups each contain at most eight skills; they are optional selections, not dependencies.", "",
             "## Download a complete edition", "",
             "[Copilot bundle](packages/bundles/finance-skills-copilot.zip?raw=1) · "
             "[Gemini bundle](packages/bundles/finance-skills-gemini.zip?raw=1) · "
             "[Both editions](packages/bundles/finance-skills-all.zip?raw=1)", "",
             "Extract a bundle first, then use its individual skill ZIPs or follow its folder-copy guide. "
             "The bundle does not provide a bulk native import or automatic activation.", "",
             "[Excel agent instructions](profiles/excel-agent-instructions.txt) · "
             "[Bundle checksums](packages/bundles/manifest.json)", "",
             "## Individual skills", "",
             "| Skill | Purpose | Copilot | Gemini |", "| --- | --- | --- | --- |"]
    for row in catalog["skills"]:
        n = row["name"]
        index.append(f"| [{row['title']}](skills/{n}/SKILL.md) | {row['summary']} | [ZIP](packages/copilot/{n}.zip) | [ZIP](packages/gemini/{n}.zip) |")
    index += ["", "## Suggested Agent Builder groups", ""]
    for group in groups:
        index += [f"### {group.title()}", "", ", ".join(f"`{r['name']}`" for r in catalog["skills"] if r["group"] == group) + ".", ""]
    outputs[Path("SKILLS.md")] = ("\n".join(index) + "\n").encode()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify checked-in generated bytes without writing")
    args = parser.parse_args()
    try:
        outputs = generate(ROOT)
        unexpected = []
        for directory in ("editions", "packages", "profiles"):
            for p in (ROOT / directory).rglob("*"):
                if p.is_symlink() or (p.is_file() and p.relative_to(ROOT) not in outputs):
                    unexpected.append(str(p.relative_to(ROOT)))
        if unexpected:
            raise ValueError(f"Unexpected generated files; preserve/review before removal: {unexpected}")
        stale = []
        for relative, data in outputs.items():
            path = ROOT / relative
            if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != ROOT.parent):
                raise ValueError(f"Linked output path refused: {relative}")
            if args.check:
                if not path.is_file() or path.read_bytes() != data:
                    stale.append(str(relative))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        if stale:
            raise ValueError("Stale generated files: " + ", ".join(stale))
        print(f"{'Verified' if args.check else 'Built'} {len(outputs)} deterministic files; both editions match canonical skills.")
        return 0
    except (ValueError, OSError, UnicodeError, KeyError, json.JSONDecodeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
