#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/../../.." && pwd)"
COURSE="$BASE/courses/ccs-foundations"
BACKUP="$COURSE/_backup/2026-09-29-pre-primary-switch"
LESSONS="$BASE/_lessons/ccs-foundations"

# Restore the pre-switch state from the preserved copies. Run from any directory.
cp -p "$BACKUP/pages/index.html" "$COURSE/index.html"
cp -p "$BACKUP/pages/CH4.html" "$COURSE/CH4.html"
cp -p "$BACKUP/ops/_gates.md" "$COURSE/_gates.md"

for id in 1 2 3 4; do
  cp -p "$BACKUP/pages/CH5-$id.html" "$COURSE/CH5-$id.html"
  cp -p "$BACKUP/lessons/ccs-foundations/CH5-$id.md" "$LESSONS/CH5-$id.md"
done

printf '%s\n' 'Restored pre-switch course files from the dated backup.'
