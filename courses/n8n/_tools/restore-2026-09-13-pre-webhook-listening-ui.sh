#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-13-pre-webhook-listening-ui"

cp "$BACKUP/m0-workflow-01-webhook.html" "$ROOT/lessons/m0-workflow-01-webhook.html"
cp "$BACKUP/m0-install-mac.html" "$ROOT/lessons/m0-install-mac.html"
cp "$BACKUP/m0-install-win.html" "$ROOT/lessons/m0-install-win.html"
cp "$BACKUP/m1-1-launch.html" "$ROOT/lessons/m1-1-launch.html"
cp "$BACKUP/m1-2-tunnel.html" "$ROOT/lessons/m1-2-tunnel.html"
cp "$BACKUP/n8n-lite-pack.zip" "$ROOT/assets/n8n-lite-pack.zip"

echo "Restored webhook Listening UI repair scope from $BACKUP"
