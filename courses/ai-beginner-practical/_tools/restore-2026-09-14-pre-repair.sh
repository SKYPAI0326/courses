#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-14-pre-repair"

cp "$BACKUP_DIR/CH1-1.html" "$COURSE_DIR/CH1-1.html"
cp "$BACKUP_DIR/module1.html" "$COURSE_DIR/module1.html"
cp "$BACKUP_DIR/unit1-practice-sheet.md" "$COURSE_DIR/assets/worksheets/unit1-practice-sheet.md"
cp "$BACKUP_DIR/unit1-dialogue-simulator.md" "$COURSE_DIR/assets/fallback/unit1-dialogue-simulator.md"

echo "Restored ai-beginner-practical files from $BACKUP_DIR"
