# Deep Review 修正報告

日期：2026-10-27

## 結果

已完成 Judge 指定的 F01～F08 `fix_now`。F09 維持 `improve_later`，未擴大修改。

## 已修正

- CH1-1 的復原練習現在會從 `classroom` 正確回到 `library`。
- CH2-2／CH2-3 與聲音資源分開處理 Record Voiceover、AI Voice、36 秒 WAV、十秒位置 WAV＋分句 WAV；每條路徑都有真實可切的停頓與完成檢查。
- 新版時間軸用語已取代相關頁面式用語；CH2-6 改為下載完整 36 秒作品。
- CH2-4 改用能證明音訊可選的實測字幕圖，WhisperDesktop 連結改到正式 `EXT1.html`。
- 學生任務改為位置／活動一／活動二／提問，可同時支援圖書館與電腦教室。
- 講師筆記把主路徑改正為 `Audio → Record Voiceover`，`Record yourself` 只保留選做畫中畫。
- CH2-6 與課綱新增課後完整新題材遷移驗收：須同步更換素材、文字、旁白、字幕與提問，繳交 MP4、可編輯網址及修改說明。
- HTML、純文字下載、搜尋索引、文字包及離線包已同步重建。

## 驗證

- 10 個受影響頁：HTML structure 0 blocked；substance machine check 0 block、0 missing assets。
- 29 個正式 HTML：本機 href／src 0 缺漏。
- 兩個 JSON 可解析；兩個 ZIP CRC 通過，離線包含 CH2-4、CH2-6、技術卡與 EXT1。
- scoped lint：0 BLOCKER。5 個課程單元頁共 30 個既有 SEO metadata 規則錯誤；修正前備份結果相同，非本輪新增。
- browser smoke：5 頁 × 3 種寬度共 15 組，0 水平溢位、0 缺圖、唯一 `.lesson-body`，關鍵修正文案皆存在。
- `git diff --check`、備份 SHA-256 與 restore script 語法通過。

## 證據邊界

- [UPDATE] 2026-10-27 後續已在授課帳號的 36 秒作品複本重跑 `Record Voiceover`：實際入口為「應用程式 → 音訊 → 錄製配音」，麥克風權限由 `prompt` 轉為 `granted`，完成後產生 12.8 秒獨立「語音錄製」音訊軌。詳見 `_validation/PLATFORM-RECORD-VOICEOVER-2026-10-27.md`。
- 本機預覽仍顯示課程密碼門；未取得密碼，因此瀏覽器檢查只證明 DOM 版面與素材載入，不宣稱登入後完整視覺驗收。
- F09 依 Judge 判決留待後續，不在本輪修正。

## 回復

執行 `_tools/restore-2026-10-27-deep-review-fixes-pre-repair.sh` 可還原本輪 52 個既有目標；原始雜湊在 `_backup/2026-10-27-deep-review-fixes-pre-repair/ORIGINAL-SHA256SUMS.txt`。
