#!/bin/bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$BASE_DIR/_backup/2026-09-13-pre-aq-key-format"

cp "$BACKUP_DIR/n8n-lite-pack.zip" "$BASE_DIR/assets/n8n-lite-pack.zip"
cp "$BACKUP_DIR/m0-install-mac.html" "$BASE_DIR/lessons/m0-install-mac.html"
cp "$BACKUP_DIR/m0-install-win.html" "$BASE_DIR/lessons/m0-install-win.html"

echo "Restored Gemini API key format repair backup."
