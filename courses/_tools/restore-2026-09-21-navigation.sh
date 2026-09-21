#!/usr/bin/env bash
set -euo pipefail

COURSES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
BACKUP_DIR="$COURSES_DIR/_backup/2026-09-21-pre-navigation"

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "Backup not found: $BACKUP_DIR" >&2
  exit 1
fi

while IFS= read -r -d '' source; do
  relative="${source#"$BACKUP_DIR/"}"
  target="$COURSES_DIR/$relative"
  mkdir -p "$(dirname "$target")"
  cp "$source" "$target"
done < <(find "$BACKUP_DIR" -type f -name '*.html' -print0)

echo "Restored navigation repair backup: $BACKUP_DIR"
