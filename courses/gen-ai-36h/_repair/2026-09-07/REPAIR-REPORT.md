# gen-ai-36h 修復報告：2026-09-07

## 證據狀態

| 類型 | 狀態 | 說明 |
|---|---|---|
| 修復前備份 | PASS | 已保存 30 個修復前課程檔案 |
| Restore script 語法 | PASS | `bash -n` 通過；未執行還原以保留修復結果 |
| HTML lint | PASS | 29 個課程頁面掃描，BLOCKER 0、ERROR 0 |
| 連結／佔位符掃描 | PASS | 素材相對路徑存在，placeholder href 0 |
| Make／n8n 工作區實跑 | NOT_RUN | 本批次不冒充外部執行證據 |
| 真人 cold follow-along | NOT_RUN | 尚未有學員試跑紀錄 |

## 未完成邊界

即使靜態驗證全部通過，也不代表 G4／G5 或課程真人驗收已通過；外部帳號、權限、版本、地區與真人試跑需另行記錄。

## 本批次已完成

- Part 5：補輸入契約、CSV 測試資料、會議文字 fixture、免費主路徑、人工覆核、checkpoint、恢復點與 `NOT_RUN` 邊界。
- Part 5：將 API／Tunnel／價格內容改為選修或需實測的環境分支，移除主流程的 API key 前置條件。
- Part 6：補固定跨 Part 交接欄位，PRAC6 改為可直接填寫與列印的模板。
- Part 7：補 MVP 證據界線，PRAC7 改為可直接填寫的發表頁，移除假連結與 HTML 編輯要求。
- Part 1–4：16 個 CH／PRAC 頁補上 Demo／Together／Solo／Check 操作契約，加入預期結果、重跑點與 `NOT_RUN` 邊界。
- Part 6–7：CH6-2、CH7-1、CH7-2、CH7-3、PRAC6、PRAC7 均補上場景地圖、MVP、展示與交接的驗收契約。

## 本批次未完成

- 尚未在實際 Make、n8n、Google Workspace、AI 服務帳號中 Import、重綁連線、執行四筆測試與確認版本／額度。
- 尚未進行零基礎真人 cold follow-along，因此課程 Gate 不提升為 G4／G5 PASS。
- 目前操作契約是頁面級靜態引導，尚未用真人 cold follow-along 驗證每個步驟的實際耗時與阻塞率。
