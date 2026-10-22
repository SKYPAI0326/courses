#!/usr/bin/env python3
"""Restore the 2026-10-22 Deep Review repair targets.

Set RESTORE_REPO_ROOT to rehearse against an isolated copy.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[1]
BACKUP_ROOT = COURSE_DIR / "_backup/2026-10-22-deep-review-fixes-pre-repair"
DEFAULT_REPO_ROOT = COURSE_DIR.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    repo_root = Path(os.environ.get("RESTORE_REPO_ROOT", DEFAULT_REPO_ROOT)).resolve()
    manifest = json.loads((BACKUP_ROOT / "manifest.json").read_text(encoding="utf-8"))
    for record in manifest["targets"]:
        source = BACKUP_ROOT / record["path"]
        destination = repo_root / record["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        actual = sha256(destination)
        if actual != record["sha256"]:
            raise SystemExit(f"restore hash mismatch: {record['path']}")
    print(f"restored and verified: {len(manifest['targets'])} files")


if __name__ == "__main__":
    main()
