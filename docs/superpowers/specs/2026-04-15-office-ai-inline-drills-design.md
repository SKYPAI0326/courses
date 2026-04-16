# office-ai 課程 — 章節內嵌隨堂演練設計文件

**日期：** 2026-04-15  
**課程：** 辦公室 AI 工具實務應用（`courses/office-ai/`）  
**範圍：** 12 個 CH 頁，每個 section 嵌入一張三步驟演練卡

---

## 背景與目標

現有課程結構為「3 個章節頁（CH）+ 1 個章末演練（PRAC）」× 4 Part，共 16 頁。
學員純粹閱讀 CH 頁，直到章末才有互動，容易注意力渙散。

**目標：** 每個 CH section 講完原理後立即嵌入一張演練卡，讓學員「聽原理 → 立刻試 → 自行對照」，循序漸進感受差異，避免純聽課過於沈悶。

---

## 演練卡設計

### 結構（三步驟固定順序）

```
┌─────────────────────────────────────┐
│  DRILL · 隨堂演練  [section 編號]    │
├─────────────────────────────────────┤
│  STEP 1 · 想一想                     │
│  一句引導語，啟動學員主動思考         │
├─────────────────────────────────────┤
│  STEP 2 · 試試看                     │
│  場景說明                            │
│                                     │
│  [Prompt 比對型] 版本 A（有瑕疵）    │
│  ┌──────────────────────────────┐   │
│  │ prompt 文字                  │   │
│  └──────────────────────────────┘   │
│  [複製 A]  [開啟 Gemini]            │
│                                     │
│  版本 B（改良版）                    │
│  ┌──────────────────────────────┐   │
│  │ prompt 文字                  │   │
│  └──────────────────────────────┘   │
│  [複製 B]                           │
│  提示：兩版都貼入 Gemini，比較差異   │
│                                     │
│  [情境操作型] 單一任務指令           │
│  [複製]  [開啟 Gemini]              │
├─────────────────────────────────────┤
│  STEP 3 · 對照一下                   │
│  [▸ 查看解析]  ← 點擊展開           │
│  差異說明 + 關鍵學習點               │
└─────────────────────────────────────┘
```

### 兩種卡型

| 卡型 | 使用時機 | Step 2 內容 |
|------|---------|-------------|
| **Prompt 比對型** | 提示詞原則、文書應用、會議準備等 | A 版（有瑕疵）+ B 版（改良）各一個 prompt box，雙複製按鈕 + 開啟 Gemini |
| **情境操作型** | 工具介紹、場景判斷、概念驗證等 | 單一任務指令，一個 prompt box，單複製 + 開啟 Gemini 或純自評問題 |

---

## 視覺設計

符合現有 `courses/office-ai/` 設計系統，以橘色左條與現有 callout（霧藍）做視覺區隔。

### CSS 規格

```css
/* 演練卡主體 */
.drill-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-a1);  /* 陶土橘，區別於 callout 的霧藍 */
  border-radius: var(--radius);
  margin: 32px 0;
  overflow: hidden;
}

/* 標題列 */
.drill-header {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 20px;
  border-bottom: 1px solid var(--c-border);
  background: rgba(181,112,58,.05);  /* var(--c-a1) 淡底 */
}
.drill-badge {
  font-size: .68rem; font-weight: 700; letter-spacing: 1.5px;
  color: var(--c-a1);
  background: rgba(181,112,58,.1);
  border: 1px solid rgba(181,112,58,.25);
  padding: 2px 10px; border-radius: 99px;
}
.drill-section-ref {
  font-size: .72rem; color: var(--c-muted);
}

/* 步驟區塊 */
.drill-step {
  padding: 18px 20px;
  border-top: 1px dashed var(--c-border);
}
.drill-step:first-of-type { border-top: none; }
.drill-step-label {
  font-size: .68rem; font-weight: 700; letter-spacing: 1px;
  color: var(--c-a2); margin-bottom: 8px;
}
.drill-q {
  font-size: .88rem; color: var(--c-text); line-height: 1.75;
}

/* Prompt box */
.drill-prompt-wrap { margin: 12px 0 8px; }
.drill-prompt-version {
  font-size: .68rem; color: var(--c-muted); margin-bottom: 5px; font-weight: 500;
}
.drill-prompt-box {
  background: var(--c-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  font-family: 'Courier New', monospace;
  font-size: .82rem; color: var(--c-text); line-height: 1.7;
  white-space: pre-wrap;
}
.drill-action-row {
  display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap;
}
.drill-hint {
  font-size: .78rem; color: var(--c-muted);
  margin-top: 10px; line-height: 1.6;
}

/* 按鈕 */
.btn-drill-copy {
  font-size: .78rem; color: var(--c-a2);
  background: rgba(107,127,163,.08);
  border: 1px solid rgba(107,127,163,.25);
  padding: 5px 14px; border-radius: var(--radius-sm); cursor: pointer;
}
.btn-drill-copy:hover { background: rgba(107,127,163,.18); }
.btn-drill-gemini {
  font-size: .78rem; color: var(--c-a1);
  background: rgba(181,112,58,.08);
  border: 1px solid rgba(181,112,58,.25);
  padding: 5px 14px; border-radius: var(--radius-sm); cursor: pointer;
  text-decoration: none; display: inline-flex; align-items: center; gap: 4px;
}
.btn-drill-gemini:hover { background: rgba(181,112,58,.18); }

/* Step 3 展開 */
.drill-reveal-btn {
  font-size: .82rem; font-weight: 500; color: var(--c-a2);
  background: none; border: 1px solid rgba(107,127,163,.3);
  padding: 7px 16px; border-radius: var(--radius-sm); cursor: pointer;
  display: flex; align-items: center; gap: 6px;
}
.drill-reveal-btn:hover { background: rgba(107,127,163,.08); }
.drill-reveal-content {
  display: none;
  margin-top: 14px; padding: 14px 16px;
  background: var(--c-card); border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  font-size: .85rem; color: var(--c-text); line-height: 1.85;
}
.drill-reveal-content.open { display: block; }
```

### JS（每頁 inline，兩個 function）

```javascript
function drillCopy(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.textContent;
    btn.textContent = '已複製';
    setTimeout(() => btn.textContent = orig, 1500);
  });
}
function drillReveal(id, btn) {
  const el = document.getElementById(id);
  const open = el.classList.toggle('open');
  btn.innerHTML = open ? '▾ 收起' : '▸ 查看解析';
}
```

---

## 內容框架

各 CH 頁的演練卡類型對照：

| CH 頁 | 主題 | 卡型建議 |
|-------|------|---------|
| CH1-1 | AI 工具全景圖 | 情境操作型（場景 → 判斷選哪個工具） |
| CH1-2 | Prompt 三個關鍵原則 | Prompt 比對型（好壞 prompt 對照） |
| CH1-3 | 現場實作 | Prompt 比對型 + 情境操作型 |
| CH2-1 | 文書三件事 | Prompt 比對型 |
| CH2-2 | 郵件自動化 | Prompt 比對型 |
| CH2-3 | 簡報大綱秒出爐 | Prompt 比對型 |
| CH3-1 | NotebookLM 實戰 | 情境操作型（操作步驟驗證） |
| CH3-2 | 會議前準備術 | Prompt 比對型 |
| CH3-3 | 提案與匯報準備 | Prompt 比對型 |
| CH4-1 | 找出高價值場景 | 情境操作型（場景自評） |
| CH4-2 | 建立個人 Prompt 庫 | Prompt 比對型 |
| CH4-3 | 三種職業全攻略 | Prompt 比對型 + 情境操作型 |

---

## 實作範圍

**在範圍內：**
- 12 個 CH 頁（`part1–4/CH*.html`），每頁加入 2–3 張演練卡
- 每頁 `<style>` 區塊增加演練卡 CSS
- 每頁末尾增加 `drillCopy` / `drillReveal` inline JS

**不在範圍：**
- 4 個 PRAC 頁（現有演練頁維持不變）
- `index.html`（導覽結構不變）
- 任何後端或 LLM API 整合（全為靜態 HTML）

---

## 開發順序

1. **CH1-2**（Prompt 三原則）— 最典型的 Prompt 比對型，作為樣版頁確認文案與樣式
2. **CH1-1、CH1-3** — 完成 Part 1
3. **Part 2（CH2-1~3）**
4. **Part 3（CH3-1~3）**
5. **Part 4（CH4-1~3）**

每完成一個 Part 請使用者確認視覺與文案再繼續。
