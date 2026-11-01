Part 5 · 人工覆核與 Make 自動化

# 條件、分流與執行紀錄

把已核對的訊息送到正確分支，也確認不合格資料會停在入口。

本節完成物：四路紀錄與兩筆阻擋證據

這一節的練習順序

01
同樣是新訊息，負責處理的人可能不同

02
先檢查是否可處理，再依分類分成四路

03
一次加一筆，查它實際走到哪裡

04
用錯誤資料確認入口真的會擋下來

05
其他工具留到主流程熟悉之後再比較

(01) · 學習與實作
## 同樣是新訊息，負責處理的人可能不同

上一節讓每筆新資料留下紀錄，現在要依分類交給不同角色。Make 的 Filter 是資料必須通過的條件，Router 則將資料分到不同路線。沿用原試算表，先看[九欄資料規格](../assets/part5-input-contract.md)和[七個測試案例](../assets/part5-test-cases.csv)，確認每種輸入預期去哪裡。

四個分類值固定為 inquiry（詢問）送業務、complaint（抱怨）送客服、partnership（合作）送合作窗口、other（其他）送待處理。顯示名稱可以幫你理解，但條件中要用這些固定值；填「詢價」並不會自動等於 inquiry。

(02) · 學習與實作
## 先檢查是否可處理，再依分類分成四路

先保存上一節成功版本，再按[從單一路線改成四路的指南](../assets/part5-stage-handoff.html#s1-to-s2)，在 Watch New Rows 後插入 Router。原 Add a Row 移到 inquiry 分支，另外加三個分支；它不能還留在 Router 前，否則資料分流之前就先寫入了。四路都寫 ProcessingLog，保留 source_key、category、route、status、draft_status。

用 T01、T02 先理解結果：T01 的 inquiry 應寫業務、已記錄、待建立；T02 的 complaint 應寫客服、已記錄、不需要。前者之後要產生草稿，後者交由客服人工處理，因此兩路的草稿狀態不同。本節還不建草稿。

按[Filter 逐欄設定表](../assets/part5-rebuild-guide.html#review-filter)，在 Watch New Rows 與 Router 之間檢查人工核准及資料完整性。九個條件用 AND，表示都成立才放行；四個合法分類放在同一個 Matches pattern 條件，直接使用表內樣式，不另外串四個 OR。
再依指南設定各分支的 category 等於條件。先用 T01 查通過和分流，再試待覆核及 unknown；資料被入口擋下時，ProcessingLog 也不應新增。

完成後應是[四路各有紀錄的狀態](../assets/part5-stage-handoff.html)，指南稱為 S2。詢問和合作記「待建立」，但 Drafts 空白是正常的，因為下一節才接草稿與防重複處理。先把這個完成位置記下，避免把還沒建的功能當成故障。

(03) · 學習與實作
## 一次加一筆，查它實際走到哪裡

T01 到 T04 一次只追加一列 ReviewedQueue，每次 Run once 後打開執行中的資料（bundle），查輸入分類、實際路線和結果列。四筆應分別到業務、客服、合作、待處理。綠勾只表示模組有執行，分類對不對仍要看值。

完全沒走路線時，查 category 的大小寫和多餘空白；同時走兩路時，查分支條件是否重疊。修好後用新的測試來源鍵再試，舊結果註明當時錯誤，留下查錯經過。

(04) · 學習與實作
## 用錯誤資料確認入口真的會擋下來

追加一筆 review_status 為待覆核的資料，應在入口被擋，ProcessingLog 和 Drafts 都不新增。再用 category 為 unknown 測一次，預期相同。如果仍被放行，就修 Filter 後重測；這項測試是在確認，即使有人填錯，流程也能停住。

保存四路結果與兩筆阻擋案例。下一節會先讓 AI 協助分類、由人確認，再把合格資料接到這裡；固定九欄就是兩段工作之間交接資料的格式。

(05) · 學習與實作
## 其他工具留到主流程熟悉之後再比較

選做比較時，n8n 也能接觸發、分流和錯誤紀錄，但要有可用環境與維護能力。本課不要求安裝已停止維護的 Desktop 版，也不使用已終止的 LINE Notify。相關狀態可查[n8n 公告](https://community.n8n.io/t/sunsetting-self-hosted-team-plan-desktop-version/25830)和[LINE Notify 公告](https://notify-bot.line.me/)；先把目前這套流程操作清楚即可。

[←
