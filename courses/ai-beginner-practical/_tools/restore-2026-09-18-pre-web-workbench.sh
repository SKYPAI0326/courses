#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-18-pre-web-workbench"

cp "$BACKUP/CH1-1.html" "$ROOT/CH1-1.html"
cp "$BACKUP/CH1-1-LESSON-PLAN.md" "$ROOT/CH1-1-LESSON-PLAN.md"
cp "$BACKUP/COURSE-BLUEPRINT.md" "$ROOT/COURSE-BLUEPRINT.md"
cp "$BACKUP/COVERAGE-LEDGER.md" "$ROOT/COVERAGE-LEDGER.md"
cp "$BACKUP/test_cold_follow_contract.py" "$ROOT/_validation/test_cold_follow_contract.py"
cp "$BACKUP/test_ui_practicality_contract.py" "$ROOT/_validation/test_ui_practicality_contract.py"
rm -f "$ROOT/_validation/test_workbench_contract.py"

echo "Restored CH1-1 web workbench repair baseline."
