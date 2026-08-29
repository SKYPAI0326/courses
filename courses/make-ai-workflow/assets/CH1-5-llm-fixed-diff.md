# CH1-5 固定 diff 範例（無 LLM 帳號備援）

本檔模擬一次合格的 LLM 回答，讓沒有 LLM 帳號或網路不穩的班級仍能練習審查。它不是 Make Blueprint，也不是執行成功的證據。

## 變更摘要

只修改兩個允許路徑：

| 路徑 | 修改前 | 修改後 | 理由 |
|---|---|---|---|
| `modules[1].input` | `feedback_text` | `needs_review` | Filter 必須讀取 Gemini 輸出的審核欄位 |
| `modules[1].condition.value` | `"false"` | `false` | 以布林值比較，避免文字型別誤放行 |

## 未修改

來源模組、Gemini prompt、Gemini 輸出契約、Google Docs 欄位、模組數量與所有連線 placeholder 均維持不變。

## 測試與還原

| 輸入 | 預期 | 固定回答中的判斷 |
|---|---|---|
| `false` | 進 Google Docs | 通過 |
| `true` | 停在 `manual_review` | 通過 |
| `"false"` | 型別錯誤、不下游 | 退回／需修正輸出契約 |

若實際結果與表格不同，狀態應為「退回」；保留 `blueprint-safe-v1.json`，不要直接覆寫未驗證版本。
