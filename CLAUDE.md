# 弄一下工作室 — 課程網頁專案規範

---

## 課程建立觸發流程

看到「課程、講義、工作坊、教材、Module、章節、步驟頁」等關鍵詞，**主動詢問後執行**，不等 `/build-course-page`。

### Step 0（必做）：讀課程大綱
執行任何頁面建立前，先嘗試讀取 `_outlines/{slug}.md`：
- **存在** → 從 frontmatter 取得主題色、學員背景、工具；從章節列表推導前後頁；略過已知資訊的詢問
- **不存在** → 繼續下方詢問流程

### 詢問流程（大綱不存在時）
- **全新課程**：一次詢問名稱、學員、工具、Module 數量、機構、主題色；同步建立 `_outlines/{slug}.md`
- **新增步驟頁**：詢問 Module 編號、節次（如 3.1）、標題、操作內容
- **執行前必讀**同目錄現有 HTML，確認主題色與導覽格式

---

## 飛輪規則

每當 Claude 犯錯（格式不對、命名跑掉、連結失效、邏輯錯誤），立刻將該錯誤轉為一條具體規則加入此文件的對應區塊。CLAUDE.md 會因此持續進化，同樣的錯誤不再發生第二次。

### 複製按鈕定位規則

- **絕對定位的複製按鈕必須同步設定父容器 padding-right**：若 `.step-example-copy`（或同類 copy button）使用 `position:absolute;top:Xpx;right:Ypx`，其父容器必須加 `padding-right:72px`，否則文字會被按鈕覆蓋
- 格式：`padding:14px 72px 14px 16px`（四值寫法，保留左側 16px 不變）
- 建立新頁面時，有 absolute copy button 的地方一律加 `padding-right:72px`

### WordPress 資料庫操作規則

- **禁止**用 Python mysql.connector 讀出 `post_content` 再寫回——會雙重跳脫 `\n` 與 `\u002d`（`--`），導致排版崩潰與 CSS 變數失效
- **必須**用 MySQL `REPLACE()` 直接在資料庫內操作，例如：
  ```sql
  UPDATE wp_posts SET post_content = REPLACE(post_content, '舊值', '新值') WHERE ID=N;
  ```
- 修改後用 `HEX()` 確認關鍵字元（換行應為 `0A`，連字符應為 `2D`）

---

## 回答行為規則

- 直接回答，第一行就是答案，不要開場白（禁止「好的！」「當然！」「Great question!」）
- 不要結尾客套話（禁止「希望這有幫助」「如有問題請告知」）
- 不要重複或改寫我的問題，直接執行
- 不確定的事情直接說「我不確定」，不要猜測或捏造
- 只做我要求的範圍，不要主動改動我沒提到的檔案或區塊
- 不要加入我沒要求的功能或「順便優化」
- 同一個檔案不要重複讀取

---

## 模型使用規則

每次對話開始時，根據任務類型主動建議切換模型：

- 開始新章節、規劃結構、複雜設計 → 提示「建議切換 /model opus」
- 一般修改、調整樣式、加功能 → 維持 Sonnet，不需提示
- 大量搜尋、讀取檔案、重複性整理 → 提示「建議切換 /model haiku」

每次提示只說一句，格式：「💡 這個任務建議使用 [模型]，輸入 /model [指令] 切換」

---

## 專案基本資訊

- **專案名稱**：弄一下工作室（課程專用網頁）
- **專案路徑**：`/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁`
- **課程資料夾**：`courses/` 下的 `ai-workshop/`、`gemini-ai/`、`gtm/`、`n8n/`、`office-ai/`
- **命名對照表**：`COURSES.md`（各課程資料夾說明）
- **規範資料夾**：`_規範/`（本地參考用，已 gitignore）

---

## 設計系統

### 色彩系統

| 變數名 | 色碼 | 用途 |
|--------|------|------|
| `--c-bg` | `#f5f3ee` | 背景（米白） |
| `--c-surface` | `#edeae3` | 側欄背景（淺灰米） |
| `--c-card` | `#ffffff` | 卡片背景 |
| `--c-border` | `#d8d4cb` | 邊框（暖灰） |
| `--c-text` | `#2c2b28` | 主文字（深褐黑） |
| `--c-muted` | `#7a766d` | 次要文字（灰褐，WCAG AA 對比度 4.7:1） |
| `--c-a1` | `#b5703a` | 陶土橘 — 主要按鈕、重點標記 |
| `--c-a2` | `#c9963a` | 芥末黃 — 次要強調 |
| `--c-a3` | `#5a7a5a` | 鼠尾草綠 — 正確/完成狀態 |
| `--c-a4` | `#6b7fa3` | 霧藍 — 資訊、程式碼關鍵字 |
| `--c-a5` | `#7a9ea3` | 灰藍綠 — 輔助色 |

每門課程各自使用一個強調色作為主色（見 `COURSES.md`）。

**嚴禁自創 `--c-a6` 及以上變數**。若需要新色，先與既有 a1–a5 比對，若無法對應則提出新增色彩系統的討論，不得各頁自行定義。

### 字體

| 用途 | 字體 | Weight |
|------|------|--------|
| 標題 | Shippori Mincho（明朝體） | 700 |
| 內文 | Noto Sans TC | 400 / 500 |
| 程式碼 | Courier New | — |

從 Google Fonts 載入：`Shippori+Mincho:wght@400;500;700` 和 `Noto+Sans+TC:wght@400;500;700`

### 版面規則

- 圓角：`6px`（一般元件）/ `4px`（小元件）
- 邊框：`1px solid`，無陰影，無漸層
- 內容區 padding：`48px`（左右）
- 卡片內距：`22px 24px`（上下 22，左右 24）；若卡片右側有 absolute 元件（如複製按鈕），右側改 `72px`
- 頂部列高：`56px`（sticky）
- 底部列高：`52px`
- 最大內容寬：`960px`（總覽頁）/ `780px`（長文單元頁），置中
- Hover 反饋：只用 `transform` + `border-color` 變化，**禁止 box-shadow**
- Focus：所有 `a` / `button` / `input` 必須顯示 `:focus-visible` 2px outline（已全域注入 `outline:2px solid var(--c-text)`）

### 禁止事項

- 不使用漸層（gradient）
- 不使用深色背景
- 不使用鮮豔高彩度顏色
- 標題不使用漸層文字效果
- 圓角不超過 `8px`
- 不使用 `box-shadow`（2026-04-16 全站清理後禁止回流）
- 不自創 `--c-a6`+ 變數（違反會被飛輪規則抓到）

### SEO & 無障礙（新頁必做）

- 每頁 `<title>` 後必須有：`meta description`、`og:title/description/url/image`、`twitter:card` 系列、`link rel="canonical"`
- 導覽用箭頭 `←` / `→` 必須包 `<span aria-hidden="true">...</span>`
- 長文單元頁（含 `.progress-fill`）須注入 localStorage 進度腳本（樣本見任一 2026-04-16 後的單元頁 `</body>` 前）
- 新頁加入後需手動重跑 sitemap 產生器（或用 Python 腳本重掃 `courses/**/*.html`）
- 每頁 `<body>` 起始第一個元素（或 gate 之後）必須是 `<a href="#main" class="skip-link">跳至主要內容</a>`，主要內容區塊用 `<main id="main">` 包起來
- 搜尋索引：新頁加入後需手動重跑 `docs/build-search-index.py`（產生 `search-index.json`）

### 單元頁範本（新增單元頁必用）

新建任何 `CH*-*.html` / `PRAC*-*.html` / `m*-*-*.html` 單元頁：

1. **先複製** `_規範/lesson-template.html` 為新檔（不要從零寫）
2. **逐一取代** `{{SECTION_NO}}` / `{{ACCENT_VAR}}` / `{{ACCENT_HEX}}` 等所有佔位符
3. **保留**：skip-link、`<main id="main">`、focus-visible 規則、progress-fill、localStorage 進度腳本
4. **禁止**：回流自創 `--c-a6+` 變數、box-shadow、漸層、刪除 `aria-hidden` 的箭頭 span
5. **完成後** 重跑 sitemap + search-index 產生器

⚠️ 既有單元頁已於 2026-04-16 批次對齊基準標準（SEO meta、focus-visible、localStorage 進度、aria-hidden 箭頭）。新增頁缺任一項視為 regression。

---

## 檔案命名規則

| 類型 | 格式 | 範例 |
|------|------|------|
| 課程資料夾 | 小寫連字號英文 | `gemini-ai/`、`office-ai/` |
| 課程總覽頁 | `index.html` | — |
| 單元頁 | `CH[章]-[節].html` | `CH1-1.html` |
| 實例演練頁 | `PRAC[章]-[節].html` | `PRAC1-1.html` |
| 模組總覽頁 | `module[N].html` | `module1.html` |
| 課程大綱文件 | `course-outline.docx` | — |

---

## 編碼規範

- 縮排：2 個空格
- 語言：HTML5 + CSS3 + 原生 JavaScript（非必要不引入框架）
- 中文編碼：UTF-8，`<meta charset="UTF-8">`
- 圖片路徑使用相對路徑
- 所有 HTML/CSS/JS 寫在單一檔案內（除非特別指定分離）
- CSS 使用 minified 單行格式（節省檔案大小）
- 不新增 JavaScript 依賴，互動效果用純 CSS 或 inline event handler
- 觸及 3 個以上檔案的任務，先列出要改哪些檔案與每步驗收標準，再動手
- 修改前必須讀取目標檔案，確認現況再動手
- 局部修改用精準替換，不重寫整個檔案
- 完成前確認所有修改的連結與邏輯正確，再回報完成

---

## 輸出格式

- 程式碼直接給，不需要解釋每一行（除非我問）
- 若需說明，三句話以內
- 若有多個選項，列出最多兩個並說明差異
