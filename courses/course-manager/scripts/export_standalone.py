#!/usr/bin/env python3
"""Export the course design system as an independent, auditable Git repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_ANYWHERE = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}
EXCLUDED_TOP_LEVEL = {
    "operations",
    "reports",
    "runtime",
    "backups",
}
EXCLUDED_FILES = {
    Path("registry/catalog.json"),
    Path("EXPORT-MANIFEST.json"),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _included(relative: Path) -> bool:
    return (
        relative not in EXCLUDED_FILES
        and relative.parts[0] not in EXCLUDED_TOP_LEVEL
        and not any(part in EXCLUDED_ANYWHERE for part in relative.parts)
        and relative.suffix != ".pyc"
    )


def export_standalone(destination: Path) -> Path:
    destination = destination.absolute()
    if destination.exists():
        if not destination.is_dir() or any(destination.iterdir()):
            raise ValueError("destination must be absent or empty")
    else:
        destination.mkdir(parents=True)
    if destination == SOURCE_ROOT or SOURCE_ROOT in destination.parents:
        raise ValueError("destination must be outside the source tree")

    exported: list[dict[str, str]] = []
    for source in sorted(SOURCE_ROOT.rglob("*")):
        relative = source.relative_to(SOURCE_ROOT)
        if not _included(relative) or source.is_symlink() or not source.is_file():
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        exported.append({"path": relative.as_posix(), "sha256": _sha256(target)})
    manifest = {
        "schema_version": 1,
        "artifact": "course-design-system",
        "source_boundary": "courses/course-manager only",
        "excludes_learner_courses": True,
        "files": exported,
    }
    (destination / "EXPORT-MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q", "-b", "main", str(destination)], check=True)
    subprocess.run(["git", "-C", str(destination), "add", "."], check=True)
    subprocess.run(
        [
            "git", "-C", str(destination),
            "-c", "user.name=Course Design System Export",
            "-c", "user.email=course-design-system@example.invalid",
            "commit", "-q", "-m", "export: standalone course design system",
        ],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "fsck", "--full", "--strict"],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = export_standalone(args.destination)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
