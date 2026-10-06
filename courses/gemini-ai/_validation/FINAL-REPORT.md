# 課程驗證：gemini-ai

狀態：`MACHINE_READY_PENDING_HUMAN`（截至 2026-10-06 再檢核）。

這個狀態代表目前結構、內容鏈、連結、素材與瀏覽器回歸已通過機器檢查；不代表真人學員已學會、AI Studio 帳號內已成功生成，或課程已證明可在 6 小時內完成。

## 本輪結果

- 11 項課程驗收測試通過；45 頁結構檢查 0 阻擋。
- 45 頁連結與錨點 0 失效；10 個核心片段與正式頁面一致；40 單元目錄及 10 站必修路線完整。
- 10 個核心單元 substance 檢查 0 block／0 missing assets；continuity 檢查 0 warnings，仍需學員試讀。
- 瀏覽器 11 項檢查通過，80 個桌機／手機 viewport 觀察，無 pageerror 或水平溢出。
- 頁面 lint：0 BLOCKER、0 ERROR、82 WARN（40 個 `data-built-at` 欄位、40 個舊字級 token、2 個 hover 動畫建議）。
- 70 筆來源明確的舊技術敘述修正均列於 `_repair/2026-10-06/re-review/technical-corrections.json`；原始教學正文可依 allowlist 完全還原。

## 待驗

學員獨立完成、理解與遷移；帳號內 AI 生成／模型呼叫／專案重開；不同帳號的實際 UI／額度；6 小時課程時長。

本輪完整證據、作者冷讀、warning 分布與回復方式見 [VERIFICATION.md](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gemini-ai/_repair/2026-10-06/re-review/VERIFICATION.md>)。`evidence.json` 與 `validation-result.json` 是先前驗證快照，不作為本輪通過證據；本輪新鮮雜湊與執行結果收在 `re-review-evidence.json`。
