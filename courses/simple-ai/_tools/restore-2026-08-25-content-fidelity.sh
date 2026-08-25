#!/bin/sh
set -eu

COURSE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-08-25-content-fidelity"

cp "$BACKUP_DIR/CH1-3.html" "$COURSE_DIR/CH1-3.html"
cp "$BACKUP_DIR/CH1-4.html" "$COURSE_DIR/CH1-4.html"
cp "$BACKUP_DIR/CH2-4.html" "$COURSE_DIR/CH2-4.html"

printf '%s\n' "Restored simple-ai content-fidelity repair scope."
