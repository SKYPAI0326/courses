#!/usr/bin/env bash
set -euo pipefail
COURSE_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
BACKUP="$COURSE_ROOT/_backup/2026-10-06-full-content-rebuild-pre"
python3 - "$COURSE_ROOT" "$BACKUP" <<'PYRESTORE'
from pathlib import Path
import json, shutil, sys
root, backup = Path(sys.argv[1]), Path(sys.argv[2])
manifest=json.loads((backup/'manifest.json').read_text())
for row in manifest['files']:
    src=backup/row['path']; dst=root/row['path']
    if not src.is_file(): raise SystemExit(f"missing backup: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src,dst)
print(f"restored {len(manifest['files'])} files")
PYRESTORE
