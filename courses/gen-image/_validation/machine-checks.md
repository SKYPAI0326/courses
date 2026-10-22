# gen-image Deep Review 修補技術檢查紀錄

- 測試時間：2026-10-22（Asia/Taipei）
- 執行者：tool-run
- 範圍：正式 44 個 HTML 結構；本輪 9 個變更頁 lint；CH5-1／PRAC2／PRAC3／PRAC4 內容與瀏覽器行為
- 模式：本地靜態檢查與瀏覽器驗收；未登入第三方生圖平台

## 指令與結果

1. `python3 _tools/test-deep-review-repair.py`
   - 41 個核心頁全部可由 index 到達；0 個 `.md#fragment`；CH5、OFFLINE-01、學員紀錄、v63／v64 與證據雜湊契約均納入檢查。
2. `python3 _tools/verify-image-refresh.py`
   - PASS：60 筆 manifest、60 個頁面實際使用的 versioned targets、0 legacy references。
3. `python3 _tools/test-learner-record-browser.py`
   - PASS：四頁控制存在；contenteditable 重載後保留；下載 JSON 可解析；CH5 在 390×844、430×932、820×1180、1440×900 無水平溢位且必要契約可見。
4. `python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py --batch courses/gen-image`
   - checked 44、blocked 0。
5. `python3 docs/lint-page.py <9 個本輪變更頁> --summary --v3-soft`
   - 9 頁；BLOCKER 0、ERROR 0、WARN 2（既有 hover／callout 建議）。
6. `python3 docs/audit-course-substance.py gen-image --page <CH5-1／PRAC2／PRAC3／PRAC4>`
   - 四頁逐頁皆 block 0、missing_assets 0；semantic review 由本輪內容自審紀錄提供。
7. `git diff --check -- courses/gen-image _lessons/gen-image/CH5-1.md _lessons/gen-image/PRAC2.md _lessons/gen-image/PRAC3.md _lessons/gen-image/PRAC4.md`
   - exit 0。
8. `_tools/restore-2026-10-22-pre-deep-review-repair.sh`
   - `bash -n` 通過；隔離還原驗證 checked 25、mismatches 0。

## 全目錄掃描的既有邊界

- 未限縮路徑的 lint 會掃到 `img/workshop2h/l4-commercial-poster-source.html` 的既有 gradient，回報 1 blocker；該檔不在本輪修改或 Deep Review 問題範圍。
- 未限縮路徑的 substance audit 會掃到 `_deep_review` 與 `_workshop/backups` 快照，回報 6 blocker／8 missing assets；這些是審查候選與備份，不是正式 learner-facing 頁。
- 本輪沒有為了讓統計變綠而修改上述無關檔案；正式 44 頁結構與 9 個變更頁均以明確範圍驗收。

## 限制

- 靜態與本地瀏覽器檢查不能證明學員可獨立完成，也不能取代第三方平台當日實跑。
- `quality-gate.md` 在目前 skill 套件中不存在；本輪改以實際 learner-action contract、course-content-substance 與 evidence format 驗收。
