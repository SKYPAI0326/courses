import re
import tomllib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_version_matches_project_metadata(self):
        version = (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        metadata = tomllib.loads(
            (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["project"]["version"], version)
        self.assertEqual(metadata["project"]["requires-python"], ">=3.11")
        self.assertEqual(metadata["project"]["dependencies"], [])

    def test_ci_covers_supported_runtime_and_release_checks(self):
        workflow = (PROJECT_ROOT / ".github/workflows/verify.yml").read_text(
            encoding="utf-8"
        )
        for required in (
            "ubuntu-latest",
            "macos-latest",
            'python: "3.11"',
            'python: "3.12"',
            "unittest discover",
            "compileall",
            "--verify-source",
            "--verify-installed",
            "course_run.py doctor",
            "test_complete_course_flow",
            "test_standalone_export",
        ):
            with self.subTest(required=required):
                self.assertIn(required, workflow)
        self.assertIsNone(re.search(r"windows-latest", workflow, re.I))


if __name__ == "__main__":
    unittest.main()
