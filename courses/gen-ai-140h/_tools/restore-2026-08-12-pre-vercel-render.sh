#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
BACKUP_ROOT="$REPO_ROOT/courses/gen-ai-140h/_backup/2026-08-12-pre-vercel-render"

restore_one() {
  local relative_path="$1"
  local source_path="$BACKUP_ROOT/$relative_path"
  local destination_path="$REPO_ROOT/$relative_path"

  if [[ ! -f "$source_path" ]]; then
    echo "Missing backup: $source_path" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$destination_path")"
  cp "$source_path" "$destination_path"
  echo "Restored: $relative_path"
}

restore_one "_outlines/gen-ai-140h.md"
restore_one "courses/gen-ai-140h/fun-apps.html"
restore_one "courses/gen-ai-140h/index.html"
restore_one "courses/gen-ai-140h/my-progress.html"
restore_one "courses/gen-ai-140h/part4/CH4-3.html"
restore_one "courses/gen-ai-140h/part4/PRAC4-4.html"
restore_one "courses/gen-ai-140h/part5/CH5-3.html"
restore_one "courses/gen-ai-140h/part5/CH5-4.html"
restore_one "courses/gen-ai-140h/part5/PRAC5-1.html"
restore_one "courses/gen-ai-140h/part5/PRAC5-2.html"
restore_one "courses/gen-ai-140h/part5/PRAC5-3.html"
restore_one "courses/gen-ai-140h/part5/PRAC5-4.html"
restore_one "courses/gen-ai-140h/part5/PRAC5-15.html"
restore_one "courses/gen-ai-140h/part5/PRAC5-16.html"
restore_one "courses/gen-ai-140h/part6/CH6-2.html"
restore_one "courses/gen-ai-140h/part7/CH7-2.html"
restore_one "courses/gen-ai-140h/part7/CH7-4.html"
restore_one "courses/gen-ai-140h/part7/PRAC7-1.html"
restore_one "courses/gen-ai-140h/part7/PRAC7-4.html"
restore_one "courses/gen-ai-140h/part7/PRAC7-5.html"

echo "Restore complete: 20 files"
