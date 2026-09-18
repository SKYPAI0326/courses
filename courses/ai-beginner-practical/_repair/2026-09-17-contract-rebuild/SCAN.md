# Scan：AI 入門即戰力契約重建

日期：2026-09-17

## 既有狀態

- 四份教案與四頁 HTML 已有大量案例、提示詞、素材與完成物；問題不是缺少課程主題，而是學員入口資訊分散在不同段落。
- 原本頁面可看見概念、示範與練習，但「一開始要用什麼材料、要存成什麼、完成後誰會使用、失敗回哪裡」不一定能在第一個動作前回答。
- CH2 的核心素材原為 Markdown 直連，對部分頁面稽核與一般學員的開啟方式不穩定；已增加可直接閱讀的素材頁，保留原始 Markdown 下載。
- 原有內容維持平台中立；NotebookLM 只在第 3 單元作為固定平台，未恢復 ChatGPT／Gemini 指定操作，也未新增資安專題。

## 本輪處理邊界

只修改 `ai-beginner-practical`：四份 lesson plan、四頁 learner-facing HTML、Blueprint、Coverage Ledger、CH2 素材頁、課程 gate 紀錄與驗收報告。其他課程的既有未提交變更保留不動。

## 風險分級

| 風險 | 原因 | 本輪處理 | 狀態 |
|---|---|---|---|
| 學員不知道第一步 | 材料、完成物與動作散落 | 四頁開場加入唯一八欄學員任務契約 | PASS |
| 只看示範、沒有可交付物 | 產物格式與下一次用途不夠靠前 | 各頁明列檔名、格式、下一位使用者與保存動作 | PASS |
| 卡住時只能重新猜 | 回復位置未集中 | 各頁加入恢復代碼與離線／安全停止路徑 | PASS |
| CH2 素材不易開啟 | 直接裸 Markdown href | 增加 HTML 素材頁，並保留原始檔下載 | PASS |
| 手機版密集表格閱讀 | 表格與程式區塊可能造成窄版壓迫 | 共用 CSS 對窄版表格啟用可控橫向閱讀；程式區塊已有換行 | MACHINE_CHECKED |
| 真人是否能獨立完成 | 靜態檢查不能替代真人冷讀 | 保留 L4a／L5 待人工或外部模型證據 | PENDING_HUMAN |

## 契約來源

以 `../_規範/learner-action-contract.md` 為唯一學員行動契約，並依 `../_規範/course-content-substance.md`、lesson-type contract、beginner continuity gate 與 quality gate 檢查。沒有另造第二套學員 checklist。
