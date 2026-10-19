#!/usr/bin/env bash
set -euo pipefail

course_dir="$(cd "$(dirname "$0")/.." && pwd -P)"
backup_dir="$course_dir/_backup/2026-10-19-pre-webp-previews"
before_list="$backup_dir/BEFORE-SHA256.tsv"
webp_list="$backup_dir/NEW-WEBP.tsv"

[[ -f "$before_list" && -f "$webp_list" ]] || {
  echo "restore evidence missing: $backup_dir" >&2
  exit 1
}

while IFS=$'\t' read -r relative_path expected_sha; do
  [[ "$relative_path" == "path" ]] && continue
  case "$relative_path" in
    *.html|_tools/verify-image-refresh.py) ;;
    *) echo "refusing unexpected restore path: $relative_path" >&2; exit 1 ;;
  esac
  source_path="$backup_dir/$relative_path"
  target_path="$course_dir/$relative_path"
  [[ -f "$source_path" ]] || { echo "backup missing: $relative_path" >&2; exit 1; }
  mkdir -p "$(dirname "$target_path")"
  cp -p "$source_path" "$target_path"
  actual_sha="$(shasum -a 256 "$target_path" | awk '{print $1}')"
  [[ "$actual_sha" == "$expected_sha" ]] || {
    echo "restore hash mismatch: $relative_path" >&2
    exit 1
  }
done < "$before_list"

while IFS= read -r relative_path; do
  [[ "$relative_path" == "path" ]] && continue
  case "$relative_path" in
    assets/*.webp|assets/*/*.webp|assets/*/*/*.webp|img/*/*.webp) ;;
    *) echo "refusing unexpected WebP path: $relative_path" >&2; exit 1 ;;
  esac
  target_path="$course_dir/$relative_path"
  [[ -e "$target_path" ]] && rm -f -- "$target_path"
done < "$webp_list"

rm -f -- "$course_dir/_tools/webp_previews.py" "$course_dir/_tools/test_webp_previews.py"

echo "restore complete: 30 files restored; 61 WebP previews and new preview tools removed"
