#!/bin/zsh
set -euo pipefail

BASE="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses"
BACKUP="$BASE/uiux-designer/_backup/2026-09-17-pre-learner-entry-repair"

cp "$BACKUP/CH6-prototype-task-test.html" "$BASE/uiux-designer/part2/CH6-prototype-task-test.html"
cp "$BACKUP/CH7-figma-handoff-export.html" "$BASE/uiux-designer/part2/CH7-figma-handoff-export.html"
cp "$BACKUP/CH8-web-git-deploy.html" "$BASE/uiux-designer/part3/CH8-web-git-deploy.html"
cp "$BACKUP/CH4-overlay-single-action.html" "$BASE/uiux-designer/part2/CH4-overlay-single-action.html"
echo "Restored learner-entry repair scope from $BACKUP"
