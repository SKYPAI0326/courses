#!/usr/bin/env python3
"""Check or restore only the files listed in this continuity-fix backup."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "_backup/2026-10-06-pre-continuity-fix"
MANIFEST = BACKUP / "manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--check", "--restore"}:
        print(f"Usage: {Path(sys.argv[0]).name} --check|--restore", file=sys.stderr)
        return 2
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for rel, expected in manifest["existing"].items():
        source = BACKUP / rel
        if not source.is_file() or digest(source) != expected:
            print(f"BACKUP_INVALID {rel}", file=sys.stderr)
            return 1
    if sys.argv[1] == "--check":
        print(f"BACKUP_OK files={len(manifest['existing'])} absent={len(manifest['absent_before_change'])}")
        return 0

    for rel in manifest["existing"]:
        source, target = BACKUP / rel, ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if digest(target) != manifest["existing"][rel]:
            print(f"RESTORE_CHECKSUM_MISMATCH {rel}", file=sys.stderr)
            return 1
    removed = 0
    for rel in manifest["absent_before_change"]:
        target = ROOT / rel
        if target.is_file():
            target.unlink()
            removed += 1
    print(f"RESTORE_OK files={len(manifest['existing'])} removed_new={removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
