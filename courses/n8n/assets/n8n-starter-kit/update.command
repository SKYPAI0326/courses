#!/bin/bash
# n8n-starter-kit 升級 n8n image (macOS)
# 用法：在 Finder 雙擊本檔
# 升級流程：拉最新 image → 重啟容器；資料自動延續（在 Docker volume）

set -e
cd "$(dirname "$0")"

echo "正在拉取最新 n8n image..."
docker compose -f n8n-compose.yml pull

echo "重啟服務..."
docker compose -f n8n-compose.yml up -d

echo ""
echo "✅ 升級完成。資料已自動延續。"
osascript -e 'display notification "n8n 升級完成" with title "n8n Starter Kit"'
