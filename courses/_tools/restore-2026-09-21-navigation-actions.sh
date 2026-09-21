#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-21-pre-navigation-actions"

if [[ ! -d "$BACKUP" ]]; then
  echo "Missing backup: $BACKUP" >&2
  exit 1
fi

find "$BACKUP" -type f -name '*.html' -print0 |
while IFS= read -r -d '' file; do
  relative="${file#"$BACKUP/"}"
  mkdir -p "$ROOT/$(dirname "$relative")"
  cp "$file" "$ROOT/$relative"
done

echo "Restored navigation-action repair backup: $BACKUP"
