#!/bin/bash
# n8n-starter-kit 一鍵啟動 (macOS)
# 用法：在 Finder 雙擊本檔
# 首次執行若被擋：系統設定 → 隱私權與安全性 → 強制打開

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

# 啟動前先偵測 port 5678 是否已被其他 container 佔用
EXISTING_5678=$(docker ps --filter publish=5678 --format '{{.Names}}' 2>/dev/null)
if [ -n "$EXISTING_5678" ]; then
  CONFLICT_LIST=$(echo "$EXISTING_5678" | head -5 | sed 's/^/  • /')
  REPLY=$(osascript <<EOF 2>/dev/null
display dialog "偵測到 port 5678 已被舊的 n8n container 佔用：

$CONFLICT_LIST

常見原因：你之前已啟動過 n8n（或解壓到不同資料夾啟了多次），舊 container 還在跑。

要停掉這些舊 container 並重啟嗎？" buttons {"取消", "停掉並重啟"} default button "停掉並重啟" with icon caution
EOF
)
  if [[ "$REPLY" == *"停掉並重啟"* ]]; then
    echo "停掉舊 container..."
    docker ps --filter publish=5678 -q | xargs -r docker stop
    docker ps -a --filter publish=5678 -q | xargs -r docker rm
    echo "舊 container 已清理。"
  else
    exit 1
  fi
fi

# 啟動 n8n
echo "正在啟動 n8n（首次需下載 image，可能花 1-5 分鐘）..."
COMPOSE_OUTPUT=$(docker compose -f n8n-compose.yml up -d 2>&1)
COMPOSE_EXIT=$?

if [ $COMPOSE_EXIT -ne 0 ]; then
  # 二次防線：up 仍失敗 → 解析錯誤類型
  if echo "$COMPOSE_OUTPUT" | grep -q "port is already allocated"; then
    osascript -e 'display dialog "Port 5678 仍被佔用，自動清理失敗。\n\n請打開 Docker Desktop → Containers，手動停掉所有跑著的 n8n container 後再雙擊 start.command。" buttons {"知道了"} default button 1 with icon stop'
  else
    osascript -e "display dialog \"啟動失敗：\n\n$(echo "$COMPOSE_OUTPUT" | tail -10)\n\n請參考課程 1.1.3 排錯手冊頁。\" buttons {\"知道了\"} default button 1 with icon stop"
  fi
  exit 1
fi
echo "$COMPOSE_OUTPUT"

# 等 n8n 起來
echo "等候 n8n 服務就緒（首次需建資料表，約 15-60 秒）..."
for i in {1..60}; do
  if curl -sf http://localhost:5678/healthz >/dev/null 2>&1; then
    open http://localhost:5678
    osascript -e 'display notification "n8n 已啟動於 http://localhost:5678" with title "n8n Starter Kit"'
    echo ""
    echo "✅ n8n 已啟動：http://localhost:5678"
    echo "   首次開啟會引導你建立 Owner Account"
    echo "   建議用 Chrome / Firefox / Edge（避開 Safari）"
    exit 0
  fi
  if (( i % 5 == 0 )); then
    echo "⏳ 已等候 $((i * 2)) 秒，n8n 還在初始化中（請耐心等候，不要關掉視窗）..."
  fi
  sleep 2
done

# 啟動超時 — 主動偵測 postgres 密碼認證失敗這個常見坑
if docker compose -f n8n-compose.yml logs n8n --tail 30 2>/dev/null | grep -q "password authentication failed"; then
  RESET_REPLY=$(osascript -e 'display dialog "偵測到 postgres 密碼認證失敗。\n\n常見原因：你之前啟動過 n8n，postgres 已用舊密碼建立了資料庫；後來改了 .env 密碼，新密碼對不上舊資料庫。\n\n如果你還沒建 Owner Account（沒有資料要保留），可以重置資料庫。\n\n要重置嗎？" buttons {"取消", "重置並重啟"} default button "重置並重啟" with icon caution' 2>/dev/null)
  if [[ "$RESET_REPLY" == *"重置並重啟"* ]]; then
    echo "重置 volumes..."
    docker compose -f n8n-compose.yml down -v
    docker compose -f n8n-compose.yml up -d
    echo "重啟完成，請等 30 秒後手動開瀏覽器 http://localhost:5678"
    exit 0
  fi
fi

osascript -e 'display dialog "n8n 啟動超時（120 秒未回應）。\n\n請開「終端機」進入本資料夾，執行：\n  docker compose -f n8n-compose.yml logs n8n --tail 50\n查看錯誤；或參考課程 1.1.3 排錯手冊頁。" buttons {"知道了"} default button 1 with icon stop'
exit 1
