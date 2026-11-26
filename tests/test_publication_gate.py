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


def write_frozen_release(root, version, project_files, release_readme=b"Generic frozen release.\n"):
    """Create a small, genuinely integrity-verifiable release with invented content."""
    import release

    folder = root / "releases" / f"v{version}"
    folder.mkdir(parents=True)
    raw = f"https://raw.githubusercontent.com/example/finance-skills/main/releases/v{version}"
    files = {f"finance-skills-v{version}-{edition}.zip": zipped({"SKILL.md": b"# Synthetic workflow\n"})
             for edition in ("copilot", "gemini", "all")}
    files[f"finance-skills-v{version}-full.zip"] = zipped(project_files)
    files["README.md"] = release_readme
    manifest = {"schemaVersion": 1, "kind": "repository-hosted-release", "version": version,
                "repository": "https://github.com/example/finance-skills", "downloadRef": "main",
                "files": [dict(release.file_record(name, data), downloadUrl=f"{raw}/{name}")
                          for name, data in sorted(files.items())],
                "projectFiles": [release.file_record(name, data) for name, data in sorted(project_files.items())]}
    files["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    files["SHA256SUMS.txt"] = release.sums(files)
    for name, data in files.items():
        (folder / name).write_bytes(data)
    release.verify_frozen(folder)
    return {f"releases/v{version}/{name}": data for name, data in files.items()}


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


class HistoryPublicationGate(unittest.TestCase):
    def test_verified_releases_have_independent_unchanged_budgets_and_complete_coverage(self):
        import release

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {"README.md": b"Current generic instructions.\n"}
            snapshots = [write_frozen_release(root, f"1.{n}.0", {"README.md": b"x" * 20_000})
                         for n in range(1, 4)]
            for name, data in release.index_files(release.existing_versions(root / "releases")).items():
                (root / "releases" / name).write_bytes(data)
            current = dict(sources)
            current.update({f"releases/{name}": (root / "releases" / name).read_bytes()
                            for name in ("README.md", "latest.json")})
            expected_batches = [current, *reversed(snapshots)]
            independent = [scan_inventory(files) for files in expected_batches]
            budget = max(result["expandedBytes"] for result in independent) + 1
            all_files = {path: data for files in expected_batches for path, data in files.items()}
            self.assertGreater(sum(result["expandedBytes"] for result in independent), budget)
            with self.assertRaisesRegex(ValueError, "inspection limit exceeded"):
                scan_inventory(all_files, max_expanded_bytes=budget)
            original = check_publication._scan_inventory
            with mock.patch.object(check_publication, "_scan_inventory", wraps=original) as inspected:
                result = check_publication.scan_project(root, sources=sources, include_history=True,
                                                        max_expanded_bytes=budget)
            self.assertTrue(result["ok"])
            self.assertEqual(result["strategy"], "current-project-and-each-verified-release")
            self.assertEqual(result["batchCount"], 4)
            self.assertEqual(result["verifiedReleaseVersions"], ["1.3.0", "1.2.0", "1.1.0"])
            self.assertEqual(result["perBatchLimits"], {"maxExpandedBytes": budget, "maxFiles": 25_000,
                                                       "maxArchiveMembers": 5_000, "maxArchiveDepth": 5})
            self.assertEqual(result["topLevelFiles"], len(all_files))
            seen = [path for call in inspected.call_args_list for path in call.args[0]]
            self.assertEqual(len(seen), len(set(seen)))
            self.assertEqual(set(seen), set(all_files))
            self.assertEqual(set(inspected.call_args_list[0].args[0]), set(current))
            for key in ("files", "expandedBytes", "archives"):
                self.assertEqual(result[key], sum(entry[key] for entry in independent))
                self.assertEqual(result[key], sum(batch[key] for batch in result["batches"]))
            self.assertTrue(all(batch["expandedBytes"] <= budget for batch in result["batches"]))
            self.assertTrue(all(len(batch["inventorySha256"]) == 64 for batch in result["batches"]))

    def test_nested_frozen_content_uses_private_policy_and_exact_exceptions_in_every_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = "independently-invented-history-marker"
            fixture_path = "tests/test_synthetic.py"
            fixture = ("https://" + "dummy@api.example.invalid/").encode()
            exception = {"path": fixture_path, "sha256": hashlib.sha256(fixture).hexdigest(),
                         "code": "credential-in-url", "reason": "Invented invalid-URL fixture."}
            nested = zipped({"SKILL.md": marker.encode(), fixture_path: fixture})
            write_frozen_release(root, "1.0.0", {"packages/nested.zip": nested})
            write_frozen_release(root, "1.1.0", {"README.md": b"Later generic release.\n"})
            result = check_publication.scan_project(root, sources={fixture_path: fixture}, include_history=True,
                                                    private_literals=(marker,), exceptions=(exception,))
            self.assertFalse(result["ok"])
            self.assertEqual({finding["code"] for finding in result["findings"]}, {"private-review-marker"})
            self.assertTrue(any(finding["path"].startswith("releases/v1.0.0/")
                                and "!/packages/nested.zip!/SKILL.md" in finding["path"]
                                for finding in result["findings"]))
            self.assertNotIn(marker, json.dumps(result))
            self.assertEqual(result["reviewedSyntheticExceptionsUsed"], 1)
            self.assertEqual(sum(batch["reviewedSyntheticExceptionsUsed"] for batch in result["batches"]), 2)

    def test_one_release_over_budget_still_fails_with_its_batch_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_frozen_release(root, "1.0.0", {"README.md": b"Generic project.\n"},
                                 release_readme=b"x" * 5000)
            with self.assertRaisesRegex(ValueError, "batch release-v1.0.0: Publication inspection limit exceeded"):
                check_publication.scan_project(root, sources={"README.md": b"Current.\n"},
                                                include_history=True, max_expanded_bytes=4000)

    def test_unknown_release_entries_and_injected_prefixes_cannot_create_budget_batches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_frozen_release(root, "1.0.0", {"README.md": b"Generic project.\n"})
            for prefix in ("releases/v1.0.0/extra.md", "releases/v9.0.0/file.md", "Releases/v1.0.0/file.md",
                           "releases//v1.0.0/file.md", "releases/../file.md"):
                with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                    check_publication.scan_project(root, sources={prefix: b"Generic text.\n"}, include_history=True)
            for name, is_directory in (("unmatched.md", False), ("v1.0.0-extra", True), ("misc", True)):
                path = root / "releases" / name
                path.mkdir() if is_directory else path.write_text("Unexpected public text.\n")
                with self.subTest(entry=name), self.assertRaises(ValueError):
                    check_publication.scan_project(root, sources={"README.md": b"Current.\n"}, include_history=True)
                path.rmdir() if is_directory else path.unlink()
            extra = root / "releases/v1.0.0/unlisted.md"
            extra.write_text("Unlisted nested file.\n")
            with self.assertRaisesRegex(ValueError, "Unexpected or missing files"):
                check_publication.scan_project(root, sources={"README.md": b"Current.\n"}, include_history=True)

    def test_symlinks_and_post_verification_changes_are_rejected(self):
        import release

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_frozen_release(root, "1.0.0", {"README.md": b"Generic project.\n"})
            manifest = release.verify_frozen(root / "releases/v1.0.0")
            target = root / "releases/v1.0.0/README.md"
            target.write_text("Changed after verification.\n")
            with mock.patch.object(release, "existing_versions", return_value=[manifest]), \
                    self.assertRaisesRegex(ValueError, "bytes changed before inspection"):
                check_publication.scan_project(root, sources={"README.md": b"Current.\n"}, include_history=True)
            target.unlink()
            outside = root / "generic.txt"
            outside.write_text("Generic linked content.\n")
            target.symlink_to(outside)
            with self.assertRaises(ValueError):
                check_publication.scan_project(root, sources={"README.md": b"Current.\n"}, include_history=True)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "releases").symlink_to(root / "missing-directory", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Linked releases directory"):
                check_publication.scan_project(root, sources={"README.md": b"Current.\n"}, include_history=True)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            actual = base / "actual"
            actual.mkdir()
            linked = base / "project"
            linked.symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "project root must be a regular directory"):
                check_publication.scan_project(linked, sources={"README.md": b"Current.\n"}, include_history=True)

    def test_no_history_retains_the_single_inventory_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "releases").mkdir()
            (root / "releases/unreviewed.md").write_text("Not requested for this source-only scan.\n")
            sources = {"README.md": b"Generic current project.\n"}
            self.assertEqual(check_publication.scan_project(root, sources=sources), scan_inventory(sources))
            self.assertEqual(check_publication.scan_project(root, sources=sources, include_history=False),
                             scan_inventory(sources))
            with self.assertRaises(ValueError):
                check_publication.scan_project(root, sources=sources, include_history=True)

    def test_history_cli_uses_the_shared_verified_release_route(self):
        import release

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            (root / "tools").mkdir()
            (root / "tools/publication-policy.json").write_text(json.dumps(
                {"schemaVersion": 1, "reviewedOn": "2026-11-26", "reviewedSyntheticTests": []}))
            marker = "independently-invented-cli-history-marker"
            private = Path(directory) / "private-policy.json"
            private.write_text(json.dumps([marker]))
            write_frozen_release(root, "1.0.0", {"README.md": marker.encode()})
            with mock.patch.object(check_publication, "ROOT", root), \
                    mock.patch.object(sys, "argv", ["check_publication.py", "--history", "--private-policy", str(private)]), \
                    mock.patch.object(release, "collect_project", return_value={"README.md": b"Generic current project."}), \
                    mock.patch("builtins.print") as output:
                self.assertEqual(check_publication.main(), 1)
            result = json.loads(output.call_args.args[0])
            self.assertEqual(result["batchCount"], 2)
            self.assertFalse(result["ok"])
            self.assertEqual(result["perBatchLimits"]["maxExpandedBytes"], 200_000_000)
            self.assertNotIn(marker, json.dumps(result))


if __name__ == "__main__":
    unittest.main()
