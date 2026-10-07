#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-10-07-part1-ch1-pre-rebuild"
TARGET_DIR="${1:-$COURSE_DIR}"
for relative_path in \
  part1/CH1-1.html \
  part1/CH1-2.html \
  part1/CH1-3.html \
  _source/fragments/part1-CH1-1.fragment \
  _source/fragments/part1-CH1-2.fragment \
  _source/fragments/part1-CH1-3.fragment \
  _source/LESSON-PLANS.md \
  _source/CURRICULUM-MAP.md \
  index.html \
  assets/materials/prompt-timer.txt \
  assets/materials/materials.zip; do
  mkdir -p "$TARGET_DIR/$(dirname -- "$relative_path")"
  cp "$BACKUP_DIR/$relative_path" "$TARGET_DIR/$relative_path"
done
