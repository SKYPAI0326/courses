# 弄一下工作室 — 課程網頁專案規範

---

## ⚡ 頁面合規檢查（所有 HTML 檢查/修正先讀這裡）

任何 HTML 頁面的**結構、SEO、設計系統、禁用組件**檢查 **一律跑 lint**，不靠自己 grep：

```bash
python3 docs/lint-page.py <file.html>     # 單頁
python3 docs/lint-page.py courses/<slug>/ # 整課
python3 docs/lint-page.py --all           # 全站
python3 docs/lint-page.py --changed       # 只查 git staged 檔
```

- **Exit 0** = 無 BLOCKER，可放行
- **Exit 1** = 有 BLOCKER，看輸出修正
- `--no-warn` 只看 BLOCKER + ERROR
- `--summary` 只看統計

**`docs/lint-page.py` 是所有 HTML 規則的唯一真相源**。要改規則去改那個腳本，不要在本檔或 skill 文件追加散文規則。

### 頁面修正完、commit 前

- `python3 docs/build-search-index.py`（重建搜尋索引）
- `python3 docs/build-sitemap.py`（重建 sitemap）
- `git commit`（pre-commit hook 自動再跑一次 lint，BLOCKER 會擋下）

### 新課上線

見 `_規範/課程製作團隊系統手冊.md` v2.0，或直接跑 `/course-register <slug>`。

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

錯誤轉規則的累積清單已移至 `_規範/飛輪規則.md`。發生新錯誤時補一條至該檔，不寫在 CLAUDE.md。

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

**色彩 / 字型 / 版面 / 禁用 / SEO / 單元頁範本**規則 **不在本檔列出**，一律以下列真相源為準：

| 真相源 | 用途 |
|-------|------|
| `_規範/design-tokens.md` | 設計系統人類閱讀版（CSS 變數、字型 8 階、組件白名單、SEO 模板、metadata 規格） |
| `_規範/lesson-template-v3.html` | 單元頁骨架，新增頁面一律從這份複製 |
| `docs/lint-page.py` | 機器強制版（BLOCKER/ERROR/WARN 規則）。`python3 docs/lint-page.py <file>` 自動驗 |

**要調整規則？** 改 `design-tokens.md` + `lint-page.py`。**不要**在本檔或 skill 文件追加散文規則。

**新建單元頁？** 複製 `_規範/lesson-template-v3.html` → 填佔位符 → 跑 lint → 跑 `build-search-index.py` + `build-sitemap.py`。

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
