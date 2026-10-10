#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$ROOT" <<'RESTORE'
import sys,json,shutil,hashlib
from pathlib import Path
root=Path(sys.argv[1]); b=root/'_backup/2026-10-11-pre-repair'
for item in json.loads((b/'manifest.json').read_text())['files']:
 src=b/'files'/item['path']; assert hashlib.sha256(src.read_bytes()).hexdigest()==item['sha256']
 dst=root/item['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
print('Restored backed-up files. Newly added review/practice files retained for audit.')
RESTORE
