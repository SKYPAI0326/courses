#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COURSE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-15-pre-repair"

for file in \
  module1.html \
  CH1-1.html \
  CH2-1.html \
  CH3-1.html \
  CH4-1.html \
  COURSE-OUTLINE.md \
  COURSE-BLUEPRINT.md \
  _gates.md \
  _plan.md \
  COVERAGE-LEDGER.md \
  _validation/status.jsonl \
  _validation/L1-L2-L3-static.txt
do
  mkdir -p "$(dirname "$COURSE_DIR/$file")"
  cp -p "$BACKUP_DIR/$file" "$COURSE_DIR/$file"
done

rm -f \
  "$COURSE_DIR/_validation/L0-generate.py" \
  "$COURSE_DIR/_validation/test_l0_contract.py" \
  "$COURSE_DIR/_validation/L0-truth-table.json" \
  "$COURSE_DIR/_validation/L0-air-conditioner-truth.txt" \
  "$COURSE_DIR/assets/worksheets/course-capstone-handoff.md"

echo "Restored files from $BACKUP_DIR"
