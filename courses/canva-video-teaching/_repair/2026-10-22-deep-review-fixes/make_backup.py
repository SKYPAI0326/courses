#!/usr/bin/env python3
"""Create the pre-repair backup with repo-relative paths and SHA-256 manifest."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = COURSE_DIR.parents[1]
BACKUP_ROOT = COURSE_DIR / "_backup/2026-10-22-deep-review-fixes-pre-repair"
TARGETS = [
    "_lessons/canva-video-teaching/CH2-1.md",
    "_lessons/canva-video-teaching/CH2-3.md",
    "courses/canva-video-teaching/ch2/CH2-1.html",
    "courses/canva-video-teaching/ch2/CH2-3.html",
    "courses/canva-video-teaching/search-index.json",
    "courses/canva-video-teaching/downloads/Canva完整操作步驟.txt",
    "courses/canva-video-teaching/downloads/canva-text-pack.zip",
    "courses/canva-video-teaching/downloads/canva-handouts-offline.zip",
    "courses/canva-video-teaching/_validation/continuity-artifact-inventory.json",
    "courses/canva-video-teaching/_validation/evidence.json",
    "courses/canva-video-teaching/_validation/FINAL-REPORT.md",
    "courses/canva-video-teaching/_validation/validation-result.json",
    "courses/canva-video-teaching/_validation/L5-evidence-manifest.json",
    "courses/canva-video-teaching/_gates.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if BACKUP_ROOT.exists():
        raise SystemExit(f"backup already exists: {BACKUP_ROOT}")

    records = []
    for relative in TARGETS:
        source = REPO_ROOT / relative
        if not source.is_file():
            raise SystemExit(f"missing backup target: {relative}")
        destination = BACKUP_ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        records.append({"path": relative, "sha256": sha256(source)})

    manifest = {
        "created_at": "2026-10-22T18:56:00+08:00",
        "repo_root": str(REPO_ROOT),
        "targets": records,
    }
    (BACKUP_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"backup ready: {len(records)} files")


if __name__ == "__main__":
    main()
