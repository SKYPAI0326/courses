# 5 小時學員網頁講義保真檢核

- 執行者：`author-self-check`
- 日期：2026-10-24
- 正式來源：`_lessons/ai-short-video-editing/CH0-1.md` 至 `CH1-4.md`
- 成品：`ai-short-video-editing/index.html` 與 CH0-1～CH1-4
- 結論：Deep Review 修正後，正式來源與 HTML 的受影響文字已同步；此為保真檢查，不代表內容阻擋已解除。

## 對照結果

| 範圍 | 正式 HTML 呈現 | 結果 |
|---|---|---|
| CH0-1～CH0-2 | 固定素材、完整示範、時間碼練習、復原與輸出檢查 | learner-content 完整保留 |
| CH0-3 | 四層、七家族、Unlink 完整示範、固定五題與答案連結 | learner-content 完整保留；平台狀態依新證據更新 |
| CH0-4 | 六格拆解、示範、跟做、固定四題與完成紀錄 | learner-content 完整保留 |
| CH1-1～CH1-2 | 原片、練習 SRT、否定詞示範、提示詞、CSV、固定 AI 候選 | learner-content 完整保留；AI 服務失效仍可完成主線 |
| CH1-3～CH1-4 | 固定三段時間碼、直式序列、字幕 fallback、參考片、取捨紀錄 | learner-content 完整保留 |

## 正式版新增內容

- 課程首頁明示 5 小時模組與 4 小時題庫、3 小時考試的邊界。
- 提供基礎素材與 AI 示範素材入口。
- 明列五項學習成果檔案，讓學員能依可觀察結果自行驗收。
- 8 頁統一正式 canonical、Twitter metadata、首頁與前後單元導覽。
- 平台說明明確區分「Premiere Pro 2024 教案用語」與「Premiere Pro 26.0.0 Build 72 實機驗證」。

## 驗證狀態

- `PASS`：9 頁 course HTML structure，`checked=9 blocked=0`。
- `PASS`：9 頁 V4 lint，`BLOCKER=0, ERROR=0, WARN=0`。
- `PASS`：8 個教學單元 substance audit，`missing_assets=0`。
- `PASS`：正式版 9 頁本機連結，`missing_assets=0`。
- `PASS`：390×844、820×1180、1440×900，共 27 組內建瀏覽器 smoke test；無頁面級水平溢位、header 遮擋或主內容結構錯誤。
- `PASS`：9 頁 skip link 均為第一個鍵盤焦點且可抵達 `#main`。
- `PASS`：首頁、CH0-3、CH1-3 三種尺寸共 9 張截圖完成目視檢查。
- `BLOCKED`：客製字幕重映射尚無完整方法與證據；CH0-3 代表練習尚缺完整參數、素材與終態證據。
- `PENDING_HUMAN`：解除內容阻擋後的零基礎 5 小時 cold follow-along。

結論：正式網頁的確定性結構與版面檢查通過，來源／成品同步；整體正式狀態為 `BLOCKED`，不可標記為 `MACHINE_READY_PENDING_HUMAN` 或 `HUMAN_READY`。
