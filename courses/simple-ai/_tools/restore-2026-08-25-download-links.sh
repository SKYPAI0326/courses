#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$BASE/_backup/2026-08-25-download-links"
ORIGINAL_ASSETS="$BACKUP/original-assets/courses/simple-ai/assets"

cp "$BACKUP/CH1-1.html" "$BASE/CH1-1.html"
cp "$BACKUP/CH1-2.html" "$BASE/CH1-2.html"
cp "$BACKUP/CH1-3.html" "$BASE/CH1-3.html"
cp "$BACKUP/CH1-4.html" "$BASE/CH1-4.html"
cp "$BACKUP/CH2-1.html" "$BASE/CH2-1.html"
cp "$BACKUP/CH2-2.html" "$BASE/CH2-2.html"
cp "$BACKUP/CH2-3.html" "$BASE/CH2-3.html"
cp "$BACKUP/CH2-4.html" "$BASE/CH2-4.html"
cp "$BACKUP/index.html" "$BASE/index.html"
cp "$BACKUP/module2.html" "$BASE/module2.html"
cp "$BACKUP/handbook.html" "$BASE/handbook.html"
cp "$ORIGINAL_ASSETS/創業-AI-實戰手冊.pdf" "$BASE/assets/創業-AI-實戰手冊.pdf"
cp "$ORIGINAL_ASSETS/創業-AI-實戰-10則Prompt精選.pdf" "$BASE/assets/創業-AI-實戰-10則Prompt精選.pdf"

rm -f "$BASE/assets/datasets/"*.txt

echo "Restored simple-ai download-link scope from $BACKUP"
