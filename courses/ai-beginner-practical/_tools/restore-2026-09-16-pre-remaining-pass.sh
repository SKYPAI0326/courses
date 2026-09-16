#!/usr/bin/env bash
set -eu

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-16-pre-remaining-pass"

cp -p "$BACKUP_DIR/CH3-1.html" "$COURSE_DIR/CH3-1.html"
cp -p "$BACKUP_DIR/CH4-1.html" "$COURSE_DIR/CH4-1.html"

echo "Restored CH3-1 and CH4-1 remaining-pass snapshot."
