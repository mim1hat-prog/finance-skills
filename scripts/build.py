"""Build portable finance skill editions using only the Python standard library."""
from __future__ import annotations

import argparse
from collections.abc import Mapping
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

import catalog_contracts

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE = re.compile(r"references/[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
EDITIONS = ("copilot", "gemini")
SUITE_NAME = "finance-suite"
EXCEL_PROFILE = Path("profiles/excel-agent-instructions.txt")
MARKDOWN_BUNDLE = Path("packages/markdown/finance-skills-markdown.zip")
BUNDLE_EDITIONS = {
    "finance-skills-copilot": ("copilot",),
    "finance-skills-gemini": ("gemini",),
    "finance-skills-all": EDITIONS,
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_skill(data: bytes, name: str, *,
                allowed_resources: Mapping[str, bytes] | None = None) -> tuple[str, str, str]:
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
    resources = {} if allowed_resources is None else allowed_resources
    if not isinstance(resources, Mapping):
        raise ValueError(f"{name}: resources must map exact relative paths to file bytes")
    for path, content in resources.items():
        if not isinstance(path, str) or not RESOURCE.fullmatch(path):
            raise ValueError(f"{name}: unsafe resource path: {path!r}")
        if not isinstance(content, bytes) or not content:
            raise ValueError(f"{name}: missing resource bytes: {path}")
    for link in re.findall(r'\]\(([^)]+)\)', body):
        if not link.startswith(("https://", "#")) and link not in resources:
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


def add_suite_packages(outputs: dict[Path, bytes], catalog: dict,
                       sources: dict[str, bytes], host_notes: dict[str, str],
                       shared: str) -> None:
    """Package one router plus exact canonical references, leaving individual skills intact."""
    names = [row["name"] for row in catalog["skills"]]
    if len(names) != len(set(names)) or set(sources) != set(names):
        raise ValueError("Suite sources must match the exact workflow catalogue")
    if "excel-agent-core" not in sources:
        raise ValueError("The finance suite requires canonical excel-agent-core defaults")
    bodies = {name: parse_skill(data, name)[2] for name, data in sources.items()}
    resources = {f"references/{name}.md": (bodies[name] + "\n").encode("utf-8")
                 for name in names}
    if len(resources) + 1 > 100:
        raise ValueError("The finance suite exceeds the portable 100-file ceiling")
    # Keep every default procedure paragraph; only replace its top-level title.
    core_defaults = bodies["excel-agent-core"].partition("\n")[2].strip()
    if not core_defaults:
        raise ValueError("The finance suite requires nonempty canonical default instructions")
    routes = []
    for row in catalog["skills"]:
        title, summary = row["title"], row["summary"]
        if any(character in title + summary for character in "\r\n"):
            raise ValueError("Suite routing titles and summaries must be single lines")
        # Escape labels/text so catalogue punctuation cannot create another link.
        escape = lambda value: re.sub(r'([\\`*_\[\]<>()])', r'\\\1', value)
        routes.append(f"- [{escape(title)}](references/{row['name']}.md): {escape(summary)}")
    index = "## Workflow index\n\n" + "\n".join(routes)
    description = (
        "Apply finance workflows for Excel, workforce planning, forecast variance, reconciliations, "
        "Power Query, Power BI, reporting and source-backed research. Use for finance tasks that need "
        "enterprise evidence, preserved business logic and independently checked results; select the "
        "relevant bundled workflow references."
    )
    front = f"---\nname: {SUITE_NAME}\ndescription: {json.dumps(description)}\n---\n\n"
    routing = (
        "## Select and read the relevant workflow\n\n"
        f"This is one registered skill with {len(names)} bundled finance workflows, not "
        f"{len(names)} separately registered skills. It does not change host limits or grant tools, "
        "permissions or data access.\n\n"
        "Understand the requested objective, then use the index to select only the relevant workflow "
        "or workflows. Read each selected reference completely before applying its procedure. "
        "The index is navigation, not a substitute for those instructions. Apply the host guidance, "
        "shared controls and default operating instructions below throughout the task.\n\n"
        "If a required reference is unavailable or unreadable, identify the exact missing resource "
        "and use an available supported route to retrieve it. Do not invent its procedure or claim "
        "that it was read or executed. Continue only work supported by the instructions and evidence "
        "actually available, and state any material remaining limitation.\n\n"
        "Use approved internal figures for business results, internal evidence for workflow status "
        "and public benchmarks only as separately cited context. Keep routine checks internal and "
        "preserve existing business logic; do not add unsolicited audit tables, audit text or worksheets."
    )
    records = []
    for edition in EDITIONS:
        adapter = host_notes.get(edition)
        if not isinstance(adapter, str) or not adapter.strip().startswith("## "):
            raise ValueError(f"Missing valid {edition} host guidance for finance suite")
        parts = ["# Finance suite", routing, index, adapter.strip()]
        if shared:
            parts.append(shared)
        parts += ["## Default operating instructions\n\n" + core_defaults,
                  "## Suite record\n\n"
                  f"Finance skills {catalog['version']}; {edition} edition; source review "
                  f"{catalog['reviewedOn']}. This is the package's source-review date, not the "
                  "freshness of business data. Package validation does not establish successful "
                  "native import, reference retrieval or task execution in the work account."]
        rendered = (front + "\n\n".join(parts) + "\n").encode("utf-8")
        parse_skill(rendered, SUITE_NAME, allowed_resources=resources)
        members = {"SKILL.md": rendered, **resources}
        folder = Path("editions") / f"{edition}-suite" / SUITE_NAME
        for name, content in members.items():
            outputs[folder / name] = content
        path = Path("packages/suites") / f"finance-suite-{edition}.zip"
        packed = archive_files(members)
        outputs[path] = packed
        records.append({
            "kind": "single-registration-native-suite", "name": SUITE_NAME,
            "edition": edition,
            "host": "Microsoft 365 Copilot" if edition == "copilot" else "Gemini",
            "sourceVersion": catalog["version"], "reviewedOn": catalog["reviewedOn"],
            "registrationCount": 1, "workflowCount": len(names),
            "nativeStatus": "not-validated", "path": path.as_posix(),
            "expandedPath": folder.as_posix(), "fileCount": len(members),
            "packageBytes": len(packed), "packageSha256": sha(packed),
            "skillCharacters": len(rendered.decode("utf-8")),
            "skillLines": len(rendered.decode("utf-8").splitlines()),
            "sharedControlsSha256": sha(shared.encode("utf-8")),
            "hostGuidanceSha256": sha(adapter.strip().encode("utf-8")),
            "files": [{"path": name, "bytes": len(content), "sha256": sha(content)}
                      for name, content in sorted(members.items())],
            "sources": [{"name": name, "path": f"skills/{name}/SKILL.md",
                         "sha256": sha(sources[name])} for name in names],
        })
    outputs[Path("packages/suites/manifest.json")] = json_bytes({
        "schemaVersion": 1, "kind": "single-registration-suite-index",
        "version": catalog["version"], "name": SUITE_NAME,
        "workflowCount": len(names), "registrationCountPerPackage": 1,
        "import": "Upload one complete edition ZIP with its root SKILL.md and references together.",
        "packages": records,
    })


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
        "This outer ZIP is a transport download, not one installable skill. Extract it first; "
        "upload an individual package from packages/copilot/ or packages/gemini/.",
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


def add_markdown_bundle(outputs: dict[Path, bytes], catalog: dict) -> None:
    """Publish complete edition bodies for copying, with metadata outside the ZIP."""
    names = [row["name"] for row in catalog["skills"]]
    selected = {"EXCEL-AGENT-INSTRUCTIONS.md": outputs[EXCEL_PROFILE]}
    for edition in EDITIONS:
        for name in names:
            source = outputs[Path("editions") / edition / name / "SKILL.md"]
            body = parse_skill(source, name)[2]
            selected[f"{edition}/{name}.md"] = (body + "\n").encode("utf-8")
    guide = [
        "# Start here: copy and paste", "",
        f"Finance skills {catalog['version']} · Markdown-only edition", "",
        f"This ZIP contains {len(names)} Copilot skill files, {len(names)} Gemini skill files, "
        "Excel agent instructions and this guide. Every file is Markdown (.md).", "",
        "## Copy and paste only", "",
        "These files intentionally omit YAML name and description metadata. Do not upload this ZIP "
        "or its individual Markdown files through Add/Upload skill. Renaming a file to SKILL.md "
        "does not add the missing metadata.", "",
        f"For native Copilot Skills, download an [individual Copilot ZIP]({catalog['repoUrl'].rstrip('/')}/tree/main/packages/copilot), "
        "then upload that package. It contains the complete SKILL.md with its required header. "
        f"[Copilot import troubleshooting]({catalog['repoUrl'].rstrip('/')}/blob/main/docs/COPILOT.md#troubleshoot-invalid-skill-information)", "",
        "## Use a skill", "",
        "1. In Windows File Explorer, choose Extract All for this ZIP.",
        "2. Choose the copilot or gemini folder, then open the skill you need in VS Code or Notepad.",
        "3. Press Ctrl+A, then Ctrl+C to copy the entire file. YAML headers have already been removed.",
        "4. Paste into your available agent or Gem Instructions field, or into an approved conversation. "
        "Save the instructions if the host provides that option, then supply your task and relevant files.", "",
        "Use one relevant workflow at a time. These are plain instructions for copying; "
        "the ZIP is not a native skill import. Pasting does not enable unavailable tools or increase host limits.", "",
        "## Your Excel agent defaults", "",
        "Copy all of EXCEL-AGENT-INSTRUCTIONS.md into the Instructions field you already use for your Excel agent. "
        "It is the shared profile; the copilot and gemini folders contain the complete edition-specific workflows.", "",
        "## Updates", "",
        "Downloaded and pasted copies do not update automatically. Download a newer version and replace "
        "the relevant instructions, preserving any approved company additions in your private account.", "",
        f"[Repository and downloads]({catalog['repoUrl'].rstrip('/')})", "",
    ]
    selected["START-HERE.md"] = "\n".join(guide).encode("utf-8")
    packed = archive_files(selected)
    outputs[MARKDOWN_BUNDLE] = packed
    outputs[Path("packages/markdown/manifest.json")] = json_bytes({
        "schemaVersion": 1,
        "kind": "markdown-copy-paste-bundle",
        "version": catalog["version"],
        "editions": list(EDITIONS),
        "skillCount": len(names),
        "fileCount": len(selected),
        "path": MARKDOWN_BUNDLE.as_posix(),
        "sha256": sha(packed),
        "bytes": len(packed),
        "files": [
            {"path": name, "sha256": sha(data), "bytes": len(data)}
            for name, data in sorted(selected.items())
        ],
    })


def generate(root: Path) -> dict[Path, bytes]:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if catalog.get("schemaVersion") != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", catalog["version"]):
        raise ValueError("Unsupported catalogue schema or version")
    markdown_version = catalog.get("markdownBundleVersion")
    if markdown_version is not None and (type(markdown_version) is not int or markdown_version != 1):
        raise ValueError("Unsupported Markdown bundle version")
    suite_version = catalog.get("suitePackageVersion")
    if "suitePackageVersion" in catalog:
        if type(suite_version) is not int or suite_version != 1:
            raise ValueError("Unsupported suite package version")
        if type(markdown_version) is not int or markdown_version != 1:
            raise ValueError("Suite packages require Markdown bundle version 1")
    presentation_version = catalog.get("projectPresentationVersion")
    if presentation_version is not None and (type(presentation_version) is not int or presentation_version != 1):
        raise ValueError("Unsupported project presentation version")
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
    shared = ""
    if catalog.get("workflowContractsVersion") is not None:
        if catalog["workflowContractsVersion"] != 1:
            raise ValueError("Unsupported workflow contract version")
        shared_path = root / "adapters/workflow-controls.md"
        if shared_path.is_symlink() or not shared_path.is_file():
            raise ValueError("Missing regular shared workflow-controls procedure")
        shared = shared_path.read_text(encoding="utf-8").strip()
        if not shared.startswith("## "):
            raise ValueError("Shared workflow controls need a Markdown section")
        outputs.update(catalog_contracts.generate(root, catalog))
        released = catalog.get("releasedOn")
        if not isinstance(released, str) or date.fromisoformat(released).isoformat() != released:
            raise ValueError("releasedOn must be the explicit ISO release date")
        citation = [
            'cff-version: "1.2.0"',
            'message: "If you use this software, cite this version and repository."',
            'type: software',
            'title: "Finance skills"',
            'authors:',
            '  - name: "Finance Skills contributors"',
            f'version: {json.dumps(catalog["version"])}',
            f'date-released: {json.dumps(released)}',
            f'repository-code: {json.dumps(catalog["repoUrl"])}',
            'license: MIT',
            'abstract: "Portable finance workflows for Microsoft 365 Copilot and Gemini, with local validation tools and a public benchmark dataset."',
            'keywords:', '  - finance', '  - agent-skills', '  - reproducibility', '',
        ]
        outputs[Path("CITATION.cff")] = "\n".join(citation).encode("utf-8")
    entries = []
    canonical_sources: dict[str, bytes] = {}
    host_notes: dict[str, str] = {}
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
        canonical_sources[name] = source
        if name == "excel-agent-core":
            outputs[EXCEL_PROFILE] = (body + "\n").encode("utf-8")
        title, rest = body.split("\n", 1)
        for edition in EDITIONS:
            adapter = (root / "adapters" / f"{edition}.md").read_text(encoding="utf-8").strip()
            host_notes[edition] = adapter
            if shared:
                adapter += "\n\n" + shared
            rendered_body = f"{title}\n\n{adapter}\n\n{rest.strip()}\n\n## Edition record\n\nFinance skills {catalog['version']}; {edition} edition; source review {catalog['reviewedOn']}. This date records the package review, not the freshness of a user's business data.\n"
            rendered = (front + "\n" + rendered_body).encode("utf-8")
            parse_skill(rendered, name)
            packed = archive(rendered)
            outputs[Path("editions") / edition / name / "SKILL.md"] = rendered
            outputs[Path("packages") / edition / f"{name}.zip"] = packed
            entries.append({"name": name, "edition": edition, "group": row["group"],
                            "sourceSha256": sha(source), "sharedControlsSha256": sha(shared.encode()), "skillSha256": sha(rendered),
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
    if markdown_version == 1:
        add_markdown_bundle(outputs, catalog)
    if suite_version == 1:
        add_suite_packages(outputs, catalog, canonical_sources, host_notes, shared)
    if presentation_version == 1:
        import project_discovery
        import project_metrics
        outputs.update(project_discovery.generate(root, catalog))
        outputs.update(project_metrics.generate(root, catalog))
    site_data = dict(catalog, counts={"skills": len(names)})
    outputs[Path("site/catalog-data.js")] = ("// Generated by scripts/build.py.\nwindow.FINANCE_SKILLS = " + json.dumps(site_data, ensure_ascii=False, indent=2).replace("<", "\\u003c") + ";\n").encode()
    choice = ("Choose one edition. Import its finance suite once for bundled workflows, or import selected individual skills. "
              if suite_version == 1 else "Choose one edition. Import each skill separately. ")
    choice += "Suggested Agent Builder groups each contain at most eight skills; they are optional selections, not dependencies."
    index = ["# Skills", "", f"{len(names)} skills · version {catalog['version']} · reviewed {catalog['reviewedOn']}", "",
             choice, "",
             "## Download a complete edition", "",
             "[Copilot bundle](packages/bundles/finance-skills-copilot.zip?raw=1) · "
             "[Gemini bundle](packages/bundles/finance-skills-gemini.zip?raw=1) · "
             "[Both editions](packages/bundles/finance-skills-all.zip?raw=1)", "",
             "Extract a bundle first, then use its individual skill ZIPs or follow its folder-copy guide. "
             "The bundle does not provide a bulk native import or automatic activation.", "",
             "[Excel agent instructions](profiles/excel-agent-instructions.txt) · "
             "[Bundle checksums](packages/bundles/manifest.json)", "",
             "[Tool inventory](TOOLS.md) · [Workflow contracts](docs/SKILL-CONTRACTS.md) · [Research registry](research/README.md)", ""]
    if suite_version == 1:
        index += ["## One native import for the finance suite", "",
                  "[Copilot suite ZIP](packages/suites/finance-suite-copilot.zip?raw=1) · "
                  "[Gemini suite ZIP](packages/suites/finance-suite-gemini.zip?raw=1) · "
                  "[Member hashes and provenance](packages/suites/manifest.json)", "",
                  f"Each suite is one native skill named `finance-suite`, with a root `SKILL.md` and {len(names)} "
                  "complete workflow references. Upload the selected suite ZIP unchanged. The host must be able "
                  "to read its bundled references; verify this in the target account. This registers one skill, "
                  "not every workflow separately, and does not increase host limits. Individual packages remain available.", ""]
    if markdown_version == 1:
        index += ["## Copy and paste", "",
                  "[Download Markdown-only ZIP](packages/markdown/finance-skills-markdown.zip?raw=1) · "
                  "[File inventory and checksum](packages/markdown/manifest.json)", "",
                  f"{2 * len(names) + 2} Markdown files: both editions, Excel agent instructions and a start guide. "
                  "Extract, open the relevant file, copy its complete contents and paste into an available "
                  "Instructions field or approved conversation. YAML headers are removed; "
                  "the full host instructions and shared controls are retained.", ""]
    if presentation_version == 1:
        index += ["[Worked example](examples/QUICKSTART.md) · [Coverage and limitations](metrics/README.md) · "
                  "[Help](SUPPORT.md) · [Contribute](CONTRIBUTING.md)", ""]
    index += ["## Individual skills", "",
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
