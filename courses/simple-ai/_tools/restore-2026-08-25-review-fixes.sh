#!/bin/sh
set -eu

COURSE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REPO_DIR=$(CDPATH= cd -- "$COURSE_DIR/../.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-08-25-review-fixes"

for file in CH1-1.html CH1-2.html CH1-3.html CH1-4.html CH2-1.html CH2-2.html CH2-3.html CH2-4.html module1.html module2.html handbook.html index.html prompt-library.html; do
  cp "$BACKUP_DIR/courses/simple-ai/$file" "$COURSE_DIR/$file"
done
cp "$BACKUP_DIR/_outlines/simple-ai.md" "$REPO_DIR/_outlines/simple-ai.md"
cp "$BACKUP_DIR/_outlines/simple-ai.style-guide.md" "$REPO_DIR/_outlines/simple-ai.style-guide.md"

printf '%s\n' "Restored simple-ai review-fixes scope."
