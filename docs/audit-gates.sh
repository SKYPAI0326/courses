#!/usr/bin/env bash
# audit-gates.sh —— 偵測課程頁面密碼關卡的常見 bug
#
# 用法（從 repo 根目錄執行）：
#   bash docs/audit-gates.sh
#
# 偵測項目：
#   1. PLACEHOLDER_HASH / TODO_HASH / XXX_HASH 字面字串（course-web-builder 沒被 inject_gate 覆蓋的情況）
#   2. 雙重 gate（同頁多個 <style id="_gs"> 或 <script> 含 K=...）
#   3. K mismatch：頁面 K 跟 inject_gate.py COURSES dict 不一致
#   4. 安全漏洞：v.length>0 / |v|| 等讓任何密碼通過的字串
#
# Exit codes：
#   0 = 沒問題
#   1 = 找到至少一個 issue

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1

ISSUES=0

echo "▶ Audit 1: PLACEHOLDER_HASH / TODO_HASH / XXX_HASH 殘留"
HITS=$(grep -rln -E 'PLACEHOLDER_HASH|TODO_HASH|XXX_HASH|FIXME_HASH' courses/ 2>/dev/null)
if [[ -n "$HITS" ]]; then
  echo "$HITS" | sed 's/^/  ✗ /'
  ISSUES=$((ISSUES + $(echo "$HITS" | wc -l)))
else
  echo "  ✓ 無 placeholder hash 殘留"
fi
echo ""

echo "▶ Audit 2: 雙重 gate（同頁多個 <style id=\"_gs\">）"
DUP_STYLE=$(for f in $(find courses -name '*.html'); do
  c=$(grep -c '<style id="_gs">' "$f")
  if [[ $c -gt 1 ]]; then echo "  ✗ $f: $c 個 <style id=\"_gs\">"; fi
done)
if [[ -n "$DUP_STYLE" ]]; then
  echo "$DUP_STYLE"
  ISSUES=$((ISSUES + $(echo "$DUP_STYLE" | wc -l)))
else
  echo "  ✓ 無雙重 style block"
fi
echo ""

echo "▶ Audit 3: K key 不一致 inject_gate.py"
MISMATCH=""
while IFS= read -r line; do
  slug=$(echo "$line" | awk -F'"' '{print $2}')
  expected_key=$(echo "$line" | awk -F'"' '{print $4}')
  if [[ -z "$slug" || -z "$expected_key" ]]; then continue; fi
  if [[ ! -d "courses/$slug" ]]; then continue; fi
  WRONG=$(grep -rln "const K='[^']*'" "courses/$slug/" 2>/dev/null | while read -r f; do
    keys=$(grep -oE "K='[^']*'" "$f" | sort -u | tr -d "'" | sed 's/K=//g')
    while IFS= read -r k; do
      if [[ -n "$k" && "$k" != "$expected_key" ]]; then
        echo "  ✗ $f: K='$k' (expected '$expected_key')"
      fi
    done <<< "$keys"
  done)
  if [[ -n "$WRONG" ]]; then
    MISMATCH+="$WRONG"$'\n'
  fi
done < <(grep -E '^\s*"[^"]+":\s*\("[^"]+",' inject_gate.py)
if [[ -n "$MISMATCH" ]]; then
  echo "$MISMATCH" | grep -v '^$'
  ISSUES=$((ISSUES + $(echo "$MISMATCH" | grep -c '✗')))
else
  echo "  ✓ 所有 K 一致"
fi
echo ""

echo "▶ Audit 4: 密碼驗證安全漏洞（v.length>0 / 任何密碼通過）"
SECURITY=$(grep -rln -E 'hex===H\|\|v\.length|hex===H\|\|v ' courses/ 2>/dev/null)
if [[ -n "$SECURITY" ]]; then
  echo "$SECURITY" | sed 's/^/  ✗ /'
  ISSUES=$((ISSUES + $(echo "$SECURITY" | wc -l)))
else
  echo "  ✓ 無已知安全漏洞模式"
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
