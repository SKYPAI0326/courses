@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0apply-fix.ps1"
if errorlevel 1 (
  echo.
  echo 修補未完成。請保留此視窗訊息與 shared 中的備份資料夾，聯絡課程支援。
  pause
  exit /b 1
)
exit /b 0
