#!/bin/bash
# Cloudflare Quick Tunnel — 不需自有網域、不需綁卡的公開 URL
# 用法：在 Finder 雙擊本檔；終端機會顯示一個 https://xxxx.trycloudflare.com 公開網址
# 結束：在終端機按 Ctrl+C，URL 即失效

cd "$(dirname "$0")"

# 確認 cloudflared 已安裝
if ! command -v cloudflared >/dev/null 2>&1; then
  osascript -e 'display dialog "找不到 cloudflared 指令。\n\n請先依課程 1.2 步驟 3 安裝 cloudflared：\n  brew install cloudflared（Mac）\n或從 Cloudflare 下載 .pkg 安裝檔。\n\n安裝完後再雙擊本檔。" buttons {"知道了"} default button 1 with icon caution'
  exit 1
fi

# 確認 n8n 在跑（quick tunnel 沒意義如果 n8n 沒跑）
if ! curl -sf http://localhost:5678/healthz >/dev/null 2>&1; then
  osascript -e 'display dialog "n8n 似乎沒有跑在 localhost:5678。\n\n請先雙擊 start.command 啟動 n8n，等看到「✅ n8n 已啟動」訊息後再雙擊本檔。" buttons {"知道了"} default button 1 with icon caution'
  exit 1
fi

echo "═════════════════════════════════════════════════════════════"
echo "  Cloudflare Quick Tunnel 啟動中..."
echo "  下方會顯示一個 https://xxxx.trycloudflare.com 公開網址"
echo "  把它貼到 Make HTTP 模組 / 瀏覽器測試即可"
echo ""
echo "  ⚠️  關閉本視窗或按 Ctrl+C → URL 立即失效"
echo "  ⚠️  每次重新啟動 URL 都會變"
echo "  ⚠️  不需要 Cloudflare 帳號、不需要綁卡、不需要自有網域"
echo ""
echo "  使用 --protocol http2（避開 ISP / 防火牆常擋的 QUIC/UDP 7844）"
echo "═════════════════════════════════════════════════════════════"
echo ""

# 預設用 http2 protocol — quic 在很多家用 ISP / 公司網路被擋
# 若 30 秒內未取得 trycloudflare.com URL，跳對話框建議改 ngrok
TUNNEL_LOG="/tmp/cf-tunnel-$$.log"
cloudflared tunnel --url http://localhost:5678 --protocol http2 2>&1 | tee "$TUNNEL_LOG" &
CF_PID=$!

# 30 秒內偵測是否取得 URL（精確 pattern：必須是 https://xxxx.trycloudflare.com 才算）
for i in {1..30}; do
  TUNNEL_URL=$(grep -oE "https://[a-z0-9-]+\.trycloudflare\.com" "$TUNNEL_LOG" 2>/dev/null | head -1)
  if [ -n "$TUNNEL_URL" ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "  ✅ Tunnel 連線成功！你的公開 URL："
    echo ""
    echo "    $TUNNEL_URL"
    echo ""
    echo "  把它複製貼到瀏覽器或 Make HTTP 模組即可使用。"
    echo "════════════════════════════════════════════════════════════"
    wait $CF_PID
    rm -f "$TUNNEL_LOG"
    exit 0
  fi
  if grep -qE "(failed to serve tunnel|context canceled|Retrying connection in)" "$TUNNEL_LOG" 2>/dev/null; then
    if [ $i -gt 15 ]; then
      # 連續失敗超過 15 秒 → 推測網路擋
      kill $CF_PID 2>/dev/null
      wait $CF_PID 2>/dev/null
      osascript -e 'display dialog "Cloudflared 連到 Cloudflare 邊緣節點失敗（可能 ISP / 防火牆 / VPN 擋）。\n\n建議改用 ngrok 替代（架構不同，通常能繞開 ISP 限制）：\n\n1. 前往 ngrok.com 註冊免費帳號\n2. 下載 ngrok 並解壓\n3. 終端機跑：./ngrok http 5678\n\n詳見講義 1.2 最下方「備用方案 · NGROK FALLBACK」段落。" buttons {"知道了"} default button 1 with icon caution' 2>/dev/null
      rm -f "$TUNNEL_LOG"
      exit 1
    fi
  fi
  sleep 1
done

# 30 秒內仍未取得 URL — 讓 cloudflared 繼續跑（可能慢，但別自動 kill）
wait $CF_PID
rm -f "$TUNNEL_LOG"
