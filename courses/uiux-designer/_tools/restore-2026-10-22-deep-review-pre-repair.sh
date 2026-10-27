#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
COURSE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
PROJECT_ROOT="${COURSE_WEB_ROOT:-$(cd "$COURSE_ROOT/../.." && pwd -P)}"
BACKUP_ROOT="$COURSE_ROOT/_backup/2026-10-22-deep-review-pre-repair"

restore_one() {
  local backup_relative="$1"
  local target_relative="$2"
  mkdir -p "$(dirname "$PROJECT_ROOT/$target_relative")"
  cp "$BACKUP_ROOT/$backup_relative" "$PROJECT_ROOT/$target_relative"
}

restore_one "_validation/FINAL-REPORT.md" "courses/uiux-designer/_validation/FINAL-REPORT.md"
restore_one "_validation/validation-result.json" "courses/uiux-designer/_validation/validation-result.json"
restore_one "_gates.md" "courses/uiux-designer/_gates.md"
restore_one "index.html" "courses/uiux-designer/index.html"
restore_one "assets/COURSE-START.html" "courses/uiux-designer/assets/COURSE-START.html"
restore_one "part3/CH8-web-git-deploy.html" "courses/uiux-designer/part3/CH8-web-git-deploy.html"
restore_one "_lessons/uiux-designer/B8-web-git-deploy.md" "_lessons/uiux-designer/B8-web-git-deploy.md"

echo "Restored uiux-designer pre-repair files."
