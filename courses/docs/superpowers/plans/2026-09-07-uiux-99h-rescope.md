# UI/UX 99h Course Rescope Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將正式課綱圖片中的 42h「介面元素與設計」與 57h「UI/UX 原型製作與資料打包」重整為可由接近零基礎學員完成的 99h 產出鏈，並以逐 Gate 證據放行。

**Architecture:** 先恢復或確認舊基線，再建立不漏行政課綱項目的 coverage matrix；接著以 16-stage 技能依賴建立 99h 大綱與時間帳本，先完成一個代表單元與真人跟做，再按 Part 逐單元產製。正式課綱圖片控制名稱、範圍與時數；ChatGPT 交接文字控制可採用的教學順序、操作契約與交接治理。

**Tech Stack:** Markdown（outline、coverage matrix、lesson plan、Gate 記錄）、HTML5/CSS3/原生 JavaScript（講義）、Figma、Adobe Photoshop、VS Code、Chrome、Git、GitHub、專案既有 lint／search index／sitemap 工具。

**Spec:** `uiux-designer/_design/2026-09-07-99h-course-rescope-design.md`

## Global Constraints

- 行政總時數固定為 42h＋57h＝99h。
- 42h 必須覆蓋色彩、字型、格線、Auto Layout、Component、Button、Form、List、Toast、Dialog、Navigation、Variants。
- 57h 必須覆蓋線框／原型／工具介紹／手機介面／元件與動畫互動、觸發、轉場、Overlay、Swap、滾動、置頂導覽、漂浮按鈕、Smart Animation、Figma／PS 發布與輸出、網頁入門、雲端部署。
- 舊「Photoshop 42h＋UI/UX 57h」版本只能作歷史，不得作新範圍或新 Gate 的來源。
- 受眾接近零基礎；每個新能力要有概念、位置、具體操作、預期結果、驗證與 Debug。
- 不納入 React、Vue、Next.js、TypeScript、Tailwind、後端框架或資料庫，除非使用者另行核准。
- 不使用 `git add -A`；每個 commit 只暫存本任務明確列出的檔案。
- 未經使用者 Gate 核准，不製作下一個代表單元或批次講義。

---

### Task 1: 確認可用課程基線

**Files:**
- Read: `uiux-designer/`
- Read: `_outlines/`
- Read: `_lessons/`
- Read: `courses/uiux-designer/`
- Create: `uiux-designer/_design/BASELINE-STATUS.md`

**Interfaces:**
- Consumes: 現有檔案、Git history、已核准設計規格。
- Produces: 一份只描述「找到哪些基線、缺哪些檔案、哪些可恢復」的狀態報告。

- [ ] **Step 1: 搜尋可能的舊基線**

```bash
rg --files .. | rg -i 'uiux|photoshop|prototype|interface|outline|lesson|gate'
git log --all --name-status -- uiux-designer _outlines _lessons courses/uiux-designer
```

Expected: 列出目前工作樹、備份、其他 branch 或 commit 中可辨識的候選檔案；不得修改內容。

- [ ] **Step 2: 記錄基線判定**

在 `BASELINE-STATUS.md` 記錄：目前找到的檔案、來源 commit／路徑、是否符合 42h＋57h 新基準，以及後續採「局部修正」或「從新基準重建」。

- [ ] **Step 3: 驗證範圍沒有漂移**

```bash
rg -n 'Photoshop 42h|429h|42h.*Photoshop|介面元素與設計|UI/UX 原型製作與資料打包' uiux-designer BASELINE-STATUS.md ../_outlines ../_lessons 2>/dev/null
```

Expected: 舊 Photoshop 42h 只被標為歷史／待處理，不被新 coverage matrix 當作正式來源。

- [ ] **Step 4: Commit baseline report**

```bash
git add uiux-designer/_design/BASELINE-STATUS.md
git commit -m "docs: record uiux course baseline"
```

### Task 2: 建立 42h／57h 正式 coverage matrix（Gate 0）

**Files:**
- Create: `uiux-designer/_design/99h-coverage-matrix.md`
- Read: `/Users/paichenwei/Downloads/1788509797593.jpg`
- Read: `/Users/paichenwei/Downloads/1788509783989.jpg`
- Read: `uiux-designer/_design/2026-09-07-99h-course-rescope-design.md`

**Interfaces:**
- Consumes: 兩張正式課綱圖片與 ChatGPT 交接規格。
- Produces: 每一個行政課綱項目的對應 Stage、候選單元、完成物、後續重用位置與來源註記。

- [ ] **Step 1: 建立 42h 行政項目表**

逐列寫入色彩、字型、格線、Auto Layout、Component、Button、Form、List、Toast、Dialog、Navigation、Variants；每列必須有候選 Stage、首次教學結果與可驗收證據。

- [ ] **Step 2: 建立 57h 行政項目表**

逐列寫入線框／原型／工具介紹／手機介面／元件與動畫互動、9 個互動／交付／部署主題；每列必須有候選 Stage、完成物與後續重用位置。

- [ ] **Step 3: 建立重疊與邊界欄**

對 Figma 元件、手機介面、Photoshop 輸出與網頁內容標示「首次教學」或「後續重用」；若同一操作在兩門課出現，明確寫出不重複計時的理由。

- [ ] **Step 4: 驗證 coverage 完整性**

```bash
rg -n '色彩|字型|格線|Auto Layout|Component|Button|Form|List|Toast|Dialog|Navigation|Variants' uiux-designer/_design/99h-coverage-matrix.md
rg -n '觸發|轉場|Overlay|Swap|滾動|置頂|漂浮|Smart Animation|發布|輸出|網頁|部署' uiux-designer/_design/99h-coverage-matrix.md
```

Expected: 42h 的 12 項與 57h 的 9 組正式主題全部命中，且每列都有完成物與驗收證據。

- [ ] **Step 5: Commit Gate 0 artifact**

```bash
git add uiux-designer/_design/99h-coverage-matrix.md
git commit -m "docs: map formal uiux 99h curriculum coverage"
```

- [ ] **Step 6: User Gate 0 review**

呈現矩陣摘要與任何「圖片未明確指定、只能來自 ChatGPT 建議」的項目；未取得使用者核准前，不進入時間分配。

### Task 3: 建立 99h Stage／單元矩陣與依賴鏈（Gate 1）

**Files:**
- Create or Modify: `_outlines/uiux-designer.md`
- Create: `uiux-designer/_design/99h-time-ledger.md`
- Create: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: `99h-coverage-matrix.md` 與 Gate 0 核准結果。
- Produces: 正式 outline、Stage／單元依賴、42h／57h／99h 時間帳本與 Gate 1 記錄。

- [ ] **Step 1: 建立 Stage 到行政項目的追溯表**
- [ ] **Step 2: 為每個單元寫目標、完成物、先備能力與後續使用位置**
- [ ] **Step 3: 建立 42h 與 57h 的分鐘帳本**
- [ ] **Step 4: 驗證每單元、每 Part 與全課的加總**

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('uiux-designer/_design/99h-time-ledger.md').read_text()
assert '42h' in text and '57h' in text and '99h' in text
print('time-ledger anchors: PASS')
PY
```

- [ ] **Step 5: User Gate 1 review**

未經核准，不建立代表單元教案。

### Task 4: 建立代表單元與試跑包（Gate 2）

**Files:**
- Create: `_lessons/uiux-designer/CH1-1-layout-system.md`
- Create: `uiux-designer/assets/CH1-1-layout-system/`
- Create: `uiux-designer/_review/CH1-1-layout-system-TRIAL.md`

**Interfaces:**
- Consumes: Gate 1 核准的單元契約、來源查證與時間帳本。
- Produces: 一個完整教案、起始檔、完成參考、錯誤狀態、Debug 路徑、驗收表與試跑紀錄。

- [ ] **Step 1: 先完成概念、micro-demo、Follow Along 與 Checkpoint**
- [ ] **Step 2: 補 Guided Practice、Independent Challenge、錯誤修復與完成物**
- [ ] **Step 3: 用零基礎冷啟動檢查教案**
- [ ] **Step 4: User Gate 2 review**

### Task 5: 建立代表講義與真人跟做（Gate 3）

**Files:**
- Create: `courses/uiux-designer/CH1-1-layout-system.html`
- Modify: `courses/uiux-designer/index.html` only if Gate 3 approves the route.
- Modify: `uiux-designer/_gates.md`

**Interfaces:**
- Consumes: Gate 2 approved lesson plan and trial package.
- Produces: 一頁 learner-facing HTML、lint／連結／手機檢查與使用者真人跟做紀錄。

- [ ] **Step 1: 建立 HTML**
- [ ] **Step 2: 執行頁面 lint、連結與手機寬度檢查**
- [ ] **Step 3: 由使用者完成實際跟做並記錄結果**
- [ ] **Step 4: 只有真人證據 PASS 才放行同 Part 其餘單元**

### Task 6: 逐 Part 產製與整合驗收（Gate 4–5）

**Files:**
- Modify: `_lessons/uiux-designer/`
- Modify: `courses/uiux-designer/`
- Modify: `uiux-designer/_gates.md`
- Modify: `uiux-designer/_design/99h-time-ledger.md`

**Interfaces:**
- Consumes: 代表頁 Gate 3 PASS 與使用者核准。
- Produces: 42h／57h 全部單元、Prototype 測試證據、Handoff、Web、Git/GitHub、部署與整合報告。

- [ ] **Step 1: 依核准順序完成 42h Part**
- [ ] **Step 2: 依核准順序完成 57h Part**
- [ ] **Step 3: 逐單元驗證產出鏈與不重複活動**
- [ ] **Step 4: 執行全課 lint、整合真跑與部署驗收**
- [ ] **Step 5: 只有全部證據通過才宣告 99h 課程可交付**

## Verification Checklist

完成任何 Task 前都必須重新確認：

- [ ] 沒有把 42h 改回 Photoshop 專修課。
- [ ] 42h／57h 每個正式項目都有 coverage、完成物與驗收證據。
- [ ] ChatGPT 提案中的 Git/GitHub、16 Stage 與成果鏈沒有未標示地變成行政必修。
- [ ] 時數沒有由找檔、等待、保存或重複操作灌出來。
- [ ] 只修改當前 Task 列出的檔案。
- [ ] 目前工作樹其他課程的變更未被暫存。
