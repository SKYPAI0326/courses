# CH1-6 Bridge 工作表：Make → n8n

這張工作表用來把 Make 變體交給 n8n。先選一種任務，再填對應欄位；兩種任務的資料不可混用。

## 1. 任務選擇

| 欄位 | 填寫內容 |
|---|---|
| `task_type`（只能選一個） | `document_request`／`customer_feedback` |
| 下游要完成的工作 |  |
| 目標 n8n 頁面 | `document_request` → M4-1；`customer_feedback` → 暫存／摘要流程，需教師確認 |
| 執行模式 | `MAKE`／`SIMULATED`／`NOT_RUN` |

## 2. 外層封裝

| 欄位 | 範例值 | 我的值 |
|---|---|---|
| `request_id` | `document-demo-001` |  |
| `source_platform` | `make` |  |
| `task_type` | `document_request` |  |
| `evidence_mode` | `SIMULATED` |  |
| `data` | 依下方任務欄位填入 |  |

## 3. 依任務填入 data

### A. `document_request`（本課與 n8n M4-1 的跟做主線）

```json
{
  "applicant": "王小明",
  "document_type": "報告",
  "due_date": "2026-09-30"
}
```

三個欄位都必填。缺一項就停在契約檢查，不建立空文件。

### B. `customer_feedback`（延伸辨識練習）

```json
{
  "customer_identity": "測試客戶 A",
  "message_text": "希望增加週末場次",
  "urgency_signal": null,
  "owner_email": "owner@example.test"
}
```

這組欄位供辨識、保存或摘要練習使用；目前 n8n M4-1 沒有文件分流路徑，不能直接套用 M4-1 的 `document_type` 規則。

## 4. 轉換與驗收

| 測試 | 輸入狀況 | 預期出口 | 實際證據／備註 |
|---|---|---|---|
| A | 完整且符合所選 `task_type` | 進入對應 n8n 路徑 |  |
| B | 缺少必填欄位 | 契約檢查停止，不建立文件或通知 |  |
| C | `task_type` 與下游頁面不符 | 停止並人工確認 |  |

完成前確認：`request_id` 可追蹤、`data` 欄位與任務型別一致、每筆測試都有 `MAKE`／`SIMULATED`／`NOT_RUN` 標記。根層 JSON 送出後，n8n Webhook 會包在 `$json.body`；Normalize 成功後才使用 `$json.bridge_data`。
