# Scan: #04 daily report provenance and factuality

日期：2026-09-13

## Evidence reviewed

- Mac execution output：`filesCount: 4`、`aiError: null`。
- `filesProcessed` 卻是 `檔案-1` 至 `檔案-4`，未保留實際檔名。
- 產出的 Markdown 讀到多份輸入中的獨特資訊，但無法從日報逐項回溯來源。

## Findings

| 類別 | 檔案 | 問題 | 嚴重度 |
|---|---|---|---|
| DATA_LINEAGE | `assets/n8n-lite-pack.zip` #04 Code | 正規化檔名未讀取 `binary.data.fileName`，Aggregate 後退回 `檔案-N`。 | BLOCKER |
| TRUST / PROMPT | `assets/n8n-lite-pack.zip` #04 Code | Prompt 未要求來源標記、未指定責任人時填未指定，也未要求揭露衝突數字。 | MAJOR |
| OUTPUT_FORMAT | `assets/n8n-lite-pack.zip` #04 Code | 模型輸出可能保留 `<br>`，寫入 Markdown 後影響閱讀。 | MINOR |
| TEACHING_ALIGNMENT | `m0-workflow-04-daily.html` | 教材描述 `{ fileName, text }`，實跑結果未呈現來源清單，學員無法驗證資料血緣。 | MAJOR |
| TEACHING_ALIGNMENT | `m0-install-mac.html`, `m0-install-win.html` | C5 只檢查日報檔案存在，未檢查 filesCount、來源清單與 aiError。 | MAJOR |

## Correctness review of current report

目前日報包含 `14 個 workflow`、`Big5`、`RPM 限速`、`21 萬`、`P0/P1/P2` 等輸入資料中的獨特內容，顯示模型確實取得文字內容。仍有三個可信度風險：模型把「可考慮」加強成「規劃」、未標示「20 萬內」與「21 萬」的前後差異、替未指定的負責人欄位補上姓名。

## Repair direction

1. 正規化時依序使用 `json.fileName`、`binary.data.fileName`、`info.Title`，最後才使用 `檔案-N`。
2. 在 prompt 中要求每個項目附 `[來源：檔名]`，未提供負責人填 `未指定`，數字或決策衝突並列並註明來源。
3. Code 節點在 Markdown 尾端加入固定來源清單、輸入數量與 AI 錯誤狀態。
4. 將 `<br>` 轉為 Markdown 可讀的換行或分號。
