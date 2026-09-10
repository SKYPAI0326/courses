#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$ROOT_DIR/_backup/2026-09-10-pre-repair"

for rel in \
  lessons/index.html \
  lessons/module1.html \
  lessons/m1-1-setup.html \
  lessons/m1-2-tunnel.html \
  lessons/m1-3-json.html \
  lessons/m4-1-remote.html \
  lessons/m3-1-watch.html \
  lessons/m3-2-rename.html \
  lessons/m4-2-hybrid.html \
  lessons/m4-3-ai.html \
  lessons/m2-2-chaining.html \
  lessons/m2-3-logic.html \
  lessons/m0-install-mac.html \
  lessons/m0-install-win.html \
  lessons/m0-workflow-01-webhook.html; do
  cp "$BACKUP_DIR/$rel" "$ROOT_DIR/$rel"
done

echo "Restored n8n repair scope from $BACKUP_DIR"
