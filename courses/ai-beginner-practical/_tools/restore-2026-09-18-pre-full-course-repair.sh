#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-18-pre-full-course-repair"

restore_file() {
  local backup_name="$1"
  local destination="$2"
  cp "$BACKUP_DIR/$backup_name" "$COURSE_DIR/$destination"
}

restore_file "CH1-1.html" "CH1-1.html"
restore_file "CH2-1.html" "CH2-1.html"
restore_file "CH3-1.html" "CH3-1.html"
restore_file "CH4-1.html" "CH4-1.html"
restore_file "CH1-1-LESSON-PLAN.md" "CH1-1-LESSON-PLAN.md"
restore_file "CH2-1-LESSON-PLAN.md" "CH2-1-LESSON-PLAN.md"
restore_file "CH3-1-LESSON-PLAN.md" "CH3-1-LESSON-PLAN.md"
restore_file "CH4-1-LESSON-PLAN.md" "CH4-1-LESSON-PLAN.md"
restore_file "COURSE-OUTLINE.md" "COURSE-OUTLINE.md"
restore_file "COURSE-BLUEPRINT.md" "COURSE-BLUEPRINT.md"
restore_file "COVERAGE-LEDGER.md" "COVERAGE-LEDGER.md"
restore_file "module1.html" "module1.html"
restore_file "index.html" "index.html"
restore_file "assets__worksheets__unit1-practice-sheet.md" "assets/worksheets/unit1-practice-sheet.md"
restore_file "assets__fallback__unit1-dialogue-simulator.md" "assets/fallback/unit1-dialogue-simulator.md"
restore_file "assets__templates__unit2-communication-scenarios.md" "assets/templates/unit2-communication-scenarios.md"
restore_file "assets__prompts__unit4-lifestyle-prompts.md" "assets/prompts/unit4-lifestyle-prompts.md"

echo "Restored 17 files from $BACKUP_DIR"
