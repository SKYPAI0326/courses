# Repair Plan: n8n webhook Listening UI wording

## Scope

- slug: `n8n`
- pages: `m0-workflow-01-webhook.html`, `m0-install-mac.html`, `m0-install-win.html`, `m1-1-launch.html`, `m1-2-tunnel.html`
- asset: `assets/n8n-lite-pack.zip`（僅 workflow #01 sticky note）
- platform coverage: macOS + Windows；Windows 維持「待實機驗證」標記

## Risk

- 近期待課：unknown
- backup required: yes
- learner risk: 學員可能等待不存在的藍色狀態，錯過可驗收的綠框與 Output 證據

## MAJOR

### [STALE_UI / LEARNER_PATH] Webhook 測試頁與空白練習

- 問題：把 `Listening for test event` 或 `Listen for test event` 當作固定按鈕／必要驗收條件。
- 修法：以畫布底部橘色 `Execute workflow`、Test URL 回應、綠框與 Output 作主路徑；保留 Listening 僅作「部分版本可能顯示」提示。
- 驗證：搜尋所有目標檔案，確認沒有把藍色 Listening 寫成必須看到；用課程驗收關鍵字檢查四項證據。

### [STALE_UI / LEARNER_PATH] Tunnel 404 修復

- 問題：404 修復只要求確認 Listening，無法涵蓋目前介面。
- 修法：改成確認執行仍在等待、Test path 正確、重新按 Execute 後立即送出 URL。
- 驗證：頁面同時說明 404 的三個檢查點，且不依賴藍色外框。

## MINOR

### [STALE_UI] Mac／Windows 安裝頁 C6

- 問題：#06 Webhook AI 測試括號文字暗示藍色 Listening 是固定畫面。
- 修法：改成「畫面進入執行／等待狀態」；學員以 curl 回應、檔案、Telegram 與綠框完成驗收。
- 驗證：Mac 與 Windows 文字保持同一邏輯，僅保留各自終端機語法差異。

## Activity Identity Audit

本次不新增 Demo / Together / Solo 活動，僅修正同一活動的介面判斷與驗收證據；無新增重複產物。

## Shared Copy Audit

| repeated copy | pages | allowed reason | action |
|---|---|---|---|
| Execute workflow／等待狀態／綠框驗收 | 5 頁 + #01 便箋 | 各頁對應不同入口或案例，屬必要操作警告 | 依頁面情境改寫，不新增整段共用口號 |

## Execution Order

1. 建立本 scope 備份與 restore script
2. 修正五個 HTML 頁面與 ZIP #01 便箋
3. 驗證 JSON、ZIP、文字錨點與 diff
4. 執行課程 lint、搜尋索引與 sitemap 重建
5. 產出 `REPAIR-REPORT.md`
6. 只提交本次 scope，commit 後 push `origin/main`
