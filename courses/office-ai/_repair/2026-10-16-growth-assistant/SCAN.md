# office-ai 成長型知識助理內容掃描

**掃描日期**：2026-10-16
**範圍**：CH1-2、CH6-1、CH6-3、課程首頁、課後指南、正式教案來源與驗證紀錄

## 結論

現有課程已教「自由生成」與「指定來源回答」的差異，也有一般 AI 工作流程與 30 天應用計畫；尚未教學員把 Gemini Notebook、`ta-core`、`ta-learning` 與 `ta-work` 組成可長期使用的助理。學員目前無法僅依講義完成 Skill 安裝、來源鎖定、唯讀驗證、來源邊界查核、受控回寫與職務客製化。

## 內容缺口

- CH1-2 仍使用舊名稱 NotebookLM，沒有交代目前課程採用「Gemini Notebook（原 NotebookLM）」名稱。
- CH1-2 沒有說明課程以免費帳號每本 50 筆來源為設計基準，也沒有提供主題式追加策略。
- CH6-1 只教一般 prompt 流程卡，沒有通用 `ta-work`、`ta-core`、Notebook 掛載或辦公行政案例。
- CH6-3 只要求制定 30 天計畫，沒有建立可實際提問、查核與回寫的課後學習助教。
- 首頁與課後指南尚未呈現「可信資料 → Gemini Notebook → ta-core → ta-learning／ta-work → 受控沉澱」的完整主線。
- 三份 Skill 檔與安裝指南位於外部 Google Drive，學員頁沒有可公開解析的本地素材入口。

## 已核對素材

- `SKILL.md`：通用 `ta-work`，包含辦公／專案協作與五項職務客製化參數。
- `SKILL 2.md`：`ta-core`，包含四階來源邊界、Notebook 檢索與受控回寫。
- `SKILL 3.md`：`ta-learning`，包含講義依據、白話教學、盲點提醒與學習沉澱。
- `成長型知識助理雙向建置與操作完全指南.pdf`：提供安裝與對話操作參考；其內含自動部署指令，本輪只作內容來源，不直接作學員上傳素材。

## 平台與方案證據

- 2026-10-16 已用指定付費帳號實際核對 Gemini Skills、Gemini Notebook 連接器與唯讀列出筆記本路徑。
- 付費驗證帳號顯示每本 300 筆；正式講義依使用者要求，以免費帳號每本 50 筆為共同基準。
- 目前帳號中的 `ta-work` 是嘉年華專案客製版；正式教材使用通用版，嘉年華版只作客製化能力示範。

## 技術基準

- 三個目標 HTML 在修改前皆為 0 BLOCKER、0 ERROR；CH1-2 與 CH6-1 各 1 個既有字階 WARN，CH6-3 有 2 個既有 WARN。
- 共用結構檢查三頁皆通過。
- 全課 validator 在修改前已為 `BLOCKED`，主因是 CH1-1、CH6-2 等既有 evidence 雜湊過期；本輪不把既有阻擋誤列為本次造成，也不宣稱全課 `HUMAN_READY`。
- 教案 frontmatter 指向 `_outlines/office-ai.style-guide.md`，但檔案目前不存在；本輪補回最小、可追溯的課程 Style Guide。
