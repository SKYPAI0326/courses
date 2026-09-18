#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-14-pre-design-improvement"

for page in CH1-1.html CH2-1.html CH3-1.html CH4-1.html module1.html; do
  cp "$BACKUP_DIR/$page" "$COURSE_DIR/$page"
done

echo "Restored design-improvement backup: $BACKUP_DIR"
