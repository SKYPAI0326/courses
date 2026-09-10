# n8n 課程修復報告

日期：2026-09-10  
修復範圍：n8n learner-facing lessons（P0 → P1 → P2）  
平台實跑：本批未執行 n8n、Make、Google Forms、Gemini 或 Gmail；頁面中的平台結果仍須以 MAKE／N8N／NOT_RUN 分開記錄。

## 已完成

### P0｜主路徑與起點

- lessons/index.html：把 Module 摘要改為可直接進入的核心實作頁，標示必修順序、完成物與延伸頁。
- lessons/m1-1-setup.html：補充 1.1.0 → 1.1.1 → 1.1.2 的主線與 1.1.3 排錯回路。
- lessons/m1-3-json.html：加入固定輸入、固定 AI 輸出文字、Webhook／Set／Code `JSON.parse()` 建立順序與 4 個 checkpoint；補 macOS／Windows 送出指令。
- lessons/m4-1-remote.html：建立本機固定資料主路徑；Forms／Make／Apps Script／Tunnel 改為延伸路徑，補 Mac／Windows 指令、前置條件與完成證據。

### P1｜可跟做與跨平台

- m3-1-watch.html：加入資料夾、手動執行、binary 與 PDF 分流檢查點。
- m3-2-rename.html：補起點與完成物，API key 改以 Header Auth 說明，保留原檔副本驗收。
- m3-3-generate.html：加入固定 AI 回覆路徑，補排程、讀檔、AI、格式化與寫檔檢查點。
- m4-2-hybrid.html：回指 4.1 完成證據，區分本機核心與外部雙向鏈路。
- m4-1／m4-2 與 `m4-bridge-contract-fixture.json`：支援 BRIDGE-1 的 `task_type`／`data` 封裝，並以 Normalize 節點統一本機與 Make 輸入。
- m4-3-ai.html：移除講師 Live Demo 依賴，提供固定 AI 回覆作為無 key 練習路徑。
- m2-2-chaining.html、m2-3-logic.html：補固定資料、空白畫布起點與分段驗收。
- m0-install-mac.html、m0-install-win.html：補 Phase A／B 停點，讓學員在環境、登入、workflow 匯入後再往下走。
- m4-1-remote.html：補本機／BRIDGE 輸入形狀 Checkpoint、Downloads 工作目錄、必填欄位驗證與契約錯誤出口。
- m4-2-hybrid.html：補 `request_id` 回傳、本機 `status`、資料夾／權限恢復與 Gmail 無測試地址時的 `NOT_RUN` 規則；Code 節點缺少申請欄位時會停止並回指 4.1 契約檢查。
- m4-3-ai.html：分離 API／固定資料驗收，補 Google AI Studio API key 與 n8n Header Auth 前置，外部回傳加入 `request_id`。

### P2｜用語與安全

- Gemini HTTP Request 範例改用 x-goog-api-key Header Auth，避免把 key 放進 URL。
- 整個 n8n/lessons 目錄清除「不是……而是……」句型，並同步修正來源審查文件的相同句型。
- m0-workflow-01-webhook.html 加上「閱讀／設計參考」定位。
- 修正 Module 1～4 的 Quick Tunnel、雲地分工與自架成本描述。

## 驗證證據

lint-page.py n8n/lessons --summary：掃描 77 頁，BLOCKER 0，ERROR 0，WARN 171。WARN 來自既有字型、metadata 與頁面結構提醒，未作為本批阻斷條件。

local-link check：排除備份／修復歷史檔後，checked 605 local links；missing 0。

JSON assets：m1-3-test-payload.json、m1-3-ai-output.json、m4-1-form-request.json、m3-3-ai-output.json、m4-3-ai-output.json 與 m4-bridge-contract-fixture.json 均通過 JSON 格式檢查。

新增文字資產：`m1-3-ai-output-text.txt` 可作為 Set 的 `ai_text` 固定輸入。

追加驗證：Make／n8n 本地連結檢查維持 605 條，缺少 0；兩份還原腳本 `bash -n` 通過；`git diff --check` 通過。

## 尚待處理

1. BRIDGE-1 已在 Make CH1-6 與 n8n m4-1／m4-2 對齊；仍需在實際工作區匯入並驗證成功、人工處理、契約錯誤三條終態。
2. 需要在 Mac 與 Windows 各實跑一次 M0、Webhook、檔案讀寫與固定 AI 回覆路徑，才能升級為平台執行證據。
3. docs/audit-course-substance.py 目前不存在；本批以頁面 lint、連結／資產檢查與 learner-path 靜態審查替代，不能取代 L4／L5 真跑驗收。

## 還原

本批原始檔案位於 n8n/_backup/2026-09-10-pre-repair/；還原腳本位於 n8n/_tools/restore-2026-09-10-pre-repair.sh。
