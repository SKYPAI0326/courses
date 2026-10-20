#!/bin/sh
set -eu

COURSE_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BACKUP="$COURSE_ROOT/_backup/2026-10-20-tone-full-course-pre-repair"
SOURCE_ROOT="$COURSE_ROOT/../../_lessons/canva-video-teaching"

cp "$BACKUP/sources/CH1-3.md" "$SOURCE_ROOT/CH1-3.md"
cp "$BACKUP/sources/CH1-4.md" "$SOURCE_ROOT/CH1-4.md"
cp "$BACKUP/sources/CH1-5.md" "$SOURCE_ROOT/CH1-5.md"
cp "$BACKUP/sources/CH1-6.md" "$SOURCE_ROOT/CH1-6.md"
cp "$BACKUP/sources/CH2-1.md" "$SOURCE_ROOT/CH2-1.md"
cp "$BACKUP/sources/CH2-2.md" "$SOURCE_ROOT/CH2-2.md"
cp "$BACKUP/sources/CH2-3.md" "$SOURCE_ROOT/CH2-3.md"
cp "$BACKUP/sources/CH2-4.md" "$SOURCE_ROOT/CH2-4.md"
cp "$BACKUP/sources/CH2-5.md" "$SOURCE_ROOT/CH2-5.md"
cp "$BACKUP/sources/CH2-6.md" "$SOURCE_ROOT/CH2-6.md"
cp "$BACKUP/sources/EXT1.md" "$SOURCE_ROOT/EXT1.md"
cp "$BACKUP/html/ch1/CH1-3.html" "$COURSE_ROOT/ch1/CH1-3.html"
cp "$BACKUP/html/ch1/CH1-4.html" "$COURSE_ROOT/ch1/CH1-4.html"
cp "$BACKUP/html/ch1/CH1-5.html" "$COURSE_ROOT/ch1/CH1-5.html"
cp "$BACKUP/html/ch1/CH1-6.html" "$COURSE_ROOT/ch1/CH1-6.html"
cp "$BACKUP/html/ch2/CH2-1.html" "$COURSE_ROOT/ch2/CH2-1.html"
cp "$BACKUP/html/ch2/CH2-2.html" "$COURSE_ROOT/ch2/CH2-2.html"
cp "$BACKUP/html/ch2/CH2-3.html" "$COURSE_ROOT/ch2/CH2-3.html"
cp "$BACKUP/html/ch2/CH2-4.html" "$COURSE_ROOT/ch2/CH2-4.html"
cp "$BACKUP/html/ch2/CH2-5.html" "$COURSE_ROOT/ch2/CH2-5.html"
cp "$BACKUP/html/ch2/CH2-6.html" "$COURSE_ROOT/ch2/CH2-6.html"
cp "$BACKUP/html/EXT1.html" "$COURSE_ROOT/EXT1.html"
cp "$BACKUP/tool/sync_two_pages.py" "$COURSE_ROOT/_repair/2026-10-20-tone-pilot/sync_two_pages.py"

echo "Restored full-course tone targets from $BACKUP"
