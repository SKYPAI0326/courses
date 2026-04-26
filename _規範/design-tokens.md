# Design Tokens — 課程網頁設計系統人類規範 SSOT

> 本檔為所有課程網頁的設計規範**人類閱讀真相源**。`build-course-page`、`course-reviewer`、`course-lesson-writer` 均引用本檔。
> **機器強制版** SSOT 在 `docs/lint-page.py`（規則的程式實現）。修改規則時**人類版 + 機器版必須同步**。
> 設計規則只改本檔（不要在 CLAUDE.md / skill 文件 / 其他規範檔重複），其他檔案僅保留引用指向。

---

## 0. 專案說明

- **用途**：職業技能線上課程系統
- **風格**：無印良品式 — 簡潔、自然、留白充足
- **受眾**：職場成人學習者
- **變更紀錄**：原 `_規範/設計規範.md`（最後更新 2026-03）已合併入本檔並刪除（2026-04-26）

---

## 1. CSS 變數

### 色彩系統

```css
:root {
  /* 底色 */
  --c-bg:      #f5f3ee;   /* 米白背景 */
  --c-surface: #edeae3;   /* 淺灰米（sidebar、次要區域） */
  --c-card:    #ffffff;   /* 純白（卡片） */
  --c-border:  #d8d4cb;   /* 暖灰（邊線） */

  /* 文字 */
  --c-text:    #2c2b28;   /* 深褐黑（主要文字） */
  --c-muted:   #8c8880;   /* 灰褐（次要文字） */

  /* 強調色色票（不直接引用，僅供各課挑選後改寫為 --c-main） */
  --c-a1:      #b5703a;   /* 陶土橘 */
  --c-a2:      #c9963a;   /* 芥末黃 */
  --c-a3:      #5a7a5a;   /* 鼠尾草綠 */
  --c-a4:      #6b7fa3;   /* 霧藍（預設 fallback） */
  --c-a5:      #7a9ea3;   /* 灰藍綠 */
  --c-a6:      #8a6a4a;   /* 奶茶棕 */

  /* 每門課程覆蓋此變數為該課主題色，組件 CSS 一律用 --c-main */
  --c-main:    var(--c-a4);
}
```

### 色彩使用規則（嚴格派 — 2026-04-26 確立）

- **組件 CSS 一律用 `var(--c-main)`，禁止直接引用 `var(--c-a1)` ~ `var(--c-a6)`**
- 各課的 `:root` 應改寫 `--c-main` 為該課主題色（例如 `--c-main: #b5703a;` for 陶土橘課程），而不是 `--c-main: var(--c-a1);` 的轉接
- `--c-a1~a6` 在 design-tokens 中**僅作為色票參考**，不參與實作
- 背景色只用 3 種：`--c-card`（白）、`--c-bg`（米白）、`--c-surface`（淺灰米）
- `--c-main` 只出現在 4 處（v3 修正）：左邊線 `border-left`、小標籤/tag、progress bar、section-eyebrow 序號（progress 改用 `var(--c-text); opacity:.75`）
- 禁止漸層 (gradient)、深色背景、高飽和色彩、漸層文字效果

> ⚠️ **既有狀態（2026-04-26）：** 14 個 `courses/*/index.html` 共 218 處 `var(--c-a*)` 直接引用尚未遷移。lint 暫不加 BLOCKER 阻擋，避免一次擋掉所有舊頁。遷移計畫見 §「遷移狀態」。

### 尺寸與間距

```css
:root {
  --content-w: 780px;     /* 內容最大寬度 */
  --radius:    6px;       /* 一般圓角 */
  --radius-sm: 4px;       /* 小元素圓角 */
}
```

| 元素 | 數值 |
|------|------|
| 內容左右 padding | 48px |
| Top bar 高度 | 56px (sticky) |
| Bottom bar 高度 | 52px |
| Sidebar 寬度 | 260px |
| 邊線樣式 | 1px solid（無 shadow、無 gradient） |
| 圓角上限 | 8px（禁止超過） |

---

## 2. 字型系統（8 階，嚴禁其他 rem 值）

### 字族

| 用途 | 字型 | 字重 |
|------|------|------|
| 標題 | Shippori Mincho（明朝體） | 700 |
| 內文 | Noto Sans TC | 400 / 500 |
| 程式碼 | Courier New | — |

Google Fonts：`https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap`

### 字型尺寸階（V4 標準：14 階 + 1 舊相容）

V4 CCS 語彙分為 4 組尺度，每組內有細微階差以支援編輯式節奏：

| 組 | rem | 主要用途 |
|----|-----|---------|
| **標題組** | 2 | `.lesson-title` / `.page-title` 頁面大標 |
|  | 1.45 | `.section-heading` 區段標題 |
|  | 1.2 | `.big-quote` 金句（舊課相容，V4 template 未用） |
|  | 1.1 | `.tool-name` / `.card-name` / `.part-title` 卡片標 |
|  | 1.05 | `.logo` / `.hero-title` |
| **內文組** | .95 | `.lesson-subtitle` / 主要說明 |
|  | .92 | `.body-text` / `.lesson-tagline` 內文 |
|  | .9 | `.intro-band` / 段落文 |
|  | .88 | `.callout-body` / 次要內文 |
| **說明組** | .85 | `.tool-summary` / `.nav-btn` / `.skip-link` |
|  | .82 | `.back-link` / `.hero-eyebrow`（Shippori Mincho 用） |
|  | .8 | `.topbar-sub` / 小說明 |
| **註解組** | .75 | `.prac-badge` / `.stat-label` |
|  | .72 | `.topbar-tag` / `.tag-inline` |
|  | .7 | `.section-eyebrow` / `.outcomes-label` 小標籤 |

**禁用（舊頁殘留，不再採用）**：`.78` / `.76` / `.73` / `.68` / `1rem` — V4 化時應改用最接近的合規值。其他非此 15 階的 rem 值（`.82.5` / `.86` 等）亦禁止。

**lint 真相源**：`docs/lint-page.py` 的 `check_font_size_tier` 函數白名單 = 此表 15 值。改一處 = 改兩處（此表 + lint）。

---

## 3. 組件白名單

> 只有以下組件允許使用。產出含不在此表的自製組件 = reviewer BLOCKER。

### 結構骨幹

| 組件 | Class | 說明 |
|------|-------|------|
| Topbar | `.topbar` `.logo` `.topbar-divider` `.topbar-sub` `.topbar-tag` | 固定頂部列 |
| Progress | `.progress-strip` `.progress-fill` | 進度條 |
| Hero | `.page-hero` `.back-link` `.hero-eyebrow` `.page-title` `.page-subtitle` | 頁面標題區 |
| Section | `.lesson-section` | **骨幹元件**，每頁 ≥ 5 個 |
| Section Eyebrow | `.section-eyebrow` | 格式：`SECTION NN · {中文副標}` |
| Section Heading | `.section-heading` | 1.45rem，`<em>` 語義高亮 |
| Section Rule | `.section-rule` `<hr>` | 區段間分隔線 |
| Body Text | `.body-text` | 0.92rem 內文 |
| Navigation | `.nav-footer` `.nav-btn` `.nav-btn.primary` | 底部導航 |
| Footer | `.footer` `.footer-logo` `.footer-div` `.footer-note` `.footer-meta` | 頁尾含 metadata |

### 內容組件（8 種）

| # | 組件 | Classes | 使用限制 |
|---|------|---------|---------|
| 1 | Tool Grid | `.tool-grid` `.tool-card` `.tool-name` `.tool-tag` `.tool-summary` `.tool-list` `.tool-list-item` `.tool-check` | 欄數寫死（`1fr 1fr` 或 `1fr 1fr 1fr`） |
| 2 | Scenario Grid | `.scenario-grid` `.scenario-row` `.scenario-task` `.scenario-pick` | `grid-template-columns: 160px 1fr` |
| 3 | Callout | `.callout` `.callout.info` `.callout.tip` `.callout.key` `.callout-icon` `.callout-body` | 每頁最多 3-4 個 |
| 4 | Big Quote | `.big-quote` | 每頁最多 1 個 |
| 5 | Steps Inline | `.steps-wrap` `.step-block` `.step-circle` `.step-content` `.step-heading` `.step-body` | 只在 SECTION 03 操作/實作使用 |
| 6 | Quiz | `.quiz-item` `.quiz-q` `.quiz-opts` `.quiz-opt` `.quiz-opt.correct` `.quiz-ans` | `<details>` 展開答案 |
| 7 | Outcomes | `.outcomes` `.outcomes-label` `.outcome-item` `.outcome-dot` | Hero 底部，3-6 條 |
| 8 | Code Block | `.code-block` | 深色主題：bg `#2c2b28`、text `#e8e4dc` |

### 輔助組件

| 組件 | Classes | 說明 |
|------|---------|------|
| Context Box | `.context-box` `.context-inner` `.context-label` `.context-text` | SECTION 01 破題 |
| Concept Grid | `.concept-grid` `.concept-card` `.concept-num` `.concept-title` `.concept-desc` | 概念卡（3 張） |
| Compare Grid | `.compare-grid` `.compare-card` `.compare-label` `.compare-item` | 對照表 |
| Verify Box | `.verify-box` `.verify-label` `.verify-text` | 驗證確認 |
| Troubleshoot | `.troubleshoot` `.ts-label` `.ts-item` `.ts-q` `.ts-a` | 故障排除 |
| Reflection | `.reflection-block` `.reflection-label` `.reflection-prompt` | 反思題 |
| Inline Code | `.inline-code` | 行內程式碼 |
| Step Tip | `.step-tip` | 步驟提示 |

### 程式碼語法高亮（`.code-block` 內）

| Class | 顏色 | 用途 |
|-------|------|------|
| `.cm` | `#6b9b8a` 灰綠 | 註解 |
| `.ky` | `#9bb4d4` 藍 | 關鍵字 |
| `.st` | `#b8d4a0` 淡綠 | 字串 |
| `.vr` | `#d4c08a` 淡黃 | 變數 |

---

## 4. 禁用組件（Pilot A 舊組件，已廢除）

以下組件**不得使用**，reviewer 偵測到 = BLOCKER：

- `concepts-strip`
- `case-block`
- `assets-box`
- `quiz-block`
- `hands-on-box`
- `reflection-block`（注意：`.reflection-block` 保留於輔助組件，但不可作為獨立 section 的主要組件）

---

## 5. Grid 規則

### 禁止

```css
/* FORBIDDEN — 會產生 3+1 孤兒排列 */
grid-template-columns: repeat(auto-fit, minmax(...));
```

### 允許的固定欄模式

| 場景 | grid-template-columns |
|------|----------------------|
| 2 欄卡片 | `1fr 1fr` |
| 3 欄卡片 | `1fr 1fr 1fr` |
| 任務-方案對照 | `160px 1fr` |
| 情境表（scenario） | `180px 1fr` |

---

## 6. 響應式斷點

| 斷點 | 條件 | 調整 |
|------|------|------|
| Desktop | 預設 | padding 48px，grid 維持多欄 |
| Mobile | `@media (max-width: 600px)` | padding ≥ 24px，grid 變單欄 `1fr` |

---

## 7. Section 對應表（教案 → HTML）

### skill-operation / programming 類型

| Section | Eyebrow | 教案來源 | 主要組件 |
|---------|---------|---------|---------|
| 01 | SECTION 01 · {破題} | 破題段 | context-box |
| 02 | SECTION 02 · KEY CONCEPTS | 概念段 | tool-grid (2 欄) |
| 03 | SECTION 03 · STEP BY STEP | 操作示範/實作 | steps-inline (5-6 步) |
| 04 | SECTION 04 · HANDS-ON | 動手段 | scenario-grid + callout |
| 05 | SECTION 05 · VERIFY | 檢核/驗證 | outcomes-style list |
| 06 | SECTION 06 · TRIAL PACK | 試跑包需求 | tool-grid cards |
| 07 | SECTION 07 · PITFALLS | 常見錯誤 3 條 | scenario-grid |
| 08 | SECTION 08 · QUIZ | 檢核題 2 條 | interactive quiz |

### concept 類型

| Section | 差異 |
|---------|------|
| 03 | → CASE ANALYSIS（scenario-grid） |
| 04 | → REFLECTION（reflection-block） |

---

## 8. Metadata 規格

### Footer metadata（必要）

```html
<span class="footer-meta"
      data-platform-version="{platform_version}"
      data-built-at="{YYYY-MM-DD}">
  本頁以 {platform_version} 製作，{YYYY-MM}
</span>
```

- `platform_version`：取自教案 frontmatter → 大綱 frontmatter（預設「未指定」）
- `built-at`：產出當天日期 `YYYY-MM-DD`
- Footer 顯示只到年月

### SEO Meta（必要）

```html
<meta name="description" content="{learning_objective}">
<meta property="og:title" content="{page_title} | {course_name}">
<meta property="og:description" content="{learning_objective}">
```

---

## 9. 檔案命名規則

| 類型 | 格式 | 範例 |
|------|------|------|
| 課程資料夾 | 小寫 kebab-case | `gemini-ai/` |
| 課程總覽 | `index.html` | — |
| 章節頁 | `CH{N}-{M}.html` | `CH1-1.html` |
| 練習頁 | `PRAC{N}-{M}.html` | `PRAC1-1.html` |
| 模組總覽 | `module{N}.html` | `module1.html` |
| 試飛頁 | `_pilots/{pilot_id}/CH1-1.html` | — |

---

## 10. 編碼規則

- 縮排：2 spaces
- HTML5 + CSS3 + vanilla JavaScript
- 編碼：UTF-8 `<meta charset="UTF-8">`
- 圖片路徑：相對路徑
- 單檔包含 HTML/CSS/JS（不拆檔）
- CSS 寫在 `<style>` 內，壓縮為單行格式
- 禁止 JS 依賴（inline handler 或純 CSS）
- 完成前驗證所有相對連結正確

---

## v3 · 距離層變數（2026-04-19 追加）

> 基於 `_pilots/ccs-foundations-marquee/` 驗證結果追加。既有色彩表 §1 不動。

```css
:root {
  --c-faint:       #bcb8ae;   /* 距離層灰，弱於 --c-muted */
  --c-border-soft: #e8e4da;   /* 次級邊線（表列 hairline 專用） */
}
```

使用規則：
- `--c-faint` **只用於**：`(NN)` 編號、標籤前綴、次要計數（如 `05 單元`）
- `--c-border-soft` **只用於**：表列行間 hairline、grid 中線分隔；**不可**取代 `--c-border` 作為卡片外框

---

## v3 · serif 小標字階例外（2026-04-19 追加）

既有 8 階（§2）**不變**。新增兩階例外，**只限 Shippori Mincho serif 小標**使用，不開放 body / Noto Sans：

| rem | 用途 | 配合規則 |
|-----|------|----------|
| `.78` | Shippori Mincho 編號 `(NN)`、hero-num、字距壓縮 serif 小標 | 必配 `'Shippori Mincho',serif` |
| `.72` | hairline 表列 `lesson-tag` / `exam-range` tabular 數據 | 必配 `letter-spacing ≥ 0.06em` |

理由：serif 小標在視覺上需比 sans 小 0.07rem 才不會喧賓奪主。

---

## v3 · 色彩克制條款（2026-04-19 追加）

既有「只用 `--c-main` 一色」規則保留。v3 新增：

- `--c-main` 在同一頁最多出現 **4 處**（原 3 處；新增 progress 計算在內）
- `--c-main` **禁止**用於：body 內 `<em>` 標題變色、長段正文強調、hover 色變
- `--c-main` **建議**用於：progress-fill、section-eyebrow 序號色、outcomes/scenario 左邊線、選中/完成狀態
- **progress-fill 改用** `var(--c-text); opacity:.75`（黑色半透明），取代 `var(--c-main)` — 原因：progress 是中性資訊不應吃 main 色配額

---

## v3 · 組件白名單補充（2026-04-19 追加）

既有 §3「8 種內容組件 + 輔助組件」**保留不動**。以下為 v3 並行可選項（不強制取代）：

| # | 組件 | Classes | 與既有關係 |
|---|------|---------|-----------|
| A | Concept List | `.concept-list` `.concept-row` `.concept-num` `.concept-body` `.concept-title` `.concept-desc` | v3 替代 `.concept-grid`，舊版保留 |
| B | Exam / Overview List | `.exam-list` `.exam-row` `.exam-paren` `.exam-name` `.exam-range` | 新增 |
| C | Intro Band | `.intro-band` `.intro-label` `.intro-text` | v3 替代 `.context-box`，舊版保留 |
| D | Editorial Big Quote | `.big-quote` 單邊 hairline 版 | 樣式變體（class 不變） |
| E | Part Head | `.part-head` `.part-paren` `.part-rule` `.part-count` `.part-title` | 新增（index 章節分組） |
| F | Hero Stats | `.hero-stats` `.stat` `.stat-num` `.stat-lbl` | 新增（總覽頁統計） |
| G | Outlined Pill Tag | `.lesson-tag` outlined 變體 | 樣式變體（class 不變） |

---

## v3 · Hover 反饋規範（2026-04-19 追加）

**單一元件 hover 同時變化不得超過 2 個屬性**。允許：`background` / `border-color` / `color` / `padding` / `opacity`。

禁止：
- `translateY()` 上抬感（紙卡感不符編輯式語彙）
- hover 時 accent 色同時套 3+ 個子元素（tag + arrow + border + title 一起變色）
- `box-shadow` 增加（本來就被既有 BLOCKER 擋）

---

## v3 · 編輯式編號規範（2026-04-19 追加）

- Part 層級：`(NN)` · 01~05 範圍
- Section 層級：`(NN)` · Shippori Mincho + `--c-faint` + `.82rem` + `letter-spacing:.1em`
- Lesson 層級：`CH N.M` 保留（不動），可併用 `(NN)` 於子層
- **禁用**：`SECTION 01` 大寫英文 + letter-spacing 間距樣式

---

## 遷移狀態（2026-04-26）

| 項目 | 狀態 | 規模 |
|------|------|------|
| 嚴格派 `--c-main` 規範確立 | ✅ 完成（本檔） | — |
| `_規範/course-index-editorial-strict.html` SSOT | ✅ 完成 2026-04-26 | 從 ccs-foundations 抽 |
| `_規範/course-index-module-landing.html` SSOT | ✅ 完成 2026-04-26 | 從 n8n 抽 |
| `_規範/course-index-lesson-section.html` SSOT | ✅ 完成 2026-04-26 | 從 prompt-basic 抽 |
| 14 個 `index.html` 移除 `var(--c-a*)` | ✅ 完成 2026-04-26 | 218 處替換為 var(--c-main) + 27 處 .band-* 多色設計修回 hex 直寫（保留 5 色對比視覺） |
| ⚠️ Round 3b 視覺驗證教訓 | ✅ 修復 2026-04-26 | batch script 把 6 課（gemini-ai/gen-ai-140h/gen-ai-36h/gtm/prompt-basic/simple-ai）的多色 .band-* 全改成單色 var(--c-main)，**lint 跟 Codex review 都沒抓到**，視覺驗證才發現。教訓：批次替換 var(--c-a*) 前須先掃描多色 design pattern |
| 修 W-v3-2 規則衝突（`--c-main` ≤ 4 vs 嚴格派必然 > 4）| ✅ 完成 2026-04-26 Round 3c | 拆 strict/relaxed：lesson ≤ 4、index ≤ 30 |
| WARN 1249 條分桶（migration-debt / metadata / structural / a11y / motion）| ✅ 完成 2026-04-26 Round 3c | `python3 docs/lint-page.py --all --summary --by-bucket` |
| 各課單元頁（CH/PRAC/module）移除 `var(--c-a*)` | ⏳ 待掃描 | 未統計 |
| `lint-page.py` 加 `--c-a*` 直接引用 BLOCKER | ⏳ 待加（待遷移完成才開） | — |
| `lint-page.py` 加 `--c-accent` 自定 token 警告 | ⏳ 待加（ccs-foundations 已踩到此坑）| — |
| `_pilots/` 加入 lint skip | ✅ 完成 2026-04-26 | — |
| `_規範/設計規範.md` 合併刪除 | ✅ 完成 2026-04-26 | — |
| `課程資料夾命名/結構` SSOT（取代 COURSES.md 過時描述） | ⏳ 待 Phase C 機器可讀 manifest | — |

**3 族家族劃分（2026-04-26 Round 2 verify 確立）：**

| 族別 | 課程（共幾門）| SSOT 位置 |
|------|-------------|----------|
| Editorial-strict（嚴格派 v4 + 0 處 --c-a*） | ccs-foundations / gen-image（2）| `_規範/course-index-editorial-strict.html` ✅ |
| Module-landing（landing + module-grid + 含 hero CTA） | n8n / digital-marketing-70h / ntub-gtm-adtech / ntub-seo-ga4（4）| `_規範/course-index-module-landing.html` ✅ |
| Lesson-section（v4 扁平 part + lesson-list + 多色 band + PRAC 區塊）| ai-workshop / gen-ai-36h / office-ai / prompt-basic / simple-ai / gemini-ai / gen-ai-140h / gtm（8）| `_規範/course-index-lesson-section.html` ✅ |

**已是嚴格派的範本：** `courses/ccs-foundations/`、`courses/gen-image/`（0 處 `var(--c-a*)`）

**遷移成本最高：** `courses/gen-ai-140h/`（43 處）、`courses/gemini-ai/` + `gen-ai-36h/`（28 處）、`courses/office-ai/`（25 處）

---

## v4 · 互動工作坊組件（2026-04-26 追加）

> 來源：`courses/gen-image/_refactor/interactive-workshop-playbook.md`（重構諮詢報告）。
> 目的：把 CH 單元頁從「講義型」轉成「互動工作坊型」——一個觀念一次演練、5–8 分鐘一個小產出。
> 既有 §3 內容組件保留不動。本節為**並行可選**新組件，不強制取代。

### 10 組新組件（用於 CH 單元 micro-cycle 化 / PRAC 任務卡升級 / Round 4-5 補件）

| # | 組件 | Classes | 用途 | 數量上限 |
|---|------|---------|------|---------|
| H | Today Deliverables | `.today-deliverables` `.today-deliverables-label` `.today-deliverables-list` `.today-deliverables-note` | hero 內「今天會交什麼」清單，3 條以內 | 每頁 1 個 |
| I | Micro Cycle | `.micro-cycle` `.cycle-eyebrow` `.cycle-question` `.cycle-bridge` `.closer` | 5–8 分鐘的「觀念→任務→檢核」循環容器 | 每頁 3–5 個 |
| J | Wrong Example | `.wrong-example` `.wrong-label` `.wrong-note` | 錯誤例子展示（cycle 內第 2 步） | 每 cycle 0–1 個 |
| K | Task Card | `.task-card` `.task-card-large` `.task-card-master` `.task-card-header` `.task-card-name` `.task-card-time` `.task-card-body` `.task-card-section` `.task-card-label` `.task-card-list` `.task-card-stuck` | 任務卡（含限時/要做什麼/完成物/通過標準/卡住怎麼辦） | 每 cycle 1 個 + PRAC 大任務不限 |
| L | Learner Output | `.learner-output` `.learner-output-label` `.learner-output-blank` `.learner-output-table` | 學員產出區（提示佔位 + 留白 contenteditable） | 每 cycle 1 個 |
| M | Self Check | `.self-check` `.self-check-label` `.self-check-rule` | 段內檢核（cycle 內第 6 步），與頁尾 `.quiz-item` 並行 | 每 cycle 1 條 |
| N | Concept Pair | `.concept-pair` `.concept-pair-card` `.concept-pair-label` | 概念對照雙卡（左右並列、固定 `1fr 1fr`） | 每頁 0–2 個 |
| O | Instructor Note | `.instructor-note`（搭 `<details>`）| 講師備註折疊區、預設 closed | 每頁 1–3 個 |
| P | Aside Tip（**Round 4 追加**） | `blockquote.aside-tip` | 段內提醒 blockquote、左灰邊線（取代舊 `.tip-callout`、避開 lint `\bcallout\b` regex 誤判） | 不限 |
| Q | Layout Mockup（**Round 4-5 追加**）| `.layout-mockup` `.lm-frame` `.lm-row` `.lm-row.lm-main` `.lm-row.lm-tall` `.lm-row.lm-xtall` `.lm-row.lm-short` `.lm-row.lm-center` `.lm-cells` `.lm-cells.lm-3col` `.lm-cells.lm-2col` `.lm-cell` `.lm-cell.lm-tall` `.lm-pct` `.lm-sub` `.lm-caption` | 版型結構示意（CSS grid + border 替代 ASCII art、避免 CJK 對齊問題、深色背景 + 半透明灰邊框）。內部用 component-scoped CSS var（`--lm-bg/--lm-fg/--lm-border/--lm-muted/--lm-highlight`）封裝深色色票、不污染全域 token | CH2-1 8 版型 |

### 與既有組件的關係

- `.task-card` **取代** `.exercise-block`（PRAC 自訂、向後相容、舊頁不強迫換）
- `.self-check` **與** `.quiz-item` **並行**：self-check 在段內、quiz-item 在頁尾
- `.today-deliverables` **附加在** `.outcomes` 之後（hero 內最後一塊）
- `.instructor-note` **取代** 舊頁中以 `.callout.info`/`.callout.tip` 包教學意圖的用法
- `.wrong-example` **取代** 舊頁中以 `.callout.tip` 包錯誤例子的用法
- `.concept-pair` **與** `.compare-grid` 並行（前者是 2 卡、後者是 N 卡）

### 規則（必須遵守）

- **micro-cycle 內 callout 仍受「每頁 ≤ 4」限制** — 改用 `.wrong-example` `.self-check` `.closer` `.instructor-note` 等不算 callout 的容器
- **Section count 仍須 ≥ 5** — 每個 micro-cycle 算 1 個 lesson-section（外層用 `<section class="lesson-section micro-cycle">`）
- **所有 CSS 必須用 V4 15 階字型 + `--c-main` 4 處上限** — 不另開字型階、不另開色變數
- **`.task-card-stuck` 必須是 `<details>` 折疊**、預設 closed
- **`.learner-output-blank` 用 `contenteditable="true"` + `data-placeholder` 屬性** — 不用 `<input>`/`<textarea>`（避免送出邏輯）
- **`.instructor-note` 必須包在 `<details>`** 內、預設 closed、學員主流程不可看到展開內容

### lint 影響

`docs/lint-page.py` 此版**不對 class 名做白名單檢查**，只擋特定禁用 class（concepts-strip / case-block / quiz-block / hands-on-box / assets-box）與計數規則（callout ≤ 4 / lesson-section ≥ 5 / big-quote ≤ 1）。

**因此新增本節 8 組件不需要更新 `lint-page.py`、不會觸發 BLOCKER**。日後若加入「組件白名單強制檢查」，本節 class 應同步進白名單。

---

## 變更紀錄

| 日期 | 內容 |
|------|------|
| 2026-04-26 | v4 互動工作坊組件（8 組件），來源 gen-image 重構諮詢報告；嚴格派 `--c-main` 規範確立；合併設計規範.md；lint exclude `_pilots/`；CLAUDE.md 真相源字眼校正（依 Codex L3 audit `7dcf26e4`） |
| 2026-04-19 | v3 追加 6 節：距離層變數、serif 字階例外、色彩克制、組件白名單補充、Hover 規範、編號規範 |
| 2026-04-16 | 初版，從 CLAUDE.md / build-course-page / 設計規範.md 合併建立 |
