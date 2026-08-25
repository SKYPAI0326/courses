#!/bin/sh
set -eu

COURSE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-08-25-pre-deliverables"

cp "$BACKUP_DIR/CH2-1.html" "$COURSE_DIR/CH2-1.html"
cp "$BACKUP_DIR/module2.html" "$COURSE_DIR/module2.html"
cp "$BACKUP_DIR/index.html" "$COURSE_DIR/index.html"
cp "$BACKUP_DIR/CH2-4.html" "$COURSE_DIR/CH2-4.html"

rm -f "$COURSE_DIR/handbook.html"
rm -f "$COURSE_DIR/quick-reference.html"
rm -f "$COURSE_DIR/assets/創業-AI-實戰手冊.pdf"
rm -f "$COURSE_DIR/assets/創業-AI-實戰-10則Prompt精選.pdf"
rm -f "$COURSE_DIR/_tools/build-deliverables.js"
rm -f "$COURSE_DIR/_repair/2026-08-25/PLATFORM-AUDIT.md"
rm -f "$COURSE_DIR/_repair/2026-08-25/REPAIR-REPORT.md"

printf '%s\n' "Restored simple-ai pre-deliverables state."
