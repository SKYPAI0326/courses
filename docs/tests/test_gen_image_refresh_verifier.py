"""Regression coverage for the gen-image legacy image migration verifier."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFIER = REPO_ROOT / "courses/gen-image/_tools/verify-image-refresh.py"


class GenImageRefreshVerifierTest(unittest.TestCase):
    def test_accepts_valid_post_migration_versioned_assets(self) -> None:
        """A valid later SVG must not invalidate the closed 59-asset migration."""

        result = subprocess.run(
            [sys.executable, str(VERIFIER)],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("59 assets", result.stdout)
        self.assertIn("0 legacy references", result.stdout)


if __name__ == "__main__":
    unittest.main()
