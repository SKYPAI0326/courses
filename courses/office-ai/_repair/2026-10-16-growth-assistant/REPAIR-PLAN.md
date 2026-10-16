# Growth Assistant Course Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將通用 `ta-core`、`ta-learning`、`ta-work` 與 Gemini Notebook 寫入 office-ai 正式講義，讓學員完成可驗收的課後學習助教與辦公行政工作助理。

**Architecture:** CH1-2 建立可信來源與方案基準；CH6-1 完成通用 `ta-work` 辦公助理與職務客製化；CH6-3 整合 `ta-learning`、受控回寫與學習／工作雙向移植。正式 Markdown 先完成內容審查，再保真轉製到既有 HTML wrapper。

**Tech Stack:** Markdown、HTML/CSS/vanilla JavaScript、Gemini Skills、Gemini Notebook、既有 course lint／validator 工具。

**Spec:** `courses/office-ai/_repair/2026-10-16-growth-assistant/SCAN.md` 與本對話已核准的課程設計。

## Global Constraints

- 正式 `ta-work` 使用通用版本；嘉年華版本只作「依需求客製化」示範。
- 講師講義是學習助教的最高可信核心，外部資訊與模型推論必須分開標示。
- 學員方案以免費帳號每本 50 筆來源為設計基準；付費測試帳號 300 筆只列平台驗證條件。
- 寫入前必須確認目標與內容；PDF／網頁等原始來源保持唯讀，沉澱內容以新增或追加文字來源處理。
- 所有核心素材在第一次使用前提供可點擊本地連結、用途、使用時機與備援。
- 保留既有 19 單元與 URL；不建立新章節頁，不改密碼 gate，不改無關頁面。
- 本輪屬 `content-change`；source、HTML、首頁、課後指南與驗證紀錄必須同步。

## Review Focus

- 免費帳號或沒有 Skills 入口時，學員仍可用手動貼入規則的備援完成核心能力。
- 未指定筆記本、來源不足或名稱相近時，助理必須停下確認，不能自行猜測。
- 唯讀驗證與受控回寫必須分開；寫入前需顯示目標、內容與新增／追加模式。
- 嘉年華案例須明確標為通用 `ta-work` 的客製結果，不能取代正式模板。
- 改名後首頁、前後頁導航、來源教案、課後指南與搜尋索引不得殘留錯誤對應。

---

### Task 1: 建立備份、復原與學員素材

**Files:**
- Create: `courses/office-ai/_backup/2026-10-16-pre-growth-assistant/`
- Create: `courses/office-ai/_tools/restore-2026-10-16-pre-growth-assistant.sh`
- Create: `courses/office-ai/assets/skills/ta-core.md`
- Create: `courses/office-ai/assets/skills/ta-learning.md`
- Create: `courses/office-ai/assets/skills/ta-work.md`

**Interfaces:**
- Consumes: 使用者提供的三份正式 Skill 原始檔。
- Produces: 可下載的學員素材與一鍵回復本輪內容修改的腳本。

- [ ] 複製所有目標檔到版本化 backup，保存原始時間與內容。
- [ ] 建立 restore script，先檢查備份存在，再逐檔還原。
- [ ] 將三份 Skill 原始檔以通用名稱複製到 `assets/skills/`，核對 SHA-256 與來源相同。
- [ ] 以 `sh -n` 驗證 restore script，並用 `diff -q` 驗證備份完整。

### Task 2: 更新大綱、Style Guide 與三份正式教案

**Files:**
- Modify: `_outlines/office-ai.md`
- Create: `_outlines/office-ai.style-guide.md`
- Modify: `_lessons/office-ai/CH1-2.md`
- Modify: `_lessons/office-ai/CH6-1.md`
- Modify: `_lessons/office-ai/CH6-3.md`

**Interfaces:**
- Consumes: Task 1 的 Skill 素材連結與已核准三層教學架構。
- Produces: HTML 轉製的唯一正式 learner-content。

- [ ] 將 CH1-2 改為 Gemini Notebook（原 NotebookLM）與 50 筆來源策略，保留工作模式判斷卡。
- [ ] 將 CH6-1 改為 `ta-core + ta-work` 辦公助理操作課，提供完整辦公案例、唯讀檢查、來源邊界、文件草擬及五項客製化表。
- [ ] 將嘉年華版呈現為通用 `ta-work` 的客製化示範，標明保留的底層契約與被替換的職務細節。
- [ ] 將 CH6-3 改為 integration-capstone：建立 `ta-core + ta-learning` 學習助教，完成引用查核、受控追加、30 天維護與工作移植。
- [ ] 為每課補齊起始材料、第一動作、可觀察結果、checkpoint、失敗回復、完成物與再次使用方式。
- [ ] 執行高風險修辭掃描、正文自驗與內容 Issue List；BLOCKER／MAJOR 歸零後才進 HTML。

### Task 3: 保真更新學員頁、首頁與課後指南

**Files:**
- Modify: `courses/office-ai/ch1/CH1-2.html`
- Modify: `courses/office-ai/ch6/CH6-1.html`
- Modify: `courses/office-ai/ch6/CH6-3.html`
- Modify: `courses/office-ai/index.html`
- Modify: `courses/office-ai/assets/after-class-guide.md`

**Interfaces:**
- Consumes: Task 2 通過內容審查的 learner-content。
- Produces: 學員可從首頁開始、依頁面與素材完成的正式講義。

- [ ] 保留既有 gate、topbar、lesson-body、navigation、footer 與 localStorage 腳本，只替換已核准內容及必要 metadata。
- [ ] 在首次使用前提供三份 Skill 下載連結、用途、安裝位置與無 Skills 入口備援。
- [ ] 同步首頁單元名稱、章六核心產出與課後素材卡。
- [ ] 修正課後指南過時的 CH3-1 NotebookLM 對應，新增成長型助理復跑流程。
- [ ] 檢查所有本地連結與前後頁導航。

### Task 4: 更新審查證據並做逐頁驗證

**Files:**
- Modify: `courses/office-ai/_review/CH1-2-content.md`
- Modify: `courses/office-ai/_review/CH1-2-fidelity.md`
- Modify: `courses/office-ai/_review/CH6-1-content.md`
- Modify: `courses/office-ai/_review/CH6-1-fidelity.md`
- Modify: `courses/office-ai/_review/CH6-3-content.md`
- Modify: `courses/office-ai/_review/CH6-3-fidelity.md`
- Modify: `courses/office-ai/_validation/evidence.json`
- Modify: `courses/office-ai/_validation/HUMAN-VALIDATION-CHECKLIST.md`
- Create: `courses/office-ai/_repair/2026-10-16-growth-assistant/REPAIR-REPORT.md`

**Interfaces:**
- Consumes: Task 3 的現行 source、HTML 與 assets hash。
- Produces: 可追溯的內容、保真、技術及待真人／平台驗證狀態。

- [ ] 逐頁核對核心概念、完整 prompt、示範輸入／輸出、練習、修復與素材首次入口。
- [ ] 移除三個變更單元的過期模擬 records，重新加入本輪 author-self-check content／fidelity 記錄；不沿用舊 hash。
- [ ] 執行三頁 lint、substance audit、HTML structure validator 與全站相對連結掃描。
- [ ] 在 1440、390、430 寬度檢查頁首、修改區、中段、底部、水平捲動、導航與 localStorage scroll state。
- [ ] 執行 course-validator；區分本輪通過項與既有全課 BLOCKED／PENDING，不宣告真人已完成。
- [ ] 檢查 PDF 登錄同步狀態與搜尋索引影響；若 mixed worktree 造成跨課變更，保留為 ops 待辦，不混入本輪成果。

## Self-Review

- Spec coverage：學習助教、辦公助理、通用／客製區分、50 筆策略、唯讀與回寫、課後使用及跨情境移植均有對應 Task。
- Step scan：每個 Task 均產生可獨立檢查的來源、頁面或證據。
- Type consistency：三個 Skill 名稱固定為 `ta-core`、`ta-learning`、`ta-work`；產品名稱固定為「Gemini Notebook（原 NotebookLM）」。
- Review Focus：帳號差異、筆記本歧義、寫入確認、客製化定位與跨頁同步都在內容或驗證步驟中有檢查。
- Proportion：保留 19 單元與既有頁面骨架，修改集中在三個教學節點與必要同步檔案。
