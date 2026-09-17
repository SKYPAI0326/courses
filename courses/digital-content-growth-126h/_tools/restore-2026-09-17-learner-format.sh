#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-17-learner-format"

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "Backup directory not found: $BACKUP_DIR" >&2
  exit 1
fi

cp "$BACKUP_DIR"/*.html "$COURSE_DIR"/
cp "$BACKUP_DIR/course-shell.css" "$COURSE_DIR/assets/course-shell.css"
cp "$BACKUP_DIR/README.md" "$COURSE_DIR/assets/README.md"
cp "$BACKUP_DIR/test_learner_render_contract.py" "$COURSE_DIR/_tools/test_learner_render_contract.py"

echo "Restored learner-format batch from $BACKUP_DIR"
