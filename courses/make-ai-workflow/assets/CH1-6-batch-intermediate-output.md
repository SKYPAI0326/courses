# CH1-6 批次變體中間輸出與預期結果

本檔是離線演練用的完整中間結果。`預期`不是 Make 實際執行證據；若在平台執行，請另填真實時間、執行 ID 與文件 URL。

## 逐筆檢查結果

| record_id | message_text | needs_review | Iterator 結果 | Gemini 輸出摘要 | 後續判斷 |
|---|---|---:|---|---|---|
| R01 | 有內容 | false | 通過 | 已整理物流延遲回饋 | 可進入聚合 |
| R02 | 有內容 | false | 通過 | 問題已解決 | 可進入聚合 |
| R03 | 有內容 | true | 通過 | 退款金額需人工確認 | 聚合後整批停在人工出口 |

## 聚合輸入

```json
{
  "period": "2026-W01",
  "record_count": 3,
  "items": [
    {"record_id":"R01","needs_review":false,"summary":"已整理物流延遲回饋"},
    {"record_id":"R02","needs_review":false,"summary":"問題已解決"},
    {"record_id":"R03","needs_review":true,"summary":"退款金額需人工確認"}
  ]
}
```

## 三條路徑

| 案例 | 聚合判斷 | Filter | Docs | 模擬證據 |
|---|---|---|---|---|
| A：三筆皆合格（將 R03 的旗標改為 false 後測試） | 全部 false | 通過 | 建立週摘要，URL `{{simulated_document_url}}` | `SIMULATED` |
| B：原始三筆 | 含一筆 true | 停在 manual_review | 不建立 | 停止位置與負責人待填 |
| C：一筆缺值（將 R02 的 message_text 清空後測試） | Iterator 不通過 | 不進下游 | 不建立 | 記錄錯誤欄位與重試位置 |

## 接手者核對

- 每個摘要都能回到 `record_id`。
- 任一 true 或缺值不會產生不完整文件。
- 批次規則是本變體的唯一主要變因；輸出契約與人工出口沿用原版。
