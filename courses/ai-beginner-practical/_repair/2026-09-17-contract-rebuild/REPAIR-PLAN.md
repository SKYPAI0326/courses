# AI 入門即戰力 Learner Contract Rebuild Implementation Plan

> **For agentic workers:** This plan follows the course-repair and learner-action-contract gates. Each task ends with a checkable artifact and a rerun of the relevant validation layer.

**Goal:** 將四個現有單元重整為符合 `learner-action-contract.md` 的完整零基礎 learner-facing handout，保留既有案例與提示詞實質，讓學員能從真實問題、可取得材料與第一個動作走到可保存、可驗收、可再利用的完成物。

**Architecture:** 以四份 Lesson Plan 作為契約與教學事實來源，HTML 只呈現已凍結的契約與完整示範。每頁在第一個工具動作前呈現八欄契約摘要，後續依「情境／材料／完成物 → 概念 → 完整示範 → 同步操作 → 單一變因轉移 → 驗收／修復／下一次使用」串接。資產連結保留可開啟的課程檔案，並以一致的 HTML wrapper 解決舊稽核器對裸 Markdown href 的誤判。

**Tech Stack:** Markdown lesson plans、learner-facing HTML、共用 CSS、既有 `lint-page.py`、`audit-course-substance.py`、cold-follow contract、learner-agent manifest。

**Spec:** `../_規範/learner-action-contract.md`、`../_規範/course-content-substance.md`、`../../.agents/skills/course-handout-designer/references/lesson-type-contract.md`、`../../.agents/skills/course-handout-designer/references/beginner-continuity-gate.md`。

## Global Constraints

- 唯一學員路徑契約為 `../_規範/learner-action-contract.md`，不新增第二套契約名稱。
- NotebookLM 是唯一固定平台；其他 LLM 以平台中立的文字對話工具呈現。
- 保留既有課程四單元、12 小時、生活化案例與課後整合產物，不新增資安專題。
- 每個 skill-operation 單元保留 5–12 個有意義階段、每 3–5 步至少一個 checkpoint、完整 worked example、單一變因轉移與可修復驗收。
- 不以 lint、manifest 或作者摘要取代 learner cold-read、NotebookLM 實機與真人證據；缺少證據維持 `PENDING_HUMAN`。
- 本輪只修改 `ai-beginner-practical` scope，保留工作樹中其他課程與既有未提交變更。

---

### Task 1: 建立可回復基線與契約來源

**Files:**
- Create: `ai-beginner-practical/_backup/2026-09-17-pre-contract-rebuild/`（本輪 scope 的既有檔案副本）
- Create: `ai-beginner-practical/_tools/restore-2026-09-17-pre-contract-rebuild.sh`
- Create: `ai-beginner-practical/_repair/2026-09-17-contract-rebuild/SCAN.md`
- Modify: `ai-beginner-practical/COURSE-BLUEPRINT.md`
- Modify: `ai-beginner-practical/COVERAGE-LEDGER.md`

**Interfaces:**
- Consumes: 四份既有教案、四個 learner-facing HTML、課程規範與現有 assets。
- Produces: 具體的四單元八欄契約矩陣、契約→教案→HTML→驗證責任鏈與可還原版本。

- [ ] **Step 1:** 核對 backup 副本與目標檔案 SHA-256 一致。
- [ ] **Step 2:** 在 Blueprint 增加四單元八欄契約與 micro-sequence 的實際檔名／完成物映射。
- [ ] **Step 3:** 在 Coverage Ledger 補齊 CH2–CH4 與 CAP 的 raw input、learner action、finished artifact、verification、repair 證據欄位，保留既有 atom ID。
- [ ] **Step 4:** 寫入 scan，逐項列出現有分散契約、orientation 失敗、資產連結與行動路徑問題。
- [ ] **Step 5:** 執行 `bash -n ai-beginner-practical/_tools/restore-2026-09-17-pre-contract-rebuild.sh`。

### Task 2: 在四份教案凍結八欄契約與教學因果

**Files:**
- Modify: `ai-beginner-practical/CH1-1-LESSON-PLAN.md`
- Modify: `ai-beginner-practical/CH2-1-LESSON-PLAN.md`
- Modify: `ai-beginner-practical/CH3-1-LESSON-PLAN.md`
- Modify: `ai-beginner-practical/CH4-1-LESSON-PLAN.md`

**Interfaces:**
- Consumes: Task 1 的矩陣、既有 worked examples、assets、課程大綱。
- Produces: 每份教案在第一個操作前明確包含角色／問題後果／材料／完成物／下一位使用者／第一動作／第一結果／失敗回復，且每次轉段都有結果—目的承接。

- [ ] **Step 1:** 在每份教案 frontmatter 後加入唯一標題 `## Learner Task Contract（學員任務契約）`，不另造第二套 checklist。
- [ ] **Step 2:** 以該單元既有真實案例填八欄，不使用 placeholder；明確列檔名、格式、保存位置、下一單元用途與安全停止狀態。
- [ ] **Step 3:** 對照 Core Operation Inventory，確認每一個核心操作都有輸入、動作、中間結果、完成品、驗證與修復。
- [ ] **Step 4:** 跑 Markdown 的 continuity、teaching-evidence 與 frontmatter 檢查；把缺口修回教案，不在 HTML 臨場發明內容。

### Task 3: 將四個內容頁重建為可獨立閱讀的完整講義

**Files:**
- Modify: `ai-beginner-practical/CH1-1.html`
- Modify: `ai-beginner-practical/CH2-1.html`
- Modify: `ai-beginner-practical/CH3-1.html`
- Modify: `ai-beginner-practical/CH4-1.html`
- Create: `ai-beginner-practical/assets/templates/unit2-communication-scenarios.html`

**Interfaces:**
- Consumes: Task 2 教案契約、既有 HTML 組件與完整 assets。
- Produces: 每頁在第一個工具動作前即可回答 30 秒入口六題；正文保留完整輸入／處理／中間結果／完成品、同步步驟、checkpoint、轉移、驗收與修復。

- [ ] **Step 1:** 將每頁開場的三欄材料表改為八欄契約呈現，保留同一份完成物與資產連結，不重複造故事卡。
- [ ] **Step 2:** 為 CH2 建立可直接開啟／複製的 HTML 素材頁，並在第一次使用前明確說明用途、時機與 Markdown 失效時的備援。
- [ ] **Step 3:** 修補所有主要轉段，使正文直接說明「剛才完成或看見了什麼，所以現在做什麼，目的是什麼」。
- [ ] **Step 4:** 保留每單元既有 5–12 個 meaningful stages；不以增加標籤、卡片或重複提示詞灌水。
- [ ] **Step 5:** 補強手機窄版的密集表格閱讀方式，確保表格不把整頁撐出水平捲動；桌面版仍保留欄位可讀性。

### Task 4: 反覆驗收與修復

**Files:**
- Create: `ai-beginner-practical/_repair/2026-09-17-contract-rebuild/REVIEW-REPORT.md`
- Create: `ai-beginner-practical/_repair/2026-09-17-contract-rebuild/COLD-FOLLOW-REPORT.md`
- Modify: `ai-beginner-practical/_validation/learner-agent/evidence-manifest.json`（由既有工具重建）
- Modify: `../search-index.json`（由既有建置工具重建）

**Interfaces:**
- Consumes: Task 3 的四個 HTML、所有 linked assets、既有驗證腳本。
- Produces: 機械、語意、資產、手機版與冷讀證據；明確分開 `MACHINE_CHECKED`、`LEARNER_READ`、`PLATFORM_VERIFIED`、`HUMAN_READY`。

- [ ] **Step 1:** 跑四頁 `lint-page.py` 正確路徑與 `audit-course-substance.py`，所有 substance BLOCKER 必須清零。
- [ ] **Step 2:** 跑 cold-follow、UI practicality、L0、manifest contract 與 asset link resolution。
- [ ] **Step 3:** 執行手機窄版 DOM 寬度檢查，確認 CH1、CH2、CH3、CH4 無 body-level horizontal overflow。
- [ ] **Step 4:** 以 learner-facing 頁面和列出的 assets 做一次從入口到完成物的冷讀；記錄六題入口答案、到第一個 checkpoint 時間、停住位置與回修契約欄位。
- [ ] **Step 5:** 若任一檢查失敗，依「契約缺漏／產出遺失／呈現遺失／驗證遺失」回修唯一責任層，再重跑失敗層與全課回歸。
- [ ] **Step 6:** 只有機器、冷讀與適用平台證據全數到位才可標示 `READY`；否則報告為 `MACHINE_READY_PENDING_HUMAN` 或 `CONDITIONAL`。

## Self-review

- 已涵蓋八欄契約、因果鏈、30 秒入口、資產可發現性、完整 worked example、5–12 stages、checkpoint、單一變因轉移、驗收與回修。
- 沒有使用 TBD、TODO 或「之後補」作為步驟內容。
- 未修改其他課程，也不以檢核器通過代替 NotebookLM 實機或真人冷讀。
