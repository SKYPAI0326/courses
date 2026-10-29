---
name: build-course-page
description: Use when converting reviewed lesson content into learner-facing course HTML, especially when each course needs its own evidence-backed visual system and full teaching atoms must survive rendering.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 課程網頁講義建置 Skill

新頁一律從已審查的 lesson record 與正式正文產出。每門課依主題、學員、任務、內容密度與主要裝置建立自己的視覺決策；共通的是內容保真、導覽、響應式、無障礙、素材可取得與實際操作驗證。

## 呼叫格式

```
/build-course-page --lesson-plan _lessons/{slug}/CH2-1.md  # 教案模式（主流）
/build-course-page --lesson-plan _pilots/_lessons/pilot-a.md       # 試飛單元
/build-course-page overview module3                                 # 模組總覽頁
/build-course-page update-cards module3.html                        # 更新 concept card 連結
/build-course-page          ← 無參數時詢問使用者要建立什麼
```

參數：`$ARGUMENTS`

---

## 專案基準路徑

所有相對路徑以下列目錄為根（稱作 `$BASE`）：

```
$BASE = $COURSE_WEB_ROOT
```

📖 **系統手冊**：`$BASE/_規範/課程製作團隊系統手冊.md`（8 角色流程、G1–G5 Gate 檢核、四課型證據契約）

**本 skill 讀寫的路徑**：
- 讀入（教案模式）：`$BASE/_lessons/{slug}/{unit-id}.md` 或 `$BASE/_pilots/_lessons/{pilot-id}.md`
- 讀入（大綱）：`$BASE/_outlines/{slug}.md` 或 `$BASE/_pilots/{slug}.md`
- 產出：`$BASE/courses/{slug}/{partN}/{unit-id}.html` 或 `$BASE/_pilots/{slug}/{unit-id}.html`
- 設計規範：`$BASE/_規範/design-tokens.md`
- 學員任務規範：`$BASE/_規範/learner-action-contract.md`（Learner Task Contract）

## Step 0：任務判斷

| `$ARGUMENTS` | 任務 | 進下一步 |
|--------------|------|----------|
| 含 `--lesson-plan <path>` | 教案模式（主流） | 跳「頁面類型 D」 |
| `overview module<N>` | 模組總覽頁 | 跳「頁面類型 B」 |
| `update-cards <file>` | 更新既有卡片連結 | 跳「頁面類型 C」 |
| 無參數 | 互動選擇 | AskUserQuestion |

**所有模式都先讀大綱**：從教案或參數推出 slug，讀 `$BASE/_outlines/{slug}.md` 取 `color / name / institution / 單元前後關係`。

---

## 規則 = 課程視覺決策 + 共通驗收

| 目的 | 真相源 |
|------|-------|
| 課程專屬視覺 | [course-visual-decision.json](references/course-visual-decision.json) |
| 內容與素材契約 | lesson record + asset manifest |
| 共通規則驗證 | `$BASE/docs/lint-page.py` + course-html-contract + pilot record |

既有模板與課程頁只能當參考，不是新課的版型規格。設計決策完成前不開始寫 HTML；G4 只製作風險最高的代表單元，通過後才能把視覺系統擴用到全課。

---

## 頁面類型 B：模組總覽頁（Module Overview）

### 檔案命名規則

```
module{N}.html
例：module3.html
```

### Concept Card Grid 規則

每個 Section 的卡片數量依該 Section 的真實概念與學習路徑決定：
- 有對應步驟頁或學員產物時，卡片應連到可讀取的內容或明確交付路徑。
- 尚未有內容的項目不要用空卡片或「建置中」文字填版面；若必須顯示規劃項目，清楚標示狀態與缺少的證據。

**可點擊概念卡的寫法**：
```html
<a href="m{N}-{M}-{slug}.html" class="concept-card"
   style="text-decoration:none;color:inherit;display:block;cursor:pointer;transition:box-shadow .2s,border-color .2s;"
   onmouseover="this.style.boxShadow='0 4px 16px rgba(107,127,163,.18)';this.style.borderColor='rgba(107,127,163,.5)'"
   onmouseout="this.style.boxShadow='';this.style.borderColor=''">
  <div class="concept-num">{N}</div>
  <div class="concept-title">{標題} →</div>
  <div class="concept-desc">{描述，說明這個步驟頁的核心內容}</div>
</a>
```

**尚未有內容的規劃卡（僅在確有導覽需要時使用）**：
```html
<div class="concept-card" style="opacity:.55">
  <div class="concept-num">{N}</div>
  <div class="concept-title">{標題}</div>
  <div class="concept-desc">{規劃目的}<br><small>狀態：{blocked／待素材／待驗收}；缺少：{具體證據}</small></div>
</div>
```

---

## 頁面類型 C：更新 Concept Cards（update-cards）

讀取指定的 module HTML 文件，找出所有 `.concept-grid` 區塊，對照同目錄已存在的步驟頁檔案，將有對應步驟頁的 Card 01 改為可點擊連結。

---

## 頁面類型 D：教案模式（Lesson Plan Mode）

**觸發**：參數含 `--lesson-plan <path>`，例：
```
/build-course-page --lesson-plan _lessons/n8n-pro/CH2-1.md
```

正式正文是內容唯一來源。先依 learner-action-contract.md 找出 learner-content 範圍，確認 evidence.json 有本版本的 content 審查；執行 `bash "$SKILLS_ROOT/course-validator/scripts/course-validator.sh" {slug} content --unit {unit_id}` 核對版本。`COURSE_WEB_ROOT` 與 `SKILLS_ROOT` 缺一即停止。沒有有效審查先交 reviewer，不能用頁面排版補內容。試飛使用相同證據規則，可在隔離專案根目錄以 COURSE_WEB_ROOT 指定測試路徑。

<!-- anchor:step-d0.5 -->
### Step D0.5：建立課程專屬視覺決策

依 [course-visual-decision.json](references/course-visual-decision.json) 記錄主題、學員、任務、內容密度與主要裝置，再決定版面、導覽、字體、色彩、響應式與內容組件。每項決定都要說明它如何支援本課的閱讀或操作，不以「沿用慣例」代替理由。

新頁必須包含：
- 完整 SEO meta（description、og:*、twitter:*、canonical）
- Skip-link `<a href="#main" class="skip-link">跳至主要內容</a>`
- 主要內容區 `<main id="main">...</main>`
- focus-visible CSS 規則
- 可辨識的課程入口、上一頁與下一頁
- 在手機、平板與桌面都能完成核心路徑的版面
- 不靠顏色單獨傳達狀態的可及性處理

可從既有模板抽取經驗，但輸出必須由本課視覺決策推導；不得複製舊課外觀後補一段理由。所有素材先登錄 asset manifest 並完成權利、版本、取得與開啟測試。

**必讀**：`$BASE/_規範/learner-action-contract.md`。產頁以 Learner Task Contract 為唯一學員路徑來源，只呈現教案已凍結的契約事實，不另造入口或故事規則。

**必讀**：`$SKILLS_ROOT/course-handout-designer/references/beginner-continuity-gate.md`。它只提供 30 秒入口與轉段測試。未設定 `SKILLS_ROOT`，或教案缺契約、素材、完整示範或必要操作證據時，停止產頁並退回 `course-designer`／素材製作；builder 不臨場補寫技術事實。

<!-- anchor:step-d1 -->
### Step D1：讀教案檔 + 依 course_type 決定骨架重心

讀取 `<path>`，解析：

**frontmatter**：
- `slug`、`unit_id`、`title`、`course_type`、`duration`
- `learning_objective` → 對應 HTML 的 `page-subtitle`
- `platform_version` → metadata 顯示「本頁以 {platform_version} 製作，YYYY-MM」

課型證據以 course-handout-designer/references/lesson-type-contract.md 為準。HTML 區塊依已審查正文的內容關係決定；不硬套 Section 編號、八區塊或卡片數。自然段落、推導、對話與表格皆可使用。

**Learner Action Rendering（操作型頁面）**：
- Hero 或 Section 01 必須明確呈現「本節完成物」與「起始狀態」。
- 可用 Demo / Together / Solo / Check 作為導航，但不得把標籤或卡片當成教學證據；連續自然段落、表格或混合呈現只要保留完整輸入、判斷、結果、檢查與修復，就可以通過。
- 若使用 step card，每張卡應包含適用的學員操作、預期結果、快速檢查與卡住時；不把固定卡片欄位套到不需要卡片的課型。
- 在關鍵決策或狀態轉換處插入 Checkpoint block；Checkpoint 要寫「現在應該看到 / 若沒看到 / 通過後才能繼續」。
- 常見錯誤除頁尾總表外，若能對應到某步，必須在該 step 附近用 `callout warn` 或 step 內「卡住時」呈現。
- 不把教案的長篇背景逐字搬進 HTML；若版面過長，優先壓縮背景文案，不刪操作、checkpoint、修復資訊。

**Teaching Atom Fidelity（強制）**：必讀 `$BASE/_規範/course-content-substance.md`。教案中的完整示範表、原始素材、完成範例、prompt、公式、中間結果、正反例與判斷理由不得壓成一句摘要卡。背景可壓縮，teaching atoms 必須原樣或資訊等價呈現。若模板現有組件不足，使用白名單中的 table、scenario-grid、code-block 或正文組合完整呈現，不得為了版面短而刪內容。

**Asset Availability Gate（正式 HTML 強制）**：
- 讀取教案「素材存在 Gate」。所有核心素材必須是 `READY`，並有實際檔案、可複製內容或明確取得路徑。
- 必讀 `$SKILLS_ROOT/course-handout-designer/references/asset-discoverability-gate.md`。逐一確認 HTML 中每項學員可見的範例檔、附件、測試資料、Blueprint、模板或完成品，在第一次使用前都有可點擊的 `href`（可開啟／下載）或可複製內容，並寫明檔名／格式、用途、使用時機與備援；只顯示 `<code>` 裸檔名或「課程資產中」不算。
- 逐一確認下載、連結、檔名、範例值、上游產物與 `href` 目標確實存在且可從目前頁面解析；頁尾資產卡不能是唯一入口。試跑包需求清單、placeholder 或「之後提供」不算素材。
- 缺素材、權限路線、完整完成品或 integration 上游產物時停止產頁，退回 `course-designer`／素材製作階段；不得自行發明或以說明文字代替。

**Learner Task Rendering（所有學員頁強制）**：
- Hero／Section 01 呈現契約中的學習問題、起始材料、完成物與用途；第一個動作前保留第一個術語定義、示範結果與成功訊號。
- 每個主要區段先寫目的與上一段的具體結果，再放表格、程式碼或 step card；結尾保留完成物、下一步用途與 stage 修復位置。
- 操作型頁面依契約呈現步驟、checkpoint、適用的支援遞減或條件變化練習與修復；concept／capstone 依各自 lesson-type contract 呈現判斷或交付證據。
- 若契約事實在教案缺失或 HTML 無法引用，停止並退回上游；不以 eyebrow、Demo/Together/Solo、長背景或新技術敘述補洞。

concept 類的「Reflection」區塊用這個新 HTML 結構（由 Troubleshoot 區塊改造）：

```html
<div class="reflection-block">
  <div class="reflection-label">反思 · REFLECTION</div>
  <div class="reflection-prompt">{教案『反思』段的開放題}</div>
</div>
```

**正文呈現原則**：只轉製正式 learner-content 範圍；完整示範、練習及答案都需保留。內部需求清單不能轉成學員素材；實際素材連結在首次使用處提供。若舊教案尚無標記，先整理既有內容並完成來源審查，不直接丟棄教師區後方的學員練習。

<!-- anchor:step-d2 -->
### Step D2：依內容關係建立 HTML 骨架

先以 lesson record 的情境、示範、跟做、獨立練習、檢查與修復關係決定資訊結構，再依視覺決策實作 head、導覽、主要內容、進度、footer 與互動。可重用既有元件的語意與程式，但 class、格線、字體、色彩與空間系統由本課決定。以下元件只提供內容呈現方法，不是必須沿用的外觀。

#### 組件用法（依設計規範選用）

完整資料表保留 thead、tbody、全部欄列與數值，窄螢幕採本課決策的重排或局部捲動。程式區保留空白與縮排。瀏覽器必須核對寬螢幕及窄螢幕；文字 hash 相同仍不能證明表格可讀。


**outcomes**（放在 hero 底部，從大綱 Outcomes 取）：
```html
<div class="outcomes">
  <div class="outcomes-label">學習成果 · OUTCOMES</div>
  <div class="outcome-item"><div class="outcome-dot"></div>{動詞開頭的成果敘述}</div>
  <!-- 依大綱實際成果逐條呈現，不用固定條數湊版面 -->
</div>
```

**tool-grid**（關鍵概念、試跑包檔案、任何要並排呈現的卡片）：
```html
<div class="tool-grid">
  <div class="tool-card">
    <div class="tool-name">{名稱}</div>
    <div class="tool-tag">{分類 tag}</div>
    <div class="tool-summary">{一句話說明}</div>
    <div class="tool-list">
      <div class="tool-list-item"><span class="tool-check">✓</span>{要點 1}</div>
    </div>
  </div>
  <!-- 只有比較或並列需要時使用卡片 -->
</div>
```

**scenario-grid**（task | pick 對應表、動手 checklist、常見錯誤對照）：
```html
<div class="scenario-grid">
  <div class="scenario-row">
    <div class="scenario-task">{任務/錯誤現象}</div>
    <div class="scenario-pick">→ <strong>{建議/原因}</strong>：{說明}</div>
  </div>
</div>
```

**callout**（info / tip / warn 三型，僅在需要提醒或檢查的地方使用）：
```html
<div class="callout info">
  <div class="callout-icon">💡</div>
  <div class="callout-body"><strong>{短標}</strong>{內文}</div>
</div>
```

**step-circles**（**只在「操作示範」section 內使用**，不能跨 section 用）：
```html
<div class="steps-inline">
  <div class="step-block">
    <div class="step-circle">1</div>
    <div class="step-content">
      <div class="step-heading">{步驟標題}</div>
      <div class="step-body">{內容}</div>
    </div>
  </div>
</div>
```

**learner-step**（同步演練 step，操作型頁面的主體）：
```html
<div class="step-block">
  <div class="step-circle">{N}</div>
  <div class="step-content">
    <div class="step-heading">{模式} · {動詞開頭的步驟標題}</div>
    <div class="step-body">
      <p>{本階段的目的，以及它如何承接上一階段的具體結果。}</p>
      <strong>學員操作：</strong>{按哪裡、填什麼、選什麼、跑什麼}<br>
      <strong>預期結果：</strong>{畫面、輸出、資料、狀態或檔案應出現什麼}<br>
      <strong>快速檢查：</strong>{一句話判斷成功與否}<br>
      <strong>卡住時：</strong>{錯誤現象 → stage ID → 回到哪裡修正 → 從哪裡重跑 → 是否清除錯誤資料 → 安全停止狀態}
      <p>{本階段完成了什麼，以及這個結果為何是下一階段的起點。}</p>
    </div>
  </div>
</div>
```

**checkpoint-block**（在關鍵決策或狀態轉換處使用）：
```html
<div class="callout tip">
  <div class="callout-icon">✓</div>
  <div class="callout-body">
    <strong>Checkpoint：{名稱}</strong>
    現在應該看到：{結果}。若沒看到：{回到哪一步 / 檢查哪個欄位}。通過後才能繼續：{前置條件}。
  </div>
</div>
```

**big-quote**（視覺休止符，每頁最多 1 個）：
```html
<div class="big-quote">挑工具的關鍵，不是<span>「誰最強」</span>，<br>而是<span>「我現在這件事，哪個最順手」</span>。</div>
```

**互動 quiz**（取代純文字 `<ul>`，用 radio + label 可點選）：
```html
<div class="quiz-item">
  <div class="quiz-q">Q1：{題幹}</div>
  <div class="quiz-opts">
    <label class="quiz-opt"><input type="radio" name="q1"><span>A. {選項}</span></label>
    <label class="quiz-opt"><input type="radio" name="q1"><span>B. {選項}</span></label>
    <label class="quiz-opt correct"><input type="radio" name="q1"><span>C. {正解選項}</span></label>
    <label class="quiz-opt"><input type="radio" name="q1"><span>D. {選項}</span></label>
  </div>
  <details class="quiz-ans"><summary>顯示答案</summary>
    <div>正確答案：<strong>C</strong>。{解說}</div>
  </details>
</div>
```

對應 CSS（互動樣式）：
```css
.quiz-opt{display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--c-card);border:1px solid var(--c-border);border-radius:var(--radius);cursor:pointer;font-size:.88rem;color:var(--c-text);transition:border-color .15s,background .15s;}
.quiz-opt:hover{border-color:var(--c-main);background:rgba(122,158,163,.04);}
.quiz-opt input[type="radio"]{margin:0;accent-color:var(--c-main);}
.quiz-opt input[type="radio"]:checked + span{color:var(--c-main);font-weight:500;}
```

<!-- anchor:step-d3 -->
### Step D3：Head / Body / CSS 規格

依本課 visual decision 實作，並用 `lint-page.py`、course-html-contract 與實際瀏覽器驗證共同驗收。靜態 lint 只能確認確定性規則，不能證明版型適合本課或學員真的能完成核心路徑。

驗證：`python3 docs/lint-page.py <output.html>` 回 Exit 0 即過。

### Step D3.5：Metadata Footer

所有教案模式產出的 HTML，footer 加入：

```html
<footer class="footer">
  <span class="footer-logo">弄一下工作室</span>
  <div class="footer-div"></div>
  <span class="footer-note">{機構名稱}</span>
  <div class="footer-div"></div>
  <span class="footer-meta" data-platform-version="{platform_version}" data-built-at="{YYYY-MM-DD}">
    本頁以 {platform_version} 製作，{YYYY-MM}
  </span>
</footer>
```

**欄位來源對照**：
- `{機構名稱}` ← 大綱 frontmatter 的 `institution` 欄位（預設「弄一下工作室」）。若大綱有 `partner` 欄位，顯示「{institution}｜{partner}」
- `{platform_version}` ← 先查教案 frontmatter，沒有再查大綱 frontmatter。兩處都沒 → 填「未指定」並在回報中提醒使用者補欄位
- `{YYYY-MM-DD}` ← 呼叫 skill 當下的日期（shell 取 `date +%Y-%m-%d`）
- `{YYYY-MM}` ← 同上日期的年月

<!-- anchor:step-d4 -->
### Step D4：檔名與輸出位置

依教案 `unit_id` 推導：
- CH1-1 → `m1-1-{slug-from-title}.html`（或直接 `CH1-1.html`，跟隨該課程既有慣例）
- pilot-a / pilot-b / pilot-c → `_pilots/{pilot_id}.html`

輸出前先 Glob 同目錄既有 HTML，確認命名慣例再決定。

<!-- anchor:step-d5 -->
### Step D5：Post-build 自動化任務（必做）

寫完 HTML 後，**不要自己結束**，接著執行：

1. **重建搜尋索引**：
   ```bash
   cd "$BASE" && python3 docs/build-search-index.py
   ```
   產出 `docs/search-index.json`，學員的全文搜尋依賴此檔。

2. **逐頁機器檢查與保真交接**：
   ```bash
   cd "$BASE" && python3 docs/audit-course-substance.py {slug} --page {output-file}
   ```
   非 0 時停止；依輸出的 `hard_failures`、`missing_assets` 與逐頁證據回補教案中的表格、示範或完成範例，不得以 lint 通過放行。此腳本只能做確定性結構與素材檢查，教案至 HTML 的內容保真仍須由 reviewer 引用原文核對。

3. **內容保真**：reviewer 逐項核對正式正文與 HTML 的核心解釋、表格、推理、輸入、中間與完成結果，依 evidence-format.md 記 fidelity 與來源／頁面／素材版本。

4. **條件式文案 Gate**：若頁面第一個主要區段直接操作、兩個主要區段間沒有結果—目的承接、連續多組固定步驟欄位沒有自然說明，或結尾只有檢核而無完成意義／日後使用，必須使用 `course-copywriter` 修復後重跑稽核。

5. **提醒 sitemap 重建**：在回報中列出「需要執行 `/course-ops {slug} sitemap` 重建 sitemap」。（本 skill 不直接跑 sitemap，由 ops 角色負責）

<!-- anchor:course-pdf-sync -->
6. **已登錄 PDF 的同步交接**：若 `$COURSE_DESIGN_STATE_ROOT/registry/pdf/catalog.json` 存在，執行：
   ```bash
   python3 "$SKILLS_ROOT/course-pdf/scripts/run.py" --root "$BASE/courses" sync --course {slug}
   ```
   此命令預設唯讀 PLAN_ONLY，不產製 PDF。該課程有登錄成品時，回報 CURRENT／STALE／UNVERIFIED／BLOCKED 與受影響清單；沒有成品就不增加 PDF 交付要求。需重建時交給 `course-pdf`，沿用使用者已授權範圍；網頁驗收不代表 PDF 已同步。

7. **回報產出摘要**：
   ```
   ✅ 產出：courses/{slug}/{file}.html（{N} 行）
   ✅ SEO meta：description / og:* / twitter:* / canonical 全備
   ✅ 結構：skip-link ✓ main#main ✓ aria-hidden 箭頭 ✓
   ✅ 搜尋索引：已重建
   ⚠️ 下一步：/course-ops {slug} sitemap 更新 sitemap
   ```

### 教案模式的執行原則

1. **不呼叫 Gemini MCP**——內容 100% 來自教案，若覺得教案不夠好，回報 course-designer 重跑
2. **契約或必要證據缺失就回報**——教案無法引用 Learner Task Contract 事實，或缺少完成任務所需的概念、示範、修復與驗收證據，停止並提示「建議重跑 /course-designer」
3. **Style Guide 欄位遵從**——受眾稱呼「你」、步驟「步驟 N」，不要把教案內容改寫成其他口吻
4. **決策先於版型**——先完成 visual decision，再選擇重用、改造或新建頁面骨架；保留決策理由與受影響裝置
5. **設計服從任務**——陰影、漸層、圓角、動畫與色彩只有在支持層級、狀態或操作回饋時使用，不能用裝飾掩蓋內容或導覽問題
6. **可跟做性優先**——依 Learner Task Contract 與 lesson-type contract 呈現；缺完成物、起始狀態、第一個動作／結果，或操作型缺足以完成任務的 meaningful stages、關鍵 checkpoint 與修復，就不能產出形式完整但不可操作的 HTML
7. **避免重複灌水**——依 course-content-substance.md 區分有效重練與無增量重印，不因同素材而刪掉支援遞減的練習
8. **不以摘要取代教學**——頁面短不是品質指標；完整示範與可理解文字優先於卡片數量、行數與視覺留白。

---

## CSS 與組件實作

在 visual decision 中先定義本課的內容寬度、字級階層、色彩角色、空間尺度、導覽與斷點，再把這些決策寫成局部 CSS tokens。重用舊元件時，先確認語意、鍵盤操作與響應式行為符合本課；不能因為現有元件方便，就改變教學內容或強迫每門課長成同一個版型。

---

## 執行原則

1. **內容來源依目前流程決定，HTML 組裝由 Codex 完成**——教案模式只使用已審查的教案正文；舊的 Gemini 直出與 Step Page 內容路徑已退場。

2. **讀取現有檔案取得課程脈絡**——建立新頁面前，先讀 module{N}.html 了解課程定位、主題色、前後節的連結關係。

3. **導覽按鈕雙向串連**——每個步驟頁底部的「← 上一頁」和「下一頁 →」必須正確指向同 module 的前後頁，最後一頁的「下一頁」指向 module{N+1}.html。

4. **code-block 內可加語法著色**——使用 `<span class="cm/ky/st/vr">` 對程式碼著色，增加可讀性。不需安裝任何 JS 語法高亮套件。

5. **維持本課一致性**——字體、圖示與語氣依 visual decision；同一功能在全課使用一致的視覺與互動，不以裝飾性 emoji 取代文字標籤。

6. **Responsive 最低標準**——在 `390px` 手機、`820px` 平板與 `1440px` 桌面實際完成核心路徑；不得有非預期水平捲動、遮擋、裁切或閱讀順序錯置。

7. **Accessibility evidence**——G4 產出代表頁時，另存符合 `contracts/course-accessibility-report.schema.json` 的實際 report，pilot 只保存其 exact evidence ID、path、SHA-256 與 claim scope。只測 keyboard、focus、reading order、overflow 時固定聲明 `basic_accessibility_smoke`；不得寫成 WCAG conformance。若聲明 `wcag_2_2_aa`，交由 validator 核對完整適用 criteria、manual／automated results、tools、user agents、assistive technology 與 findings。

## HTML 編輯保護契約（必讀）

HTML 作業前讀 `$SKILLS_ROOT/course-html-contract/SKILL.md`；未設定 `SKILLS_ROOT` 時停止。依該契約宣告變更類型，執行 DOM／文字保護、共用結構檢查、代表頁 RWD／scroll state 驗證及回復規則；驗收與授權狀態據實回報。

本角色責任：只轉製已審查的正式正文；內容缺漏退回上游。
