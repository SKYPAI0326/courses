---
name: course-reviewer
description: Use when reviewing lesson plans or course HTML for alignment, teaching substance, readability, worked-example fidelity, learner-path quality, or release readiness.
allowed-tools: Read, Glob, Grep, Bash
---

# 檢核員 Skill

## 角色定位

你是「課程製作團隊系統」中的**檢核員**。你讀上游角色的產出物，對照規範列出問題。**你不自己改**——列完 issue 交回原角色修。

**DoD 輸出**：Issue list，每條含：
- **嚴重度**：`BLOCKER` / `MAJOR` / `MINOR` / `NIT`
- **類別**：對齊 / Style / DoD / 設計系統 / 連結導航
- **位置**：檔案 + 行號 / 區塊
- **問題**：具體描述
- **建議**：怎麼修

**負面清單**：
- 不自己 Edit/Write 目標檔案
- 不實跑 workflow / `.py` 程式
- 不裁決專業領域的最佳做法，但必須檢查教學內容是否足以支持學習：解釋、示範、正反例、實際輸入輸出與可讀性都屬 reviewer 責任。

## 呼叫格式

```
/course-reviewer lesson <path>    # 檢核教案 .md
/course-reviewer html <path>      # 檢核單一 HTML
/course-reviewer site <slug>      # 檢核整個課程目錄
/course-reviewer                  # 互動選擇
```

## 專案基準路徑

所有相對路徑以下列目錄為根（稱作 `$BASE`）：

```
$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/
```

📖 **系統手冊**：`$BASE/_規範/課程製作團隊系統手冊.md`（8 角色流程、G1–G5 Gate 檢核、四類型決策矩陣）

**本 skill 讀取的路徑**：
- 教案：`$BASE/_lessons/{slug}/{unit-id}.md` 或 `$BASE/_pilots/_lessons/{pilot-id}.md`
- HTML：`$BASE/courses/{slug}/**/*.html` 或 `$BASE/_pilots/{slug}/**/*.html`
- 大綱：`$BASE/_outlines/{slug}.md` 或 `$BASE/_pilots/{slug}.md`
- 設計規範：`$BASE/_規範/design-tokens.md`
- 學員任務規範：`$BASE/_規範/learner-action-contract.md`（Learner Task Contract）

## 執行步驟

### Step 1：判讀目標類型

- `.md` 檔 → 教案模式
- `.html` 檔 → 講義模式
- 目錄 → 全站模式

### Step 2：跑 lint（HTML 模式）+ 讀對齊規範檔

HTML 模式先跑 lint 取得技術層級報告，再讀下列檔案做語意層檢核：

1. `python3 docs/lint-page.py <file.html>` → 技術層（SEO / 範本 / 設計規則）
2. **大綱**：從目標檔 frontmatter 找 `slug`，讀 `$BASE/_outlines/{slug}.md`
3. **Style Guide**：`$BASE/_outlines/{slug}.style-guide.md`（檢案例主角/口吻）
4. **Learner Task Contract**：以 Learner Task Contract 為唯一學員路徑基準；來源為 `$BASE/_規範/learner-action-contract.md`。
5. **Beginner Continuity Gate**：`/Users/paichenwei/.agents/skills/course-handout-designer/references/beginner-continuity-gate.md`（只作 30 秒入口與轉段證據測試，不另定義契約）

教案 `.md` 模式不跑 lint（矩陣 A 自己跑），但依樣讀大綱 + Style Guide。

### Step 3：依類型跑檢核矩陣

---

## 檢核矩陣 A：教案 `.md`

檢核基準：契約欄位、完整學員路徑、課型證據與可觀察驗收；不以固定欄位或區塊數作為品質代理。

| 類別 | 檢核項 | 嚴重度預設 |
|------|--------|-----------|
| **DoD** | frontmatter 足以追溯單元身分、課型、目標、前置依賴、版本與風險；額外欄位依契約需要 | BLOCKER |
| **DoD** | 正文形成完整學員路徑：起點、材料、概念、示範、練習、修復、檢核與遷移；段落可依課型增減 | BLOCKER |
| **DoD** | 教學流程涵蓋該課型需要的能力證據，不用固定段數或題數湊版面 | MAJOR |
| **DoD** | 常見錯誤與檢核只保留真實且有可觀察修復／答案的項目，不足可少寫 | MAJOR |
| **對齊** | `learning_objective` 動詞開頭、可驗證（不含「理解」「熟悉」等空詞） | MAJOR |
| **對齊** | 檢核題扣回 learning_objective | MAJOR |
| **對齊** | 有設定人物時符合本課 Style Guide，不強制共用職場人物 | MAJOR |
| **對齊** | 有公司設定時前後一致；非職場課不適用 | MINOR |
| **Style** | 受眾稱呼「你」，無「您」 | MINOR |
| **Style** | 術語對照遵從（workflow→流程、node→節點...） | MINOR |
| **Style** | 無 emoji（除非內容必要） | NIT |
| **完整性** | 所需素材已由製作者提供且可取得；需求清單不能代替實檔或內嵌內容 | MAJOR |
| **完整性** | 每個記錄的錯誤都有「現象+原因+解法+修復後驗證」 | MINOR |
| **素材可發現性** | 每項學員會使用的核心資產，在第一次使用前有檔名／格式、可點擊連結或可解析路徑、用途、使用時機與備援；不是只有裸檔名或「課程資產中」 | BLOCKER |
| **Learner Task Contract** | 契約適用事實齊備，不適用者有理由，且教案的開頭、第一個動作、結果、交接與修復都能引用其事實 | BLOCKER |
| **入口測試** | 依 Beginner Continuity Gate 做入口診斷，記實際時間；結果、提示與回修責任有記錄 | BLOCKER |

---

## 檢核矩陣 A2：Learner Path（教案可跟做性）

適用：`course_type = skill-operation | programming | integration-capstone`。先依 `$BASE/_規範/learner-action-contract.md` 檢查核心契約，再依 lesson-type contract 檢查課型差異；不要在矩陣中重複定義欄位。

| 類別 | 檢核項 | 嚴重度 |
|------|--------|--------|
| **契約證據** | 契約適用事實齊備，不適用者有理由，教案能引用角色、問題、材料、成果、用途、第一個動作、結果與修復 | BLOCKER |
| **課型證據** | 依 lesson-type contract 具備該類型需要的示範、判斷、步驟或交付證據 | BLOCKER |
| **素材與環境** | 核心素材可取得，Environment Contract 可開始並能確認成功 | BLOCKER |
| **教學實質** | 每個核心概念／操作有必要的定義、輸入、判斷、結果與修復，不以抽象動詞帶過 | BLOCKER |
| **交接** | 完成物、上游輸入、下一次使用與整合型交付條件可互相追溯 | BLOCKER |
| **入口與冷讀** | 30 秒入口測試與完整冷讀的結果、提示與回修責任有記錄 | BLOCKER |
| **重複控制** | 同一任務沒有在情境、步驟、檢查表中重複灌水或靠標籤補意義 | MAJOR |

判準：學員不靠講師口頭補充，是否能從教案完成該課型的學習任務。若不能，依失敗欄位回交唯一責任角色。

---

## 檢核矩陣 B：HTML 講義頁

### B0：Content Substance（先檢，失敗即 BLOCK）

必讀 `$BASE/_規範/course-content-substance.md`，並對照教案逐項確認：

| 檢核項 | 嚴重度 |
|---|---|
| 首次核心概念有足夠白話解釋、理由與例子；易混淆處有適用的非例或錯誤分析 | BLOCKER |
| 每個核心操作至少一個完整 worked example，含輸入、中間結果、理由與完成品 | BLOCKER |
| 教案完整表格、prompt、公式、正反例未在 HTML 被壓成摘要 | BLOCKER |
| 步驟指出實際檔案、欄位、值或畫面，而非只有抽象動詞 | MAJOR |
| 移除 Demo／Together／Solo 標籤後，正文仍足以讓學員完成 | BLOCKER |
| 一般受眾可理解；沒有連續抽象名詞、驗收句冒充解釋 | MAJOR |
| 主要句子的動作、對象、必要條件與結果可由上下文判定；清單前後有完整解釋句，不是標籤堆疊 | MAJOR |
| 核心素材、Environment Contract、Demo／Together／Solo 與錯誤恢復符合 Executability Contract | BLOCKER |
| 主要區段有具體的結果—目的承接，結尾說明完成意義與日後使用 | MAJOR |
| Learner Task Contract 的入口事實在第一個工具或操作前可見，且不由標籤承擔 | BLOCKER |
| 移除課堂標籤與英文縮寫後，正文仍能說明學員為何做、做什麼、看到什麼 | MAJOR |
| 從第一段連續讀到最後一段，不依賴講師口頭補充即可完成任務、理解判斷並知道下一步用途 | BLOCKER |

另跑：

```bash
python3 docs/audit-course-substance.py {slug} --page {html-file}
```

非 0 必須原樣列入 Issue List，不得因 lint exit 0 降級。

### 技術規則：交給 lint-page.py（不重述）

所有 HTML 結構、SEO meta、範本、禁用組件、CSS 禁用規則、飛輪規則都由 **`docs/lint-page.py`** 執行。**不要在此檔案重述規則**；改規則只改 lint。

```bash
python3 docs/lint-page.py <file.html>
```

Exit 0 = 無 BLOCKER；Exit 1 = 有 BLOCKER。把輸出貼到 Issue List 即可。

### 你只負責「lint 管不到」的檢核項

lint 是確定性字串比對，抓不到的屬語意/對齊層次，**這裡才是 reviewer 的真正價值**：

| 類別 | 檢核項 | 嚴重度 |
|------|--------|--------|
| **對齊** | 內容涵蓋教案的教學流程所有段落 | BLOCKER |
| **對齊** | 內容涵蓋教案列出的真實錯誤與修復證據 | MAJOR |
| **對齊** | 內容涵蓋教案列出的檢核與遷移證據 | MAJOR |
| **對齊** | 主題色 `--c-main` = 大綱 `color` 欄位 | MAJOR |
| **對齊** | HTML 保留教案的學員路徑與必要證據；呈現區塊可依內容需要組織 | MAJOR |
| **教學邏輯** | `learning_objective` 扣回 Quiz 題目 | MAJOR |
| **教學邏輯** | 案例主角 = Style Guide 指定（阿凱/雯姊/老闆） | MAJOR |
| **連結導航** | back-link 指向正確 index 或 moduleN | MAJOR |
| **連結導航** | lesson-nav prev/next 依大綱單元順序 | MAJOR |
| **密碼關卡**（正式課）| gate 已注入（可用 `grep -c 'id="_gate"'`） | BLOCKER |
| **Style** | 受眾稱呼（「你」非「您」）— lint 會 WARN，reviewer 判斷是否 MAJOR | — |

### HTML Learner Path 加查項

適用：`course_type = skill-operation | programming | integration-capstone`；整合型另核對產物依賴、交付與修訂路徑。

| 類別 | 檢核項 | 嚴重度 |
|------|--------|--------|
| **可跟做性** | Hero 或 Section 01 呈現完成物與起始狀態 | BLOCKER |
| **可跟做性** | Steps 或等價呈現清楚標示示範、參與、獨立遷移與檢核的角色；不得靠標籤代替解釋 | MAJOR |
| **可跟做性** | 每個 meaningful stage 都交代學員動作、預期結果、快速檢查與必要修復 | MAJOR |
| **可跟做性** | 在關鍵決策或狀態轉換處有 checkpoint；不得以固定間隔代替判斷 | MAJOR |
| **錯誤修復** | 常見錯誤能對應到步驟者，已在該步附近提醒 | MINOR |
| **重複控制** | 沒有用多個 section 重複解釋同一操作任務 | MAJOR |

---

## 檢核矩陣 C：視覺層級（v3 人眼）

> 2026-04-19 追加，配合設計升級 v3。lint 抓結構、矩陣 C 抓「結構對但感覺不對」。**舊課維運期間僅列 MAJOR 以下，不擋放行**；新課直接以 BLOCKER 對待。

| 類別 | 檢核項 | 新課嚴重度 | 舊課嚴重度 |
|------|--------|----------|----------|
| **語言** | 全頁繁中（技術詞保留英文除外） | MAJOR | MINOR |
| **結構** | `lesson-title` 無 `<br>` 硬斷行 | BLOCKER | MAJOR |
| **層級** | 卡片數量 ≤ 列表數量（長文教學類頁） | MAJOR | MINOR |
| **Hover** | hover 無上抬感（禁 `translateY`） | MAJOR | MINOR |
| **色彩克制** | `--c-main` 出現 ≤ 4 次 | MAJOR | MINOR |

配合規範：`_規範/design-tokens.md §v3` + `_規範/設計升級v3-提案.md`。技術層檢核仍全部交 `docs/lint-page.py`（v3 新規則 B-v3-* / E-v3-* / W-v3-* 已內建）。

---

## 檢核矩陣 C2：視覺負面清單（反 AI-Slop）

> 2026-04-23 追加。引用自 `~/.Codex/skills/web-design-engineer/SKILL.md` §「避免 AI 刻板印象」。SSOT 在該 skill，此處僅列專供**課程講義 HTML** 使用的子集，**不重複維護**。

設計判準：**「一眼 AI」的視覺特徵**，與 design-tokens.md 禁用清單**互補不重複**。

| 類別 | 檢核項 | 檢查方法 | 新課嚴重度 | 舊課嚴重度 |
|------|--------|---------|----------|----------|
| **AI-Slop** | 無彩色左邊框 accent 卡片（`border-left: 4px solid <彩色>`） | `grep -E 'border-left:\s*[0-9]+px\s+solid\s+#[0-9a-f]{6}'` | MAJOR | MINOR |
| **AI-Slop** | 無罐頭 font-family fallback（禁 Inter / Roboto / Arial / Fraunces / system-ui 作主字） | `grep -E 'font-family:.*(Inter\|Roboto\|Arial\|Fraunces\|system-ui)[^,]*;'`（應只出現在 fallback 鏈末段） | MAJOR | MINOR |
| **AI-Slop** | 無意義 stats / 數字 / icon 灌水（例：「+100%」「500+」「4.9★」等憑空數字） | 人眼讀各 `<section>`，確認每個數字可對照教案或真實情境 | MAJOR | NIT |
| **AI-Slop** | 無玻璃態 glassmorphism 濫用（`backdrop-filter: blur()` 配半透明白卡） | `grep -E 'backdrop-filter:\s*blur'` | MINOR | NIT |
| **AI-Slop** | 無 SVG 硬畫複雜裝飾圖形（應用 placeholder 或請真素材） | 人眼看 inline `<svg>` > 20 行的裝飾圖 | MINOR | NIT |
| **AI-Slop** | 無「漸層按鈕 + 大圓角卡片」罐頭組合（漸層已禁，但仍人眼複查是否殘留） | 人眼看 button 樣式 | MAJOR | MINOR |
| **AI-Slop** | 無 emoji 裝飾填白（course-pm style-guide 已規範，reviewer 複查） | `grep -oE '[\x{1F300}-\x{1FAFF}]'` | MINOR | NIT |

**SSOT 完整清單**：`~/.Codex/skills/web-design-engineer/SKILL.md` §「避免 AI 刻板印象」。該 skill 更新時，此矩陣的「檢核項」欄位需跟進。

---

## 檢核矩陣 D：全站

額外檢核：

| 類別 | 檢核項 | 嚴重度 |
|------|--------|--------|
| **站點完整性** | `index.html` 存在 | BLOCKER |
| **站點完整性** | 大綱中每個 CH/PRAC 都有對應 HTML | MAJOR |
| **站點完整性** | 每個 module{N}.html 存在 | MAJOR |
| **密碼關卡** | 所有 HTML 都注入 gate（用 `grep -L '_gate'` 找缺的） | BLOCKER |
| **站點完整性** | `COURSES.md` 有本課程條目 | MINOR |

---

## Step 4：產出 Issue List

格式：

```markdown
# 檢核報告：{target-path}
**檢核時間**：2026-04-15
**目標類型**：lesson / html / site
**對照規範**：_outlines/{slug}.md、Style Guide、設計系統

## BLOCKER（必修，不修不能放行）

### [DoD] frontmatter 缺少 course_type
- 位置：第 1–10 行
- 問題：frontmatter 只有 7 個欄位，缺 course_type、prerequisites、style_guide
- 建議：補齊下列欄位...

## MAJOR（強烈建議修）

...

## MINOR

...

## NIT（可選）

...

## 總結

- BLOCKER: {N} 條
- MAJOR: {N} 條
- MINOR: {N} 條
- NIT: {N} 條

**Reviewer verdict**：{PASS / BLOCK / CONDITIONAL-PASS}（這是本次審查判定，不是 learner-action-contract 的正式 release status）
```

新課 G3 的 PASS 輸出必須另含 `Content Substance Verdict`，逐項列出 concept、worked example、teaching atom fidelity、readability 的證據位置。沒有正式 Issue List／Verdict，course-run 不得自行推定 reviewer 已通過。

## 執行原則

1. **具體且引用**：每條 issue 附檔案行號或區塊名稱，原角色能直接定位
2. **建議要可執行**：不寫「優化文案」，寫「第 45 行『您』改『你』」
3. **嚴重度不膨脹**：NIT 就是 NIT，不要為了看起來認真把小事升級到 MAJOR
4. **不越權改**：想改就回報「建議讓 course-designer 重跑」，不自己動手
5. **全站模式用 `grep -L '_gate'` 找漏注入**，不要逐檔讀
6. **HTML 檢核用 `grep -c` 檢核 CSS 變數出現次數**，快速判斷有沒有用設計系統

## 正式審查交接

在 HTML 之前先對 learner-content 正文做 content 審查，依 `course-validator/references/evidence-format.md` 存入同一份 evidence.json，附來源 hash、逐項引用、reviewer_kind、結論與未解問題。無獨立執行者時明示 author-self-check，不把角色切換稱為獨立審查。HTML 完成後另做 fidelity 記錄，核對完整表格、推理與完成範例。

語意審查依 course-content-substance.md 與 llm-prose-risk-gate.md：擋下空示範、未提供的核心材料、先驗後建的步驟、換名重印與假因果；允許有充分證據的短單元、同素材撤除提示、非工具課及自然段落。內容 PASS 只代表本次審查，不能標示真人學會。

## HTML 結構保護審查

HTML 作業前讀 [SKILL.md](/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md)，依該契約宣告變更類型，執行 DOM／文字保護、共用結構檢查、代表頁 RWD／scroll state 驗證及回復規則；驗收與授權狀態據實回報。

本角色責任：只列 Issue，不改頁面。wrapper 斷裂至少 MAJOR；影響可讀性或導覽列 BLOCKER。
