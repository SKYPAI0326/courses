#!/bin/bash
set -eu
course_root="$(cd "$(dirname "$0")/.." && pwd)"
backup_dir="$course_root/_backup/2026-10-09-pre-readability"
python3 - "$course_root" "$backup_dir" "${1:---dry-run}" <<'PYRESTORE'
from pathlib import Path
import sys,shutil,json
root,backup,mode=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
if mode not in ['--dry-run','--apply']:raise SystemExit('Use --dry-run or --apply')
manifest=json.loads((root/'_repair/2026-10-09-readability/baseline.json').read_text())
for name in manifest['files']:
 src,dst=backup/name,root/name
 if not src.is_file():raise SystemExit('Missing backup: '+name)
 if mode=='--apply':shutil.copy2(src,dst)
 print(('restore ' if mode=='--apply' else 'would restore ')+name)
for name in manifest['new_files']:
 dst=root/name
 if mode=='--apply' and dst.exists():dst.unlink()
 print(('remove ' if mode=='--apply' else 'would remove ')+name)
PYRESTORE
