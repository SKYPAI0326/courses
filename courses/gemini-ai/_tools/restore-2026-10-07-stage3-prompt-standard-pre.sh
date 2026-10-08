#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$COURSE_DIR/_backup/2026-10-07-stage3-prompt-standard-pre"
TARGET_DIR="${1:-$COURSE_DIR}"
for relative_path in \
  _repair/2026-10-07/COURSE-DESIGN-CONTRACT.md \
  _repair/2026-10-07/LEGACY-CONTENT-MIGRATION-MAP.md; do
  mkdir -p "$TARGET_DIR/$(dirname -- "$relative_path")"
  cp "$BACKUP_DIR/$relative_path" "$TARGET_DIR/$relative_path"
done
