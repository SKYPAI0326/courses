# CH1-1／CH1-2 講義語氣樣板修復報告

日期：2026-10-20

task_scope：`content-change`

狀態：`PENDING_USER_TONE_CONFIRMATION`

## 結果

- 保留兩頁原有情境、概念、操作、檢查、補充練習與單元銜接。
- CH1-1 將觀看成品、檢查素材、輸入標題、復原與重開改為可掃讀步驟；可見正文由 1,854 字元降至 1,784 字元。
- CH1-2 將匯入介面拆成「新版多軌／既有頁面」兩條路徑，並把留下十秒、調整構圖及完成檢查的動作獨立列出。字元增加來自原本隱藏在長句中的兩條介面路徑，不是新增教學功能。
- 第一輪只有文字與清單結構，使用者確認畫面差異仍不明確。第二輪把必做操作放進淺綠底、完整邊界的操作區塊，並以「操作步驟」標出主要流程；用途、完成檢查、判斷方式與卡住時仍在區塊外以段落呈現。
- 視覺規則只套用在具有 `action-layout-pilot` 的 CH1-1、CH1-2，不改其他講義頁。
- 學習成果、檔名、連結目標、Canva 操作值、圖片、頁面 section 數、密碼入口及導覽均未改變。

## 修改檔案

- `_lessons/canva-video-teaching/CH1-1.md`
- `_lessons/canva-video-teaching/CH1-2.md`
- `courses/canva-video-teaching/ch1/CH1-1.html`
- `courses/canva-video-teaching/ch1/CH1-2.html`
- `courses/canva-video-teaching/assets/handout.css`（限定樣板類別的操作區樣式）
- 本目錄的計畫、同步工具與報告
- `_backup/2026-10-20-tone-pilot-pre-repair/`
- `_backup/2026-10-20-tone-clarity-pre-repair/`
- `_tools/restore-2026-10-20-tone-pilot-pre-repair.sh`
- `_tools/restore-2026-10-20-tone-clarity-pre-repair.sh`
- `_validation/tone-clarity-2026-10-20/` 的桌機與手機代表畫面

## 驗證

- 文案模式稽核：0 BLOCK；5 個 REVIEW 為「完整／最後」等上下文詞，人工確認不是空泛宣傳或機械式步驟鏈。
- HTML lint：兩頁 0 BLOCKER、0 ERROR、0 WARN。
- DOM：每頁只有一個 `.lesson-body`，所有 `.lesson-section` 均在其中；CH1-1 保留 6 節，CH1-2 保留 7 節。
- 來源忠實度：兩份正式 Markdown 的段落、標題、步驟與表格內容均可在對應 HTML 正文找到。
- 視覺標記：CH1-1 有 4 組操作區，CH1-2 有 7 組；「用途／完成檢查／卡住時／判斷方式」均正確輸出為粗體文字，沒有殘留 Markdown 星號。
- 瀏覽器：CH1-1、CH1-2 在 390 × 844、820 × 1180、1440 × 900 均無水平捲軸；操作區有非透明底色，目錄數與 section 數一致，密碼入口解鎖後不遮擋內容。
- `git diff --check`：本次目標檔無 whitespace error。

## 最終雜湊

- `CH1-1.md`: `e69ee7afc0bffd0fe245024200e5bca0d894c6a486e1673f374319a295c59709`
- `CH1-2.md`: `0097c4f80bc075f8dd5af4267544d5ee2fbbb91d25a0eda7ceff093f5559821c`
- `CH1-1.html`: `55a8b462bb24bb85db533c28c9aac251d5a213c2c1d0c3b803f5f30b97ee21f8`
- `CH1-2.html`: `f66d53addadab55ce9321967aa1c7d5ffec98d9afe1191d5f02b96b349433b86`
- `handout.css`: `3dfbd479151acf2145b67e217621f20abe0ec1b272724885b067a4a259cf5f24`

## 回復與限制

執行 `sh _tools/restore-2026-10-20-tone-pilot-pre-repair.sh` 可還原最初的四個內容檔；執行 `sh _tools/restore-2026-10-20-tone-clarity-pre-repair.sh` 可只撤回第二輪視覺層級。兩支腳本皆已通過 `sh -n`，並在隔離目錄證明還原雜湊與備份 manifest 一致。

本輪只建立兩頁語氣樣板，不代表其他十個核心單元已修復，也不宣稱零基礎真人冷讀通過。是否擴至其餘單元，需先由使用者確認這次語氣。
