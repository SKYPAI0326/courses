# 數位內容與成長行銷 126h 模組化修復計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. 每個模組完成後必須通過對應驗收，不能以全課 lint 取代模組驗收。

**Goal:** 將 `digital-content-growth-126h` 從「教案原稿、學員 HTML、素材狀態彼此脫節」修復為可以逐模組跟做、驗收、回復與交接的學員教材。

**Architecture:** `_lessons/digital-content-growth-126h/*.md` 是教學內容來源；課程 HTML 是由來源重新產生的學員呈現層，不能再從既有 HTML 回讀。每個 Part 都有自己的內容實質檢查、素材檢查、冷跟做記錄與提交邊界；M0 管理來源與轉譯正確性，M1–M6 依課程順序完善內容，M7 驗收跨模組交接。

**Tech Stack:** Python 3、BeautifulSoup、Pandoc、現有 `docs/lint-page.py`、課程本機 HTML／Markdown／CSV 資產。

**Spec:** `../_outlines/digital-content-growth-126h.md`、`../_規範/course-content-substance.md`、`../_規範/learner-action-contract.md`、`courses/digital-content-growth-126h/_gates.md`。

## Global Constraints

- 學員頁只呈現學員需要的情境、概念、案例、操作、練習、驗收與備援；講師筆記、Verification Asset Spec、製作狀態不得出現在學員頁。
- 每個核心操作都要有起始材料、動作、可觀察結果、驗證與修復；只寫「完成」「檢查」「規劃」不算教學。
- 每個第一次使用的附件都要有檔名、格式、可點擊閱讀／下載入口、用途、使用時機與無權限備援。
- 不把真實廣告預算、未驗證平台帳號、正式 Search Console 權限或教師尚未準備的素材寫成 READY。
- 不使用字數、頁數、卡片數或 lint 結果代替內容實質驗收。
- 每個模組驗收前只允許修改該模組與必要的共用生成器；不得 `git add -A`，不得混入其他課程的工作樹變更。
- 每個模組提交前必須回答：學員能否開始？能否跟做？能否驗收？卡住時能否修復？任一答案為否，狀態維持 `REVISE` 或 `BLOCK`。

## 模組狀態

`DRAFT → BUILDING → MACHINE_READY → COLD_FOLLOW_PENDING → CONDITIONAL_READY → READY`

`MACHINE_READY` 只表示檔案與結構檢查通過；未完成冷跟做不得宣稱教材可販售。外部平台尚未驗證時，最多標記 `CONDITIONAL_READY`。

### Task 0: M0 來源與學員頁轉譯管線

**Files:**
- Create: `courses/digital-content-growth-126h/_tools/test_learner_render_contract.py`
- Modify: `courses/digital-content-growth-126h/_tools/rebuild-learner-shell.py`
- Verify: `courses/digital-content-growth-126h/CH5-3.html`, `courses/digital-content-growth-126h/CH6-2.html`

**Interfaces:**
- Consumes: `../_lessons/digital-content-growth-126h/{unit-id}.md`、`assets/templates/{unit-id}.md`、Part metadata。
- Produces: 可重複執行且不會遺失教學區塊的 learner-facing HTML；可指定單一 unit 進行試跑。

- [x] **Step 1: 建立內容保留的失敗測試**

  測試 `CH5-3` 的學員頁必須包含 `Search intent`、`操作示範 / Demo`、`十三步驟示範`、`檢查點與修復`、`變化題`，並包含 `assets/templates/CH5-3.html` 與 `assets/templates/CH5-3.md`。測試也必須確認 `講師授課筆記`、`Verification Asset Spec` 與 `BLOCK：待建立` 不出現在學員頁。

- [x] **Step 2: 執行測試並確認它因現況失敗**

  失敗原因必須是目前 `CH5-3.html` 缺少完整教學區塊或素材入口，而不是測試路徑錯誤。

- [x] **Step 3: 將來源改為 `_lessons` Markdown**

  在生成器中增加 Markdown 來源讀取與 Pandoc 轉換；移除講師筆記與 Verification Asset Spec 對應的完整區塊；保留 Teaching Flow、Common Pitfalls、Quiz 等學員可用內容。若獨立 Case／Hands-on 已在 Teaching Flow 完整呈現，略去重複區塊，避免同一任務在頁面堆疊兩次。不得以現有 `CH5-3.html` 或任何已生成 HTML 作為下一次生成的來源。

- [x] **Step 4: 補上來源導向的資產入口**

  以 unit id 組合模板閱讀版與 UTF-8 下載連結，不依賴正文中是否恰好存在一個既有 `<a>`。若資產不存在，頁面必須顯示可執行的文字／合成資料備援與 `BLOCK` 狀態，不得產生裸檔名。

- [x] **Step 5: 增加單元級生成入口**

  生成器提供只重建指定 unit 的方式，M0 先只輸出 `CH5-3`；第二個指定 unit `CH6-2` 用來確認不同課型仍可工作。全課批次生成只能在 M0 通過後執行。

- [x] **Step 6: 重新執行測試與人工內容抽查**

  確認測試通過，並實際閱讀 `CH5-3`：學員能看見情境、概念、完整示範、起始材料、操作步驟、變化題、驗收與修復；確認生成前後沒有內部製作資訊。

- [x] **Step 7: M0 放行判斷**

  測試、兩個代表頁的起始材料與附件入口、教學標題保留、重複區塊移除、內部語句過濾、Markdown 粗體修復均已通過；M0 標記 `MACHINE_READY`。這不代表全課可販售，也不代表已完成冷跟做；M0 未通過前沒有批量重建。

### Task 1: M1 Part 1 共同 Brief 與能力方向

**Status:** `MACHINE_READY`；人工冷跟做記錄見 `courses/digital-content-growth-126h/_review/M1-cold-follow.md`，完成前不升級為 `CONDITIONAL_READY` 或 `READY`。

**Files:**
- Modify: `../_lessons/digital-content-growth-126h/CH1-1.md`, `CH1-2.md`, `CH1-3.md`, `PRAC1.md`
- Generate: `courses/digital-content-growth-126h/CH1-1.html`, `CH1-2.html`, `CH1-3.html`, `PRAC1.html`
- Create: `courses/digital-content-growth-126h/_review/M1-cold-follow.md`

**Acceptance:** 四頁能從學員專長開始，完成應用情境、受眾問題、價值主張與共同 Brief；至少一份完整示範 Brief、一份完整參考答案、清楚的下一單元交接；不以創業作為唯一出口。

### Task 2: M2 Part 2 影像與影片編修

**Status:** `MACHINE_READY`（文字工作流與附件入口）；人工冷跟做 `PENDING`；Affinity／OpenShot 實機、可編輯來源檔與影音示範維持 `BLOCK`。證據見 `courses/digital-content-growth-126h/_review/M2-cold-follow.md`。

**Files:**
- Modify: `../_lessons/digital-content-growth-126h/CH2-1.md`–`CH2-7.md`, `PRAC2.md`
- Generate: 對應 8 個 learner-facing HTML、20 個附件閱讀版
- Create: `courses/digital-content-growth-126h/_review/M2-cold-follow.md`

**Current evidence:** 6 項內容契約測試通過；26 個 M2 主頁／附件頁本地連結、內部語句洩漏與重複標題檢查通過。文字模板、案例卡、格式卡、來源／AI 紀錄、課前檢查、輸出檢核與評量規準已建立；工具版本與實際影音仍未驗證。

**Acceptance:** Affinity、素材取得、剪輯判斷與 OpenShot 各有完整輸入到輸出的示範；Windows 教室有安裝／版本／素材備援；學員能交付短影音、平面資產、來源紀錄與行銷判斷。

### Task 3: M3 Part 3 社群媒體經營

**Status:** `MACHINE_READY`（文字工作流與附件入口）；人工冷跟做 `PENDING`；當期平台介面、正式去識別資料包與人工發布維持 `BLOCK`／待驗證。證據見 `courses/digital-content-growth-126h/_review/M3-cold-follow.md`。

**Files:**
- Modify: `../_lessons/digital-content-growth-126h/CH3-1.md`–`CH3-7.md`, `PRAC3.md`
- Generate: 對應 8 個 learner-facing HTML、22 個附件閱讀版
- Create: `courses/digital-content-growth-126h/_review/M3-cold-follow.md`

**Current evidence:** 8 項內容契約測試通過；30 個 M3 主頁／附件頁本地連結、內部語句洩漏與重複標題檢查通過。平台角色、內容支柱、跨平台改編、月曆、互動風險、合成資料、LINE 情境與整合評量資產已建立；正式資料與平台前測尚未完成。

**Acceptance:** IG／FB／Threads 的平台判斷有差異化案例；LINE 只作延伸承接；內容月曆、互動風險與成效紀錄有可填示例和參考完成品。

### Task 4: M4 Part 4 SEO 與網站行為追蹤

**Status:** `MACHINE_READY`（文字工作流、合成資料與附件入口）；人工冷跟做 `PENDING`；LocalWP／GTM／GA4 權限、實站與 Search Console 資料仍 `BLOCK`／待驗證。證據見 `courses/digital-content-growth-126h/_review/M4-cold-follow.md`。

**Files:**
- Modify: `../_lessons/digital-content-growth-126h/CH4-1.md`–`CH4-7.md`, `PRAC4.md`
- Generate: 對應 8 個 learner-facing HTML、25 個附件閱讀版
- Create: `courses/digital-content-growth-126h/_review/M4-cold-follow.md`

**Current evidence:** 10 項內容契約測試通過；33 個 M4 主頁／附件頁本地連結、內部語句洩漏與重複標題檢查通過。搜尋意圖、關鍵字、LocalWP 檢查、GA4 閱讀／假設、GTM 事件、追蹤驗證、Search Console 合成資料與決策包資產已建立；外部權限與實機仍未驗證。

**Acceptance:** LocalWP、GA4 Demo、GTM 與 GSC 合成資料路徑分開說明；每個事件有事件名稱、參數、觸發條件、可見結果、驗證與修復；LocalWP 不被寫成正式收錄證據。

### Task 5: M5 Part 5 國際數位廣告投放

**Status:** `MACHINE_READY`（企劃工作流、合成資料與附件入口）；人工冷跟做 `PENDING`；平台帳號、介面示範、試算表檔案與真實投放維持 `BLOCK`／不列必要條件。證據見 `courses/digital-content-growth-126h/_review/M5-cold-follow.md`。

**Files:**
- Modify: `../_lessons/digital-content-growth-126h/CH5-1.md`–`CH5-7.md`, `PRAC5.md`
- Generate: 對應 8 個 learner-facing HTML、26 個附件閱讀版
- Create: `courses/digital-content-growth-126h/_review/M5-cold-follow.md`

**Current evidence:** 12 項內容契約測試通過；34 個 M5 主頁／附件頁本地連結、內部語句洩漏與重複標題檢查通過。市場選擇、渠道漏斗、Google／Meta／LINE 企劃、預算公式與護欄、兩輪決策與整合評量資產已建立；真實平台與試算表檔案未驗證。

**Acceptance:** 至少一個平台有完整深度路徑；另一平台有轉譯邏輯；合成資料包含 Round 1／Round 2、欄位定義與參考判讀；學員能完成投放包、預算表與 pause／scale／iterate 決策，不需要信用卡或真實廣告預算。

### Task 6: M6 Part 6 能力整合與提案

**Status:** `MACHINE_READY`（整合工作流、文字示例與附件入口）；人工冷跟做 `PENDING`；正式簡報／紙本包與實際外部讀者回饋仍待確認。證據見 `courses/digital-content-growth-126h/_review/M6-cold-follow.md`。

**Files:**
- Modify: `../_lessons/digital-content-growth-126h/CH6-1.md`–`CH6-3.md`, `PRAC6.md`
- Generate: 對應 4 個 learner-facing HTML
- Create: `courses/digital-content-growth-126h/_review/M6-cold-follow.md`

**Acceptance:** 前五個 Part 的產物有實際輸入欄位與交接位置；完成物包括整合企劃、提案、能力證據與 30 天行動表；提供完整參考提案與共同評量規準。

**Current evidence:** 15 項內容契約測試通過；4 個 M6 主頁與 17 個附件頁本地連結、內部語句洩漏與重複標題檢查通過；核心頁教學階段結構檢查通過。上游產物摘要、價值主張、方案範圍、能力證據、30 天行動、證據矩陣與提案評量資產已建立；DOCX／PDF／PPTX／試算表等正式交付格式與人工提案尚未驗證。

### Task 7: M7 跨模組整合與提交

**Status:** `MACHINE_READY / COLD_FOLLOW_PENDING`；本輪不 push、不宣稱可販售。人工冷跟做入口與目前邊界見 `courses/digital-content-growth-126h/MANUAL-LEARNER-RUN.md`、`courses/digital-content-growth-126h/_repair/2026-09-16/REPAIR-REPORT.md`。

**Files:**
- Modify: `courses/digital-content-growth-126h/MANUAL-LEARNER-RUN.md`, `VALIDATION-REPORT.md`, `_gates.md`
- Verify: 全課 47 個核心頁面與 40 個資產閱讀版

**Acceptance:** 完成入口到 PRAC6 的三單元微序列、跨模組產物交接、素材連結、Windows／fallback、內容 substance、連結與部署檢查；所有未完成外部條件仍明確標記，未把 CONDITIONAL_READY 寫成 READY。

**Current evidence:** 173 個發布範圍 HTML 通過本地連結檢查（0 failures）、內部製作語句檢查（0 leaks）與核心單元重複 h2 檢查（0 pages）；40 個核心頁教學階段均可定位；課程 lint BLOCKER 0、ERROR 0、WARN 127（附件頁通用規則提醒 126 頁，另有 1 個 callout 提醒）；搜尋索引 878 筆、sitemap 253 個 URL；回歸測試 15 tests OK。人工學員試跑、外部平台實機、正式 Office／PDF／簡報格式與 M6 口頭提案仍未驗證，因此不升級為 `CONDITIONAL_READY` 或 `READY`。

## 每個模組的固定驗收順序

1. 先讀來源教案與上游產物，列出本模組的核心概念與核心操作。
2. 建立或修正完整示範與參考完成品。
3. 產生 learner-facing HTML，檢查來源內容沒有遺失。
4. 檢查首次使用的資產入口與備援。
5. 做機器檢查：連結、HTML 結構、必要詞彙、內部筆記洩漏、內容區塊存在。
6. 做冷跟做：只使用入口、該模組頁面與列出的資產，不讀教案 Markdown。
7. 記錄 PASS／REVISE／BLOCK 與證據位置。
8. 模組通過後才提交與推送；未通過只保留本地修正，不宣稱完成。

## 本輪執行邊界

本輪已完成 M0–M6 的來源轉譯、模組內容與學員資產修復；M1–M6 均維持 `MACHINE_READY` 並等待人工冷跟做。M7 的機器整合驗收已完成，但人工試跑、外部平台實機與正式販售格式仍未驗證；因此本輪不 push、不宣稱整包課程已可販售或正式上線。
