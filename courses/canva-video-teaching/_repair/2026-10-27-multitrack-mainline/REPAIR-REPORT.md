# Canva 影音剪輯課程多軌主線修復報告

日期：2026-10-27

## 結果

已依改善提案完成課程主線修復。新建影片只走 Canva 多軌時間軸；兩場沿用同一支固定 36 秒作品，第一場完成 v1，第二場複製為 v2，再加入旁白、配樂與字幕。34 秒與 38 秒只保留在具名實驗副本，不接續第二場。

## 已完成

- 課程大綱與 CH1-1～CH2-6 全部改為主軌、上層視覺軌、音訊軌的單一路徑。
- CH2-2 主入口改為 `Audio → Record Voiceover`；AI 語音與 WAV 為同一音訊軌的備援。
- CH2-3 在標準 v2 實際分割一段旁白停頓，CH2-4 直接在標準 v2 校訂一處字幕文字與一處起訖／漏句。
- `Canva功能與技巧`、`時間軸與字幕實作`、開始準備、案例、學生任務與四片段恢復頁同步修正。
- 新增 `resources/舊專案相容處理.md/.html`，集中保留 2025 年 10 月以前舊設計的頁面式維護方式。
- learner-facing HTML、首頁搜尋、文字下載包、離線講義包、搜尋索引與 continuity inventory 已同步。

## 驗證結果

- 備份 manifest：全部雜湊通過；隔離目錄回復演練通過。
- YAML/frontmatter、22 個本次頁面、內部連結、搜尋索引與兩個 ZIP：通過。
- HTML contract：29 頁、0 blocked。
- course substance machine check：26 頁、0 block、0 missing assets；語意品質以本輪人工主線核對與 copy continuity 檢查補足。
- copy continuity：12 個核心單元與 7 個本次資源頁皆 0 warning。
- scoped lint：0 BLOCKER；核心單元頁仍有既有的 6 項 SEO metadata 提示，不影響本輪 learner flow。
- 瀏覽器：390×844、820×1180、1440×900 檢查首頁、CH2-4、舊專案相容頁，無水平溢位；延遲圖片載入完成。首頁搜尋「舊專案」只回傳新相容頁。
- `git diff --check`：通過。

## 目前證據邊界

- [UPDATE] 2026-10-27 後續已在授課帳號的 36 秒作品複本重跑 `Record Voiceover`：實際入口為「應用程式 → 音訊 → 錄製配音」，麥克風權限由 `prompt` 轉為 `granted`，完成後產生 12.8 秒獨立「語音錄製」音訊軌。新版完整錨點圖組仍未補齊；詳見 `_validation/PLATFORM-RECORD-VOICEOVER-2026-10-27.md`。
- 本輪未發布、未 commit、未 push，也未修改 EXT1。

## 回復

執行 `_tools/restore-2026-10-27-multitrack-mainline-pre-repair.sh` 可還原本輪目標檔案，並移除新增的舊專案相容頁與文字下載。
