import tempfile
import unittest
from pathlib import Path

from src.verify import check_local_links, iter_formal_html, verify_manifest, verify_workspace


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "formal-course").mkdir()
        (self.root / "formal-course" / "index.html").write_text(
            """<html><head><link href='../assets/style.css'></head>
            <body><a href='../missing.html'>missing</a>
            <img src='../assets/missing.png'><video poster='../assets/missing-poster.png'></video></body></html>""",
            encoding="utf-8",
        )
        (self.root / "formal-course" / "assets" / "templates").mkdir(parents=True)
        (self.root / "formal-course" / "assets" / "templates" / "reference.html").write_text(
            "<img src='missing-template.png'>\n", encoding="utf-8"
        )
        (self.root / "formal-course" / "_archive" / "legacy").mkdir(parents=True)
        (self.root / "formal-course" / "_archive" / "legacy" / "old.html").write_text(
            "<img src='missing-legacy.png'>\n", encoding="utf-8"
        )
        (self.root / "assets").mkdir()
        (self.root / "assets" / "style.css").write_text("body {}\n", encoding="utf-8")
        (self.root / "_backup" / "formal-course").mkdir(parents=True)
        (self.root / "_backup" / "formal-course" / "index.html").write_text(
            "<img src='../missing-snapshot.png'>\n", encoding="utf-8"
        )
        (self.root / "no-handout-project").mkdir()
        (self.root / "no-handout-project" / "README.md").write_text("source only\n", encoding="utf-8")
        (self.root / "course-manager").mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_formal_html_excludes_management_backup_and_no_handout(self):
        paths = [path.relative_to(self.root).as_posix() for path in iter_formal_html(self.root)]

        self.assertEqual(paths, ["formal-course/index.html"])

    def test_local_link_checker_accepts_existing_and_reports_missing_attributes(self):
        html_paths = iter_formal_html(self.root)

        issues = check_local_links(self.root, html_paths)

        self.assertEqual({issue["attribute"] for issue in issues}, {"href", "src", "poster"})
        self.assertTrue(all(issue["reason"] == "missing target" for issue in issues))

    def test_backup_snapshot_warning_does_not_block_formal_verification(self):
        report = verify_workspace(self.root)

        self.assertEqual(report["status"], "BLOCK")
        self.assertEqual(report["counts"]["formal_html"], 1)
        self.assertEqual(len(report["local_links"]), 3)
        self.assertGreaterEqual(report["counts"]["backup_warnings"], 1)
        self.assertNotIn("_backup/formal-course/index.html", report["formal_html"])

    def test_verify_detects_formal_html_count_change_from_baseline(self):
        report = verify_workspace(self.root, {"formal_html_count": 0})

        self.assertIn("formal HTML count changed", " ".join(report["unexpected_changes"]))
        self.assertEqual(report["status"], "BLOCK")

    def test_verify_manifest_detects_changed_destination_hash(self):
        destination = self.root / "archive" / "project" / "README.md"
        destination.parent.mkdir(parents=True)
        destination.write_text("changed\n", encoding="utf-8")
        manifest = {
            "verification_status": "APPLIED",
            "before": {"source": "source", "destination": "archive/project"},
            "after": {
                "destination_files": [
                    {"path": "archive/project/README.md", "bytes": 8, "sha256": "not-current"}
                ]
            },
        }

        report = verify_manifest(self.root, manifest)

        self.assertEqual(report["status"], "BLOCK")
        self.assertIn("archive/project/README.md", " ".join(report["unexpected_changes"]))


if __name__ == "__main__":
    unittest.main()
