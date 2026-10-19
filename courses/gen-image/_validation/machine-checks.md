# gen-image 技術檢查紀錄

- 測試時間：2026-10-16（Asia/Taipei）
- 執行者：tool-run
- 範圍：大綱列出的 13 個核心單元，以及課程目錄全部 42 個 HTML
- 模式：本地靜態檢查、連結稽核與瀏覽器 smoke test；未登入第三方生圖平台

## 指令與結果

1. `python3 docs/lint-page.py courses/gen-image --summary --v3-soft`
   - 42 頁；BLOCKER 0、ERROR 0、WARN 31。
   - WARN 為既有排版／callout 建議，沒有阻擋條件。
2. `python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py --batch courses/gen-image`
   - checked 42、blocked 0。
3. `python3 docs/audit-course-substance.py gen-image`
   - pages 34、block 0、machine_checked 34、missing_assets 0；semantic_review 仍須由審查紀錄提供。
4. 課程內本地 `href`／`src` 稽核
   - 42 頁、374 個本地參照、missing 0。
5. `git diff --check -- courses/gen-image _outlines/gen-image.md _outlines/gen-image.style-guide.md _lessons/gen-image`
   - exit 0。
6. 瀏覽器 smoke test
   - 既有代表學習路徑：index、PRAC2、CH3-1、PRAC3、CH4-1、CH5-1、module6、CH6-C4、quick card。
   - 最後修正版補測：CH1-1、CH2-2、PRAC4、CH5-1、CH6-B1、CH6-B3、CH6-B5、CH6-B6、CH6-C2、CH6-supplement-typography；最後語意收斂後再補測 CH6-C2、PRAC4、CH6-B1。
   - 視窗：1440×900、390×844，另曾測 430px 寬。
   - 結果：無水平溢位、無載入失敗圖片、`.lesson-body` 存在；viewport 已 reset。
7. `_tools/restore-2026-10-16-pre-repair.sh`
   - `bash -n` 通過；未執行還原。
8. `validate_course.py gen-image all`
   - 首跑揭露 13 份 source 缺少正式 learner-content 邊界；補上單一成對 marker、重建版本 hash 後重跑。
   - 最終 exit 0、errors 0、valid_record_count 3、狀態 `MACHINE_READY_PENDING_HUMAN`。

## 限制

- 靜態檢查與本地瀏覽器 smoke test不能證明學員能獨立完成，也不能取代第三方平台當日實跑。
- 平台介面、方案、權利條款、輸出能力與來源訊號會變動；課程已把這些改為上課當日 capability check。

## 2026-10-19 整併後靜態複驗

1. `python3 _tools/verify-image-refresh.py`
   - PASS：59 筆舊圖遷移資產、60 個已引用版本化目標、0 個舊路徑參照。
2. 42 個頂層 HTML 加 `assets/downloads/skeleton-quick-card.html`
   - 結構：43/43 通過，blocked 0。
   - lint：BLOCKER 0、ERROR 0、WARN 31。
3. 學員頁 substance 稽核
   - 明確範圍 36/36 通過：CH、PRAC、兩小時工作坊頁與 quick card。
   - 遞迴課程目錄會額外發現 1 個歷史備份與 1 個圖片可編輯來源 HTML；這兩個內部檔案不列入學員頁驗收。
4. `COURSE_WEB_ROOT=<isolated-worktree> course-validator.sh gen-image all`
   - exit 0、errors 0、valid_record_count 3。
   - 狀態仍為 `MACHINE_READY_PENDING_HUMAN`；人員理解／轉移與當日平台實跑並未被靜態結果代替。

## 2026-10-19 整併後瀏覽器複驗

- 範圍：19 個代表頁× 390、430、820、1440px，共 76 組。
- 方式：本機 HTTP server 與 Google Chrome；每個 viewport 獨立執行，頁面啟動前清除 localStorage。
- 結果：70 組無例外 PASS、6 組明示例外、0 個非預期失敗。
- 圖片：所有受測頁在 lazy-load 觸發與 decode 後均無破圖。
- 連結：未發現失效頁內 anchor；quick card 是獨立列印／下載產物，四種尺寸均無站內導覽，列為預期例外。
- 版面：CH2-1 的 700px funnel table 在 390px 與 430px viewport 分別造成 83px 與 43px 水平溢位；該既存例外未轉為 PASS。其餘受測頁無非預期溢位。
- 下載：quick-card HTML 與 PDF 均為 HTTP 200 且內容非空。
- 完整結果：`full-integration-browser-evidence.json`。

