#!/bin/bash
# course-validator 總入口
#
# 用法：
#   bash course-validator.sh <slug>              # 跑完整 7 層
#   bash course-validator.sh <slug> <layer>      # 只跑某層
#   bash course-validator.sh <slug> status       # 顯示目前進度
#   bash course-validator.sh <slug> report       # 從 status 生成 FINAL-REPORT（含 gate）
#
# Layer:
#   preflight | L0 | L1-L3 | L4a | L4b | L5 | status | report | all
#
# 環境變數：
#   COURSE_WEB_ROOT, COURSE_VALIDATOR_SSOT, CODEX_BRIDGE_DIR
#   VALIDATOR_KEYWORDS         L2 grep 用的關鍵字（pipe-separated）
#   VALIDATOR_RUN_ID           覆寫自動 run_id（避免每次新 run）
#
# 退出碼：
#   0 = OK
#   1 = 參數錯誤
#   2 = preflight FAIL（不可繼續）
#   3 = DEGRADED（L4-L5 進手動模式）
#   4 = report gate 失敗（不可交付）

set -eo pipefail

SLUG="${1:-}"
LAYER="${2:-all}"
case "$LAYER" in
  L0|L1-L3|L4a|L4b|L5) ;;
  *) echo "舊流程僅保留 L0/L1-L3/L4a/L4b/L5；請使用 course-validator.sh 的本機報告入口。"; exit 2 ;;
esac
if [[ ! "$SLUG" =~ ^[A-Za-z0-9][A-Za-z0-9_-]*$ ]]; then echo "invalid slug"; exit 2; fi

if [ -z "$SLUG" ]; then
  echo "用法：bash course-validator.sh <slug> [layer]"
  echo "Layer: preflight | L0 | L1-L3 | L4a | L4b | L5 | status | report | all"
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export COURSE_WEB_ROOT="${COURSE_WEB_ROOT:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁}"
export COURSE_VALIDATOR_SSOT="${COURSE_VALIDATOR_SSOT:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程檢核系統}"
export CODEX_BRIDGE_DIR="${CODEX_BRIDGE_DIR:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/ai-orchestration}"
export VALIDATOR_SLUG="$SLUG"

COURSE_DIR="$COURSE_WEB_ROOT/courses/$SLUG"
STATUS_FILE="$COURSE_DIR/_validation/status.jsonl"
RUN_ID_FILE="$COURSE_DIR/_validation/.current-run-id"
mkdir -p "$COURSE_DIR/_validation"

# ─── run_id 機制 ───
if [ -n "${VALIDATOR_RUN_ID:-}" ]; then
  RUN_ID="$VALIDATOR_RUN_ID"
elif [ "$LAYER" = "all" ] || [ "$LAYER" = "preflight" ]; then
  # 新一輪驗收：產生新 run_id
  RUN_ID="r-$(date '+%Y%m%d-%H%M%S')"
  echo "$RUN_ID" > "$RUN_ID_FILE"
elif [ -f "$RUN_ID_FILE" ]; then
  RUN_ID=$(cat "$RUN_ID_FILE")
else
  # 沒有 run_id 又不是新 run，自動建一個（warning）
  RUN_ID="r-$(date '+%Y%m%d-%H%M%S')-orphan"
  echo "$RUN_ID" > "$RUN_ID_FILE"
  echo "⚠ 沒有 current run_id，建立 orphan run：$RUN_ID" >&2
fi
export VALIDATOR_RUN_ID="$RUN_ID"

# ─── status 寫入 helper（用 Python，避免 shell 拼接破 JSON）───
status_log() {
  local layer=$1 case_id=$2 status=$3
  shift 3
  python3 "$SKILL_DIR/scripts/status_write.py" \
    "$STATUS_FILE" "$RUN_ID" "$layer" "$case_id" "$status" "$@" > /dev/null
}

# ─── preflight ───
run_preflight() {
  echo ""
  echo "▶ preflight (run_id=$RUN_ID)"
  set +e
  bash "$SKILL_DIR/scripts/preflight.sh" "$SLUG"
  local exit_code=$?
  set -e
  if [ $exit_code -eq 1 ]; then
    status_log "preflight" "all" "FAIL" "detail=嚴重缺漏"
    exit 2
  fi
  if [ $exit_code -eq 2 ]; then
    status_log "preflight" "all" "DEGRADED" "detail=Codex 不可用、L4-L5 手動模式"
    export VALIDATOR_DEGRADED=1
  else
    status_log "preflight" "all" "OK" "detail=全綠"
  fi
}

# ─── L0 Truth Table ───
run_L0() {
  echo ""
  echo "▶ L0 Truth Table"
  if [ -f "$COURSE_DIR/_validation/L0-generate.py" ]; then
    set +e
    (cd "$COURSE_WEB_ROOT" && python3 "$COURSE_DIR/_validation/L0-generate.py")
    local exit_code=$?
    set -e
    if [ $exit_code -eq 0 ]; then
      status_log "L0" "all" "OK" "detail=truth-table.json 已生成"
    else
      status_log "L0" "all" "FAIL" "detail=L0-generate.py 跑失敗"
      exit 2
    fi
  else
    echo "⚠ L0-generate.py 尚未建立"
    echo "  範本：$SKILL_DIR/scripts/L0-template.py（複製到 _validation/L0-generate.py 改用）"
    status_log "L0" "all" "MANUAL_REQUIRED" "detail=需依本課 dataset 寫 L0-generate.py"
  fi
}

# ─── L1+L2+L3 ───
run_L1_L3() {
  echo ""
  echo "▶ L1+L2+L3"
  set +e
  bash "$SKILL_DIR/scripts/run-L1-L2-L3.sh" "$SLUG" "${VALIDATOR_KEYWORDS:-}"
  local exit_code=$?
  set -e
  case $exit_code in
    0) status_log "L1-L3" "all" "OK" "detail=全綠" ;;
    2) status_log "L1-L3" "all" "FAIL_L1" "detail=L1 BLOCKER (lint)"; exit 2 ;;
    3) status_log "L1-L3" "all" "FAIL_L3" "detail=L3 BLOCKER (5骨架)"; exit 2 ;;
    *) status_log "L1-L3" "all" "ERROR" "detail=exit=$exit_code" ;;
  esac
}

# ─── L4/L5：派發 Codex consult（degraded 時改提示）───
dispatch_codex_layer() {
  local layer=$1 case_id=$2 template_name=$3
  local template_path="$COURSE_VALIDATOR_SSOT/_templates/$template_name"

  echo ""
  echo "▶ $layer / $case_id"
  if [ "${VALIDATOR_DEGRADED:-0}" = "1" ]; then
    echo "⚠ DEGRADED：請手動跑 Codex consult"
    echo "  模板：$template_path"
    status_log "$layer" "$case_id" "DEGRADED_MANUAL" "detail=請手動跑 Codex" "template=$template_path"
  else
    echo "從 $template_path 複製、填入後跑："
    echo "  bash $SKILL_DIR/scripts/codex-consult-wrapper.sh /tmp/codex-$layer.txt $layer $case_id"
    status_log "$layer" "$case_id" "PROMPT_USER" "detail=等待手動填入並跑 wrapper" "template=$template_path"
  fi
}

run_L4a() { dispatch_codex_layer "L4a" "all" "L4a-consult-template.txt"; }
run_L4b() { dispatch_codex_layer "L4b" "platform" "L4b-sentinel-template.txt"; }
run_L5()  { dispatch_codex_layer "L5" "persona" "L5-persona-template.txt"; }

# ─── status 顯示（只看當前 run）───
show_status() {
  if [ ! -f "$STATUS_FILE" ]; then
    echo "（尚無 status，先跑 preflight 或某層）"
    return
  fi
  echo "═══ 進度（$SLUG / run_id=$RUN_ID）═══"
  python3 - <<EOF
import json
from collections import OrderedDict
target_run = "$RUN_ID"
status_by_layer = OrderedDict()
with open("$STATUS_FILE") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
            if r.get('run_id') != target_run:
                continue
            key = f"{r['layer']}/{r['case_id']}"
            status_by_layer[key] = r  # 同層後寫覆蓋
        except Exception as e:
            print(f'  ⚠ JSON parse error: {e}')
for k, v in status_by_layer.items():
    s = v.get('status', '?')
    mark = '✓' if s == 'OK' else ('⚠' if 'DEGRADED' in s or 'MANUAL' in s or 'PROMPT' in s else '⏳' if s == 'PENDING_VERDICT' else '✗')
    score = v.get('score', '')
    detail = v.get('detail', '')
    verdict = v.get('verdict', '')
    extras = []
    if score: extras.append(f"score={score}")
    if verdict and verdict != 'pending': extras.append(f"verdict={verdict}")
    if detail: extras.append(detail)
    extra_str = ' / '.join(extras)
    print(f"  {mark} {k:18s} {s:22s} {extra_str}")
EOF
}

# ─── Report gate（必跑檢查）───
validate_ready_for_report() {
  if [ ! -f "$STATUS_FILE" ]; then
    echo "❌ Report Gate: 沒有 status.jsonl，先跑驗收"
    return 1
  fi

  python3 - <<EOF
import json, sys
target_run = "$RUN_ID"
status_by_key = {}
with open("$STATUS_FILE") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
            if r.get('run_id') != target_run:
                continue
            key = f"{r['layer']}/{r['case_id']}"
            status_by_key[key] = r
        except Exception:
            pass

required = ['preflight/all', 'L0/all', 'L1-L3/all']
errors = []
warnings = []

for req in required:
    if req not in status_by_key:
        errors.append(f"  ✗ {req} 缺（尚未跑）")
    elif status_by_key[req]['status'] not in ('OK',):
        errors.append(f"  ✗ {req} 狀態={status_by_key[req]['status']}（必須 OK）")

# L4a/L4b/L5 至少要有一筆且不是 PROMPT_USER / DEGRADED / pending verdict
for layer in ['L4a', 'L4b', 'L5']:
    layer_records = [v for k, v in status_by_key.items() if k.startswith(f"{layer}/")]
    if not layer_records:
        errors.append(f"  ✗ {layer} 完全沒跑")
        continue
    for v in layer_records:
        s = v.get('status', '?')
        verdict = v.get('verdict', 'pending')
        if s in ('PROMPT_USER', 'DEGRADED_MANUAL', 'MANUAL_REQUIRED'):
            errors.append(f"  ✗ {v['layer']}/{v['case_id']}: 狀態 {s}（仍待手動跑）")
        elif s == 'PENDING_VERDICT' and verdict == 'pending':
            errors.append(f"  ✗ {v['layer']}/{v['case_id']}: verdict 仍 pending（請 mark-verdict）")
        elif s != 'OK' and not s.startswith('PENDING'):
            warnings.append(f"  ⚠ {v['layer']}/{v['case_id']}: 狀態 {s}")

if errors:
    print("❌ Report Gate FAIL — 不可標可交付：")
    for e in errors:
        print(e)
    sys.exit(1)

if warnings:
    print("⚠ Report Gate WARN（會產 DRAFT）：")
    for w in warnings:
        print(w)
    sys.exit(2)

print("MACHINE_CHECKED — 舊分層紀錄齊全，正式驗收請使用 evidence.json")
sys.exit(0)
EOF
}

# ─── report 生成 ───
gen_report() {
  echo "═══ Report Gate 檢查 ═══"
  set +e
  validate_ready_for_report
  local gate_exit=$?
  set -e

  REPORT_FILE="$COURSE_DIR/_validation/FINAL-REPORT.md"

  if [ $gate_exit -eq 1 ]; then
    DRAFT_FILE="$COURSE_DIR/_validation/FINAL-REPORT-DRAFT.md"
    cp "$COURSE_VALIDATOR_SSOT/_templates/FINAL-REPORT-template.md" "$DRAFT_FILE"
    echo ""
    echo "❌ Gate 不通過，產 DRAFT 而非 FINAL：$DRAFT_FILE"
    echo "請完成所有 required 層 + Codex verdict 再跑 report"
    exit 4
  elif [ $gate_exit -eq 2 ]; then
    DRAFT_FILE="$COURSE_DIR/_validation/FINAL-REPORT-DRAFT.md"
    cp "$COURSE_VALIDATOR_SSOT/_templates/FINAL-REPORT-template.md" "$DRAFT_FILE"
    echo ""
    echo "⚠ Gate WARN，產 DRAFT：$DRAFT_FILE"
    echo "確認 warning 後可手動 mv 為 FINAL-REPORT.md"
  else
    cp "$COURSE_VALIDATOR_SSOT/_templates/FINAL-REPORT-template.md" "$REPORT_FILE"
    echo ""
    echo "✅ FINAL-REPORT 已產：$REPORT_FILE"
  fi

  echo ""
  echo "Status 摘要："
  show_status
}

# ─── dispatch ───
case "$LAYER" in
  preflight) run_preflight ;;
  L0) run_preflight; run_L0 ;;
  L1-L3) run_preflight; run_L1_L3 ;;
  L4a) run_preflight; run_L4a ;;
  L4b) run_preflight; run_L4b ;;
  L5) run_preflight; run_L5 ;;
  status) show_status ;;
  report) gen_report ;;
  all)
    run_preflight
    run_L0
    run_L1_L3
    run_L4a
    run_L4b
    run_L5
    show_status
    echo ""
    echo "▶ 所有層已派發。手動跑 Codex consult、mark-verdict 後，跑："
    echo "  bash course-validator.sh $SLUG report"
    ;;
  *)
    echo "❌ 未知 layer：$LAYER"
    echo "支援：preflight | L0 | L1-L3 | L4a | L4b | L5 | status | report | all"
    exit 1
    ;;
esac

echo ""
echo "═══ 完成 ═══"
echo "Run ID: $RUN_ID"
echo "Status: $STATUS_FILE"
