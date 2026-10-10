#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'RESTORE'
from pathlib import Path
import shutil,json
r=Path.cwd(); b=r/"_backup/2026-10-11-pre-step-by-step"
for name in json.loads((b/"manifest.json").read_text()):
 shutil.copy2(b/name,r/name)
for name in ['assets/workplace/tasks/ready-a.txt', 'assets/workplace/tasks/ready-b.txt', 'assets/workplace/tasks/ready-c.txt', 'assets/workplace/communication/email-client.txt', 'assets/workplace/communication/email-manager.txt', 'assets/workplace/communication/message.txt']:
 (r/name).unlink(missing_ok=True)
print("已還原本次範圍；其他檔案未更動。")
RESTORE
