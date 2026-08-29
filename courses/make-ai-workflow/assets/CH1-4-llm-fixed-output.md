# CH1-4｜LLM 固定輸出（無帳號替代版）

> 沒有可用的 LLM 介面時，將以下內容視為已取得的回答，直接練習填入 `workflow-spec-v1` 與 `review-checklist-v1`。它不是 Make Blueprint。

## 1. 模組清單

| 順序 | 模組角色 | 模組建議 | 輸入 | 輸出 | 驗證方式 | 疑點／限制 |
|---:|---|---|---|---|---|---|
| 1 | 資料來源 | Sheets / Watch Rows（可替換 Gmail） | 來源欄位 | `customer_identity`、`message_text`、`urgency_signal` | 必填欄位與文字內容檢查 | 連線設定需由人提供 |
| 2 | 處理 | Gemini / Generate | 三個輸入契約欄位 | `summary`、`reply_draft`、`needs_review` | 欄位存在與型別檢查 | 不接受未定義欄位 |
| 3 | 控制 | Filter | `needs_review` | `false` 通過；`true` 待人工 | 用兩個測試值驗證 | 人工確認模組未實作 |
| 4 | 後續動作 | Google Docs / Create a Document | `summary`、`reply_draft` | 文件 URL | 文件內容與 URL | 需檢查權限 |

## 2. 欄位映射

| 原始欄位 | 契約欄位 | 型別 | 下游用途 | 缺值／錯誤處理 |
|---|---|---|---|---|
| `customer_name`／`sender` | `customer_identity` | 文字 | Gemini | 空值停止來源 |
| `feedback`／`subject + body` | `message_text` | 文字 | Gemini | 合併後空白停止 |
| `rating` | `urgency_signal` | 數字或空值 | Gemini | Gmail 無此欄時不阻斷 |
| 固定設定 | `owner_email` | Email 文字 | 內部通知 | 不使用 `sender` 取代 |

## 3. 控制與失敗出口

| 觸發條件 | 控制規則 | 通過去向 | 停止位置 | 負責人 |
|---|---|---|---|---|
| `needs_review=false` | 允許繼續 | Google Docs | — | 流程負責人 |
| `needs_review=true` | 不允許繼續 | 待人工確認 | Filter | 內容負責人 |
| `needs_review="true"` | 型別錯誤，不猜測 | — | Gemini／Filter 檢查 | 流程負責人 |

## 4. 測試案例

| 案例 | 變更的輸入 | 預期結果 | 驗證證據 |
|---|---|---|---|
| A：一般回饋 | `needs_review=false` | 通過 Filter，建立 Docs | 文件 URL 與兩個文字欄位 |
| B：需人工確認 | `needs_review=true` | 停在人工出口，不建立 Docs | Filter 停止紀錄 |
| C：型別錯誤 | `needs_review="true"` | 不猜測，標記型別錯誤 | 錯誤紀錄與修正責任 |
