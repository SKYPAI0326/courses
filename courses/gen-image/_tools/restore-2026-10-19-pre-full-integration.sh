#!/usr/bin/env bash
set -euo pipefail

course_dir="$(cd "$(dirname "$0")/.." && pwd -P)"
repo_root="$(cd "$course_dir/../.." && pwd -P)"
backup_dir="$course_dir/_backup/2026-10-19-pre-full-integration"
before_list="$backup_dir/BEFORE-SHA256.tsv"
new_list="$backup_dir/NEW-FILES.tsv"

if [[ ! -f "$before_list" || ! -f "$new_list" ]]; then
  echo "restore evidence missing: $backup_dir" >&2
  exit 1
fi

while IFS=$'\t' read -r relative_path expected_sha; do
  [[ "$relative_path" == "path" ]] && continue
  case "$relative_path" in
    courses/gen-image/*|_lessons/gen-image/*|_outlines/gen-image.md|_outlines/gen-image.style-guide.md) ;;
    *) echo "refusing unexpected restore path: $relative_path" >&2; exit 1 ;;
  esac
  source_path="$backup_dir/$relative_path"
  target_path="$repo_root/$relative_path"
  [[ -f "$source_path" ]] || { echo "backup missing: $relative_path" >&2; exit 1; }
  mkdir -p "$(dirname "$target_path")"
  cp -p "$source_path" "$target_path"
  actual_sha="$(shasum -a 256 "$target_path" | awk '{print $1}')"
  [[ "$actual_sha" == "$expected_sha" ]] || { echo "restore hash mismatch: $relative_path" >&2; exit 1; }
done < "$before_list"

while IFS= read -r relative_path; do
  [[ "$relative_path" == "path" ]] && continue
  case "$relative_path" in
    courses/gen-image/*|_lessons/gen-image/*|_outlines/gen-image.md|_outlines/gen-image.style-guide.md) ;;
    *) echo "refusing unexpected removal path: $relative_path" >&2; exit 1 ;;
  esac
  target_path="$repo_root/$relative_path"
  [[ -e "$target_path" ]] && rm -f -- "$target_path"
done < "$new_list"

echo "restore complete: 56 existing targets restored; 138 integration-only targets removed"
