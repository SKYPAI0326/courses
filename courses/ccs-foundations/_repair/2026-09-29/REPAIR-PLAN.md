# Repair Plan: ccs-foundations

## Scope

- task_scope: `content-change`（僅首頁定位／導覽與 CH4 舊頁前進連結；新版單元正文不改）
- pages: `index.html`, `CH4.html`, `CH5-1.html`–`CH5-4.html`
- lessons: `_lessons/ccs-foundations/CH5-1.md`–`CH5-4.md`
- archive: `courses/ccs-foundations/_archive/2026-09-29-legacy-ch5/`
- backup: `courses/ccs-foundations/_backup/2026-09-29-pre-primary-switch/`
- release boundary: 不發布、不提交 Git、不重建全站搜尋索引或 sitemap。

## Risk

- 新 9 小時主線成為首頁入口；瀏覽器 RWD 與真人／平台驗收仍未完成，驗收狀態必須保留 `PENDING`／`BLOCKED`。
- 封存只移動已同意排除的 CH5 Markdown 與 HTML。其餘舊頁保留。
- 修改前已複製 11 個目標檔案到 pre-switch backup；使用者資料與其他課程變更不納入本次操作。

## BLOCKER

### [NAV_OPS] 舊首頁與新版課程定位不一致

- 問題：首頁仍顯示舊版 13 單元及延伸內容，主卡片沒有連至新版 v2 頁面。
- 修法：沿用原首頁版型，更新 metadata／hero／時數統計；首頁僅列 5 個 Part 1 單元及 4 個題庫單元，分別連到 9 個 v2 頁面，顯示 6 小時 + 3 小時 = 9 小時及 Q1–Q80。
- 驗證：逐卡核對連結存在；`lint-page.py`、`audit-course-substance.py`；檢查不再連到 CH5 舊頁。瀏覽器 RWD 另標待驗。

### [NAV_OPS] 封存後舊課程導覽失效

- 問題：舊首頁連到 CH5-1 至 CH5-4；CH4.html 前進連結指向 CH5-1。
- 修法：封存 4 個舊 HTML 與 4 份 Markdown；CH4.html 的下一步改回新版課程首頁。封存前版本及所有原始檔案已備份。
- 驗證：首頁 9 個新單元均存在；活動頁不再連向根目錄的 CH5；CH4.html 的首頁連結可解析；封存頁與 source lesson 副本可還原。

## MAJOR

- 題庫沒有獨立官方答案鍵；保留既有「題庫預期答案」措辭與題目疑義，不改題庫答案資料。
- RWD、真人初學者冷讀、平台實測未完成；本次不宣告 G3／G4／發布通過。

## Activity Identity Audit

此修復不更動任何教學活動，不新增或刪除學員活動；只改首頁卡片入口及舊 CH4 導覽。

## Shared Copy Audit

只整理首頁重複／過時的課程摘要；9 個新版頁面與教案全文不改。

## Execution Order

1. 建立 scan／plan，完成 11 個目標檔案備份及還原腳本。
2. 封存 4 個已核准排除的 Markdown 與 HTML。
3. 更新首頁主線及 CH4 返回首頁導覽；在 gates 留下切換及未驗收狀態。
4. 執行連結、lint、靜態結構與課程素材稽核；重跑驗證報告。
5. 不發布、不提交；列出 RWD、全站索引與 sitemap 的後續待辦。

## Addendum: legacy CH1-1 HTML syntax repair

- task_scope: `syntax-only`。使用者同意將舊版 `CH1-1.html` 納入修復；只修標籤結構，不改可見文字、href、課程順序或教學區塊。
- Root cause: 兩組比較卡內共 16 個 `.compare-item` 使用 `<span><div class="compare-dot"></span></div>`；關閉標籤順序與巢狀順序相反，令行內 span 在區塊 div 尚未關閉時先被關閉，既有 validator 接著報出連鎖的錯置／未配對標籤。
- Minimal repair: 依相鄰既有課程頁寫法，把每個錯誤片段改為同層 `<span class="compare-dot" aria-hidden="true"></span>`，保留父層 `.compare-item` 與原文字內容。
- Before/after verification: 修復前 `validate-course-structure.py` 對此頁為 BLOCK；修復後須通過同一檢查器、`lint-page.py`、`audit-course-substance.py`，並用 `check_content_unchanged.py` 證明文字與 href 不變。全課 RWD smoke 仍需另行完成。
- Backup: `_backup/2026-09-29-pre-ch1-1-syntax-fix/pages/CH1-1.html`；還原腳本 `_tools/restore-2026-09-29-ch1-1-syntax-fix.sh`。
