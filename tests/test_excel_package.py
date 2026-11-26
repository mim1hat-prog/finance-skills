"""The Excel download transports one exact skill folder, never a native ZIP import."""
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build


class ExcelFolderPackageTests(unittest.TestCase):
    @staticmethod
    def generate_catalog(catalog):
        original = Path.read_text

        def read(path, *args, **kwargs):
            return json.dumps(catalog) if path == ROOT / "catalog.json" else original(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", new=read):
            return build.generate(ROOT)

    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "catalog.json").read_text())
        cls.catalog.update(excelFolderBundleVersion=1, suitePackageVersion=2, markdownBundleVersion=1)
        cls.outputs = cls.generate_catalog(cls.catalog)

    def test_exact_name_folder_contains_the_complete_unchanged_copilot_suite(self):
        payload = self.outputs[build.EXCEL_FOLDER_BUNDLE]
        source = Path("editions/copilot-suite/finance-suite")
        expected = {f"finance-suite/{path.relative_to(source).as_posix()}": content
                    for path, content in self.outputs.items() if path.is_relative_to(source)}
        self.assertEqual(len(expected), 10)
        self.assertEqual({name.split("/", 1)[0] for name in expected}, {"finance-suite"})
        self.assertEqual(payload, self.generate_catalog(self.catalog)[build.EXCEL_FOLDER_BUNDLE])
        with zipfile.ZipFile(io.BytesIO(payload)) as packed:
            self.assertEqual(packed.namelist(), sorted(expected))
            self.assertIsNone(packed.testzip())
            self.assertNotIn("SKILL.md", packed.namelist())
            root = packed.read("finance-suite/SKILL.md")
            self.assertTrue(root.startswith(b'---\nname: finance-suite\ndescription: "'))
            resources = {name.removeprefix("finance-suite/"): data for name, data in expected.items()
                         if name != "finance-suite/SKILL.md"}
            build.parse_skill(root, "finance-suite", allowed_resources=resources)
            for info in packed.infolist():
                self.assertEqual(packed.read(info.filename), expected[info.filename])
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.external_attr >> 16, 0o100644)
                self.assertFalse(info.flag_bits & 1)
        with zipfile.ZipFile(io.BytesIO(self.outputs[Path("packages/suites/finance-suite-copilot.zip")])) as native:
            self.assertEqual({f"finance-suite/{name}": native.read(name) for name in native.namelist()}, expected)

    def test_manifest_is_external_and_distinguishes_folder_upload_from_zip_import(self):
        metadata = json.loads(self.outputs[build.EXCEL_FOLDER_MANIFEST])
        payload = self.outputs[build.EXCEL_FOLDER_BUNDLE]
        self.assertEqual(metadata["kind"], "excel-onedrive-folder-package")
        self.assertEqual(metadata["schemaVersion"], 1)
        self.assertEqual(metadata["version"], self.catalog["version"])
        self.assertEqual(metadata["folderName"], metadata["skillName"])
        self.assertEqual(metadata["skillName"], "finance-suite")
        self.assertEqual(metadata["workflowCount"], len(self.catalog["skills"]))
        self.assertEqual(metadata["registrationCount"], 1)
        self.assertEqual(metadata["nativeStatus"], "not-validated")
        self.assertEqual(metadata["installationMode"], "extract-then-upload-folder")
        self.assertIn("Extract the ZIP", metadata["instructions"])
        self.assertIn("Upload Folder", metadata["instructions"])
        self.assertIn("Refresh", metadata["instructions"])
        self.assertIn("@finance-suite", metadata["instructions"])
        self.assertEqual(metadata["bytes"], len(payload))
        self.assertEqual(metadata["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(metadata["sourceSuiteSha256"], hashlib.sha256(
            self.outputs[Path(metadata["sourceSuitePath"])]).hexdigest())
        with zipfile.ZipFile(io.BytesIO(payload)) as packed:
            self.assertEqual(metadata["fileCount"], len(packed.namelist()))
            self.assertEqual([record["path"] for record in metadata["files"]], packed.namelist())
            self.assertTrue(all(name.endswith(".md") for name in packed.namelist()))
            for record in metadata["files"]:
                content = packed.read(record["path"])
                self.assertEqual(content, self.outputs[Path(record["sourcePath"])])
                self.assertEqual(record["bytes"], len(content))
                self.assertEqual(record["sha256"], hashlib.sha256(content).hexdigest())
        self.assertIn(build.EXCEL_FOLDER_BUNDLE.as_posix(), self.outputs[Path("SKILLS.md")].decode())

    def test_opt_in_preserves_existing_skill_and_package_formats(self):
        without = deepcopy(self.catalog)
        del without["excelFolderBundleVersion"]
        baseline = self.generate_catalog(without)
        self.assertNotIn(build.EXCEL_FOLDER_BUNDLE, baseline)
        self.assertNotIn(build.EXCEL_FOLDER_MANIFEST, baseline)
        for path, content in baseline.items():
            if path.parts[0] in {"editions", "packages", "profiles"}:
                self.assertEqual(content, self.outputs[path], path.as_posix())

    def test_invalid_or_incomplete_feature_selection_fails(self):
        for invalid in (None, True, False, 0, 2, 1.0, "1", [], {}):
            catalog = deepcopy(self.catalog)
            catalog["excelFolderBundleVersion"] = invalid
            with self.subTest(flag=invalid), self.assertRaisesRegex(ValueError, "Excel folder bundle version"):
                self.generate_catalog(catalog)
        for suite in (None, 1):
            catalog = deepcopy(self.catalog)
            if suite is None:
                del catalog["suitePackageVersion"]
            else:
                catalog["suitePackageVersion"] = suite
            with self.subTest(suite=suite), self.assertRaisesRegex(ValueError, "requires grouped suite"):
                self.generate_catalog(catalog)

    def test_partial_renamed_or_unsafe_source_folders_are_rejected(self):
        source = Path("editions/copilot-suite/finance-suite")
        relevant = {path: content for path, content in self.outputs.items()
                    if path.is_relative_to(source) or path == Path("packages/suites/finance-suite-copilot.zip")}
        missing = dict(relevant)
        del missing[source / "references/controls.md"]
        with self.assertRaisesRegex(ValueError, "unresolved local resource"):
            build.add_excel_folder_package(missing, self.catalog)
        wrong_name = dict(relevant)
        wrong_name[source / "SKILL.md"] = wrong_name[source / "SKILL.md"].replace(
            b"name: finance-suite\n", b"name: renamed-suite\n", 1)
        with self.assertRaisesRegex(ValueError, "invalid name"):
            build.add_excel_folder_package(wrong_name, self.catalog)
        for path in ("references/../outside.md", "references/CON.md", "references/con.md",
                     "references/file.md:stream", "references/file.md ", "manifest.json"):
            changed = dict(relevant)
            changed[source / path] = b"Unsafe companion.\n"
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "unsafe resource|reserved filename"):
                build.add_excel_folder_package(changed, self.catalog)
        changed = dict(relevant)
        changed[source / "references/controls.md"] += b"Unreviewed change.\n"
        with self.assertRaisesRegex(ValueError, "match the complete generated"):
            build.add_excel_folder_package(changed, self.catalog)


if __name__ == "__main__":
    unittest.main()
