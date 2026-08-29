# CH1-6 變體測試矩陣

預期結果是驗收標準，不是執行證據；先在每列填寫執行模式 `MAKE` 或 `SIMULATED`，再依模式填寫結果。`MAKE` 才能填實際執行 ID、Docs URL 或平台錯誤；`SIMULATED` 只能填固定輸出、預期路由與 `{{simulated_document_url}}`，並寫「尚未在平台驗證」。

| 案例 | 執行模式 | 變體輸入 | 預期結果 | 必須觀察 | MAKE 實際結果／SIMULATED 預期結果 | 證據位置 | 狀態 |
|---|---|---|---|---|---|---|---|
| A：成功 | `MAKE`／`SIMULATED` | 三筆合法資料；`needs_review=false` | 建立一份摘要 Docs | 筆數、期間、文件 URL 或 placeholder |  |  |  |
| B：需人工 | `MAKE`／`SIMULATED` | 其中一筆 `needs_review=true` | 整批／該筆停在人工出口，不建立不完整 Docs | 停止模組、負責人、重試位置 |  |  |  |
| C：缺值 | `MAKE`／`SIMULATED` | 一筆 `message_text` 空白或 Gmail body 空白 | 在來源檢查停止，不送出不完整資料 | 錯誤訊息、修正欄位、重試位置 |  |  |  |

## 可沿用與必重跑

| 既有證據 | 可沿用？ | 理由／新增證據 |
|---|---|---|
| CH1-3 單筆成功 |  |  |
| CH1-3 待人工出口 |  |  |
| CH1-5 型別錯誤 |  |  |

## 模式判定

- `MAKE`：有平台執行紀錄，證據可填執行 ID、實際 URL、停止位置或錯誤訊息。
- `SIMULATED`：只依固定資料與模組卡推演，證據欄填預期結果、`{{simulated_document_url}}` 或固定輸出檔名；不得寫成「已執行」。
