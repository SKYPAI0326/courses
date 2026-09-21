#!/bin/zsh
set -euo pipefail

ROOT="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical"
BACKUP="$ROOT/_backup/2026-09-21-pre-typography-layout"

cp "$BACKUP/layout-redesign.css" "$ROOT/assets/layout-redesign.css"
cp "$BACKUP/index.html" "$ROOT/index.html"
cp "$BACKUP/module1.html" "$ROOT/module1.html"
cp "$BACKUP/CH1-1.html" "$ROOT/CH1-1.html"
cp "$BACKUP/CH2-1.html" "$ROOT/CH2-1.html"
cp "$BACKUP/CH3-1.html" "$ROOT/CH3-1.html"
cp "$BACKUP/CH4-1.html" "$ROOT/CH4-1.html"

print "Restored pre-typography-layout files."
