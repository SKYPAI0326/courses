#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-13-pre-quick-tunnel-repair"

cp "$BACKUP/m0-workflow-07-tunnel.html" "$ROOT/lessons/m0-workflow-07-tunnel.html"
cp "$BACKUP/post-llm-appendix-nodes.html" "$ROOT/lessons/post-llm-appendix-nodes.html"
cp "$BACKUP/n8n-lite-pack.zip" "$ROOT/assets/n8n-lite-pack.zip"
echo "Restored #07 Quick Tunnel repair backup."
