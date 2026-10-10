# UI/UX 網站上架與總課程目錄整合

授權：使用者「確認是否正式上架網站，並整合進總課程目錄當中」。
2026-10-11 檢查：GitHub Pages 使用 main 根目錄，最新 763900c7 已 built；UI/UX 入口 HTTP 200、無密碼關卡。總課程入口與 COURSES.md 尚未登錄。遠端搜尋名稱已有 UI/UX設計師，本機工具需同步。

## 修改範圍

- index.html：沿用既有卡片 DOM，將「AI 創意產出」改為「設計與創意產出」並加入 UI/UX 99h、16 堂卡片，分類數量 2 → 3。
- COURSES.md：新增課程摘要與資料夾，清單數量 25 → 26；記錄公開講義與平台／真人驗收待補。
- docs/build-search-index.py：本機補齊遠端已有的課程名稱。
- search-index.json、sitemap.xml：執行現有建置工具，只合併 UI/UX 條目與首頁修改日期；保留其他課程原條目。
- 本輪已修訂的 30 個來源／講義／材料／驗收狀態檔與修訂紀錄：遠端全部與修前備份一致，帶入已完成修正，不覆寫其他課程。
- _repair/2026-10-11-publication：保存差異、索引、部署與實際頁面證據。修訂前的 scoped-evidence 搜尋索引 hash 為歷史值，發布證據綁定新索引。

## 驗收

目錄唯一卡片與分類數量、既有卡片不變、公開連結可用、頁面 lint、來源 hash、索引範圍與 git diff 檢查；隔離副本顯式 staging、一般 push main、GitHub Pages built、實際 HTTP 頁面與發布檔 hash 相符。保留原混合工作區與暫存狀態。沿用已上架的公開存取；平台操作、真人與時數驗收仍待補。
