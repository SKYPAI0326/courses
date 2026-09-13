# Repair Report: n8n Workflow 01 interface alignment

## Changed

- `n8n/lessons/m0-workflow-01-webhook.html`
  - 以 Lite Pack #01 實際 Blueprint 對齊 GET、`lite-hello`、Test／Production URL 與三個 Set 輸出欄位。
  - 新增目前 n8n 介面的測試順序，明確區分右上角 `Publish` 與畫布下方橘色 `Execute workflow`。
  - 更新平台版本頁尾與 Windows 待驗證狀態。
- `n8n/assets/n8n-lite-pack.zip`
  - 更新 #01 sticky note 的按鈕顏色、Publish 提醒、測試期限與預期輸出。
  - workflow 邏輯與匯入結構維持不變；14 個 JSON 仍可解析。
- `m1-1-launch.html`
  - 標示 `hello` 是空白練習，與 Lite Pack #01 的 `lite-hello` 分開。
- `m0-install-mac.html`、`m0-install-win.html`、`m0-workflow-02-pdf-rename.html`、`m1-2-tunnel.html`、`post-llm-3-steps-decompose.html`、`post-llm-6-walkthrough.html`
  - 將過時的「紫色 Execute workflow」改為目前畫面可辨識的「畫布下方橘色 Execute workflow」。

## Verification

- Lite Pack ZIP：`unzip -t` 通過；14 個 JSON parse OK。
- #01 Blueprint：`GET`、Path `lite-hello`、Set assignments `message/timestamp/received_method` 通過比對。
- stale UI 掃描：目前課程頁與資產沒有殘留「紫色 Execute」說法。
- 還原腳本：`bash -n` 通過。
- HTML lint：本次 8 個頁面均 `BLOCKER 0 / ERROR 0`。
- n8n 全站 lint：`81 頁，BLOCKER 0 / ERROR 0 / WARN 165`。
- 搜尋索引：已重建，寫入 660 筆。
- Windows：僅完成文字與共用 ZIP 同步；仍待 Windows 實機驗證。

## Remaining

- 尚未在目前 n8n 實例實際按下 #01 的 `Execute workflow` 並送出 Test URL；下一步由人工驗證完成。
- `received_method` 是既有 Blueprint 欄位名稱，實際值取 `x-real-ip` 或 `host`；文件已明示，後續若要改善命名需另開行為變更修復。

## Restore

- Backup：`n8n/_backup/2026-09-13-pre-workflow-01-interface/`
- Restore script：`n8n/_tools/restore-2026-09-13-pre-workflow-01-interface.sh`

