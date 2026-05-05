#!/bin/bash
# n8n-starter-kit 停止服務 (macOS)
# 用法：在 Finder 雙擊本檔
# 注意：只停容器，資料 (workflows / credentials) 保留在 Docker volume，下次 start 自動恢復
#       要連資料一起刪請手動執行 docker compose -f n8n-compose.yml down -v

cd "$(dirname "$0")"
docker compose -f n8n-compose.yml down

osascript -e 'display notification "n8n 已停止。資料保留，下次 start 自動恢復。" with title "n8n Starter Kit"'
echo "✅ n8n 已停止。資料保留於 Docker volumes 中。"
