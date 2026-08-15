# Render Quick Deployment Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立一份不綁定特定課程或觀看對象的繁體中文 Render 快速部署單頁，提供含後端 AI App 的最短部署、驗收與排錯路徑。

**Architecture:** 只新增一個自包含 HTML，內嵌 CSS 與少量複製按鈕 JavaScript，不修改課程導覽、搜尋索引、sitemap 或其他頁面。內容採由上而下的單一路徑，先說明免費方案限制，再依序呈現準備、六步部署、完成驗收與五類排錯。

**Tech Stack:** HTML5、inline CSS、原生 JavaScript、`docs/lint-page.py`、`rg`、官方 Render 文件。

**Spec:** `courses/gen-ai-140h/_repair/2026-08-15/RENDER-QUICK-GUIDE-DESIGN.md`

## Global Constraints

- 成品路徑固定為 `courses/gen-ai-140h/render-deploy-quick-guide.html`。
- 頁面內不出現「學員」「140 小時課程」「本課」、特定機構或觀看對象。
- 專案來源可包含 AI Studio，但不得暗示只適用 AI Studio。
- 不加入 Vercel、Railway 或 Google 的部署流程。
- 不宣稱 Render 永久免費，也不要求使用者綁定信用卡。
- 不示範將真實 API key 寫進 HTML、前端 JavaScript、GitHub 或截圖。
- 不修改 index、search-index、sitemap 或其他課程檔案。
- 不 push 到 GitHub。

---

### Task 1: 建立通用 Render 快速部署單頁

**Files:**
- Create: `courses/gen-ai-140h/render-deploy-quick-guide.html`
- Read: `courses/gen-ai-140h/_repair/2026-08-15/RENDER-QUICK-GUIDE-DESIGN.md`
- Reference: `courses/gen-ai-140h/part5/CH5-4.html`
- Reference: `_規範/design-tokens.md`

**Interfaces:**
- Consumes: 核准規格中的資訊架構、文案邊界與驗收標準，以及官方 Render 文件確認後的當前介面名稱與免費方案限制。
- Produces: 一個可直接以瀏覽器開啟的獨立 HTML；複製按鈕以 `data-copy-target` 指向同頁 code block `id`，成功時短暫顯示「已複製」。

- [ ] **Step 1: 以官方資料重新確認會寫進頁面的易變資訊**

只使用 Render 官方文件，核對以下項目：

- 建立服務的介面路徑是否仍為 Dashboard → New + → Web Service。
- Node.js 的 Build Command、Start Command 與環境變數設定位置。
- Web Service 對 `PORT` 與 host binding 的要求。
- Free instance 的休眠、冷啟動、免費額度與付款方式行為。

Expected: 每個易變敘述都有官方來源支持；若官方現況與規格不同，以官方現況為準，並維持「不承諾永久免費」的邊界。

- [ ] **Step 2: 建立失敗的內容錨點檢查**

Run:

```bash
test -f courses/gen-ai-140h/render-deploy-quick-guide.html
```

Expected: FAIL，因為檔案尚未建立。

- [ ] **Step 3: 建立完整單頁骨架與內容**

使用 `apply_patch` 新增 HTML，必須包含以下語意結構與文字錨點：

```html
<main id="main">
  <section id="limits">...</section>
  <section id="prepare">...</section>
  <section id="deploy">...</section>
  <section id="verify">...</section>
  <section id="troubleshoot">...</section>
</main>
```

部署區包含六張依序編號的操作卡：

1. 專案推送到 GitHub。
2. Dashboard → New + → Web Service 並連接 repository。
3. 選擇 Node runtime，設定 Build Command 與 Start Command。
4. 在 Environment 加入 API key，範例名稱使用 `OPENAI_API_KEY`，值只顯示 `貼上你的金鑰`。
5. Deploy 後到 Events／Logs 確認服務啟動。
6. 開啟 `.onrender.com` 網址並執行正式環境測試。

排錯區必須分成五張卡，每張都包含「看到什麼／去哪裡查／怎麼修」：

- Start Command 錯誤。
- 未使用 `process.env.PORT` 或沒有綁定 `0.0.0.0`。
- Environment variable 名稱不一致。
- `package.json` dependencies 遺漏。
- Render Free 冷啟動與真正部署失敗的辨別。

視覺要求：暖白底、棕色主色、單欄閱讀、桌面最大寬度、手機斷點、code block 可橫向捲動、focus-visible 清楚、無外部 JavaScript 依賴。

- [ ] **Step 4: 實作最小複製功能**

每個需要複製的指令使用：

```html
<button type="button" class="copy-btn" data-copy-target="start-command">複製</button>
<code id="start-command">npm start</code>
```

頁尾加入單一事件委派：讀取 `data-copy-target`、呼叫 `navigator.clipboard.writeText()`、成功時將按鈕文字切換成「已複製」，1.5 秒後恢復；失敗時改為「請手動複製」。

- [ ] **Step 5: 執行內容錨點與禁語檢查**

Run:

```bash
rg -n 'New \+|Web Service|Build Command|Start Command|Environment|Events|Logs|process\.env\.PORT|0\.0\.0\.0|onrender\.com|冷啟動' courses/gen-ai-140h/render-deploy-quick-guide.html
! rg -n '學員|140 小時|本課|弄一下工作室|Railway|Vercel|Google 部署' courses/gen-ai-140h/render-deploy-quick-guide.html
```

Expected: 第一個指令完整命中所有操作錨點；第二個指令為 exit 0 且沒有輸出。

- [ ] **Step 6: 執行頁面 lint**

Run:

```bash
python3 docs/lint-page.py courses/gen-ai-140h/render-deploy-quick-guide.html
```

Expected: BLOCKER 0、ERROR 0。

- [ ] **Step 7: Scoped commit**

```bash
git add -- courses/gen-ai-140h/render-deploy-quick-guide.html
git commit -m "docs(gen-ai-140h): add standalone Render quick guide"
```

---

### Task 2: 驗證獨立性、連結與手機版結構

**Files:**
- Verify: `courses/gen-ai-140h/render-deploy-quick-guide.html`
- Verify unchanged: `search-index.json`
- Verify unchanged: `sitemap.xml`
- Verify unchanged: `courses/gen-ai-140h/index.html`

**Interfaces:**
- Consumes: Task 1 產出的單一 HTML。
- Produces: 可稽核的最終驗證結果；不產生或修改其他檔案。

- [ ] **Step 1: 驗證 HTML 基本結構與連結格式**

Run:

```bash
rg -n '<meta charset="UTF-8">|<meta name="viewport"|<main id="main">|id="limits"|id="prepare"|id="deploy"|id="verify"|id="troubleshoot"' courses/gen-ai-140h/render-deploy-quick-guide.html
rg -o 'https://[^" ]+' courses/gen-ai-140h/render-deploy-quick-guide.html
```

Expected: 必要結構全部命中；外部連結全為 HTTPS，且只連到 GitHub 或 Render 官方網域。

- [ ] **Step 2: 驗證響應式與鍵盤操作錨點**

Run:

```bash
rg -n '@media.*max-width|overflow-x:auto|focus-visible|aria-label|type="button"' courses/gen-ai-140h/render-deploy-quick-guide.html
```

Expected: 手機斷點、程式碼橫向捲動、focus 樣式與按鈕語意均有命中。

- [ ] **Step 3: 驗證沒有改動禁止範圍**

Run:

```bash
git status --short -- courses/gen-ai-140h/render-deploy-quick-guide.html courses/gen-ai-140h/index.html search-index.json sitemap.xml
git diff HEAD^ --name-only
```

Expected: 最新實作 commit 只包含 `courses/gen-ai-140h/render-deploy-quick-guide.html`；index、search-index 與 sitemap 沒有本次變更。

- [ ] **Step 4: 最終 lint 與 diff 檢查**

Run:

```bash
python3 docs/lint-page.py courses/gen-ai-140h/render-deploy-quick-guide.html --summary
git diff --check HEAD^
```

Expected: BLOCKER 0、ERROR 0；diff check 沒有輸出。

- [ ] **Step 5: 保留本地，不 push**

Run:

```bash
git log -1 --oneline
git status --short
```

Expected: 可看到本地實作 commit；不執行任何 `git push` 指令，並明確回報成品路徑。

