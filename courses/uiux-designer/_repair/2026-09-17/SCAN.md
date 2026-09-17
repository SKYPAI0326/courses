# UI/UX Designer 修復掃描

**日期**：2026-09-17
**範圍**：B6 Prototype 任務測試、B7 Handoff、B8 網頁與版本交付
**掃描方式**：HTML 連結順序、第一步文字、內部文件目標、既有 lint／連結掃描結果

## BLOCKER

### [ASSET_DISCOVERABILITY] 起始材料晚於第一次操作

B6、B7、B8 都在第一個情境表要求學員開啟起始材料，材料連結卻出現在後面的段落。學員需要回頭搜尋頁面，或依賴講師口頭指出位置。

- B6：第一段要求開啟 B6 起始頁；連結在交付段落。
- B7：第一段要求開啟 B7 起始頁；連結在凍結來源段落。
- B8：第一段要求開啟 `web-starter/index.html`；README 連結在下一段操作列表之後。

**修法**：在第一次操作前加入「起始材料」連結、檔案用途、使用時機與無法開啟時的本機路徑；保留後段交付清單作為補充。

## MAJOR

### [NAV_OPS] 學員頁暴露製作層 Blueprint

B6、B7、B8 的頁首連結指向 `../_design/COURSE-BLUEPRINT.md`，文字卻寫成「返回課程藍圖」。Blueprint 是製作層文件，不能作為學員導覽目標。

**修法**：改為「返回課程總覽」，目標為 `../index.html`（B6/B7）或 `../index.html`（B8）。

## 既有檢查結果

- HTML lint：前一輪 50 頁，0 BLOCKER、0 ERROR、0 WARN。
- 相對連結存在性：185 個連結，0 missing。
- 以上兩項沒有抓到語意錯誤，因為 Blueprint 檔案存在，起始材料連結也存在；本輪新增「目標層級」與「第一次使用順序」檢查。

## Activity Identity Audit

| page | section | role | material | artifact | path | learner decision | overlap verdict |
|---|---|---|---|---|---|---|---|
| B6 | 01–08 | Skill-operation | B4 Prototype、B6 START-HERE、TASK-TEST-FORM | case_id、Actual／Expected、repair、rerun_result | 固定任務→記錄→單一變因修正→回歸 | 判斷根因分類與是否可交 B7 | 本輪只修入口順序與導覽，活動身分不變 |
| B7 | 01–08 | Skill-operation | B6 回歸版本、B7 START-HERE、HANDOFF-CHECK | PNG／PDF、Inspect 筆記、Handoff 清單 | 凍結來源→輸出→Inspect→交接 | 判斷哪些證據已驗證、哪些仍受限 | 本輪只修入口順序與導覽，活動身分不變 |
| B8 | 01–08 | Integration-capstone | web-starter、README、B7 Handoff | 本機互動頁、手機截圖、Git diff／commit | 開頁→互動→手機驗收→版本化 | 判斷本機完成與外部發布邊界 | 本輪只修入口順序與導覽，活動身分不變 |

## Shared Copy Audit

本輪未刪除任何教學段落；只會改三個學員頁的頁首導覽與第一次材料入口。共用安全限制與交付邊界保留在各自單元的必要位置。

## 判定

`BLOCK`：修復完成並重新跑 semantic smoke、lint、相對連結與 Chrome 試走前，不交人工審查。
