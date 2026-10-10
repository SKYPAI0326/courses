#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
TASK_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
python3 - "$TASK_ROOT" <<'PYRESTORE'
from pathlib import Path
import shutil,json
r=Path(__import__("sys").argv[1]);b=r/"_backup/2026-10-11-pre-plain-language"
for f in json.loads((b/"manifest.json").read_text()):shutil.copy2(b/f,r/f)
print("Restored 14 scoped files; repair evidence retained.")
PYRESTORE
