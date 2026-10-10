# 五項教學缺口修復結果

A01–A05 已完成教材修正；只處理完整課程審查的實證問題，未新增題數或強制找錯。

- Make 設定：九欄 Filter 的欄位／運算子／右值、AND 組合、四路條件、查重陣列與來源鍵均可照填；新增可閱讀 HTML 指南。
- 跨課銜接：S1→S2 原寫入移入 inquiry 分支，S2→S3 插入讀取與防重；保留既有紀錄，核對新增量。單獨測 GET 不提前消耗測試列。
- 起始材料：Source、ReviewedQueue 各放一筆指定示例；Source 改字與 ReviewedQueue 新增列的動作／結果明列。
- 附件核對：正確可記一致，不必製造修正或不確定詞；無能力仍標 NOT_RUN。
- 專題時點：CH7-2 初稿保存後即可看示範，PRAC7 交接成果。

驗證：28 單元的原文段落／表格／程式區保真、lint、結構；383 個本地連結／錨點；3 份指南保真；24 組 UI 條件測試；21 組瀏覽器視窗、深連結另開新頁、同頁導覽與捲動還原。四份講義保留原 auth/nav，24 份其他講義內容不變。搜尋／sitemap 僅更新本課項目。

本輪 actor 為 author-self-check／tool-run，無真人試走或當日 Make 帳號實跑。Blueprint 保持原版；email pattern 的匯入跳脫解讀仍需在 Make 核對，不將本機 regex 試算稱為平台等價驗證。完整結果見 make-rule-checks.json、browser-results.json、static-checks.log。歷史 content FAIL 保留，新增修復後內容紀錄；真人與平台證據維持 PENDING。

備份：_backup/2026-10-11-followthrough-pre-repair；還原入口：_tools/restore-2026-10-11-followthrough-pre-repair.sh。發布狀態另見 RELEASE.md。
