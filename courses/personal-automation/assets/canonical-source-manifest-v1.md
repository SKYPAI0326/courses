# Canonical Source Manifest v1｜Make × n8n

**狀態**：教學主線已裁決；平台匯出與跨平台實跑仍待驗證
**Learner Pack root**：`courses/`

## 來源版本

| source_id | 顯示名稱 | 路徑（相對 Learner Pack root） | 用途 | 可否作跨平台主線 |
|---|---|---|---|---|
| `MAKE-REFERENCE-4MODULE-V1` | 原始四模組參考版 | `make-ai-workflow/assets/CH1-1-reference-4module.sanitized.blueprint.json` | 觀察 Sheets → Gemini → Docs → Email 的既有資料流與位置鍵 | 否，只作讀圖參考 |
| `MAKE-CONTRACT-V1` | 契約驅動基準版 | `make-ai-workflow/assets/CH1-3-contract-driven-v1.blueprint.spec.json` | 定義共同欄位、結構化輸出、Filter 與 A／B／C 測試 | 是；目前為規格草稿 |
| `N8N-BRIDGE-FIXTURE-V1` | n8n Bridge 固定測試候選 | `n8n/assets/workflows/m4-bridge-contract-fixture.json` | 在沒有 credential 的情況下練習契約檢查與分流 | 僅可作匯入候選；尚未升級為實跑基準 |
| `N8N-LOCAL-BASELINE-V1` | n8n 本機檔案基線 | `n8n/lessons/m3-1-watch.html`、`n8n/lessons/m3-2-rename.html` | Manual Trigger + Read/Write Files from Disk 的可重跑基線 | 是；頁面已改為主線，JSON 尚待補齊 |

## 版本使用規則

1. 完整 PDF 的跨平台主線只能使用 `MAKE-CONTRACT-V1` 與其明確標記的 n8n 轉譯內容。
2. `MAKE-REFERENCE-4MODULE-V1` 出現時，標題必須寫「原始四模組參考版」，並說明它沒有 Filter、`needs_review` 與結構化輸出。
3. 規格草稿、匯入候選、固定輸出與平台執行紀錄要分開呈現；不能用一種證據替另一種背書。
4. 每次跨平台轉譯都要保留來源版本、目標版本、差異、重測案例與證據模式。
5. Make UI 匯出、n8n 匯入與 A／B／C 實跑完成前，狀態維持 `DRAFT`、`DRAFT_IMPORT_CANDIDATE` 或 `NOT_RUN`。

## Canonical teaching contract v1

共同欄位固定為：

| 欄位 | 型別 | 來源示例 | 限制 |
|---|---|---|---|
| `customer_identity` | string | Sheets `customer_name` → `林小姐` | 不可空白 |
| `message_text` | string | Sheets `feedback` → `物流延遲，客服回覆太慢` | 不可空白 |
| `urgency_signal` | number | Sheets `rating` → `2` | 本案例代理訊號，不等於正式緊急度 |

共同輸出固定為：

| 欄位 | 型別 | 控制用途 |
|---|---|---|
| `summary` | string | 文件／人工判斷的摘要 |
| `reply_draft` | string | 後續回覆草稿 |
| `needs_review` | boolean | `false` 才能進交付；`true` 必須停在人工出口 |

`owner_email` 暫列保留欄位。原始資料沒有收件人時，不得虛構 Email 或把 Email 當作核心完成條件。
