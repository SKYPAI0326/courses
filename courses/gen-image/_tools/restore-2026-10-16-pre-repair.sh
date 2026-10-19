#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$COURSE_DIR/../.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-10-16-pre-repair"

test -d "$BACKUP_DIR/course-html"
test -d "$BACKUP_DIR/outlines"
test -d "$BACKUP_DIR/lessons"

for source in "$BACKUP_DIR/course-html"/*.html; do
  cp "$source" "$COURSE_DIR/$(basename "$source")"
done

cp "$BACKUP_DIR/outlines/gen-image.md" "$PROJECT_ROOT/_outlines/gen-image.md"
cp "$BACKUP_DIR/outlines/gen-image.style-guide.md" "$PROJECT_ROOT/_outlines/gen-image.style-guide.md"

for source in "$BACKUP_DIR/lessons"/*.md; do
  cp "$source" "$PROJECT_ROOT/_lessons/gen-image/$(basename "$source")"
done

for created in \
  README.md \
  10-industries-brief-library.md \
  8-version-library.md \
  8-prompt-examples.md \
  prompt-templates.md \
  anti-patterns.md \
  brand-dna-template.md \
  7-brand-style-system.md \
  l2-skeleton-library.md \
  skeleton-quick-card.html \
  skeleton-quick-card.pdf \
  reference-pack-manifest.md \
  human-qa-and-release-gate.md \
  platform-check-card.md
do
  rm -f "$COURSE_DIR/assets/downloads/$created"
done

rm -rf "$COURSE_DIR/assets/reference-pack"

echo "Restored gen-image course content to the 2026-10-16 pre-repair snapshot."
