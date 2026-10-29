#!/bin/bash
# L1+L2+L3 靜態檢查整合 runner
# 用法：bash run-L1-L2-L3.sh <slug> [keywords-to-check-consistency]
#
# 環境變數（可外部覆蓋）：
#   COURSE_WEB_ROOT          課程網頁根目錄
#   COURSE_VALIDATOR_SSOT    驗收方法論 SSOT
#
# 退出碼：
#   0 = 全綠
#   1 = 參數錯誤
#   2 = L1 BLOCKER
#   3 = L3 BLOCKER

set -eo pipefail

SLUG="${1:-}"
KEYWORDS="${2:-}"

if [ -z "$SLUG" ]; then
  echo "用法：bash run-L1-L2-L3.sh <slug> [keywords-to-grep]"
  exit 1
fi

: "${COURSE_WEB_ROOT:?COURSE_WEB_ROOT must be set}"
SKILL_DIR="${SKILL_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

COURSE_DIR="$COURSE_WEB_ROOT/courses/$SLUG"
OUT_DIR="$COURSE_DIR/_validation"
OUT_FILE="$OUT_DIR/L1-L2-L3-static.txt"

mkdir -p "$OUT_DIR"
cd "$COURSE_WEB_ROOT"

{
  echo "═══ L1+L2+L3 靜態檢查 ═══"
  echo "課程：$SLUG"
  echo "時間：$(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
} > "$OUT_FILE"

L1_EXIT=0
L3_EXIT=0

# ─── L1：lint ───
{
  echo "─── L1 lint ───"
} >> "$OUT_FILE"
set +e
python3 docs/lint-page.py "courses/$SLUG/" --summary >> "$OUT_FILE" 2>&1
L1_EXIT=$?
set -e
echo "" >> "$OUT_FILE"

# ─── L2：一致性 grep（無命中是好事，非錯）───
{
  echo "─── L2 一致性 grep ───"
} >> "$OUT_FILE"
if [ -n "$KEYWORDS" ]; then
  echo "Pattern: $KEYWORDS" >> "$OUT_FILE"
  RESULTS=$(grep -rnE "$KEYWORDS" --include="*.html" --include="*.md" "courses/$SLUG/" 2>&1 || true)
  if [ -z "$RESULTS" ]; then
    echo "✓ 無命中（一致性 OK）" >> "$OUT_FILE"
  else
    echo "⚠ 發現命中（需確認是否需修補）：" >> "$OUT_FILE"
    echo "$RESULTS" >> "$OUT_FILE"
  fi
else
  echo "（未指定 keywords，跳過 L2 grep）" >> "$OUT_FILE"
fi
echo "" >> "$OUT_FILE"

# ─── L3：prompt 5 骨架 ───
{
  echo "─── L3 Prompt 5 骨架 ───"
} >> "$OUT_FILE"
PROMPTS_FILES=$(find "courses/$SLUG/assets/datasets/" -name "prompts-*.md" 2>/dev/null || true)
if [ -n "$PROMPTS_FILES" ]; then
  set +e
  python3 "$SKILL_DIR/scripts/L3-prompt-parser.py" $PROMPTS_FILES >> "$OUT_FILE" 2>&1
  L3_EXIT=$?
  set -e
else
  echo "（找不到 prompts-*.md，跳過 L3）" >> "$OUT_FILE"
fi
echo "" >> "$OUT_FILE"

# ─── 結算 ───
{
  echo "═══ 結算 ═══"
  echo "L1 exit: $L1_EXIT"
  echo "L3 exit: $L3_EXIT"
  if [ $L1_EXIT -ne 0 ]; then
    echo "❌ L1 BLOCKER（lint 失敗）"
  fi
  if [ $L3_EXIT -ne 0 ]; then
    echo "❌ L3 BLOCKER（prompt 5 骨架缺）"
  fi
  if [ $L1_EXIT -eq 0 ] && [ $L3_EXIT -eq 0 ]; then
    echo "✅ L1+L2+L3 全綠"
  fi
} >> "$OUT_FILE"

cat "$OUT_FILE"

if [ $L1_EXIT -ne 0 ]; then exit 2; fi
if [ $L3_EXIT -ne 0 ]; then exit 3; fi
exit 0
