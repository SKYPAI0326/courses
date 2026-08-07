#!/bin/bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-07-19-pre-materials-repair"

cp "$BACKUP_DIR/index.html" "$COURSE_DIR/index.html"
cp "$BACKUP_DIR/assets/after-class-guide.md" "$COURSE_DIR/assets/after-class-guide.md"
cp "$BACKUP_DIR/assets/datasets/prompts-all.md" "$COURSE_DIR/assets/datasets/prompts-all.md"
cp "$BACKUP_DIR/assets/datasets/persona-templates.md" "$COURSE_DIR/assets/datasets/persona-templates.md"
cp "$BACKUP_DIR/_tools/build-student-pdfs.py" "$COURSE_DIR/_tools/build-student-pdfs.py"

echo "課後素材來源與首頁已還原。重新執行素材建置器即可重建舊版下載檔。"
