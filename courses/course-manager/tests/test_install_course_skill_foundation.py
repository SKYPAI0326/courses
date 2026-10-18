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
    verify_installed_packages,
)

verify_source_packages = getattr(installer, "verify_source_packages", None)
recover_install = getattr(installer, "recover_install", None)


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

    def authorized_rollback(self, operation):
        return rollback_install(
            operation,
            packages_root=self.packages_root,
            skills_root=self.skills_root,
            operations_root=self.operations_root,
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

    def test_verify_installed_packages_matches_manifest_and_detects_drift(self):
        self.apply_install()

        verified = verify_installed_packages(
            self.packages_root, self.skills_root, PACKAGE_NAMES
        )
        self.assertEqual(set(verified), set(PACKAGE_NAMES))

        (self.skills_root / "course-run" / "SKILL.md").write_text(
            "drift after install\n", encoding="utf-8"
        )
        with self.assertRaises(InstallError):
            verify_installed_packages(
                self.packages_root, self.skills_root, PACKAGE_NAMES
            )

    def test_source_integrity_is_a_separate_verification_mode(self):
        self.assertIsNotNone(
            verify_source_packages,
            "installer must expose source-only integrity verification",
        )
        verified = verify_source_packages(self.packages_root, PACKAGE_NAMES)
        self.assertEqual(set(verified), set(PACKAGE_NAMES))

        (self.packages_root / "course-run" / "SKILL.md").write_text(
            "source drift\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(InstallError, "source differs"):
            verify_source_packages(self.packages_root, PACKAGE_NAMES)

    def test_installed_verification_does_not_require_source_trees(self):
        self.apply_install()
        for name in PACKAGE_NAMES:
            installer.shutil.rmtree(self.packages_root / name)

        verified = verify_installed_packages(
            self.packages_root, self.skills_root, PACKAGE_NAMES
        )
        self.assertEqual(set(verified), set(PACKAGE_NAMES))

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
            self.authorized_rollback(result.operation_dir)

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
            self.authorized_rollback(result.operation_dir)

        self.assertEqual(changed.read_text(encoding="utf-8"), "使用者安裝後修改\n")

    def test_rollback_restores_exact_previous_bytes(self):
        before = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }
        result = self.apply_install()

        self.authorized_rollback(result.operation_dir)

        self.assertEqual(self.snapshot(self.skills_root / "course-run"), before["course-run"])
        self.assertEqual(self.snapshot(self.skills_root / "course-pm"), before["course-pm"])
        self.assertFalse((self.skills_root / "course-researcher").exists())
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "ROLLED_BACK")

    def test_generated_rollback_uses_governed_authority(self):
        before = {
            name: self.snapshot(self.skills_root / name)
            for name in ("course-run", "course-pm")
        }
        result = self.apply_install()
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

    def test_applied_rollback_replays_real_process_exit_at_every_mutation_boundary(self):
        boundaries = {
            "container_create": 92,
            "target_move": 93,
            "restore_stage": 94,
            "before_restore": 95,
            "cross_package": 96,
            "cleanup": 97,
            "status_intent": 98,
            "status": 99,
        }
        project_root = Path(__file__).resolve().parents[1]
        crash_script = r'''
import os
import sys
from pathlib import Path
from scripts import install_course_skill_foundation as installer

boundary = sys.argv[1]
operation, packages, skills, operations = map(Path, sys.argv[2:6])
exit_codes = {
    "container_create": 92,
    "target_move": 93,
    "restore_stage": 94,
    "before_restore": 95,
    "cross_package": 96,
    "cleanup": 97,
    "status_intent": 98,
    "status": 99,
}

real_mkdir = installer.Path.mkdir
def crash_mkdir(path, *args, **kwargs):
    result = real_mkdir(path, *args, **kwargs)
    candidate = Path(path)
    if (
        boundary == "container_create"
        and candidate.parent == skills
        and candidate.name.startswith(".course-skill-recover-")
        and candidate.name.endswith("-course-run")
    ):
        os._exit(exit_codes[boundary])
    return result

real_replace = installer.os.replace
def crash_replace(source, destination):
    result = real_replace(source, destination)
    source = Path(source)
    destination = Path(destination)
    if boundary == "target_move" and source == skills / "course-run" and destination.name == "installed":
        os._exit(exit_codes[boundary])
    if boundary == "before_restore" and source.name == "restored" and destination == skills / "course-run":
        os._exit(exit_codes[boundary])
    if boundary == "cross_package" and source == skills / "course-researcher" and destination.name == "installed":
        os._exit(exit_codes[boundary])
    return result

real_copy = installer._copy_verified
def crash_copy(source, destination, expected_hash):
    result = real_copy(source, destination, expected_hash)
    if boundary == "restore_stage" and "backups" in Path(source).parts and Path(destination).name == "restored":
        os._exit(exit_codes[boundary])
    return result

real_rmtree = installer.shutil.rmtree
def crash_rmtree(path, *args, **kwargs):
    result = real_rmtree(path, *args, **kwargs)
    candidate = Path(path)
    if (
        boundary == "cleanup"
        and candidate.parent == skills
        and candidate.name.startswith(".course-skill-recover-")
        and candidate.name.endswith("-course-run")
    ):
        os._exit(exit_codes[boundary])
    return result

real_write = installer._write_json_atomic
def crash_write(path, value):
    result = real_write(path, value)
    if (
        boundary == "status_intent"
        and value.get("status") == "ROLLING_BACK"
        and value.get("rollback_phase") == "ROLLBACK_COMPLETE_INTENT"
    ):
        os._exit(exit_codes[boundary])
    if boundary == "status" and value.get("status") == "ROLLED_BACK":
        os._exit(exit_codes[boundary])
    return result

installer.Path.mkdir = crash_mkdir
installer.os.replace = crash_replace
installer._copy_verified = crash_copy
installer.shutil.rmtree = crash_rmtree
installer._write_json_atomic = crash_write
installer.rollback_install(
    operation,
    packages_root=packages,
    skills_root=skills,
    operations_root=operations,
)
'''

        for boundary, exit_code in boundaries.items():
            with self.subTest(boundary=boundary):
                case_root = self.root / f"rollback-{boundary}"
                packages = case_root / "packages"
                skills = case_root / "skills"
                operations = case_root / "operations"
                installer.shutil.copytree(self.packages_root, packages)
                installer.shutil.copytree(self.skills_root, skills)
                before = self.snapshot(skills)
                result = install(
                    packages,
                    skills,
                    operations,
                    apply=True,
                    allow_updates=("course-run", "course-pm"),
                )

                process = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        crash_script,
                        boundary,
                        str(result.operation_dir),
                        str(packages),
                        str(skills),
                        str(operations),
                    ],
                    cwd=project_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(process.returncode, exit_code, process.stderr)
                rollback_install(
                    result.operation_dir,
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                rollback_install(
                    result.operation_dir,
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                self.assertEqual(self.snapshot(skills), before)
                self.assertEqual(list(skills.glob(".course-skill-recover-*")), [])
                manifest = json.loads(
                    (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
                )
                self.assertEqual(manifest["status"], "ROLLED_BACK")
                self.assertTrue(
                    all(record["phase"] == "ROLLED_BACK" for record in manifest["packages"])
                )

    def test_applied_rollback_cli_and_generated_script_replay_rolled_back_operation(self):
        before = self.snapshot(self.skills_root)
        result = self.apply_install()
        self.authorized_rollback(result.operation_dir)

        cli = installer.main(
            [
                "--rollback-operation",
                str(result.operation_dir),
                "--packages-root",
                str(self.packages_root),
                "--skills-root",
                str(self.skills_root),
                "--operations-root",
                str(self.operations_root),
            ]
        )
        generated = subprocess.run(
            [sys.executable, str(result.operation_dir / "rollback.py")],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(cli, 0)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        self.assertEqual(self.snapshot(self.skills_root), before)

    def test_rolled_back_status_requires_verified_before_state_and_clean_records(self):
        result = self.apply_install()
        installed = self.snapshot(self.skills_root)
        manifest_path = result.operation_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["status"] = "ROLLED_BACK"
        manifest["rollback_phase"] = "ROLLED_BACK"
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(InstallError, "completed rollback"):
            self.authorized_rollback(result.operation_dir)

        self.assertEqual(self.snapshot(self.skills_root), installed)

    def test_applied_rollback_missing_intermediate_container_fails_closed(self):
        result = self.apply_install()
        project_root = Path(__file__).resolve().parents[1]
        crash_script = r'''
import os
import sys
from pathlib import Path
from scripts import install_course_skill_foundation as installer

operation, packages, skills, operations = map(Path, sys.argv[1:5])
real_replace = installer.os.replace
def crash_after_move(source, destination):
    result = real_replace(source, destination)
    if Path(source) == skills / "course-run" and Path(destination).name == "installed":
        os._exit(93)
    return result
installer.os.replace = crash_after_move
installer.rollback_install(
    operation,
    packages_root=packages,
    skills_root=skills,
    operations_root=operations,
)
'''
        process = subprocess.run(
            [
                sys.executable,
                "-c",
                crash_script,
                str(result.operation_dir),
                str(self.packages_root),
                str(self.skills_root),
                str(self.operations_root),
            ],
            cwd=project_root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 93, process.stderr)
        manifest_path = result.operation_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = next(item for item in manifest["packages"] if item["name"] == "course-run")
        container = Path(record["recovery_container"])
        installer.shutil.rmtree(container)
        victim = self.root / "rollback-unrelated"
        victim.mkdir()
        (victim / "keep.bin").write_bytes(b"unrelated exact bytes\x00")
        victim_before = self.snapshot(victim)

        with self.assertRaises(InstallError):
            self.authorized_rollback(result.operation_dir)

        self.assertEqual(self.snapshot(victim), victim_before)
        self.assertFalse((self.skills_root / "course-run").exists())

    def test_incomplete_applied_rollback_blocks_new_install(self):
        result = self.apply_install()
        real_replace = installer.os.replace

        def crash_after_move(source, destination):
            replaced = real_replace(source, destination)
            if (
                Path(source) == self.skills_root / "course-run"
                and Path(destination).name == "installed"
            ):
                raise SystemExit("crash after durable rollback target move")
            return replaced

        with mock.patch.object(installer.os, "replace", side_effect=crash_after_move):
            with self.assertRaises(SystemExit):
                self.authorized_rollback(result.operation_dir)

        with self.assertRaisesRegex(InstallError, "unfinished rollback"):
            self.apply_install()

    def test_generated_rollback_rejects_tampered_target_without_touching_victim(self):
        result = self.apply_install()
        victim = self.root / "rollback-victim"
        victim.mkdir()
        (victim / "keep.bin").write_bytes(b"victim must survive\x00")
        victim_before = self.snapshot(victim)
        manifest_path = result.operation_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = next(
            item for item in manifest["packages"] if item["name"] == "course-researcher"
        )
        record["target"] = str(victim)
        record["after_hash"] = installer.tree_hash(victim)
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

        process = subprocess.run(
            [sys.executable, str(result.operation_dir / "rollback.py")],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(self.snapshot(victim), victim_before)

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

    def test_preflight_rejects_symlink_skills_root_before_mutation(self):
        real_skills = self.root / "real-skills"
        self.skills_root.rename(real_skills)
        self.skills_root.symlink_to(real_skills, target_is_directory=True)

        with self.assertRaises(InstallError):
            self.apply_install()

        self.assertFalse(self.operations_root.exists())

    def test_preflight_rejects_symlink_inside_existing_target_tree(self):
        target = self.skills_root / "course-run"
        legacy = target / "references" / "legacy.bin"
        legacy.unlink()
        legacy.symlink_to(target / "SKILL.md")

        with self.assertRaisesRegex(InstallError, "symbolic"):
            self.apply_install()

        self.assertTrue(legacy.is_symlink())
        self.assertFalse(self.operations_root.exists())

    def test_roots_must_be_absolute_and_pairwise_non_overlapping(self):
        with self.assertRaisesRegex(InstallError, "absolute"):
            install(
                self.packages_root,
                self.skills_root,
                Path("relative-operations"),
                apply=False,
            )

        for operations_root in (
            self.packages_root / "operations",
            self.skills_root / "operations",
        ):
            with self.subTest(operations_root=operations_root):
                with self.assertRaisesRegex(InstallError, "overlap"):
                    install(
                        self.packages_root,
                        self.skills_root,
                        operations_root,
                        apply=False,
                    )

    def test_preflight_rejects_symlink_ancestor_and_repo_local_operations(self):
        real_parent = self.root / "real-parent"
        real_parent.mkdir()
        linked_parent = self.root / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        linked_skills = linked_parent / "skills"

        with self.assertRaisesRegex(InstallError, "symbolic"):
            install(
                self.packages_root,
                linked_skills,
                self.operations_root,
                apply=False,
            )

        project_root = Path(__file__).resolve().parents[1]
        external_skills = self.root / "external-skills"
        external_skills.mkdir()
        with self.assertRaisesRegex(InstallError, "repository"):
            install(
                project_root / "skill-packages",
                external_skills,
                project_root / ".runtime-state" / "operations",
                apply=False,
            )

    def test_apply_rejects_symlink_or_file_authority_directory_before_mutation(self):
        for kind in ("symlink", "file"):
            with self.subTest(kind=kind):
                case_root = self.root / f"authority-{kind}"
                skills = case_root / "skills"
                operations = case_root / "operations"
                installer.shutil.copytree(self.skills_root, skills)
                operations.mkdir(parents=True)
                authority = operations / ".authority"
                outside = case_root / "outside"
                outside.mkdir()
                if kind == "symlink":
                    authority.symlink_to(outside, target_is_directory=True)
                else:
                    authority.write_bytes(b"not a directory\x00")
                before = self.snapshot(skills)

                with self.assertRaises(InstallError):
                    install(
                        self.packages_root,
                        skills,
                        operations,
                        apply=True,
                        allow_updates=("course-run", "course-pm"),
                    )

                self.assertEqual(self.snapshot(skills), before)
                self.assertEqual(self.snapshot(outside), {})
                self.assertEqual(
                    [path for path in operations.iterdir() if path.name != ".authority"],
                    [],
                )

    def test_authority_directory_rename_race_fails_before_package_mutation(self):
        skills = self.root / "race-skills"
        operations = self.root / "race-operations"
        outside = self.root / "race-outside"
        installer.shutil.copytree(self.skills_root, skills)
        outside.mkdir()
        before = self.snapshot(skills)
        real_rename = installer.os.rename
        raced = False

        def rename_after_directory_swap(source, destination, *args, **kwargs):
            nonlocal raced
            if not raced and str(destination).endswith(".json"):
                raced = True
                authority = operations / ".authority"
                real_rename(authority, operations / ".authority-raced")
                authority.symlink_to(outside, target_is_directory=True)
            return real_rename(source, destination, *args, **kwargs)

        with mock.patch.object(
            installer.os, "rename", side_effect=rename_after_directory_swap
        ):
            with self.assertRaises(InstallError):
                install(
                    self.packages_root,
                    skills,
                    operations,
                    apply=True,
                    allow_updates=("course-run", "course-pm"),
                )

        self.assertTrue(raced)
        self.assertEqual(self.snapshot(skills), before)
        self.assertEqual(self.snapshot(outside), {})

    def test_verify_installed_rejects_symlink_inside_tree_even_if_hash_matches(self):
        self.apply_install()
        target = self.skills_root / "course-run"
        contract = target / "references" / "contract.txt"
        contract.unlink()
        contract.symlink_to(target / "SKILL.md")
        manifest_path = self.packages_root / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for record in manifest["packages"]:
            if record["name"] == "course-run":
                record["baseline_hash"] = installer.tree_hash(target)
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(InstallError, "symbolic"):
            verify_installed_packages(
                self.packages_root, self.skills_root, ("course-run",)
            )

    def _crashed_operation(self):
        operations = sorted(self.operations_root.iterdir())
        operation_dirs = [path for path in operations if path.name != ".authority"]
        self.assertEqual(len(operation_dirs), 1)
        return operation_dirs[0]

    def authorized_recover(self, operation, **kwargs):
        return recover_install(
            operation,
            packages_root=kwargs.get("packages_root", self.packages_root),
            skills_root=kwargs.get("skills_root", self.skills_root),
            operations_root=kwargs.get("operations_root", self.operations_root),
        )

    def _interrupt_after_installed_replace(
        self,
        *,
        package_name="course-run",
        packages_root=None,
        skills_root=None,
        operations_root=None,
    ):
        packages_root = packages_root or self.packages_root
        skills_root = skills_root or self.skills_root
        operations_root = operations_root or self.operations_root
        real_replace = installer.os.replace

        def crash_after_target(source, destination):
            result = real_replace(source, destination)
            if (
                Path(source).name == "staged"
                and Path(destination) == skills_root / package_name
            ):
                raise SystemExit("simulated process crash after target replace")
            return result

        with mock.patch.object(installer.os, "replace", side_effect=crash_after_target):
            with self.assertRaises(SystemExit):
                install(
                    packages_root,
                    skills_root,
                    operations_root,
                    apply=True,
                    allow_updates=("course-run", "course-pm"),
                )
        return next(
            path for path in operations_root.iterdir() if path.name != ".authority"
        )

    def test_recovery_rejects_manifest_authority_tampering_before_mutation(self):
        operation = self._interrupt_after_installed_replace(package_name="course-pm")
        manifest_path = operation / "manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        victim = self.root / "unrelated-victim"
        victim.mkdir()
        (victim / "keep.bin").write_bytes(b"exact victim bytes\x00\xff")
        victim_before = self.snapshot(victim)

        tamper_cases = {
            "target": lambda value: value["packages"][0].update(
                {"target": str(victim), "after_hash": installer.tree_hash(victim)}
            ),
            "after_hash": lambda value: value["packages"][0].update(
                {"after_hash": "0" * 64}
            ),
            "package_name": lambda value: value["packages"][0].update(
                {"name": "course-evil", "target": str(self.skills_root / "course-evil")}
            ),
            "operation_identity": lambda value: value.update(
                {"operation_id": "forged-operation"}
            ),
        }
        for label, tamper in tamper_cases.items():
            with self.subTest(label=label):
                changed = json.loads(json.dumps(original))
                tamper(changed)
                manifest_path.write_text(json.dumps(changed) + "\n", encoding="utf-8")
                with self.assertRaises(InstallError):
                    self.authorized_recover(operation)
                self.assertEqual(self.snapshot(victim), victim_before)

        manifest_path.write_text(json.dumps(original) + "\n", encoding="utf-8")
        wrong_skills = self.root / "wrong-skills"
        wrong_skills.mkdir()
        with self.assertRaises(InstallError):
            self.authorized_recover(operation, skills_root=wrong_skills)
        self.assertEqual(self.snapshot(victim), victim_before)

    def test_recovery_rejects_foreign_matching_prefix_temp_paths(self):
        for field, prefix in (
            ("container", ".course-skill-course-run-foreign"),
            ("recovery_container", ".course-skill-recover-course-run-foreign"),
        ):
            with self.subTest(field=field):
                case_root = self.root / f"foreign-{field}"
                packages = case_root / "packages"
                skills = case_root / "skills"
                operations = case_root / "operations"
                installer.shutil.copytree(self.packages_root, packages)
                installer.shutil.copytree(self.skills_root, skills)
                operation = self._interrupt_after_installed_replace(
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                foreign = skills / prefix
                foreign.mkdir()
                (foreign / "sentinel.bin").write_bytes(b"foreign exact bytes\x00")
                before = self.snapshot(foreign)
                manifest_path = operation / "manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                record = next(
                    item for item in manifest["packages"] if item["name"] == "course-run"
                )
                record[field] = str(foreign)
                manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

                with self.assertRaises(InstallError):
                    recover_install(
                        operation,
                        packages_root=packages,
                        skills_root=skills,
                        operations_root=operations,
                    )
                self.assertEqual(self.snapshot(foreign), before)

    def test_recovery_rejects_missing_or_swapped_temp_identity(self):
        operation = self._interrupt_after_installed_replace()
        manifest_path = operation / "manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        course_run = next(
            item for item in original["packages"] if item["name"] == "course-run"
        )
        course_pm = next(
            item for item in original["packages"] if item["name"] == "course-pm"
        )
        authority = json.loads(
            (
                self.operations_root
                / ".authority"
                / f"{operation.name}.json"
            ).read_text(encoding="utf-8")
        )
        authority_pm = next(
            item for item in authority["packages"] if item["name"] == "course-pm"
        )
        cases = {
            "missing": ("container", None),
            "install-swapped": ("container", course_pm["container"]),
            "recovery-swapped": (
                "recovery_container",
                authority_pm["recovery_container"],
            ),
        }
        for label, (field, value) in cases.items():
            with self.subTest(label=label):
                changed = json.loads(json.dumps(original))
                record = next(
                    item for item in changed["packages"] if item["name"] == "course-run"
                )
                record[field] = value
                manifest_path.write_text(json.dumps(changed) + "\n", encoding="utf-8")
                with self.assertRaises(InstallError):
                    self.authorized_recover(operation)

    def test_generated_rollback_rejects_foreign_temp_path(self):
        result = self.apply_install()
        foreign = self.skills_root / ".course-skill-course-run-foreign"
        foreign.mkdir()
        (foreign / "sentinel.bin").write_bytes(b"rollback foreign exact\x00")
        before = self.snapshot(foreign)
        manifest_path = result.operation_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = next(
            item for item in manifest["packages"] if item["name"] == "course-run"
        )
        record["container"] = str(foreign)
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

        process = subprocess.run(
            [sys.executable, str(result.operation_dir / "rollback.py")],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(self.snapshot(foreign), before)

    def test_recovery_rejects_missing_recovery_container_identity(self):
        operation = self._interrupt_after_installed_replace()
        manifest_path = operation / "manifest.json"
        real_write = installer._write_json_atomic

        def exit_after_recovery_intent(path, value):
            result = real_write(path, value)
            record = next(
                item
                for item in value.get("packages", [])
                if item.get("name") == "course-run"
            )
            if record.get("phase") == "RECOVERY_CREATE_INTENT":
                raise SystemExit("crash after recovery identity journal")
            return result

        with mock.patch.object(
            installer, "_write_json_atomic", side_effect=exit_after_recovery_intent
        ):
            with self.assertRaises(SystemExit):
                self.authorized_recover(operation)

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = next(
            item for item in manifest["packages"] if item["name"] == "course-run"
        )
        record["recovery_container"] = None
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(InstallError, "recovery identity"):
            self.authorized_recover(operation)

    def test_recovery_fails_closed_without_independent_authority(self):
        operation = self._interrupt_after_installed_replace()
        authority = self.operations_root / ".authority" / f"{operation.name}.json"
        authority_bytes = authority.read_bytes()
        authority.unlink()

        with self.assertRaisesRegex(InstallError, "authority"):
            self.authorized_recover(operation)

        authority.write_bytes(authority_bytes)
        authority.chmod(0o444)
        self.authorized_recover(operation)

    def test_recovery_replays_every_durable_boundary_and_cleans_containers(self):
        phases = (
            "RECOVERY_CREATE_INTENT",
            "RECOVERY_INTENT",
            "TARGET_QUARANTINE_INTENT",
            "TARGET_QUARANTINED",
            "RESTORE_INTENT",
            "TARGET_RESTORE_INTENT",
            "CLEANUP_INTENT",
            "RECOVERY_CONTAINER_CLEANED",
            "INSTALL_CONTAINER_CLEANUP_INTENT",
            "RECOVERED",
        )
        for phase in phases:
            with self.subTest(phase=phase):
                case_root = self.root / f"replay-{phase.lower()}"
                packages = case_root / "packages"
                skills = case_root / "skills"
                operations = case_root / "operations"
                installer.shutil.copytree(self.packages_root, packages)
                installer.shutil.copytree(self.skills_root, skills)
                before = self.snapshot(skills)
                operation = self._interrupt_after_installed_replace(
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                real_write = installer._write_json_atomic

                def exit_after_phase(path, value):
                    result = real_write(path, value)
                    course_run = next(
                        record
                        for record in value.get("packages", [])
                        if record.get("name") == "course-run"
                    )
                    if course_run.get("phase") == phase:
                        raise SystemExit(f"crash after {phase}")
                    return result

                with mock.patch.object(
                    installer, "_write_json_atomic", side_effect=exit_after_phase
                ):
                    with self.assertRaises(SystemExit):
                        recover_install(
                            operation,
                            packages_root=packages,
                            skills_root=skills,
                            operations_root=operations,
                        )

                recover_install(
                    operation,
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                recover_install(
                    operation,
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                self.assertEqual(self.snapshot(skills), before)
                self.assertEqual(list(skills.glob(".course-skill-recover-*")), [])

    def test_recovery_replays_after_process_exit_at_target_quarantined(self):
        before = self.snapshot(self.skills_root)
        operation = self._interrupt_after_installed_replace()
        project_root = Path(__file__).resolve().parents[1]
        script = """
import os
import sys
from pathlib import Path
from scripts import install_course_skill_foundation as installer

operation, packages, skills, operations = map(Path, sys.argv[1:5])
real_write = installer._write_json_atomic

def exit_after_quarantine(path, value):
    result = real_write(path, value)
    record = next(
        item for item in value.get("packages", [])
        if item.get("name") == "course-run"
    )
    if record.get("phase") == "TARGET_QUARANTINED":
        os._exit(92)
    return result

installer._write_json_atomic = exit_after_quarantine
installer.recover_install(
    operation,
    packages_root=packages,
    skills_root=skills,
    operations_root=operations,
)
"""
        process = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(operation),
                str(self.packages_root),
                str(self.skills_root),
                str(self.operations_root),
            ],
            cwd=project_root,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 92, process.stderr)
        manifest = json.loads((operation / "manifest.json").read_text(encoding="utf-8"))
        record = next(
            item for item in manifest["packages"] if item["name"] == "course-run"
        )
        self.assertEqual(record["phase"], "TARGET_QUARANTINED")
        self.authorized_recover(operation)
        self.authorized_recover(operation)
        self.assertEqual(self.snapshot(self.skills_root), before)
        self.assertEqual(list(self.skills_root.glob(".course-skill-recover-*")), [])

    def test_recovery_missing_or_tampered_quarantine_fails_closed(self):
        for mode in ("missing", "tampered"):
            with self.subTest(mode=mode):
                case_root = self.root / f"quarantine-{mode}"
                packages = case_root / "packages"
                skills = case_root / "skills"
                operations = case_root / "operations"
                installer.shutil.copytree(self.packages_root, packages)
                installer.shutil.copytree(self.skills_root, skills)
                operation = self._interrupt_after_installed_replace(
                    packages_root=packages,
                    skills_root=skills,
                    operations_root=operations,
                )
                real_write = installer._write_json_atomic

                def exit_after_quarantine(path, value):
                    result = real_write(path, value)
                    record = next(
                        item
                        for item in value.get("packages", [])
                        if item.get("name") == "course-run"
                    )
                    if record.get("phase") == "TARGET_QUARANTINED":
                        raise SystemExit("crash after quarantine")
                    return result

                with mock.patch.object(
                    installer, "_write_json_atomic", side_effect=exit_after_quarantine
                ):
                    with self.assertRaises(SystemExit):
                        recover_install(
                            operation,
                            packages_root=packages,
                            skills_root=skills,
                            operations_root=operations,
                        )

                manifest = json.loads(
                    (operation / "manifest.json").read_text(encoding="utf-8")
                )
                record = next(
                    item for item in manifest["packages"] if item["name"] == "course-run"
                )
                quarantine = Path(record["recovery_container"]) / "quarantined"
                if mode == "missing":
                    installer.shutil.rmtree(quarantine)
                else:
                    (quarantine / "SKILL.md").write_text(
                        "tampered quarantine\n", encoding="utf-8"
                    )

                with self.assertRaises(InstallError):
                    recover_install(
                        operation,
                        packages_root=packages,
                        skills_root=skills,
                        operations_root=operations,
                    )
                current = json.loads(
                    (operation / "manifest.json").read_text(encoding="utf-8")
                )
                self.assertEqual(current["status"], "EXECUTING")

    def test_recovery_handles_crash_after_previous_target_move(self):
        self.assertIsNotNone(recover_install)
        before = self.snapshot(self.skills_root)
        real_replace = installer.os.replace

        def crash_after_previous(source, destination):
            result = real_replace(source, destination)
            if (
                Path(source) == self.skills_root / "course-run"
                and Path(destination).name == "previous"
            ):
                raise SystemExit("simulated process crash after previous move")
            return result

        with mock.patch.object(installer.os, "replace", side_effect=crash_after_previous):
            with self.assertRaises(SystemExit):
                self.apply_install()

        operation = self._crashed_operation()
        manifest = json.loads((operation / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "EXECUTING")
        self.assertEqual(manifest["allowed_updates"], ["course-pm", "course-run"])
        self.authorized_recover(operation)
        self.assertEqual(self.snapshot(self.skills_root), before)

    def test_recovery_handles_crash_after_new_target_replace(self):
        self.assertIsNotNone(recover_install)
        before = self.snapshot(self.skills_root)
        real_replace = installer.os.replace

        def crash_after_target(source, destination):
            result = real_replace(source, destination)
            if (
                Path(source).name == "staged"
                and Path(destination) == self.skills_root / "course-researcher"
            ):
                raise SystemExit("simulated process crash after target replace")
            return result

        with mock.patch.object(installer.os, "replace", side_effect=crash_after_target):
            with self.assertRaises(SystemExit):
                self.apply_install()

        operation = self._crashed_operation()
        self.authorized_recover(operation)
        self.assertEqual(self.snapshot(self.skills_root), before)

    def test_recovery_survives_process_exit_after_new_target_replace(self):
        self.assertIsNotNone(recover_install)
        before = self.snapshot(self.skills_root)
        project_root = Path(__file__).resolve().parents[1]
        script = """
import os
import sys
from pathlib import Path
from scripts import install_course_skill_foundation as installer

packages_root, skills_root, operations_root = map(Path, sys.argv[1:4])
real_replace = installer.os.replace

def crash_after_replace(source, destination):
    result = real_replace(source, destination)
    if (
        Path(source).name == "staged"
        and Path(destination) == skills_root / "course-researcher"
    ):
        os._exit(91)
    return result

installer.os.replace = crash_after_replace
installer.install(
    packages_root,
    skills_root,
    operations_root,
    apply=True,
    allow_updates=("course-run", "course-pm"),
)
"""
        process = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(self.packages_root),
                str(self.skills_root),
                str(self.operations_root),
            ],
            cwd=project_root,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(process.returncode, 91, process.stderr)
        operation = self._crashed_operation()
        manifest = json.loads((operation / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "EXECUTING")
        self.authorized_recover(operation)
        self.assertEqual(self.snapshot(self.skills_root), before)

    def test_recovery_accepts_prepared_manifest_before_first_swap(self):
        self.assertIsNotNone(recover_install)
        before = self.snapshot(self.skills_root)
        real_copy = installer._copy_verified

        def crash_before_first_swap(source, destination, expected_hash):
            if Path(destination).name == "staged":
                raise SystemExit("simulated process crash while staging")
            return real_copy(source, destination, expected_hash)

        with mock.patch.object(
            installer, "_copy_verified", side_effect=crash_before_first_swap
        ):
            with self.assertRaises(SystemExit):
                self.apply_install()

        operation = self._crashed_operation()
        manifest = json.loads((operation / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "PREPARED")
        self.assertEqual(
            installer.main(
                [
                    "--recover-operation",
                    str(operation),
                    "--packages-root",
                    str(self.packages_root),
                    "--skills-root",
                    str(self.skills_root),
                    "--operations-root",
                    str(self.operations_root),
                ]
            ),
            0,
        )
        self.assertEqual(self.snapshot(self.skills_root), before)

    def test_unfinished_apply_blocks_resume_until_rollback_recovers_it(self):
        real_copy = installer._copy_verified

        def crash_before_first_swap(source, destination, expected_hash):
            if Path(destination).name == "staged":
                raise SystemExit("simulated process crash while staging")
            return real_copy(source, destination, expected_hash)

        with mock.patch.object(
            installer, "_copy_verified", side_effect=crash_before_first_swap
        ):
            with self.assertRaises(SystemExit):
                self.apply_install()

        operation = self._crashed_operation()
        with self.assertRaisesRegex(InstallError, "unfinished install"):
            self.apply_install()

        self.authorized_rollback(operation)
        resumed = self.apply_install()
        self.assertTrue(resumed.applied)

    def test_manifest_failure_before_current_swap_does_not_leave_partial_install(self):
        before = self.snapshot(self.skills_root)
        real_copy = installer._copy_verified

        def fail_second_source_copy(source, destination, expected_hash):
            if Path(source).name == "course-researcher" and Path(destination).name == "staged":
                raise OSError("simulated current-item copy failure")
            return real_copy(source, destination, expected_hash)

        with mock.patch.object(installer, "_copy_verified", side_effect=fail_second_source_copy):
            with self.assertRaises(OSError):
                self.apply_install()

        self.assertEqual(self.snapshot(self.skills_root), before)

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
                self.authorized_rollback(result.operation_dir)

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
                self.authorized_rollback(result.operation_dir)

        for name in PACKAGE_NAMES:
            self.assertEqual(self.snapshot(self.skills_root / name), installed[name])
        manifest = json.loads(
            (result.operation_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "APPLIED")


if __name__ == "__main__":
    unittest.main()
