"""Generate a readable static catalogue and truthful discovery metadata, offline."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def profile(root: Path) -> dict:
    data = json.loads((root / "tools/discovery-profile.json").read_text(encoding="utf-8"))
    if (set(data) != {"schemaVersion", "title", "description", "topics"}
            or type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1):
        raise ValueError("Unsupported discovery profile")
    for key, maximum in (("title", 120), ("description", 200)):
        if not isinstance(data[key], str) or not 10 <= len(data[key]) <= maximum or "\n" in data[key]:
            raise ValueError(f"Invalid discovery {key}")
    topics = data["topics"]
    if (not isinstance(topics, list) or not 1 <= len(topics) <= 20
            or any(not isinstance(t, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", t) for t in topics)
            or len(topics) != len(set(topics))):
        raise ValueError("Use 1–20 unique lowercase GitHub topics")
    return data


def skill_rows(catalog: dict) -> str:
    """Real links and text remain useful before JavaScript enhances the catalogue."""
    rows = []
    for index, row in enumerate(catalog["skills"], 1):
        name = row["name"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("Invalid skill slug in discovery catalogue")
        title, summary, category, prompt = (html.escape(row[k]) for k in ("title", "summary", "category", "prompt"))
        rows.append(
            f'<article class="skill-row" aria-labelledby="skill-{name}">'
            f'<div class="skill-category"><span class="skill-index" aria-hidden="true">{index:02}</span>'
            f'<span>{category}</span></div><div class="skill-body"><h3 id="skill-{name}">{title}</h3>'
            f'<p>{summary}</p><details class="skill-prompt"><summary>Try this prompt</summary>'
            f'<div class="prompt-content"><p>{prompt}</p></div></details></div>'
            f'<div class="skill-actions"><a href="../packages/copilot/{name}.zip" download="{name}.zip" '
            f'aria-label="Download {title} for Copilot">Download ZIP</a>'
            f'<a href="../editions/copilot/{name}/SKILL.md" aria-label="Read {title} for Copilot">Read skill</a>'
            '</div></article>'
        )
    return "\n".join(rows)


def generate(root: Path, catalog: dict | None = None) -> dict[Path, bytes]:
    catalog = catalog or json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    config = profile(root)
    repo = catalog["repoUrl"].rstrip("/")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Discovery metadata requires the actual GitHub repository URL")
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", catalog["version"]):
        raise ValueError("Invalid discovery version")
    source_code = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": config["title"],
        "description": config["description"],
        "url": repo,
        "codeRepository": repo,
        "version": catalog["version"],
        "license": repo + "/blob/main/LICENSE",
        "programmingLanguage": ["Markdown", "Python"],
        "keywords": config["topics"],
    }
    encoded = json.dumps(source_code, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    title, description = html.escape(config["title"]), html.escape(config["description"], quote=True)
    head = "\n  ".join([
        f'<title>{title}</title>',
        f'<meta name="description" content="{description}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{description}">',
        '<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{description}">',
        f'<script type="application/ld+json">\n{encoded}\n  </script>',
    ])
    text = (root / "site/index.template.html").read_text(encoding="utf-8")
    replacements = {"PROJECT_METADATA": head, "SKILL_ROWS": skill_rows(catalog),
                    "SKILL_COUNT": str(len(catalog["skills"]))}
    for key, value in replacements.items():
        marker = "{{" + key + "}}"
        if text.count(marker) != 1:
            raise ValueError(f"Expected exactly one catalogue placeholder: {key}")
        text = text.replace(marker, value)
    if re.search(r"\{\{[A-Z_]+\}\}", text):
        raise ValueError("Unresolved catalogue placeholder")
    metadata = {
        "schemaVersion": 1,
        "kind": "prepared-discovery-metadata",
        "version": catalog["version"],
        "repository": repo,
        "title": config["title"],
        "description": config["description"],
        "topics": config["topics"],
        "settingsApplied": False,
        "publicSiteUrl": None,
        "scope": "Prepared repository settings and local static catalogue. No deployment, search indexing, rankings or adoption measurement is implied.",
        "structuredData": source_code,
    }
    return {
        Path("site/index.html"): text.encode("utf-8"),
        Path("docs/PROJECT-METADATA.json"): (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = generate(ROOT)
        for path, data in outputs.items():
            destination = ROOT / path
            if destination.is_symlink() or any(p.is_symlink() for p in destination.parents if p != ROOT.parent):
                raise ValueError(f"Linked discovery output refused: {path}")
            if args.check:
                if not destination.is_file() or destination.read_bytes() != data:
                    raise ValueError(f"Stale discovery output: {path}")
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
        print(f"{'Verified' if args.check else 'Generated'} {len(outputs)} discovery artifacts.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Discovery generation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
