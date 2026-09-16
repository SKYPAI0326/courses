# UI/UX Figma 免費瀏覽器課程完整製作與驗證計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立一門接近零基礎學員只靠講義、素材與免費 Figma 瀏覽器版即可從零完成的 UI/UX 課程，並保存從實機測試、檔案製作、教案、HTML、真人跟做到發行維護的完整證據鏈。

**Architecture:** 先鎖定 Figma Starter＋Chrome 的 Environment Contract，再用 Computer Use 逐原子步驟測試功能；測試結果回寫 Blueprint、Core Operation Inventory、Coverage Ledger 與時間帳本。每一個正式單元都由「教案 → 素材包 → learner-facing HTML → 靜態檢查 → Chrome/Figma 真跑 → 冷跟做紀錄」組成，任何一層失敗就回到對應上游修補。

**Tech Stack:** Figma Starter（瀏覽器版）、Chrome、Photoshop（僅在正式範圍需要且已驗證時使用）、VS Code、HTML/CSS、最小 JavaScript、Git/GitHub、Markdown、既有課程 lint／內容實質／驗收工具、Computer Use。

**Spec:** `uiux-designer/_design/2026-09-07-99h-course-rescope-design.md`、`uiux-designer/_design/FIGMA-STARTER-BROWSER-AUDIT.md`、`uiux-designer/_gates.md`

## Global Constraints

- 課程正式範圍維持 42h「介面元素與設計」＋57h「UI/UX 原型製作與資料打包」；未經實測不得鎖定 99h 內部單元時數。
- 必修工具基線為 Figma Starter 免費方案＋Chrome 瀏覽器；付費限定能力移出必修主線並標示條件。
- Git/GitHub 是必要交付流程，但不擴張成獨立 Git 課程；JavaScript 只保留最小網頁成果所需能力。
- 每一個核心操作必須有：起始狀態、實際輸入、操作、可見結果、驗證、常見失敗與修復。
- 每一個學員會使用的檔案、文字、圖片、完成品與替代路徑都必須在第一次使用前可取得。
- 每一個單元都必須留下可檢查完成物，並標明下一單元如何使用它。
- 沒有真人試跑證據時，狀態只能是 `NOT_RUN`、`BLOCK` 或 `DRAFT`，不得寫成 `PASS`。
- 不修改其他課程工作樹變更；不使用 `git add -A`；每次提交只包含本計畫明列的檔案。

## 人力不足時的分工

| 工作 | Skills／Codex 可自動處理 | Computer Use／使用者必須處理 |
|---|---|---|
| 課程藍圖、依賴鏈、時數、教案結構 | 建立、比對、靜態檢查 | Gate 判斷與課程取捨 |
| Figma 操作路徑 | 整理官方文件、產生測試腳本、分析紀錄 | 在 Chrome 的實際帳號操作與確認畫面 |
| 檔案與講義 | 產生 Markdown、素材索引、HTML、lint | 確認視覺呈現與是否適合學員 |
| 真跑驗證 | 讀取頁面、比對證據、產生報告 | 實際跟做、回報卡點、批准 PASS |
| 維護 | 掃描版本日期、連結與內容漂移 | 重新登入、權限、方案與 UI 變化確認 |

---

### Task 1：鎖定課程環境與證據格式

**Files:**
- Create: `uiux-designer/_design/ENVIRONMENT-CONTRACT.md`
- Create: `uiux-designer/_design/EVIDENCE-SCHEMA.md`
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: Figma Starter 免費方案、Chrome 瀏覽器、現有 `FIGMA-STARTER-BROWSER-AUDIT.md`。
- Produces: 可供教案、Computer Use、HTML 與驗收共用的環境欄位與證據格式。

- [ ] **Step 1：記錄起始環境**

寫入方案、瀏覽器、確認日期、帳號角色、是否能建立／編輯檔案、開始頁面、不可使用的付費功能與無權限備援。

- [ ] **Step 2：固定證據欄位**

每筆測試至少包含：`probe_id`、`step_id`、日期、操作前狀態、使用者動作、可見結果、截圖或頁面證據、預期結果、實際結果、判定、修復、下一步。

- [ ] **Step 3：追加 G1 阻塞紀錄**

不覆寫既有 Gate；追加目前仍缺少實機證據、不得產製正式講義的原因與下一個可執行步驟。

- [ ] **Step 4：檢查文件格式**

```bash
git diff --check
rg -n 'Figma Starter|Chrome|NOT_RUN|PASS|BLOCK|fallback|step_id' uiux-designer/_design/ENVIRONMENT-CONTRACT.md uiux-designer/_design/EVIDENCE-SCHEMA.md uiux-designer/_gates.md
```

Expected: 所有核心欄位都有定義，未把推測寫成測試結果。

### Task 2：用 Computer Use 執行 Figma 實機 Probe A

**Files:**
- Create: `uiux-designer/_validation/figma-starter-browser/PROBE-A.md`
- Create: `uiux-designer/_validation/figma-starter-browser/README.md`
- Modify: `uiux-designer/_design/FIGMA-STARTER-BROWSER-AUDIT.md`

**Interfaces:**
- Consumes: `ENVIRONMENT-CONTRACT.md`、Chrome 中實際 Figma 帳號、原子步驟規則。
- Produces: 介面系統與內容壓力的實機結果。

- [ ] **Step 1：使用者在 Chrome 開啟 Figma 並停在可操作畫面。**
- [ ] **Step 2：Codex 只給一個動作；使用者執行後回報「完成」或描述畫面。**
- [ ] **Step 3：Codex 讀取畫面，記錄該步證據，再給下一個動作。**
- [ ] **Step 4：建立手機 Frame 與一個最小登入／清單案例。**
- [ ] **Step 5：測試長中文、空狀態、錯誤狀態、增刪項目、Auto Layout 與 Component。**
- [ ] **Step 6：遇到失敗時記錄現象、回復位置與是否能繼續，不用口頭推定成功。**
- [ ] **Step 7：保存可重開檔案位置、結果與限制；不分享、不刪除正式檔。**

判定：`PASS`、`CONDITIONAL`、`BLOCK`、`NOT_RUN` 四選一；任何一個核心操作沒有證據就不能放行 A1–A7。

### Task 3：執行 Figma 實機 Probe B 與 C

**Files:**
- Create: `uiux-designer/_validation/figma-starter-browser/PROBE-B.md`
- Create: `uiux-designer/_validation/figma-starter-browser/PROBE-C.md`
- Modify: `uiux-designer/_design/FIGMA-STARTER-BROWSER-AUDIT.md`

**Interfaces:**
- Consumes: Probe A 可重開檔案與證據格式。
- Produces: Prototype、輸出、交付與部署的可行性結果。

- [ ] **Step 1：Probe B 測試觸發、互動連結、轉場、Overlay、Swap、Scroll、固定元素與 Smart Animate。**
- [ ] **Step 2：Probe B 每一項都在 Preview 實際觸發一次，記錄可見結果與失敗修復。**
- [ ] **Step 3：Probe C 測試 PNG／JPG／PDF 匯出、分享權限、Inspect 與資產命名。**
- [ ] **Step 4：Probe C 以同一成果完成最小 HTML/CSS、Git commit、GitHub 版本紀錄與公開部署測試。**
- [ ] **Step 5：分開記錄 Figma 能力與外部交付能力，不把 Git/GitHub 假裝成 Figma 功能。**

放行：B8 與網頁交付只能使用 C 中 `PASS` 或明確標示 `CONDITIONAL` 的能力。

### Task 4：建立 Course Blueprint、Core Operation Inventory 與 Coverage Ledger Pass 1

**Files:**
- Create: `uiux-designer/_design/COURSE-BLUEPRINT.md`
- Create: `uiux-designer/_design/CORE-OPERATION-INVENTORY.md`
- Create: `uiux-designer/_design/COVERAGE-LEDGER-PASS1.md`
- Modify: `../_outlines/uiux-designer.md`
- Modify: `uiux-designer/_design/99h-coverage-matrix.md`
- Modify: `uiux-designer/_design/99h-time-ledger.md`

**Interfaces:**
- Consumes: Probe A/B/C 結果、正式課綱圖片、既有 42h／57h coverage。
- Produces: 可追溯的學員故事、產物依賴圖、核心操作清單、學習原子清單與修正後大綱。

- [ ] **Step 1：為每個單元寫學員故事。**

明確寫出學員角色、工作情境、起始材料、可見完成物、下一個使用者與能力改變。

- [ ] **Step 2：建立 Artifact Dependency Graph。**

每條鏈都使用「前一份產物 → 本單元輸入 → 本單元產物 → 下一次使用 → Capstone 元件」。

- [ ] **Step 3：建立 Core Operation Inventory。**

每個無法安全推測的操作都列出輸入、動作、可見結果、驗證與修復。

- [ ] **Step 4：凍結 Coverage Ledger Pass 1。**

先列 atom ID、分類、操作 ID、必要證據，不因教案寫不出來而刪除或降級。

- [ ] **Step 5：依實測結果重配單元與時數。**

保留正式 42h／57h 邊界，但不強迫 16-stage 一對一切分；付費或不穩定功能改為限定情境、選修或刪除。

- [ ] **Step 6：使用者 Gate 審核。**

使用者確認學員成果、砍除項目、工具限制與單元順序後，才進入教案。

### Task 5：製作代表單元教案與素材包

**Files:**
- Create: `../_lessons/uiux-designer/<pilot-id>.md`
- Create: `uiux-designer/assets/<pilot-id>/START-HERE.md`
- Create: `uiux-designer/assets/<pilot-id>/source/`
- Create: `uiux-designer/assets/<pilot-id>/reference/`
- Create: `uiux-designer/assets/<pilot-id>/expected/`
- Create: `uiux-designer/_review/<pilot-id>-TRIAL.md`

**Interfaces:**
- Consumes: Gate 1 核准後的 Blueprint、Operation Inventory、Coverage Ledger Pass 1、Figma 實機結果。
- Produces: 不依賴講師補充的完整教案、起始材料、參考完成品、失敗夾具與真人試跑記錄表。

- [ ] **Step 1：以零基礎入口寫情境、已有材料、目標產物、第一個動作與第一個可觀察結果。**
- [ ] **Step 2：為核心操作提供完整 worked example：原始輸入、中間結果、判斷理由、完成品、正誤比較。**
- [ ] **Step 3：寫 5–12 個有意義操作階段；每 3–5 步有 Checkpoint。**
- [ ] **Step 4：每個主要階段補觀察到的錯誤、回到哪裡修、從哪裡重跑與安全停止狀態。**
- [ ] **Step 5：提供一個只改一個主要變因的變化練習。**
- [ ] **Step 6：在素材第一次使用前寫檔名／格式／取得方式／用途／備援。**
- [ ] **Step 7：完成 `COVERAGE-LEDGER-PASS1` 對應的第一批 evidence，未完成的維持 `BLOCK`。**

### Task 6：用講義設計器產製代表 HTML

**Files:**
- Create: `uiux-designer/<pilot-id>.html`
- Create: `uiux-designer/_review/<pilot-id>-HTML-REVIEW.md`
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: 已通過實質審查的代表教案、素材包、style guide。
- Produces: 完整 learner-facing HTML 與頁面證據。

- [ ] **Step 1：保留完整教學原子，不以標籤卡片取代解釋。**
- [ ] **Step 2：確認講義可在 Blueprint 隱藏時獨立閱讀。**
- [ ] **Step 3：執行頁面 lint、連結檢查、資產檢查與手機寬度檢查。**
- [ ] **Step 4：做 Label Removal Test；移除 Demo／Together／Solo／Check 標籤後正文仍可理解。**
- [ ] **Step 5：只在靜態內容與代表頁驗收通過後才考慮批次產製。**

### Task 7：完成 Chrome／Figma 冷跟做與三課微序列

**Files:**
- Create: `uiux-designer/_review/G3-CONTENT-REVIEW.md`
- Create: `uiux-designer/_review/COLD-FOLLOW-ALONG/<run-id>.md`
- Create: `uiux-designer/_review/ARTIFACT-CHAIN-3-LESSONS.md`
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: 代表 HTML、列出的素材、Chrome 與 Figma Starter 實際帳號。
- Produces: 使用者跟做證據、卡點分類、學員產物鏈與 Gate 3 判定。

- [ ] **Step 1：使用者只拿講義與素材，不讀 Blueprint、不接受口頭補充。**
- [ ] **Step 2：記錄開始／結束時間、第一次卡住位置、提示次數、錯誤現象與完成品。**
- [ ] **Step 3：若卡住，先記錄再修講義；不以講師即時提示填平缺口。**
- [ ] **Step 4：跑三個相連單元，確認前一單元產物真的被下一單元使用。**
- [ ] **Step 5：只有 `reviewed_by: user` 且 `three_minute_follow_test: PASS` 才能放行同 Part。**

### Task 8：按 Part 批次製作並回填 Coverage Ledger Pass 2

**Files:**
- Create: `../_lessons/uiux-designer/<unit-id>.md`
- Create: `uiux-designer/<unit-id>.html`
- Modify: `uiux-designer/_design/COVERAGE-LEDGER-PASS2.md`
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: 代表單元 Gate 3 PASS、修正後 Blueprint、素材規格與 artifact chain。
- Produces: 全部單元教案、HTML、素材包、每個 atom 的實際證據位置。

- [ ] **Step 1：先完成同一 Part，再執行該 Part 的 lint 與 substance audit。**
- [ ] **Step 2：逐單元核對起始狀態、完成物、同步演練、Checkpoint、變化練習與修復。**
- [ ] **Step 3：把每個 Pass 1 atom 回填到實際 HTML／教案位置、引用證據、產物、驗證與修復。**
- [ ] **Step 4：發現 atom ID 或分類改變時，追加書面原因與 reviewer verdict，不靜默改動。**
- [ ] **Step 5：確認所有正式課綱項目仍有對應完成物與驗收證據。**

### Task 9：執行完整驗證與發行前收尾

**Files:**
- Create: `uiux-designer/_validation/FINAL-REPORT.md`
- Create: `uiux-designer/_validation/evidence-manifest.json`
- Create: `uiux-designer/_validation/<case-study>.md`
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: 全部 learner-facing HTML、素材、Figma 真跑記錄、冷跟做記錄與 Coverage Ledger Pass 2。
- Produces: 分層驗證報告、證據 manifest、修補清單與可否交付判定。

- [ ] **Step 1：跑 preflight 與 Content Substance audit。**
- [ ] **Step 2：跑 L1–L3 靜態、骨架、數字與連結檢查。**
- [ ] **Step 3：跑 L4a 案例真跑；每個核心案例都要使用實際頁面與素材。**
- [ ] **Step 4：跑 L4b Figma／Chrome 平台 sentinel，確認免費方案與介面變化不會讓路徑失效。**
- [ ] **Step 5：跑 L5 persona journey 與課後落地檢查；manifest 必須含檔案 hash 與可見文字 hash。**
- [ ] **Step 6：若出現「不知道下一步、缺預期畫面、無法自行檢查、只能靠講師補充」，回修 designer／HTML／reviewer 上游並重跑該層。**
- [ ] **Step 7：只有所有硬門檻通過且使用者確認，才標記課程可交付。**

### Task 10：建立維護與版本漂移流程

**Files:**
- Create: `uiux-designer/_maintenance/DRIFT-CHECK.md`
- Create: `uiux-designer/_maintenance/CHANGELOG.md`
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: Figma／Chrome 實測日期、官方說明、歷次驗收報告與學員問題。
- Produces: 可由少量人力重跑的更新流程。

- [ ] **Step 1：記錄 Figma 方案、介面、官方文件與驗證日期。**
- [ ] **Step 2：每次更新先重跑代表 Probe A/B/C，不直接批次改全部講義。**
- [ ] **Step 3：若操作名稱、方案限制、匯出或分享改變，標記受影響 atom／單元／HTML。**
- [ ] **Step 4：重跑代表單元冷跟做，再決定是否批次修正。**
- [ ] **Step 5：保存變更原因、證據、修補與回復版本。**

## 完成定義

課程只有在以下條件全部滿足時，才可宣稱完成：

- [ ] Figma Starter＋Chrome 的 Environment Contract 有實測證據。
- [ ] 三組 Probe 都不是 `NOT_RUN`；付費或不穩定功能已分流。
- [ ] Blueprint、Core Operation Inventory、Coverage Ledger Pass 1／2 完整且互相可追溯。
- [ ] 每個正式單元都有教案、可取得素材、完整 learner-facing HTML 與可驗收完成物。
- [ ] 代表單元與三課微序列通過真人冷跟做。
- [ ] 靜態檢查、內容實質檢查、平台真跑、persona journey 與證據 manifest 全部完成。
- [ ] `_gates.md` 有使用者 Gate 判定；未經使用者判定不得標記 `PASS`。
- [ ] 維護檔案能讓下一位製作者知道何時、如何重跑 Figma 測試。

## 第一個實際動作

本計畫不先產製講義。下一個原子步驟是：由使用者在 Chrome 開啟 Figma，Codex 讀取當前畫面，然後只執行 Probe A 的第一個可回復動作。
