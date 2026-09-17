#!/usr/bin/env bash
set -eu

BASE="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$BASE/_backup/2026-09-17-content-repair"
LESSONS="$BASE/../_lessons/digital-content-growth-126h"

cp "$BACKUP/PRAC6.html" "$BASE/PRAC6.html"
cp "$BACKUP/CH6-1.html" "$BASE/CH6-1.html"
cp "$BACKUP/CH6-2.html" "$BASE/CH6-2.html"
cp "$BACKUP/CH6-3.html" "$BASE/CH6-3.html"
cp "$BACKUP/CH1-1.html" "$BASE/CH1-1.html"
cp "$BACKUP/CH1-2.html" "$BASE/CH1-2.html"
cp "$BACKUP/CH1-3.html" "$BASE/CH1-3.html"
cp "$BACKUP/adversarial-learner-report.md" "$BASE/_review/adversarial-learner-report.md"
cp "$BACKUP/assets-README.md" "$BASE/assets/README.md"
cp "$BACKUP/PRAC6.md" "$LESSONS/PRAC6.md"
cp "$BACKUP/CH6-1.md" "$LESSONS/CH6-1.md"
cp "$BACKUP/CH6-2.md" "$LESSONS/CH6-2.md"
cp "$BACKUP/CH6-3.md" "$LESSONS/CH6-3.md"
cp "$BACKUP/CH1-1.md" "$LESSONS/CH1-1.md"
cp "$BACKUP/CH1-2.md" "$LESSONS/CH1-2.md"
cp "$BACKUP/CH1-3.md" "$LESSONS/CH1-3.md"
rm -f "$BASE/assets/templates/PRAC6-完整成果包參考完成品.html"

echo "Restored 2026-09-17 content repair scope."
