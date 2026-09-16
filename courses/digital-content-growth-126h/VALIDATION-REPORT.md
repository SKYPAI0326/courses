# 數位內容與成長行銷人才培訓｜整合驗收報告

**驗收日期：** 2026-09-16  
**範圍：** `digital-content-growth-126h/`、對應 `_lessons/`、搜尋索引與 sitemap

## 已確認

| 項目 | 結果 | 證據 |
|---|---|---|
| 教案單元 | PASS | 40 份、總時數 126 小時、依賴鏈存在 |
| 本機資產 | PASS／部分 BLOCK | 40 份模板、3 組合成 CSV、環境與權限說明；外部平台資產列為 BLOCK |
| learner-facing HTML | PASS（結構） | 40 單元頁、6 Part 導覽頁、1 課程入口，共 47 頁 |
| 課程範圍 lint | PASS | 47/47 通過 `docs/lint-page.py` |
| 相對連結 | PASS | 0 個不存在的本機目標 |
| 佔位連結 | PASS | `#`、前後頁佔位符與 `{{...}}` 均為 0 |
| 模板可發現性 | PASS | 40/40 單元頁都有對應模板連結 |
| 文案連貫性 heuristic | PASS | 40/40 單元頁，0 warning |
| 搜尋索引 | PASS | `../search-index.json`，719 筆 |
| Sitemap | PASS | `../sitemap.xml`，94 個 URL |

## 尚未放行的項目

- LocalWP 示範網站、GTM 測試容器、GA4 Demo Account 與正式 Search Console 權限尚未完成課前驗證。
- Google Ads、Meta Ads、LINE 的示範帳號、平台畫面、正式事件與付費投放權限尚未提供；課程只使用企劃、合成資料與紙面／本機模擬。
- Part 1–6 的正式參考完成品、部分案例卡、格式卡、資料包與共同評量規準仍需教師補齊或確認。
- `audit-course-substance.py` 不存在於本專案，因此沒有以該腳本宣稱內容實質通過；本報告只記錄已執行的結構、連結與連貫性檢查。

## 人工下一步

請從 [MANUAL-LEARNER-RUN.md](MANUAL-LEARNER-RUN.md) 開始，依入口逐單元實跑。對每個 `REVISE` 或 `BLOCK` 記錄：

1. 你當下手上的材料與頁面位置。
2. 第一次卡住的句子、欄位、檔案或操作。
3. 你最後採用的修復方式，或仍缺少的外部條件。
4. 是否能產出頁面承諾的成果並回答檢核題。

全域建置器目前仍會被其他既有課程的 3 個舊 blocker 擋住；這不改變本課程上述 scoped validation 的結果，也不代表本課程已完成正式平台試教。
