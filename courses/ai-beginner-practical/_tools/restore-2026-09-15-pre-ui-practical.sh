#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-15-pre-ui-practical"

for file in index.html module1.html CH1-1.html CH2-1.html CH3-1.html CH4-1.html; do
  cp "$BACKUP_DIR/$file" "$COURSE_DIR/$file"
done
cp "$BACKUP_DIR/layout-redesign.css" "$COURSE_DIR/assets/layout-redesign.css"
printf '%s\n' "Restored UI/practicality repair backup: $BACKUP_DIR"
