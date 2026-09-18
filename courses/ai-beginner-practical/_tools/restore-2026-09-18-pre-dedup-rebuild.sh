#!/bin/zsh
set -e

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-18-pre-dedup-rebuild"

for file in \
  CH1-1.html \
  CH2-1.html \
  CH3-1.html \
  CH4-1.html \
  module1.html \
  COURSE-OUTLINE.md \
  COURSE-BLUEPRINT.md \
  COVERAGE-LEDGER.md \
  CH3-1-LESSON-PLAN.md \
  CH4-1-LESSON-PLAN.md; do
  cp "$BACKUP_DIR/$file" "$COURSE_DIR/$file"
done

echo "Restored pre-dedup-rebuild snapshot"
