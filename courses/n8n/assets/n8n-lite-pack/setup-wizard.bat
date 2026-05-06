@echo off
REM n8n Lite Pack · setup-wizard wrapper (Windows)
REM 實際邏輯在 setup-wizard.ps1，這個 .bat 只是雙擊入口
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo.
echo ==============================================================
echo   n8n Lite Pack . setup-wizard for Windows
echo ==============================================================
echo.
echo 即將以 PowerShell 執行安裝腳本...
echo.

REM 檢查 PowerShell 7+ 或 Windows PowerShell 5.1
where pwsh >nul 2>&1
if not errorlevel 1 (
  pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-wizard.ps1"
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-wizard.ps1"
)

if errorlevel 1 (
  echo.
  echo setup-wizard 失敗，請看上面錯誤訊息。
  echo 常見原因：
  echo   1. Docker Desktop 沒啟動 - 先打開 Docker Desktop
  echo   2. n8n 沒在跑 - 到 starter-kit 雙擊 start.bat
  echo   3. 沒裝 Python 3 - 到 Microsoft Store 搜尋 Python 安裝
  echo.
  pause
  exit /b 1
)

echo.
echo ==============================================================
echo   setup-wizard 執行完畢，按任意鍵關閉視窗
echo ==============================================================
pause >nul
exit /b 0
