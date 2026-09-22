# Repair Plan: office-ai

## Scope

- slug：`office-ai`
- pages：19 個單元頁 + 1 個課程總覽
- lessons：已建立 19 個 legacy-reconstructed-draft source，仍需 reviewer 逐單元核准
- related outline：`_outlines/office-ai.md`
- excluded：既有 `_backup/`、舊 `_repair/`、既有 `_validation/status.jsonl`

## Risk

- 近期開課：unknown
- 既有多批備份：yes
- 本輪備份：required
- 未經來源審查直接改 HTML：禁止

## 初始 BLOCKER（已處理）

### [VALIDATION] 建立正式正文來源

- 問題：初始沒有 `_lessons/office-ai/`，無法建立每單元的 source hash、內容審查與 HTML fidelity 交接。
- 修法：已依大綱建立 19 個 `_lessons/office-ai/{unit-id}.md`；保留 HTML 中的有效教學內容，learner content 位於邊界標記內，內部狀態位於標記外。
- 驗證：19/19 source 有 frontmatter、課型、目標、style guide、唯一 learner-content 邊界；來源仍標記為重建草稿，待 reviewer 核准。

### [VALIDATION] 建立 evidence.json

- 問題：初始 `course-validator` 因缺少 `_validation/evidence.json` 直接 BLOCKED。
- 修法：已建立 schema version 1 的 `evidence.json`，列出大綱 hash、19 個 unit、HTML page、所有學員資產與 scope note。
- 驗證：`status`、`preflight`、`all` 均回傳 `MACHINE_READY_PENDING_HUMAN`，errors 為 0；缺真人證據不升格為 PASS。

## MAJOR

### [LEARNER_PATH] 概念型四頁契約補強

- 範圍：`CH1-1`、`CH1-2`、`CH6-2`、`CH6-3`。
- 修法：不以增加步驟數灌水；補明合理的起始材料、第一個判斷或分類動作、可觀察結果、完成物用途，以及判斷錯誤時回到的例子或規則。
- 驗證：入口六題、概念型完成物、短 rationale／分類判準與自我檢查均能從講義讀出。

### [PLATFORM / VALIDATION] 實際平台條件與版本

- 範圍：使用 Google 文件語音輸入、通用 LLM、NotebookLM 或 Google 簡報的頁面。
- 修法：先依 `course-refresh` 產出人工重查清單；只有真的重跑並記錄帳號、方案、瀏覽器、權限與結果後，才更新 evidence 與 metadata。
- 驗證：實際素材能開啟，第一個動作與錯誤恢復路徑可完成；平台不適用時明示原因。

## MINOR

### [TYPOGRAPHY / MOTION] 21 個 lint 警告

- 修法：來源與內容證據穩定後，再將 `.76rem`、`1.35rem` 等非 V4 字階與 2 頁 hover 規則交給 typography／CSS 小範圍修補。
- 驗證：重新執行 `lint-page.py`，並做受影響頁面的瀏覽器 fidelity 檢查。

## Execution Order

1. 建立本輪 backup 與 restore script；不得動既有 2026-07-15 備份。
2. 整理 19 個正式正文 source；本輪已完成，保留來源重建限制。
3. 建立作者自審 content/fidelity logs，留下位置、hash 與限制；獨立 reviewer 仍待執行。
4. 建立並驗證 `_validation/evidence.json`。
5. 依正式正文確認的 Learner Path 缺口，已同步修正四個概念頁的 source 與 HTML。
6. 跑 `course-reviewer`、`course-ops`、`lint-page.py` 與 asset/link 檢查。
7. 跑 `course-validator preflight` 和 `all`。
8. 執行入口、完整跟做、理解、遷移、三課 sequence 與適用平台測試。
9. 產出 `REPAIR-REPORT.md`；本輪機器狀態為 `MACHINE_READY_PENDING_HUMAN`，真人或平台證據未完成前不得宣告 release-ready。

## 不在本輪直接做的事

- 不直接把目前 HTML 複製成沒有教學來源意義的 Markdown。
- 不憑記憶更新 Google／NotebookLM 的介面步驟。
- 不用增加步驟、卡片或口號來掩蓋正式來源缺失。
- 不沿用舊 `status.jsonl`、舊 hash 或 2026-07-15 的條件式 PASS。
