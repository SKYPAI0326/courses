# CH1-6 批次變體模組卡

本組模組卡只描述批次變體的新增責任；Gemini、Filter、Docs 的核心契約沿用 CH1-3。它不是可直接匯入 Make 的 Blueprint。

## 1. Sheets／資料集合

- **輸入**：`CH1-6-batch-input.csv` 的三筆資料。
- **輸出**：三個獨立 bundle，保留 `record_id`、`message_text`、`needs_review`。
- **檢查**：缺少 `message_text` 或 `record_id` 時，該列標記錯誤，不送 Gemini。

## 2. Iterator／逐筆檢查

- **輸入**：資料集合。
- **操作**：逐筆讀取，依 CH1-2 輸入契約檢查必填欄位與型別。
- **輸出**：合格列進入 Gemini；不合格列留下錯誤與重試位置。
- **控制**：不把空字串當成有效內容。

## 3. Aggregator／批次整理

- **輸入**：Iterator 產生的合格輸出集合。
- **操作**：保留每筆 `record_id` 與三個 Gemini 輸出欄位，加入期間與筆數。
- **輸出**：一份可追溯的週摘要輸入。
- **控制**：任一筆 `needs_review=true` 時，整批送人工出口，不建立不完整 Docs。

## 4. Gemini、Filter、Docs

- Gemini：沿用三欄輸出契約；每筆輸出必須能回到 `record_id`。
- Filter：沿用 `needs_review=false` 通過條件；任一筆 true 即停止整批。
- Docs：只有三筆合格且通過 Filter 時建立一份週摘要文件。
