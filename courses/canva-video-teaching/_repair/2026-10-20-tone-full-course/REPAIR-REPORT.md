# 全課程操作層級與文案修復報告

日期：2026-10-20

task_scope：`content-change`

狀態：`MACHINE_READY_PENDING_HUMAN`

## 結果

- 使用者已人工確認 CH1-1、CH1-2 樣板更易閱讀；本輪依相同標準完成 CH1-3～CH1-6、CH2-1～CH2-6 與 EXT1。
- 13 份單元頁現在都以淺綠操作區呈現必做步驟；概念、用途、判斷方式、完成檢查與卡住時處理保留為區塊外的完整段落。
- 原本藏在長段落中的動畫、轉場、時間重排、聲畫對齊、字幕母片、學生任務、交付材料及 WhisperDesktop 安裝／燒錄流程，已改為可依序掃讀的步驟。
- 每組步驟前補上具體任務句；沒有把表格、用途說明、判斷原則或參考內容全面清單化。
- 首頁、module 頁與 resources 查閱頁未套用操作框，避免將導覽與參考資料誤作逐步任務。

## 保留事實

- 學習成果、單元順序、案例主題與版本規格不變。
- Canva 操作路徑、時間值、片段長度、檔名、字幕與音訊設定不變。
- 所有正文 href 的順序與目標不變；圖片、表格、下載檔及補充練習保留。
- 每頁原有 section 數、目錄、gate、前後單元導覽、head 與 footer 保留。

## 修改檔案

- 11 份正式來源：`_lessons/canva-video-teaching/CH1-3.md`～`CH1-6.md`、`CH2-1.md`～`CH2-6.md`、`EXT1.md`
- 11 份學員頁：`ch1/CH1-3.html`～`CH1-6.html`、`ch2/CH2-1.html`～`CH2-6.html`、`EXT1.html`
- `_repair/2026-10-20-tone-pilot/sync_two_pages.py`：改為只同步呼叫時明確列出的單元頁
- 本目錄的計畫、雜湊與報告
- `_backup/2026-10-20-tone-full-course-pre-repair/`
- `_tools/restore-2026-10-20-tone-full-course-pre-repair.sh`
- `_validation/tone-full-course-2026-10-20/`

## 驗證

- 備份：23 個檔案的 SHA-256 manifest 全數通過；還原腳本通過 `sh -n`，並在隔離課程樹完成逐檔 `cmp`。
- HTML 結構：13 頁 `checked=13 blocked=0`；每頁只有一個 `.lesson-body`，所有 `.lesson-section` 均在正文容器內。
- 來源忠實度：13 份正式 Markdown 的段落、標題、步驟、表格均可在對應 HTML 找到；沒有 Markdown 粗體標記外露。
- 殼層保護：本輪 11 頁的正文 href 順序、head、gate、nav footer 與 footer 均與備份一致。
- 操作區：13 頁皆有 `action-layout-pilot` 與至少一組非透明 `action-steps`；合計 47 組操作區。
- HTML lint：13 頁 0 BLOCKER、0 ERROR；初次 1 個講師視角 WARN 已改為學員視角，需以最終檢查重驗。
- 文案模式稽核：0 BLOCK；REVIEW 為「完整／最後」等上下文詞，未當作行銷句或機械串場。
- 內容充分性：25 個課程／資源頁 `block=0`、`missing_assets=0`；語意審查仍依工具規則為 `PENDING`。
- 瀏覽器：13 頁在 390 × 844、820 × 1180、1440 × 900 共 39 組通過；無頁面水平溢位，gate 解鎖後不遮內容，目錄數與 section 數一致，操作區底色可見。
- 錨點：13 頁在 390 與 1440 px 的第二節錨點均未被固定頂端列遮住。
- 代表畫面：人工檢視 CH1-4、CH2-4、EXT1 的手機與桌機截圖，操作框、說明段落與功能標籤層級可辨。

最終雜湊記錄於 `FINAL-HASHES.sha256`。

## 回復與限制

執行 `sh _tools/restore-2026-10-20-tone-full-course-pre-repair.sh` 可還原本輪 11 份來源、11 份 HTML 與同步工具。CH1-1、CH1-2 使用先前的兩階段還原腳本。

本輪沒有執行 Git commit 或 push，也沒有修改發布設定。CH1-1、CH1-2 已有人工作者確認；其餘 11 頁完成機器檢查與作者視覺抽查，尚未取得零基礎真人逐頁冷讀，因此狀態維持 `MACHINE_READY_PENDING_HUMAN`。
