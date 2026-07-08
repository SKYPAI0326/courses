# _gates.md — admin-ai-assistant 品質檢核存證

> **一門課一份、append-only。** 每個 G 檢核點結束時把問答記在下面。
> 禁止刪除舊條目，要改就另開新條目並註明「修正前述 X」。

**課程 slug**：admin-ai-assistant
**負責人**：sky8697
**建立**：2026-07-08

---

## G1 大綱定位（PM → 設計師放行）

**日期**：2026-07-08
**問答**：

- Q1：6 個單元裡哪一個你最沒把握？為什麼？
  A：CH2（會議紀錄）。20 分鐘內要學員親手完成逐字稿→會議紀錄轉換，時間最緊、也最容易出現「討論中寫成已決議」的錯誤。已在 outline 加入「教學設計風險與對策」要求 course-designer 縮短素材、埋混淆點、加錯誤示範對照。

- Q2：受眾畫像跟你預想的客戶側寫有沒有對不上的地方？
  A：符合，無需調整。

- Q3：「學習成果」哪一條你覺得最浮泛、需要更具體？
  A：不是單條學習成果字句的問題，而是整體提示詞包的說服力不足——現代模型即使不用精確提示詞也常給出「看起來還可以」的輸出，導致學員覺得學不學都沒差。已在 outline 加入強制設計原則：CH2~CH5 每單元都要有「裸問 vs 結構化提示詞」並排對照，用真實輸出差異（誤植決議、捏造數字、遺漏待填、語氣格式不符）說服學員，而非用文字告知。

- Q4：這門課的品牌調性跟你既有課程有什麼差異？
  A：同意草稿寫法——2h 精簡 DEMO 定位，不追求完整工具教學，跟 140h/36h 完整職訓課或 office-ai-cases（6h 客製案例課）區隔開。

**結論**：☑ 放行

---

## G2 教案審核

**日期**：2026-07-08
**審核項**：

- ☑ 每單元 9 frontmatter 完整（CH1~CH6 逐一核對過）
- ☑ 6 正文區塊齊（教學流程/講師筆記/試跑包/商業情境/動手題/常見錯誤/檢核題，實際 7 個含講師筆記）
- ☑ 試跑包規格符合 course_type（skill-operation：均列出 Gemini/NotebookLM 帳號需求 + 具體示範素材 + 逐字提示詞）
- ☑ 商業情境案例具體、可驗證（全用欣怡/協理，公司弄一下顧問股份有限公司，任務具體到可檢查的產出物）
- ☑ 常見錯誤 3 條真實（非湊數，各單元均含具體錯誤現象如「捏造搬遷日期」「捏造講師費數字」）
- ☑ 檢核題 2 條有標準答案
- ☑ CH2~CH5 均落實「裸問 vs 結構化提示詞」並排對照（G1 核心教學主張）
- ☑ 禁用詞/跨課主角掃描乾淨（grep 掃 CH1~CH6，僅話術引號內「我們」，符合 style guide 例外規則）
- ☑ 依賴鏈與大綱一致（CH2/CH3/CH4/CH6 → [CH1]；CH5 → [CH4]）
- △ 行數：CH1~CH6 介於 144–207 行，低於模板建議 300–600 行區間，但 6 大區塊皆無空欄、密度與 CH1 一致，判斷為「2h 精簡 DEMO」定位下的合理篇幅，不強制灌水

**放行決定**：☑ Pass（無 Hard-fail 項）

---

## G3 講義驗收

**日期**：2026-07-08
**排版視覺**：Pass（7 頁全用 lesson-template-v3 骨架，主題色 #7a9ea3 均未超 4 處配額）
**敘事連貫**：Pass（CH1→CH6 導覽鏈完整，欣怡/協理主角一致，依賴鏈與大綱對齊）
**AI 味偵測**：Pass（grep 掃全站禁用詞/花式措詞用語乾淨，各單元 course-lesson-writer 回報 0 違規）
**試跑包驗證**：Pass（各單元均附逐字提示詞 + 示範素材，Gemini/NotebookLM 帳號需求明確）
**SEO / 連結 / 行為**：Pass（`python3 docs/lint-page.py courses/admin-ai-assistant/` → 0 BLOCKER / 0 ERROR / 2 WARN，皆為既有允許例外：CH2 serif 小標字階 `.78rem`〔design-tokens.md §v3〕、index.html hover 屬性數量〔沿用 ccs-foundations 既有 pattern〕）

**站台完整性**：`python3 docs/check-integrity.py` 顯示 admin-ai-assistant 尚未登錄 COURSES.md / inject_gate.py COURSES——此為 G4 course-register 步驟的預期狀態，非 G3 缺陷。（另有 4 條與本課無關的既有站台問題：courses/output/、courses/tmp/、gen-image、ntub-gtm-adtech 未登錄，屬既有債務，不在本課範圍內不動它們）

**飛輪**：本課無新發現需要轉 lint 規則的模式。

---

---

## G4 收尾

**日期**：2026-07-08
**項目**：

- ☑ 全站 `python3 docs/build-all.py` 全綠（lint --baseline 無 new BLOCKER、search-index 645 筆、sitemap 42 URL）
- ☑ `python3 docs/check-integrity.py` admin-ai-assistant 相關 0 ERROR
- ☑ inject_gate.py 已登錄（adminai_auth）、8 頁全部注入 gate、密碼記錄於本地密碼對照表（不進 git）
- ☑ COURSES.md 已加入本課表列
- ☑ 統一入口頁（根目錄 index.html）「AI 入門與工作應用」組加卡片（band-5 灰藍綠），組計數 9→10 門
- ☑ build-search-index.py COURSE_LABEL 已登錄
- ☑ _outlines/admin-ai-assistant.md 與最終章節對齊（CH6 標題/成果已隨 Codex 修正同步）
- 註：sitemap 從 51→42 URL 屬設計行為（密碼頁排除於 sitemap）；本次 inject 同時修復 codex-basic 10 頁缺 gate 的既有問題（順手修復，非本課範圍）

**檢討**：
- 本課最耗時：CH6 平台機制三輪修正（人工貼上→Gem 掛載→成長迴圈→Codex 降承諾）。教訓已存記憶：平台功能先查證 + 先對照站內已驗證課程（gemini-notebooklm-workshop/CH3）
- 下一課想改的流程：涉及 Gemini/NotebookLM 串聯的單元，教案階段就強制引用 CH3 已驗證架構為基準，不從零寫

### 補件：課後可帶走資產頁（2026-07-08，使用者主動要求）

使用者在 G3 過關後追問「行政 Gem 系統提示詞、NotebookLM 資料是否具備」，發現原本 7 頁只有各單元內嵌的零散提示詞，沒有可帶走的整合資產。已補建 `courses/admin-ai-assistant/prompt-library.html`，含：

1. 行政 AI 虛擬助理 Gem 系統提示詞（完整組合版，七條規則，可直接貼進 Gemini 自訂 Gem）
2. NotebookLM 示範素材（逐字沿用 CH6 的請假流程說明 + 新人請假常見問題整理）
3. AI 產出檢核清單整合版（決議/數字/日期/承諾/待填五大類）
4. 行政虛擬助理使用流程卡（6 步驟，含進階留底步驟）

`index.html` 已加連結。`python3 docs/lint-page.py courses/admin-ai-assistant/` → 8 頁，0 BLOCKER / 0 ERROR / 2 WARN（皆既有允許例外）。

### 修正：CH6 改為 Gem 原生掛載 NotebookLM 架構（2026-07-08，修正前述 G2/G3 的 CH6 內容）

使用者指出 CH6 教的「NotebookLM 查詢→人工複製貼上→Gemini 產出」是過時做法。查證確認：Gemini Gem 自 2025-12 起原生支援在「加入檔案供 Gem 參考」選單直接掛載 NotebookLM 筆記本（自動同步、附引用），且本站 gemini-notebooklm-workshop/CH3 已用此正確架構授課。教訓再次應證 feedback_platform_spec_drift_verify：平台規格問題必先查證 + 先對照站內已驗證課程，不可憑訓練知識回答。

已修正（lint 重跑 8 頁 0 BLOCKER，search-index/sitemap 已重建）：
- `_lessons/admin-ai-assistant/CH6.md` 全面改版：「三條資料匯入路徑＋人工帶回 Gemini」→「6 步驟動手建連結 NotebookLM 筆記本的 Gem」，title/learning_objective/動手題/常見錯誤/檢核題全數更新
- `CH6.html` 依新教案重建（steps-wrap 6 步驟、來源狀態標示、動手題改實作）
- `prompt-library.html` 資產 1 Gem 系統提示詞改版：規則一改為「知識來源優先順序（①連結的 NotebookLM 筆記本 ②對話提供資料 ③推論）」、規則七加來源狀態標示（✅/🧠/❓）；資產 2/4 與頁首使用建議同步改為掛載架構
- `_outlines/admin-ai-assistant.md`（Outcome 6、試跑包 CH6、單元矩陣 CH6）、`index.html`（hero/outcome/CH6 卡片）、`CH1.html`（CH6 預告 callout）、`CH5.html`（導覽按鈕文字）同步更新

### 補強：成長迴圈架構（2026-07-08，使用者重新聚焦課程核心機制）

使用者定義本課核心機制為「NotebookLM 保存規範/資料/紀錄 + Gem 掛載連接 + Gem Prompt 設規則邊界 + 資料為本併用 LLM/網路檢索 + 有價值對話回流筆記本 + 網路資料整併進筆記本 = 隨使用成長的助理」。比對後發現三缺口並已修正（WebSearch 查證 Gemini 原生「新增至筆記本」功能存在、筆記本跨 Gemini/NotebookLM 自動同步後才動工）：

1. **系統提示詞開放網路層**：資產 1 規則一從三層（筆記本→對話→推論、禁上網）改為四層（筆記本→對話→網路搜尋→推論），網路限「時效性查證/背景補充」且須與知識庫分開標示；規則七來源狀態加 🌐 標記（對齊 gemini-notebooklm-workshop/CH3 的四層架構）
2. **對話回流路徑**：CH6 教案+HTML 新增「讓助理成長的兩條回流路徑」——路徑一教 Gemini 原生「新增至筆記本」（非手動複製貼上）
3. **網路資料整併路徑**：路徑二教把公開網頁連結加進筆記本當來源、Gem 回答分開標示公司規定與網路來源

連動更新：CH6 概念區加「回流」卡片、來源狀態改三層標示、檢核/self-check/試跑包步驟（+回流兩步）、講師筆記（時間重分配 + 回流實機示範 + 「新增至筆記本」帳號可用性課前驗證）、資產 4 流程卡進階步驟改兩條回流路徑。lint 0 BLOCKER，search-index/sitemap 已重建。

### 補強：任務規範文檔派工機制（簡易 skill 架構，2026-07-08，使用者授權）

使用者提議「規則文檔＋提示詞點名調用」的簡易 skill 架構。確認 Gemini 無 @文件語法（@ 是給連接的應用程式），但「《文檔名》點名 + RAG 檢索」可達同等效果。已實作：

1. **資產 5．任務規範文檔 ×4**（prompt-library.html 新增群組）：《規範｜會議紀錄整理》《規範｜Email 公文通知》《規範｜資料彙整摘要》《規範｜簡報內容包》，各 5 條規則、附派工句，貼進「行政知識庫」筆記本當來源
2. **系統提示詞規則八（派工表）**：收到任務先判斷類型→讀對應《規範｜…》→照文檔作業；點名優先；**輸出開頭固定回報「本次適用規範」+ 2~3 條關鍵規則**（防呆核心：驗證真的讀了文檔）；找不到規範要明講、不可裝作有讀到
3. **CH2~CH5 各加「進階」callout**（教案+HTML）：本章規則可存成《規範｜…》文檔，日常派工縮成一句話
4. **CH6 成長迴圈補「規範文檔也是知識庫來源」段落**、資產 4 流程卡步驟二改「丟資料＋一句派工」、index.html 資產庫連結描述、outline 試跑包規格同步

已知風險（記錄於資產 5 使用說明）：RAG 檢索非確定性調用，靠「本次適用規範」回報驗證是否生效；規範文檔一任務一份、條列短文以維持遵循率。lint 8 頁 0 BLOCKER，search-index/sitemap 已重建。

### G5 Codex L3 全課審核與修正（2026-07-08）

Codex consult `57fbaa72`（330.8s，讀 15 檔 4,566 行）總評「修完再上線」：2 BLOCKER、8 MAJOR、4 MINOR。verdict 標記 `actionable`（14 條採納 13 條；MINOR 4 之 CH2 `.78rem` 為 design-tokens §v3 允許例外、index hover 沿用既有 pattern，判 noise 不修）。抽查證實 CH2 示範表格確把「約月底」線索升級成期限、CH4「實際確定人數 15」為 AI 加總指標——皆違反本課自己教的規則，屬最傷教學可信度的一類。

修正全數完成（lint 8 頁 0 BLOCKER / 0 ERROR / 2 允許例外 WARN）：
- **BLOCKER 1+MAJOR 7（CH6 功能承諾）**：掛載/自動同步/新增至筆記本全改條件式敘述＋fallback（看不到 NotebookLM 選項→上傳 Gem Knowledge 檔；沒有新增至筆記本→複製到 Google 文件再手動加來源）
- **BLOCKER 2（25 分鐘過度樂觀）**：CH6 改「講師完整示範＋學員最小完成線」（課堂：筆記本+1 來源+引用標記；完整建置課後照資產頁步驟卡），self-check 拆兩層
- **MAJOR 1（派工非確定性）**：規則八回報升級為「規範名+來源標題+引用 2 條原文，引用不出就停」；資產 5 與 CH2~CH6 措辭改「初步檢查、抽查對回原文」
- **MAJOR 2（規則一/四衝突）**：規則四改「內部數字只能來自筆記本/使用者；外部公開數字可來自網路但標來源+查詢日期、不可混寫」
- **MAJOR 3（CH2 示範自違規）**：期限「待預算核准（約月底）」→「〔待填〕（預算可能月底核准，需確認）」＋線索不升級原則註記
- **MAJOR 4（CH4 指標未定義）**：改三欄位「表單有效 18／已繳費確認 15／未繳費待確認 3」，不自創「實際確定人數」
- **MAJOR 5（CH5 案例斷裂）**：CH5 全段從虛構三部門改為真正承接 CH4 教育訓練案例，數字逐字對齊（18/15/3、23,400、講師費衝突未定），裸問錯誤示範與 CH4 常見錯誤呼應
- **MAJOR 6（限額無日期）**：CH6 加學員可見「平台限制與帳號檢查」區塊（50/50/10 標 2026-07 查證、以實測為準＋開課前兩項帳號檢查）
- **MAJOR 8（術語密度）**：CH6 概念區加白話對照表（掛載/派工/來源狀態/回流）
- **MINOR 1~3**：CH4 教案簡體字、CH1「六章→五章」、CH3「五個關鍵概念→四個關鍵概念與一個風險提醒」
- **連動**：index.html CH6 卡片同步改條件式描述

search-index/sitemap 已重建。課程狀態：Codex 修正完畢，待使用者最終確認後跑 `/course-register admin-ai-assistant` 上線。

---

## 備忘（非 Gate 但值得留存）

- 來源文件：《行政AI虛擬助理_2小時課程介紹.docx》（使用者提供，2026-07-08 讀取）
- 本課 CH6「完整方案：NotebookLM×Gemini 串聯助理」為獨立精簡改寫，不引用 gemini-notebooklm-workshop 頁面
- 主題色 #7a9ea3（灰藍綠）與 ccs-foundations / gen-ai-36h / prompt-basic 共用色票，使用者已知情並確認選用
