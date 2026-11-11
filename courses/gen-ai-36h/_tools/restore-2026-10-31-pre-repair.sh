#!/bin/bash
set -eu

COURSE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_ROOT="$COURSE_ROOT/_backup/2026-10-31-pre-repair"

if [ "${1:-}" = "--proof-root" ] && [ -n "${2:-}" ]; then
  MODE="proof"
  DEST_ROOT="$2"
elif [ "${1:-}" = "--apply" ]; then
  MODE="apply"
  DEST_ROOT=""
else
  echo "Usage: $0 --proof-root ISOLATED_ROOT | --apply" >&2
  exit 2
fi

python3 - "$COURSE_ROOT" "$BACKUP_ROOT" "$MODE" "$DEST_ROOT" <<'PY'
from pathlib import Path
import hashlib, json, shutil, sys

course_root = Path(sys.argv[1])
backup_root = Path(sys.argv[2])
mode = sys.argv[3]
dest_root = Path(sys.argv[4]) if sys.argv[4] else None
manifest = json.loads((backup_root / "MANIFEST.json").read_text())
prefix = Path("_backup/2026-10-31-pre-repair")

for item in manifest["files"]:
    backup = course_root / item["backup"]
    relative = Path(item["backup"]).relative_to(prefix)
    destination = Path(item["source"]) if mode == "apply" else dest_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup, destination)
    actual = hashlib.sha256(destination.read_bytes()).hexdigest()
    if actual != item["sha256"]:
        raise SystemExit(f"SHA-256 mismatch after restore: {destination}")

print(f"restored_and_verified={len(manifest['files'])}")
PY
