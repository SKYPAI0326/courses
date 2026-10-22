#!/bin/sh
set -eu

course_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
target_dir=${GEN_IMAGE_RESTORE_ROOT:-$course_dir}
backup_dir="$course_dir/_backup/2026-10-22-pre-deep-review-fixes"

mkdir -p "$target_dir/_workshop"
cp "$backup_dir/workshop-2h-poster-social.html" "$target_dir/workshop-2h-poster-social.html"
cp "$backup_dir/AI生圖到設計完稿-2h.md" "$target_dir/_workshop/AI生圖到設計完稿-2h.md"
cp "$backup_dir/AI生圖到設計完稿-2h-content-review.md" "$target_dir/_workshop/AI生圖到設計完稿-2h-content-review.md"
cp "$backup_dir/AI生圖到設計完稿-2h-image-manifest.md" "$target_dir/_workshop/AI生圖到設計完稿-2h-image-manifest.md"

printf '%s\n' 'Deep Review fixes restored.'
