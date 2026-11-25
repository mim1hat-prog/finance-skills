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


def archive(data: bytes) -> bytes:
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        entry = zipfile.ZipInfo("SKILL.md", date_time=(1980, 1, 1, 0, 0, 0))
        entry.create_system = 3
        entry.external_attr = 0o100644 << 16
        entry.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(entry, data, compresslevel=9)
    return target.getvalue()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def generate(root: Path) -> dict[Path, bytes]:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if catalog.get("schemaVersion") != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", catalog["version"]):
        raise ValueError("Unsupported catalogue schema or version")
    names = [s["name"] for s in catalog["skills"]]
    if not names or len(names) != len(set(names)):
        raise ValueError("Empty catalogue or duplicate names")
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
        title, rest = body.split("\n", 1)
        for edition in ("copilot", "gemini"):
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
    for edition in ("copilot", "gemini"):
        selected = dict(manifest, skills=[e for e in entries if e["edition"] == edition])
        outputs[Path("packages") / edition / "manifest.json"] = json_bytes(selected)
    site_data = dict(catalog, counts={"skills": len(names)})
    outputs[Path("site/catalog-data.js")] = ("// Generated by scripts/build.py.\nwindow.FINANCE_SKILLS = " + json.dumps(site_data, ensure_ascii=False, indent=2).replace("<", "\\u003c") + ";\n").encode()
    index = ["# Skills", "", f"Version {catalog['version']} · reviewed {catalog['reviewedOn']}", "",
             "Choose one edition. Import each skill separately. The three suggested groups each fit the eight-skill Agent Builder limit; they are optional selections, not dependencies.", "",
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
        for directory in ("editions", "packages"):
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
