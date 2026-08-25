# simple-ai 章節下載連結修復計畫

## Scope

- slug: `simple-ai`
- learner pages: `CH1-1.html`–`CH1-4.html`, `CH2-1.html`–`CH2-4.html`
- course-level links: `index.html`, `module2.html`, `CH2-4.html`
- generated page: `handbook.html`（由 `_tools/build-deliverables.js` 重建）
- assets: `assets/datasets/*.txt`

## Problem

目前章節素材只嵌在 HTML，學員無法在對應章節下載可保存的文字檔；既有 PDF 下載卡雖有 `download`，但缺少另開分頁屬性。修復後每個素材連結都必須指向實際存在且非空的 `.txt`，並具備 `target="_blank" rel="noopener" download`。

## Material mapping

| page | downloadable material |
|---|---|
| CH1-1 | EF-08 個人化 AI 助理設定對照與驗證素材 |
| CH1-2 | EF-01 會議逐字稿、EF-05 客戶 LINE 長訊息 |
| CH1-3 | 三張 EF-02 報價單、EF-04 漲價與棘手信件情境卡 |
| CH1-4 | 三條資安紅線 NG/OK 對照與發佈前檢查清單 |
| CH2-1 | NotebookLM 品牌資料庫的官網文案、菜單、評論摘要 |
| CH2-2 | TK-02 品牌定位輸入素材 |
| CH2-3 | MK-01/02/03 社群內容產線的完整範例素材 |
| CH2-4 | CS-01 FAQ 的跨行業填空範本、常見問題與 SOP |

## Acceptance

1. 每個 CH 頁面至少有一個章節專屬 `.txt` 下載連結；不以檔名代替內容。
2. 每個新增或既有 PDF 下載 anchor 均有 `target="_blank" rel="noopener" download`。
3. 所有 anchor 的 `href` 均能在本機 HTTP server 解析，目標檔案非空。
4. 以瀏覽器實際點擊至少一個章節素材與一個 PDF，記錄下載事件／檔名，並核對另開分頁屬性。
5. `python3 docs/lint-page.py courses/simple-ai/ --summary` 無 BLOCKER。
6. 重建 `handbook.html` 後再次檢查連結與 lint；不宣稱 PDF 內嵌的本機 `file://` 連結可供其他學員使用。

## Execution order

1. backup + restore script
2. add source-derived `.txt` files
3. add chapter links and PDF anchor attributes
4. rebuild generated deliverables
5. browser click verification, lint, diff check, scoped commit
