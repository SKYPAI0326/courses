import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.install_course_skill_foundation import (
    InstallError,
    install,
    rollback_install,
)


PACKAGE_NAMES = ("course-run", "course-researcher", "course-pm")


class CourseSkillFoundationInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.packages_root = self.root / "packages"
        self.skills_root = self.root / "skills"
        self.operations_root = self.root / "operations"
        self.packages_root.mkdir()
        self.skills_root.mkdir()

        for name in PACKAGE_NAMES:
            package = self.packages_root / name
            (package / "references").mkdir(parents=True)
            (package / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Use when testing {name}.\n---\nnew {name}\n",
                encoding="utf-8",
            )
            (package / "references" / "contract.txt").write_bytes(
                f"new-{name}\n".encode("utf-8")
            )

        for name in ("course-run", "course-pm"):
            target = self.skills_root / name
            (target / "references").mkdir(parents=True)
            (target / "SKILL.md").write_text(f"old {name}\n", encoding="utf-8")
            (target / "references" / "legacy.bin").write_bytes(b"\x00old\r\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def snapshot(self, root):
        if not root.exists():
            return None
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def apply_install(self):
        return install(
            self.packages_root,
            self.skills_root,
            self.operations_root,
            apply=True,
        )

    def test_dry_run_does_not_write_skill_root(self):
        before = self.snapshot(self.skills_root)

        result = install(
            self.packages_root,
            self.skills_root,
            self.operations_root,
            apply=False,
        )

        self.assertFalse(result.applied)
        self.assertIsNone(result.operation_dir)
        self.assertEqual(self.snapshot(self.skills_root), before)
        self.assertFalse(self.operations_root.exists())
        self.assertEqual(
            [(action.name, action.action) for action in result.actions],
            [
                ("course-run", "UPDATE"),
                ("course-researcher", "ADD"),
                ("course-pm", "UPDATE"),
            ],
        )

    def test_apply_backs_up_existing_skills_before_replace(self):
        previous = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }

        result = self.apply_install()

        for name in ("course-run", "course-pm"):
            backup = result.operation_dir / "backups" / name
            self.assertEqual(self.snapshot(backup), previous[name])
        self.assertFalse(
            (result.operation_dir / "backups" / "course-researcher").exists()
        )

    def test_apply_installs_new_researcher_and_updates_existing_packages(self):
        self.apply_install()

        for name in PACKAGE_NAMES:
            self.assertEqual(
                self.snapshot(self.skills_root / name),
                self.snapshot(self.packages_root / name),
            )

    def test_manifest_records_before_and_after_hashes(self):
        result = self.apply_install()
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        packages = {item["name"]: item for item in manifest["packages"]}

        self.assertEqual(manifest["status"], "APPLIED")
        self.assertTrue(packages["course-run"]["before_exists"])
        self.assertIsNotNone(packages["course-run"]["before_hash"])
        self.assertIsNotNone(packages["course-run"]["after_hash"])
        self.assertFalse(packages["course-researcher"]["before_exists"])
        self.assertIsNone(packages["course-researcher"]["before_hash"])
        self.assertIsNotNone(packages["course-researcher"]["after_hash"])
        self.assertTrue((result.operation_dir / "rollback.py").is_file())

    def test_rollback_refuses_when_installed_files_changed_after_install(self):
        result = self.apply_install()
        changed = self.skills_root / "course-run" / "SKILL.md"
        changed.write_text("user changed this after install\n", encoding="utf-8")

        with self.assertRaises(InstallError):
            rollback_install(result.operation_dir)

        self.assertEqual(
            changed.read_text(encoding="utf-8"), "user changed this after install\n"
        )
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "APPLIED")

    def test_rollback_restores_exact_previous_bytes(self):
        before = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }
        result = self.apply_install()

        rollback_install(result.operation_dir)

        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before["course-run"])
        self.assertEqual(self.snapshot(self.skills_root / "course-pm"), before["course-pm"])
        self.assertFalse((self.skills_root / "course-researcher").exists())
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "ROLLED_BACK")

    def test_generated_rollback_is_self_contained(self):
        before = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }
        result = self.apply_install()
        manifest_path = result.operation_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["installer_path"] = str(self.root / "removed-worktree" / "installer.py")
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        process = subprocess.run(
            [sys.executable, str(result.operation_dir / "rollback.py")],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before["course-run"])
        self.assertEqual(self.snapshot(self.skills_root / "course-pm"), before["course-pm"])
        self.assertFalse((self.skills_root / "course-researcher").exists())


if __name__ == "__main__":
    unittest.main()
