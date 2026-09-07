# gen-ai-36h 課程完善修正設計

日期：2026-09-07
狀態：已獲使用者確認，待執行修復計畫

## 問題定義

目前 36h 課程的 HTML 靜態 lint 通過，但學員路徑仍有四個會阻擋獨立完成的缺口：

1. 大綱明確排除 API，Part 5 卻把 API key 當成主流程前置條件。
2. 實作頁引用事先建立的表單、試算表、音檔、頻道與連線，課程沒有提供固定素材、起始狀態、權限或替代路徑。
3. 多數操作只有步驟敘述，沒有每階段的預期結果、快速檢查、恢復點與安全停止條件。
4. PRAC6／PRAC7 含有需要學員自行改 HTML 的佔位符，無法直接產出有效成果物。

## 設計決策

採用分階段修復，而不是一次重寫 29 頁：

- 第一階段先修最高風險的 Part 5–7 核心交付路徑，建立課程級素材與執行契約。
- API 不再是 36h 零基礎主路徑的必要條件；API 內容若保留，必須標為選修、風險與未驗證分支。
- 免費主路徑採「人工 AI 判斷 + 零代碼自動化」：AI 產生分類／回覆決策，Make 或 n8n 負責表單、試算表、通知與歸檔；不以未驗證的 API 串接宣稱可完成。
- 所有實作以課程提供的最小 fixture 與可複製欄位格式開始，外部 SaaS 工作區的實跑證據另行標記為 `NOT_RUN`，不與靜態教材混稱。
- PRAC6／PRAC7 改成學員可直接填寫、列印或另存 PDF 的成果模板，不要求修改 HTML 原始碼。

## 修復範圍

第一階段預計修改：

- `gen-ai-36h/part5/CH5-1.html`
- `gen-ai-36h/part5/CH5-2.html`
- `gen-ai-36h/part5/CH5-3.html`
- `gen-ai-36h/part5/CH5-4.html`
- `gen-ai-36h/part5/PRAC5.html`
- `gen-ai-36h/part6/CH6-1.html`
- `gen-ai-36h/part6/PRAC6.html`
- `gen-ai-36h/part7/CH7-1.html`
- `gen-ai-36h/part7/PRAC7.html`
- 新增 `gen-ai-36h/assets/` 的最小測試素材與欄位說明
- 新增 `gen-ai-36h/_repair/2026-09-07/` 的修復計畫、驗收報告與 restore script

第二階段在第一階段驗證後，批次補強 Part 1–4 與未涵蓋的章節頁，統一加入 Demo／Together／Solo／Check 契約；不在第一階段偷偷擴大範圍。

## 學員交付鏈

Part 5 產出固定格式的輸入表、AI 判斷紀錄、流程測試紀錄與通知／歸檔證據。

Part 6 將前述交付物映射到場景、觸發條件、輸入欄位、AI 判斷、輸出、例外處理與重跑起點。

Part 7 使用同一份欄位與證據格式完成 MVP 提案、實作紀錄與展示頁，不再要求人工拼接 HTML 片段。

## 驗收條件

- 所有新增或修改 HTML 通過 `python3 docs/lint-page.py`。
- Part 5 主路徑不要求 API key、信用卡或付費方案才能開始。
- 每一個核心操作階段都有可觀察的預期結果、快速檢查與恢復／停止說明。
- 課程提供的 fixture 可讓零基礎學員在沒有自己準備資料時開始操作。
- PRAC6／PRAC7 不再要求修改 HTML 原始碼，且不含假連結或無效佔位 href。
- 靜態驗證與 SaaS 實跑、真人 cold follow-along 分開記錄；未執行者維持 `NOT_RUN`。
- 修復前檔案可由 restore script 還原，修復後產出報告列出未完成的外部驗證。

## 明確不做

- 不把未執行的 Make、n8n、Google Workspace 或 AI 服務操作寫成已通過。
- 不在本階段新增 API、RAG、Agent 或 Function Calling 教學。
- 不以換色、改版或 lint 通過掩蓋學員無法開始、檢查或恢復的問題。
