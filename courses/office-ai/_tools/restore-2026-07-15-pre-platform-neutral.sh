#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
BACKUP="$ROOT/courses/office-ai/_backup/2026-07-15-pre-platform-neutral"
COURSE="$ROOT/courses/office-ai"

cp "$BACKUP/index.html" "$COURSE/index.html"
cp "$BACKUP/ch1/CH1-1.html" "$COURSE/ch1/CH1-1.html"
cp "$BACKUP/ch1/CH1-2.html" "$COURSE/ch1/CH1-2.html"
cp "$BACKUP/ch1/CH1-3.html" "$COURSE/ch1/CH1-3.html"
cp "$BACKUP/ch1/CH1-4.html" "$COURSE/ch1/CH1-4.html"
cp "$BACKUP/ch2/CH2-3.html" "$COURSE/ch2/CH2-3.html"
cp "$BACKUP/ch3/CH3-1.html" "$COURSE/ch3/CH3-1.html"
cp "$BACKUP/ch4/CH4-3.html" "$COURSE/ch4/CH4-3.html"
cp "$BACKUP/ch6/CH6-3.html" "$COURSE/ch6/CH6-3.html"
cp "$BACKUP/assets/after-class-guide.md" "$COURSE/assets/after-class-guide.md"
cp "$BACKUP/_repair/2026-07-15/REPAIR-REPORT.md" "$COURSE/_repair/2026-07-15/REPAIR-REPORT.md"
cp "$BACKUP/outline/office-ai.md" "$ROOT/_outlines/office-ai.md"

echo "已還原 platform-neutral 改寫前版本。請重跑 lint、search index 與 sitemap。"
