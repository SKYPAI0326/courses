#!/usr/bin/env bash
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESTORE_PY="$COURSE_DIR/_backup/2026-10-09-pre-repair/restore.py"

if [[ ! -f "$RESTORE_PY" ]]; then
  printf 'Backup restore tool not found: %s\n' "$RESTORE_PY" >&2
  exit 1
fi

if [[ "${1:-}" == "--live" ]]; then
  shift
  python3 "$RESTORE_PY" "$@"
elif [[ "${1:-}" == "--dry-run" || "${1:-}" == "--target" ]]; then
  python3 "$RESTORE_PY" "$@"
else
  printf 'Usage: %s --dry-run | --target COPY_DIR | --live\n' "$0" >&2
  printf 'Live restore copies only the 37 manifest originals. New files remain for review.\n' >&2
  exit 2
fi
