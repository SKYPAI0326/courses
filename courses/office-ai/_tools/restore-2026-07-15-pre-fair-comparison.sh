#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-07-15-pre-fair-comparison"

cp "$BACKUP_DIR/ch1/CH1-4.html" "$COURSE_DIR/ch1/CH1-4.html"
cp "$BACKUP_DIR/ch3/CH3-1.html" "$COURSE_DIR/ch3/CH3-1.html"

echo "Restored fair-comparison pages from $BACKUP_DIR"
