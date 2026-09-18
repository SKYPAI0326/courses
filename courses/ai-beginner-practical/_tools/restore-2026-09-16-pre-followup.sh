#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-16-pre-followup"

for file in CH1-1.html CH2-1.html CH3-1.html CH4-1.html module1.html; do
  cp "$BACKUP_DIR/$file" "$COURSE_DIR/$file"
done
cp "$BACKUP_DIR/text-llm-minimum-start.md" "$COURSE_DIR/assets/fallback/text-llm-minimum-start.md"
cp "$BACKUP_DIR/unit1-practice-sheet.md" "$COURSE_DIR/assets/worksheets/unit1-practice-sheet.md"
cp "$BACKUP_DIR/test_cold_follow_contract.py" "$COURSE_DIR/_validation/test_cold_follow_contract.py"
echo "Restored ai-beginner-practical from $BACKUP_DIR"
