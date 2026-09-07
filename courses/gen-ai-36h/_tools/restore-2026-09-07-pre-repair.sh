#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-09-07-pre-repair"

if [[ ! -d "$BACKUP_DIR" ]]; then
  printf 'Backup directory not found: %s\n' "$BACKUP_DIR" >&2
  exit 1
fi

while IFS= read -r -d '' file; do
  relative="${file#"$BACKUP_DIR/"}"
  destination="$COURSE_DIR/$relative"
  mkdir -p "$(dirname "$destination")"
  cp -p "$file" "$destination"
done < <(find "$BACKUP_DIR" -type f -print0)

printf 'Restored pre-repair files from %s\n' "$BACKUP_DIR"
