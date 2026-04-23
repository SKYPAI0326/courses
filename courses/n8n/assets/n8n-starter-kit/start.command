#!/bin/bash
# n8n-starter-kit 一鍵啟動 (macOS)
# 用法：在 Finder 雙擊本檔
# 首次執行若被擋：系統設定 → 隱私權與安全性 → 強制打開

set -e
cd "$(dirname "$0")"

# 確認 docker 指令存在
if ! command -v docker >/dev/null 2>&1; then
  osascript -e 'display dialog "找不到 docker 指令。\n\n請先安裝 Docker Desktop：\nhttps://www.docker.com/products/docker-desktop/" buttons {"知道了"} default button 1 with icon caution'
  exit 1
fi

# 確認 Docker Desktop 已啟動
if ! docker info >/dev/null 2>&1; then
  osascript -e 'display dialog "Docker Desktop 未啟動。\n\n請先打開 Docker Desktop（左上角應看到鯨魚圖示），等待啟動完成後再次執行本檔。" buttons {"知道了"} default button 1 with icon caution'
  exit 1
fi

# 確認 .env 存在；不存在則從範本複製並請使用者編輯
if [ ! -f .env ]; then
  cp .env.example .env
  osascript -e 'display dialog "已從 .env.example 建立 .env 檔。\n\n請修改 POSTGRES_PASSWORD 為強密碼後存檔，然後再次執行 start.command。" buttons {"知道了"} default button 1'
  open -a TextEdit .env
  exit 0
fi

# 確認 shared 資料夾存在（給 Watch Folder 用）
mkdir -p shared

# 啟動 n8n
echo "正在啟動 n8n（首次需下載 image，可能花 1-5 分鐘）..."
docker compose up -d

# 等 n8n 起來
echo "等候 n8n 服務就緒..."
for i in {1..60}; do
  if curl -sf http://localhost:5678/healthz >/dev/null 2>&1; then
    open http://localhost:5678
    osascript -e 'display notification "n8n 已啟動於 http://localhost:5678" with title "n8n Starter Kit"'
    echo ""
    echo "✅ n8n 已啟動：http://localhost:5678"
    echo "   首次開啟會引導你建立 Owner Account"
    exit 0
  fi
  sleep 2
done

osascript -e 'display dialog "n8n 啟動超時（120 秒未回應）。\n\n請開「終端機」進入本資料夾，執行：\n  docker compose logs n8n --tail 50\n查看錯誤；或參考課程 1.1.3 排錯手冊頁。" buttons {"知道了"} default button 1 with icon stop'
exit 1
