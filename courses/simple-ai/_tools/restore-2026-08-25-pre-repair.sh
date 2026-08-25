#!/bin/zsh
set -euo pipefail

COURSE_DIR="${0:A:h}/.."
BACKUP_DIR="$COURSE_DIR/_backup/2026-08-25-pre-repair"

if [[ ! -d "$BACKUP_DIR" ]]; then
  print -u2 "找不到備份：$BACKUP_DIR"
  exit 1
fi

while IFS= read -r rel; do
  [[ -z "$rel" ]] && continue
  mkdir -p "$COURSE_DIR/${rel:h}"
  cp "$BACKUP_DIR/$rel" "$COURSE_DIR/$rel"
done <<'EOF'
index.html
CH1-1.html
CH1-2.html
CH1-3.html
CH1-4.html
CH2-1.html
CH2-2.html
CH2-3.html
CH2-4.html
handbook.html
assets/創業-AI-實戰手冊.pdf
assets/創業-AI-實戰-10則Prompt精選.pdf
assets/datasets/ch1-3-ef02-quotation-set.txt
assets/datasets/ch1-3-ef04-letter-scenarios.txt
assets/datasets/ch1-3-photo-assets.txt
assets/datasets/ch1-4-security-checklist.txt
assets/datasets/ch2-2-positioning-input.txt
assets/datasets/ch2-3-social-content-pack.txt
assets/datasets/ch2-4-faq-material-pack.txt
EOF

if [[ -f "$BACKUP_DIR/outlines/simple-ai.md" ]]; then
  cp "$BACKUP_DIR/outlines/simple-ai.md" "$COURSE_DIR/../../_outlines/simple-ai.md"
  cp "$BACKUP_DIR/outlines/simple-ai.style-guide.md" "$COURSE_DIR/../../_outlines/simple-ai.style-guide.md"
fi

print "已還原 2026-08-25 修復範圍。"
