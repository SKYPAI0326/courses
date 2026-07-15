# Course Repair Scan: office-ai

- 掃描日期：2026-07-15
- 模式：`scan`（只盤點，不修改課程內容）
- 範圍：`courses/office-ai/` 的 20 個 HTML（19 個單元頁 + 1 個總覽頁）
- 大綱：`_outlines/office-ai.md`
- 教案：未找到 `_lessons/office-ai/`
- Style Guide：未找到 `_outlines/office-ai.style-guide.md`
- 判準：`_規範/learner-action-contract.md`、`_規範/design-tokens.md`、`docs/lint-page.py`

## Executive Summary

現有頁面在機器規則上可通過，但尚未達 Learner Action Contract 的「學員可不靠講師口頭補充完成」標準。

- `TECH_LINT`：20 頁皆為 0 BLOCKER / 0 ERROR；全課共 41 WARN。
- `LEARNER_PATH`：19 個單元頁皆未找到可觀察的 Checkpoint；多數頁只有 3 個 `step-item`，內容是原則或方法條列，不是 5–12 個含操作與預期結果的同步演練步驟。
- `STALE_UI`：19 個單元頁標示 `data-platform-version="2026-04-v3"`，且全部缺 `data-built-at`；需交由 refresh 判斷操作畫面是否已漂移，不能憑記憶改寫。
- `TYPOGRAPHY`：19 個單元頁皆使用 V4 字階白名單外的 `.68rem`、`.73rem`、`.76rem` 等 6 個值。
- `CONTENT_THIN`：頁面已有案例、prompt 與注意事項，但操作節奏普遍停在「看範例／帶走模板」，缺少逐步實作、途中檢核和對應步驟的卡關修復。
- `VALIDATION`：沒有教案可對照，也尚未執行案例真跑或 persona journey；本次 scan 不宣稱內容正確或可交付。

## Severity Summary

### BLOCKER

#### [LEARNER_PATH] 19 個單元頁缺同步演練最低完成線

- 缺少可明確辨識的「完成物 + 起始狀態 + 5–12 個可操作步驟 + Checkpoint」組合。
- 全部單元頁未找到 Checkpoint / 快速檢查 / 若沒看到等可觀察檢核結構。
- 現有 `.step-item` 多用於概念條列，例如「三個把關動作」或工具選項，不等同 Step Schema。
- 操作型頁面即使有 prompt 真跑，也多是展示輸入輸出，尚未交代學員每一步做什麼、看到什麼、失敗如何回復。

受影響頁面：

- `ch1/CH1-1.html` ～ `ch1/CH1-4.html`
- `ch2/CH2-1.html` ～ `ch2/CH2-3.html`
- `ch3/CH3-1.html` ～ `ch3/CH3-3.html`
- `ch4/CH4-1.html` ～ `ch4/CH4-3.html`
- `ch5/CH5-1.html` ～ `ch5/CH5-3.html`
- `ch6/CH6-1.html` ～ `ch6/CH6-3.html`

### MAJOR

#### [LEARNER_PATH] 操作頁缺途中檢核、卡關修復與變化練習閉環

- `CH1-3`、`CH1-4`、章二至章五、`CH6-1` 應優先視為 skill-operation 候選。
- `CH1-3` 雖有登入與三步操作，但步數不足、沒有逐步預期結果與 checkpoint。
- `CH5-1` 雖列三種轉文字方案，仍是工具選擇說明，沒有完成一條最短成功路徑。
- `CH2-3`、章三、章四、`CH5-2`、`CH5-3` 有真跑案例，但沒有讓學員獨立重做的完整 Solo / Check 閉環。
- 多數錯誤說明集中在「注意事項」段，未接回對應操作步驟。

#### [CONTENT_THIN] 共用六段模板造成實作深度不足

- 19 頁高度重複「情境 → 核心要點 → 範例演練 → 完整擴充變體 → 注意事項 → 延伸應用」。
- 結構一致本身不是問題，但多數頁的「核心要點」都是 3 條原則；「延伸應用」常以模板或提示詞收尾，沒有驗證學員真的產出。
- 修復時應保留案例內容，將實作頁重心改成 Demo / Together / Solo / Check，而不是再補背景文案。

#### [STALE_UI] 平台 metadata 過舊或不完整

- 19 個單元頁：`data-platform-version="2026-04-v3"`。
- 19 個單元頁：缺 `data-built-at`。
- `index.html`：`data-platform-version="2026-06-v4"`、`data-built-at="2026-06-15"`。
- 建議先跑 `course-refresh office-ai`，再決定哪些登入、按鈕、上傳或匯出步驟需要重查。

#### [VALIDATION] 缺教案與真跑證據

- `_lessons/office-ai/` 不存在，無法確認 lesson type、案例輸入、預期輸出、試跑包與講師筆記。
- 本輪只做靜態掃描，未驗證 Gemini、NotebookLM、Google 文件或 Google 簡報目前介面與輸出。

### MINOR

#### [TYPOGRAPHY] 19 個單元頁使用非 V4 字階

- lint 每頁均回報 `.68rem`、`.73rem`、`.76rem` 等 6 個非白名單值。
- 應在 Learner Path 修復後統一處理，避免內容重構與 CSS 修補互相干擾。

#### [VOICE] 3 頁使用「您」

- `ch2/CH2-1.html`：6 處。
- `ch5/CH5-3.html`：2 處。
- `ch6/CH6-1.html`：2 處。

## Page Triage

| 頁面群 | 初步類型 | 主要問題 | 優先級 |
|---|---|---|---|
| CH1-1、CH1-2、CH6-2、CH6-3 | concept 候選 | 缺可辨識學習產物、2–4 題有判準的短練習 | BLOCKER（待 plan 確認類型） |
| CH1-3、CH1-4、CH2-1、CH2-2 | skill-operation | 只有 3–4 條概念/操作摘要，缺最短可跑路徑與 checkpoint | BLOCKER |
| CH2-3、CH3-1～CH3-3 | skill-operation / flagship | 有真跑案例，但缺學員逐步重做與 Solo / Check | BLOCKER |
| CH4-1～CH4-3 | skill-operation | 有示範，缺從大綱到內容/配圖的連續產物與檢核 | BLOCKER |
| CH5-1～CH5-3 | skill-operation | 方法與案例存在，缺完整操作鏈；平台步驟需 refresh | BLOCKER |
| CH6-1 | skill-operation | 有流程概念，缺學員完成一份可保存 workflow 模板的逐步路徑 | BLOCKER |
| index.html | course index | lint 乾淨；本輪未發現 Learner Path blocker | PASS（scan scope） |

## Lint Evidence

執行：

```bash
cd "$BASE" && python3 docs/lint-page.py courses/office-ai/
```

結果：

- 掃描：20 頁
- BLOCKER：0
- ERROR：0
- WARN：41
- WARN 組成：19 頁缺 `data-built-at`；19 頁使用非 V4 字階；另有 3 頁共 10 處「您」。

逐頁 `--summary` 亦全部 exit 0；這只代表通過機器 lint，不代表通過 Learner Action Contract。

## Metadata Evidence

執行：

```bash
grep -R 'data-platform-version=' courses/office-ai
grep -R 'data-built-at=' courses/office-ai
```

結果：

- 20 頁皆有 `data-platform-version`。
- 僅 `index.html` 有 `data-built-at`。
- 單元頁版本全部停在 `2026-04-v3`。

## Recommended Next Command

先執行：

```bash
/course-repair office-ai plan
```

Plan 應先確認每頁 lesson type，分批排序：

1. flagship 操作頁：`CH2-3`、`CH3-1`、`CH3-2`、`CH5-2`
2. 其餘操作頁：`CH1-3`、`CH1-4`、`CH2-1`、`CH2-2`、`CH3-3`、章四、`CH5-1`、`CH5-3`、`CH6-1`
3. concept 候選頁：`CH1-1`、`CH1-2`、`CH6-2`、`CH6-3`
4. refresh / typography / metadata / ops

進入任何 `fix` 前，必須先建立本次 scope 的 backup 與可驗證 restore script。
