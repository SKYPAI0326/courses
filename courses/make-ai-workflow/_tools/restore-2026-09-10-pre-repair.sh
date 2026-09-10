#!/bin/zsh
set -euo pipefail
BASE="$(cd "$(dirname "$0")/../../.." && pwd)"
BACKUP="$BASE/courses/make-ai-workflow/_backup/2026-09-10-pre-repair"

restore() {
  local target_rel="$1"
  local backup_rel="$2"
  mkdir -p "$BASE/$(dirname "$target_rel")"
  cp "$BACKUP/$backup_rel" "$BASE/$target_rel"
}

for f in CH1-1.html CH1-2.html CH1-3.html CH1-4.html CH1-5.html CH1-6.html index.html course-outline.md README.md; do
  restore "courses/make-ai-workflow/$f" "$f"
done
for f in "$BACKUP"/assets/*; do
  [ -f "$f" ] || continue
  restore "courses/make-ai-workflow/assets/$(basename "$f")" "assets/$(basename "$f")"
done
for f in "$BACKUP"/_lessons/*; do
  [ -f "$f" ] || continue
  restore "_lessons/make-ai-workflow/$(basename "$f")" "_lessons/$(basename "$f")"
done
restore "_outlines/make-ai-workflow.md" "make-ai-workflow.md"
printf '%s\n' "Restored make-ai-workflow 2026-09-10 pre-repair scope. Newly added files outside the backup are retained."
