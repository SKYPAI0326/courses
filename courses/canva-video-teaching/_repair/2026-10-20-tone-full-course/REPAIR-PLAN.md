# 全課程操作層級與文案修復計畫

日期：2026-10-20

task_scope：`content-change`

使用者授權：人工確認 CH1-1、CH1-2 樣板較易閱讀，依同一標準修改其餘課程頁面。

## 範圍

本輪處理 11 份尚未套用樣板的正式單元來源與學員頁：

- CH1-3～CH1-6
- CH2-1～CH2-6
- EXT1

CH1-1、CH1-2 已通過人工樣板確認，本輪只列入全課回歸驗證，不重寫。首頁、場次總覽與資源頁屬導覽或查閱資料，不把它們改成操作講義。

## Finding 與責任層

- `explanation_gap`／G3：操作常藏在長段落中，學員無法快速分辨必做動作、用途與判斷。
- `practice_instruction_gap`／G3：部分頁面的完成檢查與卡住時處理混在操作句尾，掃讀時不易找到。
- `interface_block`／G4：其餘單元尚未套用 CH1-1、CH1-2 已確認的操作區視覺層級。

## 修改原則

1. 保留學習成果、操作順序、檔名、時間值、介面路徑、連結、圖片、表格與補充練習。
2. 把必須依序完成的動作放入獨立步驟；概念、理由、判斷與限制維持段落。
3. 適用時以「用途／完成檢查／判斷方式／卡住時」直接標示段落功能，不為對稱而強加標籤。
4. 每一組步驟前先說明任務；步驟後保留可觀察結果或回復位置。
5. HTML 僅由正式 Markdown 重新產生正文，再以 DOM 工具套用 `action-layout-pilot`、`action-steps` 與主要清單標籤；保留既有殼層、gate、導覽與 href。

## 目標檔案

- `_lessons/canva-video-teaching/CH1-3.md`～`CH1-6.md`
- `_lessons/canva-video-teaching/CH2-1.md`～`CH2-6.md`
- `_lessons/canva-video-teaching/EXT1.md`
- `courses/canva-video-teaching/ch1/CH1-3.html`～`CH1-6.html`
- `courses/canva-video-teaching/ch2/CH2-1.html`～`CH2-6.html`
- `courses/canva-video-teaching/EXT1.html`
- `_repair/2026-10-20-tone-pilot/sync_two_pages.py` 改為可接受明確頁面清單的同步工具
- 本目錄的報告、備份 manifest 與回復腳本

不修改大綱、學習成果、素材、下載檔、JavaScript、密碼、發布設定、首頁、module 頁或 resources 頁。

## 驗收

- 13 個單元頁都只把必做操作放進淺綠操作區；說明與用途仍可連續閱讀。
- 正式來源與 HTML 可見正文一致，沒有 Markdown 標記外露。
- 每頁維持唯一 `.lesson-body`，所有 `.lesson-section` 均在其中，section、目錄、導覽與 gate 正常。
- HTML lint、結構檢查、文案風險掃描、來源忠實度及 `git diff --check` 通過。
- 390、820、1440 px 代表頁與全頁自動 smoke test 無水平捲軸；操作區有明確底色，桌機與手機均可讀。
- 本輪可達 `MACHINE_READY_PENDING_HUMAN`；不以作者模擬宣稱全課真人冷讀或平台功能全部通過。

## 回復

第一次修改前建立 `_backup/2026-10-20-tone-full-course-pre-repair/`，保存 11 份正式來源、11 份 HTML 與同步工具，產生 SHA-256 manifest 與 `_tools/restore-2026-10-20-tone-full-course-pre-repair.sh`。還原腳本須通過語法與隔離雜湊驗證。
