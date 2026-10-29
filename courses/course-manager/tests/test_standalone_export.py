import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = PROJECT_ROOT / "scripts/export_standalone.py"


class StandaloneExportTests(unittest.TestCase):
    def test_runtime_bytecode_does_not_change_package_integrity(self):
        from scripts.install_course_skill_foundation import tree_hash

        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            package.mkdir()
            (package / "SKILL.md").write_text("# Test\n", encoding="utf-8")
            (package / "scripts").mkdir()
            before = tree_hash(package)
            cache = package / "scripts" / "__pycache__"
            cache.mkdir(parents=True)
            (cache / "module.cpython-312.pyc").write_bytes(b"runtime-only")
            self.assertEqual(tree_hash(package), before)

    def test_export_is_an_independent_repo_and_clean_clone_verifies(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            exported = base / "course-design-system"
            completed = subprocess.run(
                [sys.executable, str(EXPORT_SCRIPT), "--destination", str(exported)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                Path(
                    subprocess.check_output(
                        ["git", "-C", str(exported), "rev-parse", "--show-toplevel"],
                        text=True,
                    ).strip()
                ),
                exported.resolve(),
            )
            self.assertFalse((exported / "courses").exists())
            self.assertFalse((exported / "operations").exists())
            self.assertFalse((exported / "reports").exists())
            self.assertFalse((exported / "registry/catalog.json").exists())
            manifest = json.loads((exported / "EXPORT-MANIFEST.json").read_text())
            self.assertEqual(manifest["schema_version"], 1)
            self.assertTrue(manifest["files"])

            clone = base / "clean-clone"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-local", str(exported), str(clone)],
                check=True,
            )
            verification = subprocess.run(
                [sys.executable, "scripts/install_course_skill_foundation.py", "--verify-source"],
                cwd=clone,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(verification.returncode, 0, verification.stderr)
            self.assertIn("verified", verification.stdout.lower())


if __name__ == "__main__":
    unittest.main()
