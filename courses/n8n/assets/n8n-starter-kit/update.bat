@echo off
REM n8n-starter-kit 升級 n8n image (Windows)
REM 用法：在檔案總管雙擊本檔
REM 升級流程：拉最新 image → 重啟容器；資料自動延續（在 Docker volume）
chcp 65001 >nul

cd /d "%~dp0"

echo 正在拉取最新 n8n image...
docker compose -f n8n-compose.yml pull

echo 重啟服務...
docker compose -f n8n-compose.yml up -d

echo.
echo 升級完成。資料已自動延續。
echo.
timeout /t 3 /nobreak >nul
