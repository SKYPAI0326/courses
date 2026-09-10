# CH1-5 固定測試案例

用同一份修改後 fixture 依序測試。先填執行模式 `MAKE` 或 `SIMULATED`。`MAKE` 才能填平台執行證據；`SIMULATED` 只填固定輸出與預期路由，並標示「尚未在平台驗證」。下表的預期是驗收標準，不是替學員代填的執行證據。

| 編號 | 執行模式 | 輸入 `needs_review` | 預期路由 | 預期下游 | MAKE 實際結果／SIMULATED 預期結果 | 證據位置 | 決策 |
|---|---|---|---|---|---|---|---|
| A | `MAKE`／`SIMULATED` | `false`（布林值） | Google Docs | 建立文件 |  |  |  |
| B | `MAKE`／`SIMULATED` | `true`（布林值） | `manual_review` | 不建立文件 |  |  |  |
| C | `MAKE`／`SIMULATED` | `"false"`（文字） | `type_error` | 不執行下游 |  |  |  |

## 測試紀錄提示

每一列至少記錄：執行時間（或模擬日期）、使用版本、停止位置或文件 URL placeholder、錯誤訊息（如有）、操作者。`MAKE` 模式記錄執行 ID、實際 URL 或平台錯誤；`SIMULATED` 模式記錄固定輸出、預期路由與 `{{simulated_document_url}}`，不得填虛構 URL。若 A、B、C 任一結果不符合預期，將 diff 狀態標為「退回」，保留安全副本後再建立下一張變更需求。
