#!/usr/bin/env bash
# safe-push.sh —— push 後驗證 origin 收到、檢查 PR race 風險
#
# 用法（從 repo 根目錄執行）：
#   bash docs/safe-push.sh             # 推當前 branch 並驗證
#   bash docs/safe-push.sh --no-push   # 只驗證，不推
#
# 解決問題：使用者按 merge 比 Claude push 快 4 分鐘，導致最後 commit 漏進 PR。
#
# 動作：
#   1. 記下本地 HEAD hash
#   2. git push（除非 --no-push）
#   3. git fetch + 比對 remote HEAD
#   4. hash 不一致時警告
#   5. 若 branch 有 open PR，列出 PR HEAD + 提醒最後 commit 是否包含
#
# Exit codes：
#   0 = 同步成功（local == remote）
#   1 = git 操作失敗
#   2 = race 偵測（local != remote）

set -u

NO_PUSH=0
[[ "${1:-}" == "--no-push" ]] && NO_PUSH=1

BRANCH=$(git branch --show-current)
[[ -z "$BRANCH" ]] && { echo "✗ 不在 branch 上（detached HEAD?）"; exit 1; }

LOCAL_BEFORE=$(git rev-parse HEAD)
echo "▶ branch: $BRANCH"
echo "▶ local HEAD before push: ${LOCAL_BEFORE:0:7}"

if [[ $NO_PUSH -eq 0 ]]; then
  echo "▶ 執行 git push..."
  git push 2>&1 | sed 's/^/  /'
  PUSH_RC=${PIPESTATUS[0]}
  [[ $PUSH_RC -ne 0 ]] && { echo "✗ push 失敗 (exit $PUSH_RC)"; exit 1; }
fi

echo "▶ fetch origin/$BRANCH..."
git fetch origin "$BRANCH" --quiet 2>/dev/null || echo "  (fetch 警告，繼續)"

# 確認 upstream 存在
if ! git rev-parse "@{u}" >/dev/null 2>&1; then
  echo "✗ 沒有 upstream tracking branch（首次 push 用 git push -u）"
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
  echo "  可能原因：他人也 push 了 / push 失敗 / push 還在進行中"
  exit 2
fi

# 檢查 open PR（需 gh CLI）
if command -v gh >/dev/null 2>&1; then
  PR_INFO=$(gh pr list --head "$BRANCH" --state open --json number,headRefOid,url 2>/dev/null)
  if [[ -n "$PR_INFO" && "$PR_INFO" != "[]" ]]; then
    PR_NUMBER=$(echo "$PR_INFO" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['number']) if d else None" 2>/dev/null)
    PR_HEAD=$(echo "$PR_INFO" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['headRefOid']) if d else None" 2>/dev/null)
    PR_URL=$(echo "$PR_INFO" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['url']) if d else None" 2>/dev/null)
    echo ""
    echo "▶ open PR #$PR_NUMBER → $PR_URL"
    echo "  PR HEAD: ${PR_HEAD:0:7}"
    if [[ "$PR_HEAD" == "$LOCAL_AFTER" ]]; then
      echo "  ✓ PR 已含本次 commit"
    else
      echo "  ⚠ PR HEAD 不等於最後 commit——使用者按 merge 前需 GitHub 自動同步"
      echo "    建議等 30 秒讓 GitHub 重整 PR HEAD 再請使用者 merge"
    fi
  fi
fi

echo ""
echo "✓ safe-push 完成。可以告訴使用者 merge 了。"
