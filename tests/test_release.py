"""Release snapshots are immutable and independently verifiable download artifacts."""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build
import release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.catalog = {
            "schemaVersion": 1, "version": "1.1.0", "reviewedOn": "2026-11-25",
            "repoUrl": "https://github.com/example/finance-skills",
            "skills": [{"name": name, "title": name.title(), "summary": "A useful finance task.",
                        "category": "Core", "group": "core", "prompt": "Do the task."}
                       for name in ("excel-agent-core", "sample-task")],
        }
        for name in ("README.md", "AGENTS.md", "LICENSE", "docs/RELEASES.md", ".gitattributes"):
            self.write(name, b"Reviewed public project content.\n")
        for script in ("build.py", "release.py", "catalog_contracts.py"):
            self.write("scripts/" + script, (ROOT / "scripts" / script).read_bytes())
        self.write("tests/test_fixture.py", b"# Synthetic regression fixture\n")
        self.write("examples/sample.csv", b"period,value\n2026-01,10\n")
        self.write("assets/mark.svg", b'<svg xmlns="http://www.w3.org/2000/svg"/>\n')
        self.write("requirements-xlsx.txt", b"openpyxl==3.1.5\n")
        for name in ("excel-agent-core", "sample-task"):
            self.write(f"skills/{name}/SKILL.md", (
                f'---\nname: {name}\ndescription: "Use for a finance task"\n---\n\n'
                f"# {name.title()}\n\nApply the reviewed procedure.\n"
            ).encode())
        for edition in ("copilot", "gemini"):
            self.write(f"adapters/{edition}.md", b"## Host\n\nUse available tools.\n")
        self.set_version("1.1.0")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, data):
        destination = self.root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    def set_version(self, version):
        self.catalog["version"] = version
        self.write("catalog.json", build.json_bytes(self.catalog))
        self.write(f"release-notes/v{version}.md", (
            f"# Finance skills v{version}\n\n## Changes\n\nReviewed changes for {version}.\n"
        ).encode())
        self.rebuild()

    def rebuild(self):
        for path, data in build.generate(self.root).items():
            self.write(path, data)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}

    def test_freeze_noop_and_check_do_not_rewrite_identical_files(self):
        self.assertEqual(release.run(self.root)["status"], "created")
        before = self.snapshot()
        self.assertEqual(release.run(self.root)["status"], "unchanged")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(release.run(self.root, check=True)["status"], "verified")
        self.assertEqual(self.snapshot(), before)
        checked = subprocess.run(
            [sys.executable, "-E", str(self.root / "scripts/release.py"), "--check"],
            cwd=self.root, capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "scripts/__pycache__").exists())
        self.assertFalse((self.root / "releases/.release.lock").exists())

    def test_zip_content_checksums_metadata_and_download_urls(self):
        release.run(self.root)
        folder = self.root / "releases/v1.1.0"
        manifest = json.loads((folder / "manifest.json").read_bytes())
        for row in manifest["files"]:
            content = (folder / row["path"]).read_bytes()
            self.assertEqual(row["sha256"], hashlib.sha256(content).hexdigest())
            self.assertEqual(row["bytes"], len(content))
            self.assertEqual(row["downloadUrl"], "https://raw.githubusercontent.com/example/finance-skills/main/releases/v1.1.0/" + row["path"])
        for variant in ("copilot", "gemini", "all"):
            self.assertEqual((folder / f"finance-skills-v1.1.0-{variant}.zip").read_bytes(),
                             (self.root / f"packages/bundles/finance-skills-{variant}.zip").read_bytes())
        with zipfile.ZipFile(folder / "finance-skills-v1.1.0-full.zip") as archive:
            expected = release.collect_project(self.root)
            self.assertEqual(archive.namelist(), sorted(expected))
            for info in archive.infolist():
                self.assertEqual(archive.read(info.filename), expected[info.filename])
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr >> 16, 0o100644)
            for name in ("scripts/build.py", "scripts/release.py", "docs/RELEASES.md",
                         "release-notes/v1.1.0.md", "profiles/excel-agent-instructions.txt",
                         "site/catalog-data.js", "SKILLS.md", "tests/test_fixture.py", "requirements-xlsx.txt"):
                self.assertIn(name, archive.namelist())
            self.assertFalse(any(n.startswith("releases/") for n in archive.namelist()))
        expected_sums = release.sums({p.name: p.read_bytes() for p in folder.iterdir() if p.name != "SHA256SUMS.txt"})
        self.assertEqual((folder / "SHA256SUMS.txt").read_bytes(), expected_sums)
        readme = (folder / "README.md").read_text()
        self.assertIn("Reviewed changes for 1.1.0.", readme)
        self.assertEqual(sum(line.startswith("# ") for line in readme.splitlines()), 1)
        self.assertIn("## Release notes\n\n### Changes", readme)
        notes = (self.root / "release-notes/v1.1.0.md").read_bytes()
        self.assertTrue(notes.startswith(b"# Finance skills v1.1.0\n\n## Changes"))
        self.assertEqual(manifest["notes"]["sha256"], hashlib.sha256(notes).hexdigest())
        self.assertEqual(release.embedded_notes("## Added\n```text\n## Literal\n```\n## Fixed", "1.1.0"),
                         "### Added\n```text\n## Literal\n```\n### Fixed")

    def test_full_archive_excludes_private_runtime_unlisted_roots_and_unknown_types(self):
        forbidden = [".git/config", ".local/key.json", ".env", "private/plan.csv", "work-data/actual.csv",
                     "outputs/report.md", "upstream-sources/vendor/README.md", "node_modules/package/index.js",
                     "scripts/__pycache__/release.pyc", "docs/private/internal.md", "examples/.env",
                     "site/runtime/trace.json", "examples/raw.xlsx", "secret.txt"]
        baseline = release.prepare(self.root)[1]
        for name in forbidden:
            self.write(name, b"Must stay out of public release.\n")
        self.assertEqual(release.prepare(self.root)[1], baseline)

    def test_markdown_release_preserves_legacy_snapshots_and_lists_five_archives(self):
        for version in ("1.1.0", "1.2.0"):
            self.set_version(version)
            release.run(self.root)
            folder = self.root / f"releases/v{version}"
            self.assertEqual(release.verify_frozen(folder)["schemaVersion"], 1)
            self.assertEqual({p.name for p in folder.iterdir()}, {
                f"finance-skills-v{version}-{variant}.zip" for variant in ("copilot", "gemini", "all", "full")
            } | {"README.md", "manifest.json", "SHA256SUMS.txt"})
        old = {name: value for name, value in self.snapshot().items()
               if name.startswith(("releases/v1.1.0/", "releases/v1.2.0/"))}
        self.catalog["markdownBundleVersion"] = 1
        self.set_version("1.3.0")
        self.assertEqual(release.run(self.root)["status"], "created")
        folder = self.root / "releases/v1.3.0"
        manifest = release.verify_frozen(folder)
        archives = {f"finance-skills-v1.3.0-{variant}.zip"
                    for variant in ("copilot", "gemini", "all", "markdown", "full")}
        self.assertEqual(manifest["schemaVersion"], 2)
        self.assertEqual({p.name for p in folder.iterdir()}, archives | {"README.md", "manifest.json", "SHA256SUMS.txt"})
        self.assertEqual({r["path"] for r in manifest["files"]}, archives | {"README.md"})
        self.assertEqual((folder / "finance-skills-v1.3.0-markdown.zip").read_bytes(),
                         (self.root / "packages/markdown/finance-skills-markdown.zip").read_bytes())
        index = json.loads((self.root / "releases/latest.json").read_bytes())
        self.assertEqual(index["version"], "1.3.0")
        self.assertEqual({r["path"] for r in index["downloads"]}, {f"releases/v1.3.0/{name}" for name in archives})
        self.assertIn("START-HERE.md", (folder / "README.md").read_text())
        after = self.snapshot()
        self.assertEqual({name: after[name] for name in old}, old)
        before = self.snapshot()
        self.assertEqual(release.run(self.root, check=True)["status"], "verified")
        self.assertEqual(release.run(self.root)["status"], "unchanged")
        self.assertEqual(self.snapshot(), before)

    def test_suite_release_preserves_legacy_formats_and_has_exact_direct_imports(self):
        release.run(self.root)
        self.catalog["markdownBundleVersion"] = 1
        self.set_version("1.3.0")
        release.run(self.root)
        old = {name: value for name, value in self.snapshot().items()
               if name.startswith(("releases/v1.1.0/", "releases/v1.3.0/"))}

        self.catalog["suitePackageVersion"] = 1
        self.set_version("1.5.0")
        self.assertEqual(release.run(self.root)["status"], "created")
        folder = self.root / "releases/v1.5.0"
        manifest = release.verify_frozen(folder)
        variants = {"copilot-suite", "gemini-suite", "copilot", "gemini", "all", "markdown", "full"}
        archives = {f"finance-skills-v1.5.0-{variant}.zip" for variant in variants}
        self.assertEqual(manifest["schemaVersion"], 3)
        self.assertEqual({p.name for p in folder.iterdir()}, archives | {"README.md", "manifest.json", "SHA256SUMS.txt"})
        self.assertEqual({r["path"] for r in manifest["files"]}, archives | {"README.md"})
        for edition in ("copilot", "gemini"):
            payload = (folder / f"finance-skills-v1.5.0-{edition}-suite.zip").read_bytes()
            self.assertEqual(payload, (self.root / f"packages/suites/finance-suite-{edition}.zip").read_bytes())
            with zipfile.ZipFile(io.BytesIO(payload)) as suite:
                self.assertEqual(set(suite.namelist()), {"SKILL.md", "references/excel-agent-core.md", "references/sample-task.md"})
                self.assertTrue(suite.read("SKILL.md").startswith(b"---\nname: finance-suite\n"))
        index = json.loads((self.root / "releases/latest.json").read_bytes())
        self.assertEqual(index["version"], "1.5.0")
        self.assertEqual({r["path"] for r in index["downloads"]}, {f"releases/v1.5.0/{name}" for name in archives})
        readme = (folder / "README.md").read_text()
        self.assertIn("upload unchanged: one skill, all workflows", readme)
        self.assertIn("one finance-suite skill containing 2 workflow references", readme)
        self.assertIn("Individual Copilot packages — extract first", readme)
        self.assertIn("Every file in that ZIP is Markdown", readme)
        after = self.snapshot()
        self.assertEqual({name: after[name] for name in old}, old)
        checked = subprocess.run(
            [sys.executable, "-E", str(self.root / "scripts/release.py"), "--check"],
            cwd=self.root, capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(release.run(self.root)["status"], "unchanged")
        self.assertEqual(self.snapshot(), after)

    def test_suite_release_rejects_payload_differing_from_full_project(self):
        self.catalog.update(markdownBundleVersion=1, suitePackageVersion=1)
        self.set_version("1.5.0")
        release.run(self.root)
        folder = self.root / "releases/v1.5.0"
        name = "finance-skills-v1.5.0-copilot-suite.zip"
        with zipfile.ZipFile(folder / name) as original:
            entries = {path: original.read(path) for path in original.namelist()}
        entries["SKILL.md"] += b"\nUnreviewed replacement procedure.\n"
        replacement = build.archive_files(entries)
        (folder / name).write_bytes(replacement)
        manifest = json.loads((folder / "manifest.json").read_bytes())
        record = next(r for r in manifest["files"] if r["path"] == name)
        record.update(release.file_record(name, replacement))
        (folder / "manifest.json").write_bytes(build.json_bytes(manifest))
        (folder / "SHA256SUMS.txt").write_bytes(release.sums({
            p.name: p.read_bytes() for p in folder.iterdir() if p.name != "SHA256SUMS.txt"
        }))
        with self.assertRaisesRegex(release.ReleaseError, "Frozen suite package differs from full-project source"):
            release.verify_frozen(folder)

    def test_release_manifest_schema_and_inventory_are_strict_for_all_formats(self):
        release.run(self.root)
        self.catalog["markdownBundleVersion"] = 1
        self.set_version("1.3.0")
        release.run(self.root)
        self.catalog["suitePackageVersion"] = 1
        self.set_version("1.5.0")
        release.run(self.root)
        for version, schema in (("1.1.0", 1), ("1.3.0", 2), ("1.5.0", 3)):
            folder = self.root / f"releases/v{version}"
            manifest_path = folder / "manifest.json"
            original = manifest_path.read_bytes()
            for invalid in (None, True, False, 1.0, 2.0, 3.0, 0, 4, "1", [], {}):
                with self.subTest(version=version, schema=invalid):
                    manifest = json.loads(original)
                    manifest["schemaVersion"] = invalid
                    manifest_path.write_bytes(build.json_bytes(manifest))
                    with self.assertRaisesRegex(release.ReleaseError, "Invalid release manifest"):
                        release.verify_frozen(folder)
            for wrong_schema in {1, 2, 3} - {schema}:
                manifest = json.loads(original)
                manifest["schemaVersion"] = wrong_schema
                manifest_path.write_bytes(build.json_bytes(manifest))
                with self.assertRaisesRegex(release.ReleaseError, "Unexpected or missing files"):
                    release.verify_frozen(folder)
            manifest_path.write_bytes(original)
            variant = {1: "copilot", 2: "markdown", 3: "copilot-suite"}[schema]
            archive = folder / f"finance-skills-v{version}-{variant}.zip"
            archive_bytes = archive.read_bytes()
            archive.unlink()
            with self.assertRaisesRegex(release.ReleaseError, "Unexpected or missing files"):
                release.verify_frozen(folder)
            archive.write_bytes(archive_bytes)
            extra = folder / "unsupported.zip"
            extra.write_bytes(archive_bytes)
            with self.assertRaisesRegex(release.ReleaseError, "Unexpected or missing files"):
                release.verify_frozen(folder)
            extra.unlink()
            for invalid in ("missing", "duplicate", "unknown", "invalid path"):
                with self.subTest(version=version, inventory=invalid):
                    manifest = json.loads(original)
                    if invalid == "missing":
                        manifest["files"].pop()
                    elif invalid == "duplicate":
                        manifest["files"][-1] = manifest["files"][0]
                    else:
                        manifest["files"][0]["path"] = "unknown.zip" if invalid == "unknown" else []
                    manifest_path.write_bytes(build.json_bytes(manifest))
                    with self.assertRaisesRegex(release.ReleaseError, "Invalid release file inventory"):
                        release.verify_frozen(folder)
            manifest_path.write_bytes(original)
            self.assertEqual(release.verify_frozen(folder)["schemaVersion"], schema)

    def test_unsupported_markdown_bundle_version_cannot_create_a_release(self):
        for invalid in (True, False, 0, 2, 1.0, "1", [], {}):
            with self.subTest(version=invalid):
                self.catalog["markdownBundleVersion"] = invalid
                self.write("catalog.json", build.json_bytes(self.catalog))
                before = self.snapshot()
                with self.assertRaisesRegex(release.ReleaseError, "Unsupported Markdown bundle version"):
                    release.run(self.root)
                self.assertEqual(self.snapshot(), before)
                self.assertFalse((self.root / "releases").exists())

    def test_unsupported_suite_version_or_missing_markdown_cannot_create_a_release(self):
        self.catalog["markdownBundleVersion"] = 1
        for invalid in (None, True, False, 0, 2, 1.0, "1", [], {}):
            with self.subTest(version=invalid):
                self.catalog["suitePackageVersion"] = invalid
                self.write("catalog.json", build.json_bytes(self.catalog))
                before = self.snapshot()
                with self.assertRaisesRegex(release.ReleaseError, "Unsupported suite package version"):
                    release.run(self.root)
                self.assertEqual(self.snapshot(), before)
                self.assertFalse((self.root / "releases").exists())
        self.catalog["suitePackageVersion"] = 1
        self.catalog.pop("markdownBundleVersion")
        self.write("catalog.json", build.json_bytes(self.catalog))
        before = self.snapshot()
        with self.assertRaisesRegex(release.ReleaseError, "Suite packages require Markdown bundle version 1"):
            release.run(self.root)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "releases").exists())

    def test_determinism_ignores_mtime_and_source_file_permissions(self):
        first = release.prepare(self.root)[1]
        for file in self.root.rglob("*"):
            if file.is_file():
                os.utime(file, (1234567890, 1234567890))
                file.chmod(0o600)
        self.assertEqual(release.prepare(self.root)[1], first)

    def test_source_notes_or_ref_change_cannot_rewrite_existing_version(self):
        release.run(self.root)
        frozen = {p.name: p.read_bytes() for p in (self.root / "releases/v1.1.0").iterdir()}
        for name in ("README.md", "release-notes/v1.1.0.md"):
            original = (self.root / name).read_bytes()
            self.write(name, original + b"Changed after freeze.\n")
            with self.assertRaisesRegex(release.ReleaseError, "existing version"):
                release.run(self.root)
            with self.assertRaisesRegex(release.ReleaseError, "frozen version"):
                release.run(self.root, check=True)
            self.write(name, original)
        with self.assertRaisesRegex(release.ReleaseError, "existing version"):
            release.run(self.root, download_ref="stable")
        self.assertEqual({p.name: p.read_bytes() for p in (self.root / "releases/v1.1.0").iterdir()}, frozen)

    def test_build_drift_fails_without_creating_or_changing_release_outputs(self):
        before = self.snapshot()
        source = self.root / "skills/sample-task/SKILL.md"
        source.write_bytes(source.read_bytes() + b"\nNew canonical instruction.\n")
        for check in (False, True):
            with self.assertRaisesRegex(release.ReleaseError, "build drift"):
                release.run(self.root, check=check)
        self.assertFalse((self.root / "releases").exists())
        for name, (data, modified) in before.items():
            if name != "skills/sample-task/SKILL.md":
                self.assertEqual((self.root / name).read_bytes(), data)
                self.assertEqual((self.root / name).stat().st_mtime_ns, modified)
        self.rebuild()
        self.write("packages/copilot/unexpected.zip", b"not a package")
        with self.assertRaisesRegex(release.ReleaseError, "Unexpected"):
            release.run(self.root)

    def test_semver_is_strict_and_index_sorts_numerically_preserving_older_versions(self):
        for bad in ("01.1.0", "1.01.0", "1.1.00", "v1.1.0", "1.1", "1.1.0-rc.1", "1.1.0+build", "1.1.0\n", 1):
            with self.subTest(version=bad), self.assertRaises(release.ReleaseError):
                release.version_key(bad)
        self.assertEqual(release.version_key("0.0.0"), (0, 0, 0))
        release.run(self.root)
        first = {p.name: p.read_bytes() for p in (self.root / "releases/v1.1.0").iterdir()}
        for version in ("1.10.0", "1.9.0"):
            self.set_version(version)
            release.run(self.root)
        index = json.loads((self.root / "releases/latest.json").read_bytes())
        self.assertEqual(index["version"], "1.10.0")
        readme = (self.root / "releases/README.md").read_text()
        self.assertLess(readme.index("| 1.10.0 |"), readme.index("| 1.9.0 |"))
        self.assertEqual({p.name: p.read_bytes() for p in (self.root / "releases/v1.1.0").iterdir()}, first)
        release.run(self.root, check=True)

    def test_missing_notes_invalid_paths_case_collisions_and_symlinks_fail(self):
        notes = self.root / "release-notes/v1.1.0.md"
        original = notes.read_bytes()
        notes.unlink()
        with self.assertRaisesRegex(release.ReleaseError, "release notes"):
            release.prepare(self.root)
        notes.write_bytes(original)
        for path in ("../escape.txt", "/absolute.txt", "a//b", "a\\b", "CON.txt", "a:stream", "trailing.", "space "):
            with self.subTest(path=path), self.assertRaises(release.ReleaseError):
                release.safe_path(path)
        self.write("docs/guide.md", b"first")
        self.write("docs/GUIDE.md", b"second")
        with self.assertRaisesRegex(release.ReleaseError, "case collision"):
            release.prepare(self.root)
        (self.root / "docs/GUIDE.md").unlink()
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("private")
        link = self.root / "docs/linked.md"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        with self.assertRaisesRegex(release.ReleaseError, "Symlink"):
            release.run(self.root)
        self.assertEqual(outside.read_text(), "private")

    def test_corrupted_old_release_and_index_drift_are_detected_read_only(self):
        release.run(self.root)
        index = self.root / "releases/latest.json"
        index.write_bytes(b"{}\n")
        before = self.snapshot()
        with self.assertRaisesRegex(release.ReleaseError, "index drift"):
            release.run(self.root, check=True)
        self.assertEqual(self.snapshot(), before)
        release.run(self.root)  # Mutable indexes may be regenerated; frozen bytes may not.
        self.set_version("1.2.0")
        old = self.root / "releases/v1.1.0/finance-skills-v1.1.0-copilot.zip"
        old.write_bytes(old.read_bytes() + b"corrupt")
        before = self.snapshot()
        with self.assertRaisesRegex(release.ReleaseError, "checksum mismatch"):
            release.run(self.root)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "releases/v1.2.0").exists())

    def test_partial_stage_is_cleaned_and_missing_check_creates_nothing(self):
        before = self.snapshot()
        with self.assertRaises(release.ReleaseError):
            release.run(self.root, check=True)
        self.assertEqual(self.snapshot(), before)
        with mock.patch.object(Path, "rename", side_effect=OSError("synthetic rename failure")):
            with self.assertRaisesRegex(OSError, "rename failure"):
                release.run(self.root)
        self.assertEqual(list((self.root / "releases").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
