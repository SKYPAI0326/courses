#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COURSE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BASE_DIR=$(CDPATH= cd -- "$COURSE_DIR/../.." && pwd)
BACKUP_DIR="$COURSE_DIR/_backup/2026-10-16-pre-growth-assistant"

restore_file() {
  source_file=$1
  target_file=$2
  if [ ! -f "$source_file" ]; then
    echo "Missing backup: $source_file" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$target_file")"
  cp -p "$source_file" "$target_file"
}

restore_file "$BACKUP_DIR/course/ch1/CH1-2.html" "$COURSE_DIR/ch1/CH1-2.html"
restore_file "$BACKUP_DIR/course/ch1/CH1-1.html" "$COURSE_DIR/ch1/CH1-1.html"
restore_file "$BACKUP_DIR/course/ch1/CH1-3.html" "$COURSE_DIR/ch1/CH1-3.html"
restore_file "$BACKUP_DIR/course/ch5/CH5-3.html" "$COURSE_DIR/ch5/CH5-3.html"
restore_file "$BACKUP_DIR/course/ch6/CH6-1.html" "$COURSE_DIR/ch6/CH6-1.html"
restore_file "$BACKUP_DIR/course/ch6/CH6-2.html" "$COURSE_DIR/ch6/CH6-2.html"
restore_file "$BACKUP_DIR/course/ch6/CH6-3.html" "$COURSE_DIR/ch6/CH6-3.html"
restore_file "$BACKUP_DIR/course/index.html" "$COURSE_DIR/index.html"
restore_file "$BACKUP_DIR/course/assets/after-class-guide.md" "$COURSE_DIR/assets/after-class-guide.md"
restore_file "$BACKUP_DIR/course/_validation/evidence.json" "$COURSE_DIR/_validation/evidence.json"
restore_file "$BACKUP_DIR/course/_validation/HUMAN-VALIDATION-CHECKLIST.md" "$COURSE_DIR/_validation/HUMAN-VALIDATION-CHECKLIST.md"
restore_file "$BACKUP_DIR/course/_validation/FINAL-REPORT.md" "$COURSE_DIR/_validation/FINAL-REPORT.md"
restore_file "$BACKUP_DIR/course/_validation/L5-evidence-manifest.json" "$COURSE_DIR/_validation/L5-evidence-manifest.json"
restore_file "$BACKUP_DIR/course/_validation/validation-result.json" "$COURSE_DIR/_validation/validation-result.json"

for review_name in CH1-2-content.md CH1-2-fidelity.md CH6-1-content.md CH6-1-fidelity.md CH6-3-content.md CH6-3-fidelity.md; do
  restore_file "$BACKUP_DIR/course/_review/$review_name" "$COURSE_DIR/_review/$review_name"
done

for lesson_name in CH1-2.md CH6-1.md CH6-3.md; do
  restore_file "$BACKUP_DIR/project/_lessons/office-ai/$lesson_name" "$BASE_DIR/_lessons/office-ai/$lesson_name"
done

restore_file "$BACKUP_DIR/project/_outlines/office-ai.md" "$BASE_DIR/_outlines/office-ai.md"
restore_file "$BACKUP_DIR/project/search-index.json" "$BASE_DIR/search-index.json"

if [ -f "$BACKUP_DIR/project/_outlines/office-ai.style-guide.md" ]; then
  restore_file "$BACKUP_DIR/project/_outlines/office-ai.style-guide.md" "$BASE_DIR/_outlines/office-ai.style-guide.md"
else
  rm -f "$BASE_DIR/_outlines/office-ai.style-guide.md"
fi

rm -f "$COURSE_DIR/assets/skills/ta-core.md" "$COURSE_DIR/assets/skills/ta-learning.md" "$COURSE_DIR/assets/skills/ta-work.md"
rmdir "$COURSE_DIR/assets/skills" 2>/dev/null || true
rm -f \
  "$COURSE_DIR/_review/navigation-title-sync-2026-10-16.md" \
  "$COURSE_DIR/_review/platform-growth-assistant-2026-10-16.md" \
  "$COURSE_DIR/_review/technical-growth-assistant-2026-10-16.md"

echo "Restored office-ai files to the 2026-10-16 pre-growth-assistant state."
