# #06 Webhook UI 文案與驗收修正計畫

## Scope

- `n8n/assets/n8n-lite-pack.zip`
- `n8n/lessons/m0-workflow-06-webhook-ai.html`
- `n8n/lessons/m0-install-mac.html`
- `n8n/lessons/m0-install-win.html`
- `n8n/lessons/post-llm-appendix-nodes.html`

## 目標

讓學員按照同一套 C6 流程完成本機 POST 測試，能辨認目前 n8n 的等待狀態，並知道 5 節點主路徑與 3 節點 Web UI 分支的範圍。

## 修正項目

1. 更新 ZIP #06 sticky note：以 `Waiting for you to call the Test URL` 為目前介面判準，保留 `Listening` 作版本差異提示。
2. 更新 #06 網頁講義：標示 `5 POST NODES + 3 UI NODES`，補上 Web UI 分支流程與節點說明，保留主 POST 路徑的五節點拆解。
3. 更新 Mac／Windows C6：四項通過判準統一為 curl 回應、輸出檔、Telegram、Code `aiError`。
4. 更新 ZIP `_change-log.md`，留下此次 UI 與驗收修正紀錄。
5. 修正 #06 回應路由：Webhook 改用 `responseNode`，將原 Set 節點改為 Respond to Webhook，讓 fan-out 同時執行時仍固定回傳 `{"status":"ok",...}`，並同步更新網頁節點說明。
6. 重新封裝 ZIP 時保留 Unix 檔案模式，確保 macOS `setup-wizard.command` 為 `0755` 可執行。

## 驗證

- ZIP 內 14 個 workflow JSON 可解析，#06 節點數與 sticky note 文字符合修正。
- HTML targeted lint 與全站 lint 通過。
- `git diff --check` 通過。
- 備份可由 `n8n/_backup/2026-09-13-pre-webhook-ui-copy-repair/` 回復。
