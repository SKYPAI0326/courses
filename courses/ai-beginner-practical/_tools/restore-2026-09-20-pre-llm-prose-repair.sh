#!/usr/bin/env bash
set -euo pipefail

COURSE_ROOT="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical"
for FILE in CH1-1.html CH2-1.html CH3-1.html CH4-1.html; do
  cp "$COURSE_ROOT/_backup/2026-09-20-pre-llm-prose-repair/$FILE" "$COURSE_ROOT/$FILE"
done
printf 'Restored CH1-1.html through CH4-1.html from the pre-llm-prose-repair backup.\n'
