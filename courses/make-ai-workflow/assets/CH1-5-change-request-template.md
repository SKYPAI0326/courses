# CH1-5 變更需求單：change-request-v1

> 先複製本檔再填寫。一次只處理一個主要變因；不要把「順便優化」放進同一張需求單。

## 1. 基本資料

| 欄位 | 填寫內容 |
|---|---|
| 需求編號 | change-request-v1 |
| 提出人／日期 |  |
| 基準版本 | blueprint-safe-v1.json |
| 變更目的（一句話） |  |

## 2. 允許的變更

| JSON 路徑 | 修改前 | 修改後 | 為什麼要改 |
|---|---|---|---|
| `modules[1].input` | `feedback_text` | `needs_review` | Filter 應讀取 Gemini 的審核欄位 |
| `modules[1].condition.value` | `"false"` | `false` | 契約要求布林值，不把文字當布林值 |

## 3. 不變條件

- [ ] 不新增或刪除模組。
- [ ] 不改 Gemini 的輸入、輸出欄位或提示詞。
- [ ] 不改 Google Docs 的欄位與版型。
- [ ] 不改任何連線、credential、token 或 placeholder。
- [ ] 不把整份 JSON 重排成無法比較的新版。

## 4. 驗收條件

1. `needs_review=false` 只通往 Google Docs。
2. `needs_review=true` 停在 `manual_review`，不建立文件。
3. `needs_review="false"` 被標記為型別錯誤，不得進入下游。
4. 每一項變更都有 diff、理由、測試與還原方式。

## 5. 風險與需人工確認

若無法確認欄位型別、路徑或實際執行結果，填寫「需人工確認」，不要請 LLM 猜測。
