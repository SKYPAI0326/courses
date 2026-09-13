# #07 Quick Tunnel 回應路由修復｜PLAN

## 目標

讓學員以目前 Lite Pack 與 n8n 介面完成一次可觀察的公開 GET webhook 測試：瀏覽器取得固定 JSON、Telegram 收到通知，兩者都能在 n8n 執行結果中核對。

## 變更

1. Webhook 改用 `responseNode`，避免 Telegram 分支的完成順序影響 HTTP 回應。
2. 將 `Respond: pong` 改為 `Respond to Webhook v1.1`，回傳 Code 產生的 `status`、`message`、`received_at`、`from` 四欄 JSON。
3. 讓頁面程式碼、節點名稱、GET 方法、Publish／production URL、成功訊號與 Blueprint 一致。
4. 在頁面加入從啟動 Tunnel、發布 workflow、呼叫 URL 到收尾關閉的完整測試路徑。
5. 將 Quick Tunnel 的暫時性與停止方式寫清楚，保留 Windows `.bat` 與 macOS `.command` 的共同說明。
6. 更新節點附錄的 type／typeVersion／角色。

## 驗收

- ZIP 可解壓、31 個項目完整，14 個 workflow JSON 均可解析。
- #07 `responseMode=responseNode`，回應節點為 `respondToWebhook` v1.1。
- macOS `setup-wizard.command` 仍為 0755。
- HTML 不再宣稱 GET + POST、`lastNode` 或不存在的回應欄位。
- 透過既有 lint 與頁面索引檢查。
- 人工驗證：啟動 Quick Tunnel、Publish #07、GET `/webhook/external-ping?message=hello`，核對瀏覽器 JSON、Telegram 與節點綠框。
