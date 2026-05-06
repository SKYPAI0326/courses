@echo off
REM n8n-starter-kit 一鍵啟動 (Windows)
REM 用法：在檔案總管雙擊本檔
chcp 65001 >nul
setlocal

cd /d "%~dp0"

REM 確認 docker 指令存在
where docker >nul 2>&1
if errorlevel 1 (
  echo.
  echo 找不到 docker 指令。
  echo 請先安裝 Docker Desktop：
  echo   https://www.docker.com/products/docker-desktop/
  echo.
  pause
  exit /b 1
)

REM 確認 Docker Desktop 已啟動
docker info >nul 2>&1
if errorlevel 1 (
  echo.
  echo Docker Desktop 未啟動。
  echo 請先打開 Docker Desktop（工具列應看到鯨魚圖示），等待啟動完成後再次執行本檔。
  echo.
  pause
  exit /b 1
)

REM 確認 .env 存在
if not exist .env (
  copy .env.example .env >nul
  echo.
  echo 已從 .env.example 建立 .env 檔。
  echo 請修改 POSTGRES_PASSWORD 為強密碼後存檔，然後再次執行 start.bat。
  echo.
  notepad .env
  exit /b 0
)

REM 確認 shared 資料夾存在
if not exist shared mkdir shared

REM 啟動 n8n
echo 正在啟動 n8n（首次需下載 image，可能花 1-5 分鐘）...
docker compose -f n8n-compose.yml up -d

REM 等 n8n 起來（最多 120 秒）
echo 等候 n8n 服務就緒...
for /l %%i in (1,1,60) do (
  curl -sf http://localhost:5678/healthz >nul 2>&1
  if not errorlevel 1 (
    start "" http://localhost:5678
    echo.
    echo n8n 已啟動：http://localhost:5678
    echo 首次開啟會引導你建立 Owner Account
    echo.
    timeout /t 3 /nobreak >nul
    exit /b 0
  )
  timeout /t 2 /nobreak >nul
)

echo.
echo n8n 啟動超時（120 秒未回應）。
echo 請開 PowerShell 進入本資料夾，執行：
echo   docker compose -f n8n-compose.yml logs n8n --tail 50
echo 查看錯誤；或參考課程 1.1.3 排錯手冊頁。
echo.
pause
exit /b 1
