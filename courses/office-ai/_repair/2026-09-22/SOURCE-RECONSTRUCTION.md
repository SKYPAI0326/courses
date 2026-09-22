# Source Reconstruction Record: office-ai

## 目的

本課程原本只有 learner-facing HTML，缺少可供 `course-designer`、`course-reviewer` 與 `course-validator` 追溯的單元來源。本輪先把現有頁面中已存在的教學內容整理成 19 份 Markdown source，再以新規則檢查，不把重建結果冒充全新教案或真人驗證。

## 來源與範圍

- 來源頁面：`courses/office-ai/ch*/CH*.html`
- 對照大綱：`_outlines/office-ai.md`
- 產出：`_lessons/office-ai/CH*.md`，共 19 份
- 每份 source 都有 frontmatter、課型、學習目標、style guide、唯一 learner-content 邊界與來源狀態 `legacy-reconstructed-draft`。
- `<!-- learner-content:start -->` 與 `<!-- learner-content:end -->` 以外的內容只供設計、審查與版本追蹤，不會送進學員講義。

## 保真規則

1. 保留現有 HTML 的標題、情境、輸入、示範、輸出、練習、檢查、修復、延伸與本地素材引用。
2. 只把 HTML 結構轉成可讀 Markdown，不憑記憶增加平台功能、步驟或案例事實。
3. 發現概念頁缺少任務契約時，先補一個有目的的起始材料／第一個判斷／完成物／修復段落，再同步 source 與 HTML；不以增加卡片或步數灌水。
4. 平台路徑仍依 validator 保留待驗：目前 `CH1-2` 與 `CH5-1` 需要實際平台測試，其餘頁面採平台中立文字不宣稱已驗證。

## 本輪新增契約

- `CH1-1`：四個辦公情境分類，產出任務適配判斷表。
- `CH1-2`：會議逐字稿來源邊界判斷，產出工作模式卡。
- `CH6-2`：四種資料情境的敏感性分類，產出去識別化檢查表。
- `CH6-3`：低風險週任務選擇與基準／頻率／checkpoint 規劃，產出 30 天計畫。

## 限制

來源重建與作者自審只證明目前檔案可追溯、機器可檢查；它不能證明學員能獨立完成。獨立 reviewer、平台實跑、真人 cold follow-along、理解、遷移與三課 sequence 仍須依 `_validation/FINAL-REPORT.md` 的 pending 清單完成。
