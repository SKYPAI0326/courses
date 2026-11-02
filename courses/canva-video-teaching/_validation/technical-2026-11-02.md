# Canva 全課機器檢查（2026-11-02）

- 執行時間：2026-11-02 11:36 +08:00
- 範圍：canva-video-teaching 全課，13 個 lesson unit；29 個 HTML 檔 lint，26 個學員單元與資源 HTML 做本地連結／素材檢查。
- 方法與結果：
  - `python3 docs/lint-page.py courses/canva-video-teaching --summary`：退出碼 0；掃描 29 頁，0 BLOCKER、90 ERROR、0 WARN。
  - `python3 docs/audit-course-substance.py canva-video-teaching`：退出碼 0；26 頁通過、0 BLOCK、0 missing assets。
  - 以同一 audit 的 `discover_pages`／`audit_page` 統計：檢查 333 個本地連結，0 broken links。
- 結論：本次機器檢查沒有 BLOCKER 或失效本地連結。90 個 lint ERROR 保留在報告中，沒有在本卡範圍內修正。
- 限制：此紀錄只證明本次靜態檢查結果，不證明內容審查、Canva 平台完整流程、真人學員理解或課程可發布。
