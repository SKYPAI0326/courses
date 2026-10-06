#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
course_root="$(cd -- "$script_dir/.." && pwd)"
if [[ $# -gt 1 ]]; then
  echo "usage: $0 [course-root]" >&2
  exit 2
fi
if [[ $# -eq 1 ]]; then
  course_root="$(cd -- "$1" && pwd)"
fi
backup_root="$course_root/_backup/2026-10-06-re-review/files"
manifest="$course_root/_backup/2026-10-06-re-review/manifest.json"
python3 - "$course_root" "$backup_root" "$manifest" <<'PY'
from pathlib import Path, PurePosixPath
import hashlib, json, shutil, sys
root, backup_root, manifest_path = map(Path, sys.argv[1:])
manifest=json.loads(manifest_path.read_text())
files=manifest.get('files')
if not isinstance(files,list) or not files:
    raise SystemExit('refusing empty or invalid manifest')
if manifest.get('file_count') != len(files):
    raise SystemExit('manifest file_count mismatch')
validated=[]
seen=set()
for item in files:
    rel=item.get('path','')
    posix=PurePosixPath(rel)
    if not rel or posix.is_absolute() or '..' in posix.parts or rel in seen:
        raise SystemExit(f'refusing unsafe or duplicate path: {rel!r}')
    seen.add(rel)
    src=backup_root.joinpath(*posix.parts)
    if not src.is_file(): raise SystemExit(f'missing backup: {rel}')
    raw=src.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=item.get('sha256') or len(raw)!=item.get('bytes'):
        raise SystemExit(f'backup checksum/size mismatch: {rel}')
    dst=root.joinpath(*posix.parts)
    if not dst.resolve().is_relative_to(root.resolve()):
        raise SystemExit(f'refusing destination outside course root: {rel}')
    validated.append((src,dst))
for src,dst in validated:
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)
print(f'restored {len(validated)} files from verified backup')
PY
