"""Exercise real suite bytes, resource failures and compatibility with individual imports."""
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build


class SuitePackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "catalog.json").read_text())
        cls.catalog["suitePackageVersion"] = 1
        cls.catalog["markdownBundleVersion"] = 1
        cls.outputs = cls.generate_catalog(cls.catalog)

    @staticmethod
    def generate_catalog(catalog):
        """Vary catalogue flags without modifying the shared repository."""
        read_text = Path.read_text
        replacement = json.dumps(catalog)

        def read(path, *args, **kwargs):
            return replacement if path == ROOT / "catalog.json" else read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", new=read):
            return build.generate(ROOT)

    def test_suites_preserve_all_procedures_and_have_exact_stable_members(self):
        repeated = self.generate_catalog(self.catalog)
        names = {row["name"] for row in self.catalog["skills"]}
        references = {f"references/{name}.md" for name in names}
        expected = references | {"SKILL.md"}
        manifest = json.loads(self.outputs[Path("packages/suites/manifest.json")])
        self.assertEqual(manifest["version"], self.catalog["version"])
        self.assertEqual(manifest["name"], "finance-suite")
        self.assertEqual(manifest["workflowCount"], len(names))
        self.assertEqual(manifest["registrationCountPerPackage"], 1)
        self.assertEqual({r["edition"] for r in manifest["packages"]}, set(build.EDITIONS))
        core = build.parse_skill((ROOT / "skills/excel-agent-core/SKILL.md").read_bytes(),
                                 "excel-agent-core")[2]
        shared = (ROOT / "adapters/workflow-controls.md").read_text().strip()
        for record in manifest["packages"]:
            edition = record["edition"]
            package_path = Path(record["path"])
            payload = self.outputs[package_path]
            self.assertEqual(payload, repeated[package_path])
            self.assertEqual(record["sourceVersion"], self.catalog["version"])
            self.assertEqual(record["registrationCount"], 1)
            self.assertEqual(record["nativeStatus"], "not-validated")
            self.assertEqual(record["workflowCount"], len(names))
            self.assertEqual(record["fileCount"], len(expected))
            self.assertEqual(record["packageBytes"], len(payload))
            self.assertEqual(record["packageSha256"], hashlib.sha256(payload).hexdigest())
            with zipfile.ZipFile(io.BytesIO(payload)) as packed:
                self.assertEqual(packed.namelist(), sorted(expected))
                self.assertFalse(any(name.endswith(".zip") for name in packed.namelist()))
                resources = {name: packed.read(name) for name in references}
                root = packed.read("SKILL.md")
                front, description, body = build.parse_skill(root, "finance-suite",
                                                             allowed_resources=resources)
                self.assertTrue(front.startswith("---\nname: finance-suite\ndescription: \""))
                self.assertTrue(description.strip())
                self.assertLess(len(root.decode("utf-8")), 20000)
                self.assertLess(len(body.splitlines()), 500)
                self.assertFalse(root.startswith(b"\xef\xbb\xbf"))
                self.assertNotIn(b"\r", root)
                self.assertIn(core.partition("\n")[2].strip(), body)
                self.assertIn(shared, body)
                self.assertIn((ROOT / "adapters" / f"{edition}.md").read_text().strip(), body)
                self.assertIn("Read each selected reference completely before applying", body)
                self.assertIn("unavailable or unreadable", body)
                self.assertIn("one registered skill", body)
                local = {link for link in re.findall(r'\]\(([^)]+)\)', body)
                         if not link.startswith(("https://", "#"))}
                self.assertEqual(local, references)
                for name in names:
                    canonical = (ROOT / "skills" / name / "SKILL.md").read_bytes()
                    canonical_body = build.parse_skill(canonical, name)[2]
                    self.assertEqual(resources[f"references/{name}.md"],
                                     (canonical_body + "\n").encode("utf-8"))
                self.assertEqual([row["path"] for row in record["files"]], sorted(expected))
                for row in record["files"]:
                    content = packed.read(row["path"])
                    self.assertEqual(row["bytes"], len(content))
                    self.assertEqual(row["sha256"], hashlib.sha256(content).hexdigest())
                    expanded = Path(record["expandedPath"]) / row["path"]
                    self.assertEqual(self.outputs[expanded], content)
                    self.assertEqual(repeated[expanded], content)
                self.assertEqual({row["name"] for row in record["sources"]}, names)
                for row in record["sources"]:
                    self.assertEqual(row["sha256"],
                                     hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest())
                for entry in packed.infolist():
                    self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(entry.external_attr >> 16, 0o100644)
        self.assertEqual(self.outputs[Path("packages/suites/manifest.json")],
                         repeated[Path("packages/suites/manifest.json")])

    def test_suite_flag_preserves_individual_packages_and_transport_contracts(self):
        legacy_catalog = deepcopy(self.catalog)
        del legacy_catalog["suitePackageVersion"]
        legacy = self.generate_catalog(legacy_catalog)
        self.assertFalse(any(path.parts[:2] == ("packages", "suites") for path in legacy))
        for path, content in legacy.items():
            if (path.parts[:2] in (("packages", "copilot"), ("packages", "gemini"),
                                  ("packages", "bundles"), ("packages", "markdown"),
                                  ("editions", "copilot"), ("editions", "gemini"),
                                  ("editions", "gemini-gems"))
                    or path.as_posix() in ("packages/manifest.json", "profiles/excel-agent-instructions.txt")):
                self.assertEqual(content, self.outputs[path], path.as_posix())
        individual = json.loads(self.outputs[Path("packages/manifest.json")])
        self.assertEqual(len(individual["skills"]), len(self.catalog["skills"]) * 2)
        self.assertNotIn("finance-suite", {row["name"] for row in individual["skills"]})

    def test_suite_flag_is_explicit_and_requires_markdown_bundle_version_one(self):
        for flag in (None, True, False, 0, 2, 1.0, "1", {}):
            catalog = deepcopy(self.catalog)
            catalog["suitePackageVersion"] = flag
            with self.subTest(flag=flag), self.assertRaisesRegex(ValueError, "suite package version"):
                self.generate_catalog(catalog)
        for markdown in (None, "missing"):
            catalog = deepcopy(self.catalog)
            if markdown == "missing":
                del catalog["markdownBundleVersion"]
            else:
                catalog["markdownBundleVersion"] = markdown
            with self.subTest(markdown=markdown), self.assertRaisesRegex(ValueError, "require Markdown"):
                self.generate_catalog(catalog)

    def test_local_reference_allowlist_requires_actual_bytes_and_is_opt_in(self):
        source = (b'---\nname: finance-suite\ndescription: "Use for finance tasks"\n---\n\n'
                  b'# Finance suite\n\nRead [the procedure](references/sample-task.md).\n')
        resources = {"references/sample-task.md": b"# Sample task\n\nUse approved inputs.\n"}
        with self.assertRaisesRegex(ValueError, "unresolved local resource"):
            build.parse_skill(source, "finance-suite")
        with self.assertRaisesRegex(ValueError, "unresolved local resource"):
            build.parse_skill(source, "finance-suite", allowed_resources={})
        build.parse_skill(source, "finance-suite", allowed_resources=resources)
        for invalid in (None, b"", "not file bytes"):
            with self.subTest(content=invalid), self.assertRaisesRegex(ValueError, "missing resource bytes"):
                build.parse_skill(source, "finance-suite", allowed_resources={"references/sample-task.md": invalid})
        with self.assertRaisesRegex(ValueError, "must map"):
            build.parse_skill(source, "finance-suite", allowed_resources=["references/sample-task.md"])

    def test_unsafe_paths_and_unbundled_local_links_are_rejected(self):
        template = '---\nname: finance-suite\ndescription: "Use for finance tasks"\n---\n\n# Suite\n\nRead [procedure]({}).\n'
        safe = {"references/sample-task.md": b"# Procedure\n\nUse approved inputs.\n"}
        for path in ("../sample-task.md", "/references/sample-task.md", "references/../sample-task.md",
                     "references//sample-task.md", "references\\sample-task.md", "references/%2e%2e.md",
                     "references/Sample-task.md", "references/sample-task.md?raw=1", "file:///sample-task.md"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "unsafe resource path"):
                build.parse_skill(template.format(path).encode(), "finance-suite", allowed_resources={path: b"content"})
        for path in ("references/missing.md", "references/sample-task.md#heading", "../sample-task.md"):
            with self.subTest(link=path), self.assertRaisesRegex(ValueError, "unresolved local resource"):
                build.parse_skill(template.format(path).encode(), "finance-suite", allowed_resources=safe)

    def test_minimal_catalogue_supports_suite_generation_without_changing_legacy_fixture_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = ("excel-agent-core", "sample-task")
            catalog = {"schemaVersion": 1, "version": "9.8.7", "reviewedOn": "2026-11-26",
                       "repoUrl": "https://github.com/example/finance", "markdownBundleVersion": 1,
                       "suitePackageVersion": 1,
                       "skills": [{"name": name, "title": name.title(), "summary": "Use approved data.",
                                   "category": "Core", "group": "selection", "prompt": "Check the task."}
                                  for name in names]}
            (root / "catalog.json").write_text(json.dumps(catalog))
            for name in names:
                folder = root / "skills" / name
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(
                    f'---\nname: {name}\ndescription: "Use for finance tasks"\n---\n\n# {name}\n\n'
                    'Apply the complete canonical procedure.\n')
            (root / "adapters").mkdir()
            for edition in build.EDITIONS:
                (root / "adapters" / f"{edition}.md").write_text(f"## {edition}\n\nUse available tools.\n")
            outputs = build.generate(root)
            manifest = json.loads(outputs[Path("packages/suites/manifest.json")])
            self.assertEqual(manifest["workflowCount"], 2)
            for record in manifest["packages"]:
                self.assertEqual(record["fileCount"], 3)
                self.assertEqual(record["sourceVersion"], "9.8.7")
            del catalog["suitePackageVersion"]
            (root / "catalog.json").write_text(json.dumps(catalog))
            self.assertNotIn(Path("packages/suites/manifest.json"), build.generate(root))

    def test_suite_rejects_missing_defaults_mismatched_sources_and_excessive_file_count(self):
        def source(name, body="Apply approved defaults."):
            return (f'---\nname: {name}\ndescription: "Use for finance tasks"\n---\n\n'
                    f'# {name}\n\n{body}\n').encode()

        notes = {edition: f"## {edition}\n\nUse available tools." for edition in build.EDITIONS}
        catalog = {"version": "9.8.7", "reviewedOn": "2026-11-26", "skills": [
            {"name": "sample-task", "title": "Sample", "summary": "Use for a sample task."}]}
        with self.assertRaisesRegex(ValueError, "requires canonical excel-agent-core"):
            build.add_suite_packages({}, catalog, {"sample-task": source("sample-task")}, notes, "")
        with self.assertRaisesRegex(ValueError, "match the exact workflow catalogue"):
            build.add_suite_packages({}, catalog, {}, notes, "")
        names = ["excel-agent-core"] + [f"workflow-{index}" for index in range(99)]
        catalog["skills"] = [{"name": name, "title": "Task", "summary": "Check."} for name in names]
        with self.assertRaisesRegex(ValueError, "100-file ceiling"):
            build.add_suite_packages({}, catalog, {name: source(name) for name in names}, notes, "")


if __name__ == "__main__":
    unittest.main()
