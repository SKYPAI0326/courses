#!/usr/bin/env bash
set -eu

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-16-pre-content-substance"

cp -p "$BACKUP_DIR/CH1-1.html" "$COURSE_DIR/CH1-1.html"
cp -p "$BACKUP_DIR/CH1-1-LESSON-PLAN.md" "$COURSE_DIR/CH1-1-LESSON-PLAN.md"
cp -p "$BACKUP_DIR/COVERAGE-LEDGER.md" "$COURSE_DIR/COVERAGE-LEDGER.md"
cp -p "$BACKUP_DIR/CH2-1.html" "$COURSE_DIR/CH2-1.html"

echo "Restored CH1-1 content substance repair snapshot."
