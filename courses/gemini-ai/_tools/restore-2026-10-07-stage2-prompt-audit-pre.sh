#!/usr/bin/env bash
set -euo pipefail
COURSE_ROOT='/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gemini-ai'
BACKUP_DIR='/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gemini-ai/_backup/2026-10-07-stage2-prompt-audit-pre'
cp "$BACKUP_DIR/LEGACY-CONTENT-INVENTORY.md" "$COURSE_ROOT/_repair/2026-10-07/LEGACY-CONTENT-INVENTORY.md"
cp "$BACKUP_DIR/LEGACY-CONTENT-MIGRATION-MAP.md" "$COURSE_ROOT/_repair/2026-10-07/LEGACY-CONTENT-MIGRATION-MAP.md"
cp "$BACKUP_DIR/COURSE-DESIGN-CONTRACT.md" "$COURSE_ROOT/_repair/2026-10-07/COURSE-DESIGN-CONTRACT.md"
cp "$BACKUP_DIR/STAGE3-CASE-ROUTE-RECOMMENDATION.md" "$COURSE_ROOT/_repair/2026-10-07/STAGE3-CASE-ROUTE-RECOMMENDATION.md"
