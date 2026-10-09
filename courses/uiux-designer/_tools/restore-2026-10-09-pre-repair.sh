#!/bin/bash
set -euo pipefail
course_root="$(cd "$(dirname "$0")/.." && pwd)"
site_root="$(cd "$course_root/../.." && pwd)"
python3 - "$course_root" "$site_root" <<'PY'
from pathlib import Path
import json, shutil, sys, hashlib
course, site = map(Path, sys.argv[1:])
backup = course / '_backup/2026-10-09-pre-repair'
manifest = json.loads((backup / 'manifest.json').read_text())
for item in manifest:
    src = backup / 'site' / item['path']
    assert hashlib.sha256(src.read_bytes()).hexdigest() == item['sha256'], item['path']
for item in manifest:
    dst = site / item['path']
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup / 'site' / item['path'], dst)
print(f"Restored {len(manifest)} original files. New repair files are retained for review.")
PY
