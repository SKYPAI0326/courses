# 輸入與紀錄表
同一試算表建立Source、ReviewedQueue、ProcessingLog、Drafts。
Source與ReviewedQueue第一列表頭固定九欄：submitted_at,name,email,subject,message,category,summary,next_action,review_status。
Source保存原文；AI建議由人覆核。ReviewedQueue只追加已覆核完整新列，中途不可空白；更新Source舊列不觸發Watch New Rows。
ProcessingLog：source_key,category,route,status,draft_status,error。Drafts：source_key,recipient,subject,body,status；recipient僅測試本人，status=未寄出。
去重鍵= submitted_at + | + 小寫且去前後空白的 email + | + 去前後空白的 subject。一次處理一列；此教學做法不保證並行時不重複。
