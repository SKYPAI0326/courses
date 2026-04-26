# 設計升級 V4 — CCS 語彙傳播到全課程

> 源：`courses/ccs-foundations/` 今日（2026-04-19）建立的編輯式視覺語彙
> 目標：將 CCS 的字型/排版/元件語彙套到其他 10 個課程（~400 頁）
> 方針：保留各課程的 accent 色彩識別（brown/green/blue），只換「語彙層」

---

## 1. V4 做什麼、不做什麼

### 做
- 字型切換：display → `Shippori Mincho`；body 續用 `Noto Sans TC`
- 7 個共用元件排版語彙對齊 CCS
- 間距節奏微調（section 72→64）
- 全頁通用色彩 token 對齊（CCS 已在今天 V3 commit 中完成）

### 不做
- 不改各課程 `--c-a1` 主色（brown/blue/green 等保留為課程識別）
- 不改 CCS 的 per-chapter 色輪機制（那是 CCS 專屬）
- 不動各課程 bespoke 元件（`.tool-card`、`.drill-card`、`.faq-list`、`.output-box`、`.ch-card` 等保留）
- 不改 HTML 結構（只動 `<style>` block）

---

## 2. 轉換規則表（源→目標）

### 2.1 字型載入
```html
<!-- 舊 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<!-- 新 -->
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
```

### 2.2 字族字串
全檔 `replace_all`：
```
'Noto Serif TC',serif  →  'Shippori Mincho',serif
```

### 2.3 topbar-tag（課程章節 pill）
用課程主色（`--c-a1`）替代 `--c-a2`，RGB 與該主色一致：
```css
/* 舊（office-ai 範例）*/
.topbar-tag{color:var(--c-a2);border:1px solid rgba(107,127,163,.3);background:rgba(107,127,163,.07);...}
/* 新 */
.topbar-tag{color:var(--c-a1);border:1px solid rgba({a1-rgb},.3);background:rgba({a1-rgb},.07);...}
```

### 2.4 progress-strip
```css
/* 舊 */ .progress-strip{height:3px;background:var(--c-surface);...}
/* 新 */ .progress-strip{height:2px;background:transparent;...}
```

### 2.5 hero-part / hero-num
```css
/* 新 */
.hero-part{font-size:.73rem;color:var(--c-muted);letter-spacing:.08em;font-weight:500;font-variant-numeric:tabular-nums}
.hero-num{font-family:'Shippori Mincho',serif;font-size:.78rem;color:var(--c-a1);letter-spacing:.1em;font-weight:500;font-variant-numeric:tabular-nums}
```
HTML 建議：`.hero-num` 顯示格式改 `(01·01)` 括號式編號（選配，可後批次做）。

### 2.6 lesson-title
加 `letter-spacing:-.005em`：
```css
.lesson-title{font-family:'Shippori Mincho',serif;font-size:2rem;font-weight:700;line-height:1.3;color:var(--c-text);margin-bottom:20px;letter-spacing:-.005em}
```

### 2.7 outcomes（學完這章，你會）
從水平雙線改為**左側引用線**：
```css
/* 新 */
.outcomes{display:flex;flex-direction:column;gap:10px;padding:4px 0 4px 24px;border-left:1px solid var(--c-text)}
.outcomes-label{font-size:.73rem;color:var(--c-text);letter-spacing:.15em;font-weight:500;margin-bottom:4px}
.outcome-item{display:flex;align-items:flex-start;gap:10px;font-size:.9rem;color:var(--c-text)}
.outcome-dot{width:5px;height:5px;border-radius:50%;background:var(--c-a1);margin-top:8px;flex-shrink:0}
```

### 2.8 section-eyebrow / section-heading
```css
/* 新 */
.section-eyebrow{font-family:'Shippori Mincho',serif;font-size:.8rem;color:var(--c-faint);letter-spacing:.1em;font-weight:500;margin-bottom:10px;font-variant-numeric:tabular-nums}
.section-heading{font-family:'Shippori Mincho',serif;font-size:1.45rem;font-weight:700;color:var(--c-text);margin-bottom:20px;line-height:1.4;letter-spacing:-.005em}
.section-heading em{font-style:normal;color:var(--c-text)}
```

### 2.9 間距
```css
.lesson-section{margin-bottom:64px}   /* 舊 72 */
.section-rule{border:none;border-top:1px solid var(--c-border);margin:64px 0}  /* 舊 72 */
```

### 2.10 callout
從 border-left only 改為 surface 底 + 深色左線：
```css
.callout{display:flex;gap:16px;padding:18px 22px;border-radius:var(--radius);margin:24px 0;background:var(--c-surface);border-left:2px solid var(--c-text)}
.callout.info,.callout.tip,.callout.key{background:var(--c-surface);border-left:2px solid var(--c-text)}
```

### 2.11 lesson-nav（下一節／上一節）
從「實心強調按鈕」改為 CCS 極簡雙卡片：
```css
.lesson-nav{max-width:var(--content-w);margin:0 auto;padding:0 48px 80px;display:flex;gap:16px}
.nav-btn{display:flex;align-items:center;gap:10px;padding:14px 22px;background:var(--c-card);border:1px solid var(--c-border);border-radius:var(--radius);text-decoration:none;color:var(--c-text);font-size:.85rem;transition:border-color .2s;flex:1}
.nav-btn:hover{border-color:var(--c-a1)}
.nav-prev{background:var(--c-card);color:var(--c-text);border:1px solid var(--c-border)}
.nav-prev:hover{background:var(--c-card);border-color:var(--c-a1)}
.nav-next{background:var(--c-card);color:var(--c-text);border:1px solid var(--c-border);justify-content:flex-end;text-align:right}
.nav-next:hover{background:var(--c-card);border-color:var(--c-a1)}
.nav-label{font-size:.7rem;color:var(--c-muted);margin-bottom:2px}
```

---

## 3. 各課程 accent RGB 對照

| 課程 | --c-a1 hex | RGB |
|---|---|---|
| office-ai | #b5703a | 181,112,58 |
| ai-workshop | （查檔案確認） | — |
| gemini-ai | （查檔案確認） | — |
| 其他 | 各課程獨立 | — |

套 `.topbar-tag` 的 rgba() 時要用對應 RGB。

---

## 4. 施作順序

1. **Pilot**（完成）：office-ai/part1/CH1-1.html
2. **Phase A**：office-ai 全課程（21 頁）
3. **Phase B**：ai-workshop、prompt-basic（43 頁，課程規模小）
4. **Phase C**：office-ai 式系列（gemini-ai、gtm、n8n，113 頁）
5. **Phase D**：gen-ai 系列（140h + 36h，95 頁）
6. **Phase E**：marketing 系列（digital-marketing-70h、ntub-*，141 頁）

每 Phase 完後跑：
```bash
python3 docs/lint-page.py courses/{slug}/
```

全部完成後：
```bash
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
git commit -m "style(v4): propagate CCS editorial language to all courses"
```

---

## 5. 風險與緩解

| 風險 | 緩解 |
|---|---|
| 各頁 inline style 非齊整、regex 失敗 | 改用 Python AST-lite 逐檔檢查，找不到 pattern 就記入 log 人工補 |
| 課程獨特元件干擾（如 tool-card） | 本規則只改「共用元件」白名單，不動 bespoke CSS |
| Nav 按鈕文字不見（舊的 `.nav-label` class 可能用法不同） | 視覺驗證每個 phase 頭尾頁 |
| Shippori Mincho 字型載入慢 | 已經 preconnect + `display=swap` |

---

## 6. 當前狀態（2026-04-19）

- ✅ Pilot: office-ai/part1/CH1-1.html
- ⏳ Phase A–E: 待批次執行
- 📄 Migration script: 待寫（見 `docs/apply-v4-style.py`）
