# 生成式 AI 工作應用班（36h）— 專案規範

---

## 專案定位

弄一下工作室出品，140h 訓練班的「上班族濃縮版」。
- 學員：零基礎上班族，沒寫過程式
- 不涵蓋：API / RAG / Agent / Function Calling
- 主軸：基本對話與核對 + 來源筆記 + 小工具測試 + 人工覆核後 Make 自動化 + 結業專題；n8n 為選做

- **課程根目錄**：`courses/gen-ai-36h/`
- **課程入口**：`courses/gen-ai-36h/index.html`
- **課程大綱**：`_outlines/gen-ai-36h.md`
- **觸發詞**：「繼續 36h 課程」

---

## 暫停 / 恢復協議

遵循全域協議（`~/.claude/CLAUDE.md`），本專案差異：

- **觸發詞**：「繼續 36h 課程」
- **恢復額外步驟**：讀 `index.html` 確認哪些 lesson-card 還是 `locked` 狀態

---

## 檔案結構

```
gen-ai-36h/
├── index.html      課程總目錄（含 7 個 Part 導覽）
├── CLAUDE.md       本檔
├── part1/          AI 基礎與提示詞（3 CH + 1 PRAC）
├── part2/          辦公室高頻寫作自動化（3 CH + 1 PRAC）
├── part3/          知識管理與會議協作（2 CH + 1 PRAC）
├── part4/          零代碼 AI 工具開發（4 CH + 1 PRAC）
├── part5/          人工覆核與 Make 自動化（4 CH + 1 PRAC）
├── part6/          個人 AI 系統整合（2 CH + 1 PRAC）
└── part7/          結業專題（3 CH + 1 PRAC）
```

**檔案命名規則：**
- 章節頁：`CH章-節.html`（如 CH4-2.html）
- 實例演練：`PRAC章.html`（每 Part 只有 1 份 deliverable，如 PRAC4.html）

---

## 課程單元總覽（28 單元 · 36h）

| Part | 主題 | 單元 | 時數 |
|------|------|------|------|
| 1 | AI 基礎與提示詞 | 3 CH + 1 PRAC | 4h |
| 2 | 辦公室高頻寫作自動化 | 3 CH + 1 PRAC | 6h |
| 3 | 知識管理與會議協作 | 2 CH + 1 PRAC | 4h |
| 4 | 零代碼 AI 工具開發 | 4 CH + 1 PRAC | 8h |
| 5 | 人工覆核與 Make 自動化 | 4 CH + 1 PRAC | 6h |
| 6 | 個人 AI 系統整合 | 2 CH + 1 PRAC | 4h |
| 7 | 結業專題 | 3 CH + 1 PRAC | 4h |

---

## 設計規範

- 主題色：**灰藍綠 `#7a9ea3` (--c-a5)**——topbar tag、進度條、CTA 一律用主色
- Part band 配色（lesson-band）：
  - Part 1：陶土橘 band-1
  - Part 2：芥末黃 band-2
  - Part 3：鼠尾草綠 band-3
  - Part 4：霧藍 band-4
  - Part 5：灰藍綠 band-5
  - Part 6：陶土橘 band-1（循環）
  - Part 7：鼠尾草綠 band-3（循環）
- 字體：標題 Shippori Mincho 700，內文 Noto Sans TC
- 禁止漸層、深色背景、鮮豔高彩色

---

## 內容資產來源（建頁面時優先參考）

| Part | 既有素材來源 |
|------|------------|
| 1 | `office-ai/Part 1` + `gen-ai-140h/Part 1.3-1.4` |
| 2 | `gen-ai-140h/Part 2` 精華 + `office-ai/Part 2` |
| 3 | `office-ai/Part 3` + `gemini-ai` 免費工具庫 |
| 4 | `gemini-ai/Part 2-3` + `gen-ai-140h/Part 4` |
| 5 | 本課九欄教學資料、已覆核新列與 Make 測試流程；n8n 僅選做參考 |
| 6 | `office-ai/Part 4` + `ai-workshop/Session 6` |
| 7 | `gen-ai-140h/Part 7` 精簡版 |

---

## 新增頁面標準流程

每次建立一個新的 CH 或 PRAC 頁面：

1. 讀 `_outlines/gen-ai-36h.md` 取得該單元的學習目標與內容要點
2. 對照「內容資產來源」表，先讀來源課程的對應頁面，避免重新發明
3. 參考同 Part 已有的 HTML 確認配色、版型、字型一致
4. 用 build-course-page skill 的 step-page 範本建立 HTML
5. 更新 `index.html`：將對應卡片從 `locked href="#"` 改為實際路徑，`status-lock` → `status-available`，`建置中` → `可學習`

---

## 飛輪規則

錯誤轉規則的累積清單見 `_規範/飛輪規則.md`。發生新錯誤時補一條至該檔。

## 2026-10-09 教學修訂

正式正文由 `_repair/2026-10-09/lesson-plans/` 的 learner-content 範圍轉製；同步至全站 `_lessons/gen-ai-36h/`。28頁URL、設計、導覽與密碼關卡保留。
七欄工具卡統一；PRAC6/7使用各自本機保存鍵與JSON備份。Make使用ReviewedQueue新列觸發，九欄、四分類、待覆核／已覆核，只寫未寄出草稿。教學工作區已跑T01–T07；原有五份AI秘書藍圖保留為進階延伸，對照見`assets/part5-existing-blueprints-guide.md`。
素材見 `assets/START-HERE.md`；備份、還原、執行證據與待驗項目見 `_repair/2026-10-09/`。未完成瀏覽器／平台／真人試走不得稱開課就緒。
