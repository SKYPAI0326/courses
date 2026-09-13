# Repair Plan: n8n Workflow 01 interface alignment

## Scope

- `m0-workflow-01-webhook.html`：以 Lite Pack #01 的可匯入 Blueprint 為教材基準。
- Lite Pack ZIP 內 `workflows/01-webhook-hello-world.json`：修正便箋的目前介面提示與預期輸出說明。
- 共用介面文字：Mac／Windows 安裝頁、Tunnel 頁、#02 與課後 walkthrough 的 Execute workflow 顏色說法。
- `m1-1-launch.html`：標明空白工作流練習與 Lite Pack #01 的差異，避免 `hello` 與 `lite-hello` 混用。

## BLOCKER

### [對齊] `m0-workflow-01-webhook.html`

- 問題：頁面寫 POST、`hello`、`status/received_at/echo`；可匯入 Blueprint 實際為 GET、`lite-hello`、`message/timestamp/received_method`。
- 修法：改用 ZIP 內實際設定，補上可跟做的測試步驟、Test／Production URL 與完整預期回應。
- 驗證：逐項比對 JSON；頁面測試網址與輸出欄位完全一致。

### [對齊] Lite Pack #01 便箋

- 問題：便箋寫「紫色」且只列一個輸出欄位。
- 修法：改為「畫布下方橘色 Execute workflow」，提醒右上角 Publish 不用按，並列出三個回應欄位。
- 驗證：重新打包後解壓，檢查 JSON 可解析且便箋文字一致。

## MAJOR

### [STALE_UI] 共用 Execute workflow 文字

- 問題：多頁仍寫「紫色」；目前 n8n 畫面為底部橘色按鈕。
- 修法：統一為「畫布下方橘色 Execute workflow」；保留按鈕英文名稱，降低主題色變動造成的誤解。

### [連貫] `m1-1-launch.html`

- 問題：空白練習使用 `hello`，但學員可能從 Lite Pack #01 進入而看到 `lite-hello`。
- 修法：在該步驟明示這是獨立的空白練習，兩個 Path 不可混用。

## Activity Identity Audit

| page | section | role | material | artifact | path | learner decision | overlap verdict |
|---|---|---|---|---|---|---|---|
| m0-workflow-01-webhook | 實際驗證 | Demo／跟做基線 | Lite Pack #01 Blueprint | GET webhook 的 JSON 回應 | Execute → Test URL → Output | 判斷 Listening、網址與三欄位輸出 | 與 m1-1 空白練習分開 |
| m1-1-launch | 步驟 6 | Together | 空白 workflow | 學員自行建立的 `hello` webhook | Create Workflow → Webhook | 判斷節點綠燈與請求資料 | 不重跑 Lite Pack #01 |

## Execution Order

1. 建立備份與還原腳本。
2. 修正 #01 HTML 與 Lite Pack 便箋。
3. 修正共用 UI 顏色提示與跨頁辨識文字。
4. 重新打包 Lite Pack，驗證 14 個 JSON 可解析。
5. 執行 lint、連結與內容對齊檢查。

