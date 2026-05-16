# 課程完整性檢核 SOP

**版本**：v1.0 · 2026-05-16  
**適用**：所有課程（帶入 `{SLUG}` 即可套用）  
**SSOT**：本檔案（機器可讀指令 + 人類流程說明）

---

## 角色定位

本 SOP 定義「課程完整性審核員」的執行程序。

**與 `course-reviewer` 的分工：**

| 工具 | 負責範圍 |
|------|---------|
| `course-reviewer` | 設計系統對齊、HTML 結構規範、教案格式 |
| `check-rule`（本文件）| 內容層事實正確性、素材存在性、提示詞可執行性 |

兩者互補，不重疊。`lint-page.py` 負責技術結構，不在本 SOP 範疇但作為 Phase B 的工具。

---

## 觸發條件

執行本 SOP 的時機：

1. **新課上線前**（G4 Gate 前，緊接 `course-reviewer` 之後）
2. **課程素材更新後**（datasets 異動、prompts 增刪）
3. **`platform_version` 更新時**（AI 平台能力有重大異動）
4. **學員回報「步驟無法執行」**（即時觸發，只跑 Phase C/E/F）

---

## 適用參數

套用本 SOP 時，先定義以下變數：

```
SLUG        = 課程代碼（e.g., office-ai-cases）
BASE        = _規範/../courses/{SLUG}/
ASSETS_DIR  = {BASE}/assets/
DATASETS    = {ASSETS_DIR}/datasets/
OUTLINE     = _outlines/{SLUG}.md
PROMPTS_SRC = {DATASETS}/prompts-56.md    # 若存在，否則為空
AI_ORCH     = ../ai-orchestration          # codex_bridge.py 所在路徑
```

---

## 四層檢查架構

```
L1  技術結構      →  lint-page.py（已有，Phase B 直接呼叫）
L2  交叉引用完整性 →  grep + 素材清單比對（Phase C + D）
L3  AI 能力準確性  →  Codex consult 第一輪（Phase E）
L4  提示詞×素材匹配 →  Codex consult 第二輪（Phase F）
```

---

## 七階段執行流程

### Phase A：準備

**目標**：建立三份基準清單，後續 Phase 比對用。

```bash
# A1 已知素材清單（datasets 目錄下所有檔案）
ls {DATASETS}/ > /tmp/known_assets.txt

# A2 已知頁面清單（課程目錄下所有 HTML）
ls {BASE}/*.html | xargs -I{} basename {} > /tmp/known_pages.txt

# A3 課程承諾清單（從大綱手動提取，見下方格式）
```

**A3 格式** — 從 `{OUTLINE}` 的「學習成果」與「試跑包交付規格」手動建立：

```
承諾-履行對照表 初始版（每行格式：類型|承諾描述|對應頁面/素材）
LEARNING|能生成週報草稿|CH1-1.html
LEARNING|能合併業務行程與費用分析|CH1-2.html
ASSET|ecom-orders-500.csv 可上機操作|datasets/ecom-orders-500.csv
...
```

---

### Phase B：技術層掃描（L1）

```bash
cd /Users/paichenwei/Library/Mobile\ Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁
python3 docs/lint-page.py courses/{SLUG}/
```

**記錄**：BLOCKER N 條 / ERROR N 條 / WARN N 條  
**判定**：有 BLOCKER → 先修，本 SOP 其他 Phase 照跑但最終 BLOCK

---

### Phase C：交叉引用掃描（L2）

**C1 素材存在性** — 找 HTML 中提及但 datasets/ 不存在的檔案：

```bash
# 提取 HTML 中所有副檔名提及
grep -rhoE '[a-z0-9_-]+\.(csv|txt|md|xlsx|json)' courses/{SLUG}/*.html | sort -u > /tmp/html_refs.txt

# 比對 known_assets.txt（用 comm 找只在 html_refs 不在 assets 的行）
comm -23 <(sort /tmp/html_refs.txt) <(sort /tmp/known_assets.txt)
```

輸出為「dead reference 清單」，每行即 BLOCKER 一條。

**C2 頁面引用完整性** — 找 HTML 中引用但不存在的頁面：

```bash
# 提取 HTML 中所有同課頁面連結
grep -rhoE '(CH|PRAC|module)[0-9A-Za-z-]+\.html' courses/{SLUG}/*.html | sort -u > /tmp/page_refs.txt

# 比對 known_pages.txt
comm -23 <(sort /tmp/page_refs.txt) <(sort /tmp/known_pages.txt)
```

輸出為「broken page link 清單」，每行即 BLOCKER 一條。

**C3 提示詞庫引用** — 找 HTML 中提及但 prompts 庫不存在的編號（若有 `{PROMPTS_SRC}`）：

```bash
# 提取 HTML 中 P-XX 格式編號
grep -rhoE 'P-[0-9]+' courses/{SLUG}/*.html | sort -u > /tmp/prompt_refs.txt

# 提取 prompts 庫中實際編號
grep -oE 'P-[0-9]+' {PROMPTS_SRC} | sort -u > /tmp/prompt_known.txt

# 找差異
comm -23 <(sort /tmp/prompt_refs.txt) <(sort /tmp/prompt_known.txt)
```

輸出為「orphan prompt reference 清單」，每行即 MAJOR 一條。

---

### Phase D：承諾履行掃描（L2）

**目標**：對照 Phase A 建立的「承諾-履行對照表」，逐條確認是否有對應 HTML 內容。

逐條檢查流程（人工 + grep 輔助）：

```bash
# 確認特定關鍵詞是否出現在對應 HTML
grep -l "週報" courses/{SLUG}/CH1-1.html   # LEARNING 承諾確認範例
```

**判定規則**：

| 結果 | 說明 | 嚴重度 |
|------|------|--------|
| YES | 對應 HTML section 或步驟明確存在 | — |
| PARTIAL | 有提到但步驟不完整或缺素材連結 | MINOR |
| NO | 承諾項目在 HTML 中完全找不到 | MAJOR |

最終輸出格式：

```
承諾-履行對照表（完整版）
LEARNING|能生成週報草稿|CH1-1.html|YES
LEARNING|能合併業務行程與費用分析|CH1-2.html|PARTIAL|缺費用彙總的驗證步驟
ASSET|ecom-orders-500.csv 可上機操作|datasets/ecom-orders-500.csv|YES
```

---

### Phase E：Codex 第一輪 — AI 能力準確性（L3）

> **前置確認**：`~/.claude/orchestration/codex_workflow.json` 中 `enabled: true`  
> **Plan mode 下禁止執行本 Phase**（成本保護）

**E1 提取 AI 工具能力聲明**：

從各 HTML 手動或 grep 提取所有涉及 AI 工具能力的描述，例如：
- 「ChatGPT 免費版可上傳 CSV 檔」
- 「Gemini 免費版可分析 500 筆資料」
- 「NotebookLM 可上傳 PDF 作為知識庫」

彙整為純文字清單（能力聲明.txt），每行一條聲明。

**E2 執行 Codex consult**：

```bash
python3 {AI_ORCH}/codex_bridge.py \
  --task consult \
  --prompt "你是 AI 平台能力核查員。請逐條核實以下能力聲明，以 2026 年 5 月當前免費版實際能力為準，對每條標注：ACCURATE / OUTDATED / UNCERTAIN，並附簡短說明（30 字內）。

$(cat /tmp/能力聲明.txt)"
```

**E3 記錄與標記**：

```bash
# 取得輸出後標記 verdict
python3 {AI_ORCH}/codex_bridge.py --mark-verdict <CALL_ID> --verdict accepted|actionable|rejected|noise
```

**輸出呈現格式（強制）**：

```
Codex 建議：[摘要，列出 OUTDATED N 條]
我的判斷：[接受/拒絕/部分採納]
理由：[一句話]
```

**判定**：OUTDATED 條目 → MAJOR；UNCERTAIN 且影響主流程 → MINOR

---

### Phase F：Codex 第二輪 — 提示詞×素材可執行性（L4）

> 同 Phase E 前置確認與 Plan mode 限制

**F1 建立提示詞-素材組合清單**：

從各 HTML 提取「提示詞 + 對應上傳素材」的搭配，例如：
- P-01 + work-log-5day.txt（CH1-1）
- P-15 + sales-50.csv + visit-30.csv（CH1-2）
- P-28 + ecom-orders-500.csv（CH2-1）

彙整為「組合清單.txt」，格式：`{提示詞編號或全文} | {素材檔名} | {平台（ChatGPT/Gemini/etc.）}`

**F2 執行 Codex consult**：

```bash
python3 {AI_ORCH}/codex_bridge.py \
  --task consult \
  --prompt "你是課程品質審核員。請判斷以下提示詞與素材的組合是否可實際執行，評估：格式相符性、步驟完整性、指定平台免費版可執行性。對每組標注：EXECUTABLE / NEEDS_ADJUSTMENT / BROKEN，並附說明。

$(cat /tmp/組合清單.txt)"
```

**F3 記錄與標記**（同 Phase E 格式）

**判定**：BROKEN → BLOCKER；NEEDS_ADJUSTMENT → MAJOR

---

### Phase G：彙整報告

整合 Phase B–F 所有問題，輸出 Issue List。

**格式範本**：

```markdown
# 課程完整性檢核報告：{SLUG}
**檢核時間**：YYYY-MM-DD
**執行者**：Claude Code + Codex L3

---

## BLOCKER（必修，不修不能放行）

### [C1] dead_reference: expense-manual.pdf
- 位置：CH1-2.html（搜尋「expense-manual」）
- 問題：HTML 提及此檔但 assets/datasets/ 不存在
- 建議：確認正確檔名或補上素材

---

## MAJOR（強烈建議修）

### [E] OUTDATED: ChatGPT 免費版上傳 CSV 說明
- 聲明：「ChatGPT 免費版可直接上傳 CSV 進行分析」
- Codex 判定：OUTDATED（2026-05 免費版已限制上傳頻率）
- 建議：補充「每日 10 次上傳限制」或改為 Gemini 示範

---

## MINOR

...

## NIT

...

---

## 總結

| 層 | 問題數 |
|----|--------|
| L1 技術結構（lint）| BLOCKER N / ERROR N / WARN N |
| L2 交叉引用（C1 dead refs）| N 條 |
| L2 交叉引用（C2 broken pages）| N 條 |
| L2 交叉引用（C3 orphan prompts）| N 條 |
| L2 承諾履行（D PARTIAL/NO）| N 條 |
| L3 AI 能力（E OUTDATED）| N 條 |
| L4 可執行性（F BROKEN/ADJUST）| N 條 |

**Codex CALL_ID**：Phase E: {xxx} / Phase F: {xxx}

**放行判定**：PASS / BLOCK / CONDITIONAL-PASS
```

---

## 放行標準

| 條件 | 判定 |
|------|------|
| 所有層 BLOCKER = 0 | **PASS** |
| 任意 BLOCKER > 0 | **BLOCK**（修正後重跑對應 Phase）|
| BLOCKER = 0，MAJOR ≤ 3 且有對應修正計畫 | **CONDITIONAL-PASS** |

BLOCK 後重跑規則：
- C1/C2/C3 問題修正 → 重跑 Phase C
- E 問題修正（HTML 文案更新）→ 重跑 Phase E（確認修正）
- F 問題修正 → 重跑 Phase F

---

## Codex 整合限制

| 限制 | 說明 |
|------|------|
| Plan mode 下禁止執行 Phase E/F | 成本保護（`--task imagegen` 亦同）|
| 必須記錄 CALL_ID | 每次 consult 均寫入檢核報告 |
| 必須標記 verdict | 執行 `--mark-verdict` 才算完成一輪 |
| 命中率 < 30%（樣本 ≥ 10）| 暫停 Codex 輪次，改人工確認 |
| imagegen 不在本 SOP 範疇 | 另見 ORCHESTRATION 文件 |

---

## 執行記錄（每次追加至本節）

格式：

```
## [YYYY-MM-DD] {SLUG} 檢核
- Phase B: BLOCKER {N} / ERROR {N} / WARN {N}
- Phase C: dead_refs {N} / broken_pages {N} / orphan_prompts {N}
- Phase D: YES {N} / PARTIAL {N} / NO {N}
- Phase E: CALL_ID {xxx}，verdict {accepted}，OUTDATED {N} 條
- Phase F: CALL_ID {xxx}，verdict {actionable}，BROKEN {N} 組
- 放行判定: PASS / BLOCK / CONDITIONAL-PASS
- 備註: （若有）
```

---

## [2026-05-16] office-ai-cases 檢核
- Phase B: BLOCKER 0 / ERROR 0 / WARN 9（字型尺度 × 7 頁、callout 超數 × 3 頁、hover 多屬性 × 1 頁）
- Phase C: dead_refs 0 / broken_pages 0 / orphan_prompts 0（C3 N/A，本課不使用 P-XX 格式）
- Phase D: 承諾履行——MAJOR 1（CH2-2 投影片計數 5→7 張，CH2-1 slide ③ 來源未標）/ MINOR 1（home-recipes.md 檔名誤導）
- Phase E: CALL_ID 634a8ca5，verdict actionable，OUTDATED 1 條（ChatGPT free context「32,000 字」→「16K tokens」）/ UNCERTAIN 2 條（Claude reset 機制、Gemini/ChatGPT 比較主觀）
- Phase F: CALL_ID 117c4cd2，verdict accepted，NEEDS_ADJUSTMENT 3 組（B P1-2A 地址省略已是教學設計、E join 由 AI 處理已規避、F 貼文字方式已規避上傳限制）
- 放行判定: PASS（修正後）
- 備註: 共修 MAJOR 2 + MINOR 2 + NIT 2；after-class-guide.md 重命名（原 home-recipes.md）；lint 整站 BLOCKER 0 確認

---
