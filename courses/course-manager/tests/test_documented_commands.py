import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DocumentedCommandTests(unittest.TestCase):
    def test_active_docs_never_advertise_the_removed_raw_pass_command(self):
        root = Path(__file__).resolve().parents[1]
        documents = [root / "README.md", *root.glob("docs/*.md")]
        documents.extend((root / "skill-packages").glob("*/**/*.md"))
        offenders = [
            str(path.relative_to(root))
            for path in documents
            if "course_contract.py pass" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])

    def test_documented_portable_verify_install_doctor_and_resume_commands_execute(self):
        root = Path(__file__).resolve().parents[1]
        docs = (root / "docs/course-skill-family-foundation.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "--verify-source",
            "--verify-installed",
            "--allow-update course-run",
            "scripts/course_run.py\" doctor",
            "scripts/course_run.py\" resume",
        ):
            self.assertIn(required, docs)

        with tempfile.TemporaryDirectory() as temporary:
            sandbox = Path(temporary)
            web = sandbox / "web"
            skills = sandbox / "skills"
            state = sandbox / "state"
            unrelated = sandbox / "cwd"
            for path in (web, skills, state, unrelated):
                path.mkdir()
            environment = {
                **os.environ,
                "HOME": str(sandbox / "clean-home"),
                "COURSE_DESIGN_SYSTEM_ROOT": str(root),
                "COURSE_WEB_ROOT": str(web),
                "SKILLS_ROOT": str(skills),
                "COURSE_DESIGN_STATE_ROOT": str(state),
            }

            commands = [
                [sys.executable, str(root / "scripts/install_course_skill_foundation.py"), "--verify-source"],
                [sys.executable, str(root / "scripts/install_course_skill_foundation.py"), "--apply", "--skills-root", str(skills)],
                [sys.executable, str(root / "scripts/install_course_skill_foundation.py"), "--verify-installed", "--skills-root", str(skills)],
                [sys.executable, str(root / "scripts/course_run.py"), "doctor"],
                [
                    sys.executable,
                    str(root / "scripts/course_contract.py"),
                    "init",
                    "--root",
                    str(web),
                    "--slug",
                    "documented-smoke",
                    "--title",
                    "Documented Smoke",
                    "--created-by",
                    "course-run",
                    "--at",
                    "2026-10-18T23:30:00+08:00",
                ],
                [
                    sys.executable,
                    str(root / "scripts/course_run.py"),
                    "resume",
                    "--contract",
                    str(web / "_design/documented-smoke/course-contract.json"),
                    "--actor",
                    "course-run",
                    "--at",
                    "2026-10-18T23:31:00+08:00",
                ],
            ]
            for command in commands:
                process = subprocess.run(
                    command,
                    cwd=unrelated,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)


if __name__ == "__main__":
    unittest.main()
