#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-13-pre-daily-report-provenance"

cp "$BACKUP/n8n-lite-pack.zip" "$ROOT/assets/n8n-lite-pack.zip"
cp "$BACKUP/m0-workflow-04-daily.html" "$ROOT/lessons/m0-workflow-04-daily.html"
cp "$BACKUP/m0-install-mac.html" "$ROOT/lessons/m0-install-mac.html"
cp "$BACKUP/m0-install-win.html" "$ROOT/lessons/m0-install-win.html"

echo "Restored daily report provenance repair scope from $BACKUP"
