#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_DIR="$REPO_DIR/n8n/_backup/2026-09-13-pre-gemini-thinking-level"

while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  mkdir -p "$REPO_DIR/$(dirname "$rel")"
  cp "$BACKUP_DIR/$rel" "$REPO_DIR/$rel"
done <<'FILES'
n8n/assets/n8n-lite-pack.zip
n8n/lessons/m0-install-mac.html
n8n/lessons/m0-install-win.html
n8n/lessons/m0-local-llm-guide.html
n8n/lessons/m0-workflow-02-pdf-rename.html
n8n/lessons/m0-workflow-03-batch.html
n8n/lessons/m0-workflow-04-daily.html
n8n/lessons/m0-workflow-06-webhook-ai.html
FILES

echo "Restored Gemini thinking-level backup."
