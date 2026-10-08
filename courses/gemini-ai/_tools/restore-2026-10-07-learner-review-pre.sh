#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BACKUP="$ROOT/_backup/2026-10-07-learner-review-pre"
for rel in \
  part1/PRAC1-1.html part1/PRAC1-3.html \
  part2/CH2-3.html part2/PRAC2-3.html \
  part3/PRAC3-1.html part4/PRAC4-1.html \
  part5/PRAC5-4.html part5/PRAC5-6.html part5/PRAC5-9.html \
  part5/PRAC5-10.html part5/PRAC5-11.html \
  _source/CURRICULUM-MAP.md \
  _repair/2026-10-06/full-content-rebuild/REPAIR-REPORT.md
do
  cp "$BACKUP/$rel" "$ROOT/$rel"
done
printf '%s\n' 'Restored the 13 pre-learner-review files.'
