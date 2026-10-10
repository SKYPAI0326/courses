#!/bin/bash
set -euo pipefail
course_dir="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$course_dir" <<'PY'
from pathlib import Path
import hashlib,json,shutil,sys
root=Path(sys.argv[1]); base=root.parents[1]; backup=root/'_backup/2026-10-11-pre-repair'
m=json.loads((backup/'manifest.json').read_text())
for row in m['files']:
 p=backup/'site'/row['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
for row in m['files']:
 dst=base/row['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(backup/'site'/row['path'],dst)
print('已還原',len(m['files']),'個修復前檔案；新增檔保留，清單見manifest.json。')
PY
