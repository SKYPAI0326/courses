# #06 Webhook UI 文案與驗收掃描

日期：2026-09-13

## 範圍

- `n8n/assets/n8n-lite-pack.zip` 內 #06 sticky note
- `n8n/lessons/m0-workflow-06-webhook-ai.html`
- `n8n/lessons/m0-install-mac.html`、`m0-install-win.html` 的 C6 驗收
- `n8n/lessons/post-llm-appendix-nodes.html` 的 #06 節點對照表

## 發現

1. #06 sticky note 仍寫「Webhook 變藍色」，目前 n8n 2.37.7 介面顯示 `Waiting for you to call the Test URL`。
2. #06 workflow 實際有 5 個主要 POST 節點，另有 3 個 Web UI 節點；講義只標示 5 節點，未清楚說明這是主要 POST 路徑。
3. C6 Mac／Windows 驗收文字未完全對齊：Mac 缺少 curl 回應判準，Windows 缺少 `aiError` 與回應內容判準。
4. 上次人工驗證已確認檔案與 Telegram；仍需依 C6 原定判準補看 curl 回應與 Code `aiError`。
5. 本次人工 curl 回應實際為 Telegram API 的 `{"ok":true,"result":...}`，未回傳講義預期的 `{"status":"ok",...}`；原因是 Webhook 使用 `lastNode`，fan-out 後的最後完成節點可能是 Telegram，Set 節點無法保證成為 response。
6. 附錄仍將 #06 回應節點標為 `set v3.4`，與修正後應使用的 Respond to Webhook 不一致。
7. 重新打包後 ZIP 的 `setup-wizard.command` 權限為 `0600`，macOS Finder 因此無法執行；原始備份為 `0755`。

## 風險分級

| 類別 | 風險 | 等級 |
|---|---|---|
| UI_COPY | 舊版顏色描述會讓初學者等待不存在的狀態 | MAJOR |
| SCOPE | 主要 POST 與 Web UI 分支的節點數範圍不明 | MAJOR |
| ACCEPTANCE | 雙平台 C6 驗收條件不一致 | MAJOR |
| RESPONSE_ROUTING | fan-out 使用 `lastNode`，curl 可能收到 Telegram API 回應 | MAJOR |
| PACKAGE_PERMISSION | macOS 啟動腳本失去 executable bit | BLOCKER |
