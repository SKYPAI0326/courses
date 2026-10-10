# U07｜一筆原文到可路由資料
先讀 CH5-3。這是方法示範；其他案例由你自行判斷。

原列：U07，SRC-U07，2026-10-01 09:30，吳立，learner07@example.com，服務時間，「請問你們平日幾點營業？」。

| 九欄欄名 | 候選值 | 為什麼填這個值 |
|---|---|---|
| submitted_at | 2026-10-01 09:30 | 照抄來源，不用今天時間 |
| name | 吳立 | 來源姓名 |
| email | learner07@example.com | 來源測試地址 |
| subject | 服務時間 | 來源主旨，不改成摘要 |
| message | 請問你們平日幾點營業？ | 保留原文 |
| category | inquiry | 詢問資訊，未反映服務不滿 |
| summary | 詢問平日營業時間 | 不替來源填營業時段 |
| next_action | 查正式營業時間後擬未寄出草稿 | 待查工作，不承諾具體時間 |
| review_status | 待覆核 | 尚未由人核對 |

case_id 與 source_id 存在旁邊的追溯表，不塞進九欄，亦不拿 source_id 代替去重鍵。

```csv
submitted_at,name,email,subject,message,category,summary,next_action,review_status
2026-10-01 09:30,吳立,learner07@example.com,服務時間,請問你們平日幾點營業？,inquiry,詢問平日營業時間,查正式營業時間後擬未寄出草稿,待覆核
```

人工核對五個來源值、分類理由、摘要與下一步後，再查 ProcessingLog 是否已有來源鍵：
`2026-10-01 09:30|learner07@example.com|服務時間`。

未重複、九欄完整、分類與下一步可接受時，由人把最後一欄改為「已覆核」，其餘八欄不改，再追加 ReviewedQueue。已覆核代表准許依分類路由，不代表已查到營業時間或可寄出正式答覆。Drafts 可先保存「營業時間待人工查核，未寄出」；不要把未知填成事實。

退回示範：U05 缺姓名及 email。即使知道是退款問題，仍記「退回補來源欄」，只留 Source 和補件原因；不使用「未知@example.com」湊九欄，也不追加佇列。

核對紀錄範例：`U07／分類與九欄已核對／同鍵未找到／准許路由／營業時間仍待查／覆核者填自己的名字及日期`。這是示範格式，不能代替你實際查表。
