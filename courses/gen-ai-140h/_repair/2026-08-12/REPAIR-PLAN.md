# Vercel／Render 部署角色一致化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 gen-ai-140h 全課部署建議統一為 Render 含後端主路徑、Vercel Hobby 個人非商業作品補充路徑，以及 GitHub Pages 純靜態路徑。

**Architecture:** 先建立全 scope 備份與還原腳本，再依「核心操作頁、靜態／作品頁、專題延伸頁、大綱與導覽」分批修正。每批先用文字錨點證明舊敘述存在，精準修改後以相同錨點、頁面 lint 與跨頁語意搜尋驗收；不重構 HTML、CSS 或 JavaScript。

**Tech Stack:** HTML5、inline CSS／JavaScript、Markdown、Python `docs/lint-page.py`、`rg`、Git。

## Global Constraints

- `Render Free Web Service` 是含 Node.js／Express 後端與可能商用情境的主方案。
- `Vercel Hobby` 只定位為個人作品集、課堂練習與非商業 Demo 的補充方案。
- `GitHub Pages` 只用於純靜態輸出，且不得包含必須保密的 API key。
- Railway 不再作為免費主路徑，也不得描述為可長期免費使用。
- Render 免費限制在第一次操作前說明：閒置 15 分鐘休眠、冷啟動約一分鐘、無付款方式超額時暫停、不適合正式 production SLA。
- 完整 Vercel 條款集中在核心判斷頁；其他頁只用 `Vercel Hobby（個人非商業）` 等精簡標註。
- 只修改本計畫列出的 19 個 HTML 與 `_outlines/gen-ai-140h.md`，不改版型、色彩、互動元件或無關課程內容。
- 修改前備份全部 20 個來源檔並建立可執行 restore script。
- mixed worktree 中既有修改不納入本次 staging；每次只 `git add --` 明列檔案。

---

## Scope 與檔案責任

**核心操作頁**

- Modify: `courses/gen-ai-140h/part4/CH4-3.html`
- Modify: `courses/gen-ai-140h/part5/CH5-4.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-2.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-4.html`

**作品展示與延伸引用**

- Modify: `courses/gen-ai-140h/fun-apps.html`
- Modify: `courses/gen-ai-140h/index.html`
- Modify: `courses/gen-ai-140h/my-progress.html`
- Modify: `courses/gen-ai-140h/part4/PRAC4-4.html`
- Modify: `courses/gen-ai-140h/part5/CH5-3.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-1.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-3.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-15.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-16.html`

**進階與專題引用**

- Modify: `courses/gen-ai-140h/part6/CH6-2.html`
- Modify: `courses/gen-ai-140h/part7/CH7-2.html`
- Modify: `courses/gen-ai-140h/part7/CH7-4.html`
- Modify: `courses/gen-ai-140h/part7/PRAC7-1.html`
- Modify: `courses/gen-ai-140h/part7/PRAC7-4.html`
- Modify: `courses/gen-ai-140h/part7/PRAC7-5.html`

**規格與稽核產物**

- Modify: `_outlines/gen-ai-140h.md`
- Create: `courses/gen-ai-140h/_repair/2026-08-12/SCAN.md`
- Create: `courses/gen-ai-140h/_backup/2026-08-12-pre-vercel-render/`
- Create: `courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh`
- Create: `courses/gen-ai-140h/_repair/2026-08-12/REPAIR-REPORT.md`

---

### Task 1: 建立 scan、全 scope 備份與還原閘門

**Files:**

- Create: `courses/gen-ai-140h/_repair/2026-08-12/SCAN.md`
- Create: `courses/gen-ai-140h/_backup/2026-08-12-pre-vercel-render/...`
- Create: `courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh`

**Interfaces:**

- Consumes: `VERCEL-RENDER-DESIGN.md` 的平台角色與本計畫 Scope。
- Produces: 可回滾的 20 檔快照、逐檔 restore 映射、平台文字基線。

- [ ] **Step 1: 產生修改前語意基線**

Run from repository root:

```bash
rg -n -i 'Vercel|Railway|Render'   _outlines/gen-ai-140h.md courses/gen-ai-140h   --glob '*.html' --glob '*.md'   --glob '!_backup/**' --glob '!_repair/**'
```

Expected: 命中 19 個 HTML 與大綱；CH5-4、PRAC5-4 可看到 Railway UI、`.up.railway.app` 與免費主路徑殘留。

- [ ] **Step 2: 寫入 SCAN.md**

記錄 `STALE_UI`（Railway 操作）、`LEARNER_PATH`（平台角色不一致）、`CONTENT_THIN`（Vercel 商業邊界缺漏）、Activity Identity 不變理由與 Shared Copy Audit。

- [ ] **Step 3: 逐檔建立備份**

以 Scope 為唯一清單，把 19 個 HTML 與大綱複製到 `courses/gen-ai-140h/_backup/2026-08-12-pre-vercel-render/`，保留 repo 相對結構，不使用 glob 擴張範圍。

- [ ] **Step 4: 建立 restore script**

腳本解析自身所在 repo、逐一檢查 20 個來源、逐一複製回原路徑、任一缺檔立即非零退出；不得使用 `rm`、`git reset` 或寬泛 glob。

- [ ] **Step 5: 驗證 restore**

```bash
bash -n courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh
rg -n '^restore_one ' courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh
```

Expected: `bash -n` exit 0；恰有 20 筆 `restore_one` 呼叫。

- [ ] **Step 6: scoped commit**

```bash
git add -- courses/gen-ai-140h/_repair/2026-08-12/SCAN.md   courses/gen-ai-140h/_backup/2026-08-12-pre-vercel-render   courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh
git diff --cached --check
git commit -m "chore(gen-ai-140h): back up deployment platform content"
```

### Task 2: 將 CH5-4 與 PRAC5-4 改為 Render 可跟做主線

**Files:**

- Modify: `courses/gen-ai-140h/part5/CH5-4.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-4.html`

**Interfaces:**

- Consumes: 現有 Node.js／Express、`process.env.PORT`、`OPENAI_API_KEY` 教學骨架。
- Produces: Render Dashboard 可完整跟做的主線，供 Part 7 與大綱引用。

- [ ] **Step 1: 證明舊操作存在**

```bash
rg -n 'railway\.app|\.up\.railway\.app|New Project|Generate Domain|Railway 常見問題|Railway 或 Render'   courses/gen-ai-140h/part5/CH5-4.html   courses/gen-ai-140h/part5/PRAC5-4.html
```

Expected: 有命中；完成後這些舊主線錨點必須歸零。

- [ ] **Step 2: 改寫 CH5-4 最短可跑路徑**

保留五步節奏與程式碼，部署段改為 Render：GitHub＋Render＋API key 準備、`onrender.com` 成功網址、`New + → Web Service`、Node runtime、`npm install`、`npm start`、Free instance、Environment 與 Logs。操作前加入休眠、冷啟動、超額暫停與非 production 限制；排錯明列 `0.0.0.0`、`process.env.PORT`、Start Command 與環境變數拼字。

- [ ] **Step 3: 改寫 PRAC5-4 全部依賴文案**

同步準備、STEP 3／4、結果檢查、常見卡點、placeholder、參考答案、prompt 與 rubric。Vercel 只能作個人非商業 serverless 補充，不與 Express Render 主線並列為等價一鍵操作。

- [ ] **Step 4: 驗證新舊錨點**

```bash
! rg -n 'railway\.app|\.up\.railway\.app|Generate Domain|Railway 常見問題|Railway 或 Render'   courses/gen-ai-140h/part5/CH5-4.html   courses/gen-ai-140h/part5/PRAC5-4.html
rg -n 'onrender\.com|New Web Service|Build Command|Start Command|OPENAI_API_KEY|15 分鐘|冷啟動'   courses/gen-ai-140h/part5/CH5-4.html   courses/gen-ai-140h/part5/PRAC5-4.html
```

Expected: 舊錨點歸零；兩頁都有新操作與限制錨點。

- [ ] **Step 5: lint 與 commit**

```bash
python3 docs/lint-page.py courses/gen-ai-140h/part5/CH5-4.html
python3 docs/lint-page.py courses/gen-ai-140h/part5/PRAC5-4.html
git add -- courses/gen-ai-140h/part5/CH5-4.html courses/gen-ai-140h/part5/PRAC5-4.html
git diff --cached --check
git commit -m "fix(gen-ai-140h): move backend deployment lessons to Render"
```

Expected: lint exit 0，無 BLOCKER。

### Task 3: 校正靜態部署與個人作品展示路徑

**Files:**

- Modify: `courses/gen-ai-140h/part4/CH4-3.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-2.html`
- Modify: `courses/gen-ai-140h/fun-apps.html`
- Modify: `courses/gen-ai-140h/index.html`
- Modify: `courses/gen-ai-140h/my-progress.html`
- Modify: `courses/gen-ai-140h/part4/PRAC4-4.html`
- Modify: `courses/gen-ai-140h/part5/CH5-3.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-1.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-3.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-15.html`
- Modify: `courses/gen-ai-140h/part5/PRAC5-16.html`

**Interfaces:**

- Consumes: Vercel Hobby 個人非商業用途邊界、GitHub Pages 無私密 key 邊界。
- Produces: 靜態與作品頁一致的平台標籤。

- [ ] **Step 1: 列出 Vercel 決策點**

用 `rg -n -i -C 1 'Vercel'` 檢查本 Task 11 頁。Expected: 可逐筆分類為平台選擇、部署操作、導覽或純技術列舉。

- [ ] **Step 2: 改寫 CH4-3 與 PRAC5-2 完整判斷**

平台表明確區分：GitHub Pages＝純靜態無私密 key；Vercel Hobby＝個人非商業作品／課堂 Demo；Render＝含後端、公司／客戶或可能商用。PRAC5-2 的 Vercel 實作保留，但第一次 Deploy 前提示 Hobby 邊界；咖啡店客戶案例改選 GitHub Pages／Render。

- [ ] **Step 3: 精簡同步其餘九頁**

個人作品保留 `Vercel Hobby（個人非商業）`；公司、群組共享、受薪工作與客戶案例改指向 Render；純路徑相容性或技術棧列舉可保留原名。PRAC5-15／16 的 PRAC5-17 引用明示只適合個人非商業可分享 Demo。

- [ ] **Step 4: 驗證用途分流**

```bash
rg -n 'Vercel Hobby|個人非商業|個人、非商業|Render'   courses/gen-ai-140h/part4/CH4-3.html   courses/gen-ai-140h/part5/PRAC5-2.html   courses/gen-ai-140h/part5/PRAC5-15.html   courses/gen-ai-140h/part5/PRAC5-16.html
rg -n -C 2 '咖啡|客戶|公司|群組' courses/gen-ai-140h/part5/PRAC5-2.html
```

Expected: 核心兩頁有三路判斷；商業案例不推薦 Vercel Hobby。

- [ ] **Step 5: lint 11 頁**

逐頁執行 `python3 docs/lint-page.py <file>`。Expected: 全部 exit 0，無 BLOCKER。

- [ ] **Step 6: scoped commit**

只 stage 本 Task 11 頁，執行 `git diff --cached --check` 後提交：

```bash
git commit -m "fix(gen-ai-140h): bound Vercel to personal portfolio use"
```

### Task 4: 校正 Part 6／7 專題與職涯延伸

**Files:**

- Modify: `courses/gen-ai-140h/part6/CH6-2.html`
- Modify: `courses/gen-ai-140h/part7/CH7-2.html`
- Modify: `courses/gen-ai-140h/part7/CH7-4.html`
- Modify: `courses/gen-ai-140h/part7/PRAC7-1.html`
- Modify: `courses/gen-ai-140h/part7/PRAC7-4.html`
- Modify: `courses/gen-ai-140h/part7/PRAC7-5.html`

**Interfaces:**

- Consumes: Render 主路徑與 Vercel Hobby 補充路徑。
- Produces: 專題部署、成果發表與職涯建議不再延續錯誤免費或商用暗示。

- [ ] **Step 1: 列出六頁部署建議**

用 `rg -n -i -C 2 'Vercel|Railway|Render'` 檢查六頁。Expected: 可辨識靜態、含後端、成果展示與職涯工具棧情境。

- [ ] **Step 2: 依情境改寫**

靜態個人成果可用 GitHub Pages 或 Vercel Hobby；含後端專題使用 Render Free 並提醒冷啟動；公司／客戶／收費方向不得推薦 Hobby；職涯工具棧以 Render 作教學／原型，Vercel Pro 才對應專業或商業情境。Railway 只有必要比較才保留。

- [ ] **Step 3: 驗證舊描述歸零**

```bash
! rg -n 'Render / Railway（免費方案有睡眠機制）|Vercel / Railway 拿到公開網址'   courses/gen-ai-140h/part7
rg -n 'Vercel Hobby|Vercel Pro|Render|冷啟動|非商業'   courses/gen-ai-140h/part6/CH6-2.html courses/gen-ai-140h/part7
```

Expected: 舊描述歸零，各用途有對應角色標籤。

- [ ] **Step 4: lint 與 commit**

逐頁 lint 六頁，全部 exit 0 後只 stage 六頁，`git diff --cached --check`，提交：

```bash
git commit -m "fix(gen-ai-140h): align capstone deployment guidance"
```

### Task 5: 同步大綱與完成全課驗收

**Files:**

- Modify: `_outlines/gen-ai-140h.md`
- Create: `courses/gen-ai-140h/_repair/2026-08-12/REPAIR-REPORT.md`

**Interfaces:**

- Consumes: Tasks 2–4 已落地的平台角色。
- Produces: 大綱 SSOT、全課驗證證據、剩餘風險與 restore 入口。

- [ ] **Step 1: 同步大綱**

frontmatter tools 加入 Render 並保留 Vercel；PRAC5-2 明示 Vercel Hobby 個人非商業作品；PRAC5-4 改為 Render；PRAC5-17 改為個人非商業可分享 proxy Demo。不得改時數或其他 Part 結構。

- [ ] **Step 2: 全課平台語意搜尋**

```bash
rg -n -i 'Vercel|Railway|Render'   _outlines/gen-ai-140h.md courses/gen-ai-140h   --glob '*.html' --glob '*.md'   --glob '!_backup/**' --glob '!_repair/**'
```

Expected: 每個 Vercel 操作建議都有用途邊界或屬純技術列舉；Railway 沒有免費主路徑；Render 是 Express 後端主方案。

- [ ] **Step 3: 全課 lint**

```bash
python3 docs/lint-page.py courses/gen-ai-140h/ --summary
```

Expected: exit 0，無 BLOCKER。

- [ ] **Step 4: 重建索引與 sitemap**

```bash
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
```

Expected: 兩次 exit 0；只接受本次文案導致的生成差異，不 stage 無關檔案。

- [ ] **Step 5: Shared Copy Audit 與 restore 複驗**

```bash
rg -n '個人非商業|個人、非商業|Hobby.*非商業' courses/gen-ai-140h --glob '*.html'
bash -n courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh
```

Expected: 完整條款集中核心頁，其他頁是短標註；restore 語法通過。

- [ ] **Step 6: 寫 REPAIR-REPORT.md**

列出 Changed、lint、全課搜尋、Shared Copy Audit、search index、sitemap、remaining risk 與 restore script；明示免費方案屬時效性資訊，未來需由 course-refresh 重查。

- [ ] **Step 7: 最終 scoped commit**

只 stage 大綱、報告及確認屬本次的索引／sitemap 差異；不得使用 `git add -A`。

```bash
git diff --cached --check
git commit -m "docs(gen-ai-140h): finalize deployment platform guidance"
```

## 完成定義

- 20 個來源檔都有修改前備份，restore script 可通過語法與映射檢查。
- 19 個 HTML 的平台角色一致。
- CH5-4 與 PRAC5-4 可從零完成 Render 部署並處理常見錯誤。
- Vercel Hobby 只作個人非商業作品展示補充方案。
- 公司、客戶、受薪工作、收費與商業宣傳案例沒有 Hobby 部署建議。
- 所有修改頁 lint 通過，全課 lint exit 0。
- search index、sitemap、SCAN、REPAIR-REPORT 與 scoped Git evidence 齊全。
