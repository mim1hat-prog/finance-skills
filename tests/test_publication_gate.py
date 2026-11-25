import io
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_publication import scan_inventory
import check_publication


def zipped(files):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return out.getvalue()


class PublicationGate(unittest.TestCase):
    def test_private_policy_cli_keeps_public_exception_policy_separate(self):
        import release
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory) / "private-policy.json"
            private.write_text('["independently-invented-cli-marker"]', encoding="utf-8")
            with mock.patch.object(sys, "argv", ["check_publication.py", "--private-policy", str(private)]), \
                    mock.patch.object(release, "collect_project", return_value={"README.md": b"Generic method"}), \
                    mock.patch("builtins.print"):
                self.assertEqual(check_publication.main(), 0)

    def test_reviewed_synthetic_exception_is_bound_to_exact_bytes_and_one_code(self):
        path = "tests/test_example.py"
        content = ("https://" + "dummy@api.example.invalid/").encode()
        record = {"path": path, "sha256": hashlib.sha256(content).hexdigest(), "code": "credential-in-url", "reason": "Invented invalid-URL fixture."}
        self.assertTrue(scan_inventory({path: content}, exceptions=(record,))["ok"])
        self.assertFalse(scan_inventory({path: content + b" changed"}, exceptions=(record,))["ok"])
        self.assertFalse(scan_inventory({"other.py": content}, exceptions=(record,))["ok"])
    def test_nested_native_packages_are_inspected_not_just_source(self):
        host = "tenant" + ".sharepoint.com"
        leaked = ("https://" + host + "/private-source").encode()
        package = zipped({"SKILL.md": leaked})
        release = zipped({"packages/skill.zip": package})
        result = scan_inventory({"full.zip": release})
        self.assertFalse(result["ok"])
        self.assertIn("private-enterprise-link", {x["code"] for x in result["findings"]})

    def test_office_caches_private_paths_and_opaque_files_block(self):
        result = scan_inventory({"assets/image.png": b"\x89PNG\xff", "examples/report.xlsx": b"fake", "private/input.csv": b"x\n1\n"})
        self.assertEqual({x["code"] for x in result["findings"]}, {"unreviewed-binary-artifact", "opaque-office-data-or-document", "private-or-runtime-path"})

    def test_keys_in_metadata_or_urls_are_not_echoed(self):
        secret = "synthetic" + "-secret-for-test"
        url = "https://api.example.invalid/data?" + "appId=" + secret
        result = scan_inventory({"metadata.json": json.dumps({"api" + "Key": secret, "source": url}).encode()})
        self.assertFalse(result["ok"])
        self.assertNotIn(secret, json.dumps(result))
        self.assertEqual({x["code"] for x in result["findings"]}, {"credential-value-in-json", "credential-query-parameter"})

    def test_private_policy_is_literal_and_not_a_public_default(self):
        marker = "example-sensitive-marker"
        result = scan_inventory({"notes.txt": marker.encode()}, private_literals=(marker,))
        self.assertFalse(result["ok"])
        self.assertNotIn(marker, json.dumps(result))
        self.assertTrue(scan_inventory({"notes.txt": b"generic synthetic method"})["ok"])

    def test_archive_traversal_duplicates_and_expansion_are_detected(self):
        self.assertFalse(scan_inventory({"bad.zip": zipped({"../escaped.txt": b"x"})})["ok"])
        result = scan_inventory({"big.zip": zipped({"large.txt": b"x" * 1000})}, max_expanded_bytes=2000)
        self.assertFalse(result["ok"])

    def test_public_provider_urls_and_local_usage_docs_are_allowed(self):
        content = b"https://data-api.ecb.europa.eu/service/data/EXR/example?startPeriod=2026-01-01\nhttp://127.0.0.1:8765/v1/datasets\n"
        self.assertTrue(scan_inventory({"docs/use.md": content})["ok"])


if __name__ == "__main__":
    unittest.main()
