# platform-map-v1｜Make × n8n 平台映射

這份表是轉譯檢查表，不是「一鍵搬家」對照表。每一列都要連回 `workflow-spec-v1`、`mapping-v1` 與 `test-cases-v1`，轉換後重新測試。

| 通用責任 | Make | n8n | 轉譯時要檢查 |
|---|---|---|---|
| 整條流程 | Scenario | Workflow | 啟動方式、保存版本、執行紀錄 |
| 一個工作步驟 | Module | Node | 輸入／輸出資料形狀與認證方式 |
| 單筆資料 | Bundle | Item | 是否一筆變多筆、是否需要拆分或合併 |
| 欄位引用 | Mapping | Expression | 欄位路徑、上一節點名稱、缺值行為 |
| 條件攔截 | Filter | IF | 通過、停止與人工出口是否相同 |
| 多路分配 | Router | Switch／分支 | 路由條件、未匹配資料與合併方式 |
| 逐筆處理 | Iterator | Loop Over Items／逐項節點 | 批次邊界、順序與重試行為 |
| 多筆合併 | Aggregator | Aggregate／資料合併 | 聚合欄位、空集合與輸出形狀 |
| 錯誤處理 | Error handler | Continue On Fail／錯誤路徑 | 是否停止、是否保留錯誤資料、誰接手 |
| 外部觸發 | Webhook／Watch | Webhook／Trigger | 公開網址、驗證、timeout 與重放風險 |

## 轉譯紀錄格式

每個要轉換的步驟填四欄：

1. **原平台**：節點／模組名稱與輸入欄位。
2. **目標平台**：對應節點與 Expression。
3. **不確定處**：資料形狀、認證、分支、等待或錯誤行為的差異。
4. **重跑測試**：從 `test-cases-v1` 指定成功、需人工、缺值至少各一案。

## 不可直接宣稱的結果

- 匯出 JSON 能被另一平台讀取，不代表連線、欄位、分支與錯誤處理已完成。
- n8n 本機執行不代表呼叫雲端 LLM 時資料沒有離開本機。
- 模擬輸出只能證明規則與映射，不等於 Make 或 n8n 的實際執行證據。
