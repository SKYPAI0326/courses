# 行政 AI 虛擬助理實戰學員版 PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 產生 6 份 A4 章節分冊、1 份全課合併版與 NotebookLM 索引。

**Architecture:** Node/Playwright 從現有 HTML 抽取章節與資產庫內容，注入共用印刷 CSS 後輸出帶文字層 PDF。Python/pypdf 移除空白頁、寫入 metadata／書籤並合併全課版；Poppler 與 Pillow 負責全頁渲染驗證。

**Tech Stack:** HTML/CSS、Node.js 24、Playwright、Python 3、pypdf、Poppler、Pillow。

## Global Constraints

- 不修改 `admin-ai-assistant/index.html`、`CH1.html` 至 `CH6.html`、`prompt-library.html`。
- 正式產物只寫入 `output/pdf/admin-ai-assistant/`。
- A4 直式、可雙面列印、保留文字層、灰階可辨識。
- 練習題留在正文，答案集中到各分冊末尾與合併版答案附錄。
- 分冊檔名固定為 `ADMIN-AI-CH01` 至 `ADMIN-AI-CH06`。

---

### Task 1: 建立建置與後處理器

**Files:**
- Create: `admin-ai-assistant/_tools/build-print-handouts.mjs`
- Create: `admin-ai-assistant/_tools/postprocess-print-pdfs.py`
- Test: Node 語法檢查、Python compile、來源清冊檢查

**Interfaces:**
- `build-print-handouts.mjs` 讀取 6 章與資產庫 HTML，輸出分冊、合併版、README、manifest。
- `postprocess-print-pdfs.py module <pdf> <chapter> <title> <source>` 後處理分冊。
- `postprocess-print-pdfs.py full <pdf> <module-json> <appendix-pdf>` 合併全課版。

- [ ] **Step 1: 驗證建置器尚不存在**

Run: `test ! -e admin-ai-assistant/_tools/build-print-handouts.mjs`
Expected: exit 0。

- [ ] **Step 2: 建立最小建置器與後處理器**

建置器必須固定 `CH1.html` 至 `CH6.html` 順序；抽取 `.page-hero` 到 `.nav-footer`；將 `.quiz-ans` 移至答案區；對所有 `details` 加 `open`；移除 button、密碼關卡、topbar、導覽與 footer；產生 A4 PDF。後處理器必須以文字量判斷 footer-only 空白頁，重建章節書籤與 metadata。

- [ ] **Step 3: 執行語法與來源清冊測試**

Run: `node --check admin-ai-assistant/_tools/build-print-handouts.mjs && python3 -m py_compile admin-ai-assistant/_tools/postprocess-print-pdfs.py`
Expected: exit 0、無錯誤輸出。

### Task 2: 生成正式 PDF 與索引

**Files:**
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-CH01-從-AI-工具到行政虛擬助理方案.pdf`
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-CH02-用-Gemini-處理會議紀錄.pdf`
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-CH03-Email-公文與行政通知撰寫.pdf`
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-CH04-資料彙整與主管摘要.pdf`
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-CH05-簡報製作-產出乾淨內容包.pdf`
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-CH06-完整行政虛擬助理方案.pdf`
- Create: `output/pdf/admin-ai-assistant/ADMIN-AI-FULL-行政AI虛擬助理實戰-學員版.pdf`
- Create: `output/pdf/admin-ai-assistant/README.md`
- Create: `output/pdf/admin-ai-assistant/manifest.json`

**Interfaces:**
- Consumes: Task 1 兩個建置腳本。
- Produces: 7 份正式 PDF 與 NotebookLM 來源對照。

- [ ] **Step 1: 執行建置**

Run: `node admin-ai-assistant/_tools/build-print-handouts.mjs`
Expected: 6 行 `built ...CHxx...pdf`、1 行合併版與索引輸出。

- [ ] **Step 2: 核對檔案清冊**

Run: `find output/pdf/admin-ai-assistant -maxdepth 1 -type f | sort`
Expected: 7 份 PDF、`README.md`、`manifest.json`。

### Task 3: 全量內容與印刷驗證

**Files:**
- Create: `admin-ai-assistant/tmp/pdfs/admin-ai-validation-final/*.png`
- Create: `admin-ai-assistant/tmp/pdfs/admin-ai-validation-final/CONTACT-CH*.png`

**Interfaces:**
- Consumes: Task 2 的 7 份 PDF 與 manifest。
- Produces: 機器驗證結果與人工視覺檢查證據。

- [ ] **Step 1: 驗證文字層、A4、metadata、書籤與頁數**

使用 pypdf 逐冊驗證來源檔名、章節標題、595.28 × 841.89 pt、metadata 與 outline；合併版頁數必須等於六冊頁數加資產庫附錄頁數。

- [ ] **Step 2: 渲染全部頁面**

Run: `pdftoppm -r 96 -png <each-chapter-pdf> admin-ai-assistant/tmp/pdfs/admin-ai-validation-final/<prefix>`
Expected: 每個 PDF 頁面各有一張 PNG。

- [ ] **Step 3: 掃描與人工檢視**

以 Pillow 驗證尺寸一致、零近空白頁，建立每冊 contact sheet；人工檢查封面、正文、Prompt、表格、練習、答案與全冊縮圖，要求零裁切、重疊與黑方塊。

- [ ] **Step 4: 最終範圍檢查**

Run: `git diff --check -- admin-ai-assistant output/pdf/admin-ai-assistant`
Expected: exit 0；未修改既有 8 份 HTML。

