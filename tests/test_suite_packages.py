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
        cls.catalog.pop("excelFolderBundleVersion", None)
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
        for flag in (None, True, False, 0, 3, 1.0, 2.0, "1", {}):
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


class GroupedSuitePackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "catalog.json").read_text())
        cls.catalog.pop("excelFolderBundleVersion", None)
        cls.catalog.update(suitePackageVersion=2, markdownBundleVersion=1)
        cls.outputs = SuitePackagingTests.generate_catalog(cls.catalog)
        cls.manifest = json.loads(cls.outputs[Path("packages/suites/manifest.json")])
        cls.sources = {row["name"]: (ROOT / "skills" / row["name"] / "SKILL.md").read_bytes()
                       for row in cls.catalog["skills"]}
        # Split independently of the production parser, preserving its declared body contract.
        cls.bodies = {name: source.decode("utf-8").split("\n---\n", 1)[1].strip()
                      for name, source in cls.sources.items()}

    @staticmethod
    def minimum_members(count=1):
        root = (b'---\nname: finance-suite\ndescription: "Use for finance tasks"\n---\n\n'
                b'# Finance suite\n\nUse approved inputs.\n')
        return {"SKILL.md": root,
                **{f"references/group-{number}.md": b"# Reference\n\nKeep approved inputs.\n"
                   for number in range(count)}}

    def test_grouped_packages_keep_all_workflows_in_nine_companions(self):
        expected_resources = {f"references/{category}.md" for category in (
            "agent-setup", "core", "controls", "planning", "analysis", "reporting",
            "design", "research", "pipeline")}
        names = {row["name"] for row in self.catalog["skills"]}
        self.assertEqual(len(names), 30)
        self.assertEqual(self.manifest["schemaVersion"], 2)
        self.assertEqual(self.manifest["layoutVersion"], 2)
        self.assertEqual(self.manifest["companionFileCountPerPackage"], 9)
        self.assertEqual(self.manifest["workflowCount"], 30)
        self.assertEqual(self.manifest["registrationCountPerPackage"], 1)
        repeated = SuitePackagingTests.generate_catalog(self.catalog)
        self.assertEqual(self.outputs[Path("packages/suites/manifest.json")],
                         repeated[Path("packages/suites/manifest.json")])
        core_defaults = self.bodies["excel-agent-core"].split("\n", 1)[1].strip()
        for record in self.manifest["packages"]:
            with self.subTest(edition=record["edition"]):
                path = Path(record["path"])
                payload = self.outputs[path]
                self.assertEqual(payload, repeated[path])
                self.assertEqual(record["layoutVersion"], 2)
                self.assertEqual(record["companionFileCount"], 9)
                self.assertEqual(record["fileCount"], 10)
                self.assertEqual(record["workflowCount"], 30)
                self.assertEqual(record["nativeStatus"], "not-validated")
                self.assertEqual(record["packageSha256"], hashlib.sha256(payload).hexdigest())
                self.assertEqual(record["packageBytes"], len(payload))
                with zipfile.ZipFile(io.BytesIO(payload)) as packed:
                    self.assertEqual(packed.namelist(), sorted(expected_resources | {"SKILL.md"}))
                    self.assertIsNone(packed.testzip())
                    resources = {name: packed.read(name) for name in expected_resources}
                    root = packed.read("SKILL.md")
                    text = root.decode("utf-8")
                    self.assertTrue(text.startswith('---\nname: finance-suite\ndescription: "'))
                    self.assertLess(len(text), 20000)
                    self.assertFalse(root.startswith(b"\xef\xbb\xbf"))
                    self.assertNotIn(b"\r", root)
                    self.assertIn(core_defaults, text)
                    self.assertIn((ROOT / "adapters/workflow-controls.md").read_text().strip(), text)
                    self.assertIn((ROOT / "adapters" / f"{record['edition']}.md").read_text().strip(), text)
                    self.assertIn("read that entire workflow section", text)
                    self.assertIn("Invoke `finance-suite` and select that section", text)
                    self.assertIn("Copying this root alone does not include the referenced procedures", text)
                    routes = re.findall(r"^- \[[^\n]+\]\((references/[^)]+)\), `([^`]+)`:", text, re.M)
                    self.assertEqual(len(routes), 30)
                    self.assertEqual({name for _, name in routes}, names)
                    route_by_name = {name: path for path, name in routes}
                    self.assertEqual(set(route_by_name.values()), expected_resources)
                    self.assertEqual(len(record["workflows"]), 30)
                    self.assertEqual({row["name"] for row in record["workflows"]}, names)
                    all_section_names = []
                    for content in resources.values():
                        all_section_names += re.findall(rb"^## Workflow: ([a-z0-9-]+)$", content, re.M)
                    self.assertEqual(sorted(name.decode() for name in all_section_names), sorted(names))
                    for workflow in record["workflows"]:
                        name = workflow["name"]
                        body = (self.bodies[name] + "\n").encode("utf-8")
                        resource = workflow["resource"]
                        self.assertEqual(route_by_name[name], resource)
                        self.assertEqual(workflow["sectionHeading"], f"Workflow: {name}")
                        offset, length = workflow["bodyOffsetBytes"], workflow["bodyLengthBytes"]
                        self.assertEqual(resources[resource][offset:offset + length], body)
                        self.assertEqual(sum(content.count(body) for content in resources.values()), 1)
                        self.assertEqual(workflow["bodySha256"], hashlib.sha256(body).hexdigest())
                        self.assertEqual(workflow["sourceSha256"], hashlib.sha256(self.sources[name]).hexdigest())
                        self.assertEqual(workflow["sourcePath"], f"skills/{name}/SKILL.md")
                    for row in record["files"]:
                        content = packed.read(row["path"])
                        self.assertEqual(row["bytes"], len(content))
                        self.assertEqual(row["sha256"], hashlib.sha256(content).hexdigest())
                        self.assertEqual(self.outputs[Path(record["expandedPath"]) / row["path"]], content)
                    self.assertEqual(sum(entry.file_size for entry in packed.infolist()),
                                     sum(len(packed.read(name)) for name in packed.namelist()))
                    for entry in packed.infolist():
                        self.assertFalse(entry.flag_bits & 1)
                        self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                        self.assertEqual(entry.external_attr >> 16, 0o100644)
                    build.validate_portable_suite_members({"SKILL.md": root, **resources}, payload)

    def test_grouped_layout_keeps_individual_and_legacy_suite_contracts(self):
        legacy_catalog = deepcopy(self.catalog)
        legacy_catalog["suitePackageVersion"] = 1
        legacy = SuitePackagingTests.generate_catalog(legacy_catalog)
        for path, content in legacy.items():
            if (path.parts[:2] in (("packages", "copilot"), ("packages", "gemini"),
                                  ("packages", "bundles"), ("packages", "markdown"),
                                  ("editions", "copilot"), ("editions", "gemini"),
                                  ("editions", "gemini-gems"))
                    or path.as_posix() in ("packages/manifest.json", "profiles/excel-agent-instructions.txt")):
                self.assertEqual(content, self.outputs[path], path.as_posix())
        manifest = json.loads(legacy[Path("packages/suites/manifest.json")])
        self.assertEqual(manifest["schemaVersion"], 1)
        self.assertNotIn("layoutVersion", manifest)
        for record in manifest["packages"]:
            self.assertNotIn("workflows", record)
            self.assertNotIn("companionFileCount", record)
            with zipfile.ZipFile(io.BytesIO(legacy[Path(record["path"])])) as packed:
                self.assertEqual(set(packed.namelist()), {"SKILL.md"} | {
                    f"references/{name}.md" for name in self.sources})

    def test_portability_guard_rejects_ungrouped_current_workflows(self):
        legacy_catalog = deepcopy(self.catalog)
        legacy_catalog["suitePackageVersion"] = 1
        legacy = SuitePackagingTests.generate_catalog(legacy_catalog)
        with zipfile.ZipFile(io.BytesIO(legacy[Path("packages/suites/finance-suite-copilot.zip")])) as packed:
            members = {name: packed.read(name) for name in packed.namelist()}
        self.assertEqual(len(members), 1 + len(legacy_catalog["skills"]))
        with self.assertRaisesRegex(ValueError, "20-companion"):
            build.validate_portable_suite_members(members)

    def test_companion_count_and_byte_boundaries(self):
        build.validate_portable_suite_members(self.minimum_members(20))
        with self.assertRaisesRegex(ValueError, "20-companion"):
            build.validate_portable_suite_members(self.minimum_members(21))
        members = self.minimum_members(2)
        members["references/group-0.md"] = b"x" * 5_000_000
        members["references/group-1.md"] = b"y" * 5_000_000
        build.validate_portable_suite_members(members)
        too_large = dict(members)
        too_large["references/group-0.md"] += b"x"
        with self.assertRaisesRegex(ValueError, "5 MB"):
            build.validate_portable_suite_members(too_large)
        too_many_bytes = dict(members, **{"references/extra.md": b"z"})
        with self.assertRaisesRegex(ValueError, "10 MB total"):
            build.validate_portable_suite_members(too_many_bytes)

    def test_compressed_and_root_instruction_boundaries(self):
        members = self.minimum_members()
        build.validate_portable_suite_members(members, b"x" * 10_000_000)
        with self.assertRaisesRegex(ValueError, "10 MB compressed"):
            build.validate_portable_suite_members(members, b"x" * 10_000_001)
        root = members["SKILL.md"]
        members["SKILL.md"] = root + b"x" * (19999 - len(root))
        build.validate_portable_suite_members(members)
        members["SKILL.md"] += b"x"
        with self.assertRaisesRegex(ValueError, "20,000-character"):
            build.validate_portable_suite_members(members)

    def test_unsafe_and_reserved_companion_paths_are_rejected(self):
        root = self.minimum_members(0)["SKILL.md"]
        for path in ("references/../escape.md", "references/CON.md", "references/.hidden.md",
                     "/references/file.md", "references\\file.md", "references/con.md",
                     "references/lpt1.md"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "unsafe resource|reserved filename"):
                build.validate_portable_suite_members({"SKILL.md": root, path: b"# Safe content\n"})

    def test_grouping_rejects_ambiguous_missing_or_excessive_categories(self):
        rows = deepcopy(self.catalog["skills"])
        for invalid in (None, "", " Core", "Core ", "Core/Tasks", "Core\nTasks", "日本", "CON"):
            rows[0]["category"] = invalid
            with self.subTest(category=invalid), self.assertRaisesRegex(ValueError, "category|reserved filename"):
                build.grouped_suite_resources(rows, self.sources, self.bodies)
        rows = deepcopy(self.catalog["skills"])
        rows[0]["category"], rows[1]["category"] = "Core Tasks", "Core-Tasks"
        with self.assertRaisesRegex(ValueError, "categories collide"):
            build.grouped_suite_resources(rows, self.sources, self.bodies)
        for number, row in enumerate(rows):
            row["category"] = f"Category {number}"
        with self.assertRaisesRegex(ValueError, "20-companion"):
            build.grouped_suite_resources(rows, self.sources, self.bodies)

    def test_workflow_mapping_rejects_missing_duplicate_changed_or_mislocated_bodies(self):
        record = self.manifest["packages"][0]
        with zipfile.ZipFile(io.BytesIO(self.outputs[Path(record["path"])])) as packed:
            resources = {name: packed.read(name) for name in packed.namelist() if name != "SKILL.md"}
        original = record["workflows"]
        validate = lambda refs, mappings: build.validate_grouped_workflows(
            self.catalog["skills"], self.sources, self.bodies, refs, mappings)
        for mappings in (original[:-1], original + [original[0]]):
            with self.assertRaisesRegex(ValueError, "exactly once"):
                validate(resources, mappings)
        for key, value in (("bodyOffsetBytes", True), ("bodyOffsetBytes", 0),
                           ("bodySha256", "0" * 64), ("sourceSha256", "0" * 64),
                           ("sectionHeading", "Workflow: wrong")):
            mappings = deepcopy(original)
            mappings[0][key] = value
            with self.subTest(key=key, value=value), self.assertRaisesRegex(ValueError, "mapping differs"):
                validate(resources, mappings)
        first = original[0]
        path, offset = first["resource"], first["bodyOffsetBytes"]
        changed = dict(resources)
        changed[path] = changed[path][:offset] + b"!" + changed[path][offset + 1:]
        with self.assertRaisesRegex(ValueError, "mapping differs"):
            validate(changed, original)
        duplicate = dict(resources)
        duplicate[path] += (self.bodies[first["name"]] + "\n").encode()
        with self.assertRaisesRegex(ValueError, "duplicates or omits"):
            validate(duplicate, original)
        unknown = dict(resources)
        unknown[path] += b"\n## Workflow: unknown\n\nUnexpected procedure.\n"
        with self.assertRaisesRegex(ValueError, "section inventory differs"):
            validate(unknown, original)
        with self.assertRaisesRegex(ValueError, "unmapped resources"):
            validate({**resources, "references/extra.md": b"# Unmapped\n"}, original)


if __name__ == "__main__":
    unittest.main()
