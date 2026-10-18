#!/bin/bash
# Codex consult 包裝：自動 parse Call ID 與評分、寫 status.jsonl
#
# 用法：bash codex-consult-wrapper.sh <prompt-file> <layer> [case-id]
#   <prompt-file>  /tmp/codex-l4a-case2.txt 之類
#   <layer>        L4a / L4b / L5
#   [case-id]      e.g. "case2c" / "platform" / "persona"
#
# 環境變數：
#   CODEX_BRIDGE_DIR    Codex bridge 目錄（自動 default）
#   COURSE_WEB_ROOT     課程根目錄
#   VALIDATOR_SLUG      課程 slug（用於 status.jsonl 路徑）
#
# 退出碼：
#   0 = 成功跑完、有 Call ID
#   1 = 參數錯誤
#   2 = Codex 跑失敗（DEGRADED）
#   3 = 沒抓到 Call ID（DEGRADED）

set -eo pipefail

PROMPT_FILE="${1:-}"
LAYER="${2:-}"
CASE_ID="${3:-default}"

if [ -z "$PROMPT_FILE" ] || [ ! -f "$PROMPT_FILE" ] || [ -z "$LAYER" ]; then
  echo "用法：bash codex-consult-wrapper.sh <prompt-file> <layer> [case-id]" >&2
  exit 1
fi

export PATH="$HOME/.npm-global/bin:$PATH"
CODEX_BRIDGE_DIR="${CODEX_BRIDGE_DIR:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/ai-orchestration}"
COURSE_WEB_ROOT="${COURSE_WEB_ROOT:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁}"

if [ ! -d "$CODEX_BRIDGE_DIR" ]; then
  echo "❌ Codex bridge 找不到：$CODEX_BRIDGE_DIR" >&2
  exit 2
fi

cd "$CODEX_BRIDGE_DIR"

# ─── 跑 consult ───
set +e
RAW_OUTPUT=$(python3 codex_bridge.py --task consult --prompt "$(cat "$PROMPT_FILE")" 2>&1)
CODEX_EXIT=$?
set -e

if [ $CODEX_EXIT -ne 0 ]; then
  echo "❌ Codex consult 失敗（exit=$CODEX_EXIT）" >&2
  echo "$RAW_OUTPUT" >&2
  exit 2
fi

# ─── 抽 Call ID（多 pattern fallback）───
CALL_ID=$(echo "$RAW_OUTPUT" | grep -oE 'consult \[[a-f0-9]{8,}\]' | head -1 | sed 's/consult \[\(.*\)\]/\1/' || true)
if [ -z "$CALL_ID" ]; then
  CALL_ID=$(echo "$RAW_OUTPUT" | grep -oE '\[[a-f0-9]{8,}\]' | head -1 | tr -d '[]' || true)
fi
if [ -z "$CALL_ID" ]; then
  CALL_ID=$(echo "$RAW_OUTPUT" | grep -oE 'mark-verdict [a-f0-9]{8,}' | head -1 | awk '{print $2}' || true)
fi

if [ -z "$CALL_ID" ]; then
  echo "⚠ 沒抓到 Call ID（DEGRADED）。完整輸出：" >&2
  echo "$RAW_OUTPUT" >&2
  exit 3
fi

# ─── 抽評分（多 pattern fallback）───
SCORE=""
for pattern in 'Verdict[:：]\s*\*?\*?\s*[0-9.]+/10' 'verdict[:：]\s*[0-9.]+/10' '[0-9]+(\.[0-9])?/10'; do
  SCORE=$(echo "$RAW_OUTPUT" | grep -oiE "$pattern" | head -1 || true)
  if [ -n "$SCORE" ]; then break; fi
done

# ─── 存原始輸出 ───
OUTFILE="/tmp/codex-output-${LAYER}-${CASE_ID}-${CALL_ID}.md"
echo "$RAW_OUTPUT" > "$OUTFILE"

# ─── 寫 status.jsonl（用 Python helper，避免 shell 拼接破 JSON）───
if [ -n "${VALIDATOR_SLUG:-}" ]; then
  STATUS_FILE="$COURSE_WEB_ROOT/courses/$VALIDATOR_SLUG/_validation/status.jsonl"
  RUN_ID_FILE="$COURSE_WEB_ROOT/courses/$VALIDATOR_SLUG/_validation/.current-run-id"
  mkdir -p "$(dirname "$STATUS_FILE")"

  # 取得 run_id（從 env 或 file，沒有就 fallback）
  RUN_ID="${VALIDATOR_RUN_ID:-}"
  if [ -z "$RUN_ID" ] && [ -f "$RUN_ID_FILE" ]; then
    RUN_ID=$(cat "$RUN_ID_FILE")
  fi
  if [ -z "$RUN_ID" ]; then
    RUN_ID="r-$(date '+%Y%m%d-%H%M%S')-wrapper-orphan"
  fi

  SKILL_DIR="${SKILL_DIR:-$HOME/.agents/skills/course-validator}"
  python3 "$SKILL_DIR/scripts/status_write.py" \
    "$STATUS_FILE" "$RUN_ID" "$LAYER" "$CASE_ID" "PENDING_VERDICT" \
    "call_id=$CALL_ID" \
    "score=$SCORE" \
    "verdict=pending" \
    "output_file=$OUTFILE" \
    "prompt_file=$PROMPT_FILE" > /dev/null
fi

echo "═══ Codex Consult 完成 ═══"
echo "Layer:     $LAYER"
echo "Case ID:   $CASE_ID"
echo "Call ID:   $CALL_ID"
echo "評分:      $SCORE"
echo "輸出存檔:  $OUTFILE"
if [ -n "${VALIDATOR_SLUG:-}" ]; then
  echo "Status:    $COURSE_WEB_ROOT/courses/$VALIDATOR_SLUG/_validation/status.jsonl"
fi
echo ""
echo "請執行 mark-verdict："
echo "  python3 $CODEX_BRIDGE_DIR/codex_bridge.py --mark-verdict $CALL_ID --verdict {accepted|actionable|noise|rejected}"
