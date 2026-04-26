# Gen AI 基礎課程修正計畫

**課程路徑：** `courses/gemini-ai/` 及 `courses/courses/office-ai/`
**觸發指令：** 啟動Gen AI基礎課程修正計畫
**建立日期：** 2026-04-11
**狀態：** 待執行

---

## 背景說明

`courses/office-ai/`（辦公室 AI 工具實務應用）課程架構已完成，共 6 章，但所有 `ch1/`～`ch6/` 目錄內只有 `.gitkeep`，內容頁面完全空白。本計畫的目標是依優先順序建立課程內容，並同步修正架構問題。

---

## 執行順序

### Phase 1：建立基礎內容頁（最高優先）

將 CH1 與 CH2 合併為單一章節「認識 AI 並開口問 AI」（約 60 分），內容涵蓋：
- 三大免費工具簡介（Gemini / NotebookLM / Google Workspace AI）
- Prompt 三個關鍵原則
- 帶走產出：AI 工具速查表 + Prompt 範本 20 句（合一份）

接著依序建立：
- CH3：文書處理（週報 / 公告 / 摘要）
- CH4：簡報大綱（Google Slides + Gemini）
- CH5：會議記錄（NotebookLM 逐字稿整理）
- CH6：打造個人 AI 工作流程（含 3 種職業情境範本）

**每個章節頁面結構：**
```
- 頂部：章節編號 / 標題 / 預計時間 / 帶走產出說明
- 主體 Section 1：概念說明（300 字以內）
- 主體 Section 2：步驟操作（3～5 步，附截圖位置說明）
- 主體 Section 3：帶走產出（可複製的 Prompt 或模板）
- 底部：前後章節導航
```

---

### Phase 2：補充 NotebookLM（中優先）

CH5 目前規劃已涵蓋 NotebookLM，但需提前在 CH1 或課程 index 補充一段工具介紹，說明 NotebookLM 與 Gemini 的使用場景差異。

---

### Phase 3：加入 PRAC 演練頁（中優先）

至少為以下兩章新增互動演練頁：
- `ch2/PRAC2.html`：Prompt 黃金公式填空台（可參考 gemini-ai/part1/PRAC1-1.html 的結構）
- `ch3/PRAC3.html`：文書模板套用器（三種格式切換 + 一鍵複製）

---

### Phase 4：架構調整（低優先，可在 Phase 1 執行時同步）

- 將 index.html 的 6 個章節依邏輯分成 3 個 Part：
  - **Part 1 基礎**：CH1+2（合併後的章節）
  - **Part 2 任務**：CH3 / CH4 / CH5
  - **Part 3 整合**：CH6
- 在 index.html 英雄區下方加入「如何使用本課程」2～3 行說明
- 加入學習進度追蹤（參考 gemini-ai/index.html 的 progress bar 邏輯）

---

## 技術規格提醒

- 強調色：`--c-a2`（#c9963a 芥末黃），與其他課程區分
- 章節頁面命名：`ch1/CH1.html`，`ch2/CH2.html`……（扁平結構，非 CH1-1 格式）
- 演練頁命名：`ch2/PRAC2.html`（與 gemini-ai 的 PRAC1-1 格式不同，注意區分）
- 修改前先讀取 `courses/office-ai/index.html` 確認現有結構與色碼
- 每完成一個章節頁面後，回到 index.html 將對應卡片的 `locked` class 移除，改為 `status-available`

---

## 驗收標準

- [ ] CH1（合併版）可正常開啟，帶走產出可複製
- [ ] CH3 / CH4 / CH5 / CH6 各有完整內容頁
- [ ] PRAC2 和 PRAC3 工具可運作
- [ ] index.html 所有章節卡片解鎖為「可學習」狀態
- [ ] Push 至 GitHub 並確認連結有效
