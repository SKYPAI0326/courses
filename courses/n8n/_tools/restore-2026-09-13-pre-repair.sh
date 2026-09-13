#!/bin/bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$BASE/_backup/2026-09-13-pre-repair"

cp "$BACKUP/m0-install-mac.html" "$BASE/lessons/m0-install-mac.html"
cp "$BACKUP/m0-install-win.html" "$BASE/lessons/m0-install-win.html"
cp "$BACKUP/m1-1-launch.html" "$BASE/lessons/m1-1-launch.html"
cp "$BACKUP/starter-kit-README.md" "$BASE/assets/n8n-starter-kit/README.md"
cp "$BACKUP/n8n-lite-pack.zip" "$BASE/assets/n8n-lite-pack.zip"
cp "$BACKUP/n8n-starter-kit.zip" "$BASE/assets/n8n-starter-kit.zip"
echo "Restored 2026-09-13 pre-repair files."
