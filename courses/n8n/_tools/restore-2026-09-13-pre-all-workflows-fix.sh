#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$BASE_DIR/_backup/2026-09-13-pre-all-workflows-fix"

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "Backup not found: $BACKUP_DIR" >&2
  exit 1
fi

restore_file() {
  local rel="$1"
  cp -p "$BACKUP_DIR/$rel" "$BASE_DIR/$rel"
  echo "restored $rel"
}

restore_file "lessons/index.html"
restore_file "lessons/m0-workflow-tour.html"
restore_file "lessons/m0-workflow-02-pdf-rename.html"
restore_file "lessons/m0-workflow-03-batch.html"
restore_file "lessons/m0-workflow-05-telegram.html"
restore_file "lessons/m0-workflow-08-expression.html"
restore_file "lessons/m0-workflow-10-folder-organize.html"
restore_file "lessons/m0-workflow-11-csv-clean.html"
restore_file "lessons/m0-workflow-12-knowledge-rag.html"
restore_file "lessons/m0-workflow-13-daily-ops.html"
restore_file "lessons/m0-workflow-14-api-monitor.html"
restore_file "assets/n8n-lite-pack.zip"
restore_file "assets/n8n-starter-kit.zip"

echo "Restored pre-fix files from $BACKUP_DIR"
