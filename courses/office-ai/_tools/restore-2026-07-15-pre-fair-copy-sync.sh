#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-07-15-pre-fair-copy-sync"

cp "$BACKUP_DIR/ch1/CH1-4.html" "$COURSE_DIR/ch1/CH1-4.html"

echo "Restored fair-copy-sync page from $BACKUP_DIR"
