# Part 5 輸入契約

## 主路徑

本課先用人工 AI 判斷，再用 Make 或 n8n 做零代碼路由、通知與歸檔。學員不需要 API key、信用卡或付費方案才能開始。

## 表單欄位

| 欄位 | 必填 | 格式 | 用途 |
|---|---|---|---|
| `submitted_at` | 是 | `YYYY-MM-DD HH:mm` | 追蹤提交時間 |
| `name` | 是 | 文字 | 回覆對象 |
| `email` | 是 | Email | 通知或追問 |
| `subject` | 是 | 文字 | 初步分類線索 |
| `message` | 是 | 20–500 字 | AI 判斷與人工覆核 |
| `category` | 是 | `inquiry` / `complaint` / `partnership` / `other` | 路由欄位 |
| `summary` | 是 | 1–2 句 | 通知與歸檔 |
| `next_action` | 是 | 動詞開頭 | 下一步 |
| `review_status` | 是 | `待覆核` / `已覆核` | 防止未檢查資料直接外發 |

## 證據要求

完成一次流程至少保存：輸入列、AI 判斷紀錄、路由結果、通知或歸檔位置。外部工作區尚未實跑時，請標記 `NOT_RUN`，不要填寫 `PASS`。
