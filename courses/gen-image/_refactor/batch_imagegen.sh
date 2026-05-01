#!/bin/bash
# 批次 imagegen 11 張剩餘圖片（A2-A6 + C1-C6）
# 每張順序跑、每張 reset-quota、預期總耗時 14-30 min

set -e
BRIDGE="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/ai-orchestration/codex_bridge.py"
IMG_DIR="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gen-image/img"
PROMPT_DIR="/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gen-image/_refactor/prompts"

mkdir -p "$PROMPT_DIR"

run_one() {
  local id=$1 size=$2 fname=$3 prompt_file=$4
  echo "═══ $id imagegen 開始 ═══"
  python3 "$BRIDGE" \
    --task imagegen \
    --prompt "$(cat $prompt_file)" \
    --out "$IMG_DIR/$fname" \
    --size "$size" \
    --reset-quota --yes 2>&1 | tail -3
  echo ""
}

# 逐張跑（prompt 從 Python 腳本內讀）
python3 - <<'PYEOF'
import sys
sys.path.insert(0, '/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gen-image/_refactor')
from gen_ch6_cards import CARDS
from pathlib import Path

PROMPT_DIR = Path('/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gen-image/_refactor/prompts')
PROMPT_DIR.mkdir(exist_ok=True)

for c in CARDS:
    if c['id'] == 'A1': continue  # already done
    f = PROMPT_DIR / f"{c['id']}.txt"
    f.write_text(c['prompt_full'], encoding='utf-8')

print("Prompts written")
PYEOF

# 接著用 bash 跑 11 個 imagegen 順序
SIZES=(
  "A2:1024x1024"
  "A3:1024x1280"
  "A4:1024x1280"
  "A5:1792x1024"
  "A6:1792x1024"
  "C1:1024x1280"
  "C2:1024x1280"
  "C3:1024x1280"
  "C4:1024x1280"
  "C5:1024x1024"
  "C6:1024x1280"
)

FILES=(
  "A2:v52-a2-campaign-kv.png"
  "A3:v53-a3-brand-poster.png"
  "A4:v54-a4-editorial-cover.png"
  "A5:v55-a5-brand-identity-board.png"
  "A6:v56-a6-bilingual-layout.png"
  "C1:v57-c1-bento-grid.png"
  "C2:v58-c2-comparison.png"
  "C3:v59-c3-step-by-step.png"
  "C4:v60-c4-founder-portrait.png"
  "C5:v61-c5-sticker-set.png"
  "C6:v62-c6-lookbook-grid.png"
)

for entry in "${FILES[@]}"; do
  id=${entry%%:*}
  fname=${entry##*:}
  size=$(echo "${SIZES[@]}" | tr ' ' '\n' | grep "^${id}:" | cut -d: -f2)
  prompt_file="$PROMPT_DIR/$id.txt"
  run_one "$id" "$size" "$fname" "$prompt_file"
done

echo "═══ 全部完成 ═══"
