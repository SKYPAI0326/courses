# gen-image 課程「講義型 → 互動工作坊型」重構諮詢報告

**作者**：course-designer / 對話日期 2026-04-26
**任務來源**：使用者要求把 `courses/gen-image/` 從「講義型」轉成「互動工作坊型」
**核心原則**：一個觀念一次演練、5–8 分鐘一個小產出、檢核分散到每個觀念後面、PM 定位不變
**本檔角色**：諮詢報告（不直接改 HTML）。本檔核可後再分課施工。

---

## 0. 現況體檢（先看數據再談重構）

| 指標 | 現況 | 解讀 |
|------|------|------|
| 總頁數 | 13 個（10 CH + 3 PRAC + index + 5 module + assets） | 體量適中 |
| 最重的單元 | CH5-1 = 1251 行 / 39 callout / 10 step | **最該手術**（資訊過載） |
| 第二重 | CH2-2 = 1161 行 / 15 callout + 14 step / 0 inline 練習 | **demo 對象** |
| PRAC 平均 | ~548 行，已有 4-step 流程 + 4 項驗收 + 卡住備援 | **接近任務卡，缺 learner-output** |
| 已有元件 | callout / step-block / quiz-item / tool-grid / scenario-grid / brief-card / error-block / exercise-block | **基礎扎實** |
| 缺的元件 | micro-cycle / task-card / learner-output / self-check / instructor-note | **要加，但需走 lint 流程** |
| PM 定位 | 「需求判定者 / 骨架驗收者 / 系列把關者」已內化於 PRAC2 文案 | **不能滑成設計課** |

**一句話結論**：PRAC 已是樣板（小修即可），**CH 才是病灶**。重構主戰場在 SECTION 02「學」——把「逐欄列出」改成「逐欄演練」。

---

## §1 整體重構策略（7 點）

### 策略 1：把「看 / 學 / 做」三段大格局，改成「看–學–做」迴圈 ×N
**現況**：SECTION 01 看（10 min）→ SECTION 02 學（20 min）→ SECTION 03 做（15 min）。學員前 30 分鐘是被動接收，最後 15 分鐘才動手。
**重構**：把「看–學–做」壓縮成 5–8 分鐘的 micro-cycle，一個觀念跑一輪。一頁有 3–5 個 micro-cycle，學員每個迴圈都有產出。
**結構轉換**：
- 舊：`SECTION 01 看 (10 min)` + `SECTION 02 學 (20 min)` + `SECTION 03 做 (15 min)`
- 新：`SECTION 01 暖身 (3 min)` + `Cycle 1 (8 min)` + `Cycle 2 (8 min)` + `Cycle 3 (8 min)` + `SECTION 02 整合任務 (15 min)` + `SECTION 03 收束 (3 min)`

### 策略 2：每頁開頭從「learning_objective 全文」改成「今天會交出什麼」
**現況**：lesson-tagline 是長句說明（「能用 brief 六件套把任意廣告需求改寫成可丟 AI 的 prompt …」）。學員讀不出「我等下要產出什麼」。
**重構**：在 hero 下方、SECTION 01 之前，加一個 `today-deliverables` 區塊，3 條以內：
- 1 份填好的 brief 六件套
- 1 個版型選擇 + 理由
- 1 段可複製 prompt
完成這 3 件就算過關。其他延伸內容是 bonus。

### 策略 3：把 SECTION 02「學」拆成「逐欄 micro-cycle」，禁止整段平鋪
**現況**：CH2-2 SECTION 02 用 6 個 `part-divider` 列出六件套——欄位 1-6 一氣呵成，沒有任何學員動作。
**重構**：每欄都是一個 micro-cycle：給壞例子 → 講判準 → 學員填一格自己的內容 → 對照判準打勾 → 老師收斂句。每 5 分鐘一輪。
**操作**：把現有 `tool-grid` 的「填什麼/為什麼/判準/常見錯誤」4 件物，重新分配到 cycle 的 4 步：
- 觀念 = 為什麼這欄重要（30 秒講）
- 錯誤例子 = ✕ 列表（10 秒看）
- 小任務 = 填你的這欄（2 分鐘做）
- 檢核 = 對照判準（30 秒打勾）

### 策略 4：檢核分散到每個 cycle 後面，頁尾 quiz 降級為「整合題」
**現況**：每頁底有 `.quiz-item × 2`（Q1 觀念複述、Q2 應用題）。學員過完 30 分鐘才碰到第一題。
**重構**：每個 micro-cycle 結尾掛 1 條 `.self-check`（單句判斷題或單欄填空），共 3–5 條。頁尾 quiz 保留 1 題就好，作為「整合判斷」（綜合多個 cycle）。
**self-check vs quiz-item 區別**：
- `.self-check` 是**段內動作**：學員當下就要回答、不展開答案、答對才往下滑
- `.quiz-item` 是**頁尾總考**：含詳解、可展開、用於課後複習

### 策略 5：把 brief 大表拆解三次後，才允許出現整大表
**現況**：CH2-2「階段 1 填 brief」直接給 6 欄空表（line 609-619），學員一次面對 6 欄空白。
**重構**：先在 cycle 1-3 各填一欄（業種 / 商品 / 客群），cycle 4 講「訴求 vs 必要元素」差異判斷，cycle 5 講「風格 preset 速查」。學員到「整合任務」時才看到完整六欄表，但**前面已經分別填過**——只是把碎片貼回來。
**這條對應使用者原則**：「不要讓學員一次填完整大表，除非前面已經逐步拆解」。

### 策略 6：講師備註全部包進 `.instructor-note` 折疊區，學員主流程禁見「為什麼這樣設計」
**現況**：CH2-2 line 161-164 `.intro-band` 寫「brief 六件套不是套路作業，是 PM 的工作語言。缺一欄，AI 就自己猜一欄」——這是給講師的設計理由，但學員主流程看到。CH5-1 39 個 callout 中估計有 1/3 是這類。
**重構**：學員主流程只留「現在要做什麼 + 為什麼這個動作必要」。**設計理由、教學意圖、預期差異、AI 特性說明**全部移到 `<details class="instructor-note">` 折疊區，預設關閉，講師翻開講解時才展開。

### 策略 7：PRAC 不大改，只補 `learner-output` + 強化「卡住怎麼辦」
**現況**：PRAC2/3/4 已是任務卡型（限時 / 完成物 / 通過標準齊全），PM 思維文案到位。
**唯二差距**：
1. 沒有 `.learner-output` 區塊讓學員「就地交件」（目前要學員自己拿紙筆寫，產出散落）
2. 「卡住怎麼辦」散在常見錯誤段，不是任務卡內建欄位
**重構**：
- 每個任務卡末尾加 `.learner-output`（一個淡色框 + 「請在此寫下你的成果：」+ 留白 60-100px 高）
- 任務卡新增「Stuck?」摺疊區，3 條 if-else 備援（「如果 X → 試 Y」「如果還卡 → 跳下一張」）

---

## §2 單元頁面模板（V4 互動工作坊版）

> 沿用既有 `_規範/lesson-template-v3.html` 的視覺骨幹（topbar / page-hero / lesson-section / nav-footer），只在 SECTION 結構與內部組件做改動。

### 模板骨架

```
┌─ topbar
├─ page-hero
│  ├─ back-link
│  ├─ hero-eyebrow ((NN) · CH N.M)
│  ├─ lesson-title
│  ├─ lesson-tagline (≤ 1 行，把目標壓成 1 句話)
│  ├─ outcomes (3 條，動詞開頭：能…、能…、能…)
│  └─ today-deliverables ★新增  「今天會交出什麼」3 條
│
├─ SECTION 01 · 暖身 (3 min)
│  ├─ section-eyebrow / section-heading
│  └─ context (問題現場 + 為什麼今天要學這個)
│
├─ SECTION 02 · CYCLE 1 (8 min) ★用 .micro-cycle 包
│  ├─ cycle-eyebrow (循環 1 of 3 · 觀念名)
│  ├─ cycle-question (一句設問)
│  ├─ wrong-example (錯誤例子 1 個)
│  ├─ task-card (小任務：限時 / 要做什麼 / 完成物)
│  ├─ learner-output (學員填空區)
│  ├─ self-check (段內檢核 1 條)
│  └─ closer (老師收斂 1 句)
│
├─ SECTION 03 · CYCLE 2 (8 min) ★同上結構
├─ SECTION 04 · CYCLE 3 (8 min) ★同上結構
│
├─ SECTION 05 · 整合任務 (15 min)
│  ├─ task-card (大任務 = 把 3 個 cycle 的產出組合)
│  ├─ learner-output (整合產出區)
│  └─ verify (4 項驗收清單)
│
├─ SECTION 06 · 收束 (3 min)
│  ├─ quiz-item (1 題綜合判斷)
│  └─ next-step (下一單元銜接 1 句)
│
└─ details.instructor-note (講師備註，整頁折疊，置於頁尾)
   ├─ 教學意圖
   ├─ 常見卡關點 + 解法
   ├─ 試跑包需求
   └─ 工具書 / 延伸資料連結
```

### 與舊模板的差異對照

| 區段 | 舊（CH2-2） | 新（互動工作坊） |
|------|------------|----------------|
| Hero | learning_objective 全文 | + today-deliverables 3 條 |
| SECTION 01 | 「看」段 10 min（含 8 min 操作） | 暖身 3 min（純破題、不操作） |
| SECTION 02-04 | 「學」段 20 min（六件套一次列） | 3 個 micro-cycle，各 8 min |
| SECTION 05 | 「做」段 15 min（單一大任務） | 整合任務 15 min（組合前 3 cycle 產出） |
| 試跑包 / 案例 / 練習 / 常見錯誤 | 4 個獨立 SECTION（共 ~400 行） | 全部移入 `.instructor-note` 折疊區 |
| 檢核 | quiz-item × 2 在頁尾 | self-check × 3-5 在每 cycle，頁尾留 1 題 |

### 新區塊：today-deliverables（hero 內）

```html
<!-- 放在 .outcomes 下方、page-hero 結尾前 -->
<div class="today-deliverables">
  <div class="today-deliverables-label">今天結束時，你會交出</div>
  <ol class="today-deliverables-list">
    <li>1 份填好的 brief 六件套（業種 + 商品 + 客群 + 訴求 + 必要元素 + 風格 preset）</li>
    <li>1 個版型選擇 + 一句理由（A-H 任一）</li>
    <li>1 張 1:1 完稿（4 項驗收 ≥ 3 項通過）</li>
  </ol>
  <p class="today-deliverables-note">完成這 3 件就算過關。其他段落是延伸 / 工具書，可帶回家慢慢看。</p>
</div>
```

**CSS hook**（提案，需後續加進 design-tokens v4）：
```css
.today-deliverables{margin-top:32px;padding:20px 24px;border:1px dashed var(--c-border);border-radius:var(--radius);background:var(--c-bg)}
.today-deliverables-label{font-family:'Shippori Mincho',serif;font-size:.85rem;color:var(--c-text);letter-spacing:.08em;font-weight:700;margin-bottom:12px}
.today-deliverables-list{list-style:decimal;padding-left:20px;display:flex;flex-direction:column;gap:8px;font-size:.92rem;color:var(--c-text);line-height:1.8}
.today-deliverables-note{font-size:.82rem;color:var(--c-muted);margin-top:12px;font-style:italic}
```

---

## §3 互動循環模板（micro-cycle）

### 概念定義

**micro-cycle = 5–8 分鐘的「觀念→任務→檢核」最小完整單元**。一個 CH 單元裡放 3–5 個。
**核心承諾**：學員每個 cycle 結束時手上都有「一個可貼到下一個 cycle 的小產出」（一句話、一格表、一個選擇、一段 prompt 片段）。

### 循環骨架（8 步、可裁減）

```
┌──── micro-cycle 8 步 ────────────────┐
│ 1. 觀念名稱（cycle-question）        │ ← 1 句、設問形式（「為什麼 AI 會猜配色？」）
│ 2. 錯誤例子（wrong-example）         │ ← 1 個 ✕、現場可見、不抽象
│ 3. 觀念說明（concept）               │ ← 30 秒講完、1-2 句、有 「因為…所以…」邏輯
│ 4. 小任務（task-card）               │ ← 限時 + 要做什麼 + 完成物 + 通過標準
│ 5. 學員產出區（learner-output）      │ ← 留白 + 提示，學員就地填寫
│ 6. 段內檢核（self-check）            │ ← 1 條、是非題或 1 欄判斷
│ 7. 老師收斂句（closer）              │ ← 1 句、把這個 cycle 的精華濃縮成一句金句
│ 8. 銜接到下一個 cycle（連接句）       │ ← 1 行、預告下一 cycle 在解什麼問題
└──────────────────────────────────────┘
```

> **可裁減原則**：步驟 1、3、4、5、6、7 是必要 6 步。步驟 2「錯誤例子」與步驟 8「銜接」可省。整個 cycle 控制在 100-180 行 HTML（含內容）。

### HTML 樣本（提案、含 .micro-cycle 新 class）

```html
<section class="lesson-section micro-cycle">
  <div class="cycle-eyebrow">循環 1 of 3 · 業種</div>
  <h2 class="section-heading">業種沒講對，AI 整套配色都偏掉</h2>

  <!-- 1. 設問 -->
  <p class="cycle-question">「服務業」「消費品」算不算業種？</p>

  <!-- 2. 錯誤例子 -->
  <div class="wrong-example">
    <span class="wrong-label">看一個壞例子</span>
    <code>幫我做一張服務業的 1:1 廣告</code>
    <p class="wrong-note">→ AI 拿到「服務業」3 個字，腦中喚起的視覺詞彙太廣（餐飲？美容？銀行？保險？），配色和字體只能瞎猜。</p>
  </div>

  <!-- 3. 觀念 -->
  <p class="body-text">業種要對應到 <strong>10 業種庫</strong>（餐飲 / 美妝 / App / 旅遊 / 教育 / 活動 / 醫美 / 寵物 / 居家 / 健身）之一，至少要能讓第三人理解「你在賣什麼類別」。AI 才能把對的視覺詞彙庫拉到桌面。</p>

  <!-- 4. 小任務 -->
  <div class="task-card">
    <div class="task-card-header">
      <span class="task-card-label">小任務</span>
      <span class="task-card-time">限時 90 秒</span>
    </div>
    <div class="task-card-body">
      <p><strong>要做什麼</strong>：寫下你今天要練習的業種（如果你是接案者，就寫你最常接的；如果是品牌方，就寫自家業種）</p>
      <p><strong>完成物</strong>：1 行文字，5-12 字</p>
      <p><strong>通過標準</strong>：能對應到 10 業種之一，或第三人能理解</p>
    </div>
  </div>

  <!-- 5. 學員產出區 -->
  <div class="learner-output">
    <div class="learner-output-label">在此寫下你的業種</div>
    <div class="learner-output-blank" contenteditable="true" data-placeholder="例：手沖咖啡店"></div>
  </div>

  <!-- 6. 段內檢核 -->
  <div class="self-check">
    <span class="self-check-label">段內檢核</span>
    <p>你寫的這個業種，能不能讓你身邊不懂行的朋友 5 秒內想像出大致畫面？</p>
    <p class="self-check-rule">能 → 進下一 cycle ｜ 不能 → 把它具體化（如「咖啡店」改「手沖咖啡店」「連鎖咖啡店」）</p>
  </div>

  <!-- 7. 老師收斂句 -->
  <blockquote class="closer">
    業種不是分類學，是給 AI 的視覺詞彙索引。寫得越具體，AI 撈出的詞彙越精準。
  </blockquote>

  <!-- 8. 銜接 -->
  <p class="cycle-bridge">→ 下一個循環：你選的這個業種要賣什麼商品？</p>
</section>
```

### CSS hook（提案）

```css
.micro-cycle{position:relative;border-left:2px solid var(--c-border-soft);padding-left:24px;margin:32px 0}
.micro-cycle .cycle-eyebrow{font-family:'Shippori Mincho',serif;font-size:.82rem;color:var(--c-faint);letter-spacing:.1em;font-weight:500;margin-bottom:10px}
.micro-cycle .cycle-question{font-family:'Shippori Mincho',serif;font-size:1.1rem;font-weight:500;color:var(--c-text);margin:8px 0 18px;font-style:italic}
.wrong-example{background:var(--c-surface);border-radius:var(--radius);padding:14px 18px;margin:16px 0;border-left:2px solid var(--c-faint)}
.wrong-example .wrong-label{font-size:.72rem;letter-spacing:.12em;color:var(--c-muted);font-weight:500;display:block;margin-bottom:8px}
.wrong-example code{display:block;background:#2c2b28;color:#e8e4dc;padding:10px 14px;border-radius:var(--radius-sm);font-size:.85rem;margin-bottom:8px}
.wrong-example .wrong-note{font-size:.85rem;color:var(--c-muted);line-height:1.7;margin:0}
.task-card{border:1px solid var(--c-border);border-radius:var(--radius);overflow:hidden;margin:16px 0}
.task-card-header{background:var(--c-text);color:#fff;padding:10px 18px;display:flex;justify-content:space-between;align-items:center}
.task-card-label{font-family:'Shippori Mincho',serif;font-size:.85rem;font-weight:700;letter-spacing:.06em}
.task-card-time{font-size:.72rem;letter-spacing:.08em;font-variant-numeric:tabular-nums;opacity:.85}
.task-card-body{padding:16px 20px;display:flex;flex-direction:column;gap:8px;font-size:.88rem;line-height:1.8}
.learner-output{background:var(--c-bg);border:1px dashed var(--c-border);border-radius:var(--radius);padding:14px 18px;margin:16px 0}
.learner-output-label{font-size:.72rem;letter-spacing:.12em;color:var(--c-text);font-weight:500;margin-bottom:8px}
.learner-output-blank{min-height:48px;padding:10px 12px;background:var(--c-card);border:1px solid var(--c-border-soft);border-radius:var(--radius-sm);font-size:.92rem;color:var(--c-text);line-height:1.7}
.learner-output-blank:empty::before{content:attr(data-placeholder);color:var(--c-faint);font-style:italic}
.self-check{background:var(--c-surface);border-radius:var(--radius);padding:14px 18px;margin:16px 0;border-left:2px solid var(--c-text)}
.self-check-label{font-size:.72rem;letter-spacing:.12em;color:var(--c-text);font-weight:500;display:block;margin-bottom:8px}
.self-check p{font-size:.88rem;color:var(--c-text);line-height:1.7;margin:0 0 6px}
.self-check-rule{font-size:.82rem;color:var(--c-muted);line-height:1.7;margin-top:8px!important}
.closer{margin:18px 0;padding:16px 20px;font-family:'Shippori Mincho',serif;font-size:1.05rem;font-weight:500;color:var(--c-text);line-height:1.7;background:transparent;border-left:3px solid var(--c-text);font-style:normal}
.cycle-bridge{font-size:.85rem;color:var(--c-muted);margin-top:12px;font-style:italic}
```

### 撰寫紀律（給未來施工者）

| 紀律 | 為什麼 |
|------|-------|
| 一個 cycle 只解 **1 個**觀念 | 違反就違反「一個觀念一次演練」 |
| `cycle-question` 必須是設問句（「為什麼…？」「…算不算…？」「…和…差在哪？」）| 設問才能拉學員注意力 |
| `wrong-example` 必須具體可見（給壞 prompt、給壞圖、給壞 brief 文字），**不可抽象**（「不夠精準」「太籠統」）| 抽象的錯例 = 沒講錯例 |
| `task-card` 限時必須在 1–4 分鐘內 | 超過 5 分鐘就不是 micro 任務 |
| `learner-output` **必須有提示佔位文字** | 沒提示學員不知道格式 |
| `self-check` 限 1 條、回答時間 30 秒內 | 超過就退化成 quiz |
| `closer` 必須是金句、可被學員口述複述 | 收斂句就是要讓學員「能帶走」 |

---

## §4 PRAC 任務卡模板（task-card 標準格式）

### 與現有 PRAC2 的關係

PRAC2 已有 `exercise-block`（內含 phase-label / phase-title），結構良好但**少 4 件事**：
1. 沒有可視覺化的「限時計時器」設計（時間在文字裡，學員容易忽視）
2. 沒有「卡住怎麼辦」內建欄位（散在常見錯誤段）
3. 沒有 `.learner-output` 就地交件區（學員拿紙筆寫，產出散落）
4. 沒有「通過 / 不通過」的 explicit decision 行（PRAC2 用 `.result-decision` 但只在 step 4 一次性出現）

新模板把這 4 件補進來，**升級 `exercise-block` → `task-card`**，並讓 task-card 同時可用於 CH 的 micro-cycle 內 + PRAC 的整段演練。差別只在尺寸和資料量。

### 任務卡 6 欄位（標準格式）

```
┌─ 任務名稱（task-name）         ← 動詞開頭、5-12 字
│
├─ 限時（time-budget）            ← 數字 + 單位、tabular-nums 對齊
│
├─ 要做什麼（what-to-do）         ← 3-5 行、條列、動詞開頭
│
├─ 完成物（deliverable）          ← 1-2 行、可拍照可貼可複製
│
├─ 通過標準（pass-criteria）      ← 4 項打勾清單、明確不主觀
│
└─ 卡住怎麼辦（stuck-fallback）   ← <details> 折疊、3 條 if-else
```

### HTML 樣本

```html
<div class="task-card task-card-large">
  <!-- Header -->
  <div class="task-card-header">
    <div class="task-card-name">任務 1｜挑業種 + 商品 + 客群</div>
    <div class="task-card-time">限時 4 min</div>
  </div>

  <!-- Body -->
  <div class="task-card-body">
    <!-- 要做什麼 -->
    <div class="task-card-section">
      <div class="task-card-label">要做什麼</div>
      <ul class="task-card-list">
        <li>從 <code>10-industries-brief-library.md</code> 挑 1 個你最常接案的業種</li>
        <li>填上具體商品名（如「春季限定 抹茶提拉米蘇拿鐵」）</li>
        <li>寫 2-3 項客群描述（年齡 + 性別 + 生活風格）</li>
      </ul>
    </div>

    <!-- 完成物 -->
    <div class="task-card-section">
      <div class="task-card-label">完成物</div>
      <p>brief 卡片前 3 欄填好、可拍照可截圖</p>
    </div>

    <!-- 通過標準 -->
    <div class="task-card-section">
      <div class="task-card-label">通過標準（4/4 打勾）</div>
      <ul class="check-list">
        <li>業種能對應到 10 業種庫之一</li>
        <li>商品有具體名稱 + 規格 / 容量 / 價格</li>
        <li>客群至少 2 項描述</li>
        <li>第三人 5 秒內能想像「你要賣什麼給誰」</li>
      </ul>
    </div>
  </div>

  <!-- Stuck fallback -->
  <details class="task-card-stuck">
    <summary>卡住怎麼辦？</summary>
    <ul>
      <li><strong>選不出業種</strong> → 直接用「咖啡店」當練習素材，課後回來換自己的</li>
      <li><strong>商品想不到具體名稱</strong> → 抄 PRAC2 範例（春季限定 抹茶提拉米蘇拿鐵 ¥680），改成你的價格</li>
      <li><strong>客群只想得到「一般大眾」</strong> → 想一個你最常服務的客戶、把他寫下來</li>
      <li><strong>還卡 → 直接跳下一個 cycle</strong>，這欄回家補</li>
    </ul>
  </details>
</div>

<!-- 學員產出區 -->
<div class="learner-output">
  <div class="learner-output-label">在此寫下你的 brief 前 3 欄</div>
  <table class="learner-output-table">
    <tbody>
      <tr><th>業種</th><td contenteditable="true" data-placeholder="例：手沖咖啡店"></td></tr>
      <tr><th>商品</th><td contenteditable="true" data-placeholder="例：春季限定 抹茶提拉米蘇拿鐵 ¥680"></td></tr>
      <tr><th>客群</th><td contenteditable="true" data-placeholder="例：25-35 歲女性、注重生活風格"></td></tr>
    </tbody>
  </table>
</div>
```

### CSS hook 補充（接續 §3）

```css
.task-card-large{margin:24px 0}
.task-card-large .task-card-body{padding:20px 24px;display:flex;flex-direction:column;gap:18px}
.task-card-section .task-card-label{font-size:.72rem;letter-spacing:.12em;color:var(--c-text);font-weight:500;margin-bottom:6px}
.task-card-section p,.task-card-section ul{font-size:.88rem;color:var(--c-text);line-height:1.8}
.task-card-list{padding-left:20px;display:flex;flex-direction:column;gap:4px}
.task-card-stuck{border-top:1px solid var(--c-border-soft);padding:12px 24px;background:var(--c-bg)}
.task-card-stuck summary{cursor:pointer;font-size:.85rem;color:var(--c-muted);font-weight:500;padding:4px 0;list-style:none}
.task-card-stuck summary::before{content:"▸ ";color:var(--c-faint)}
.task-card-stuck[open] summary::before{content:"▾ "}
.task-card-stuck ul{padding:8px 0 4px 20px;display:flex;flex-direction:column;gap:6px;font-size:.85rem;color:var(--c-text);line-height:1.7}
.learner-output-table{width:100%;border-collapse:collapse;margin:8px 0}
.learner-output-table th{width:90px;text-align:left;font-family:'Shippori Mincho',serif;font-weight:500;font-size:.85rem;color:var(--c-muted);padding:8px 12px;background:transparent;border:none}
.learner-output-table td{padding:8px 12px;background:var(--c-card);border:1px solid var(--c-border-soft);border-radius:var(--radius-sm);font-size:.92rem;line-height:1.7;min-height:40px}
.learner-output-table td:empty::before{content:attr(data-placeholder);color:var(--c-faint);font-style:italic}
```

### task-card 在 CH 單元 vs PRAC 的尺寸差別

| 用途 | class 變體 | 限時 | 完成物量 | 通過標準項數 |
|------|----------|------|---------|------------|
| CH micro-cycle 內 | `.task-card`（基本） | 1–3 min | 1 行字 / 1 個選擇 | 1–2 條 |
| PRAC 整段任務 | `.task-card.task-card-large` | 5–20 min | 1-3 個物件 | 3-5 條 |
| PRAC 整頁總任務 | `.task-card.task-card-master` | 30 min | 3-5 個物件清單 | 4-6 條 |

---

## §5 CH2-2 demo 重構（前 3 個 micro-cycle）

> **範圍紀律**：本節只示範前 3 個 cycle。原 CH2-2 共 8 個 SECTION，重構後預估總共 5 個 cycle（覆蓋六件套全部 + 對比實驗 + 整合任務）。完整 5 cycle 版本待本報告核可後另案產出。

### Demo 對照總表

| 重構後 | 對應原 CH2-2 段落 | 行數縮減 |
|-------|----------------|---------|
| Hero + today-deliverables | line 142-153（Hero）+ 新增 today-deliverables | +12 行 |
| SECTION 01 暖身 | line 155-267（看段全部，含 90 秒情境 + 對比實驗 + 範例圖）| -90 行（範例圖移到 cycle 1）|
| **Cycle 1**：對比實驗（觀念：AI 不是設計師、你是需求方）| line 167-237（90 秒情境 + 對比實驗 3 步 + 範例圖）| -30 行 |
| **Cycle 2**：填業種 + 商品 + 客群（觀念：缺一欄就猜一欄）| line 285-347（欄位 1 / 2 / 3）| -50 行 |
| **Cycle 3**：訴求 vs 必要元素（觀念：訴求是溫度、必要元素是骨架）| line 349-447（欄位 4 / 5 + 8 版型表 + 速查表）| -120 行（8 版型表移到 details）|
| 試跑包 / 案例 / 練習題 / 常見錯誤 / 檢核題 | line 700-1120（5 個 SECTION）| **全部移入 instructor-note 折疊區** |

**預估**：CH2-2 重構後從 1161 行降到 ~700 行，學員主流程約 400 行。

---

### Cycle 1：AI 不是設計師、你是需求方

**觀念**：模糊指令時，AI 會在每個你沒講的地方自己做設計決定。
**對應原段落**：CH2-2 SECTION 01「現場對比實驗 8 min」+ 開場 90 秒情境。
**重構策略**：把「3 步驟」變成「2 步對比 + 1 個學員產出」，把範例圖留在後段給學員對照。

```html
<section class="lesson-section micro-cycle">
  <div class="cycle-eyebrow">循環 1 of 3 · 觀念</div>
  <h2 class="section-heading">AI 不是設計師、你是需求方</h2>

  <!-- 1. 設問 -->
  <p class="cycle-question">同樣丟「幫我做廣告」給 AI，為什麼每次跑出來都不一樣？</p>

  <!-- 2. 錯誤例子 -->
  <div class="wrong-example">
    <span class="wrong-label">看一個壞例子</span>
    <code>幫我做一張好看的咖啡店廣告，1:1 尺寸</code>
    <p class="wrong-note">→ AI 沒拿到：要哪種咖啡店？什麼商品？給誰看？什麼風格？什麼版型？什麼配色？這 6 個你沒講，AI 全部自己決定。每次決定不一樣，所以每張都不一樣。</p>
  </div>

  <!-- 3. 觀念 -->
  <p class="body-text">這不是 AI 不夠聰明的問題——是 <strong>你還沒做需求方該做的事</strong>。需求方的工作是把腦中模糊想法**結構化成清單**，AI 才能穩定產出。</p>

  <!-- 4. 小任務 -->
  <div class="task-card">
    <div class="task-card-header">
      <span class="task-card-label">小任務｜現場對比實驗</span>
      <span class="task-card-time">限時 5 min</span>
    </div>
    <div class="task-card-body">
      <p><strong>要做什麼</strong>：</p>
      <ol style="padding-left:20px;line-height:1.9;font-size:.88rem">
        <li>打開 Gemini 或 ChatGPT，丟上面那個壞例子，等 30 秒</li>
        <li>同對話再丟下方的「結構化版」，等 30 秒</li>
        <li>把兩張截圖並排（手機分割 / 印出）</li>
      </ol>

      <details style="margin-top:12px">
        <summary style="cursor:pointer;font-size:.85rem;color:var(--c-muted);font-weight:500">展開結構化版 prompt（複製即用）</summary>
        <pre class="code-block" style="margin-top:10px;font-size:.78rem">請產出 1:1 商業橫幅、用「A 主視覺版」風格：
【業種】手沖咖啡店
【商品】春季限定 抹茶提拉米蘇拿鐵 ¥680
【客群】25-35 歲女性、注重生活風格
【訴求】手作、季節感、療癒
【必要元素】中央杯子 / 左上季節 tag / 主標 2 行 / 左下價格
【風格 preset】鼠尾草綠 + 奶油白；明朝體粗體；手作感

⚠️ 字體名稱（Shippori Mincho 等）僅為渲染指令、不要寫進圖中</pre>
      </details>

      <p style="margin-top:8px"><strong>完成物</strong>：兩張並排截圖（不存檔也行，看完就好）</p>
    </div>
  </div>

  <!-- 5. 學員產出 -->
  <div class="learner-output">
    <div class="learner-output-label">寫下你的觀察（30 秒）</div>
    <div class="learner-output-blank" contenteditable="true"
         data-placeholder="例：模糊版的咖啡杯顏色每次都不同 / 結構化版至少配色一致"></div>
  </div>

  <!-- 6. 段內檢核 -->
  <div class="self-check">
    <span class="self-check-label">段內檢核</span>
    <p>你看到的差異中，至少有 <strong>1 個</strong>是「結構化版有講、模糊版你沒講、所以 AI 在猜」的嗎？</p>
    <p class="self-check-rule">有 → 進 cycle 2 ｜ 沒有 → 重看你的兩張，找出 AI 在哪裡自由發揮</p>
  </div>

  <!-- 7. 老師收斂句 -->
  <blockquote class="closer">
    你不講的，AI 一定自己決定。決定品質取決於它的訓練資料、不是你的需求。
  </blockquote>

  <!-- 8. 銜接 -->
  <p class="cycle-bridge">→ 下一循環：那要講哪些？最重要的前 3 件事——業種、商品、客群。</p>
</section>
```

**降級到 instructor-note**（原 CH2-2 line 161-164、234-236、257-266）：
- 「brief 六件套不是套路作業，是 PM 的工作語言」（教學意圖）
- 「預期差異：模糊指令版每人都會不同…」（AI 特性說明）
- 「本段結論：brief 不是模板作業…」（4 點收斂，過於詳盡）

**圖片處理**（原 line 244-256）：兩張對照範例圖（v09-brief-vague.png / v10-brief-structured.png）移到 cycle 1 任務後的「參考圖」`<details>` 區，學員自己跑完才能看（避免被牽著鼻子）。

---

### Cycle 2：缺一欄就猜一欄（業種 + 商品 + 客群）

**觀念**：六件套的前 3 欄定義「你要賣什麼給誰」——缺任一欄，AI 立刻在那欄自由發揮。
**對應原段落**：CH2-2 SECTION 02 欄位 1（line 285-303）+ 欄位 2（306-325）+ 欄位 3（327-347）。
**重構策略**：3 欄合成 1 個 cycle，因為性質相近（都是「需求事實」陳述）。學員在 task-card 裡一次填 3 欄，self-check 有 3 條對應 3 欄。

```html
<section class="lesson-section micro-cycle">
  <div class="cycle-eyebrow">循環 2 of 3 · 需求事實</div>
  <h2 class="section-heading">先講「賣什麼給誰」——前 3 欄定錨整張圖</h2>

  <!-- 1. 設問 -->
  <p class="cycle-question">業種、商品、客群——這 3 欄漏掉任一個，畫面會壞在哪裡？</p>

  <!-- 2. 錯誤例子（一次給 3 個壞例子） -->
  <div class="wrong-example">
    <span class="wrong-label">看 3 個壞例子</span>
    <ul style="padding-left:20px;font-size:.85rem;line-height:1.85;color:var(--c-text)">
      <li><code>業種：服務業</code> → 太抽象，AI 不知該用咖啡感、銀行感、還是醫美感</li>
      <li><code>商品：我的新商品</code> → AI 只能在畫面隨便擺一個物件</li>
      <li><code>客群：一般大眾</code> → 配色、字體、文案調性全部變平均值（= 沒特色）</li>
    </ul>
  </div>

  <!-- 3. 觀念 -->
  <p class="body-text">這 3 欄是 AI 拉視覺詞彙庫的<strong>索引鍵</strong>：</p>
  <ul style="padding-left:20px;font-size:.88rem;line-height:1.85;margin-bottom:18px">
    <li><strong>業種</strong> → 拉哪一組詞彙庫（餐飲 / 美妝 / App 不同庫）</li>
    <li><strong>商品</strong> → 主視覺物件長什麼樣（瓶？罐？杯？mockup？）</li>
    <li><strong>客群</strong> → 整體情緒氣質（25 歲女 IG 族 vs 45 歲男企業主，配色字體完全不同）</li>
  </ul>

  <!-- 4. 小任務 -->
  <div class="task-card task-card-large">
    <div class="task-card-header">
      <div class="task-card-name">任務｜填你的前 3 欄</div>
      <div class="task-card-time">限時 4 min</div>
    </div>
    <div class="task-card-body">
      <div class="task-card-section">
        <div class="task-card-label">要做什麼</div>
        <ul class="task-card-list">
          <li>從你最熟的業種開始（自家品牌 / 客戶 / 副業皆可）</li>
          <li>填具體商品名 + 規格 / 容量 / 價格</li>
          <li>寫 2-3 項客群描述（年齡 + 生活風格 / 痛點）</li>
        </ul>
      </div>
      <div class="task-card-section">
        <div class="task-card-label">完成物</div>
        <p>brief 卡片前 3 欄填好</p>
      </div>
      <div class="task-card-section">
        <div class="task-card-label">通過標準</div>
        <ul class="check-list">
          <li>業種能對應到 10 業種庫之一（餐飲 / 美妝 / App / 旅遊 / 教育 / 活動 / 醫美 / 寵物 / 居家 / 健身）</li>
          <li>商品有具體名稱、第三人能想像形狀</li>
          <li>客群至少 2 項描述、能想到 2-3 個具體的人</li>
        </ul>
      </div>
    </div>
    <details class="task-card-stuck">
      <summary>卡住怎麼辦？</summary>
      <ul>
        <li><strong>選不出業種</strong> → 直接借用「手沖咖啡店」當練習素材，課後換自己的</li>
        <li><strong>商品名只想得到「主打商品」</strong> → 抄 demo 案例「春季限定 抹茶提拉米蘇拿鐵 ¥680」改數字</li>
        <li><strong>客群想不出來</strong> → 想一個你最常服務的客戶（不是「一般大眾」）寫下來</li>
        <li><strong>還卡 → 跳 cycle 3 寫訴求</strong>，這 3 欄回家補</li>
      </ul>
    </details>
  </div>

  <!-- 5. 學員產出 -->
  <div class="learner-output">
    <div class="learner-output-label">在此寫下你的前 3 欄</div>
    <table class="learner-output-table">
      <tbody>
        <tr><th>業種</th><td contenteditable="true" data-placeholder="例：手沖咖啡店"></td></tr>
        <tr><th>商品</th><td contenteditable="true" data-placeholder="例：春季限定 抹茶提拉米蘇拿鐵 Regular ¥680 / Tall ¥730"></td></tr>
        <tr><th>客群</th><td contenteditable="true" data-placeholder="例：25-35 歲女性、注重生活風格、IG 重度使用者"></td></tr>
      </tbody>
    </table>
  </div>

  <!-- 6. 段內檢核（3 條對應 3 欄） -->
  <div class="self-check">
    <span class="self-check-label">段內檢核（3 條都要過）</span>
    <ul style="padding:0;margin:8px 0;list-style:none;display:flex;flex-direction:column;gap:8px">
      <li><strong>業種</strong>：能不能在 10 業種庫中圈出 1 個？</li>
      <li><strong>商品</strong>：第三人看完能不能畫出商品大致形狀與大小？</li>
      <li><strong>客群</strong>：能不能聯想到 2-3 個具體的人？</li>
    </ul>
    <p class="self-check-rule">3 條全過 → 進 cycle 3 ｜ 任一不過 → 補完再走</p>
  </div>

  <!-- 7. 老師收斂句 -->
  <blockquote class="closer">
    前 3 欄是<strong>事實陳述</strong>——你賣什麼給誰、不是品味問題。寫得越具體，AI 的視覺詞彙就拉得越準。
  </blockquote>

  <!-- 8. 銜接 -->
  <p class="cycle-bridge">→ 下一循環：事實講完了，接下來講「感覺」——訴求、必要元素、風格 preset。</p>
</section>
```

**降級到 instructor-note**：
- 原 SECTION 02 line 277「本課最重要的教學物。每欄含填什麼 + 為什麼重要 + 範例 + 填好的判準 + 常見錯誤」（這是教學意圖）
- 「為什麼重要」的長段說明可保留在 `wrong-example` 註解，但不另開 tool-card

**版面壓縮**：原本 3 欄共 3 個 `tool-grid`（每個 2 欄卡片 = 6 張 tool-card），改成 1 個 `task-card.task-card-large` + 1 個 `learner-output-table`，HTML 行數從 ~63 行縮到 ~50 行，但學員產出從 0 變 1。

---

### Cycle 3：訴求是溫度、必要元素是骨架

**觀念**：訴求和必要元素長得像，但功能完全不同——訴求決定畫面「溫度感」（情緒形容詞），必要元素決定畫面「骨架」（物件位置與占比）。學員常把這兩個混在一起。
**對應原段落**：CH2-2 SECTION 02 欄位 4（line 349-370）+ 欄位 5（372-447，含 8 版型表 + 版型-訴求速查表）。
**重構策略**：訴求 vs 必要元素是「概念區辨」型 cycle，重點不是填表，是讓學員**判斷**——給 6 個詞，學員分類「這個是訴求？還是必要元素？」。8 版型表移到 details，學員按需展開。

```html
<section class="lesson-section micro-cycle">
  <div class="cycle-eyebrow">循環 3 of 3 · 概念區辨</div>
  <h2 class="section-heading">訴求 vs 必要元素——一個管溫度、一個管骨架</h2>

  <!-- 1. 設問 -->
  <p class="cycle-question">「療癒」「商品中央」「手作感」「左下放價格」——哪些是訴求？哪些是必要元素？</p>

  <!-- 2. 錯誤例子 -->
  <div class="wrong-example">
    <span class="wrong-label">看一個壞例子（混在一起）</span>
    <code>訴求：好用、療癒、商品要放中間、左下價格、季節感</code>
    <p class="wrong-note">→ 這把「訴求」（療癒、季節感）跟「必要元素」（商品中間、左下價格）混了，又夾「好用」這種功能描述（兩邊都不是）。AI 會把這串當成標籤雲、結果什麼都顧到、什麼都不重。</p>
  </div>

  <!-- 3. 觀念 -->
  <div class="concept-pair">
    <div class="concept-pair-card">
      <div class="concept-pair-label">欄位 4：訴求</div>
      <p><strong>定義</strong>：3-5 個情緒關鍵字（不是功能、不是位置）</p>
      <p><strong>管什麼</strong>：畫面整體的「溫度感」——療癒 vs 刺激、手作 vs 科技、職人 vs 大眾</p>
      <p><strong>例</strong>：手作、季節感、療癒、留白、職人</p>
    </div>
    <div class="concept-pair-card">
      <div class="concept-pair-label">欄位 5：必要元素</div>
      <p><strong>定義</strong>：對應你選的版型（A-H）、列出每個槽位放什麼</p>
      <p><strong>管什麼</strong>：畫面的「骨架」——什麼物件、放在哪、占多大</p>
      <p><strong>例</strong>：中央杯子 70%、左上季節 tag、左下價格 + CTA</p>
    </div>
  </div>

  <p class="body-text" style="margin-top:14px"><strong>關鍵分辨</strong>：訴求用「形容詞」，必要元素用「名詞 + 位置 + 占比」。混淆會讓 AI 不知道哪些要顯形（畫面）、哪些要影響整體（氛圍）。</p>

  <!-- 4. 小任務（分類題、不是填空） -->
  <div class="task-card">
    <div class="task-card-header">
      <span class="task-card-label">小任務｜分類 6 個詞</span>
      <span class="task-card-time">限時 3 min</span>
    </div>
    <div class="task-card-body">
      <p><strong>要做什麼</strong>：把下方 6 個詞分到「訴求」或「必要元素」，並指出 2 個應該丟掉的（功能描述）</p>
      <p style="margin:10px 0;padding:10px 14px;background:var(--c-surface);border-radius:var(--radius-sm);font-size:.92rem;line-height:1.9">
        ① 療癒 ・ ② 主視覺商品 80% ・ ③ 多功能<br>
        ④ 手作感 ・ ⑤ 左上季節 tag ・ ⑥ 大字優惠
      </p>
      <p><strong>完成物</strong>：3 欄分類（訴求 / 必要元素 / 丟掉）</p>
      <p><strong>通過標準</strong>：訴求 = ①④、必要元素 = ②⑤、丟掉 = ③⑥（含理由 1 句）</p>
    </div>
  </div>

  <!-- 5. 學員產出 -->
  <div class="learner-output">
    <div class="learner-output-label">在此寫下你的分類</div>
    <table class="learner-output-table">
      <tbody>
        <tr><th>訴求</th><td contenteditable="true" data-placeholder="例：①④"></td></tr>
        <tr><th>必要元素</th><td contenteditable="true" data-placeholder="例：②⑤"></td></tr>
        <tr><th>丟掉（為什麼）</th><td contenteditable="true" data-placeholder="例：③⑥ — 都是功能描述、不是調性也不是物件"></td></tr>
      </tbody>
    </table>
  </div>

  <!-- 6. 段內檢核 -->
  <div class="self-check">
    <span class="self-check-label">段內檢核</span>
    <p>把你 cycle 2 寫的商品、想 3 個訴求形容詞 + 2 個必要元素位置——你能不能寫得出來且<strong>不混淆</strong>？</p>
    <p class="self-check-rule">能 → 進整合任務 ｜ 不能 → 看上面分類題的答案，重做一次</p>
  </div>

  <!-- 7. 老師收斂句 -->
  <blockquote class="closer">
    訴求是<strong>形容詞</strong>，必要元素是<strong>名詞 + 位置 + 占比</strong>。混在一起寫，AI 會猜你是想畫氛圍還是畫骨架。
  </blockquote>

  <!-- 8. 銜接 -->
  <p class="cycle-bridge">→ 整合任務：把前 3 個 cycle 的產出組成完整 6 欄 brief、跑出第 1 張 AI 圖。</p>

  <!-- 折疊：8 版型完整對照表（原 line 393-446） -->
  <details class="instructor-note" style="margin-top:24px">
    <summary>📚 延伸：8 版型 → 必要元素對照表（按需展開）</summary>
    <p style="font-size:.85rem;color:var(--c-muted);margin-bottom:8px">需要參考時再展開、不在主流程必看：</p>
    <table>
      <thead><tr><th>版型</th><th>必要元素清單模板</th></tr></thead>
      <tbody>
        <tr><td><strong>A 主視覺版</strong></td><td>主角商品 80-90% / 文字 ≤ 20% / 黃金視覺位置放亮點</td></tr>
        <tr><td><strong>B 橫幅版</strong></td><td>左 50% 商品 70%+ 高度 / 右 50% 文字</td></tr>
        <tr><td><strong>C 社群版</strong></td><td>主角商品 70%+ / 大量留白 / 文字 &lt; 30%</td></tr>
        <tr><td>……</td><td>（其餘 D-H 完整列）</td></tr>
      </tbody>
    </table>
  </details>
</section>
```

**新元件提案**：`.concept-pair`（左右並列的概念對照卡）。CSS：
```css
.concept-pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
.concept-pair-card{border:1px solid var(--c-border);border-radius:var(--radius);padding:16px 20px;background:var(--c-card)}
.concept-pair-label{font-family:'Shippori Mincho',serif;font-size:1rem;font-weight:700;color:var(--c-text);margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--c-border-soft)}
.concept-pair-card p{font-size:.88rem;color:var(--c-text);line-height:1.7;margin-bottom:6px}
@media(max-width:600px){.concept-pair{grid-template-columns:1fr}}
```

**降級到 instructor-note**：
- 8 版型完整對照表（原 line 393-406，13 行 table）→ details 折疊
- 版型-訴求速查表（原 line 408-446，38 行 scenario-grid）→ details 折疊
- 「快捷做法」tip-callout（原 line 448）→ instructor-note 講師備註

**為什麼這樣降級**：8 版型表是「工具書內容」，學員寫 prompt 時才查，不是學的時候看。原本放在主流程造成資訊密度暴衝。

---

### Demo 三循環的學員產出總結

走完 cycle 1-3，學員手上會有：

| 循環 | 學員產出 | 後續用途 |
|------|---------|---------|
| Cycle 1 | 兩張對比截圖 + 1 段觀察文字 | 內化「需求方」身份 |
| Cycle 2 | brief 前 3 欄填好（業種 / 商品 / 客群） | 整合任務直接複製貼上 |
| Cycle 3 | 6 個詞的分類結果（訓練概念區辨） | 整合任務寫訴求 + 必要元素時不混淆 |

**到「整合任務」（cycle 4 之後）時**，學員只剩「寫訴求 + 必要元素 + 風格 preset」3 欄要填，brief 大表是「拼回來」而不是「從零填」。這就是策略 5 的落地。

---

## §6 應該從主流程移出的內容類型

### 移到 `<details class="instructor-note">`（講師備註，預設折疊）

| 內容類型 | 範例（在 CH2-2 出現位置） |
|---------|----------------------|
| 教學意圖說明（「本課最重要的教學物…」）| line 277、line 603 |
| 為什麼這樣設計（「brief 不是模板作業…」）| line 161-164 |
| AI 特性說明（「預期差異：模糊指令版每人都會不同…」）| line 234-236、line 501 |
| 段落結論複述（「本段結論：六件套缺一個就猜一個…」）| line 257-266 |
| 試跑包準備清單（「課前備齊以下清單」）| line 700-808（整段 SECTION 04） |

### 移到 `<details>` 工具書區（預設折疊、學員按需展開）

| 內容類型 | 範例 |
|---------|------|
| 完整對照表（8 版型 × 必要元素）| line 393-406 |
| 速查表（版型-訴求對應）| line 408-446 |
| 完整 prompt 模板（含註解）| line 508-524 |
| 替代 preset 卡（韓系 / 美式復古…）| line 482-491 |

### 移到頁尾「商業情境案例」獨立區塊（不要混在主流程）

| 內容類型 | 範例 |
|---------|------|
| 完整 brief 範例（弄一下咖啡工作室六件套全填）| line 815-847 |
| 完整動手練習題（含 4 步流程說明）| line 854-915 |

### 移到下載素材區 / 外部 .md 檔（連結即可、不要塞進 HTML）

| 內容類型 | 對應檔 |
|---------|-------|
| 10 業種主題庫 | `10-industries-brief-library.md` |
| 8 版型 prompt 範例 | `8-prompt-examples.md` |
| 11 種風格 preset 速查 | `11-presets-quickref.md` |

### 直接刪除（重構後不再需要）

| 內容類型 | 為什麼可刪 |
|---------|---------|
| 重複的「常見錯誤 ✕ vs ✓」清單（每欄都列）| micro-cycle 的 wrong-example 已涵蓋 |
| 「Tip 1 / Tip 2 / Tip 3」blockquote 連發（line 549-589）| 工具書內容、不是學的內容 |
| 頁尾「檢核題 Q1 應用驗證」附完整答案範例（line 1072-1082）| 答案範例放 details 即可、不要全展開 |

---

## §7 單元自我檢查清單（重構是否到位）

> 用法：拿這份對照已重構的單元頁。每條打勾才算過。

### 結構面（10 條）

- [ ] **頁首有 today-deliverables**（3 條以內，學員 5 秒內能說出今天會交什麼）
- [ ] **SECTION 01 是暖身（≤ 3 min）**，純破題，不操作不練習
- [ ] **整頁有 3-5 個 micro-cycle**，每個 5-8 min
- [ ] **每個 cycle 結尾有 self-check**，不是只在頁尾出現
- [ ] **每個 cycle 結尾有 closer**（金句、學員可口述）
- [ ] **頁尾 quiz-item 只剩 1-2 題**（綜合判斷型，不是觀念複述）
- [ ] **試跑包 / 商業案例 / 動手練習 / 常見錯誤** 全部移入 instructor-note 或 details
- [ ] **講師備註全部包在 `.instructor-note` 或 `<details>`**，預設折疊
- [ ] **沒有任何「為什麼這樣設計」「教學意圖」直接出現在學員主流程**
- [ ] **頁面總行數 ≤ 800**（CH 單元）或 ≤ 600（PRAC）

### 互動面（10 條）

- [ ] **每個小任務都有「限時 + 要做什麼 + 完成物 + 通過標準」**
- [ ] **每個小任務都有 `.learner-output`** 區（不要學員拿紙筆寫）
- [ ] **限時 ≤ 4 分鐘**（CH 內 micro-task）或 ≤ 20 分鐘（PRAC 整段）
- [ ] **有「卡住怎麼辦」備援**（task-card-stuck，3 條 if-else）
- [ ] **完成物可被檢查**（不是「請思考一下」「請體會」）
- [ ] **通過標準明確不主觀**（不是「畫面好看」「自己滿意」）
- [ ] **小任務間有銜接句**（cycle-bridge），預告下一 cycle
- [ ] **大表（brief 六欄、8 版型對照）出現前，學員已經分別填過 / 接觸過**
- [ ] **每頁至少有 1 個「分類 / 判斷」型任務**（不是只有「填空」型）
- [ ] **PRAC 任務卡有「就地交件」設計**（learner-output 緊鄰 task-card）

### PM 定位面（5 條）

- [ ] **所有 cycle 都在訓練「需求判定 / 骨架驗收 / 系列把關」**，沒有滑成設計課
- [ ] **沒有「美感判斷」「色彩配搭」「字體選擇」這類設計師訓練**（除非是 PM 跟 designer 對話的台詞）
- [ ] **驗收標準是「對照清單」，不是「看起來對不對」**
- [ ] **修正指令範例是「具體條件式」**（「把配色限制在 3 色內」），不是「再好看一點」
- [ ] **學員產出物可被「非設計背景的 PM 同事」5 秒內讀懂**

### 內容降級面（5 條）

- [ ] **長篇背景說明 → 已移到 instructor-note**
- [ ] **完整對照表 → 已移到 `<details>` 折疊**
- [ ] **替代方案卡片（如韓系 vs 日系）→ 已移到 details**
- [ ] **重複的「常見錯誤 ✕ vs ✓」→ 整合進 wrong-example、不另列**
- [ ] **外部資料（10 業種庫、8 版型 .md）→ 連結即可、不塞 HTML**

---

## 附錄 A：新元件 lint 註冊清單（給未來施工者）

報告核可後施工前，必須先把以下 5 個新 class 寫入 `_規範/design-tokens.md` v4 區與 `docs/lint-page.py` 白名單，否則 BLOCKER 會擋。

| Class | 用途 | 應屬區塊 | 與既有元件關係 |
|-------|------|---------|--------------|
| `.micro-cycle` | 觀念→任務→檢核循環容器 | 內容組件 9 | 取代 `.lesson-section` 內無結構排列 |
| `.task-card` `.task-card-large` `.task-card-master` | 任務卡（含 header / body / stuck） | 內容組件 10 | 升級 `.exercise-block`，向後相容 |
| `.learner-output` `.learner-output-table` `.learner-output-blank` | 學員產出區 | 內容組件 11 | 新增（無對應舊元件） |
| `.self-check` | 段內檢核 | 內容組件 12 | 與 `.quiz-item` 並行（自我檢核 vs 頁尾複習） |
| `.instructor-note` | 講師備註折疊區 | 輔助組件 | 新增（無對應舊元件） |
| `.today-deliverables` | hero 內「今天交什麼」清單 | 結構骨幹（hero 區） | 新增 |
| `.concept-pair` | 概念對照雙卡（左右並列） | 內容組件 13 | 與 `.compare-grid` 並行 |
| `.wrong-example` | 錯誤例子展示 | 輔助組件 | 與 `.callout.tip` 並行 |
| `.cycle-question` `.cycle-bridge` `.closer` | micro-cycle 內輔助文字 | 輔助組件 | 新增 |

**字型尺寸驗收**：所有提案 CSS 已使用 V4 標準 15 階（2 / 1.45 / 1.2 / 1.1 / 1.05 / .95 / .92 / .9 / .88 / .85 / .82 / .8 / .75 / .72 / .7）。無新增非標 rem。

**Hover 規範驗收**：所有提案無 `translateY()`、無 `box-shadow`、無 hover 同時變超過 2 屬性。

**色彩驗收**：所有提案只用 `--c-text` / `--c-muted` / `--c-faint` / `--c-border` / `--c-border-soft` / `--c-bg` / `--c-surface` / `--c-card` 與 `--c-main`。**未直接引用 `--c-a*`**。

---

## 附錄 B：施工優先順序建議

**核可後施工順序**（不一次重構全部，分 3 階段）：

| 階段 | 對象 | 估時 | 為什麼先做 |
|------|------|------|---------|
| 1 | **CH2-2 完整 5 cycle 重構** | 2-3 hr | demo 已示範 3 cycle，補完 cycle 4-5 即可，產出「樣板課」 |
| 2 | **CH5-1 全頁手術**（1251 行 → 700 行）| 4-6 hr | 資訊最密、改動效益最大 |
| 3 | **PRAC2/3/4 補 learner-output + stuck 區** | 各 30 min | 任務卡已成形，只是補件 |
| 4 | **CH4-1 / CH4-2 / CH4-3 三頁**（互動較弱）| 各 1.5 hr | 系列課程，一次重構保持風格一致 |
| 5 | CH1-1 / CH1-2 / CH2-1 / CH3-1 / CH3-2 | 各 1 hr | 互動度尚可，最後做 |

**Lint 同步施工**：階段 1 開始前必做。否則所有重構頁會被 BLOCKER 擋。

**驗收節奏**：每階段結束跑：
```bash
python3 docs/lint-page.py courses/gen-image/
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
```

---

## 附錄 C：避免事項對照（使用者提的「請避免以下改法」）

| 使用者原則 | 本報告如何遵守 |
|----------|--------------|
| ✕ 不要只是把文字變短 | 重構是「結構轉換 + 增加學員動作」，不是純壓縮 |
| ✕ 不要只是改標題 | 每個 SECTION 不只改名、結構也跟著動（看-學-做 → micro-cycle） |
| ✕ 不要新增更多理論 | 全部既有內容，新增的只有「動詞型 task-card 包裝」 |
| ✕ 不要把所有內容變成選擇題 | cycle 1 是觀察、cycle 2 是填空、cycle 3 是分類，類型多元 |
| ✕ 不要讓學員一次填完整大表 | 拆成 3 個 cycle 分別填、最後在整合任務拼回 |
| ✕ 不要讓檢核只出現在頁尾 | self-check 在每個 cycle 後面，頁尾 quiz 只剩 1 題 |
| ✕ 不要把老師備註放在學員主流程 | 全部進 `.instructor-note` 折疊 |

---

## 結論：重構後學員的 1 天

走完一個 V4 互動工作坊版的 CH2-2 後，學員手上會有：

1. ✅ 兩張 AI 對比截圖（從 cycle 1 來）
2. ✅ 一份填好的 brief 六件套（cycle 2 + cycle 3 + 整合任務組合）
3. ✅ 一個版型選擇 + 理由（在訴求 / 必要元素 cycle 中決定）
4. ✅ 一段可貼到 AI 的 prompt（整合任務的 prompt 模板填空）
5. ✅ 一張 1:1 完稿（整合任務跑出來）
6. ✅ 一份 4 項驗收打勾結果

**這 6 件**全部可帶回工作場域使用。對比現況：學員上完課可能只有「我學過六件套」的記憶，沒有具體產出。

工作坊型 vs 講義型的最大差別不是「學的內容」，是「結束時手上有沒有東西」。

---

**報告結束。請使用者依驗收 4 點檢查。核可後另開計畫進入施工階段。**
