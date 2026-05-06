@echo off
REM Cloudflare Quick Tunnel — 不需自有網域、不需綁卡的公開 URL
REM 用法：雙擊本檔；命令提示字元會顯示一個 https://xxxx.trycloudflare.com 公開網址
REM 結束：按 Ctrl+C，URL 即失效

cd /d "%~dp0"

where cloudflared >nul 2>nul
if errorlevel 1 (
  echo 找不到 cloudflared 指令。
  echo 請先依課程 1.2 步驟 3 從 Cloudflare 下載並安裝 cloudflared.exe，並把它放入 PATH。
  pause
  exit /b 1
)

curl -sf http://localhost:5678/healthz >nul 2>nul
if errorlevel 1 (
  echo n8n 似乎沒有跑在 localhost:5678。
  echo 請先雙擊 start.bat 啟動 n8n，等啟動完成後再雙擊本檔。
  pause
  exit /b 1
)

echo =============================================================
echo   Cloudflare Quick Tunnel 啟動中...
echo   下方會顯示一個 https://xxxx.trycloudflare.com 公開網址
echo   把它貼到 Make HTTP 模組 / 瀏覽器測試即可
echo.
echo   * 關閉本視窗或按 Ctrl+C → URL 立即失效
echo   * 每次重新啟動 URL 都會變
echo   * 不需要 Cloudflare 帳號、不需要綁卡、不需要自有網域
echo =============================================================
echo.

REM 預設用 http2 protocol — quic 在很多家用 ISP / 公司網路被擋
REM 若連續失敗請依講義 1.2 最下方「備用方案 · NGROK FALLBACK」改用 ngrok
cloudflared tunnel --url http://localhost:5678 --protocol http2
