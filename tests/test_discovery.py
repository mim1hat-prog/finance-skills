"""Static discovery, safe rendering and explicit community-publication boundaries."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import copy
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import project_discovery
import release


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class DiscoveryTests(unittest.TestCase):
    def test_static_catalogue_has_every_skill_and_truthful_metadata(self):
        catalog = json.loads((ROOT / "catalog.json").read_text())
        outputs = project_discovery.generate(ROOT, catalog)
        self.assertEqual(outputs, project_discovery.generate(ROOT, catalog))
        text = outputs[Path("site/index.html")].decode()
        doc = Document(text)
        rows = [a for t, a in doc.tags if t == "article" and a.get("class") == "skill-row"]
        self.assertEqual(len(rows), len(catalog["skills"]))
        ids = [a["id"] for _, a in doc.tags if "id" in a]
        self.assertEqual(len(ids), len(set(ids)))
        links = {a["href"] for t, a in doc.tags if t == "a"}
        for row in catalog["skills"]:
            self.assertIn(f"skill-{row['name']}", ids)
            self.assertIn(f"../packages/copilot/{row['name']}.zip", links)
            self.assertIn(f"../editions/copilot/{row['name']}/SKILL.md", links)
        self.assertIn("../packages/markdown/finance-skills-markdown.zip", links)
        self.assertNotIn("{{", text)
        structured = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)[1])
        self.assertEqual(structured["@type"], "SoftwareSourceCode")
        self.assertEqual(structured["codeRepository"], catalog["repoUrl"])
        self.assertEqual(structured["version"], catalog["version"])
        self.assertNotIn("aggregateRating", structured)
        self.assertNotIn("review", structured)
        metadata = json.loads(outputs[Path("docs/PROJECT-METADATA.json")])
        self.assertIs(metadata["settingsApplied"], False)
        self.assertIsNone(metadata["publicSiteUrl"])
        self.assertFalse(any(t == "link" and a.get("rel") == "canonical" for t, a in doc.tags))

    def test_untrusted_catalogue_text_cannot_inject_markup_or_close_json_script(self):
        catalog = json.loads((ROOT / "catalog.json").read_text())
        catalog = copy.deepcopy(catalog)
        payload = '</script><img src=x onerror="bad()">&'
        for key in ("title", "summary", "category", "prompt"):
            catalog["skills"][0][key] = payload
        config = dict(project_discovery.profile(ROOT), title=payload, description=payload)
        with mock.patch.object(project_discovery, "profile", return_value=config):
            text = project_discovery.generate(ROOT, catalog)[Path("site/index.html")].decode()
        self.assertNotIn(payload, text)
        self.assertIn("&lt;/script&gt;", text)
        self.assertIn("\\u003c/script>", text)
        self.assertFalse(any(t == "img" and a.get("src") == "x" for t, a in Document(text).tags))

    def test_profile_rejects_unknown_claims_and_invalid_topics(self):
        good = project_discovery.profile(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tools").mkdir()
            for changes in ({"schemaVersion": True}, {"topics": ["Invalid Topic"]},
                            {"topics": ["finance", "finance"]}, {"topics": [f"topic-{i}" for i in range(21)]},
                            {"aggregateRating": 5}, {"description": "short"}):
                data = dict(good, **changes)
                (root / "tools/discovery-profile.json").write_text(json.dumps(data))
                with self.subTest(changes=changes), self.assertRaises(ValueError):
                    project_discovery.profile(root)

    def test_template_drift_and_invalid_version_fail(self):
        catalog = json.loads((ROOT / "catalog.json").read_text())
        with self.assertRaises(ValueError):
            project_discovery.generate(ROOT, dict(catalog, version="01.4.0"))
        original = Path.read_text
        template = ROOT / "site/index.template.html"
        def changed(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            return text.replace("{{SKILL_ROWS}}", "") if path == template else text
        with mock.patch.object(Path, "read_text", changed), self.assertRaisesRegex(ValueError, "placeholder"):
            project_discovery.generate(ROOT, catalog)

    def test_cli_refuses_linked_outputs_without_modifying_the_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "keep.txt"
            target.write_text("Preserve this existing file.")
            (root / "site").mkdir()
            (root / "site/index.html").symlink_to(target)
            for flag in ([], ["--check"]):
                with mock.patch.object(project_discovery, "ROOT", root), \
                     mock.patch.object(project_discovery, "generate", return_value={Path("site/index.html"): b"new"}), \
                     mock.patch.object(sys, "argv", ["project_discovery.py", *flag]), \
                     redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(project_discovery.main(), 1)
                self.assertEqual(target.read_text(), "Preserve this existing file.")

    def test_only_explicit_community_files_enter_public_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            allowed = {".github/ISSUE_TEMPLATE/bug_report.md", ".github/ISSUE_TEMPLATE/skill_request.md",
                       ".github/PULL_REQUEST_TEMPLATE.md"}
            for name in release.REQUIRED | allowed | {".github/extra.md", ".github/workflows/check.yml"}:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Public fixture\n")
            files = release.collect_project(root)
            self.assertEqual({name for name in files if name.startswith(".github/")}, allowed)
            for name in allowed:
                self.assertTrue(release.public_path(name))
            self.assertFalse(release.public_path(".github/extra.md"))
            self.assertFalse(release.public_path(".github/workflows/check.yml"))
            (root / ".github").rename(root / "unlisted")
            (root / ".github").symlink_to(root / "unlisted", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Linked parent"):
                release.collect_project(root)


if __name__ == "__main__":
    unittest.main()
