"""Run: python3 -m unittest discover -s docs/tests -v"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "docs")]
from course_paths import is_public_html, iter_public_html

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="_course-scope-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.public = ["_unlock.html", "courses/demo/CH1.html", "courses/demo/_assets/demo.html"]
        self.internal = ["courses/demo/_backup/old.html", "courses/.worktrees/demo/CH1.html",
                         "node_modules/demo/a.html", "courses/demo/tmp/a.html",
                         "courses/output/a.html", "_規範/template.html", "courses/demo/_validation/a.html"]
        for rel in self.public + self.internal:
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("<html><body>fixture</body></html>")

    def test_root_relative_and_filename_policy(self):
        for rel in self.public:
            self.assertTrue(is_public_html(self.root / rel, self.root), rel)
        for rel in self.internal:
            self.assertFalse(is_public_html(self.root / rel, self.root), rel)

    def test_traversal_prunes_internals(self):
        self.assertEqual({str(p.relative_to(self.root)) for p in iter_public_html(self.root, self.root)}, set(self.public))
        self.assertEqual(list(iter_public_html(self.root / "courses/.worktrees", self.root)), [])

    def test_traversal_honors_gitignore_but_keeps_new_pages(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text(
            "courses/demo/generated/\n* 2.html\n", encoding="utf-8"
        )
        tracked = self.root / "courses/demo/CH1.html"
        untracked = self.root / "courses/demo/CH2.html"
        ignored_build = self.root / "courses/demo/generated/print-source.html"
        ignored_copy = self.root / "courses/demo/CH1 2.html"
        untracked.write_text("<html><body>new</body></html>", encoding="utf-8")
        ignored_build.parent.mkdir(parents=True, exist_ok=True)
        ignored_build.write_text("<html><body>generated</body></html>", encoding="utf-8")
        ignored_copy.write_text("<html><body>conflict</body></html>", encoding="utf-8")
        subprocess.run(["git", "add", ".gitignore", str(tracked.relative_to(self.root))],
                       cwd=self.root, check=True)

        found = {str(p.relative_to(self.root)) for p in iter_public_html(self.root, self.root)}
        self.assertIn("courses/demo/CH1.html", found)
        self.assertIn("courses/demo/CH2.html", found)
        self.assertNotIn("courses/demo/generated/print-source.html", found)
        self.assertNotIn("courses/demo/CH1 2.html", found)

    def test_sitemap_lastmod_uses_git_date_with_untracked_fallback(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.root, check=True)
        tracked = self.root / "courses/demo/CH1.html"
        subprocess.run(["git", "add", str(tracked.relative_to(self.root))],
                       cwd=self.root, check=True)
        commit_env = dict(os.environ, GIT_AUTHOR_DATE="2024-01-02T12:00:00+00:00",
                          GIT_COMMITTER_DATE="2024-01-02T12:00:00+00:00")
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.root,
                       env=commit_env, check=True)
        os.utime(tracked, (datetime(2025, 2, 3).timestamp(),) * 2)

        untracked = self.root / "courses/demo/CH2.html"
        untracked.write_text("<html><body>new</body></html>", encoding="utf-8")
        os.utime(untracked, (datetime(2025, 3, 4).timestamp(),) * 2)

        sitemap = load("stable_sitemap", ROOT / "docs/build-sitemap.py")
        sitemap.ROOT = self.root
        sitemap._GIT_LASTMOD_BY_PATH = None
        self.assertEqual(sitemap.file_lastmod(tracked), "2024-01-02")
        self.assertEqual(sitemap.file_lastmod(untracked), "2025-03-04")

    def test_outside_and_symlink_cannot_escape(self):
        self.assertFalse(is_public_html(self.root.parent / "outside.html", self.root))
        (self.root / "courses/demo/leak.html").symlink_to(self.root / "_規範/template.html")
        (self.root / "courses/demo/alias").symlink_to(self.root / "_規範", target_is_directory=True)
        self.assertEqual({str(p.relative_to(self.root)) for p in iter_public_html(self.root, self.root)}, set(self.public))

    def test_four_consumers_agree(self):
        lint = load("scope_lint", ROOT / "docs/lint-page.py")
        search = load("scope_search", ROOT / "docs/build-search-index.py")
        sitemap = load("scope_sitemap", ROOT / "docs/build-sitemap.py")
        gate = load("scope_gate", ROOT / "inject_gate.py")
        lint.ROOT = search.ROOT = sitemap.ROOT = self.root
        gate.BASE = self.root / "courses"
        for rel in self.public + self.internal:
            p = self.root / rel
            want = rel in self.public
            self.assertEqual(not lint.is_internal_page(p), want)
            self.assertEqual(not search.should_ignore(p), want)
            self.assertEqual(not sitemap.should_ignore(p), want)
            self.assertEqual(gate.is_public_course_html(p), want)

    def test_staged_unicode_paths(self):
        lint = load("scope_lint_unicode", ROOT / "docs/lint-page.py")
        lint.ROOT = self.root
        p = self.root / "courses/demo/中文.html"
        p.write_text("<body>test</body>")
        with patch.object(lint.subprocess, "check_output", return_value="courses/demo/中文.html\0") as command:
            self.assertEqual(lint.collect_files(SimpleNamespace(all=False, changed=True, paths=[])), [p])
            self.assertIn("-z", command.call_args.args[0])

    def test_gate_changes_only_public_fixture(self):
        gate = load("scope_gate_run", ROOT / "inject_gate.py")
        gate.BASE = self.root / "courses"
        gate.COURSES = {"demo": ("fixture-key", "0" * 64)}
        before = {rel:(self.root / rel).read_bytes() for rel in self.internal}
        gate.main()
        for rel, content in before.items():
            self.assertEqual((self.root / rel).read_bytes(), content)
        self.assertIn('id="_gate"', (self.root / "courses/demo/CH1.html").read_text())
        self.assertIn('id="_gate"', (self.root / "courses/demo/_assets/demo.html").read_text())

    def test_explicit_template_lint_not_worktree(self):
        lint = load("scope_lint_explicit", ROOT / "docs/lint-page.py")
        lint.ROOT = self.root
        args = SimpleNamespace(all=False, changed=False, paths=["_規範/template.html", "courses/.worktrees/demo/CH1.html"])
        self.assertEqual(lint.collect_files(args), [self.root / "_規範/template.html"])

if __name__ == "__main__":
    unittest.main()
