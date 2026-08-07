# Digital Marketing 70h Learning Path Repair Plan

**Execution status:** Completed on 2026-07-19. Verification evidence is recorded in `REPAIR-REPORT.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 讓零基礎學員依序建立 AI 與數位行銷能力，並把前九個模組的階段產物整合成 M10 完整企劃案。

**Architecture:** 不重排 10 個模組，不刪除既有教學內容。以「角色重整 + 承接產物 + 整合來源欄位」修正學習路徑，將首次教學、渠道深化與專案整合明確分開。

**Tech Stack:** HTML5、inline CSS、原生 JavaScript、Markdown、`docs/lint-page.py`。

## Global Constraints

- 修改前建立 `_backup/2026-07-19-pre-repair/` 與可執行還原腳本。
- 每批修改 1–3 頁後跑單頁 lint。
- 不刪除既有段落；本計畫只修改定位文字、學習目標、承接提示與產物驗收欄位。
- HTML 規則以 `docs/lint-page.py` 為準。
- 全部完成後重建 search index 與 sitemap。

---

### Task 1：建立可回復基線

**Files:**
- Create: `digital-marketing-70h/_backup/2026-07-19-pre-repair/`
- Create: `digital-marketing-70h/_tools/restore-2026-07-19-pre-repair.sh`

- [x] 備份本計畫列出的 13 個 HTML 目標頁。
- [x] 建立逐檔還原腳本，不使用萬用字元覆蓋整課。
- [x] 執行 `bash -n`；預期 exit 0。

### Task 2：修正文案首次教學角色

**Files:**
- Modify: `digital-marketing-70h/m2c-1-text.html`
- Modify: `digital-marketing-70h/m3-2-audience.html`
- Modify: `digital-marketing-70h/m3-4-positioning.html`

**Produces:** M2C 共通 AI 文案基礎、M3 真實品牌策略輸入。

- [ ] M2C-1 Hero 與 outcomes 明示此時使用範例 brief，學習生成、人工判斷與查核，不宣稱已完成渠道策略。
- [ ] M2C-1 增加「進入 M3 前保存」產物：`copy-workflow.md`，包含 Prompt、初稿、人工修訂與採納理由。
- [ ] M3-2 Persona 產物加入「提供給後續文案／渠道單元」欄位。
- [ ] M3-4 定位產物加入核心訊息與證據，作為 M4–M9 的共同輸入。
- [ ] 逐頁 lint；預期 0 BLOCKER、0 ERROR。

### Task 3：建立渠道文案深化鏈

**Files:**
- Modify: `digital-marketing-70h/m4-1-attention.html`
- Modify: `digital-marketing-70h/m4-3-shortform.html`
- Modify: `digital-marketing-70h/m5-4-onpage.html`
- Modify: `digital-marketing-70h/m8-2-copywriting.html`
- Modify: `digital-marketing-70h/m9-2-email-psychology.html`
- Modify: `digital-marketing-70h/m9-3-lead-magnet.html`

**Consumes:** `copy-workflow.md`、M3 Persona、定位與核心訊息。
**Produces:** 各渠道可驗收的文案變體與選擇理由。

- [ ] M4-1 限定為自然內容停留與觀看訊號，產物含 Hook 假設。
- [ ] M4-3 明示承接 M2C-3 的 AI 製作流程，新增平台、情緒弧線與 CTA 決策。
- [ ] M5-4 要求 SEO 內容引用搜尋意圖、Persona 與核心訊息。
- [ ] M8-2 把 Hook 改成付費廣告深化：漏斗階段、版位、KPI 與 A/B 假設。
- [ ] M9-2 明示 Email 分層承接 M2C 預覽，加入名單來源與行為訊號。
- [ ] M9-3 Landing Page 文案引用 Lead Magnet、Persona、核心訊息與轉換目標。
- [ ] 逐頁 lint；預期 0 BLOCKER、0 ERROR。

### Task 4：把 M10 從重教改為整合

**Files:**
- Modify: `digital-marketing-70h/m10-1-kickoff.html`
- Modify: `digital-marketing-70h/m10-2-strategy.html`
- Modify: `digital-marketing-70h/m10-3-execution.html`
- Modify: `digital-marketing-70h/m10-4-presentation.html`

**Consumes:** M1–M9 階段產物。
**Produces:** kickoff brief、strategy brief、execution pack、final A3。

- [ ] M10-1 將 Persona／旅程改成匯入、證據校正與版本鎖定，不再作首次教學。
- [ ] M10-2 的渠道、KPI 與 90 天計畫加入來源欄位及取捨理由。
- [ ] M10-3 的 SEO、內容與 GTM 三項產物分別引用 M3/M4/M5/M7/M10-2 輸入。
- [ ] M10-4 A3 增加 AI 使用紀錄、關鍵假設與下一輪優化，不把企劃壓縮成只剩六格摘要。
- [ ] 逐頁 lint；預期 0 BLOCKER、0 ERROR。

### Task 5：全課驗收與交付

**Files:**
- Modify: `search-index.json`
- Modify: `sitemap.xml`
- Create: `digital-marketing-70h/_repair/2026-07-19/REPAIR-REPORT.md`

- [ ] 跑 `python3 docs/lint-page.py courses/digital-marketing-70h/ --summary`；預期 0 BLOCKER、0 ERROR。
- [ ] 跑 `python3 docs/build-search-index.py`；預期成功產出索引。
- [ ] 跑 `python3 docs/build-sitemap.py`；預期成功產出 sitemap。
- [ ] 搜尋 `copy-workflow.md`、`Persona`、`核心訊息`、`來源產物`、`A/B 假設`，確認能力鏈跨模組存在。
- [ ] 完成報告，列出修改檔、驗證結果、剩餘 WARN 與還原方式。

---

## 課後素材包全面修復（2026-07-19 追加授權）

### Scope

- 補齊 M10-1～M10-4 可直接填寫的完整模板。
- 建立 M2→M3→M10 跨模組產物接力工作簿。
- Persona PDF 保留為完成範例，另增可填寫、可標證據狀態的 Excel。
- 補強復跑手冊 M6～M10 的起始狀態、預期結果、快速檢查與卡關處理。
- 將固定績效數字改為示範門檻，要求依品牌基線與樣本量調整。

### Files

- Modify: `assets/after-class-guide.md`
- Modify: `assets/datasets/prompts-all.md`
- Modify: `assets/datasets/persona-templates.md`
- Modify: `index.html`
- Modify/Create: `_tools/build-student-pdfs.py`
- Create: `_tools/build-learning-workbooks.mjs`
- Create: `assets/downloads/Persona研究與受眾簡報.xlsx`
- Create: `assets/downloads/整合行銷企劃工作簿.xlsx`

### Acceptance

- M10 四階段不再出現「同課程頁 deliverable」占位文字。
- Persona 工作簿含六維度、證據狀態、來源、訪談紀錄與版本日期。
- 整合工作簿依產物鏈分頁，M10 A3 可追溯到前置 brief 與執行證據。
- M6～M10 每個復跑案例都有準備、產物、快速檢查與卡住時處理。
- PDF、兩份新 Excel 逐頁／逐表渲染檢查，無截字與公式錯誤。
- 首頁所有下載連結存在；整課 lint 為 0 BLOCKER、0 ERROR。
