#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COURSE_ROOT="${COURSE_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
GLOBAL_ROOT="${GLOBAL_ROOT:-$COURSE_ROOT/../../_lessons/gen-ai-36h}"
BACKUP_DIR="$COURSE_ROOT/_backup/2026-11-01-course-ai-workflow-pass2-before-fix"
restore() { mkdir -p "$(dirname "$2")"; cp "$BACKUP_DIR/$1" "$2"; }
restore 'part2/PRAC2.html' "$COURSE_ROOT/part2/PRAC2.html"
restore '_repair/2026-10-09/lesson-plans/PRAC2.md' "$COURSE_ROOT/_repair/2026-10-09/lesson-plans/PRAC2.md"
restore '_repair/2026-10-09/lesson-meta.json' "$COURSE_ROOT/_repair/2026-10-09/lesson-meta.json"
restore '_repair/2026-10-31/SCAN.md' "$COURSE_ROOT/_repair/2026-10-31/SCAN.md"
restore '_repair/2026-10-31/REPAIR-PLAN.md' "$COURSE_ROOT/_repair/2026-10-31/REPAIR-PLAN.md"
restore 'global-lessons/PRAC2.md' "$GLOBAL_ROOT/PRAC2.md"
restore 'global-lessons/CH2-3.md' "$GLOBAL_ROOT/CH2-3.md"
