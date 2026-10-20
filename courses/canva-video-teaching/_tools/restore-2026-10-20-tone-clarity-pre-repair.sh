#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
COURSE_DIR=${RESTORE_COURSE_DIR:-$SOURCE_COURSE_DIR}
REPO_DIR=${RESTORE_REPO_DIR:-$(CDPATH= cd -- "$SOURCE_COURSE_DIR/../.." && pwd)}
BACKUP_DIR="$SOURCE_COURSE_DIR/_backup/2026-10-20-tone-clarity-pre-repair"

mkdir -p "$COURSE_DIR/ch1"
mkdir -p "$COURSE_DIR/assets"
mkdir -p "$COURSE_DIR/_repair/2026-10-20-tone-pilot"
mkdir -p "$REPO_DIR/_lessons/canva-video-teaching"

cp "$BACKUP_DIR/courses/canva-video-teaching/ch1/CH1-1.html" "$COURSE_DIR/ch1/CH1-1.html"
cp "$BACKUP_DIR/courses/canva-video-teaching/ch1/CH1-2.html" "$COURSE_DIR/ch1/CH1-2.html"
cp "$BACKUP_DIR/courses/canva-video-teaching/assets/handout.css" "$COURSE_DIR/assets/handout.css"
cp "$BACKUP_DIR/courses/canva-video-teaching/_repair/2026-10-20-tone-pilot/sync_two_pages.py" "$COURSE_DIR/_repair/2026-10-20-tone-pilot/sync_two_pages.py"
cp "$BACKUP_DIR/_lessons/canva-video-teaching/CH1-1.md" "$REPO_DIR/_lessons/canva-video-teaching/CH1-1.md"
cp "$BACKUP_DIR/_lessons/canva-video-teaching/CH1-2.md" "$REPO_DIR/_lessons/canva-video-teaching/CH1-2.md"

printf '%s\n' "Restored pre-clarity-pilot files from $BACKUP_DIR"
