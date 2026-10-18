---
name: course-repair
description: Use when an existing course has thin practice, repeated cases or workflows, duplicated Demo and Together activities, missing learner checkpoints, stale UI guidance, or delivery and lint problems that require a reversible repair.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# 現存課程修復總管 Skill

## 角色定位

你是「課程製作團隊系統」中的**舊課整修總管**。你的任務不是從零做課，而是把已存在的課程修到可交付、可跟做、可維護。

你負責統籌：
- `course-reviewer`：語意對齊與 Learner Path issue
- `course-refresh`：平台 UI 漂移風險
- `course-typography-fixer`：CJK 排版修補
- `course-ops`：SEO / links / search-index / sitemap / gates
- `course-validator`：G4 分層實測與學員視角驗收

**DoD 輸出**：
1. `courses/{slug}/_repair/{YYYY-MM-DD}/REPAIR-PLAN.md`
2. `courses/{slug}/_backup/{YYYY-MM-DD}-pre-repair/`
3. `courses/{slug}/_tools/restore-{YYYY-MM-DD}-pre-repair.sh`
4. 修補後的 `REPAIR-REPORT.md`
5. 驗證紀錄：lint / reviewer / ops / validator 的結果摘要

## 硬邊界

- 不在沒有備份與還原腳本時直接改現存課程。
- 不把「補幾段文案」當修復；操作型頁面必須補到學員可 step by step 跟做。
- 不把同類 Learner Path 問題逐頁打補丁；先依 Learner Task Contract 判斷是契約、教案產出、HTML 呈現或驗證層失效，再修唯一責任層。
- 不同時大改全站與多個課程；一次以一個 slug 或單頁為主。
- 不刪除既有內容，除非使用者明示同意；`REPAIR-PLAN.md` 必須逐項列出預計刪除／合併的重複段落，使用者核准該 plan 後才可執行。
- 不跳過驗證宣稱完成。

## Activity Identity 與角色契約

Learner Path 完整不等於學習活動有效。每個 Demo / Together / Solo 都必須先記錄**Activity Identity**：

| 欄位 | 要回答的問題 |
|------|--------------|
| 素材 | 使用哪份信件、逐字稿、表格、案例資料？ |
| 產物 | 學員完成後留下什麼？ |
| 操作路徑 | 執行哪些 prompt、轉換或查核？ |
| 學員決策 | 學員必須自行判斷什麼？ |
| 認知工作 | 這次新增哪個判斷、限制、比較或除錯？ |
| 支援程度 | 講師提供完整示範、部分提示，還是學員獨立完成？ |

**Demo / Together / Solo Role Contract**：

- `Demo`：講師建模第一次出現的判斷；可完整示範，或停在關鍵決策前交給 Together。
- `Together`：依 course-content-substance.md，可沿用示範素材並減少提示、提取理由或自行檢查；須有可觀察的認知工作與回饋。
- `Solo`：獨立遷移，改變一個或多個真正需要重新判斷的條件，且有不依賴講師的通過標準。
- `Check`：只驗證結果與判斷，不產生第二份相同成品。

重複判定看學員是否新增認知工作與獨立性，不採固定相同欄位數門檻。若兩個活動只是換素材、換標題或換提示文字，卻沒有新的判斷、限制、錯誤修復或產物責任，列為重複；若保留相同素材或相同產物，但新增條件、理由、提取判斷、錯誤修復或支援遞減，必須在 Activity Identity 說明其學習價值。Demo 已完整產出成品時，Together 仍可用相同素材作有目的的重練；只有沒有新增認知工作與獨立性的重跑才退回。

## 呼叫格式

```bash
/course-repair <slug> scan              # 掃描並產問題盤點，不改檔
/course-repair <slug> plan              # 產 REPAIR-PLAN.md，不改課程內容
/course-repair <slug> backup            # 建備份與還原腳本
/course-repair <slug> fix               # 依 plan 修補；若無 backup 先停止
/course-repair <slug> verify            # 重跑 lint/reviewer/ops/必要 validator
/course-repair <slug> report            # 產 REPAIR-REPORT.md
/course-repair <slug> all               # scan → plan → backup → fix → verify → report
/course-repair <slug> --page part1/foo.html fix
/course-repair <slug> scan --dry-run
```

無子命令時預設 `scan`。

## 專案基準路徑

```
$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/
```

**讀取**：
- `$BASE/courses/{slug}/**/*.html`
- `$BASE/_lessons/{slug}/*.md`
- `$BASE/_outlines/{slug}.md`
- `$BASE/_outlines/{slug}.style-guide.md`
- `$BASE/_規範/learner-action-contract.md`
- `$BASE/_規範/design-tokens.md`

**寫入**：
- `$BASE/courses/{slug}/_repair/{YYYY-MM-DD}/`
- `$BASE/courses/{slug}/_backup/{YYYY-MM-DD}-pre-repair/`
- `$BASE/courses/{slug}/_tools/restore-{YYYY-MM-DD}-pre-repair.sh`
- 只有在 `fix` 階段才改目標 HTML / lesson md。

## 問題分類

| 類別 | 說明 | 預設處理 |
|------|------|----------|
| `LEARNER_PATH` | Learner Task Contract 欄位缺失，或契約事實在教案／HTML／驗證中遺失 | 依責任層回修；不要逐頁複製同一補丁 |
| `CONTENT_THIN` | 文案冗長但實作薄、同一任務重複描述 | 壓縮背景，補操作與檢查 |
| `STALE_UI` | 平台版本過舊或缺 metadata | 標記 refresh，必要時重寫步驟 |
| `TYPOGRAPHY` | 中文斷字、表格過密、欄寬錯亂 | 可交給 typography fixer |
| `TECH_LINT` | SEO / template / design-token / lint 問題 | 依 lint 修 |
| `NAV_OPS` | 連結、搜尋索引、sitemap、gate 問題 | 交給 ops 或本 skill 執行命令 |
| `ASSET_DISCOVERABILITY` | 資產存在但學員找不到、無法開啟，或不知道何時／為何使用 | 回修教案與 HTML；缺檔或斷鏈時先 `BLOCKER` |
| `VALIDATION` | 真跑案例、persona journey 不通 | 交給 validator，回寫 plan |

## Step 1：scan

目的：盤點問題，不改內容。

1. 若 `$BASE/AGENTS.md` 存在先讀；不存在時沿用可見的專案指示，再讀大綱、Style Guide、Learner Task Contract。
2. Glob 目標：
   - HTML：`courses/{slug}/**/*.html`，排除 `_backup/`、`_repair/`
   - 教案：`_lessons/{slug}/*.md`
3. 對每頁 HTML 跑：
   ```bash
   cd "$BASE" && python3 docs/lint-page.py courses/{slug}/path.html --summary
   ```
4. 先把每個問題對應到 Learner Task Contract 欄位與責任層（契約缺欄位／教案遺失／HTML 遺失／驗證遺失），再對教案 / HTML 做 Learner Path 快速檢查：
   - 是否有完成物
   - 是否有起始狀態
   - 是否有足以完成任務的可操作階段；每一階段都有動作、結果、檢查與必要修復
   - 是否在關鍵決策或狀態轉換處設置 checkpoint，而非機械套用固定間隔
   - 是否有「卡住時」或錯誤修復
   - 是否同一任務重複描述
   - 為每個 Demo / Together / Solo 建立含認知工作與支援程度的 Activity Identity 表
   - 依 `course-handout-designer` 的 Asset Discoverability Gate，逐一檢查學員會使用的範例檔、附件、測試資料、Blueprint、模板與完成品：第一次使用前是否有檔名／格式、可點擊連結或可解析路徑、用途、使用時機與備援；不能只看頁尾資產清單
   - 比對同頁不同段落是否以相同素材重跑相同產物
   - 比對跨頁是否將同一 workflow 換標題後重新教一次
5. 跑 Shared Copy Audit：
   - 抽取跨頁完整相同或高度近似的結尾、口號、安全提醒與模板說明
   - 非導航、法律聲明或必要操作警告，完整段落出現超過 2 頁列 `MINOR`
   - 若共用文案擠壓本節完成證據或實作，升為 `MAJOR`
6. 跑 metadata 掃描：
   ```bash
   grep -R 'data-platform-version=' courses/{slug}
   grep -R 'data-built-at=' courses/{slug}
   ```
7. 產出 scan summary 到 `courses/{slug}/_repair/{YYYY-MM-DD}/SCAN.md`，必須包含 `Activity Identity Audit` 與 `Shared Copy Audit`；未產出視為 scan 未完成。

## Step 2：plan

目的：把問題變成可執行修復清單。

產出 `REPAIR-PLAN.md`，格式：

```markdown
# Repair Plan: {slug}

## Scope
- slug:
- pages:
- lessons:

## Risk
- near-term class: yes/no/unknown
- backup required: yes

## BLOCKER
### [LEARNER_PATH] {file}
- 問題：
- 修法：
- 驗證：

## MAJOR
...

## Activity Identity Audit
| page | section | role | material | artifact | path | learner decision | overlap verdict |
|------|---------|------|----------|----------|------|------------------|-----------------|

## Shared Copy Audit
| repeated copy | pages | allowed reason | action |
|---------------|-------|----------------|--------|

## Execution Order
1. backup
2. learner-path fixes
3. typography / lint fixes
4. ops rebuild
5. reviewer / validator verification
```

嚴重度規則：
- 缺完成物 / 起始狀態 / 可跟做步驟：`BLOCKER`
- 有步驟但缺 checkpoint / 預期結果 / 卡關修復：`MAJOR`
- 重複描述、背景文案擠壓實作：`MAJOR`
- Demo 與 Together 沒有新增認知工作或獨立性：`MAJOR`
- Together 沒有新增學員決策，只是重播 Demo：`MAJOR`
- Solo 未改素材、對象、限制或決策，或沒有獨立通過標準：`MAJOR`
- 核心資產缺少學員取得方式、第一次使用前的連結／路徑，或 `href` 目標不存在：`BLOCKER`
- 資產可以取得但未說明其輸入、輸出或使用時機：`MAJOR`
- 非必要完整共用段落出現超過 2 頁：`MINOR`；擠壓本節實作時升 `MAJOR`
- 純排版問題：`MINOR`，除非影響閱讀

## Step 3：backup

目的：讓修復可回滾。

1. 建立：
   ```bash
   courses/{slug}/_backup/{YYYY-MM-DD}-pre-repair/
   courses/{slug}/_tools/
   ```
2. 複製本次 scope 內會改的 HTML / md 到 backup，保留相對路徑。
3. 建立還原腳本：
   ```bash
   courses/{slug}/_tools/restore-{YYYY-MM-DD}-pre-repair.sh
   ```
4. 驗證：
   ```bash
   bash -n courses/{slug}/_tools/restore-{YYYY-MM-DD}-pre-repair.sh
   ```

沒有 backup + restore script，不准進 `fix`。

## Step 4：fix

目的：依 plan 外科式修補。

修補順序：
1. **Learner Path**：先修正契約或教案來源，再把已修正的事實呈現到 HTML；缺 universal 欄位才回修核心契約，單頁／單平台問題留在對應層。
2. **Content Thinness**：刪減重複文案，保留必要概念，增加操作、檢查、修復。
3. **Activity Roles**：先依 Activity Identity 決定案例屬於 Demo、Together 或 Solo；不得先保留完整 Demo，再為了補步數新增同案例 Together。
4. **HTML Rendering**：把已分工的活動轉成 Demo / Together / Solo / Check 節奏。
5. **Typography**：只處理明確 CJK 排版問題；可套用 `course-typography-fixer` 規則。
6. **Tech Lint**：修 lint BLOCKER / ERROR。
7. **Ops**：重建 search-index；sitemap / gates 交給 `course-ops` 或在 verify 提醒。

修補原則：
- 小批次改，每批可被 reviewer 驗證。
- 不重排全頁、不順手美化。
- 操作型內容優先補「做什麼、看到什麼、怎麼檢查、卡住怎麼辦」。
- 第一次出現 prompt 時就決定由學員操作或講師示範；若學員已在 Together 完成，不在前段另放完整輸出。
- Demo 已完整展示時，後段可保留相同素材的提示遞減或提取練習；若只重跑示範而沒有新增判斷、修復或獨立性，才合併或刪除。
- Together 沿用 Demo 素材時，依共通內容實質契約說明支援遞減、提取判斷或修復的學習用途。
- 共用口號與安全提醒集中在課程級 checkpoint；其餘頁面改成本節專屬完成證據。
- 修補若需要平台最新 UI，先標 `STALE_UI`，不要憑記憶亂改。

## Step 5：verify

至少執行：

```bash
cd "$BASE" && python3 docs/lint-page.py courses/{slug}/ --summary
cd "$BASE" && python3 docs/build-search-index.py
```

依修補類型加跑：
- Learner Path 修補 → 用 `course-reviewer` 矩陣 A2 / HTML Learner Path 重查。
- Learner Path 修補 → 重建 Activity Identity Audit；任兩活動 3 欄以上相同或 Together 無新增決策即驗收失敗。
- 多頁內容修補 → 重跑 Shared Copy Audit；未說明的共用完整段落超過 2 頁即不得宣告全課完成。
- 多頁或交付前 → 建議跑 `course-validator <slug> preflight`，必要時跑 L1-L3 / L5。
- 連結或 gate 相關 → 跑 `course-ops <slug> links|gates|all`。

不可只因檔案已修改就宣稱完成。

## Step 6：report

產出 `REPAIR-REPORT.md`：

```markdown
# Repair Report: {slug}

## Changed
- file:
- issue fixed:

## Verification
- lint:
- search-index:
- reviewer:
- validator:
- activity-identity-audit:
- shared-copy-audit:

## Remaining
- item:
- owner:

## Restore
- backup:
- restore script:
```

## 與其他 skill 的銜接

- 發現 UI 漂移很多 → 先跑 `/course-refresh <slug>`，不要直接補文案。
- 只剩 CJK 排版 → 交給 `/course-typography-fixer <slug>`。
- 只剩 SEO / links / sitemap / gates → 交給 `/course-ops <slug> all`。
- 交付前或 learner path 大改 → 跑 `/course-validator <slug> preflight`，必要時跑 L5 persona。

## 執行原則

1. **先盤點再修**：`scan/plan` 不改內容。
2. **先備份再動手**：沒有 backup + restore script 就停。
3. **先修可跟做性**：Learner Path BLOCKER 高於視覺與文案。
4. **少量多驗證**：修 1-3 頁就跑一次 lint/reviewer，不等全課改完。
5. **保留追蹤檔**：所有 scan/plan/report 都進 `_repair/{YYYY-MM-DD}/`。
6. **舊課不假裝新課**：缺平台資訊就標 `STALE_UI`，不可用記憶補最新畫面。
7. **不以欄位完整冒充教學有效**：必要方法、checkpoint 與練習證據齊全後，仍必須通過 Activity Identity 與 Shared Copy Audit。

## 常見誤判

| 誤判 | 正確處理 |
|------|----------|
| 「學員親手再做一次，所以不是重複」 | 若 Demo 已完整展示，而後續活動沒有新增認知工作、限制、修復或獨立性，仍是重複。 |
| 「已有 Solo，所以 Together 重播可以保留」 | Solo 不會抵銷前面的重複；Together 仍須新增決策。 |
| 「同一句話很重要，所以每頁都放」 | 集中在開場、關鍵 checkpoint 或結訓；其餘頁放本節完成證據。 |
| 「lint 與 preflight 全綠，所以修好了」 | 技術驗證不涵蓋語意重複；兩項 audit 都通過才能結案。 |

修正正式正文後先重做 content 審查再轉製；HTML 修改後重做受影響 fidelity 與學習證據。版本格式與範圍依 course-validator/references/evidence-format.md，不能保留舊 hash 的 PASS。

## HTML 編輯保護契約（必讀）

HTML 作業前讀 [SKILL.md](/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md)，依該契約宣告變更類型，執行 DOM／文字保護、共用結構檢查、代表頁 RWD／scroll state 驗證及回復規則；驗收與授權狀態據實回報。

本角色責任：fix 前在 REPAIR-PLAN 記錄變更類型並備份；驗證失敗即回復，不堆疊修補。
