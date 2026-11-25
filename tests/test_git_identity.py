from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_git_identity as identity


def record(sha="a" * 40, author="123+fixture@users.noreply.github.com", committer="noreply@github.com"):
    return {"sha": sha, "author": {"name": "Private example name", "email": author},
            "committer": {"name": "Private example committer", "email": committer},
            "message": "Private example commit message"}


class IdentityGuardTests(unittest.TestCase):
    def test_both_github_response_shapes_and_public_bot_identity(self):
        git_data = record()
        rest_data = {"sha": "b" * 40, "commit": record(author="418+fixture[bot]@users.noreply.github.com"),
                     "author": {"login": "ignored-profile"}, "committer": None}
        result = identity.review_records([git_data, rest_data])
        self.assertTrue(result["ok"])
        self.assertEqual((result["commitCount"], result["identityCount"]), (2, 4))
        self.assertEqual(result["historyCompleteness"], "not-established-by-export")
        self.assertTrue(identity.review_records(git_data)["ok"])

    def test_private_invalid_or_lookalike_identities_fail_without_echoing_values(self):
        for address in ("controller@example.invalid", "fixture@users.noreply.github.com.attacker.invalid",
                        " name@users.noreply.github.com", "fixture@example.invalid@users.noreply.github.com",
                        "", None, 12):
            with self.subTest(kind=type(address).__name__):
                row = record(author=address)
                result = identity.review_records(row)
                self.assertFalse(result["ok"])
                self.assertEqual(result["findings"][0]["role"], "author")
                rendered = json.dumps(result)
                self.assertNotIn("Private example", rendered)
                self.assertNotIn("@", rendered)
        result = identity.review_records(record(committer="controller@example.invalid"))
        self.assertEqual(result["findings"][0]["role"], "committer")

    def test_invalid_missing_or_duplicate_records_cannot_inflate_coverage(self):
        result = identity.review_records([record(), record(), {"sha": "invalid-private-value"}, "private-value"])
        self.assertFalse(result["ok"])
        self.assertEqual(result["commitCount"], 1)
        self.assertEqual(result["identityCount"], 2)
        self.assertEqual(len(result["findings"]), 3)
        self.assertNotIn("private-value", json.dumps(result))
        self.assertFalse(identity.review_records({"sha": "a" * 40, "commit": None})["ok"])
        with self.assertRaisesRegex(identity.IdentityCheckError, "empty-commit-export"):
            identity.review_records([])

    def test_exports_stay_outside_project_and_errors_are_redacted(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "repo"
            root.mkdir()
            outside = base / "metadata.json"
            outside.write_text(json.dumps(record()), encoding="utf-8")
            self.assertTrue(identity.review_export(outside, project_root=root)["ok"])
            inside = root / "metadata.json"
            inside.write_text(outside.read_text(), encoding="utf-8")
            with self.assertRaisesRegex(identity.IdentityCheckError, "outside-project"):
                identity.review_export(inside, project_root=root)
            link = base / "metadata-link.json"
            link.symlink_to(outside)
            with self.assertRaisesRegex(identity.IdentityCheckError, "linked-export-refused"):
                identity.review_export(link, project_root=root)
            outside.write_text('invalid controller@example.invalid', encoding="utf-8")
            output = io.StringIO()
            with mock.patch.object(identity, "ROOT", root), redirect_stdout(output):
                self.assertEqual(identity.main(["--export", str(outside)]), 1)
            result = json.loads(output.getvalue())
            self.assertEqual(result["code"], "unreadable-commit-export")
            self.assertNotIn("controller", output.getvalue())
            self.assertNotIn(str(outside), output.getvalue())

    def test_real_local_history_and_missing_parent_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            def commit(email):
                subprocess.run(["git", "-C", str(root), "-c", "user.name=Fixture", "-c", "user.email=" + email,
                                "commit", "--allow-empty", "-qm", "Synthetic metadata check"], check=True, capture_output=True)
                return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            first = commit("123+fixture@users.noreply.github.com")
            clean = identity.review_local_history(root)
            self.assertTrue(clean["ok"])
            self.assertEqual(clean["historyCompleteness"], "all-local-refs-traversed")
            second = commit("controller@example.invalid")
            result = identity.review_local_history(root)
            self.assertFalse(result["ok"])
            self.assertEqual(result["commitCount"], 2)
            self.assertEqual(len(result["findings"]), 2)
            self.assertNotIn("@", json.dumps(result))
            shallow = root / ".git" / "shallow"
            shallow.write_text(second + "\n", encoding="ascii")
            with self.assertRaisesRegex(identity.IdentityCheckError, "incomplete-shallow-git-history"):
                identity.review_local_history(root)
            shallow.unlink()
            (root / ".git" / "objects" / first[:2] / first[2:]).unlink()
            with self.assertRaisesRegex(identity.IdentityCheckError, "incomplete-or-unreadable-git-history"):
                identity.review_local_history(root)

    def test_local_git_errors_never_emit_stderr(self):
        result = subprocess.CompletedProcess([], 128, stdout=b"", stderr=b"controller@example.invalid")
        with mock.patch.object(identity.subprocess, "run", return_value=result):
            with self.assertRaises(identity.IdentityCheckError) as caught:
                identity.review_local_history(ROOT)
        self.assertNotIn("controller", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
