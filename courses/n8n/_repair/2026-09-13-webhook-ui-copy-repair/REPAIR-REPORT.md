# Repair Report: n8n #06 Webhook UI 文案與驗收

## Changed

- `n8n/assets/n8n-lite-pack.zip`
  - 更新 #06 sticky note，改用目前 n8n 介面的 `Waiting for you to call the Test URL`。
  - 保留 `Listening` 作為舊版介面提示。
  - 明確區分 5 個 POST 主路徑節點與 3 個 GET Web UI 節點。
  - 統一本機測試的回應、輸出檔、Telegram、`aiError` 四項驗收條件。
  - 修正 fan-out 回應路由：Webhook 改用 `responseNode`，由 Respond to Webhook 固定回傳 `status/question/answer`。
  - 恢復 `setup-wizard.command` 的 Unix `0755` 執行權限，修正 macOS Finder 顯示無法執行的問題。
- `n8n/lessons/m0-workflow-06-webhook-ai.html`
  - 標示 5 POST NODES + 3 UI NODES。
  - 補上 Web UI 分支的入口、方法與驗收邊界。
  - 補上目前介面的等待提示與 POST 測試入口。
  - 將回應節點說明改為 Respond to Webhook，移除 `lastNode` 在多分支情境下可能回傳錯誤節點結果的描述。
- `n8n/lessons/m0-install-mac.html`、`m0-install-win.html`
  - C6 首步改為目前 n8n 介面的等待提示，兩平台驗收條件一致。
- `n8n/lessons/post-llm-appendix-nodes.html`
  - 同步 #06 回應節點的類型與版本，避免附錄仍顯示舊 Set 節點。
- `n8n/_tools/restore-2026-09-13-pre-webhook-ui-copy-repair.sh`
  - 新增本次範圍的可回復腳本。

## Verification

- targeted content assertions：通過；#06 頁、Mac、Windows 與 sticky note 文字一致，已移除舊的「變藍色」描述。
- ZIP integrity：通過；`unzip -t` 無錯誤。
- workflow JSON：通過；14 個 workflow JSON 可解析，#06 有 8 個可執行節點（另含 1 個 sticky note）。
- response routing：通過靜態檢查；#06 Webhook 為 `responseNode`，Respond 節點為 `respondToWebhook` v1.1，回應內容含 `status/question/answer`。
- package permissions：通過；`setup-wizard.command` 為 `0755`，`.bat`／`.ps1` 保持 Windows 腳本格式。
- restore script：通過；`bash -n`。
- `git diff --check`：通過。
- targeted lint：通過；3 頁 BLOCKER 0、ERROR 0。
- full lint：通過；1330 頁 BLOCKER 0、ERROR 0。
- search-index：已重建，660 筆。
- manual evidence：本次人工測試已確認 #06 產生 `shared/ai-output/` Markdown 檔、收到 Telegram 通知，且 Code Output 的 `aiError` 為 `null`。原始 curl 曾回傳 Telegram API JSON，已定位為 `lastNode` fan-out 路由問題並完成修正；修正版仍需重新匯入 #06 後再確認 curl 回傳 `{"status":"ok",...}`。

## Remaining

- 學員下次匯入或重新下載 Lite Pack 後，需再次確認 #06 sticky note 顯示新版等待文案。
- 重新匯入修正版 #06 後，需再次執行 curl，確認回應由 Telegram API JSON 改為 `{"status":"ok",...}`。
- 重新下載 ZIP 後，macOS 需確認 Finder 可直接開啟 `setup-wizard.command`；若系統仍攔截，依安裝頁的 Gatekeeper 步驟處理。
- 既有 n8n 工作區已匯入的 workflow 不需重裝；若要更新 sticky note，重新匯入修正版 #06 即可。

## Restore

- backup: `n8n/_backup/2026-09-13-pre-webhook-ui-copy-repair/`
- restore script: `n8n/_tools/restore-2026-09-13-pre-webhook-ui-copy-repair.sh`
