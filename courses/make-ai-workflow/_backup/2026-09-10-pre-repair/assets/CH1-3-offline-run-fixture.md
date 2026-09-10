# CH1-3 離線模擬執行包

本檔提供沒有 Make 連線時的「模擬證據」。它用固定輸入、固定輸出與路由判斷重現教學邏輯，但不會建立真實 Scenario、Filter 執行紀錄或 Google Docs URL；課堂紀錄請標示 `SIMULATED`。

## 模擬流程

```text
來源資料 → 契約欄位 → Gemini 固定輸出 → Filter 判斷 → Docs 預期結果
```

## 案例 A：需要人工確認

| 階段 | 固定輸入／輸出 | 模擬結果 |
|---|---|---|
| Sheets | 林小姐／評分 2／物流延遲 | 讀到一筆來源資料 |
| Gemini | `summary`、`reply_draft`、`needs_review=true` | 三欄且型別正確 |
| Filter | 比較 `needs_review` 與 `false` | 不通過，進待人工確認出口 |
| Docs | 不執行 | 不建立文件（無 URL） |

## 案例 B：一般回饋

| 階段 | 固定輸入／輸出 | 模擬結果 |
|---|---|---|
| Sheets | 陳先生／評分 5／問題已解決 | 讀到一筆來源資料 |
| Gemini | `summary`、`reply_draft`、`needs_review=false` | 三欄且型別正確 |
| Filter | 比較 `needs_review` 與 `false` | 通過 |
| Docs | 使用 summary 與 reply_draft | 模擬建立文件，URL 記為 `{{simulated_document_url}}` |

## 案例 C：型別錯誤

| 階段 | 固定輸入／輸出 | 模擬結果 |
|---|---|---|
| Gemini | `needs_review="false"`（文字） | 輸出契約不合格 |
| Filter | 不進行文字轉布林 | 停止，標記型別錯誤 |
| Docs | 不執行 | 不建立文件 |

## 離線紀錄規則

- 執行時間填寫實際模擬時間，執行模式填 `SIMULATED`。
- 文件 URL 只能使用 placeholder，不得填寫不存在的真實連結。
- `scenario-v1-offline-map` 是流程判斷成果；只有在 Make 工作區實跑後，才能改稱 `scenario-v1` 可執行版本。
- 要進入 CH1-4 前，交付「流程圖、三案例預期路由、契約映射與限制」，不提交虛構的 Make 執行畫面。
