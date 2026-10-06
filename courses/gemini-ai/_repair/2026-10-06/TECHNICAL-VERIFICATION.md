# 本次技術與操作證據

日期：2026-10-06。執行者：tool-run；教學判斷與真人能力另列。

- `lint-page.py courses/gemini-ai/ --summary`：45 頁，0 BLOCKER、0 ERROR、83 WARN。原基準41頁為82 WARN；本次沒有擴大處理非核心的字型與 metadata 維護債。完整輸出：lint.log。
- `validate-course-structure.py part1/*.html … part6/*.html`：40 學習頁全部通過。index 用原有15個卡片 lesson-body 的實際數量檢查，不新增講義 wrapper，通過。
- `audit-course-substance.py gemini-ai`：40 學習頁，0 BLOCK、0 missing assets；這個工具的 semantic_review 本來就是PENDING，不能當語意放行。
- `_tools/verify-static.py`：45頁連結／錨點／重複ID、10站下一頁閉環、源頭正文與連結保真、ZIP與逐檔一致、非本課搜尋紀錄保留，通過。
- `_tools/verify-browser.cjs`：隔離Chrome，11組操作檢查、63個viewport／位置觀察，無pageerror。完整動作與結果：evidence/browser-results.json。
- 作者閱覽桌面預算修改區、手機AI交辦及手機預算截圖；表格在自身容器滑動，頁面未滿版或水平溢出。1440px代表頁測頂／修改區／中／底，390與430px測入口與導覽。未測全部選修的所有互動分支。
- 匯出成品：evidence/budget-report.csv、budget-backup.json、budget-print.pdf；kpi-monthly-report.csv、kpi-backup.json、kpi-print.pdf。PDF已讀取與檢視，均1頁；KPI表頭方向欄的表單顯示較窄，完整方向另於各指標正文呈現。這不是已完成AI生成工具的證據。
- 舊挑戰計時器新增檢查：Node VM實際跑倒數歸零，record.verified=false，紀錄不顯示通過勾號；evidence/legacy-timer-results.json。此檢查使用DOM替身，不冒充瀏覽器畫面。
- 還原腳本：bash -n通過；在/private/tmp隔離資料夾實際還原41頁及搜尋／sitemap，逐檔hash與備份完全一致，restore-test.json。
- 搜尋／sitemap：官方產生器輸出到候選檔，再只合併本課；已套用45筆搜尋、4筆非關卡參考頁sitemap。其他課程紀錄原樣保留，ops-baseline.json。
- `git diff --check`：通過。沒有stage、commit、push或部署。

## 中間失敗與修復

HTML編輯先遇meta序列化差異，未寫入頁面；改成保留屬性順序的局部opening-tag更新。SEO檢查器要求name/property置於content前，已同步修正，最後0 ERROR。

熱點未知樣式最初使用不合規漸層，改為實色與虛線邊框，最後0 BLOCKER。素材掃描曾把內部HTML片段當完整頁，改用.fragment副檔名，正式頁素材沒有缺檔。

無頭Chrome在沙盒內無法啟動，改以已核准的隔離本機測試執行。第一輪JSON上傳測試未等檔案讀取完成而誤判；補非同步狀態等待後，非法還原保留資料與有效還原都通過。失敗紀錄保留於evidence/browser-failure.txt，不把它當現行測試狀態。

最後新增低餘額改造文字與下載連結、修正舊倒數未驗收紀錄後，重新核對受影響內容、結構、素材、連結及diff。瀏覽器截圖保留測試當時版本；後續純文字變更的影響分析見正文複核。

## 平台與真人待驗

實際開啟AI Studio到Google「驗證您的身分」畫面，無可直接使用的登入環境。本次未登入、未接受新權限、未建立AI專案或呼叫模型。

故本次僅支持本機技術條件與作者內容／保真自審。Chat生成、Build語意與保存、實際帳號條件，以及真人入口、完成、理解、遷移與三站連續跟做均PENDING，不能宣稱HUMAN_READY或全課實際授課已通過。
