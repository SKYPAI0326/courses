# Scan: webhook Listening UI wording

日期：2026-09-13

## Scope

本次只處理 n8n 課程中與 Webhook 測試等待狀態相關的介面文字，以及 Lite Pack #01 便箋。Mac 人工驗證已確認目前介面可直接看到橘色 `Execute workflow`、成功通知、節點綠框、連線 `1 item` 與 Output；藍色 `Listening for test event` 未在本次成功畫面出現。

## Findings

| 類別 | 檔案 | 問題 | 嚴重度 |
|---|---|---|---|
| STALE_UI / LEARNER_PATH | `n8n/lessons/m0-workflow-01-webhook.html` | 將藍色 Listening 寫成按 Execute 後應出現，404 修復也要求回到 Listening。 | MAJOR |
| STALE_UI / LEARNER_PATH | `n8n/assets/n8n-lite-pack.zip`（workflow #01 便箋） | 將藍色 Listening 寫成固定測試步驟。 | MAJOR |
| STALE_UI | `n8n/lessons/m0-install-mac.html` | #06 驗證步驟將藍色 Listening 寫成必要狀態。 | MINOR |
| STALE_UI | `n8n/lessons/m0-install-win.html` | #06 驗證步驟將藍色 Listening 寫成必要狀態。 | MINOR |
| STALE_UI / LEARNER_PATH | `n8n/lessons/m1-1-launch.html` | 空白 Webhook 練習要求使用目前介面未必出現的 `Listen for test event` 按鈕與藍色狀態。 | MAJOR |
| STALE_UI / LEARNER_PATH | `n8n/lessons/m1-2-tunnel.html` | Tunnel 測試將藍色 Listening 寫成必要驗收條件，404 修復依賴該文字。 | MAJOR |

## Current evidence

- `01 · Webhook hello-world` 實測結果：Webhook 與 Set 節點綠框、勾號、連線 `1 item`，Output 三欄位正確。
- 右上角 `Publish` 未參與本次測試；底部橘色 `Execute workflow` 為手動測試入口。
- Test URL `/webhook-test/lite-hello` 回傳 `message`、`timestamp`、`received_method`。

## Proposed acceptance wording

將「藍色 Listening」降為版本差異提示。每一個 Webhook 測試都以四個可觀察證據引導學員：

1. 按底部橘色 `Execute workflow`，畫面進入執行／等待狀態。
2. 在等待期間送出 Test URL。
3. 瀏覽器收到預期回應，且沒有 404。
4. 回到 n8n 確認節點綠框、連線 item 數與 Output 欄位。

## Asset Discoverability

Lite Pack #01 檔案存在於課程下載包內，URL 與欄位均已在講義列出；本次只修正便箋的驗收語句，不改 workflow JSON 邏輯。
