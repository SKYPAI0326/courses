import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import install_course_skill_foundation as installer
from scripts.install_course_skill_foundation import (
    InstallError,
    _rollback_script,
    install,
    load_package_manifest,
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
        (self.packages_root / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "packages": [
                        {
                            "name": name,
                            "role": "core",
                            "entrypoint": "SKILL.md",
                            "baseline_hash": installer.tree_hash(
                                self.packages_root / name
                            ),
                        }
                        for name in PACKAGE_NAMES
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
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
            allow_updates=("course-run", "course-pm"),
        )

    def test_installer_reads_manifest_instead_of_hardcoded_tuple(self):
        manifest_path = self.packages_root / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["packages"] = [manifest["packages"][1]]
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        self.assertEqual(load_package_manifest(manifest_path), ("course-researcher",))
        result = install(
            self.packages_root,
            self.skills_root,
            self.operations_root,
            apply=False,
        )
        self.assertEqual([action.name for action in result.actions], ["course-researcher"])

    def test_identical_installed_package_is_unchanged_and_not_replaced(self):
        source = self.packages_root / "course-researcher"
        target = self.skills_root / "course-researcher"
        installer.shutil.copytree(source, target)
        inode_before = target.stat().st_ino

        result = self.apply_install()

        action = next(item for item in result.actions if item.name == "course-researcher")
        self.assertEqual(action.action, "UNCHANGED")
        self.assertEqual(target.stat().st_ino, inode_before)
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertNotIn(
            "course-researcher", {item["name"] for item in manifest["packages"]}
        )

    def test_changed_installed_package_requires_explicit_update_and_backup(self):
        before = self.snapshot(self.skills_root / "course-run")

        with self.assertRaises(InstallError):
            install(
                self.packages_root,
                self.skills_root,
                self.operations_root,
                apply=True,
            )

        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before)
        self.assertFalse(self.operations_root.exists())

        result = self.apply_install()
        self.assertEqual(
            self.snapshot(result.operation_dir / "backups" / "course-run"), before
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

    def test_rollback_preserves_post_install_user_edits(self):
        result = self.apply_install()
        changed = self.skills_root / "course-pm" / "SKILL.md"
        changed.write_text("使用者安裝後修改\n", encoding="utf-8")

        with self.assertRaises(InstallError):
            rollback_install(result.operation_dir)

        self.assertEqual(changed.read_text(encoding="utf-8"), "使用者安裝後修改\n")

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

    def test_committed_operation_rollbacks_match_current_generator(self):
        project_root = Path(__file__).resolve().parents[1]
        rollback_paths = sorted(
            (project_root / "operations" / "course-skill-foundation").glob(
                "*/rollback.py"
            )
        )

        self.assertTrue(rollback_paths)
        for rollback_path in rollback_paths:
            with self.subTest(rollback_path=rollback_path):
                self.assertEqual(
                    rollback_path.read_text(encoding="utf-8"), _rollback_script()
                )

    def test_preflight_rejects_existing_non_directory_target_without_changes(self):
        target = self.skills_root / "course-run"
        original = self.snapshot(target)
        for path in sorted(target.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        target.rmdir()
        target.write_bytes(b"existing-file\x00")

        with self.assertRaises(InstallError):
            self.apply_install()

        self.assertEqual(target.read_bytes(), b"existing-file\x00")
        self.assertFalse(self.operations_root.exists())
        self.assertIsNotNone(original)

    def test_preflight_rejects_dangling_symlink_without_changes(self):
        target = self.skills_root / "course-researcher"
        target.symlink_to(self.root / "missing-target", target_is_directory=True)
        before = self.snapshot(self.skills_root / "course-run")

        with self.assertRaises(InstallError):
            self.apply_install()

        self.assertTrue(target.is_symlink())
        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before)
        self.assertFalse(self.operations_root.exists())

    def test_install_restores_current_target_when_staged_replace_fails(self):
        before = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }
        real_replace = installer.os.replace

        def fail_staged_replace(source, destination):
            if Path(source).name == "staged" and Path(destination).name == "course-run":
                raise OSError("simulated staged replace failure")
            return real_replace(source, destination)

        with mock.patch.object(installer.os, "replace", side_effect=fail_staged_replace):
            with self.assertRaises(OSError):
                self.apply_install()

        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before["course-run"])
        self.assertEqual(self.snapshot(self.skills_root / "course-pm"), before["course-pm"])
        self.assertFalse((self.skills_root / "course-researcher").exists())

    def test_install_restores_all_targets_when_applied_manifest_write_fails(self):
        before = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }
        real_write = installer._write_json_atomic

        def fail_applied_manifest(path, value):
            if value.get("status") == "APPLIED":
                raise OSError("simulated manifest write failure")
            return real_write(path, value)

        with mock.patch.object(
            installer, "_write_json_atomic", side_effect=fail_applied_manifest
        ):
            with self.assertRaises(OSError):
                self.apply_install()

        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before["course-run"])
        self.assertEqual(self.snapshot(self.skills_root / "course-pm"), before["course-pm"])
        self.assertFalse((self.skills_root / "course-researcher").exists())

    def test_rollback_restores_installed_target_when_backup_copy_fails(self):
        result = self.apply_install()
        installed = {
            name: self.snapshot(self.skills_root / name) for name in PACKAGE_NAMES
        }
        real_copy = installer._copy_verified

        def fail_restore_copy(source, destination, expected_hash):
            if "backups" in Path(source).parts:
                raise OSError("simulated restore copy failure")
            return real_copy(source, destination, expected_hash)

        with mock.patch.object(
            installer, "_copy_verified", side_effect=fail_restore_copy
        ):
            with self.assertRaises(OSError):
                rollback_install(result.operation_dir)

        for name in PACKAGE_NAMES:
            self.assertEqual(self.snapshot(self.skills_root / name), installed[name])
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "APPLIED")

    def test_rollback_restores_installed_targets_when_manifest_write_fails(self):
        result = self.apply_install()
        installed = {
            name: self.snapshot(self.skills_root / name) for name in PACKAGE_NAMES
        }
        real_write = installer._write_json_atomic

        def fail_rolled_back_manifest(path, value):
            if value.get("status") == "ROLLED_BACK":
                raise OSError("simulated rollback manifest failure")
            return real_write(path, value)

        with mock.patch.object(
            installer, "_write_json_atomic", side_effect=fail_rolled_back_manifest
        ):
            with self.assertRaises(OSError):
                rollback_install(result.operation_dir)

        for name in PACKAGE_NAMES:
            self.assertEqual(self.snapshot(self.skills_root / name), installed[name])
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "APPLIED")


if __name__ == "__main__":
    unittest.main()
