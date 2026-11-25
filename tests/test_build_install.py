import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build
import install_edition


class PackagingTests(unittest.TestCase):
    def test_all_packages_are_deterministic_standalone_and_exact(self):
        first, second = build.generate(ROOT), build.generate(ROOT)
        self.assertEqual(first, second)
        manifest = json.loads(first[Path("packages/manifest.json")])
        self.assertEqual(len(manifest["skills"]), 2 * len(json.loads((ROOT / "catalog.json").read_text())["skills"]))
        for row in manifest["skills"]:
            source = first[Path("editions") / row["edition"] / row["name"] / "SKILL.md"]
            data = first[Path(row["path"])]
            with zipfile.ZipFile(io.BytesIO(data)) as packed:
                self.assertEqual(packed.namelist(), ["SKILL.md"])
                self.assertEqual(packed.read("SKILL.md"), source)
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["packageSha256"])
            self.assertEqual(hashlib.sha256(source).hexdigest(), row["skillSha256"])
            self.assertLess(len(source.decode()), 20000)

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
