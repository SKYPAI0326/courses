# BRIDGE-1｜Make ↔ n8n 跨平台資料契約 v1

這份文件是 Make 與 n8n 課程共用的銜接規格。它讓接手者先看懂資料的任務，再決定欄位要原樣傳遞或建立轉換。文件只使用去敏固定資料；`MAKE`、`SIMULATED`、`NOT_RUN` 代表不同證據狀態，不能互相替代。

## 1. 先分清楚兩個課程的任務

Make 課程的基準案例處理「客戶回饋」：

| 欄位 | 意義 | 型別 | 必填 |
|---|---|---|---|
| `customer_identity` | 回饋來自誰 | 文字 | 是 |
| `message_text` | 回饋內容 | 文字 | 是 |
| `urgency_signal` | 額外的緊急程度線索 | 數字或 `null` | 否 |
| `owner_email` | 內部負責人收件地址 | Email 文字 | 是 |

n8n Module 4 的基準案例處理「文件申請」：

| 欄位 | 意義 | 型別 | 必填 |
|---|---|---|---|
| `applicant` | 文件申請人 | 文字 | 是 |
| `document_type` | 要產生的文件類型 | 文字，例：報告／企劃／合約 | 是 |
| `due_date` | 文件期限 | `YYYY-MM-DD` 文字 | 是 |

兩組欄位描述不同工作。`customer_identity` 只有在「申請人」與「回饋者」確實是同一角色時，才可由人員確認後映射到 `applicant`；課程範例預設保留原欄位，避免自動猜測。

## 2. 共用封裝格式

跨平台傳送時，使用一個外層封裝，讓 n8n 能先判斷任務，再讀取對應的 `data`：

資料會依序經過「送出的根層 JSON → n8n Webhook 看到的 `$json.body` → Normalize 成功後供下游使用的 `$json.bridge_data`」三層；本文件的範例先看根層，M4-1 操作時再依這三層定位欄位。

```json
{
  "request_id": "demo-feedback-001",
  "source_platform": "make",
  "task_type": "customer_feedback",
  "evidence_mode": "SIMULATED",
  "data": {
    "customer_identity": "林小姐",
    "message_text": "物流延遲，客服回覆太慢",
    "urgency_signal": 2,
    "owner_email": "owner@example.invalid"
  }
}
```

外層欄位規則：

| 欄位 | 規則 | 失敗處理 |
|---|---|---|
| `request_id` | 每筆請求唯一，文字 | 缺值時停在輸入檢查 |
| `source_platform` | `make` 或 `n8n` | 未列出的值標記契約錯誤 |
| `task_type` | `customer_feedback` 或 `document_request` | 先停下，禁止猜測欄位 |
| `evidence_mode` | `MAKE`、`SIMULATED` 或 `NOT_RUN` | 沿用原證據狀態 |
| `data` | 依 `task_type` 使用相應欄位 | 由轉換節點檢查必填與型別 |

## 3. 範例 A：Make 回饋原樣交給 n8n

當 n8n 只需要保存回饋、產生本機 Markdown 或進行人工分流，保留 Make 的四個欄位。n8n 讀取的位置是 `data.customer_identity`、`data.message_text`、`data.urgency_signal`、`data.owner_email`。

```json
{
  "request_id": "demo-feedback-001",
  "source_platform": "make",
  "task_type": "customer_feedback",
  "evidence_mode": "SIMULATED",
  "data": {
    "customer_identity": "林小姐",
    "message_text": "物流延遲，客服回覆太慢",
    "urgency_signal": 2,
    "owner_email": "owner@example.invalid"
  }
}
```

此路徑不需要把欄位改名。若要產生 n8n 可讀的固定輸出，結果可放在 `result`：

```json
{
  "request_id": "demo-feedback-001",
  "task_type": "customer_feedback",
  "route": "manual_review",
  "result": {
    "summary": "物流延遲且客服回覆時間過長",
    "needs_review": true
  },
  "evidence_mode": "SIMULATED"
}
```

## 4. 範例 B：Make 只負責傳送文件申請

當 n8n 要執行 Module 4 的文件申請流程，Make 只負責接收來源或轉送資料；`data` 改用 n8n 的三個欄位：

```json
{
  "request_id": "demo-document-001",
  "source_platform": "make",
  "task_type": "document_request",
  "evidence_mode": "SIMULATED",
  "data": {
    "applicant": "王小明",
    "document_type": "報告",
    "due_date": "2026-09-30"
  }
}
```

Make 的 Webhook、HTTP Request 或表單模組只映射這三個欄位。n8n Webhook 收到後，先讀 `body.task_type`，再讀 `body.data.document_type` 進行 Switch。這筆資料不應填入 `customer_identity` 或 `message_text`。

## 5. 跟著做：決定是否需要轉換

1. **確認任務**：在交接表寫 `customer_feedback` 或 `document_request`，只能選一個。
2. **列出資料**：從 Make 執行紀錄或固定測試檔找出 `request_id`、來源平台與 `data`。
3. **比對欄位**：逐列檢查目標 n8n 節點需要的欄位、型別與缺值規則。
4. **選擇路徑**：欄位語意相同就原樣傳遞；語意不同就新增一個「Normalize／Transform」節點，並留下前後對照。
5. **測試三種情況**：一筆合格資料、一筆缺少必填欄位、一筆任務型別不符。每筆記錄輸出、停止位置與證據模式。

### 轉換前後對照範例

以下只示範人員已確認「客戶回饋者就是文件申請人」的特殊情況；轉換決定要寫入交接紀錄：

```json
{
  "request_id": "demo-convert-001",
  "task_type": "document_request",
  "evidence_mode": "SIMULATED",
  "data": {
    "applicant": "林小姐",
    "document_type": "報告",
    "due_date": "2026-09-30"
  },
  "transform_note": "人工確認 customer_identity 可代表 applicant；message_text 未轉入 document_type。"
}
```

如果無法說明轉換理由，保留原欄位並停在人工確認出口。這個停站保護下游文件與通知，讓接手者知道下一步要找誰確認。

## 6. 驗收表

| 檢查項目 | 通過條件 | 證據欄位 |
|---|---|---|
| 任務型別 | 只有一個 `task_type`，與下游流程一致 | `task_type`、流程截圖或 log |
| 欄位語意 | 每個欄位都有來源、型別與用途 | 映射表 |
| 缺值處理 | 必填缺值會停止，選填 `urgency_signal` 可為 `null` | 停止紀錄或固定預期 |
| 轉換責任 | 改名或合併欄位都有人工決定與備註 | `transform_note` |
| 證據狀態 | `MAKE` 有平台執行證據；`SIMULATED` 有固定輸出；`NOT_RUN` 有待驗證項目 | 執行紀錄 |
| 安全 | JSON 沒有 credential、token、真實帳號或個資 | 去敏檢查表 |

## 7. 交接時要附上的檔案

- 這份 `BRIDGE-1-make-n8n-contract-v1.md`
- 轉換前 JSON 與轉換後 JSON（檔名加上 `before`／`after`）
- 欄位映射與 `transform_note`
- 三筆測試紀錄：成功、缺值、任務型別不符
- Make／n8n 各自的證據狀態與尚待真人驗證項目
- 還原方式：移除 Normalize／Transform 節點，回到原始契約版本
