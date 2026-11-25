"""Release snapshots are immutable and independently verifiable download artifacts."""
from __future__ import annotations

import hashlib
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
