# ICT AI Digital Workflow Course Pipeline Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 `ict-ai-digital-workflow` 從已核准大綱與五章教案，製作成可驗證、免費工具優先、可部署但尚未正式上線的完整課程網站。

**Architecture:** `_outlines/` 是課程定位來源，`_lessons/` 是教學內容來源，`courses/ict-ai-digital-workflow/` 存放總覽頁、五章 HTML、試跑素材、Gate 與驗證證據。每章從同一套 V4 模板產生，先個別 lint，再做跨頁導覽、語意、完整性與全站建置檢查。

**Tech Stack:** Markdown、HTML5、inline CSS、原生 JavaScript、Python 專案驗證工具。

## Global Constraints

- 課程總時數固定 300 分鐘：CH1 50、CH2 70、CH3 70、CH4 70、CH5 40。
- 核心路徑只能依賴免費帳號；不得要求信用卡、試用期、付費專屬功能或管理員權限。
- 學員可單人完成；同儕互評或小組發表不得成為必要條件。
- 每章必須保留 Learner Action Contract、Checkpoint、卡關修復與離線／固定輸出備援。
- HTML 必須通過 `docs/lint-page.py`；不得以 grep 取代頁面合規 lint。
- 不執行 commit、push、course-register 或公開部署，除非使用者另行授權。

---

### Task 1: Pipeline governance and source lock

**Files:**
- Create: `courses/ict-ai-digital-workflow/_plan.md`
- Create: `courses/ict-ai-digital-workflow/_gates.md`
- Read: `_outlines/ict-ai-digital-workflow.md`
- Read: `_lessons/ict-ai-digital-workflow/CH1.md` through `CH5.md`

**Interfaces:**
- Consumes: G1-approved outline and G2 lesson plans.
- Produces: auditable gate state and execution checklist.

- [x] Record G1 user answers and free-tool constraint.
- [x] Verify five lessons contain required fields, sections, steps, checkpoints and 300 total minutes.
- [x] Record G2 evidence review without representing inferred judgments as user quotations.

### Task 2: Build five lesson pages

**Files:**
- Create: `courses/ict-ai-digital-workflow/CH1.html`
- Create: `courses/ict-ai-digital-workflow/CH2.html`
- Create: `courses/ict-ai-digital-workflow/CH3.html`
- Create: `courses/ict-ai-digital-workflow/CH4.html`
- Create: `courses/ict-ai-digital-workflow/CH5.html`

**Interfaces:**
- Consumes: matching `_lessons/ict-ai-digital-workflow/CHN.md`, outline frontmatter, `_outlines/_style_guide_template.md`, `_規範/lesson-template-v3.html`.
- Produces: learner-facing V4 HTML pages with sequential navigation.

- [x] Build each page from the matching lesson plan without including lecturer-only notes.
- [x] Preserve explicit learner operations, expected results, checkpoints and stuck recovery.
- [x] Add platform metadata and `data-built-at="2026-08-04"`.
- [x] Run `python3 docs/lint-page.py courses/ict-ai-digital-workflow/CHN.html` after each page.

### Task 3: Build course overview and trial assets

**Files:**
- Create: `courses/ict-ai-digital-workflow/index.html`
- Create: `courses/ict-ai-digital-workflow/assets/` trial files required by CH1–CH5.

**Interfaces:**
- Consumes: outline outcomes, unit matrix and each lesson's verification asset spec.
- Produces: course navigation, learner deliverables and no-account fallbacks.

- [x] Build the course overview from the approved outline using an approved index template.
- [x] Create only assets directly required by the lesson plans; use `.txt` for learner-readable datasets.
- [x] Verify every HTML asset link resolves to an existing file.

### Task 4: G3 human review and repair

**Files:**
- Modify only files created in Tasks 2–3 when a verified issue requires repair.
- Append: `courses/ict-ai-digital-workflow/_gates.md`.

**Interfaces:**
- Consumes: built HTML pages, G3 human checklist and style guide.
- Produces: reviewed pages with documented findings.

- [x] Check layout hierarchy, narrative continuity, AI-like filler, trial assets, SEO, links and learner actions.
- [x] Run per-page lint and course-directory lint.
- [x] Repair Hard-fail and justified Soft-fail items within this course only.

### Task 5: G4/G5 verification and deployment readiness

**Files:**
- Modify generated search index and sitemap only if their official build scripts require it.
- Append: `courses/ict-ai-digital-workflow/_gates.md`.

**Interfaces:**
- Consumes: reviewed course pages and assets.
- Produces: evidence-backed deployment-readiness status without publishing.

- [x] Run scoped course lint and link/integrity checks.
- [x] Run official search-index and sitemap builders if required by the project workflow.
- [x] Run course-validator layers available without live paid accounts; record unrun live-persona items explicitly.
- [x] Stop before registration, password generation, commit, push or deployment.
