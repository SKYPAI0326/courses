# Repair Scan：make-ai-workflow（2026-09-10）

## 範圍

- Make 課程六頁：`CH1-1.html`～`CH1-6.html`
- Make 素材：`assets/`
- n8n 銜接所需的資料契約與課程連結

## 既有狀態

- 六頁已具備通用概念、範例示範、跟做步驟、Checkpoint 與完成驗證。
- Make 契約使用 `customer_identity`、`message_text`、`urgency_signal`、`owner_email`。
- n8n Module 4 目前使用 `applicant`、`document_type`、`due_date`。
- 兩套欄位名稱與語意不同，頁面尚未提供共同的跨平台封裝與轉換判斷。

## 本次主要問題

1. 學員完成 Make 課程後，無法只依頁面判斷哪些欄位可以原樣交給 n8n。
2. 直接把 `customer_identity` 當成 `applicant` 會改變欄位語意；需要明確的 `task_type` 與轉換步驟。
3. n8n bridge fixture 將 Make 的選填 `urgency_signal` 當成必填數字，與 CH1-2 契約不一致。
4. Make CH1-6 的交接包尚未把跨平台契約、轉換前後範例與證據模式列為完成物。

## 放行前提

- 補上可下載的跨平台契約文件與固定 JSON 範例。
- Make CH1-6 加入跨平台銜接示範、選擇步驟、Checkpoint 與完成驗證。
- n8n Module 4 連回同一份契約文件，並修正選填欄位驗證。
- 完成 HTML lint、連結、JSON、語法與禁用句型檢查。
- 真實 Make／n8n 匯入與執行仍由課堂人工驗證，靜態通過不視為平台執行證據。
