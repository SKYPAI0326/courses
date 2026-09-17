#!/bin/sh
set -eu

BASE="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
BACKUP="$BASE/_backup/2026-09-16-asset-attachments"

cp "$BACKUP"/html/*.html "$BASE/"
cp "$BACKUP"/assets/course-shell.css "$BASE/assets/course-shell.css"
cp "$BACKUP"/assets/templates/*.md "$BASE/assets/templates/"
cp "$BACKUP"/assets/datasets/*.csv "$BASE/assets/datasets/"
find "$BASE/assets/templates" -maxdepth 1 -type f -name '*.html' -delete
cp "$BACKUP"/tools/rebuild-learner-shell.py "$BASE/_tools/rebuild-learner-shell.py"

printf '%s\n' 'restored 2026-09-16 asset attachment repair backup'
