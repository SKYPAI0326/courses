#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COURSES_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
BACKUP_DIR="$COURSES_ROOT/n8n/_backup/2026-09-28-pre-ui-gate-fix"

for file in m0-install-mac.html m0-install-win.html; do
  if [[ ! -s "$BACKUP_DIR/$file" ]]; then
    echo "Backup missing: $BACKUP_DIR/$file" >&2
    exit 1
  fi
done

cp -p "$BACKUP_DIR/m0-install-mac.html" "$COURSES_ROOT/n8n/lessons/m0-install-mac.html"
cp -p "$BACKUP_DIR/m0-install-win.html" "$COURSES_ROOT/n8n/lessons/m0-install-win.html"
echo "Restored the two n8n install pages from $BACKUP_DIR"
