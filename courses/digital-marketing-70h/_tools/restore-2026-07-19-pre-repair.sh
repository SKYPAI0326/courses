#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-07-19-pre-repair"

for file in \
  m2c-1-text.html \
  m3-2-audience.html \
  m3-4-positioning.html \
  m4-1-attention.html \
  m4-3-shortform.html \
  m5-4-onpage.html \
  m8-2-copywriting.html \
  m9-2-email-psychology.html \
  m9-3-lead-magnet.html \
  m10-1-kickoff.html \
  m10-2-strategy.html \
  m10-3-execution.html \
  m10-4-presentation.html
do
  test -f "$BACKUP_DIR/$file"
  cp "$BACKUP_DIR/$file" "$COURSE_DIR/$file"
done

echo "Restored 13 course pages from $BACKUP_DIR"
