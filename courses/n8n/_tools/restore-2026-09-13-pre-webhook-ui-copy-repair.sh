#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP="$ROOT/n8n/_backup/2026-09-13-pre-webhook-ui-copy-repair"

cp "$BACKUP/n8n-lite-pack.zip" "$ROOT/n8n/assets/n8n-lite-pack.zip"
cp "$BACKUP/m0-workflow-06-webhook-ai.html" "$ROOT/n8n/lessons/m0-workflow-06-webhook-ai.html"
cp "$BACKUP/m0-install-mac.html" "$ROOT/n8n/lessons/m0-install-mac.html"
cp "$BACKUP/m0-install-win.html" "$ROOT/n8n/lessons/m0-install-win.html"
cp "$BACKUP/post-llm-appendix-nodes.html" "$ROOT/n8n/lessons/post-llm-appendix-nodes.html"

echo "Restored #06 Webhook UI copy repair scope from $BACKUP"
