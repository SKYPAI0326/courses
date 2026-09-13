# Repair Report: n8n AQ authorization key compatibility

## Result
修補已完成，Lite Pack wizard v1.3.3 不再寫死金鑰前綴；`AIza` standard key、`AQ.` authorization key 與後續格式都會先通過非空檢查，再由 Gemini smoke test 判定可用性。

## Evidence
- macOS `setup-wizard.command`: `bash -n` 通過；前綴測試涵蓋 `AQ.`、`AIza` 與拒絕值。
- Lite Pack zip：`unzip -t` 通過，包含 14 個 workflow JSON。
- Windows wizard：已同步修改 PowerShell 的前綴檢查、舊版偵測與秘密掃描；需在 Windows 實機執行 PowerShell 語法與 smoke test。
- macOS／Windows 安裝頁：Gemini key 說明已標示兩種格式，下載連結更新為 v1.3.3。

## Remaining manual gate
使用 AQ. key 實際執行 wizard，確認 Gemini smoke test 回報 `OK`。若 API 回傳 401／429，保留完整錯誤訊息供下一輪診斷；不能只依前綴判定通過。
