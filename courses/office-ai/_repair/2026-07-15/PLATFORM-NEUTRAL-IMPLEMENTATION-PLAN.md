# Office AI Platform-Neutral Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 1.2 改寫為通用 LLM 與 NotebookLM（RAG）的工作模式差異，並移除全課對特定通用 LLM 的推薦與操作依賴。

**Architecture:** 保留 `CH1-2.html` URL 與六段課程結構，只替換學習目標、概念比較、示範與練習。全課使用「通用 LLM」作操作介面名稱，特定模型名稱只保留在既有實測 provenance；NotebookLM 保留作指定來源與引用回查工具。

**Tech Stack:** HTML5、inline CSS／JavaScript、Markdown、Python 課程 lint／索引產生器。

## Global Constraints

- 不改 `CH1-2.html` 檔名或章節編號。
- 不建立模型排行榜，不比較 ChatGPT、Gemini、Copilot 規格。
- 特定模型名稱只可留在實測 provenance，不可成為推薦或操作前置。
- NotebookLM 必須連結「指定來源、引用、回查、RAG」。
- 先建立本次增量備份與還原腳本，再修改 live HTML。
- CSS class 如 `.btn-drill-gemini` 不在本次重構範圍。

---

### Task 1: 建立增量備份與回復入口

**Files:**
- Create: `courses/office-ai/_backup/2026-07-15-pre-platform-neutral/`
- Create: `courses/office-ai/_tools/restore-2026-07-15-pre-platform-neutral.sh`
- Modify later: `courses/office-ai/index.html`、`ch1/CH1-1.html`、`ch1/CH1-2.html`、`ch1/CH1-3.html`、`ch1/CH1-4.html`、其餘含平台推薦字眼的 lesson HTML、`assets/after-class-guide.md`、`_outlines/office-ai.md`

**Interfaces:**
- Consumes: 目前 main 上 commit `5d72345` 的 office-ai live files。
- Produces: 保留相對路徑的備份檔與可執行 restore script。

- [ ] **Step 1: 列出 live 可見文字命中**

Run:
```bash
rg -n -i "ChatGPT|Gemini|Copilot|NotebookLM|主流工具|工具選擇" courses/office-ai _outlines/office-ai.md \
  --glob '*.html' --glob '*.md' --glob '!_backup/**' --glob '!_repair/**' --glob '!_validation/**'
```
Expected: 列出 1.2、首頁、導航、操作前置與案例 provenance；CSS class 命中不列為內容修改。

- [ ] **Step 2: 建立 scoped backup**

只備份確定會改的檔案，保留 `courses/office-ai/` 下相對路徑；大綱另存為 `outline/office-ai.md`。

- [ ] **Step 3: 建立 restore script**

Script 必須逐檔把備份複製回 live 路徑，最後提示重跑 lint、search index、sitemap。

- [ ] **Step 4: 驗證 restore script**

Run:
```bash
bash -n courses/office-ai/_tools/restore-2026-07-15-pre-platform-neutral.sh
```
Expected: exit 0。

### Task 2: 改寫 1.2 與全課平台用語

**Files:**
- Modify: `courses/office-ai/ch1/CH1-2.html`
- Modify: `courses/office-ai/index.html`
- Modify: `courses/office-ai/ch1/CH1-1.html`
- Modify: `courses/office-ai/ch1/CH1-3.html`
- Modify: `courses/office-ai/ch1/CH1-4.html`
- Modify: 其他掃描後確認含推薦／操作依賴字眼的 `courses/office-ai/ch*/CH*.html`
- Modify: `courses/office-ai/assets/after-class-guide.md`
- Modify: `_outlines/office-ai.md`

**Interfaces:**
- Consumes: `PLATFORM-NEUTRAL-DESIGN.md` 的內容邊界。
- Produces: 平台中立課程文案與新的 1.2 工作模式判斷卡。

- [ ] **Step 1: 改寫 1.2 metadata 與 Hero**

使用標題「通用 LLM 與 NotebookLM：生成與依據來源的差異」。學習成果必須包含：判斷自由生成或指定來源、知道何時要求引用回查、完成工作模式判斷卡。

- [ ] **Step 2: 改寫 1.2 六段正文**

正文只比較：

```text
通用 LLM：依指令生成、改寫、摘要、發想；可使用一般知識與推論，重要事實需人工回查。
NotebookLM（RAG）：先指定來源，再依來源回答並提供引用；適合多文件查找與需要回查依據的任務。
```

保留同一份逐字稿的對照示範，但將判準寫成「是否限定來源、是否附引用、是否能回到原文」。

- [ ] **Step 3: 改寫 1.2 產出物與四題練習**

產出物名稱改為「工作模式判斷卡」。四題至少涵蓋：邀請信起草、短文改寫、多文件共同規定、逐句附來源摘要；答案只在「通用 LLM／NotebookLM」間判斷並附人工查核點。

- [ ] **Step 4: 同步首頁、大綱與導航名稱**

將「主流工具介紹」統一改成「通用 LLM 與 NotebookLM」，首頁工具 chips 改成「通用 LLM」「NotebookLM（RAG）」；素材說明改成貼入「你慣用的通用 LLM」。

- [ ] **Step 5: 同步操作前置與平台聲明**

將「開啟 ChatGPT 或 Gemini」等操作指示改為「開啟你慣用的通用 LLM」。保留「本頁示範以 Gemini 免費版實測」的 provenance，但刪除「換其他平台結論一樣」等未驗證聲明。

課後手冊同步將 Gemini 專屬上傳、等待與歷史紀錄指示改成通用 LLM 可執行描述；多文件、指定來源與引用回查仍導向 NotebookLM。

- [ ] **Step 6: 執行平台字眼審計**

Run:
```bash
rg -n -i "ChatGPT|Gemini|Copilot" courses/office-ai \
  --glob '*.html' --glob '!_backup/**' --glob '!_repair/**' --glob '!_validation/**'
```
Expected: 可見文字只剩案例 provenance；CSS class 命中可保留。

### Task 3: 驗證並更新修復報告

**Files:**
- Modify: `courses/office-ai/_repair/2026-07-15/REPAIR-REPORT.md`
- Generated: `search-index.json`
- Generated: `sitemap.xml`

**Interfaces:**
- Consumes: Task 2 的 live HTML 與 outline。
- Produces: lint／導航／索引證據與可追溯報告。

- [ ] **Step 1: 跑整課 lint**

Run:
```bash
python3 docs/lint-page.py courses/office-ai/ --summary
```
Expected: 20 頁，0 BLOCKER、0 ERROR、0 WARN。

- [ ] **Step 2: 驗證內部連結**

解析排除 `_backup` 的 20 頁相對 `href`／`src`；Expected: broken 0。

- [ ] **Step 3: 重建衍生檔**

Run:
```bash
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
```
Expected: 兩個指令 exit 0，office-ai 搜尋索引仍有 20 筆。

- [ ] **Step 4: 更新修復報告**

在 `REPAIR-REPORT.md` 新增「平台中立增量修正」：列出 1.2 新定位、全課同步規則、保留 provenance 原因、驗證結果與增量 restore script。

- [ ] **Step 5: 最終差異檢查**

Run:
```bash
git diff --check -- courses/office-ai _outlines/office-ai.md
git diff --name-only -- courses/office-ai _outlines/office-ai.md search-index.json sitemap.xml
```
Expected: 無 whitespace error；變更只含規格所列 scope 與衍生檔。
