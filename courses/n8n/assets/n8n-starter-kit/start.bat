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

REM 確認 n8n-compose.yml 存在（避免在錯目錄雙擊）
if not exist n8n-compose.yml (
  echo.
  echo 找不到 n8n-compose.yml。
  echo 請確認你是在 n8n-starter-kit 資料夾內雙擊 start.bat。
  echo 如果你只看到 start.bat 而沒看到 n8n-compose.yml，
  echo 表示你的 zip 解壓位置不對 - 重新下載 zip 並雙擊解壓。
  echo.
  pause
  exit /b 1
)

REM 確認 .env 存在
if not exist .env (
  if not exist .env.example (
    echo.
    echo 找不到 .env.example，無法建立 .env。
    echo 試跑包不完整，請重新下載 n8n-starter-kit.zip
    echo.
    pause
    exit /b 1
  )
  copy .env.example .env >nul
  echo.
  echo 已從 .env.example 建立 .env 檔。
  echo 即將打開記事本讓你修改 POSTGRES_PASSWORD 為強密碼。
  echo 改完存檔關閉記事本，然後再次雙擊 start.bat 真正啟動 n8n。
  echo.
  notepad .env
  pause
  exit /b 0
)

REM 確認 shared 資料夾存在
if not exist shared mkdir shared

REM 啟動 n8n
echo 正在啟動 n8n（首次需下載 image，可能花 1-5 分鐘）...
docker compose -f n8n-compose.yml up -d
if errorlevel 1 (
  echo.
  echo docker compose 啟動失敗。請截圖上方錯誤訊息給講師看。
  echo 常見原因：postgres 密碼跟 volume 內舊密碼不一致 - 改用：
  echo   docker compose -f n8n-compose.yml down -v
  echo 清 volume 後重雙擊 start.bat
  echo.
  pause
  exit /b 1
)

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
