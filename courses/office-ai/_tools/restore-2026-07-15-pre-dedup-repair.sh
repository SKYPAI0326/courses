#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-07-15-pre-dedup-repair"

for chapter in ch1 ch2 ch3 ch4 ch5 ch6; do
  if [ -d "$BACKUP_DIR/$chapter" ]; then
    cp "$BACKUP_DIR/$chapter"/*.html "$COURSE_DIR/$chapter/"
  fi
done

echo "Restored office-ai pages from $BACKUP_DIR"
