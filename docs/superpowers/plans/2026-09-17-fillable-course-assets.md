# 可填寫課程資產生成機制 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將數位內容與成長行銷人才培訓的 HTML 資產生成器，從「閱讀版另存檔案」改成能區分參考資產與學員工作表，並為工作表提供可填寫、離線儲存與完成版匯出的 learner path。

**Architecture:** 以資產名稱與明確規則判定 `worksheet` 或 `reference`。閱讀版保留完整教學內容；`worksheet` 工作版在生成時把可回答的表格欄位轉成 `<textarea>`／checkbox，注入自足的儲存與匯出 runtime；`reference` 只生成可攜式閱讀版，不再假裝是工作表。所有下載檔仍由同一個生成器產生，測試直接檢查產物契約。

**Tech Stack:** Python 3、BeautifulSoup、既有 Pandoc Markdown 轉換、原生 HTML/CSS/JavaScript、Python unittest。

**Spec:** `courses/digital-content-growth-126h/_repair/2026-09-17/REPAIR-PLAN.md`

## Global Constraints

- 生成後的學員工作版不依賴外部 CSS、JavaScript、伺服器或帳號。
- 不刪除原有教學內容；工作版只能增加填寫介面、操作說明與交付工具。
- 參考完成品、案例、術語與資料資產不生成可填寫假介面。
- 每個 worksheet 必須有起始說明、可填欄位、儲存草稿、下載完成版與完成檢查。
- Windows 瀏覽器可直接開啟；localStorage 不可用時，下載完成版仍可運作。
- 先以 CH1-1 的工作流驗證，再由同一機制重建全課；不逐頁手工 patch。

---

### Task 1: 建立修復記錄與可回復備份

**Files:**
- Create: `courses/digital-content-growth-126h/_repair/2026-09-17/REPAIR-PLAN.md`
- Create: `courses/digital-content-growth-126h/_backup/2026-09-17-pre-fillable-workbook-repair/html/`
- Create: `courses/digital-content-growth-126h/_tools/restore-2026-09-17-pre-fillable-workbook-repair.sh`

- [ ] **Step 1: 備份本次會重建的 generator、測試、主課頁與所有 HTML 資產。**
- [ ] **Step 2: 建立 restore script，使用明確來源與目標路徑，不碰其他課程。**
- [ ] **Step 3: 以 `bash -n` 驗證 restore script。**

### Task 2: 先寫資產分類與 learner contract 的失敗測試

**Files:**
- Modify: `courses/digital-content-growth-126h/_tools/test_learner_render_contract.py`

**Interfaces:**
- `data-workbook-kind="worksheet"`：必須有文字欄位、儲存按鈕、完成版匯出按鈕與 inline runtime。
- `data-workbook-kind="reference"`：不可出現儲存／匯出工作表控制項。
- 閱讀版下載文字必須與資產類型一致。

- [ ] **Step 1: 新增 worksheet/reference 產物契約測試。**
- [ ] **Step 2: 新增保存、Blob 匯出、離線備援的 runtime token 測試。**
- [ ] **Step 3: 執行測試並確認目前產物因沒有欄位與 runtime 而失敗。**

### Task 3: 在 generator 建立資產分類與表格欄位轉換

**Files:**
- Modify: `courses/digital-content-growth-126h/_tools/rebuild-learner-shell.py`

**Interfaces:**
- `asset_kind_for_code(code: str) -> str` 回傳 `worksheet` 或 `reference`。
- `work_download_name(code: str, kind: str) -> str` 產生不與舊下載檔撞名的使用者檔名。
- `build_fillable_asset_fragment(html: str, code: str) -> str` 將 worksheet 的表格資料欄轉為可填寫欄位。
- `workbook_runtime() -> str` 回傳不依賴網路的儲存與完成版匯出 JavaScript。

- [ ] **Step 1: 建立 reference pattern 與 worksheet default 規則，並在工作版 body 宣告 kind。**
- [ ] **Step 2: 對 worksheet 表格的第一欄保留欄位名稱，後續資料欄生成提示文字與 textarea；空白 checkbox 保留可勾選。**
- [ ] **Step 3: 對以冒號結尾的清單項目生成補充欄位，沒有可推斷欄位時提供通用補充欄位。**
- [ ] **Step 4: 注入工作版操作面板、狀態文字與完成檢查。**
- [ ] **Step 5: 注入 localStorage 儲存、清除、完成版 HTML Blob 匯出，以及 localStorage 不可用時的備援訊息。**
- [ ] **Step 6: reference 資產改顯示「參考版」，不出現可填寫工作表按鈕。**

### Task 4: 以 CH1-1 重新生成並完成冷跟做驗證

**Files:**
- Generated: `courses/digital-content-growth-126h/CH1-1.html`
- Generated: `courses/digital-content-growth-126h/assets/templates/CH1-1-工作版.html`

- [ ] **Step 1: 重新生成 CH1-1 的閱讀版與工作版。**
- [ ] **Step 2: 確認 CH1-1 有起始說明、文字欄位、勾選、儲存草稿與下載完成版。**
- [ ] **Step 3: 用本機 HTTP server 開啟頁面，實際填寫一個欄位、儲存、重新載入並匯出完成版。**
- [ ] **Step 4: 檢查匯出的完成版包含輸入值，不含編輯工具列。**

### Task 5: 全課重建與驗收

**Files:**
- Generated: `courses/digital-content-growth-126h/*.html`
- Generated: `courses/digital-content-growth-126h/assets/templates/*.html`
- Modify: `courses/digital-content-growth-126h/_validation/L5-evidence-manifest.json`

- [ ] **Step 1: 重新生成 47 個教學頁與 126 組資產頁。**
- [ ] **Step 2: 執行 21 項 learner render contract tests。**
- [ ] **Step 3: 執行全課 lint、內容實質審計與 `git diff --check`。**
- [ ] **Step 4: 重新統計 worksheet/reference 分布，確認沒有 worksheet 缺少文字欄位。**
- [ ] **Step 5: 產出 `REPAIR-REPORT.md`，列出剩餘需要人工判斷的教學內容問題。**

### Task 6: 提交與發布門檻

- [ ] **Step 1: 只 stage 本課程、修復計畫、測試與 generator，不納入其他課程工作區變更。**
- [ ] **Step 2: 建立修復 commit。**
- [ ] **Step 3: 發布前確認 public lesson 與直接工作版均回傳 200，且 live HTML 含 workbook contract。**
