# CH1-1 四模組 Blueprint 匯入對照

這份檔案說明 `CH1-1-reference-4module.sanitized.blueprint.json` 的去敏欄位。它保留已驗證的 4 個模組與 Make Blueprint 結構；匯入到自己的工作區後，必須重新綁定連線與目的地。沒有工作區權限時，直接使用本頁的表格與測試資料，不把匯入當成本節的必要條件。

| 模組 ID | 模組 | 需要重新綁定 | 本節要觀察的輸入／輸出 |
|---:|---|---|---|
| 1 | `google-sheets:watchRows` | Google 連線、試算表、工作表 | 輸入是一列資料；匯出 Bundle 以位置鍵 `0`、`1`、`2`、`3` 對應時間、姓名、評分、回饋 |
| 2 | `gemini-ai:createACompletionGeminiPro` | Gemini 連線、模型可用性 | 將 `{{1.\`1\`}}`、`{{1.\`2\`}}`、`{{1.\`3\`}}` 放入 Prompt；輸出是單一文字欄位 `result` |
| 7 | `google-docs:createADocument` | Google 連線、目的資料夾 | 文件名稱使用 `客服回饋：{{1.\`0\`}}-{{1.\`1\`}}`（時間＋姓名）；`{{2.result}}` 作為文件內容；輸出文件名稱與 URL／ID |
| 8 | `google-email:sendAnEmail` | Gmail 連線、收件人 | 主旨使用 `{{7.name}}`，內文使用 `{{2.result}}`；輸出寄信狀態 |

## 去敏欄位

- `[REPLACE_*]` 不是可直接寄送的帳號或 ID。匯入後依工作區畫面重新選取連線、試算表、資料夾與收件人。
- 不要把原始 Blueprint 中的連線識別、固定收件人或資料夾 ID 複製回課程資產。
- 若 Make 拒絕含 placeholder 的匯入，改用模組順序表逐一建立 4 個模組；這是連線重綁問題，不是學員資料映射錯誤。

## 不在本節的內容

本 4 模組基準沒有 Filter、Router、ParseJSON 或 `needs_review`。需要分流或結構化輸出時，留到後續單元另行設計，不在 CH1-1 先假設不存在的欄位。
