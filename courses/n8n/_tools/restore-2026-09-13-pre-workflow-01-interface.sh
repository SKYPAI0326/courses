#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP="$REPO/n8n/_backup/2026-09-13-pre-workflow-01-interface"
cd "$REPO"
for f in \
  n8n/lessons/m0-workflow-01-webhook.html \
  n8n/lessons/m1-1-launch.html \
  n8n/lessons/m1-2-tunnel.html \
  n8n/lessons/m0-install-mac.html \
  n8n/lessons/m0-install-win.html \
  n8n/lessons/m0-workflow-02-pdf-rename.html \
  n8n/lessons/post-llm-3-steps-decompose.html \
  n8n/lessons/post-llm-6-walkthrough.html \
  n8n/assets/n8n-lite-pack.zip; do
  cp "$BACKUP/$f" "$f"
done
echo "Restored workflow-01 interface repair scope from $BACKUP"
