#!/bin/bash
# Preflight 檢查：確認執行環境健全
#
# 用法：bash preflight.sh
#
# 退出碼：
#   0 = 全綠（OK）
#   1 = 嚴重缺漏（不可繼續）
#   2 = 部分降級（Codex 不可用、進入 DEGRADED_MANUAL_REVIEW_REQUIRED 模式）

set -e

# ─── 環境變數（必要設定；不猜測個人目錄）───
: "${COURSE_WEB_ROOT:?COURSE_WEB_ROOT must be set}"
: "${COURSE_VALIDATOR_SSOT:?COURSE_VALIDATOR_SSOT must be set}"
: "${CODEX_BRIDGE_DIR:?CODEX_BRIDGE_DIR must be set}"
export COURSE_WEB_ROOT COURSE_VALIDATOR_SSOT CODEX_BRIDGE_DIR
export CODEX_WORKFLOW_JSON="${CODEX_WORKFLOW_JSON:-$HOME/.claude/orchestration/codex_workflow.json}"

PASS=0
WARN=0
FAIL=0
DEGRADED=0

ok() { echo "  ✓ $1"; PASS=$((PASS+1)); }
warn() { echo "  ⚠ $1"; WARN=$((WARN+1)); }
fail() { echo "  ✗ $1"; FAIL=$((FAIL+1)); }

echo "═══ course-validator preflight ═══"
echo ""

# ─── 1. 環境變數 ───
echo "─── 環境變數 ───"
for var in COURSE_WEB_ROOT COURSE_VALIDATOR_SSOT CODEX_BRIDGE_DIR; do
  val="${!var}"
  if [ -d "$val" ]; then
    ok "$var = $val"
  else
    fail "$var 指向不存在：$val"
  fi
done
echo ""

# ─── 2. 必要工具 ───
echo "─── 必要工具 ───"
command -v python3 >/dev/null && ok "python3 found" || fail "python3 missing"
command -v grep >/dev/null && ok "grep found" || fail "grep missing"

# 把 npm global path 加入後再檢
export PATH="$HOME/.npm-global/bin:$PATH"
if command -v codex >/dev/null; then
  ok "codex CLI found ($(which codex))"
else
  warn "codex CLI 找不到（會進入 DEGRADED 模式）"
  DEGRADED=1
fi
echo ""

# ─── 3. 既有專案檔案 ───
echo "─── 既有專案檔案 ───"
[ -f "$COURSE_WEB_ROOT/docs/lint-page.py" ] && ok "lint-page.py" || fail "lint-page.py 找不到"
[ -f "$CODEX_BRIDGE_DIR/codex_bridge.py" ] && ok "codex_bridge.py" || fail "codex_bridge.py 找不到"
[ -f "$CODEX_WORKFLOW_JSON" ] && ok "codex_workflow.json" || warn "codex_workflow.json 找不到（DEGRADED）"
echo ""

# ─── 4. Codex 啟用真檢（讀 JSON 不用 grep）───
echo "─── Codex 啟用狀態 ───"
if [ -f "$CODEX_WORKFLOW_JSON" ]; then
  CODEX_ENABLED=$(python3 -c "
import json, sys
try:
    with open('$CODEX_WORKFLOW_JSON') as f:
        cfg = json.load(f)
    print('true' if cfg.get('enabled') else 'false')
except Exception as e:
    print(f'error:{e}', file=sys.stderr)
    print('false')
" 2>/dev/null)

  if [ "$CODEX_ENABLED" = "true" ]; then
    ok "Codex enabled: true"
  else
    warn "Codex enabled: $CODEX_ENABLED（DEGRADED：L4a/L4b/L5 進入手動模式）"
    DEGRADED=1
  fi
else
  DEGRADED=1
fi
echo ""

# ─── 5. SSOT 方法論索引 ───
echo "─── SSOT 方法論索引 ───"
for f in 00-架構總覽.md 06-修補手冊.md 07-Codex-consult-template-library.md _templates _case-studies; do
  if [ -e "$COURSE_VALIDATOR_SSOT/$f" ]; then
    ok "SSOT/$f"
  else
    warn "SSOT/$f 找不到"
  fi
done

# 5b：templates SSOT 必存（manifest 指向）
echo "─── SSOT templates（不雙存）───"
for f in L0-truth-table-template.py L4a-consult-template.txt L4b-sentinel-template.txt L5-persona-template.txt FINAL-REPORT-template.md; do
  if [ -f "$COURSE_VALIDATOR_SSOT/_templates/$f" ]; then
    ok "SSOT/_templates/$f"
  else
    fail "SSOT/_templates/$f 找不到（skill 沒備援複本、必須修 SSOT）"
  fi
done
echo ""

# ─── 6. 課程目錄（若有指定 slug）───
if [ -n "$1" ]; then
  SLUG=$1
  echo "─── 課程：$SLUG ───"
  COURSE_DIR="$COURSE_WEB_ROOT/courses/$SLUG"
  if [ -d "$COURSE_DIR" ]; then
    ok "course directory: $COURSE_DIR"

    [ -d "$COURSE_DIR/assets/datasets" ] && ok "datasets/" || warn "datasets/ 不存在（純概念課？）"
    [ -f "$COURSE_WEB_ROOT/_outlines/$SLUG.md" ] && ok "大綱 _outlines/$SLUG.md" || warn "大綱不存在"

    mkdir -p "$COURSE_DIR/_validation"
    if [ -w "$COURSE_DIR/_validation" ]; then
      ok "_validation/ 可寫"
    else
      fail "_validation/ 不可寫"
    fi
  else
    fail "課程目錄不存在：$COURSE_DIR"
  fi
  echo ""
fi

# ─── 結算 ───
echo "═══ 結算 ═══"
echo "  PASS: $PASS"
echo "  WARN: $WARN"
echo "  FAIL: $FAIL"
echo ""

if [ $FAIL -gt 0 ]; then
  echo "❌ 嚴重缺漏 $FAIL 條，不可繼續。"
  exit 1
elif [ $DEGRADED -gt 0 ]; then
  echo "⚠ 進入 DEGRADED_MANUAL_REVIEW_REQUIRED 模式：L0-L3 可跑，L4a/L4b/L5 改產 prompt 檔給人類手動跑 Codex。"
  echo "ENV 已設定：COURSE_WEB_ROOT / COURSE_VALIDATOR_SSOT / CODEX_BRIDGE_DIR"
  exit 2
else
  echo "✅ 全綠，可開跑 7 層驗證。"
  echo "ENV 已設定：COURSE_WEB_ROOT / COURSE_VALIDATOR_SSOT / CODEX_BRIDGE_DIR"
  exit 0
fi
