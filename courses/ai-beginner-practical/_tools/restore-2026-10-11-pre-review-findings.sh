#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
python3 - <<'PYRESTORE'
from pathlib import Path
import json, shutil
root=Path.cwd(); backup=root/'_backup/2026-10-11-pre-review-findings'
manifest=json.loads((backup/'manifest.json').read_text())
for name in manifest['originals']:
    shutil.copy2(backup/name,root/name)
for name in manifest['new_files']:
    (root/name).unlink(missing_ok=True)
print('Restored this repair only.')
PYRESTORE
