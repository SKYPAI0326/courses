import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


try:
    from src import runtime
except ImportError:
    runtime = None


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.system = self.root / "renamed-design-system"
        self.web = self.root / "managed-courses"
        self.skills = self.root / "agent-skills"
        self.state = self.root / "runtime-state"
        for path in (self.system, self.web, self.skills, self.state):
            path.mkdir()
        (self.system / "contracts").mkdir()
        (self.system / "src").mkdir()
        (self.system / "scripts").mkdir()
        (self.system / "skill-packages").mkdir()
        (self.system / "contracts/course-contract.schema.json").write_text("{}\n")
        (self.system / "scripts/course_contract.py").write_text("# fixture\n")
        self.environment = {
            "COURSE_DESIGN_SYSTEM_ROOT": str(self.system),
            "COURSE_WEB_ROOT": str(self.web),
            "SKILLS_ROOT": str(self.skills),
            "COURSE_DESIGN_STATE_ROOT": str(self.state),
        }

    def tearDown(self):
        self.temporary.cleanup()

    def require_runtime(self):
        self.assertIsNotNone(runtime, "src.runtime must provide the portable root contract")
        return runtime

    def test_resolves_four_explicit_roots_independent_of_cwd_and_home(self):
        module = self.require_runtime()
        unrelated = self.root / "unrelated-cwd"
        unrelated.mkdir()
        clean_home = self.root / "clean-home"
        clean_home.mkdir()
        with mock.patch.dict(os.environ, {**self.environment, "HOME": str(clean_home)}, clear=True):
            with mock.patch.object(Path, "cwd", return_value=unrelated):
                paths = module.resolve_runtime_paths()

        self.assertEqual(paths.design_system_root, self.system)
        self.assertEqual(paths.course_web_root, self.web)
        self.assertEqual(paths.skills_root, self.skills)
        self.assertEqual(paths.state_root, self.state)

    def test_missing_or_relative_required_root_fails_closed(self):
        module = self.require_runtime()
        for key in self.environment:
            with self.subTest(key=key):
                environment = dict(self.environment)
                del environment[key]
                with self.assertRaises(module.RuntimeConfigurationError):
                    module.resolve_runtime_paths(environment)

        environment = dict(self.environment)
        environment["COURSE_WEB_ROOT"] = "relative/course-root"
        with self.assertRaises(module.RuntimeConfigurationError):
            module.resolve_runtime_paths(environment)

    def test_state_root_must_be_external_and_roots_must_be_directories(self):
        module = self.require_runtime()
        environment = dict(self.environment)
        nested_state = self.system / "operations"
        nested_state.mkdir()
        environment["COURSE_DESIGN_STATE_ROOT"] = str(nested_state)
        with self.assertRaises(module.RuntimeConfigurationError):
            module.resolve_runtime_paths(environment)

        not_directory = self.root / "skills-file"
        not_directory.write_text("no\n")
        environment = dict(self.environment)
        environment["SKILLS_ROOT"] = str(not_directory)
        with self.assertRaises(module.RuntimeConfigurationError):
            module.resolve_runtime_paths(environment)

    def test_doctor_is_read_only_and_reports_ready_or_blocked(self):
        module = self.require_runtime()
        absent_state = self.root / "absent-state"
        environment = {**self.environment, "COURSE_DESIGN_STATE_ROOT": str(absent_state)}
        report = module.doctor(environment=environment, platform="linux")

        self.assertEqual(report["status"], "BLOCKED")
        self.assertFalse(absent_state.exists())
        self.assertEqual(report["checks"]["platform_lock"]["status"], "READY")
        self.assertEqual(report["checks"]["state_root"]["status"], "BLOCKED")

        windows = module.doctor(environment=self.environment, platform="win32")
        self.assertEqual(windows["status"], "BLOCKED")
        self.assertIn("unsupported", windows["checks"]["platform_lock"]["detail"].lower())

    def test_doctor_reports_invalid_root_topology_as_blocked(self):
        module = self.require_runtime()
        nested_state = self.system / "runtime-state"
        nested_state.mkdir()
        environment = {
            **self.environment,
            "COURSE_DESIGN_STATE_ROOT": str(nested_state),
        }

        report = module.doctor(environment=environment, platform="linux")

        self.assertEqual(report["status"], "BLOCKED")
        self.assertEqual(report["checks"]["root_topology"]["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
