#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-06-25-pre-content-balance"
OUTLINE_DIR="$(cd "$COURSE_DIR/../.." && pwd)/_outlines"

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "Backup not found: $BACKUP_DIR" >&2
  exit 1
fi

cp "$BACKUP_DIR"/*.html "$COURSE_DIR"/
cp "$BACKUP_DIR/gemini-notebooklm-workshop.md" "$OUTLINE_DIR/gemini-notebooklm-workshop.md"

echo "Restored gemini-notebooklm-workshop HTML and outline from:"
echo "$BACKUP_DIR"
