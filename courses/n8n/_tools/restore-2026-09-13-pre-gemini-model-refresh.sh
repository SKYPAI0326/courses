#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_DIR="$REPO_DIR/n8n/_backup/2026-09-13-pre-gemini-model-refresh"

while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  mkdir -p "$REPO_DIR/$(dirname "$rel")"
  cp "$BACKUP_DIR/$rel" "$REPO_DIR/$rel"
done <<'FILES'
n8n/_lessons/post-llm/post-llm-6-walkthrough.md
n8n/_lessons/post-llm/post-llm-9-format-adapt.md
n8n/assets/workflows/m4-4-ai-secretary-migration.json
n8n/lessons/m0-local-llm-guide.html
n8n/lessons/m0-workflow-02-pdf-rename.html
n8n/lessons/m3-2-rename.html
n8n/lessons/m3-3-generate.html
n8n/lessons/m4-3-ai.html
n8n/lessons/m4-4-ai-secretary-migration.html
n8n/lessons/post-llm-6-walkthrough.html
n8n/lessons/post-llm-9-format-adapt.html
FILES

echo "Restored Gemini model refresh backup."
