#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
course_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
project_root=$(CDPATH= cd -- "$course_dir/../.." && pwd)
target_root=${1:-$project_root}
backup_root="$course_dir/_backup/2026-10-22-pre-deep-review-repair"
target_course="$target_root/courses/gen-image"
target_lessons="$target_root/_lessons/gen-image"

mkdir -p "$target_course" "$target_lessons"

cp -R "$backup_root/course/." "$target_course/"
cp -R "$backup_root/sources/_lessons/gen-image/." "$target_lessons/"

rm -f \
  "$target_course/assets/learner-record.js" \
  "$target_course/_tools/test-deep-review-repair.py" \
  "$target_course/_tools/test-learner-record-browser.py" \
  "$target_course/_validation/deep-review-repair-self-check.md" \
  "$target_course/_repair/2026-10-22-deep-review/REPAIR-REPORT.md"

printf '%s\n' "Restored pre-repair files to $target_root"
