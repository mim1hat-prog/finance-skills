"""Copy a verified edition into a user-selected skills folder; never change the host account.

Use --apply after checking the default preview. Existing user edits are preserved.
For Excel/PowerPoint, select the exact folder the application's skills UI created.
Gemini Apps still requires upload/replacement through its own interface.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ".finance-skills-install.json"


def linked(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        # Windows name-surrogate reparse points include junctions. Ordinary
        # OneDrive placeholders do not have this tag bit and are not rejected.
        return bool(getattr(path.lstat(), "st_reparse_tag", 0) & 0x20000000)
    except FileNotFoundError:
        return False


def guard_destination(path: Path) -> None:
    if linked(path) or any(linked(p) for p in path.parents):
        raise ValueError("Destination must not traverse symbolic links or junctions")


def digest(path: Path) -> str:
    if linked(path) or not path.is_file():
        raise ValueError(f"Expected regular file: {path.name}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plan(root: Path, edition: str, destination: Path, names: list[str] | None):
    destination = destination.expanduser().absolute()
    guard_destination(destination)
    if destination.resolve().is_relative_to(root.resolve()):
        raise ValueError("Choose a work folder outside this repository")
    manifest = json.loads((root / "packages" / edition / "manifest.json").read_text(encoding="utf-8"))
    selected = manifest["skills"]
    allowed = {r["name"] for r in selected}
    if names:
        unknown = set(names) - allowed
        if unknown:
            raise ValueError(f"Unknown skills: {sorted(unknown)}")
        selected = [r for r in selected if r["name"] in names]
    receipt_path = destination / RECEIPT
    if linked(receipt_path):
        raise ValueError("Linked installation receipt refused")
    previous = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.is_file() else {"skills": {}}
    if previous.get("edition", edition) != edition:
        raise ValueError("Use separate destination folders for Copilot and Gemini editions")
    changes = []
    receipt = dict(previous.get("skills", {}))
    for entry in selected:
        name = entry["name"]
        if not name or "/" in name or "\\" in name or name in (".", ".."):
            raise ValueError("Invalid manifest name")
        source = root / "editions" / edition / name / "SKILL.md"
        if digest(source) != entry["skillSha256"]:
            raise ValueError(f"{name}: source does not match package manifest; rebuild or download clean source")
        if digest(root / "packages" / edition / f"{name}.zip") != entry["packageSha256"]:
            raise ValueError(f"{name}: package checksum mismatch")
        folder = destination / name
        target = folder / "SKILL.md"
        if linked(folder) or linked(target):
            raise ValueError(f"{name}: linked target refused")
        if folder.exists() and (not folder.is_dir() or {p.name for p in folder.iterdir()} != {"SKILL.md"}):
            raise ValueError(f"{name}: existing custom folder preserved")
        current = digest(target) if target.is_file() else None
        if current and current != entry["skillSha256"]:
            if current != previous.get("skills", {}).get(name, {}).get("sha256"):
                raise ValueError(f"{name}: local edits or unmanaged file preserved; choose a new destination")
        status = "unchanged" if current == entry["skillSha256"] else "update" if current else "add"
        changes.append({"name": name, "status": status, "source": source, "target": target,
                        "oldSha256": current, "sourceSha256": entry["skillSha256"]})
        receipt[name] = {"version": manifest["version"], "sha256": entry["skillSha256"], "reviewedOn": manifest["reviewedOn"]}
    return changes, {"schemaVersion": 1, "edition": edition, "skills": receipt}


def apply(changes: list[dict], receipt: dict, destination: Path):
    # Recheck every destination before the first write. Never delete unrelated skills.
    guard_destination(destination)
    if linked(destination / RECEIPT):
        raise ValueError("Linked installation receipt refused")
    for item in changes:
        target = item["target"]
        guard_destination(target.parent)
        if digest(item["source"]) != item["sourceSha256"]:
            raise ValueError(f"{item['name']}: source changed since preview")
        current = digest(target) if target.exists() else None
        if current != item["oldSha256"]:
            raise ValueError(f"{item['name']}: destination changed since preview")
    destination.mkdir(parents=True, exist_ok=True)
    for item in changes:
        if item["status"] == "unchanged":
            continue
        target = item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".finance-", delete=False) as out:
            temp = Path(out.name)
            out.write(item["source"].read_bytes())
        temp.replace(target)
    path = destination / RECEIPT
    with tempfile.NamedTemporaryFile(dir=destination, prefix=".finance-receipt-", mode="w", encoding="utf-8", delete=False) as out:
        temp = Path(out.name)
        json.dump(receipt, out, ensure_ascii=False, indent=2)
        out.write("\n")
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", choices=("copilot", "gemini"), required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--skills", nargs="+")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        destination = args.destination.expanduser().absolute()
        changes, receipt = plan(ROOT, args.edition, destination, args.skills)
        for row in changes:
            print(f"{row['status']:9} {row['name']}")
        if args.apply:
            apply(changes, receipt, destination)
            print("Verified edition copied. Refresh/upload in the target app; account activation was not performed.")
        else:
            print("Preview only. Add --apply to copy the listed files.")
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
