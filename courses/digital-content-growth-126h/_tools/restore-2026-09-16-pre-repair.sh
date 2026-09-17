#!/bin/zsh
set -e

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-16-pre-repair/html"

cp "$BACKUP_DIR"/*.html "$COURSE_DIR/"
echo "Restored learner HTML from $BACKUP_DIR"
