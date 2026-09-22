#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_FILE="$COURSE_DIR/_backup/2026-09-22-pre-case-narrative/index.html"
TARGET_FILE="$COURSE_DIR/index.html"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Missing backup: $BACKUP_FILE" >&2
  exit 1
fi

cp -p "$BACKUP_FILE" "$TARGET_FILE"
printf 'Restored office-ai/index.html from 2026-09-22 pre-case-narrative backup.\n'
