#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COURSE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-14-pre-full-course-repair"

cp "$BACKUP_DIR/CH1-1.html" "$COURSE_DIR/CH1-1.html"
cp "$BACKUP_DIR/CH2-1.html" "$COURSE_DIR/CH2-1.html"
cp "$BACKUP_DIR/CH3-1.html" "$COURSE_DIR/CH3-1.html"
cp "$BACKUP_DIR/CH4-1.html" "$COURSE_DIR/CH4-1.html"
cp "$BACKUP_DIR/COURSE-BLUEPRINT.md" "$COURSE_DIR/COURSE-BLUEPRINT.md"

cp "$BACKUP_DIR/lessons/CH1-1-LESSON-PLAN.md" "$COURSE_DIR/CH1-1-LESSON-PLAN.md"
cp "$BACKUP_DIR/lessons/CH2-1-LESSON-PLAN.md" "$COURSE_DIR/CH2-1-LESSON-PLAN.md"
cp "$BACKUP_DIR/lessons/CH3-1-LESSON-PLAN.md" "$COURSE_DIR/CH3-1-LESSON-PLAN.md"
cp "$BACKUP_DIR/lessons/CH4-1-LESSON-PLAN.md" "$COURSE_DIR/CH4-1-LESSON-PLAN.md"

cp "$BACKUP_DIR/assets/worksheets/unit1-practice-sheet.md" "$COURSE_DIR/assets/worksheets/unit1-practice-sheet.md"
cp "$BACKUP_DIR/assets/worksheets/unit3-notebooklm-reading-pack.md" "$COURSE_DIR/assets/worksheets/unit3-notebooklm-reading-pack.md"
cp "$BACKUP_DIR/assets/templates/unit2-communication-scenarios.md" "$COURSE_DIR/assets/templates/unit2-communication-scenarios.md"

# These two files are introduced by this repair and did not exist in the backup.
rm -f "$COURSE_DIR/assets/datasets/unit4-air-conditioner-comparison.md"
rm -f "$COURSE_DIR/assets/worksheets/unit4-lifestyle-application-card.md"

echo "Restored pre-full-course-repair files from: $BACKUP_DIR"
