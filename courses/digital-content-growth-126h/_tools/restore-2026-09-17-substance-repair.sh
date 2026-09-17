#!/usr/bin/env bash
set -eu

BASE="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$BASE/_backup/2026-09-17-substance-repair/lessons"
LESSONS="$BASE/../_lessons/digital-content-growth-126h"

for file in "$BACKUP"/*.md; do
  cp "$file" "$LESSONS/$(basename "$file")"
done

echo "Restored 2026-09-17 substance-repair lesson sources."
