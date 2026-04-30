# 140h 課堂即時作業 — 設計規格

- 文件版本：v0.4
- v0.4 更新（Part 5 處理策略）：
  - **Part 5（前端實戰）採跨章「個人作品集網站」case**：CH5-1 v1（純 HTML/CSS）→ CH5-2 v2（AI 迭代改寫 + 互動）→ CH5-3 v3（push GitHub Pages 上線）→ CH5-4 v4（加 AI chatbot 後端代理）。學員 4 章後有真實作品集可放履歷。
  - **與 Part 1-4 風格差異記錄**：Part 1-4 學員產出是 prompt / 工作流文件 / 評估報告；Part 5 學員產出是 **HTML/CSS/JS code + Git commits + 部署 URL**。動手做、能訪問才算過關。
  - **學員主題自選**：3 個建議主題（個人作品集 / 工作室介紹 / 履歷網站），允許自帶。指定情境性質完全不同於 Part 1-4 的 Lina/Daniel/Mira 等角色。
  - **與 PRAC5-1~5-4 互補**：PRAC 是「練小頁」，CH5 assignment 是「跨章整合大作品」。
- 文件版本：v0.3
- 建立日期：2026-04-30
- v0.3 更新（CH1-1 完成後校準）：
  - **CHECKPOINT 全課移除**：18 個 CH 頁的 `instructor-check` 已批次砍除（原因：學員不願分享、assignment 已接管課堂節奏切點職能）。第 1.2 節組件盤點移除該列，第 3.1 節順序圖簡化。
  - **assignment 拆「核心 20 + 進階 20」**：CH1-1 實測 30–40 分鐘負擔過重，採 Codex 第二輪建議改拆兩段。第 2.2 節素材深度補拆解規格。
  - **mini-prac 銜接強化**：填法示範段補「直接拿前面 mini-prac 寫的 prompt 來用」提示，避免學員從零開始。第 3.1 節 HTML 模板補此區塊。
  - **待驗證項目清單**：第 7 節新增 4 條等真實課堂驗證的觀察點（transfer / 拆分合理性 / 工時實測 / CHECKPOINT 移除影響）。
- v0.2 更新：(1) 補盤點現有 SOLO/CHECKPOINT 區塊與整合策略；(2) 下載原則精確化為「檔案類素材才下載」；(3) 執行策略從「試點 3 章評估」改為「一次一章順序完善」
- 目標課程：gen-ai-140h（生成式 AI 職訓實務應用班）
- 影響範圍：56 單元中的 CH 章節頁（10 個 CH）+ 少數整合性章節升級獨立頁

---

## 1. 背景與動機

### 1.1 學員回饋

現有兩種教學頁（CH 章節頁、PRAC 互動工具頁）已上線，但學員回饋：
- CH 內既有的 mini-prac 短練習**題目偏概念對標、缺真實素材**，學員仍要自行假想客戶/數據/檔案的樣子才能做。
- PRAC 整頁是**互動工具**（學員操作工具完成作品），不是「題目+素材+解答」結構的作業。
- 缺一塊「**有完整商業情境 + 詳細素材 + 標準解答**，讓學員當堂運用該節技巧」的課堂作業。

### 1.2 現有組件盤點（決策不重蹈設計）

| 組件 | 位置 | 顆粒 | 現況 / 本設計關係 |
|------|------|------|------|
| `mini-prac` 迷你練習 | CH 內嵌（全 Part） | 5–10 分鐘暖身 | **保留不動**，當作正式作業前的暖身 |
| `result-compare` 三模型對打 | CH 內嵌（部分 Part 3+ 章節） | 10–15 分鐘 | **保留不動** |
| `peer-handoff` SOLO·自我演練 | CH 內嵌（Part 3, 4） | 5–8 分鐘自練 | **題目改寫**：寄生 assignment 素材，學員「同素材換角度再練一次」（transfer practice）。組件本身不動 |
| ~~`instructor-check` CHECKPOINT·講師檢核~~ | ~~CH 內嵌（全 18 個 CH 頁）~~ | — | **2026-04-30 已批次移除全部 18 個 CH 頁**。原因：學員不願公開分享、assignment 已接管課堂節奏切點職能（30–40 分鐘正式作業比 1 分鐘 CHECKPOINT prompt 更強）|
| `case-study` 延伸案例 | 主要在 PRAC | 自學閱讀 | **借精神**：情境+任務+評分+折疊解答+變體 |
| `peer-activity` 同儕互評 | 每 Part 第一個 PRAC | 互評 | 不變 |
| PRAC 整頁互動工具 | 獨立頁 | 課堂 2–3h | 不變 |
| **`assignment` 課堂作業（新）** | CH 內嵌 / 少數獨立頁 | 課堂 20–40 分鐘 | **本設計新增** — 緊接 mini-prac 後，提供完整情境與素材，學員當堂運用該節技巧 |

**關鍵診斷**（v0.2 寫 / v0.3 校準）：

Part 3, 4 的 SOLO 與 CHECKPOINT 失效根因是「**有結構、無素材**」：
- SOLO 例：「請 LLM 針對欄位病灶診斷表追問」← 學員手上沒這份表
- CHECKPOINT 例：「把你帶來的雜亂 CSV + AI 清理後對照版貼協作板」← 學員沒帶 CSV

**v0.2 對策**：新增 assignment 提供素材，SOLO/CHECKPOINT 題目改寫寄生 assignment 素材。
**v0.3 修正**：CHECKPOINT 經評估後**直接移除**（18 個 CH 頁全砍），不採 v0.2 的「題目改寫」策略 — 因為學員不願公開分享是組件本質問題、不是文案問題。SOLO 仍維持 v0.2 的「題目改寫」策略（學員自我練習，非公開）。

---

## 2. 設計決策（已敲定）

### 2.1 位置：CH 內新增「課堂作業」區塊（標準）+ 少數升級獨立 HW 頁

- **標準作法**：每個 CH 頁在 mini-prac 之後**緊接**一塊 `assignment` 區塊。mini-prac 是 5 分鐘暖身、assignment 是 20–40 分鐘正式演練，兩者分工明確不重複。
- **升級條件**（升為獨立 `HW章-節.html`）：
  1. 素材包含 3 份以上獨立檔案
  2. 任務需多階段交付（非一次完成）
  3. 製作時間預估 > 60 分鐘
  4. 需印給學員紙本參照
- **升級候選**（試點期觀察，非預先全選）：CH5-2 完整頁面開發、CH6-3 Function Calling 整合、CH7-x 專題類

### 2.2 素材深度：B 中量 + 拆「核心 20 + 進階 20」（v0.3 新增）

每個 `assignment` 區塊包含：
- **情境敘述**（150–300 字，含公司/角色/週/緊迫感）
- **跟前面 mini-prac 的關聯**（v0.3 新增）：明白告訴學員「前面練個人應用、現在練客觀判斷」，避免學員不知道整合
- **本作業拆解**（v0.3 新增）：
  - **核心 20 min（必做）**：所有任務做基本判斷（型態 + 工具）+ 高頻任務做成本估算（其餘可寫「邊際 $0」或「N/A」）
  - **進階 20 min（可選）**：總結 + 替代方案比較 + 反思
  - 設計目的：避免學員疲勞、CHECKPOINT 移除後 assignment 仍可分階段交付
- **詳細素材**（5–10 筆樣本，依章節類型不同）：
  - 文字章節：客訴對話、會議紀錄段、Email 範本
  - 表格章節：5–10 列 CSV 樣本
  - 視覺章節：1–2 張 UI mockup（Codex `imagegen`）
  - 流程章節：步驟描述 + 既有 SOP 文件節錄
- **填法示範**（v0.3 新增）：素材區末段補「任務 1 已填好讓學員照格式做剩 7 件」+「💬 直接拿 mini-prac 寫的 prompt 來用」提示
- **任務清單**（3–5 項具體交付，非開放式）
- **評分標準**：基本 4 條 rubric + 加分 3 項（v0.3：自架前端 / POC / 人工抽查屬加分而非基本，避免本節未教就要求）
- **折疊式參考解答**（學員可選擇何時打開）
- **1–2 個變體**（給做完想再練的學員）

### 2.3 承載形式：文字內嵌（預設）+ 檔案類素材才下載

**判斷規則**（明確切點，非個案判斷）：
- 內嵌：情境敘述、Prompt 範例、規則說明、5 行內的小範例、對話片段
- **下載**（觸發條件：素材本質就是「檔案物件」）：
  - **信件**（多封 Email 串、需要 reply 操作）
  - **文件**（DOCX、合約節本、會議紀錄全文）
  - **試算表**（CSV、Excel，10 列以上資料）
  - **多檔案資料包**（一份案子跨 3 個檔以上）
  - **大圖原檔**（mockup、海報、截圖原圖）

**動線設計目的**：模擬職場「收檔 → 開 Excel/Word 處理 → 交付」流程；純文字情境（如 Prompt 公式）不強迫下載。

**HTML 用法**：
```html
<a href="../_assets/HW/CH3-1/HW3-1-customer-data.csv" download>📥 下載素材檔（CSV·12 列）</a>
```

**檔名規則**：英文 + 連字號，不用中文，避免 URL-encode 卡某些瀏覽器。例：`HW3-1-customer-data.csv`、`HW2-2-meeting-notes.docx`。

### 2.4 製作流程：C 雙引擎協作 + D' 一次一章順序完善

**雙引擎分工（C）**：
| 內容類型 | 主寫 | 交叉審 | 你的角色 |
|---------|------|--------|---------|
| 情境敘述 | Claude | Codex consult（揪商業情境不合理） | 拍板 |
| 任務清單 + 評分 | Claude | Codex consult（揪邏輯漏洞） | 拍板 |
| CSV 樣本資料 | Python script（schema 由 Codex 寫） | Claude 檢查合理性 | 抽查 |
| UI mockup 圖 | Codex `imagegen`（每節最多 1–2 張） | Claude 檢查與情境一致 | 拍板採用 |
| 解答示範 | Claude | Codex consult（揪示範是否真的好） | 拍板 |
| HTML 套版 | Claude | — | — |

**imagegen 配額管理**：每 session 上限 5 張，跨 session 累計需確認。imagegen 觸發時機限定於「需 UI mockup / 海報 / 設計稿」的章節（如 CH4-x、CH5-x），文字主導章節不用。

**一次一章順序完善（D'）**：

不採「試點 3 章評估後擴張」策略（理由：使用者拍板「追求課程完善」，不是試錯導向）。改採：

- **執行順序**：CH1-1 → CH1-2 → CH1-3 → CH1-4 → CH2-1 → ... → CH7-x（依大綱章節順序）
- **每章獨立完成**：assignment 寫完 + 素材製作 + lint 通過 + 你拍板 → 即上線
- **第一章（CH1-1）特殊性**：因為它同時驗證模板，做完後若發現結構需調整，**回頭修 CH1-1 同時鎖定模板版本**，後續章節用穩定模板
- **Part 3, 4 章節到位時**：assignment 寫完後**同步改寫**該章節 SOLO 與 CHECKPOINT 文案（每章追加 ~5 分鐘工時），不要等回頭批次改
- **不刻意停下來等驗收**：但每完成一章你要拍板才進下一章，發現系統性問題（例：模板要改、下載動線要改）就回頭整頓
- **進度追蹤**：在 `courses/gen-ai-140h/_進度/140h-進度追蹤.md` 增列「assignment 完成度」欄

---

## 3. HTML 模板規格

### 3.1 新增 CSS 組件：`assignment`

放在 `courses/gen-ai-140h/_assets/assignment-v1.css`（新檔），CH 頁透過 `<link>` 引用，不寫進個別頁的 inline CSS（避免 56 單元各自重複）。

組件結構（HTML 骨架）：
```html
<section class="assignment" data-assignment-id="CH1-2">
  <header class="assignment-head">
    <span class="assignment-eyebrow">課堂即時作業</span>
    <span class="assignment-time">⏱ 30 分鐘</span>
    <h3 class="assignment-title">{{作業標題}}</h3>
  </header>

  <div class="assignment-context">
    <p class="assignment-lede">{{情境敘述 150–300 字}}</p>
  </div>

  <div class="assignment-materials">
    <div class="materials-label">素材</div>
    <!-- 內嵌素材：文字、Prompt、客訴等 -->
    <div class="material-inline">{{內嵌文字素材}}</div>
    <!-- 外掛下載 -->
    <a class="material-download" href="../_assets/HW/CH1-2/HW1-2-pack.zip" download>
      📥 下載素材包（含 customer-feedback.csv 等 3 份）
    </a>
  </div>

  <ol class="assignment-tasks">
    <li>{{任務 1}}</li>
    <li>{{任務 2}}</li>
    <li>{{任務 3}}</li>
  </ol>

  <div class="assignment-rubric">
    <div class="rubric-label">評分標準</div>
    <ul>
      <li>{{rubric 條 1}}</li>
      <!-- 4 條 -->
    </ul>
  </div>

  <details class="assignment-answer">
    <summary>📖 展開參考解答（建議自己先試 15 分鐘再開）</summary>
    <div class="answer-body">{{解答示範}}</div>
  </details>

  <div class="assignment-variants">
    <div class="variants-label">想再練？變體版本</div>
    <ul>
      <li>{{變體 1}}</li>
      <li>{{變體 2}}</li>
    </ul>
  </div>
</section>
```

### 3.2 視覺風格

對齊現有設計系統（`_規範/design-tokens.md`）：
- 背景：`#fafaf5`（同 mini-prac、case-study 的 off-white）
- 邊框：`1px solid var(--c-border)` + 左邊 `4px solid var(--c-a1)`（用該 Part 主色）
- 圓角：`var(--radius)` = 6px
- 標題字型：Shippori Mincho 700
- 內文字型：Noto Sans TC
- 禁止漸層、禁止重 box-shadow（依 repo 規範）

### 3.3 與現有元件的視覺區隔

| 元件 | 左邊條色 | 用途 |
|------|---------|------|
| `mini-prac` | `var(--c-a2)` 芥末黃 | 5 分鐘暖身 |
| `assignment`（新） | `var(--c-a1)` Part 主色 | **課堂作業** |
| `case-study` | `var(--c-a1)` Part 主色 | 自學延伸案例 |
| `peer-activity` | `#b5703a` 陶土橘 | 同儕互評 |

---

## 4. 檔案結構

```
courses/gen-ai-140h/
├── _assets/
│   ├── assignment-v1.css       ← 新增（共用 CSS）
│   └── HW/                     ← 新增目錄
│       ├── CH1-2/
│       │   ├── HW1-2-pack.zip
│       │   └── （個別檔案也保留供單獨下載）
│       ├── CH3-1/
│       │   └── HW3-1-customer-data.csv
│       └── CH4-1/
│           ├── HW4-1-mockup.png
│           └── HW4-1-spec.md
├── part1/
│   └── CH1-2.html              ← 修改：新增 <section class="assignment">
└── part3/
    └── CH3-1.html              ← 修改
```

---

## 5. 製作 SOP（試點 3 章用）

每節作業製作流程：

1. **讀大綱**：取得該節學習目標、教學重點、預期技巧
2. **設計情境**（Claude 主寫 → Codex consult 審）
   - 真實職場角色（不要「某公司小王」這種）
   - 緊迫感（截止時間、利害關係人）
   - 與該節技巧 1:1 對應（學員不用本節技巧做不出來）
3. **產素材**
   - 文字：Claude 寫 + Codex 審「商業合理性」
   - CSV：Python script 生（Codex 寫 schema → 跑 script → 你抽查 5 列）
   - Mockup：Codex `imagegen`（先確認 prompt + 用途，再生）
4. **寫任務 + 評分**（Claude → Codex 審「邏輯漏洞」）
5. **寫解答**（Claude → Codex 審「示範品質」）
6. **打包素材**（zip + 個別檔案雙存）
7. **套 HTML 模板**（Claude 機械化）
8. **跑 lint**：`python3 docs/lint-page.py courses/gen-ai-140h/part1/CH1-2.html`
9. **你最終審改 + 拍板上架**

每節驗收清單（給你審用）：
- [ ] 情境是否真實到讀完想動手做
- [ ] 素材是否夠細到不用空想
- [ ] 任務是否能用本節技巧完成
- [ ] 評分標準是否能客觀判定
- [ ] 解答是否示範到位（不只給答案，還說「為什麼這樣寫」）
- [ ] 變體是否有梯度
- [ ] HTML lint 通過

---

## 6. 風險與緩解

| 風險 | 機率 | 緩解 |
|------|------|------|
| CH 頁變太長，閱讀流被打斷 | 中 | 解答用 `<details>` 折疊；素材若 > 20 行也折疊 |
| 試點章節做完發現結構要改 | 中 | 試點期間 CSS 命名加 `-v1` 後綴，方便日後分版 |
| Codex imagegen 配額用完 | 中 | 每 session 上限 5 張；試點 3 章預估 6 張，分 2 session |
| 中文檔名 URL-encode 卡住 | 低 | 強制英文檔名規則 |
| 學員下載 zip 不會解壓 | 低 | 個別檔案也直接提供下載（雙存）|
| 素材製作工時超出預估 | 中 | D 試點先行，跑完 3 章用實測數據再決定擴張 |

---

## 7. 驗收標準（每章完成即驗收）

每章 assignment 完成時你逐項拍板：
- [ ] 情境是否真實到讀完想動手做（職場感、緊迫感）
- [ ] 素材是否夠細到不用空想（無「想像力填空」）
- [ ] 任務是否能用本節技巧完成（1:1 對應該節學習目標）
- [ ] 評分標準是否能客觀判定（4 條 rubric 不模糊）
- [ ] 解答是否示範到位（不只給答案，還說「為什麼這樣寫」）
- [ ] 變體是否有梯度（不是同題改字）
- [ ] 檔案類素材是否真的需要下載（小素材就內嵌）
- [ ] 中文檔名不存在（`_assets/HW/CHX-Y/` 全英文）
- [ ] HTML lint 通過：`python3 docs/lint-page.py courses/gen-ai-140h/partN/CHX-Y.html`
- [ ] 進度追蹤同步更新

**Part 3, 4 章節額外檢查**（v0.3 修正）：
- [ ] SOLO 題目已改寫成「用 assignment 素材做變體 X」
- [ ] ~~CHECKPOINT 交付物已改成「assignment 完成版」~~ → **CHECKPOINT 已全砍，無此檢查項**

---

## 7.5 待真實課堂驗證項目（v0.3 新增）

CH1-1 完成後，以下項目須等實際開課後驗證：

- [ ] **assignment 銜接 mini-prac 的 transfer**：學員是否會把 mini-prac 1/2/3 寫過的 prompt 直接拿來用，還是仍從零開始？驗證 CH1-1 已加的「💬 提示」段是否夠明確。
- [ ] **核心 20 + 進階 20 拆分合理性**：學員多少人做完核心、多少人做到進階？比例是否合理？
- [ ] **assignment 30–40 分鐘工時實測**：估算 vs 實際。如果學員普遍 50 分鐘以上才完成，要重新校準顆粒。
- [ ] **CHECKPOINT 移除後的影響**：講師是否還需要某種「課堂節奏切點」？assignment 完成後是否需要簡短共識／講評儀式（不必回到 CHECKPOINT，但可在 lesson-template 加 next-step 提示）？
- [ ] **「松果科技 Lina」敘事宇宙的續用範圍**：CH1-1/1-2/1-3 都用同一情境（內容運營專員 + Lina），CH1-3 還與 CH1-2 P3 形成跨章敘事連續。**Codex 第二輪建議**：CH1-4（System Prompt）可延續 Lina；**CH2-1 起建議淡化**改成一般職場任務，避免角色疲乏。待 CH1-4 完成後評估，必要時校準 design 為 v0.4。

驗證後依結果回校準 design doc → v0.4。

每完成 5 章（一個 Part 完成）回頭整體檢視：
- 是否有共通模板問題（CSS 命名、區塊順序、元件樣式）
- 製作工時實測值 vs 規格估算（1.5–2.5h）
- 你的審改負擔是否可持續（若 > 30% 你的時間在審改，就重新校準 Claude 主寫品質）

---

## 8. 不在本設計範圍

明確劃出的非目標（避免 scope creep）：
- 不改 PRAC 互動工具頁（PRAC 是工具，不是作業）
- 不改 mini-prac（保留作為暖身）
- 不做學員作業繳交系統（無後端）
- 不做自動評分（rubric 是給人讀的，不是給機器跑的）
- 不做 Part 6/7（這兩 Part 整體還在規劃中）
- ~~不動 CHECKPOINT~~ → v0.3 已批次移除 CHECKPOINT，不再保留

---

## 9. 後續步驟

本 design 通過後：
1. 進 writing-plans skill 寫 **CH1-1 第一章作業實作計畫**（單章粒度）
2. 同步建立通用基礎建設：
   - `_assets/assignment-v1.css` 共用樣式檔
   - `_assets/HW/` 目錄結構
   - `_進度/140h-進度追蹤.md` 增列 assignment 欄
3. 製作 CH1-1（同時鎖定模板版本）
4. 你拍板上架 → 進 CH1-2 → 依序至 CH7-x
5. 每完成一個 Part 回頭整體檢視一次
