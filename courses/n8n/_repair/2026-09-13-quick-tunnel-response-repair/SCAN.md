# #07 Quick Tunnel 回應路由修復｜SCAN

日期：2026-09-13
範圍：`m0-workflow-07-tunnel.html`、Lite Pack `07-quick-tunnel-receiver.json`、節點附錄

## 發現

1. Webhook 使用 `responseMode: lastNode`，Code 後同時分流到 Telegram 與回應節點；完成順序不固定，呼叫端可能收到 Telegram API 的內容。
2. Blueprint 的回應節點實際是 `set v3.4`，講義卻把它描述成可控的 webhook 回應；回應欄位也與 Code 產出的 `response` 物件不一致。
3. Blueprint 的 Webhook 實際只接受 `GET`，頁面卻寫成 GET + POST，後面的 Make／表單範例也使用 POST，學員照做會得到方法不符。
4. 頁面程式碼範例與 Blueprint 程式碼不同，學員無法用講義逐行比對。
5. 頁面使用 `Active`、固定「3 秒開通」與「預設 24 小時斷線」等描述，與目前 n8n 介面及腳本可觀察行為不完全相符。
6. 本次修復前已備份至 `_backup/2026-09-13-pre-quick-tunnel-repair/`。

## 風險分級

| 類別 | 風險 | 等級 |
| --- | --- | --- |
| RESPONSE_ROUTING | fan-out + `lastNode` 可能回傳錯誤節點內容 | BLOCKER |
| CONTRACT | GET／POST、回應欄位與實際 Blueprint 不一致 | MAJOR |
| TEACHING_PATH | 測試入口與目前 Publish 介面不一致 | MAJOR |
| RECOVERY | 變更前已有 HTML、ZIP 與附錄備份 | PASS |
