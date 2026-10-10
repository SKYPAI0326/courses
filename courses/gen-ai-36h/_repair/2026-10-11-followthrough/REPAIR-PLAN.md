# 修復計畫
scope: content-change；基準 b39d1cc3；使用者已要求執行 A01–A05 修改，先前已授權 push main。

1. A01：以現有 Blueprint 設定為準，在 part5-rebuild-guide 補九欄 Filter 的左值／運算子／右值、AND 組合、email 與分類樣式、陣列查重三欄、輸入／預期例。依官方 Filter／Router／Array 文件核對。Blueprint 行為不改。
2. A02：在 part5-stage-handoff 補 S1→S2 明確插入 Router、保留原寫入作 inquiry 分支、另建三路；S2→S3 插入查重並核對 Filter 位置。CH5-2 連到指定步驟。
3. A03：CH5-1 與表格配置明列 Source 第2列與 ReviewedQueue 第2列的示例、修改欄位與觀察。
4. A04：CH2-3 將必填人工修正改為核對結果；無誤可記一致，音訊沒有不確定詞同理。
5. A05：worked-example 第一段統一為 CH7-2 基準初稿保存後開啟。
6. 新增重建指南 HTML；更新引用它的 CH5-1、CH5-4、階段頁及素材總入口。僅轉製四份受影響講義並同步同課 _lessons。

允許文字變更：上述具體替換與補充；不刪既有教學成果、案例、測試或導覽。所有新增完整正文保存在對應來源，HTML 保真轉製，wrapper/auth/nav 不變。

驗收：來源與 Blueprint 條件等價核對；S1/S2/S3 文字狀態追蹤；逐段保真、結構、lint、素材連結；代表頁 1440／390／430 瀏覽器與分頁／保存捲動驗證。真人及目標 Make 帳號仍待驗；不把本機條件模擬當平台 PASS。

備份：兩個工作副本的 _backup/2026-10-11-followthrough-pre-repair/。還原脚本需 bash -n。

必要工具修正：render-lessons.py 的素材路徑檢查需分離 #anchor，並核對 HTML 的 id，讓講義能直達具體設定；工具已先備份。
