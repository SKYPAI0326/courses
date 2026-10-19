#!/bin/sh
set -eu

course_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
backup_dir="$course_dir/_backup/2026-10-17-pre-standalone-naming"

cp "$backup_dir/workshop-2h-poster-social.html" "$course_dir/workshop-2h-poster-social.html"
cp "$backup_dir/AI生圖到設計完稿-2h.md" "$course_dir/_workshop/AI生圖到設計完稿-2h.md"
cp "$backup_dir/AI生圖到設計完稿-2h-content-review.md" "$course_dir/_workshop/AI生圖到設計完稿-2h-content-review.md"
cp "$backup_dir/AI生圖到設計完稿-2h-image-manifest.md" "$course_dir/_workshop/AI生圖到設計完稿-2h-image-manifest.md"

printf '%s\n' 'Standalone naming repair restored.'
