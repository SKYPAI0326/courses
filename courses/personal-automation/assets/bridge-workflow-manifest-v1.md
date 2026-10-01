# Bridge Workflow Manifest v1

這份清單把 Bridge-1 的兩個工作流資產分開標示，避免「規格」與「可匯入候選」被學員誤認為同一種檔案。

**Learner Pack root**：`courses/`。下表路徑皆從此根目錄解析；本清單位於 `courses/personal-automation/assets/`，不以目前文件所在資料夾作為路徑根。

| 平台 | 檔案 | 用途 | 狀態 | 匯入／執行限制 |
|---|---|---|---|---|
| Make | `../../make-ai-workflow/assets/CH1-3-contract-driven-v1.blueprint.spec.json` | 契約驅動流程的模組、欄位、分流與測試規格 | `DRAFT_NOT_IMPORTABLE` | Make Filter 的實際匯出結構尚未由工作區驗證；需在 Make UI 建立或匯出後更新版本 |
| n8n | `../../n8n/assets/workflows/m4-bridge-contract-fixture.json` | 無 credential 的 Webhook → 契約檢查 → A／B／C 分流練習 | `DRAFT_IMPORT_CANDIDATE` | 匯入後先用固定 POST payload 測試；回應標記為 `SIMULATED`，不呼叫 Gemini／Google API |

## n8n 固定測試 payload

將下列 JSON POST 到匯入後的 webhook。URL 需使用你自己的 n8n webhook URL，不要把下列路徑當成已公開網址。

### A｜需要人工確認

```json
{
  "case": "A",
  "customer_name": "林小姐",
  "rating": 2,
  "feedback": "物流延遲，客服回覆太慢"
}
```

預期回應：`route = manual_review`、`needs_review = true`、`artifact.status = stopped_before_delivery`。

### B｜通過文件路徑

```json
{
  "case": "B",
  "customer_name": "陳先生",
  "rating": 5,
  "feedback": "謝謝快速處理，問題已經解決"
}
```

預期回應：`route = google_docs`、`needs_review = false`、`artifact.status = simulated_created`。這不是 Google Docs 真實建立證據。

### C｜型別錯誤

```json
{
  "case": "C",
  "customer_name": "林小姐",
  "rating": 2,
  "feedback": "物流延遲，客服回覆太慢"
}
```

預期回應：`route = contract_error_stop`，原因是固定 fixture 的 `needs_review` 是文字 `"false"`，不得自動轉型。

## 人工驗證紀錄要求

匯入後請另外記錄：n8n 版本／Docker image、匯入時間、Webhook 執行時間、三個 payload 的 execution evidence、實際回應 JSON，以及錯誤時從哪個節點修復。沒有這些紀錄前，這份資產只能留在 `DRAFT_IMPORT_CANDIDATE`。
