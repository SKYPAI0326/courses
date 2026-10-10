# 輸入與紀錄表
同一試算表建立Source、ReviewedQueue、ProcessingLog、Drafts。
Source與ReviewedQueue第一列表頭固定九欄：submitted_at,name,email,subject,message,category,summary,next_action,review_status。
Source保存原文；AI建議由人覆核。ReviewedQueue只追加已覆核完整新列，中途不可空白；更新Source舊列不觸發Watch New Rows。
CH5-1 起始資料：從 [已覆核示例 CSV](part5-reviewed-queue.csv) 只複製第一筆「小林／詢問方案」的九欄，分別放入 Source、ReviewedQueue 第 2 列；先不放後三筆。每個值各佔一格，兩張表的 submitted_at 都應是 `2026-10-09T09:00`。ProcessingLog、Drafts 先只保留表頭。
完成第一次寫入後，對照練習只改 Source 第 2 列 message：「請問基礎方案月費」改為「請問基礎方案費用」。ReviewedQueue 不改，也不新增列；應不觸發。下一步才把示例第二筆「小安／交期問題」追加到 ReviewedQueue 第 3 列，測新增列觸發。
ProcessingLog：source_key,category,route,status,draft_status,error。Drafts：source_key,recipient,subject,body,status；recipient僅測試本人，status=未寄出。
去重鍵= submitted_at + | + 小寫且去前後空白的 email + | + 去前後空白的 subject。一次處理一列；此教學做法不保證並行時不重複。
