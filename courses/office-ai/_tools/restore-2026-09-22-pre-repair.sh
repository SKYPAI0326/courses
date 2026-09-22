#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-22-pre-repair"
FILES=''
index=0
for backup_file in $(find "$BACKUP_DIR" -type f -name '*.html' | sort); do
  relative_path=${backup_file#"$BACKUP_DIR/"}
  if [ ! -f "$backup_file" ]; then
    echo "Missing backup: $backup_file" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$COURSE_DIR/$relative_path")"
  cp -p "$backup_file" "$COURSE_DIR/$relative_path"
  index=$((index + 1))
done
printf 'Restored %s office-ai HTML files from 2026-09-22 pre-repair backup.\n' "$index"
