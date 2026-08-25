# simple-ai Deliverable Repair Report

status: BLOCKED
date: 2026-08-25
slug: simple-ai

## Scope

本輪完成工作包 A、B、C、D；Task 7 的技術回歸已執行，但內容實質稽核仍有 BLOCKER，因此本課不宣告 READY TO DEPLOY。

## Commits

| 包次 | commit | 內容 |
|---|---|---|
| Baseline | `d8299f8` | 建立四個既有頁面的可回復基線 |
| A | `05b477e` | 完整版手冊 HTML、建置腳本與 65 頁 PDF |
| B | `69941eb` | A4 雙面 10 則 Prompt 精華版 |
| C | `75f38d9` | NotebookLM → Gemini → NotebookLM 查證流程 |
| D | `cf812e0` | 三個課程入口頁的真實 PDF 下載連結 |

## Technical verification

| Check | Result |
|---|---|
| 整課 `lint-page.py courses/simple-ai/ --summary` | PASS：14 頁、BLOCKER 0、ERROR 0、WARN 20 |
| 完整版 PDF | PASS：65 頁、A4 |
| A4 雙面 PDF | PASS：2 頁、A4 |
| 完整版文字錨點 | PASS：五零件、逐字稿、結構化資料、三條紅線、品牌知識庫、三角度、一週七則、15 則、WF-10 |
| 精華版 Prompt 代碼 | PASS：EF-08、EF-01、EF-02、EF-04、NB-01、TK-02、MK-01、MK-02、MK-03、CS-01 |
| 兩份 PDF 彩色／灰階預覽 | PASS：文字、分欄、底色與 Prompt 可讀 |
| 還原腳本 | PASS：`bash -n courses/simple-ai/_tools/restore-2026-08-25-pre-deliverables.sh` |
| 下載連結冷啟動靜態走讀 | PASS：首頁、第二堂、結訓頁的兩份相對 PDF 路徑均存在 |

## Search index and sitemap

Task 7 執行產生器的結果為：`search-index.json` 1332 筆、`sitemap.xml` 119 筆 URL。兩個檔案在 Task 7 開始前已有使用者未提交差異，且重建會納入其他課程的全站變更；為避免誤提交，已恢復到 Task 7 前快照，未納入本輪 commit。

目前 sitemap 只收錄 `simple-ai/handbook.html` 與 `simple-ai/quick-reference.html`；其他課程頁含 `id="_gate"`，依 `docs/build-sitemap.py` 規則刻意排除。

## Content substance blockers

`python3 docs/audit-course-substance.py simple-ai` 目前為 BLOCK：

1. `CH1-3.html` 缺少教案要求的「症狀／原因／Plan B」等價教學表格。
2. `CH1-4.html` 缺少教案要求的「症狀／Plan B」等價教學表格。
3. `CH2-4.html` 缺少教案要求的「學員狀況／Plan B」等價教學表格。
4. `_review/G3-CONTENT-REVIEW.md` 缺少通過的 Content Substance reviewer 存證。
5. `_review/G3-CONTENT-REVIEW.md` 缺少使用者親自完成的三分鐘跟讀／跟做簽核。

稽核工具另外產生了 `_validation/L5-evidence-manifest.json`，目前保留為未提交的驗證中間產物；L5 persona 尚未執行，不把它解讀成放行證據。

## Remaining

- 為 CH1-3、CH1-4、CH2-4 建立新增內容的備份與修復計畫，補回教案要求的完整表格與 Plan B。
- 取得 reviewer 存證與使用者三分鐘真人跟讀／跟做簽核。
- 重新執行 substance audit、L5 evidence／persona 與全課回歸。
- QR Code 仍不加入：目前沒有已驗證的正式公開 PDF URL。
