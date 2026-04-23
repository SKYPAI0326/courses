@echo off
REM n8n-starter-kit 停止服務 (Windows)
REM 用法：在檔案總管雙擊本檔
REM 注意：只停容器，資料 (workflows / credentials) 保留在 Docker volume，下次 start 自動恢復
REM       要連資料一起刪請手動執行 docker compose down -v
chcp 65001 >nul

cd /d "%~dp0"
docker compose down

echo.
echo n8n 已停止。資料保留於 Docker volumes 中。
echo.
timeout /t 3 /nobreak >nul
