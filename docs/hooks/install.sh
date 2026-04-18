#!/usr/bin/env bash
# 一鍵安裝 pre-commit + pre-push hook
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"

cp "$REPO_ROOT/docs/hooks/pre-commit" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"
echo "✅ pre-commit hook 已安裝"
echo "   每次 git commit 前會自動跑 lint-page.py --changed --baseline"

cp "$REPO_ROOT/docs/hooks/pre-push" "$REPO_ROOT/.git/hooks/pre-push"
chmod +x "$REPO_ROOT/.git/hooks/pre-push"
echo "✅ pre-push hook 已安裝"
echo "   每次 git push 前會自動跑 build-all.py（lint + search-index + sitemap）"

echo ""
echo "   緊急略過：git commit --no-verify / git push --no-verify"
