import tempfile
import unittest
from pathlib import Path

from src.catalog import file_sha256, relative_posix
from src.discover import scan_workspace


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._write("formal-course/index.html", "<h1>Formal</h1>")
        self._write("formal-course/CH1-1.html", "<h1>Lesson</h1>")
        self._write("source-only/COURSE-OUTLINE.md", "# Source Course\n")
        self._write("no-handout-project/README.md", "A project without handouts\n")
        self._write("_backup/old/index.html", "<h1>Old</h1>")
        self._write("assets/shared/course-shell.css", "body { color: black; }\n")
        self._write("course-manager/README.md", "Management project\n")
        self._write(".worktrees/ignored-course/index.html", "<h1>Ignored</h1>\n")

        outside = self.root.parent / "course-manager-discovery-outside"
        outside.mkdir(exist_ok=True)
        (outside / "outside.txt").write_text("outside\n", encoding="utf-8")
        try:
            (self.root / "no-handout-project" / "external-link").symlink_to(outside)
        except OSError:
            self.skipTest("symlink creation is unavailable")

    def tearDown(self):
        outside = self.root.parent / "course-manager-discovery-outside"
        if outside.exists():
            (outside / "outside.txt").unlink(missing_ok=True)
            outside.rmdir()
        self.temp_dir.cleanup()

    def _write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _items(self):
        return {item["path"]: item for item in scan_workspace(self.root)["items"]}

    def test_classifies_formal_course_as_course_html(self):
        item = self._items()["formal-course"]
        self.assertEqual(item["kind"], "course-html")
        self.assertEqual(item["learner_html_count"], 2)
        self.assertEqual(item["risk"]["move"], "blocked-by-default")

    def test_classifies_source_only_project(self):
        item = self._items()["source-only"]
        self.assertEqual(item["kind"], "source-only")
        self.assertEqual(item["html_count"], 0)
        self.assertIn("COURSE-OUTLINE", item["search_terms"])

    def test_classifies_independent_non_html_project(self):
        item = self._items()["no-handout-project"]
        self.assertEqual(item["kind"], "no-handout-project")
        self.assertEqual(item["risk"]["move"], "requires-proposal")
        self.assertNotIn("external-link/outside.txt", item["fingerprint"]["files"])

    def test_classifies_support_and_management_items(self):
        items = self._items()
        self.assertEqual(items["_backup"]["kind"], "support")
        self.assertEqual(items["assets"]["kind"], "support")
        self.assertEqual(items["course-manager"]["kind"], "management")
        self.assertEqual(items["_backup"]["learner_html_count"], 0)
        self.assertNotIn(".worktrees", items)

    def test_fingerprint_counts_files_without_following_symlinked_directories(self):
        item = self._items()["no-handout-project"]
        self.assertEqual(item["fingerprint"]["file_count"], 1)
        self.assertEqual(len(item["fingerprint"]["files"]), 1)

    def test_paths_are_workspace_relative_posix_paths(self):
        catalog = scan_workspace(self.root)
        self.assertEqual(catalog["root"], ".")
        for item in catalog["items"]:
            self.assertEqual(item["path"], relative_posix(self.root / item["path"], self.root))
            self.assertNotIn("\\", item["path"])

    def test_file_sha256_is_stable(self):
        path = self.root / "formal-course" / "index.html"
        self.assertEqual(file_sha256(path), file_sha256(path))


if __name__ == "__main__":
    unittest.main()
