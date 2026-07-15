# Repair Plan: office-ai

## Scope

- slug: `office-ai`
- source scan: `courses/office-ai/_repair/2026-07-15/SCAN.md`
- pages to repair: 19 lesson pages
- index page: inspect during final ops verification; no content change planned
- lessons: `_lessons/office-ai/` not found; this repair will use the outline and existing HTML as source material unless a later lesson-design scope is explicitly approved
- deletion policy: preserve existing content; compress or relocate repeated material only after it is included in backup

### Planned HTML Scope

- `ch1/CH1-1.html` ～ `ch1/CH1-4.html`
- `ch2/CH2-1.html` ～ `ch2/CH2-3.html`
- `ch3/CH3-1.html` ～ `ch3/CH3-3.html`
- `ch4/CH4-1.html` ～ `ch4/CH4-3.html`
- `ch5/CH5-1.html` ～ `ch5/CH5-3.html`
- `ch6/CH6-1.html` ～ `ch6/CH6-3.html`

## Risk

- near-term class: unknown
- backup required: yes
- restore script required: yes
- content risk: high — 19 pages share one legacy structure; broad mechanical replacement could erase page-specific cases
- platform risk: medium/high — lesson metadata is `2026-04-v3`; current UI has not been verified
- validation risk: high — no lesson files and no current true-run evidence
- safe execution rule: fix only 1–3 pages per batch, review the diff, then lint and recheck Learner Action Contract before continuing

## Repair Contract

Each repaired `skill-operation` page must contain:

1. one named learner deliverable;
2. explicit starting state and required material;
3. one minimum successful path;
4. 5–12 executable steps with action and expected result;
5. a checkpoint every 3–5 steps;
6. step-linked recovery guidance;
7. at least one Solo variation exercise with a pass criterion.

Each repaired `concept` page must contain:

1. one identifiable learning artifact;
2. 2–4 short scenario judgments or exercises;
3. a checkable criterion for each exercise.

Existing examples, prompts and factual caveats remain the source material. Repair does not authorize invented platform steps or new claims.

## BLOCKER

### [LEARNER_PATH] Concept candidate pages

Files:

- `ch1/CH1-1.html` — AI 能幫我做什麼
- `ch1/CH1-2.html` — 主流工具介紹
- `ch6/CH6-2.html` — 安全與限制
- `ch6/CH6-3.html` — 持續學習的方法

- 問題：缺可辨識學習產物，以及 2–4 題具有判準的短練習；現有情境與條列主要供閱讀。
- 修法：保留現有概念內容，分別產出「任務適配判斷表」「工具選擇卡」「去識別化檢查表」「30 天應用計畫」，加入情境題與可核對答案。
- 驗證：每頁能指出唯一產物；練習題數 2–4；每題有明確判準；lint 0 BLOCKER / 0 ERROR。

### [LEARNER_PATH] Foundation operation pages

Files：

- `ch1/CH1-3.html` — 基礎操作指南
- `ch1/CH1-4.html` — 有效溝通第一步
- `ch2/CH2-1.html` — 進階指令技巧
- `ch2/CH2-2.html` — 調整風格與語氣

- 問題：只有 3–4 條操作或概念摘要，缺最短可跑路徑、步驟預期結果與 checkpoint。
- 修法：以同一份低風險辦公素材串成 Demo → Together → Solo → Check；每頁完成一份可保存 prompt 或輸出。
- 驗證：每頁 5–12 步；至少 2 個 checkpoint；每步具操作與預期結果；至少 1 個卡關修復和 1 題變化練習。

### [LEARNER_PATH] Flagship true-run pages

Files：

- `ch2/CH2-3.html` — 客訴信三輪修正
- `ch3/CH3-1.html` — 週報真跑
- `ch3/CH3-2.html` — 表格整理與計算驗證
- `ch5/CH5-2.html` — 會議紀錄真跑

- 問題：已有案例與風險揭露，但主要是觀看真跑；缺學員逐步重做、途中停點與獨立變化練習。
- 修法：優先修成示範頁標竿。沿用現有案例，拆成準備資料、第一輪、核對、repair、最終交付、Solo 變化與自我檢查。
- 驗證：案例輸入、每輪 prompt、預期輸出、紅旗與修復行動可以一一對應；Solo 任務不依賴講師口頭補充；lint 和 reviewer A2 通過。

### [LEARNER_PATH] Remaining document and presentation pages

Files：

- `ch3/CH3-3.html`
- `ch4/CH4-1.html` ～ `ch4/CH4-3.html`
- `ch5/CH5-1.html`
- `ch5/CH5-3.html`
- `ch6/CH6-1.html`

- 問題：有示範或方法，但缺連續產物、完整同步步驟與檢核閉環。
- 修法：每頁只保留一條最小成功主線；將替代方法放在主線完成後，避免選項說明取代實作。
- 驗證：完成物、起始狀態、5–12 步、checkpoint、卡關修復與變化練習全部可定位。

## MAJOR

### [CONTENT_THIN] 六段共用模板重複，實作密度不足

- 問題：19 頁反覆使用「情境／核心要點／範例／變體／注意／延伸」，實作常被概念條列與第二次描述擠壓。
- 修法：保留頁面主題與案例，但把操作型頁面的主體改為「做、看、查、修」；重複安全提醒集中到關鍵 checkpoint，不在各段重說。
- 驗證：操作、預期結果、檢核、修復與練習占正文主體；同一任務不以不同說法重複描述。

### [STALE_UI] 平台畫面與 metadata 未確認

- 問題：19 頁標記 `2026-04-v3` 且缺 `data-built-at`；Google Gemini、NotebookLM、文件與簡報介面可能已漂移。
- 修法：在撰寫任何按鈕名稱或畫面位置前執行 `course-refresh office-ai`；需要當前 UI 的頁面只依可驗證畫面更新。完成後補真實 platform version 與 built date。
- 驗證：refresh 清單有處置紀錄；metadata 與實際核對日期一致；不保留未驗證的精確 UI 指令。

### [VALIDATION] 缺教案和案例真跑證據

- 問題：沒有 `_lessons/office-ai/`；目前無法確認案例輸入與聲稱輸出可重現。
- 修法：修復時在 repair report 記錄每個 flagship 案例的測試輸入、模型/平台與結果；無法重現的輸出標成示意，不冒充實測。
- 驗證：flagship 頁執行 reviewer A2；整課完成後執行 validator preflight，必要時跑 L5 persona。

### [NAV_OPS] 多頁修復後需重建衍生檔

- 問題：內容與 metadata 變更會影響站內搜尋和 sitemap；連結也需重查。
- 修法：全部批次完成後重建 search index 和 sitemap，再跑 links / gates 檢查。
- 驗證：build scripts exit 0；course-ops links / gates 無 BLOCKER。

## MINOR

### [TYPOGRAPHY] 非 V4 字階

- 問題：19 頁均含 `.68rem`、`.73rem`、`.76rem` 等 6 個非白名單值。
- 修法：內容結構穩定後，以 `course-typography-fixer` 規則做單一 CSS 批次，不改內容或 HTML 結構。
- 驗證：lint 不再回報非 V4 字階；桌面與 mobile 的中文標題、表格與卡片無異常斷行。

### [VOICE] 「您」與學員語氣不一致

- 問題：`CH2-1` 6 處、`CH5-3` 2 處、`CH6-1` 2 處。
- 修法：只在學員敘述中改為「你」；案例引文若為正式信件稱謂則保留並註明語境。
- 驗證：lint voice WARN 消失，且不誤改案例正文。

## Batch Execution and Acceptance

### Batch 0 — Refresh and backup gate

Files：19 個 scope HTML。

- 動作：跑 refresh；建立 `_backup/2026-07-15-pre-repair/`；建立 `_tools/restore-2026-07-15-pre-repair.sh`。
- 驗收：備份檔數與 scope 相符；restore script 通過 `bash -n`；抽查還原來源與目的路徑；未改 live HTML。

### Batch 1 — Flagship pilot

Files：`CH2-3`、`CH3-1`。

- 動作：建立第一套 Demo / Together / Solo / Check 節奏，確認共用修復模式。
- 驗收：逐頁 Learner Action Contract 全項通過；逐頁 lint 0 BLOCKER / 0 ERROR；diff 只含指定頁。

### Batch 2 — Flagship completion

Files：`CH3-2`、`CH5-2`。

- 動作：沿用已驗證模式，但保留表格計算與會議決議的不同核對機制。
- 驗收：真跑輸入輸出有紀錄；數學與決議判準不交給 LLM 自行判定；reviewer A2 通過。

### Batch 3 — Foundation operations

Files：`CH1-3`、`CH1-4`、`CH2-1`。

- 動作：建立新手最短成功路徑，完成第一組可保存 prompt。
- 驗收：登入前置、輸入位置、預期畫面與卡關修復可照做；逐頁 lint 通過。

### Batch 4 — Prompt variation

Files：`CH2-2`、`CH3-3`。

- 動作：補語氣變化與長文摘要的 Solo / Check；避免再教一次相同 prompt 公式。
- 驗收：兩頁產物與練習不同；摘要中的數字核對有明確 checkpoint。

### Batch 5 — Presentation chain

Files：`CH4-1`、`CH4-2`、`CH4-3`。

- 動作：串成「大綱 → 單頁內容 → 配圖 brief」連續產物，各頁仍可單獨完成。
- 驗收：每頁明示承接輸入與本頁輸出；〔待補〕與不可新增資訊判準可檢查；當前工具 UI 已核對或標示為工具無關步驟。

### Batch 6 — Meeting and administration

Files：`CH5-1`、`CH5-3`、`CH6-1`。

- 動作：各自完成一條轉文字、行政通知、個人 AI workflow 主線。
- 驗收：CH5-1 不用三個選項代替主線；CH5-3 的待填欄位全部可檢查；CH6-1 留下可重用 workflow 模板。

### Batch 7 — Concept artifacts

Files：`CH1-1`、`CH1-2`、`CH6-2`。

- 動作：補任務判斷、工具選擇與安全去識別化產物。
- 驗收：每頁 2–4 題、有答案判準、不要求無意義 step-by-step。

### Batch 8 — Course closure

Files：`CH6-3`。

- 動作：把整課方法收斂成 30 天應用計畫與自我檢核。
- 驗收：產物可保存；能回扣前面各章但不重複整課內容；lint 通過。

### Batch 9 — Typography and voice

Files：19 個 scope HTML。

- 動作：統一 V4 字階；精準處理「您」；不改內容結構。
- 驗收：全課 lint 0 BLOCKER / 0 ERROR；相關 WARN 清零；mobile / desktop 視覺抽查通過。

### Batch 10 — Ops and G5 verification

Files：全課與衍生索引。

- 動作：重建 search index、sitemap；跑 links / gates；執行 reviewer 與 validator preflight。
- 驗收：build scripts exit 0；導航無斷鏈；reviewer 無 BLOCKER；validator 未通過項目列入 report，不以「已修改」代替完成。

## Execution Order

1. `course-refresh office-ai`
2. backup 19 個 scope HTML
3. 驗證 restore script
4. Batch 1–2：flagship learner-path fixes
5. Batch 3–6：其餘 operation fixes
6. Batch 7–8：concept artifacts
7. Batch 9：typography / voice / metadata lint fixes
8. Batch 10：ops rebuild
9. reviewer / validator verification
10. 產出 `REPAIR-REPORT.md`

## Stop Conditions

- backup 或 restore script 缺失／驗證失敗：不得進入 fix。
- refresh 顯示 UI 已漂移但無法取得當前畫面：暫停該頁的精確 UI 步驟，只修工具無關內容。
- flagship 案例無法重現：標成示意並列入 remaining，不得冒充真跑。
- 任一批次 lint 出現 BLOCKER / ERROR：停止下一批，先修回該批。
- diff 出現 scope 外檔案：停止並釐清，不順手修改。
