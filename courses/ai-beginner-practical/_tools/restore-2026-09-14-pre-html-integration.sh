#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-14-pre-html-integration"

cp "$BACKUP_DIR/CH1-1.html" "$COURSE_DIR/CH1-1.html"
cp "$BACKUP_DIR/module1.html" "$COURSE_DIR/module1.html"

echo "Restored ai-beginner-practical navigation files from $BACKUP_DIR"
