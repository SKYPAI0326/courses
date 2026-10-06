# Gemini AI 課程邏輯銜接回修：技術驗證

日期：2026-10-06（Asia/Taipei）
性質：可重跑的靜態與素材檢查紀錄；不替代平台操作或真人測試。

## PASS

- `python3 _tools/verify-static.py`：45 頁連結及錨點、10 站路線、正式來源保真、素材 ZIP、長文重複及搜尋範圍檢查通過。
- `validate-course-structure.py --batch .`：檢查 45 個 HTML，`blocked=0`。
- `docs/lint-page.py` 指定本次 12 個 HTML：掃描 12 頁，BLOCKER 0、ERROR 0、WARN 24。WARN 為既有 metadata／字體遷移類提醒；未作為通過內容審查的替代證據。
- `docs/audit-course-substance.py` 的 `audit_page`：10 個必修單元均為 `MACHINE_CHECKED`，頁面引用素材可讀取且具雜湊。
- 針對 `reference-answers.json`、CSV 和 ZIP 的斷言：預算新資料餘額 3,700 不提醒；講師實支 11,200 後實支 23,000、餘額 2,000 且提醒開啟；既有 KPI 狀態符合方向；A/B task_id 非空且唯一並無依賴；C 的「安排印刷」依賴「品牌定稿」；驗收 CSV 16 列皆有預期答案、觀察留白且待測；ZIP 完整並含新增的逐字稿 C 及 capstone 指令。
- `python3 _tools/restore-2026-10-06-continuity-fix.py --check`：備份檔雜湊有效，`files=28`、`absent=6`。
- `validate_course.py gemini-ai report`：狀態 `MACHINE_READY_PENDING_HUMAN`、errors 0、有效記錄 3；平台實測、真人各層與完整課程序列仍列 PENDING。

## PENDING 與範圍限制

- Google AI Studio 的 Build 生成、模型呼叫、登入條件及同一專案關閉／回開未實測；platform 保持 PENDING。
- 未由初學者實際跟做；entry、completion、understanding、transfer 與 sequence 保持 PENDING。
- 未執行桌面／手機瀏覽器 smoke。CUA 明確阻擋 `file:` 課程預覽並禁止透過本機伺服器達成同一結果；本次尊重限制，未做本機預覽替代。
- 共享站台搜尋索引與 sitemap 在本課目錄外，沒有更新。

以上 PASS 僅表示所列靜態、來源、結構、素材及數字檢查成功。
