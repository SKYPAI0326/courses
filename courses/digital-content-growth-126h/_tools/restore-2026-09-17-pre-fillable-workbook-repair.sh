#!/bin/zsh
set -euo pipefail

COURSE_DIR="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/digital-content-growth-126h"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-17-pre-fillable-workbook-repair"

find "$COURSE_DIR/assets/templates" -maxdepth 1 -name '*-參考版.html' -delete
rm -f "$COURSE_DIR/_tools/asset-contracts.json"
cp "$BACKUP_DIR/tools/rebuild-learner-shell.py" "$COURSE_DIR/_tools/rebuild-learner-shell.py"
cp "$BACKUP_DIR/tools/test_learner_render_contract.py" "$COURSE_DIR/_tools/test_learner_render_contract.py"
cp "$BACKUP_DIR/html/"*.html "$COURSE_DIR/"
cp "$BACKUP_DIR/html/assets/templates/"*.html "$COURSE_DIR/assets/templates/"
cp "$BACKUP_DIR/L5-evidence-manifest.json" "$COURSE_DIR/_validation/L5-evidence-manifest.json"

print "Restored pre-fillable-workbook-repair HTML, generator, tests, and evidence manifest."
