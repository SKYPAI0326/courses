# 創業 AI 實戰缺漏交付物 Implementation Plan

> **執行方式：** 本計畫預設由單一 agent 依序執行。除非使用者另行核准，不啟動子 agent。每個工作包完成後必須停下，交由使用者驗收。

**Goal:** 補齊 `simple-ai` 的完整版手冊、A4 雙面精華版、NotebookLM 與 Gemini 雙向工作流，以及三個課程入口頁的真實下載路徑。

**Architecture:** 以兩份獨立、可列印的 HTML 作為 PDF 單一來源，新增一支課程內 PDF 建置腳本，固定輸出兩份正式 PDF。既有課程只修改 CH2-1、第二堂導覽、首頁與結訓頁；所有變更先備份，A、B、C、D 四包依序驗收。

**Tech Stack:** HTML5、CSS3、原生 JavaScript、Playwright/Chromium、Poppler (`pdfinfo`、`pdftotext`、`pdftoppm`)、既有 `docs/lint-page.py`、`docs/build-search-index.py`、`docs/build-sitemap.py`。

**Spec:** `courses/simple-ai/_repair/2026-08-25/DELIVERABLE-DESIGN.md`

## Global Constraints

- 核心路徑限免費手機版 ChatGPT、Gemini、NotebookLM；不可要求信用卡、試用或付費功能。
- 完整範例必須包含：情境、可用素材、填妥 Prompt、手機步驟、完整輸出、判讀、錯誤修復、完成證據。
- 案例主線只使用咖啡館與手工皂創業者；其他產業只能作短篇臨演對照。
- 手冊頁數目標 55–65 頁，不得以重複內容、放大字級或空白頁灌頁。
- A4 精華版必須恰為兩頁，且十則 Prompt 與完整版手冊文字一致。
- 「雙向」只表示人工在 NotebookLM 與 Gemini 間搬運及查核內容，不宣稱原生自動同步。
- 沒有已驗證的正式公開 PDF 網址時，不建立 QR Code 占位圖，也不宣稱 QR Code 完成。
- 不修改 `simple-ai` 以外課程，不重做既有視覺系統，不刪除未經核准的既有教學內容。
- 不使用 `git add -A`；每次只暫存本計畫列出的精確檔案。

---

## File Map

### 新增

- `courses/simple-ai/handbook.html`：完整版手冊唯一排版來源。
- `courses/simple-ai/quick-reference.html`：A4 雙面精華版唯一排版來源。
- `courses/simple-ai/_tools/build-deliverables.js`：建置兩份 PDF，並檢查頁數契約。
- `courses/simple-ai/assets/創業-AI-實戰手冊.pdf`：工作包 A 正式成品。
- `courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf`：工作包 B 正式成品。
- `courses/simple-ai/_repair/2026-08-25/REPAIR-PLAN.md`：本輪精確修復範圍與風險。
- `courses/simple-ai/_repair/2026-08-25/PLATFORM-AUDIT.md`：手機版功能查證日期、來源與採用措辭。
- `courses/simple-ai/_repair/2026-08-25/REPAIR-REPORT.md`：最終變更與驗證證據。
- `courses/simple-ai/_tools/restore-2026-08-25-pre-deliverables.sh`：還原既有頁面並移除本輪新增交付物。

### 修改

- `courses/simple-ai/CH2-1.html`：加入 NotebookLM → Gemini → NotebookLM 完整示範。
- `courses/simple-ai/module2.html`：同步第二堂摘要與真實教材入口。
- `courses/simple-ai/index.html`：新增兩份教材入口。
- `courses/simple-ai/CH2-4.html`：新增結訓下載區，移除尚無實據的 Google Form／QR 承諾。

### 備份

- `courses/simple-ai/_backup/2026-08-25-pre-deliverables/CH2-1.html`
- `courses/simple-ai/_backup/2026-08-25-pre-deliverables/module2.html`
- `courses/simple-ai/_backup/2026-08-25-pre-deliverables/index.html`
- `courses/simple-ai/_backup/2026-08-25-pre-deliverables/CH2-4.html`

---

### Task 1: Scope Lock、修復清單與可回復基線

**Files:**
- Create: `courses/simple-ai/_repair/2026-08-25/REPAIR-PLAN.md`
- Create: `courses/simple-ai/_backup/2026-08-25-pre-deliverables/{CH2-1.html,module2.html,index.html,CH2-4.html}`
- Create: `courses/simple-ai/_tools/restore-2026-08-25-pre-deliverables.sh`

**Interfaces:**
- Consumes: 核准的 `DELIVERABLE-DESIGN.md`、本計畫及四個現有 HTML。
- Produces: 後續 Task 2–7 共用的固定 scope、備份與還原入口。

- [ ] **Step 1: 確認 scope 與 dirty worktree 邊界**

Run:

```bash
git status --short -- courses/simple-ai
git diff --name-only -- courses/simple-ai
```

Expected: 除本輪兩份規格檔外，不得把使用者既有修改誤納入 scope；若四個目標 HTML 已有未提交修改，停止並先向使用者報告。

- [ ] **Step 2: 寫入 REPAIR-PLAN**

內容必須逐一列出 A–D 工作包、四個既有頁面、五個新交付檔、備份需求、QR 排除條件與每包驗收閘門。嚴重度至少包含：PDF 實檔缺失 `BLOCKER`、A4 精華版缺失 `BLOCKER`、雙向流程缺失 `MAJOR`、假 QR／Google Form 承諾 `MAJOR`。

- [ ] **Step 3: 建立四個既有頁面的逐檔備份**

Run:

```bash
mkdir -p courses/simple-ai/_backup/2026-08-25-pre-deliverables
cp courses/simple-ai/CH2-1.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/CH2-1.html
cp courses/simple-ai/module2.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/module2.html
cp courses/simple-ai/index.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/index.html
cp courses/simple-ai/CH2-4.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/CH2-4.html
```

- [ ] **Step 4: 建立精確還原腳本**

腳本只可覆回上述四個 HTML，並只移除本輪明列的新檔：`handbook.html`、`quick-reference.html`、兩份 PDF、`build-deliverables.js`、`PLATFORM-AUDIT.md`、`REPAIR-REPORT.md`。不得遞迴刪除目錄。

- [ ] **Step 5: 驗證還原腳本語法與備份一致性**

Run:

```bash
bash -n courses/simple-ai/_tools/restore-2026-08-25-pre-deliverables.sh
cmp courses/simple-ai/CH2-1.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/CH2-1.html
cmp courses/simple-ai/module2.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/module2.html
cmp courses/simple-ai/index.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/index.html
cmp courses/simple-ai/CH2-4.html courses/simple-ai/_backup/2026-08-25-pre-deliverables/CH2-4.html
```

Expected: `bash -n` 與四次 `cmp` 全部 exit 0。

---

### Task 2: 工作包 A 完整版手冊 HTML

**Files:**
- Create: `courses/simple-ai/handbook.html`
- Read only: `courses/simple-ai/CH1-1.html` 至 `CH2-4.html`
- Read only: `courses/simple-ai/prompt-library.html`

**Interfaces:**
- Consumes: 八個單元既有內容、55 條 Prompt、雙主線 Style Guide。
- Produces: 可由 Task 3 建置成 55–65 頁 PDF 的單一 HTML。

- [ ] **Step 1: 建立 A4 印刷骨架**

建立封面、目錄、十章、頁尾頁碼區與 `@page { size: A4; }`。導覽、密碼關卡、複製按鈕與互動腳本不得進入手冊。

- [ ] **Step 2: 完成 CH1-1 與 CH1-2 章節**

CH1-1 完整範例使用手工皂創業者，必須展示填妥的 EF-08、AI 確認回覆、設定判讀及設定遺失修復。CH1-2 必須內嵌完整兩角色會議逐字稿、EF-01 填妥 Prompt、五點摘要、三欄待辦、錯誤日期對照與 `[待確認]` 修復。

- [ ] **Step 3: 完成 CH1-3 與 CH1-4 章節**

CH1-3 必須以文字表格完整呈現報價單所有欄位、EF-02、結構化輸出、Email 三語氣與數字查核。CH1-4 必須含三條紅線、六個陷阱、錯誤公開文案、修正版本與可勾選發佈表。

- [ ] **Step 4: 完成 CH2-1 與 CH2-2 章節**

CH2-1 先收錄不依賴即時 UI 的品牌來源包、NB-01 完整輸入與來源式輸出；雙向 UI 細節由 Task 5 查證後補入。CH2-2 必須展示咖啡館的功能／情感／對立三版完整輸出、三問判讀及最後人工改寫版本。

- [ ] **Step 5: 完成 CH2-3 與 CH2-4 章節**

CH2-3 必須完整呈現七則貼文骨架、一則貼文 A/B 標題、30 秒逐鏡短影音腳本及不合格空泛版對照。CH2-4 必須完整呈現 5 問題 × 3 語氣的 15 則 FAQ、發佈檢查與修正後版本。

- [ ] **Step 6: 完成十條工作流與 55 條 Prompt 導讀**

十條 WF 每條都要列輸入、工具順序、產物、人工決策與免費版備援。55 條 Prompt 採索引導讀，不在此處重複印出已於章節完整呈現的相同 Prompt。

- [ ] **Step 7: 執行完整範例靜態契約檢查**

Run:

```bash
rg -n '完整素材|填妥 Prompt|預期輸出|判讀|錯誤對照|修復|完成證據' courses/simple-ai/handbook.html
rg -n 'EF-08|EF-01|EF-02|EF-04|NB-01|TK-02|MK-01|MK-02|MK-03|CS-01|WF-10' courses/simple-ai/handbook.html
rg -n '瑜伽|花藝|n8n|Zapier|Make.com|信用卡|免費試用' courses/simple-ai/handbook.html
```

Expected: 前兩次搜尋覆蓋所有章節與指定 Prompt；第三次不得出現新的固定案例、禁用自動化工具或付款要求。若「免費試用」只出現在否定提醒中，需人工確認語意。

---

### Task 3: 工作包 A PDF 建置與驗收閘門

**Files:**
- Create: `courses/simple-ai/_tools/build-deliverables.js`
- Create: `courses/simple-ai/assets/創業-AI-實戰手冊.pdf`

**Interfaces:**
- Consumes: `handbook.html`、`quick-reference.html`（Task 4 完成前允許只建手冊模式）。
- Produces: `node .../build-deliverables.js handbook` 與 `node .../build-deliverables.js quick-reference` 兩個固定命令。

- [ ] **Step 1: 實作 handbook 建置模式**

使用工作區 Playwright Chromium，載入本機 `handbook.html`、等待 `document.fonts.ready`、模擬 print media，輸出 A4、背景色與頁碼。建置後以 `pdfinfo` 讀取頁數；少於 55 或多於 65 時 exit 1。

- [ ] **Step 2: 先跑建置並確認頁數契約**

Run:

```bash
node courses/simple-ai/_tools/build-deliverables.js handbook
pdfinfo courses/simple-ai/assets/創業-AI-實戰手冊.pdf | rg '^Pages:'
```

Expected: `Pages:` 在 55–65。

- [ ] **Step 3: 驗證 PDF 文字與必要錨點**

Run:

```bash
pdftotext courses/simple-ai/assets/創業-AI-實戰手冊.pdf /tmp/simple-ai-handbook.txt
rg -n '五零件|逐字稿|結構化資料|三條絕對紅線|品牌知識庫|功能.*情感.*對立|一週七則|15 則 FAQ|WF-10' /tmp/simple-ai-handbook.txt
```

Expected: 九個內容錨點全部命中。

- [ ] **Step 4: 逐頁渲染並檢查版面**

Run:

```bash
mkdir -p /tmp/simple-ai-handbook-pages
pdftoppm -png -r 110 courses/simple-ai/assets/創業-AI-實戰手冊.pdf /tmp/simple-ai-handbook-pages/page
```

逐頁檢查：空白頁、截字、孤立標題、Prompt 與輸出錯位、表格破裂、小於可讀尺寸的正文。發現問題只調整 `handbook.html`，重新建置一次；第二次仍失敗即停止並回報。

- [ ] **Step 5: 工作包 A 停看點**

向使用者提交 PDF、頁數、九個文字錨點及逐頁檢查結果。未獲使用者核准，不進 Task 4。

---

### Task 4: 工作包 B A4 雙面精華版

**Files:**
- Create: `courses/simple-ai/quick-reference.html`
- Create: `courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf`
- Modify: `courses/simple-ai/_tools/build-deliverables.js`

**Interfaces:**
- Consumes: `handbook.html` 中十則已核准 Prompt 文字。
- Produces: 恰為兩頁的 A4 PDF；不得另寫不同版本 Prompt。

- [ ] **Step 1: 建立雙面兩頁版型**

正面放 EF-08、EF-01、EF-02、EF-04、NB-01；背面放 TK-02、MK-01、MK-02、MK-03、CS-01。每則只保留用途、必要填空、可直接複製文字與完成物；頁尾放三條紅線及發佈三問。

- [ ] **Step 2: 加入 quick-reference 建置模式與硬性頁數檢查**

建置腳本輸出 PDF 後用 `pdfinfo` 檢查 `Pages: 2`；不是兩頁即 exit 1。

- [ ] **Step 3: 驗證十則 Prompt 與頁數**

Run:

```bash
node courses/simple-ai/_tools/build-deliverables.js quick-reference
pdfinfo courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf | rg '^Pages:[[:space:]]+2$'
pdftotext courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf /tmp/simple-ai-quick-reference.txt
for code in EF-08 EF-01 EF-02 EF-04 NB-01 TK-02 MK-01 MK-02 MK-03 CS-01; do rg -q "$code" /tmp/simple-ai-quick-reference.txt || exit 1; done
```

Expected: 兩頁，十個代碼全部存在。

- [ ] **Step 4: 彩色與灰階渲染檢查**

Run:

```bash
mkdir -p /tmp/simple-ai-quick-pages
pdftoppm -png -r 150 courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf /tmp/simple-ai-quick-pages/color
pdftoppm -gray -png -r 150 courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf /tmp/simple-ai-quick-pages/gray
```

人工確認四張圖中文字、分欄、底色與 Prompt 均可讀；最多一次版面補救。

- [ ] **Step 5: 工作包 B 停看點**

向使用者提交雙面 PDF、彩色與灰階預覽、頁數及十代碼檢查。未獲核准，不進 Task 5。

---

### Task 5: 工作包 C 手機版查證與雙向完整示範

**Files:**
- Create: `courses/simple-ai/_repair/2026-08-25/PLATFORM-AUDIT.md`
- Modify: `courses/simple-ai/CH2-1.html`
- Modify: `courses/simple-ai/module2.html`
- Modify: `courses/simple-ai/handbook.html`

**Interfaces:**
- Consumes: 官方 NotebookLM、Gemini 當期說明與實際手機版可觀察流程。
- Produces: 有查證日期、可免費完成、具固定備援的雙向課程段落。

- [ ] **Step 1: 查證當期官方功能與手機限制**

只使用 Google 官方說明及實際手機頁面，記錄：來源網址、查證日期、可上傳來源類型、引用／來源顯示方式、Gemini 貼入長文字流程、是否存在原生互傳。無官方證據的功能不得寫入課程。

- [ ] **Step 2: 寫入 PLATFORM-AUDIT**

文件必須分成 `Confirmed`、`Not claimed`、`Fallback` 三區。`Not claimed` 明列「不宣稱原生自動同步」；`Fallback` 固定為複製 NotebookLM 摘要與來源摘錄到 Gemini，再將可驗證句子貼回 NotebookLM 查核。

- [ ] **Step 3: 在 CH2-1 加入完整雙向示範**

示範包含三份咖啡館來源全文、NotebookLM 品牌聲音摘要與引用、送往 Gemini 的完整 Prompt、完整貼文草稿、回送 NotebookLM 的逐句查核 Prompt、支持／無依據結果、修正後可發佈版本、手機操作與卡關備援。

- [ ] **Step 4: 同步 module2 與 handbook**

`module2.html` 只更新單元目標，不複製整段示範。`handbook.html` 的 CH2-1 章同步已查證流程與同一組完整輸出，避免網頁與 PDF 說法分歧。

- [ ] **Step 5: 跑語意與 lint 驗證**

Run:

```bash
rg -n 'NotebookLM.*Gemini|Gemini.*NotebookLM|不宣稱.*自動同步|來源|無依據|複製' courses/simple-ai/CH2-1.html courses/simple-ai/module2.html courses/simple-ai/handbook.html
python3 docs/lint-page.py courses/simple-ai/CH2-1.html --summary
python3 docs/lint-page.py courses/simple-ai/module2.html --summary
```

Expected: 雙向、來源查核與備援錨點全部命中；兩頁 lint exit 0。

- [ ] **Step 6: 重建手冊並重跑 Task 3 驗證**

CH2-1 更新後重新產生完整版 PDF，頁數仍須 55–65，九個內容錨點仍須全數命中。

- [ ] **Step 7: 工作包 C 停看點**

向使用者提交 `PLATFORM-AUDIT.md`、完整示範所在頁面、PDF 更新及免費手機備援證據。未獲核准，不進 Task 6。

---

### Task 6: 工作包 D 真實下載入口與舊承諾清理

**Files:**
- Modify: `courses/simple-ai/index.html`
- Modify: `courses/simple-ai/module2.html`
- Modify: `courses/simple-ai/CH2-4.html`

**Interfaces:**
- Consumes: 已驗收的兩份 PDF 相對路徑。
- Produces: 本機與部署環境都能開啟的下載按鈕；有正式 URL 時才產 QR。

- [ ] **Step 1: 在首頁新增兩份教材入口**

連結固定使用 `assets/創業-AI-實戰手冊.pdf` 與 `assets/創業-AI-實戰-10則Prompt精選.pdf`，標示檔案用途，不寫未驗證頁數以外的宣傳數字。

- [ ] **Step 2: 修正第二堂導覽的 PDF 承諾**

把「拿到完整版 PDF 手冊 QR Code」改成可實際點擊的兩份教材連結。若已有正式公開網址且通過 HTTP 讀取測試，再加入 QR；否則不加入 QR 元件。

- [ ] **Step 3: 修正結訓頁**

新增教材下載區與十條工作流入口；移除「QR Code 落地頁有 Google Form，作業會逐一回覆」等目前沒有實際表單與服務證據的承諾，保留可執行的三選一課後作業。

- [ ] **Step 4: 驗證相對連結與 stale copy**

Run:

```bash
rg -n '創業-AI-實戰手冊\.pdf|創業-AI-實戰-10則Prompt精選\.pdf' courses/simple-ai/index.html courses/simple-ai/module2.html courses/simple-ai/CH2-4.html
rg -n 'QR Code 落地頁有 Google Form|稍後提供|href="#"' courses/simple-ai/index.html courses/simple-ai/module2.html courses/simple-ai/CH2-4.html
test -s courses/simple-ai/assets/創業-AI-實戰手冊.pdf
test -s courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf
```

Expected: 三頁皆有兩份教材的有效相對路徑；stale copy 與空連結零命中；兩份 PDF 非空。

- [ ] **Step 5: 跑三頁 lint**

Run:

```bash
python3 docs/lint-page.py courses/simple-ai/index.html --summary
python3 docs/lint-page.py courses/simple-ai/module2.html --summary
python3 docs/lint-page.py courses/simple-ai/CH2-4.html --summary
```

Expected: 三次皆 exit 0。

- [ ] **Step 6: 工作包 D 停看點**

向使用者提交三個入口頁、連結檢查與 QR 是否因正式網址條件而納入。未獲核准，不進最終收尾。

---

### Task 7: 全課驗證、報告與精確提交

**Files:**
- Modify: `search-index.json`（由既有建置腳本產生於站根目錄）
- Modify: `sitemap.xml`（由既有建置腳本產生於站根目錄）
- Create: `courses/simple-ai/_repair/2026-08-25/REPAIR-REPORT.md`

**Interfaces:**
- Consumes: A–D 全部已驗收成果。
- Produces: 可稽核的 lint、PDF、連結、還原與提交證據。

- [ ] **Step 1: 跑整課 lint**

Run:

```bash
python3 docs/lint-page.py courses/simple-ai/ --summary
```

Expected: exit 0；若新印刷 HTML 不屬於一般課程頁契約而被 lint 拒絕，報告中必須逐項說明，不能以排除參數掩蓋真正 BLOCKER。

- [ ] **Step 2: 重建搜尋索引與 sitemap**

Run:

```bash
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
```

Expected: 兩次 exit 0。

- [ ] **Step 3: 執行 PDF 最終回歸**

Run:

```bash
node courses/simple-ai/_tools/build-deliverables.js all
pdfinfo courses/simple-ai/assets/創業-AI-實戰手冊.pdf | rg '^Pages:'
pdfinfo courses/simple-ai/assets/創業-AI-實戰-10則Prompt精選.pdf | rg '^Pages:[[:space:]]+2$'
bash -n courses/simple-ai/_tools/restore-2026-08-25-pre-deliverables.sh
```

Expected: 完整版 55–65 頁、精華版 2 頁、還原腳本語法正確。

- [ ] **Step 4: 冷啟動走讀**

以未讀過課程的學員順序完成：首頁下載 → EF-08 設定 → 會議輸出 → NotebookLM 品牌庫 → Gemini 草稿 → 回 NotebookLM 查核 → FAQ → 下載精華版。每一步記錄起始素材、完成物、判斷點、卡關恢復；任何核心素材缺失即驗收失敗。

- [ ] **Step 5: 寫入 REPAIR-REPORT**

報告逐檔列出變更，附上：整課 lint、兩份 PDF 頁數、逐頁渲染、十代碼、平台查證、三頁下載連結、搜尋索引、sitemap、冷啟動走讀、備份與還原腳本結果。QR 未執行時列入 `Remaining`，原因固定為「缺已驗證正式公開網址」。

- [ ] **Step 6: 精確檢查 staged scope**

Run:

```bash
git status --short -- courses/simple-ai search-index.json sitemap.xml
git diff --check
git diff --cached --name-only
```

只以明確路徑 `git add` 本計畫檔案；不得加入其他課程或使用者原有 dirty files。

- [ ] **Step 7: 依工作包建立可審計提交**

建議提交邊界：

```text
feat(simple-ai): add printable handbook deliverable
feat(simple-ai): add two-page prompt reference
feat(simple-ai): add verified NotebookLM Gemini workflow
feat(simple-ai): connect course download deliverables
docs(simple-ai): record deliverable repair verification
```

每次 commit 前只暫存該工作包的明列檔案，並確認 pre-commit hook 通過。

---

## Final Definition of Done

- 工作包 A、B、C、D 均分別取得使用者核准。
- 完整版 PDF 55–65 頁且完整範例契約八項全數成立。
- 精華版 PDF 恰為兩頁，十則 Prompt 齊全且與完整版一致。
- 雙向工作流有官方／實機查證、完整示範、來源查核與免費手機備援。
- 三個課程入口可開啟兩份真實 PDF，沒有假 QR、空連結或不存在的 Google Form 承諾。
- 整課 lint、搜尋索引、sitemap、PDF 回歸、冷啟動走讀與還原腳本均有實際證據。
