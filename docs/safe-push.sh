#!/usr/bin/env bash
# safe-push.sh —— push 後驗證 origin 收到、檢查 PR race 風險
#
# 用法（從 repo 根目錄執行）：
#   bash docs/safe-push.sh             # 推當前 branch 並驗證
#   bash docs/safe-push.sh --no-push   # 只驗證，不推
#   bash docs/safe-push.sh --pr 76     # 連帶驗證指定 PR 的狀態（防 race after merge）
#
# v2 修補（依 Codex 2026-05-09 review）：
#   - git fetch 失敗改 exit 1（不再只 warn）
#   - 偵測 first-time push 無 upstream → 自動 git push -u
#   - 加 --pr N 選項，能驗證指定 PR（即使已 merge）
#   - 強化錯誤處理：python3/gh 缺失時明確 SKIP 而非 swallow
#
# Exit codes：
#   0 = 同步成功（local == remote）
#   1 = git 操作失敗 / fetch 失敗 / first-push 無 upstream 處理失敗
#   2 = race 偵測（local != remote，或 PR 已 merged 但 head 不含本次 commit）

set -uo pipefail

NO_PUSH=0
PR_NUMBER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-push) NO_PUSH=1; shift ;;
    --pr) PR_NUMBER="$2"; shift 2 ;;
    *) echo "✗ 不認識的參數: $1"; exit 1 ;;
  esac
done

BRANCH=$(git branch --show-current)
[[ -z "$BRANCH" ]] && { echo "✗ 不在 branch 上（detached HEAD?）"; exit 1; }

LOCAL_BEFORE=$(git rev-parse HEAD)
echo "▶ branch: $BRANCH"
echo "▶ local HEAD before push: ${LOCAL_BEFORE:0:7}"

if [[ $NO_PUSH -eq 0 ]]; then
  # 偵測是否 first-time push
  if ! git rev-parse "@{u}" >/dev/null 2>&1; then
    echo "▶ 首次 push 此 branch，使用 git push -u origin $BRANCH"
    git push -u origin "$BRANCH" 2>&1 | sed 's/^/  /'
    PUSH_RC=${PIPESTATUS[0]}
  else
    echo "▶ 執行 git push..."
    git push 2>&1 | sed 's/^/  /'
    PUSH_RC=${PIPESTATUS[0]}
  fi
  [[ $PUSH_RC -ne 0 ]] && { echo "✗ push 失敗 (exit $PUSH_RC)"; exit 1; }
fi

echo "▶ fetch origin/$BRANCH..."
if ! git fetch origin "$BRANCH" --quiet 2>/dev/null; then
  echo "✗ git fetch 失敗（網路問題？權限問題？）"
  exit 1
fi

# 確認 upstream 存在
if ! git rev-parse "@{u}" >/dev/null 2>&1; then
  echo "✗ 沒有 upstream tracking branch（push -u 失敗或被拒？）"
  exit 1
fi

REMOTE=$(git rev-parse "@{u}")
LOCAL_AFTER=$(git rev-parse HEAD)

echo "▶ local HEAD after push:  ${LOCAL_AFTER:0:7}"
echo "▶ remote HEAD:            ${REMOTE:0:7}"

if [[ "$LOCAL_AFTER" == "$REMOTE" ]]; then
  echo "✓ push synced to origin"
else
  echo "✗ RACE detected: local ($LOCAL_AFTER) != remote ($REMOTE)"
  exit 2
fi

# 檢查指定 PR（含 merged 狀態）
if [[ -n "$PR_NUMBER" ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "  ⚠ gh CLI 不可用，SKIP --pr 驗證"
  else
    PR_DATA=$(gh pr view "$PR_NUMBER" --json state,mergedAt,headRefOid 2>/dev/null || echo '')
    if [[ -z "$PR_DATA" ]]; then
      echo "  ⚠ PR #$PR_NUMBER 不存在或 gh 無權限"
    else
      PR_STATE=$(echo "$PR_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin).get('state',''))" 2>/dev/null || echo '')
      PR_HEAD=$(echo "$PR_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin).get('headRefOid',''))" 2>/dev/null || echo '')
      echo ""
      echo "▶ PR #$PR_NUMBER state: $PR_STATE / head: ${PR_HEAD:0:7}"
      if [[ "$PR_HEAD" == "$LOCAL_AFTER" ]]; then
        echo "  ✓ PR HEAD = local HEAD"
      else
        echo "  ✗ PR HEAD ($PR_HEAD) != local HEAD ($LOCAL_AFTER)"
        if [[ "$PR_STATE" == "MERGED" ]]; then
          echo "    🚨 PR 已 merged 但不含本次 commit——使用者按太快，需開新 PR"
        fi
        exit 2
      fi
    fi
  fi
elif command -v gh >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  # 自動偵測 open PR
  PR_INFO=$(gh pr list --head "$BRANCH" --state open --json number,headRefOid,url 2>/dev/null || echo '[]')
  if [[ -n "$PR_INFO" && "$PR_INFO" != "[]" ]]; then
    PR_NUMBER_AUTO=$(echo "$PR_INFO" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['number']) if d else None" 2>/dev/null || echo '')
    PR_HEAD=$(echo "$PR_INFO" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['headRefOid']) if d else None" 2>/dev/null || echo '')
    PR_URL=$(echo "$PR_INFO" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['url']) if d else None" 2>/dev/null || echo '')
    if [[ -n "$PR_NUMBER_AUTO" ]]; then
      echo ""
      echo "▶ open PR #$PR_NUMBER_AUTO → $PR_URL"
      echo "  PR HEAD: ${PR_HEAD:0:7}"
      if [[ "$PR_HEAD" == "$LOCAL_AFTER" ]]; then
        echo "  ✓ PR 已含本次 commit"
      else
        echo "  ⚠ PR HEAD 不等於最後 commit——等 30 秒讓 GitHub 重整再請使用者 merge"
      fi
    fi
  fi
else
  echo "  ⚠ gh / python3 不可用，SKIP PR 自動偵測"
fi

echo ""
echo "✓ safe-push 完成。可以告訴使用者 merge 了。"
