# AI Beginner Practical Typography Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task with verification checkpoints.

**Goal:** 在不改變講義文字與既有互動流程的前提下，改善 `ai-beginner-practical` 全課頁面的易讀性、佈局節奏與日系編輯式視覺一致性。

**Architecture:** 以共用 `assets/layout-redesign.css` 為唯一主要修改點，透過內容寬度、字級 token、CJK 表格規則、低對比邊框與間距調整，讓六個正式頁面同步改善。保留既有 HTML 結構、表格資料、收合式工作台與手機表格區域捲動。

**Tech Stack:** HTML/CSS、Python page lint、Playwright browser checks。

**Spec:** 本次對話中的「易讀性／佈局風格／日系設計風格」建議，以及 `../_規範/design-tokens.md`。

## Global Constraints

- 不改變任何學員可見文字、表格內容、欄位 ID、表單流程或互動行為。
- 不修改全站 `design-tokens.md`；只在本課程共用 CSS 使用既有語意色與字級規範。
- 不使用 `git add -A`；只檢視與驗證本次排版相關檔案。
- 先建立本次修正的 backup 與 restore script，再修改目標檔案。
- 完成後必須通過 page lint、`git diff --check`、連結檢查與多尺寸 RWD 檢查。

---

### Task 1: 建立排版修正基線與備份

**Files:**
- Read: `ai-beginner-practical/assets/layout-redesign.css`
- Read: `ai-beginner-practical/index.html`, `module1.html`, `CH1-1.html`, `CH2-1.html`, `CH3-1.html`, `CH4-1.html`
- Create: `ai-beginner-practical/_backup/2026-09-21-pre-typography-layout/`
- Create: `ai-beginner-practical/_tools/restore-2026-09-21-pre-typography-layout.sh`

- [x] **Step 1: 確認目前正式頁面與 shared CSS 範圍**
  - 排除 `_backup/`、`_repair/` 與工作表支援檔，只把六個正式頁面與 shared CSS 列為本次 scope。
- [x] **Step 2: 備份本次會修改的 CSS 與正式頁面**
  - 保留相對路徑，避免覆蓋既有 2026-09-20 備份。
- [x] **Step 3: 驗證 restore script 語法**
  - Run: `bash -n ai-beginner-practical/_tools/restore-2026-09-21-pre-typography-layout.sh`

### Task 2: 修正共用版面、字級與 CJK 表格規則

**Files:**
- Modify: `ai-beginner-practical/assets/layout-redesign.css`

- [x] **Step 1: 收斂 lesson prose 寬度並保留首頁／索引寬版配置**
  - 讓長文正文維持約 760–860px 的閱讀寬度；表格仍可在局部容器水平捲動。
- [x] **Step 2: 整理既有字級為規範階梯**
  - 將非 token 的 `1rem`、`.98rem`、`.86rem` 等值改為相鄰既有階梯，不縮小正文與操作指示。
- [x] **Step 3: 加入 CJK 表格斷行與短標籤欄規則**
  - 使用 `word-break: keep-all`、`overflow-wrap: break-word`；只對短標籤欄使用 `white-space: nowrap`。
- [x] **Step 4: 增加表格 row 呼吸感與手機捲動提示**
  - 不改表格內容，調整 cell padding、line-height 與既有 scroll note 的視覺提示。
- [x] **Step 5: 降低過度粗重的色條與卡片感**
  - 將一般區塊的 3px 色條改為較安靜的 hairline／淡色底，保留真正需要強調的狀態色。
- [x] **Step 6: 保留並強化日系視覺語意**
  - 保留暖紙色、墨色、藍灰色與既有字體；以 spacing、細邊框與少量主色完成層級，而非增加裝飾。

### Task 3: 驗證視覺與技術回歸

**Files:**
- Verify: `ai-beginner-practical/assets/layout-redesign.css`
- Verify: six formal HTML pages and generated search index state

- [x] **Step 1: 執行 page lint**
  - Run: `python3 docs/lint-page.py ai-beginner-practical/ --summary --baseline`
- [x] **Step 2: 執行靜態差異與連結檢查**
  - Run: `git diff --check`
  - Verify all local links resolve without changing unrelated files.
- [x] **Step 3: 執行多尺寸 RWD 檢查**
  - Check 320, 360, 390, 414, 768, 1024 and 1440px for page-level horizontal overflow, loaded fonts, heading geometry and table-local scrolling.
- [x] **Step 4: 檢查文字未被改寫**
  - Compare normalized body text against the Task 1 backup for all formal pages.
- [x] **Step 5: 產出修正報告**
  - Create `ai-beginner-practical/_repair/2026-09-21-typography-layout/REPAIR-REPORT.md` with changed selectors, verification evidence, remaining limitations and restore path.
