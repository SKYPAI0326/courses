#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-07-15-pre-repair"

FILES='
ch1/CH1-1.html
ch1/CH1-2.html
ch1/CH1-3.html
ch1/CH1-4.html
ch2/CH2-1.html
ch2/CH2-2.html
ch2/CH2-3.html
ch3/CH3-1.html
ch3/CH3-2.html
ch3/CH3-3.html
ch4/CH4-1.html
ch4/CH4-2.html
ch4/CH4-3.html
ch5/CH5-1.html
ch5/CH5-2.html
ch5/CH5-3.html
ch6/CH6-1.html
ch6/CH6-2.html
ch6/CH6-3.html
'

for relative_path in $FILES; do
  if [ ! -f "$BACKUP_DIR/$relative_path" ]; then
    echo "Missing backup: $BACKUP_DIR/$relative_path" >&2
    exit 1
  fi
done

for relative_path in $FILES; do
  cp -p "$BACKUP_DIR/$relative_path" "$COURSE_DIR/$relative_path"
done

echo "Restored 19 office-ai lesson pages from 2026-07-15 pre-repair backup."
