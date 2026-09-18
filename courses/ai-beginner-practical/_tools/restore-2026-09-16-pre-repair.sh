#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-16-pre-repair"

cp "$BACKUP_DIR/index.html" "$COURSE_DIR/index.html"
cp "$BACKUP_DIR/module1.html" "$COURSE_DIR/module1.html"
cp "$BACKUP_DIR/CH1-1.html" "$COURSE_DIR/CH1-1.html"
cp "$BACKUP_DIR/CH2-1.html" "$COURSE_DIR/CH2-1.html"
cp "$BACKUP_DIR/CH3-1.html" "$COURSE_DIR/CH3-1.html"
cp "$BACKUP_DIR/CH4-1.html" "$COURSE_DIR/CH4-1.html"
cp "$BACKUP_DIR/assets/fallback/unit3-notebooklm-text-fallback.md" "$COURSE_DIR/assets/fallback/unit3-notebooklm-text-fallback.md"
cp "$BACKUP_DIR/assets/worksheets/course-capstone-handoff.md" "$COURSE_DIR/assets/worksheets/course-capstone-handoff.md"

echo "Restored 2026-09-16 pre-repair course files."
