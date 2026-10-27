# ACP PR 5 小時模組技術檢查紀錄

- 日期：2026-10-24
- 執行者：`tool-run`
- 範圍：CH0-1～CH1-4 教案、內容檢核型 HTML、固定素材、功能地圖 PDF
- 不包含：Windows Premiere Pro 2024 實機操作、教室版截圖、真人跟做

## 教案與 HTML

- 8 份教案執行 `audit_copy_continuity.py`：全部 0 warnings。
- 8 份 HTML 執行 `validate-course-structure.py`：全部 `HTML structure OK`。
- 8 份 HTML 執行 `audit_copy_continuity.py`：全部 0 warnings。
- 8 份 HTML 逐頁執行 `docs/audit-course-substance.py acp-pr --page ...`：全部 `block=0`、`missing_assets=0`。
- 入口與 8 份單元頁共 9 個 HTML 做本機 `href`／`src` 解析：0 missing links。

## 實際瀏覽器

- 以 Chromium 實際開啟 CH0-1～CH1-4。
- 每頁測試 390×844、820×1180、1440×900，共 24 組。
- 全部通過：無頁面級水平捲動、唯一 `main#main`、唯一 learner root、唯一 `h1`、skip link 可聚焦並到達 `#main`。
- CH0-1、CH1-1、CH1-3 另做 1440×1000 預覽目視檢查：標題、警示、圖片／影片容器無重疊或裁切。

## 固定媒體

- 三段基礎 MP4：H.264、1920×1080、25 fps、AAC 48 kHz stereo；長度 12、10、14 秒。
- 基礎 WAV：PCM s16le、48 kHz stereo、20 秒；音訊模式不是全段靜音。
- AI 示範：H.264、1920×1080、25 fps、AAC 48 kHz stereo、120 秒。
- 直式參考片：H.264、1080×1920、25 fps、AAC 48 kHz stereo、25.101 秒。
- 基礎三段、AI 示範三個時間點與直式參考片皆完成代表影格目視檢查，沒有黑畫面或錯置素材。

## PDF

- `object-panel-function-map-v1.pdf`：2 頁、A4 橫式、可文字抽取。
- 兩頁均轉成點陣預覽並逐頁目視檢查：沒有裁切、重疊或不可讀區塊。

## 結論

所測確定性條件成立。這份紀錄只支持內容、檔案、媒體與瀏覽器的機器檢查，不支持 `PLATFORM_VERIFIED` 或 `HUMAN_READY`；Windows Premiere 與真人 Gate 保留待驗。
