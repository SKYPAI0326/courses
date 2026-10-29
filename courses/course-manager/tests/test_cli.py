import contextlib
import io
import os
import tempfile
import sys
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from manager import build_parser, main
from src.catalog import write_catalog
from src.discover import scan_workspace


class CliContractTests(unittest.TestCase):
    def test_registers_all_management_commands(self):
        parser = build_parser()
        argument_sets = (
            ["scan"],
            ["find", "ai"],
            ["inspect", "office-ai"],
            ["propose-new", "SQL Server"],
            ["propose-move", "source", "destination"],
            ["propose-merge", "source", "target"],
            ["verify"],
            ["apply", "proposal.json", "--approval", "approval.json"],
            ["rollback", "manifest.json", "--approval", "approval.json"],
        )

        for argv in argument_sets:
            namespace = parser.parse_args(argv)
            self.assertEqual(namespace.command, argv[0])

    def test_find_prints_copyable_absolute_path_and_open_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "workspace with spaces"
            project = root / "office-ai"
            project.mkdir(parents=True)
            (project / "README.md").write_text("Office AI course source\n", encoding="utf-8")
            state_root = Path(temporary) / "external-state"
            write_catalog(state_root / "registry" / "catalog.json", scan_workspace(root))
            output = io.StringIO()

            with contextlib.redirect_stdout(output):
                result = main([
                    "--root", str(root), "--state-root", str(state_root),
                    "find", "office-ai",
                ])

        self.assertEqual(result, 0)
        resolved_project = project.resolve()
        self.assertIn(f"PROJECT_PATH: {resolved_project}", output.getvalue())
        self.assertIn(f"OPEN_COMMAND: open '{resolved_project}'", output.getvalue())
        self.assertNotIn('"fingerprint"', output.getvalue())

    def test_find_json_contains_copyable_absolute_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "managed"
            root.mkdir()
            project = root / "office-ai"
            project.mkdir()
            (project / "README.md").write_text("Office AI course source\n", encoding="utf-8")
            state_root = Path(temporary) / "external-state"
            write_catalog(state_root / "registry" / "catalog.json", scan_workspace(root))
            output = io.StringIO()

            with contextlib.redirect_stdout(output):
                result = main([
                    "--root", str(root), "--state-root", str(state_root),
                    "find", "office-ai", "--json",
                ])

        self.assertEqual(result, 0)
        self.assertIn(f'"open_path": "{project.resolve()}"', output.getvalue())

    def test_inspect_includes_copyable_absolute_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "managed"
            root.mkdir()
            project = root / "office-ai"
            project.mkdir()
            (project / "README.md").write_text("Office AI course source\n", encoding="utf-8")
            output = io.StringIO()

            with contextlib.redirect_stdout(output):
                result = main([
                    "--root", str(root), "--state-root", str(Path(temporary) / "state"),
                    "inspect", "office-ai",
                ])

        self.assertEqual(result, 0)
        self.assertIn(f'"absolute_path": "{project.resolve()}"', output.getvalue())

    def test_scan_writes_catalog_and_report_only_to_external_state_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "arbitrary-managed-root"
            state = Path(temporary) / "runtime-state"
            (root / "demo").mkdir(parents=True)
            (root / "demo/README.md").write_text("demo\n", encoding="utf-8")
            output = io.StringIO()

            with contextlib.redirect_stdout(output):
                result = main([
                    "--root", str(root), "--state-root", str(state), "scan", "--write"
                ])

            self.assertEqual(result, 0)
            self.assertTrue((state / "registry/catalog.json").is_file())
            self.assertTrue(any((state / "reports/scans").glob("scan-*.md")))
            self.assertFalse((root / "course-manager").exists())

    def test_manager_rejects_state_overlap_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for root, state in (
                (base / "managed", base / "managed/runtime-state"),
                (base / "state/managed", base / "state"),
            ):
                with self.subTest(root=root, state=state):
                    (root / "demo").mkdir(parents=True, exist_ok=True)
                    with self.assertRaisesRegex(RuntimeError, "overlap"):
                        main([
                            "--root", str(root), "--state-root", str(state),
                            "scan", "--write",
                        ])
                    self.assertFalse((state / "registry/catalog.json").exists())

    def test_missing_workspace_or_state_configuration_fails_closed(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "COURSE_WEB_ROOT"):
                main(["scan"])


if __name__ == "__main__":
    unittest.main()
