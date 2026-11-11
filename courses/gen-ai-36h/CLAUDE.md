# 生成式 AI 工作應用班（36h）— 專案規範

---

## 專案定位

弄一下工作室出品，140h 訓練班的「上班族濃縮版」。
- 學員：零基礎上班族，沒寫過程式
- 不涵蓋：API / RAG / Agent / Function Calling
- 主軸：學員指揮生成式 AI 完成工作——對話與追問 + 文字與附件處理 + NotebookLM 文件問答 + AI 生成小工具 + AI 整理後交 Make 自動處理 + 個人 AI 工作流程 + 結業專題；n8n 為選做。分工、核對、承接與用語規則見下方「核心方法與分工」

- **課程根目錄**：`courses/gen-ai-36h/`
- **課程入口**：`courses/gen-ai-36h/index.html`
- **課程大綱**：`_outlines/gen-ai-36h.md`
- **觸發詞**：「繼續 36h 課程」

---

## 核心方法與分工

改寫與新增學員頁時一律遵守（共用技能依 `_規範/learner-action-contract.md`「核心方法、分工與正文用語」讀取本節）。

- 核心方法：學員指揮生成式 AI。完成物主項是 AI 做出的成果（摘要、信件、表格、小工具等）；核對紀錄只附在後面。Make 流程頁的完成物，看流程是否接上前面用 AI 做出的成果，流程本身不必含 AI。
- 核對：交給 AI 標出處、列依據、比對差異，或換一個模型交叉檢查；學員只抽看 AI 指出的 3 處以內，決定採用、修改或重問。學員的修改紀錄、反思或比較說明，也先請 AI 起草，學員只修改或確認。不安排逐句、逐欄、逐筆人工比對，也不安排多組輸入逐一記錄的測試矩陣。練習後的自查與對照參考答案也算核對：請 AI 比較學員版本和參考答案差在哪、挑出最需要看的 3 處以內，學員看完再決定；不另設學員自己逐點勾核的清單。
- 單人完成：每頁一個人就能做完；需要同事、委託人或使用者的角色時，開新對話請 AI 扮演。
- 承接：每個 `##` 段的第一句接住上一段的具體結果。CH 頁結尾說明下一節會怎麼用本節成果；PRAC 頁收回本 Part 學會的能力並說明下一個 Part 延伸到哪裡；PRAC7 收回全課能力與之後怎麼用。
- 用語：學員是零基礎上班族，正文不用案例碼、英文欄位名、章節碼；必須照填的代碼同一句附內容說明，每段第一次出現時再說明。
- 驗收：依 `_review/2026-11-01/rubric.md` v1.1。各頁標題與完成物以 `_outlines/gen-ai-36h.md` 為準。

---

## 接續工作

使用者說「繼續 36h 課程」時，先讀 `index.html` 確認哪些 lesson-card 還是 `locked` 狀態。

---

## 檔案結構

```
gen-ai-36h/
├── index.html      課程總目錄（含 7 個 Part 導覽）
├── CLAUDE.md       本檔
├── part1/          AI 基礎與提示詞（3 CH + 1 PRAC）
├── part2/          用 AI 處理辦公文字與附件（3 CH + 1 PRAC）
├── part3/          用 NotebookLM 從文件找答案（2 CH + 1 PRAC）
├── part4/          用 AI 做出工作小工具（4 CH + 1 PRAC）
├── part5/          用 AI 整理訊息，交給 Make 自動處理（4 CH + 1 PRAC）
├── part6/          建立自己的 AI 工作流程（2 CH + 1 PRAC）
└── part7/          結業專題：用 AI 完成一件自己的工作（3 CH + 1 PRAC）
```

**檔案命名規則：**
- 章節頁：`CH章-節.html`（如 CH4-2.html）
- 實例演練：`PRAC章.html`（每 Part 只有 1 份 deliverable，如 PRAC4.html）

---

## 課程單元總覽（28 單元 · 36h）

| Part | 主題 | 單元 | 時數 |
|------|------|------|------|
| 1 | AI 基礎與提示詞 | 3 CH + 1 PRAC | 4h |
| 2 | 用 AI 處理辦公文字與附件 | 3 CH + 1 PRAC | 6h |
| 3 | 用 NotebookLM 從文件找答案 | 2 CH + 1 PRAC | 4h |
| 4 | 用 AI 做出工作小工具 | 4 CH + 1 PRAC | 8h |
| 5 | 用 AI 整理訊息，交給 Make 自動處理 | 4 CH + 1 PRAC | 6h |
| 6 | 建立自己的 AI 工作流程 | 2 CH + 1 PRAC | 4h |
| 7 | 結業專題：用 AI 完成一件自己的工作 | 3 CH + 1 PRAC | 4h |

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
| 5 | 本課九欄教學資料（由 AI 整理產生）與 Make 測試流程；n8n 僅選做參考 |
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

## 2026-10-09 教學修訂（2026-11-01 更新）

2026-11-01 起，學員正文以 `_lessons/gen-ai-36h/` 為唯一落筆層，改完再轉製 HTML；`_repair/2026-10-09/lesson-plans/` 只保留教師與版本紀錄。28頁URL、設計、導覽與密碼關卡保留。改寫驗收依 `_review/2026-11-01/rubric.md`（v1.1）三套標準；改寫規劃見 `_review/2026-11-01/rewrite-plan.md`。
七欄工具卡統一；PRAC6/7使用各自本機保存鍵與JSON備份。Make 主線：AI 把訊息整理成九欄資料列並分類，AI 標出沒把握的列由學員決定，新列進入 ReviewedQueue 後由 Make 觸發分流，只寫未寄出草稿。教學工作區已跑T01–T07，T01–T07 為教師驗收用，學員頁不出現測試碼；原有五份AI秘書藍圖保留為進階延伸，對照見`assets/part5-existing-blueprints-guide.md`。
素材見 `assets/START-HERE.md`；備份、還原、執行證據與待驗項目見 `_repair/2026-10-09/`。未完成瀏覽器／平台／真人試走不得稱開課就緒。
