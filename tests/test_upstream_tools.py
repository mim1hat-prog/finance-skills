"""Source acquisition and update checks must remain bounded and non-executing."""

from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest import mock
import urllib.error
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import fetch_upstreams as fetch
import check_updates as updates

PIN = "a" * 40
ARCHIVE_ROOT = "example-" + PIN


def source_record(**changes):
    result = {
        "id": "example", "repository": "review/example",
        "commit": PIN, "archiveSha256": None,
    }
    result.update(changes)
    return result


def zip_bytes(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload, mode in entries:
            info = zipfile.ZipInfo(name)
            info.create_system = 3
            if mode is not None:
                info.external_attr = mode << 16
            archive.writestr(info, payload)
    return output.getvalue()


def fake_download(payload):
    def download(url, output, **kwargs):
        output.write_bytes(payload)
        return hashlib.sha256(payload).hexdigest()
    return download


class ArchiveValidationTests(unittest.TestCase):
    def validate(self, entries, **kwargs):
        with zipfile.ZipFile(io.BytesIO(zip_bytes(entries))) as archive:
            return fetch.validate_archive(archive, ARCHIVE_ROOT, **kwargs)

    def test_rejects_traversal_and_windows_unsafe_paths(self):
        paths = [
            "../escape.txt", "/absolute.txt", ARCHIVE_ROOT + "/../escape.txt",
            ARCHIVE_ROOT + r"/folder\escape.txt", ARCHIVE_ROOT + "/C:stream",
            ARCHIVE_ROOT + "/CON.txt", ARCHIVE_ROOT + "/trailing.",
            ARCHIVE_ROOT + "/space ", ARCHIVE_ROOT + "/.git/config",
            ARCHIVE_ROOT + "//empty.txt", ARCHIVE_ROOT + "/wild?.txt",
            ARCHIVE_ROOT + "/CONIN$",
        ]
        for path in paths:
            with self.subTest(path=path), self.assertRaises(fetch.SourceError):
                self.validate([(path, b"data", None)])

    def test_rejects_case_collisions_and_file_as_parent(self):
        for paths in [
            ["README.md", "readme.md"],
            ["parent", "parent/child.txt"],
        ]:
            with self.subTest(paths=paths), self.assertRaises(fetch.SourceError):
                self.validate([(ARCHIVE_ROOT + "/" + p, b"data", None) for p in paths])

    def test_rejects_symlinks_for_extraction(self):
        with self.assertRaisesRegex(fetch.SourceError, "symlink"):
            self.validate([(ARCHIVE_ROOT + "/link", b"../../outside", stat.S_IFLNK | 0o777)])

    def test_rejects_wrong_pin_root_and_expansion_limit(self):
        with self.assertRaisesRegex(fetch.SourceError, "root"):
            self.validate([("example-main/a.txt", b"data", None)])
        with self.assertRaisesRegex(fetch.SourceError, "expanded"):
            self.validate([(ARCHIVE_ROOT + "/a.txt", b"12345", None)], max_expanded_bytes=4)
        with self.assertRaisesRegex(fetch.SourceError, "file-size"):
            self.validate([(ARCHIVE_ROOT + "/a.txt", b"12345", None)], max_file_bytes=4)


class AcquisitionTests(unittest.TestCase):
    def test_extracts_exact_bytes_and_records_checksum_without_execution(self):
        payload = zip_bytes([
            (ARCHIVE_ROOT + "/SKILL.md", b"Review this source.", None),
            (ARCHIVE_ROOT + "/run.py", b"raise RuntimeError('must not run')\n", stat.S_IFREG | 0o755),
        ])
        digest = hashlib.sha256(payload).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            record = source_record(archiveSha256=digest)
            receipt = fetch.acquire_source(record, destination, download_fn=fake_download(payload))
            target = fetch.source_target(record, destination)
            self.assertEqual((target / "source/SKILL.md").read_bytes(), b"Review this source.")
            self.assertEqual(receipt["integrity"], "matched_reviewed_checksum")
            self.assertFalse(receipt["runtimeInstalled"])
            self.assertFalse(receipt["upstreamCodeExecuted"])
            self.assertEqual(json.loads((target / "SOURCE-RECEIPT.json").read_text()), receipt)

    def test_existing_target_is_never_overwritten_or_downloaded(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            record = source_record()
            target = fetch.source_target(record, destination)
            target.mkdir()
            marker = target / "keep.txt"
            marker.write_text("keep me")
            downloader = mock.Mock()
            with self.assertRaisesRegex(fetch.SourceError, "overwrite"):
                fetch.acquire_source(record, destination, download_fn=downloader)
            downloader.assert_not_called()
            self.assertEqual(marker.read_text(), "keep me")

    def test_hash_mismatch_and_unsafe_zip_leave_no_source_target(self):
        safe = zip_bytes([(ARCHIVE_ROOT + "/a.txt", b"data", None)])
        unsafe = zip_bytes([(ARCHIVE_ROOT + "/../outside.txt", b"data", None)])
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            for record, payload in [(source_record(archiveSha256="0" * 64), safe), (source_record(), unsafe)]:
                with self.subTest(record=record), self.assertRaises(fetch.SourceError):
                    fetch.acquire_source(record, destination, download_fn=fake_download(payload))
                self.assertFalse(fetch.source_target(record, destination).exists())
                self.assertFalse((destination / "outside.txt").exists())

    def test_archive_only_preserves_zip_without_creating_links(self):
        payload = zip_bytes([(ARCHIVE_ROOT + "/link", b"../../outside", stat.S_IFLNK | 0o777)])
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            record = source_record()
            receipt = fetch.acquire_source(
                record, destination, archive_only=True, download_fn=fake_download(payload)
            )
            target = fetch.source_target(record, destination)
            self.assertEqual((target / "source.zip").read_bytes(), payload)
            self.assertFalse((target / "source").exists())
            self.assertEqual(receipt["stage"], "source_archive_saved")
            self.assertEqual(receipt["unextractedSymlinkEntries"], 1)
            self.assertFalse(receipt["workPcHostActivated"])

    def test_destination_protects_public_repository_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            with self.assertRaises(fetch.SourceError):
                fetch.choose_destination(repo / "skills", repo)
            self.assertEqual(
                fetch.choose_destination(repo / "upstream-sources", repo),
                repo / "upstream-sources",
            )
            self.assertEqual(fetch.choose_destination(Path(directory) / "external", repo), Path(directory) / "external")


class UpdateReviewTests(unittest.TestCase):
    def test_new_head_is_a_review_need_not_compatibility(self):
        def reader(url, **kwargs):
            return json.dumps([{"sha": "b" * 40, "commit": {"message": "new change"}}]).encode(), {}
        result = updates.check_source(source_record(), timeout=1, reader=reader)
        self.assertEqual(result["status"], "new_commit_requires_review")
        self.assertFalse(result["compatibilityVerified"])
        self.assertEqual(result["reviewedCommit"], PIN)

    def test_rate_limit_is_reported_as_unavailable(self):
        def reader(url, **kwargs):
            raise urllib.error.HTTPError(
                url, 403, "Forbidden",
                {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1800000000"}, None,
            )
        result = updates.check_source(source_record(), timeout=1, reader=reader)
        self.assertEqual(result["status"], "unavailable")
        self.assertIn("rate limit exhausted", result["error"])
        self.assertIsNone(result["latestCommit"])

    def test_document_reachability_is_not_a_semantic_review(self):
        def reader(url, **kwargs):
            return b"<html>current documentation</html>", {"httpStatus": 200, "contentType": "text/html"}
        doc = {"id": "doc", "url": "https://learn.microsoft.com/example", "contentSha256": None}
        first = updates.check_document(doc, timeout=1, reader=reader)
        self.assertEqual(first["status"], "reachable_unbaselined")
        self.assertFalse(first["semanticReviewPerformed"])
        doc["contentSha256"] = "0" * 64
        changed = updates.check_document(doc, timeout=1, reader=reader)
        self.assertEqual(changed["status"], "changed_bytes_requires_review")

    def test_report_does_not_mutate_pins_and_protects_unrelated_files(self):
        lock = {"schemaVersion": 1, "reviewedOn": "2026-11-25", "sources": [source_record()], "documents": []}
        original = copy.deepcopy(lock)
        def reader(url, **kwargs):
            return json.dumps([{"sha": "b" * 40, "commit": {}}]).encode(), {}
        report = updates.collect_report(lock, timeout=1, reader=reader)
        self.assertEqual(lock, original)
        self.assertFalse(report["pinsChanged"])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            output.write_text('{"businessData":"keep"}')
            with self.assertRaisesRegex(fetch.SourceError, "Refusing"):
                updates.write_report(report, output)
            self.assertEqual(output.read_text(), '{"businessData":"keep"}')
            output.unlink()
            updates.write_report(report, output)
            updates.write_report(report, output)
            self.assertEqual(json.loads(output.read_text())["summary"]["newCommits"], 1)

    def test_network_url_policy_rejects_credentialed_or_unreviewed_hosts(self):
        for url in [
            "http://api.github.com/repos/x/y",
            "https://api.github.com.evil.example/repos/x/y",
            "https://secret@api.github.com/repos/x/y",
            "https://api.github.com:444/repos/x/y",
            "https://127.0.0.1/internal",
        ]:
            with self.subTest(url=url), self.assertRaises(fetch.SourceError):
                fetch.validate_https_url(url, {"api.github.com"})

    def test_real_lock_has_full_pins_and_requested_sources(self):
        lock = fetch.load_lock(ROOT / "upstream.lock.json")
        ids = {source["id"] for source in lock["sources"]}
        self.assertTrue(set(fetch.REQUESTED_TOOLS) <= ids)
        self.assertEqual(len(ids), len(lock["sources"]))
        for source in lock["sources"]:
            self.assertFalse(source["status"]["runtimeInstalledOnWorkPc"])

    def test_lock_refuses_floating_branch_and_duplicate_ids(self):
        for sources in [
            [source_record(commit="main")],
            [source_record(), source_record()],
            [source_record(archiveSha256="not-a-checksum")],
        ]:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "lock.json"
                path.write_text(json.dumps({"schemaVersion": 1, "sources": sources}))
                with self.subTest(sources=sources), self.assertRaises(fetch.SourceError):
                    fetch.load_lock(path)


if __name__ == "__main__":
    unittest.main()
