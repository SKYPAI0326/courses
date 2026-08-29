# CH1-3｜四張模組卡（離線跟做版）

> 這份模組卡是 Make 介面不可用時的替代材料。它保留本節要驗證的責任、輸入、輸出與停止條件；有 Make 權限時，依同樣欄位在 Scenario 中設定。

## 模組 1｜Google Sheets / Watch Rows

- **角色**：資料來源
- **輸入**：新增一列，欄位為 `customer_name`、`rating`、`feedback`
- **設定**：只讀取尚未處理的測試列
- **輸出**：一筆來源資料，交給 CH1-2 的輸入契約映射
- **通過條件**：`customer_name` 與 `feedback` 有文字，`rating` 是數字或空值
- **失敗出口**：沒有新列或必要欄位空白時，記錄原因，停在來源檢查，不送 Gemini

## 模組 2｜Gemini / Generate

- **角色**：處理
- **輸入**：`customer_identity`、`message_text`、`urgency_signal`
- **設定**：只回傳 `summary`、`reply_draft`、`needs_review` 三個欄位
- **輸出**：符合 `contract-output-v1` 的結果
- **通過條件**：兩個文字欄位不可空白，`needs_review` 必須是布林值
- **失敗出口**：欄位遺漏、空白或型別錯誤時，記錄輸出，停在 Gemini 檢查

## 模組 3｜Filter

- **角色**：控制
- **輸入**：Gemini 的 `needs_review`
- **設定**：只有 `needs_review = false` 通過
- **輸出**：通過路徑，或待人工確認的停止狀態
- **通過條件**：布林值 `false` 才能繼續
- **失敗出口**：`true` 或型別不明時，不建立 Docs，記錄待人工確認或型別錯誤

## 模組 4｜Google Docs / Create a Document

- **角色**：後續交付
- **輸入**：`summary`、`reply_draft`
- **設定**：文件標題包含測試識別，內容保留摘要與回覆草稿
- **輸出**：文件 URL 與可讀內容
- **通過條件**：URL 存在，文件內容與 Gemini 輸出一致
- **失敗出口**：URL 缺失或內容空白時，記錄權限／映射問題，暫停通知

## 最短路徑

```text
Sheets / Watch Rows
  → Gemini / Generate
  → Filter：needs_review = false
  → Docs / Create a Document
```

`needs_review=true` 沒有連到下一個模組；它是本節刻意保留的「待人工確認」出口。
