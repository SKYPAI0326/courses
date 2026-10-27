#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BASE_DIR=$(CDPATH= cd -- "$COURSE_DIR/../.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-10-16-pre-beginner-rewrite"

cp "$BACKUP_DIR/course/part1/CH1-1.html" "$COURSE_DIR/part1/CH1-1.html"
cp "$BACKUP_DIR/course/part1/CH1-2.html" "$COURSE_DIR/part1/CH1-2.html"
cp "$BACKUP_DIR/course/part1/CH1-3.html" "$COURSE_DIR/part1/CH1-3.html"
cp "$BACKUP_DIR/course/part1/CH1-4.html" "$COURSE_DIR/part1/CH1-4.html"
cp "$BACKUP_DIR/course/part1/CH1-5.html" "$COURSE_DIR/part1/CH1-5.html"
cp "$BACKUP_DIR/course/part1/PRAC1.html" "$COURSE_DIR/part1/PRAC1.html"
cp "$BACKUP_DIR/course/part2/CH2-1.html" "$COURSE_DIR/part2/CH2-1.html"
cp "$BACKUP_DIR/course/part3/CH3-1.html" "$COURSE_DIR/part3/CH3-1.html"
cp "$BACKUP_DIR/course/part3/CH3-2.html" "$COURSE_DIR/part3/CH3-2.html"
cp "$BACKUP_DIR/course/part3/CH3-3.html" "$COURSE_DIR/part3/CH3-3.html"

for lesson in CH1-1 CH1-2 CH1-3 CH1-4 CH1-5 PRAC1 CH2-1 CH3-1 CH3-2 CH3-3; do
  cp "$BACKUP_DIR/lessons/$lesson.md" "$BASE_DIR/_lessons/acp-ae/$lesson.md"
done

printf '%s\n' "Restored ACP-AE files from 2026-10-16 pre-beginner rewrite backup."
