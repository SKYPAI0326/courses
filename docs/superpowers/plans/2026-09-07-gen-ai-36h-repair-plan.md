# gen-ai-36h 完善修正執行計畫

## 目標

把 `gen-ai-36h` 從「靜態頁面可讀」提升到「零基礎學員有固定起點、可操作、可檢查、可恢復，並能帶走成果物」；保留未做 SaaS 實跑與真人試跑的 `NOT_RUN` 邊界。

## 執行順序

### 1. 建立治理與回復邊界

- 備份修復前的課程檔案到 `gen-ai-36h/_backup/2026-09-07-pre-repair/`。
- 建立 `gen-ai-36h/_tools/restore-2026-09-07-pre-repair.sh`，可將修復前檔案逐一還原。
- 建立 `gen-ai-36h/_repair/2026-09-07/REPAIR-PLAN.md` 與 `REPAIR-REPORT.md`。

驗收：備份檔數量與原始課程檔數一致；restore script 通過 shell 語法檢查。

### 2. 建立課程級素材與執行契約

- 新增最小可用的表單／試算表欄位說明、測試案例、會議文字與流程輸入資料。
- 明示主路徑所需帳號、免費／未驗證限制、替代路徑與 `NOT_RUN` 證據界線。
- 固定 Part 5→6→7 的交付物名稱、欄位與證據格式。

驗收：學員不需自行發明資料格式即可開始；跨 Part 交付物有明確檔名與欄位。

### 3. 修正 Part 5 操作主線

- `CH5-1`：補固定起始表格、欄位、觸發與首個可觀察結果。
- `CH5-2`：將安裝／Tunnel 內容拆成可選環境分支，補安全停止與重跑起點。
- `CH5-3`：移除 API key 作為主流程前置條件，將 API 留為選修未驗證分支；主流程改為人工 AI 判斷加零代碼通知／歸檔。
- `CH5-4`：改寫費用與工具選擇表，避免未驗證的絕對免費或價格宣稱。
- `PRAC5`：將長 Demo 改為階段卡，加入 expected output、quick check、recovery、evidence 與 NOT_RUN 標記。

驗收：主線可在無 API key／信用卡下開始；每階段可判斷成功或停下來修復。

### 4. 修正 Part 6–7 成果鏈

- `CH6-1`：提供固定的 Part 1–5 交付物索引與填寫欄位。
- `PRAC6`：改成可直接填寫、列印／另存 PDF 的系統圖譜模板，移除 HTML 修改要求。
- `CH7-1`：用 Part 6 欄位作為專題 MVP 入口，補範圍檢核與證據要求。
- `PRAC7`：改成可填寫的成果發表頁，不保留假連結或無效佔位 href。

驗收：PRAC6／PRAC7 不需修改原始碼；產出可被 Part 7 使用的成果物。

### 5. 驗證與報告

- 對所有修改 HTML 執行 `python3 docs/lint-page.py`。
- 執行 `git diff --check`、佔位符／無效連結掃描與跨 Part 欄位掃描。
- 更新 `REPAIR-REPORT.md`，分開列出靜態通過、外部 SaaS 實跑與真人 cold follow-along 的狀態。
- 只在證據存在時宣稱完成；未執行的外部驗證維持 `NOT_RUN`。

## 不在本批次

- 不新增 API、RAG、Agent 或 Function Calling 教學。
- 不批次重寫 Part 1–4 的所有教學頁；先以 Part 5–7 交付鏈驗證修復設計，再決定第二階段。
- 不以 lint 通過取代真人試跑或目標 SaaS 工作區驗證。
