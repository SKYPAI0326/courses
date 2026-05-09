#!/usr/bin/env bash
# audit-gates.sh —— 偵測課程頁面密碼關卡的常見 bug
#
# 用法（從 repo 根目錄執行）：
#   bash docs/audit-gates.sh
#
# v2 修補（依 Codex 2026-05-09 review）：
#   - audit 2 改成「gate invariant」：有 _gate 必須剛好 1 個 _gs（不只是 ≥2）
#   - audit 3 改用 process substitution + null delimiter，避免 here-string 沙箱失敗
#   - placeholder regex 加 __GATE_*_PLACEHOLDER__ / TODO_HASH 等變體
#   - audit 4 抓更廣的「if 內含 hex 與 || 但無單純 hex===H」模式
#   - find 改 -print0 處理空白檔名
#   - 加 set -uo pipefail（不 -e 因 grep 無 match 會 exit 1）
#
# Exit codes：0 = 沒問題；1 = 找到至少一個 issue

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1

ISSUES=0

echo "▶ Audit 1: PLACEHOLDER hash / key 殘留"
HITS=$(grep -rln -E 'PLACEHOLDER_HASH|TODO_HASH|XXX_HASH|FIXME_HASH|__GATE_[A-Z]+_PLACEHOLDER__|YOUR_HASH_HERE' courses/ 2>/dev/null || true)
if [[ -n "$HITS" ]]; then
  echo "$HITS" | sed 's/^/  ✗ /'
  ISSUES=$((ISSUES + $(echo "$HITS" | wc -l)))
else
  echo "  ✓ 無 placeholder 殘留"
fi
echo ""

echo "▶ Audit 2: Gate invariant (id=\"_gate\" 對應的 <style id=\"_gs\"> 必須剛好 1 個)"
INVARIANT_ISSUES=""
while IFS= read -r -d '' f; do
  ge=$(grep -c 'id="_gate"' "$f" 2>/dev/null) || ge=0
  gs=$(grep -c '<style id="_gs">' "$f" 2>/dev/null) || gs=0
  if [[ "$ge" -ge 1 && "$gs" -ne 1 ]]; then
    INVARIANT_ISSUES+="  ✗ $f: gate_div=$ge style_block=$gs (style 應 = 1)"$'\n'
  fi
done < <(find courses -name '*.html' -type f -print0)
if [[ -n "$INVARIANT_ISSUES" ]]; then
  printf '%s' "$INVARIANT_ISSUES"
  ISSUES=$((ISSUES + $(printf '%s' "$INVARIANT_ISSUES" | grep -c '✗')))
else
  echo "  ✓ 全站 gate invariant 通過"
fi
echo ""

echo "▶ Audit 3: K key 不一致 inject_gate.py"
MISMATCH=""
while IFS= read -r line; do
  slug=$(echo "$line" | awk -F'"' '{print $2}')
  expected_key=$(echo "$line" | awk -F'"' '{print $4}')
  if [[ -z "$slug" || -z "$expected_key" || ! -d "courses/$slug" ]]; then continue; fi
  while IFS= read -r -d '' f; do
    keys=$(grep -oE "K='[^']*'" "$f" 2>/dev/null | sort -u | sed -E "s/K='([^']*)'/\\1/")
    if [[ -z "$keys" ]]; then continue; fi
    while IFS= read -r k; do
      if [[ -n "$k" && "$k" != "$expected_key" ]]; then
        MISMATCH+="  ✗ $f: K='$k' (expected '$expected_key')"$'\n'
      fi
    done < <(printf '%s\n' "$keys")
  done < <(find "courses/$slug" -name '*.html' -type f -print0)
done < <(grep -E '^\s*"[^"]+":\s*\("[^"]+",' inject_gate.py)
if [[ -n "$MISMATCH" ]]; then
  printf '%s' "$MISMATCH"
  ISSUES=$((ISSUES + $(printf '%s' "$MISMATCH" | grep -c '✗')))
else
  echo "  ✓ 所有 K 一致"
fi
echo ""

echo "▶ Audit 4: 密碼驗證安全漏洞（gate script 內任何密碼通過）"
# 精準抓：同一行內同含 'crypto.subtle.digest' (gate 特徵) + 任一繞過模式
# 這樣排除學員進度頁、課程內容頁的 v.length 偽陽性
HITS=$(grep -rlnE "crypto\.subtle\.digest.*(v\.length|v\.trim|!!v|v!=='')" courses/ 2>/dev/null || true)
HITS2=$(grep -rln 'hex===H||' courses/ 2>/dev/null || true)
HITS3=$(grep -rln 'hex !== H ||' courses/ 2>/dev/null || true)
ALL_HITS=$(printf '%s\n%s\n%s' "$HITS" "$HITS2" "$HITS3" | sort -u | grep -v '^$' || true)
if [[ -n "$ALL_HITS" ]]; then
  echo "$ALL_HITS" | sed 's/^/  ✗ /'
  ISSUES=$((ISSUES + $(echo "$ALL_HITS" | wc -l)))
else
  echo "  ✓ gate script 無安全漏洞模式"
fi
echo ""

echo "═══ 總結 ═══"
if [[ $ISSUES -eq 0 ]]; then
  echo "✓ 全站 gate 配置乾淨"
  exit 0
else
  echo "✗ 找到 $ISSUES 個 gate-related issue"
  exit 1
fi
