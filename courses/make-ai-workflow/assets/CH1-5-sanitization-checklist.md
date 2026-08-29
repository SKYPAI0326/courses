# CH1-5 去敏檢查表

使用 `CH1-5-sanitized-blueprint.fixture.json` 或教師提供的去敏副本。這張表的目的，是在內容交給 LLM 前先阻止秘密與個資外流。

## 逐項搜尋

| 搜尋字樣／類型 | 找到時的處理 | 檢查結果 |
|---|---|---|
| `token`、`secret`、`password`、`api_key` | 以 `{{removed_secret}}` 取代 | [ ] |
| `credential`、OAuth 連線值 | 保留欄位名，值改為 `{{removed_credential}}` | [ ] |
| 真實 Email、姓名、電話、地址 | 改成 `{{sample_email}}` 等範例值 | [ ] |
| Drive／Docs／Sheet 固定 ID | 改成 `{{removed_file_id}}` | [ ] |
| 內部網址、Webhook、公司代號 | 改成 `{{removed_endpoint}}` | [ ] |

## 結構確認

- [ ] 模組順序、模組名稱與欄位名稱仍可讀。
- [ ] Filter 的舊條件仍保留，能與修改後比較。
- [ ] 輸入、輸出與路由仍可用固定值重現。
- [ ] JSON 可解析，沒有多餘逗號或被截斷的字串。

## 放行規則

只有「所有敏感值已替換」且「結構仍可重現」兩項都勾選，才可將副本貼給 LLM。未確定的值先標記 `{{needs_human_check}}`，不要猜。
