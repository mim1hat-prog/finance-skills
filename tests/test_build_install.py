from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build
import install_edition


class PackagingTests(unittest.TestCase):
    def test_all_packages_are_deterministic_standalone_and_exact(self):
        first, second = build.generate(ROOT), build.generate(ROOT)
        self.assertEqual(first, second)
        catalog = json.loads((ROOT / "catalog.json").read_text())
        names = {row["name"] for row in catalog["skills"]}
        manifest = json.loads(first[Path("packages/manifest.json")])
        self.assertEqual(len(manifest["skills"]), 2 * len(names))
        for row in manifest["skills"]:
            source = first[Path("editions") / row["edition"] / row["name"] / "SKILL.md"]
            data = first[Path(row["path"])]
            with zipfile.ZipFile(io.BytesIO(data)) as packed:
                self.assertEqual(packed.namelist(), ["SKILL.md"])
                self.assertEqual(packed.read("SKILL.md"), source)
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["packageSha256"])
            self.assertEqual(hashlib.sha256(source).hexdigest(), row["skillSha256"])
            self.assertLess(len(source.decode()), 20000)

        canonical = (ROOT / "skills/excel-agent-core/SKILL.md").read_bytes()
        body = build.parse_skill(canonical, "excel-agent-core")[2]
        profile_path = Path("profiles/excel-agent-instructions.txt")
        self.assertEqual(first[profile_path], (body + "\n").encode("utf-8"))
        self.assertFalse(first[profile_path].startswith(b"---"))
        bundle_index = json.loads(first[Path("packages/bundles/manifest.json")])
        self.assertEqual(bundle_index["version"], catalog["version"])
        expected_bundles = {
            "finance-skills-copilot": ["copilot"],
            "finance-skills-gemini": ["gemini"],
            "finance-skills-all": ["copilot", "gemini"],
        }
        self.assertEqual({r["name"] for r in bundle_index["bundles"]}, set(expected_bundles))
        for record in bundle_index["bundles"]:
            editions = expected_bundles[record["name"]]
            expected = {"manifest.json", "START-HERE.md", profile_path.as_posix()}
            for edition in editions:
                expected.add(f"packages/{edition}/manifest.json")
                expected.update(f"editions/{edition}/{name}/SKILL.md" for name in names)
                expected.update(f"packages/{edition}/{name}.zip" for name in names)
                if edition == "gemini":
                    expected.update(f"editions/gemini-gems/{name}.txt" for name in names)
            payload = first[Path(record["path"])]
            self.assertEqual(record["editions"], editions)
            self.assertEqual(record["skillCount"], len(names))
            self.assertEqual(record["packageCount"], len(names) * len(editions))
            self.assertEqual(record["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(record["bytes"], len(payload))
            with zipfile.ZipFile(io.BytesIO(payload)) as transport:
                self.assertEqual(transport.namelist(), sorted(expected))
                self.assertEqual(record["fileCount"], len(expected))
                self.assertFalse(any(path.startswith("packages/bundles/") for path in transport.namelist()))
                self.assertEqual(transport.read(profile_path.as_posix()), first[profile_path])
                bundled_manifest = json.loads(transport.read("manifest.json"))
                self.assertEqual(bundled_manifest["version"], catalog["version"])
                self.assertEqual(bundled_manifest["editions"], editions)
                self.assertEqual(bundled_manifest["skillCount"], len(names))
                self.assertEqual(bundled_manifest["packageCount"], len(names) * len(editions))
                files = bundled_manifest["files"]
                self.assertEqual([f["path"] for f in files], sorted(expected - {"manifest.json"}))
                for file in files:
                    data = transport.read(file["path"])
                    self.assertEqual(file["sha256"], hashlib.sha256(data).hexdigest())
                    self.assertEqual(file["bytes"], len(data))
                    if file["path"] != "START-HERE.md":
                        self.assertEqual(data, first[Path(file["path"])])
                guide = transport.read("START-HERE.md").decode("utf-8")
                self.assertIn("extract this outer ZIP", guide)
                self.assertIn("one skill at a time", guide)
                for edition in editions:
                    self.assertIn(catalog["repoUrl"].rstrip("/") + f"/blob/main/docs/{edition.upper()}.md", guide)
                    for name in names:
                        package_path = f"packages/{edition}/{name}.zip"
                        skill_path = f"editions/{edition}/{name}/SKILL.md"
                        with zipfile.ZipFile(io.BytesIO(transport.read(package_path))) as native:
                            self.assertEqual(native.namelist(), ["SKILL.md"])
                            self.assertEqual(native.read("SKILL.md"), transport.read(skill_path))
                for entry in transport.infolist():
                    self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(entry.external_attr >> 16, 0o100644)

    def test_small_catalogue_uses_actual_repo_and_checks_profile_outputs_without_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            names = ["excel-agent-core", "sample-task"]
            catalog = {
                "schemaVersion": 1, "version": "9.8.7", "reviewedOn": "2026-11-25",
                "repoUrl": "https://github.com/example/financial-control",
                "skills": [{
                    "name": name, "title": name.title(), "summary": "A useful task.",
                    "category": "Core", "group": "selection", "prompt": "Do the task.",
                } for name in names],
            }
            (root / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            for name in names:
                folder = root / "skills" / name
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_bytes((
                    f'---\nname: {name}\ndescription: "Use for a useful task"\n---\n\n'
                    f"# {name.title()}\n\nApply the canonical procedure.\n"
                ).encode("utf-8"))
            (root / "adapters").mkdir()
            for edition in ("copilot", "gemini"):
                (root / "adapters" / f"{edition}.md").write_text(
                    f"## {edition} overlay\n\nUse the available tools.", encoding="utf-8",
                )
            outputs = build.generate(root)
            bundles = json.loads(outputs[Path("packages/bundles/manifest.json")])["bundles"]
            self.assertEqual({record["skillCount"] for record in bundles}, {2})
            self.assertEqual({record["packageCount"] for record in bundles}, {2, 4})
            with zipfile.ZipFile(io.BytesIO(outputs[Path("packages/bundles/finance-skills-all.zip")])) as packed:
                self.assertIn(
                    b"https://github.com/example/financial-control/blob/main/docs/COPILOT.md",
                    packed.read("START-HERE.md"),
                )
                profile = packed.read("profiles/excel-agent-instructions.txt")
                self.assertEqual(profile, b"# Excel-Agent-Core\n\nApply the canonical procedure.\n")
                self.assertNotIn(b"overlay", profile)
            index = outputs[Path("SKILLS.md")].decode("utf-8")
            self.assertIn("2 skills", index)
            self.assertNotIn("three suggested groups", index)
            for path in ("profiles/excel-agent-instructions.txt",
                         "packages/bundles/finance-skills-copilot.zip",
                         "packages/bundles/finance-skills-gemini.zip",
                         "packages/bundles/finance-skills-all.zip"):
                self.assertIn(path, index)
                if path.endswith(".zip"):
                    self.assertIn(path + "?raw=1", index)
            for relative, data in outputs.items():
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
            unexpected = root / "profiles/private-note.txt"
            unexpected.write_text("Preserve this file.", encoding="utf-8")
            with mock.patch.object(build, "ROOT", root), mock.patch.object(sys, "argv", ["build.py", "--check"]):
                error = io.StringIO()
                with redirect_stderr(error), redirect_stdout(io.StringIO()):
                    self.assertEqual(build.main(), 1)
                self.assertIn("Unexpected generated files", error.getvalue())
                self.assertEqual(unexpected.read_text(), "Preserve this file.")
                self.assertEqual((root / "profiles/excel-agent-instructions.txt").read_bytes(),
                                 outputs[Path("profiles/excel-agent-instructions.txt")])
                unexpected.unlink()
                profile_path = root / "profiles/excel-agent-instructions.txt"
                profile_path.write_text("Local profile edit.", encoding="utf-8")
                error = io.StringIO()
                with redirect_stderr(error), redirect_stdout(io.StringIO()):
                    self.assertEqual(build.main(), 1)
                self.assertIn("Stale generated files", error.getvalue())
                self.assertEqual(profile_path.read_text(), "Local profile edit.")

    def test_invalid_names_unbundled_resources_and_bom_fail(self):
        base = b'---\nname: good-name\ndescription: "A useful trigger"\n---\n\n# Good\n\nDo a task.\n'
        build.parse_skill(base, "good-name")
        for data, name in [(base, "other-name"), (b'\xef\xbb\xbf' + base, "good-name"),
                           (base + b'\nSee [file](missing.py).', "good-name"),
                           (base.replace(b'good-name', b'bad--name'), "bad--name")]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                build.parse_skill(data, name)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.dest = Path(self.temp.name) / "office"
        self.root.mkdir()
        # A tiny real format fixture keeps installer tests independent of the full catalogue.
        skill = b'---\nname: test-skill\ndescription: "Use for test tasks"\n---\n\n# Test\n\nDo a task.\n'
        package = build.archive(skill)
        source = self.root / "editions/copilot/test-skill/SKILL.md"
        source.parent.mkdir(parents=True)
        source.write_bytes(skill)
        folder = self.root / "packages/copilot"
        folder.mkdir(parents=True)
        (folder / "test-skill.zip").write_bytes(package)
        self.manifest = {"version": "1.0.0", "reviewedOn": "2026-11-25", "skills": [{"name": "test-skill", "skillSha256": build.sha(skill), "packageSha256": build.sha(package)}]}
        (folder / "manifest.json").write_text(json.dumps(self.manifest))

    def tearDown(self):
        self.temp.cleanup()

    def test_preview_then_apply_is_idempotent_and_preserves_local_edits(self):
        changes, receipt = install_edition.plan(self.root, "copilot", self.dest, None)
        self.assertFalse(self.dest.exists())
        install_edition.apply(changes, receipt, self.dest)
        changes, receipt = install_edition.plan(self.root, "copilot", self.dest, None)
        self.assertEqual(changes[0]["status"], "unchanged")
        target = self.dest / "test-skill/SKILL.md"
        target.write_text("local customization")
        with self.assertRaises(ValueError):
            install_edition.plan(self.root, "copilot", self.dest, None)
        self.assertEqual(target.read_text(), "local customization")

    def test_package_corruption_and_source_race_fail_before_writes(self):
        changes, receipt = install_edition.plan(self.root, "copilot", self.dest, None)
        changes[0]["source"].write_text("changed")
        with self.assertRaises(ValueError):
            install_edition.apply(changes, receipt, self.dest)
        self.assertFalse(self.dest.exists())
        with self.assertRaises(ValueError):
            install_edition.plan(self.root, "copilot", self.dest, None)

    def test_linked_targets_are_refused(self):
        self.dest.mkdir()
        external = Path(self.temp.name) / "external"
        external.mkdir()
        try:
            (self.dest / "test-skill").symlink_to(external, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"This account cannot create directory symlinks: {exc}")
        with self.assertRaises(ValueError):
            install_edition.plan(self.root, "copilot", self.dest, None)
        self.assertEqual(list(external.iterdir()), [])

    def test_destination_link_created_after_preview_is_refused(self):
        changes, receipt = install_edition.plan(self.root, "copilot", self.dest, None)
        external = Path(self.temp.name) / "external"
        external.mkdir()
        try:
            self.dest.symlink_to(external, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"This account cannot create directory symlinks: {exc}")
        with self.assertRaises(ValueError):
            install_edition.apply(changes, receipt, self.dest)
        self.assertEqual(list(external.iterdir()), [])

    @unittest.skipUnless(shutil.which("git"), "Optional Git checkout regression needs Git")
    def test_autocrlf_checkout_keeps_hashed_markdown_and_zip_bytes(self):
        checkout = Path(self.temp.name) / "windows-checkout"
        checkout.mkdir()
        def git(*args):
            return subprocess.run(["git", "-C", str(checkout), *args], check=True, capture_output=True)
        git("init", "--quiet")
        git("config", "core.autocrlf", "true")
        git("config", "core.hooksPath", str(checkout / "no-hooks"))
        shutil.copyfile(ROOT / ".gitattributes", checkout / ".gitattributes")
        expected = {"skill.md": b"# Skill\n\nDo a task.\n", "skill.zip": build.archive(b"# Skill\n")}
        for name, data in expected.items():
            (checkout / name).write_bytes(data)
        git("add", ".gitattributes", "skill.md", "skill.zip")
        git("-c", "user.name=Local test", "-c", "user.email=test@example.invalid", "commit", "--quiet", "--no-gpg-sign", "-m", "Fixture")
        for name in expected:
            (checkout / name).unlink()
        git("checkout", "--", "skill.md", "skill.zip")
        for name, data in expected.items():
            self.assertEqual((checkout / name).read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
