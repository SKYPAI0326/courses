# make-ai-workflow 修正報告

日期：2026-09-10  
範圍：Make 六頁、跨平台契約、n8n Module 4 銜接

## 已完成

### P0｜跨平台契約

- 新增 `assets/BRIDGE-1-make-n8n-contract-v1.md`。
- 定義 `request_id`、`source_platform`、`task_type`、`evidence_mode`、`data` 外層封裝。
- 以 `customer_feedback` 與 `document_request` 兩個任務型別示範原樣傳遞、轉換與人工確認。
- Make CH1-6 新增跨平台銜接示範、四步操作、Checkpoint 與完成物。
- CH1-6 新增 `CH1-6-bridge-worksheet.md`，明確區分 `document_request` 主線與 `customer_feedback` 延伸，並連到 n8n M4-1／M4-2。
- CH1-3 補上 Make UI 操作卡：試算表建立／CSV 匯入、Watch Rows、Gemini、Filter 布林條件、Docs 映射與 A／B 測試。
- CH1-3～CH1-5 將版本與證據提示移到 page hero 之後，先呈現情境、完成物與材料。

### P1｜n8n 對齊

- n8n m4-1、m4-2 連回 BRIDGE-1，外部路徑改用 `task_type`／`data`。
- n8n m4-1 加入 Normalize bridge data，兼容本機固定資料與 Make 封裝後資料。
- n8n m4-2 的文件產生範例先讀取 `bridge_data`，回傳增加 `request_id`，通知使用課程提供的測試收件地址。
- n8n bridge fixture 允許 Make 選填欄位 `urgency_signal=null`，仍保留 `SIMULATED` 證據邊界。
- n8n M1-3 改用 Set 的 `ai_text` 與 Code `JSON.parse()`，新增 `m1-3-ai-output-text.txt` 固定文字資產及 macOS／Windows 指令。
- n8n M4-1 增加本機／BRIDGE Checkpoint、下載後工作目錄、必填驗證與契約錯誤出口；M4-2 補 `request_id`、`status` 與檔案恢復；M4-3 分離 API／固定資料驗收並補 Header Auth 取得方式。

### P2｜語句與驗證

- 修正課程來源文件中四處「不是……而是……」句型。
- 建立 `make-ai-workflow/_tools/restore-2026-09-10-pre-repair.sh`，可回復本批修正前檔案。

## 驗證結果

- Make lint：7 頁，BLOCKER 0、ERROR 0、WARN 13。
- n8n lint：77 頁，BLOCKER 0、ERROR 0、WARN 171。
- HTML 本地連結：排除備份與修復歷史檔後，Make／n8n 合計檢查 605 條，缺少 0。
- 新增與既有 JSON fixture：可解析 PASS。
- `m1-3-ai-output-text.txt` 固定 JSON 文字可讀取 PASS。
- bridge fixture 邏輯試跑：`customer_feedback` A／B／C 與 `document_request` 各一筆均得到預期的 valid／invalid 路由。
- `bash -n make-ai-workflow/_tools/restore-2026-09-10-pre-repair.sh`：PASS。
- `git diff --check`：PASS。
- 禁用句型掃描（排除 backup／repair 歷史檔）：命中 0。

## 尚待真人驗證

- 尚未在學員的 Make 工作區匯入、重綁連線並執行 BRIDGE-1。
- 尚未在學員的 n8n Docker 環境匯入 bridge fixture，確認不同版本節點畫面與 Webhook Output。
- 尚未完成 Make → Tunnel → n8n 的 Windows／macOS 雙系統 cold follow-along。
- `MAKE`、`SIMULATED`、`NOT_RUN` 的證據狀態仍須依真人執行紀錄填寫，靜態檢查不代表平台已執行。

## 還原

執行 `make-ai-workflow/_tools/restore-2026-09-10-pre-repair.sh` 可回復本批修正前的 Make 頁面、素材、教案與大綱。新增的 BRIDGE-1 與修正紀錄會保留，若需移除請另行確認。
