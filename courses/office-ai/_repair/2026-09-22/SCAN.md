# Course Repair Scan: office-ai

**掃描日期**：2026-09-22  
**模式**：`scan -> reconstruct -> repair -> validate`
**範圍**：`courses/office-ai/` 的 20 個 HTML（19 個單元頁 + 1 個總覽頁）  
**大綱**：`_outlines/office-ai.md`  
**正式教案**：已建立 `_lessons/office-ai/`（19 個來源，標記為 legacy-reconstructed-draft）
**Style Guide**：已建立 `_outlines/office-ai.style-guide.md`

## 結論

現有 HTML 已經過 2026-07-15 的舊修復，操作型頁面大多已有起始狀態、完成物、步驟、快速檢查與卡關修復。這次不能把它當成未修復課程重新灌內容；本輪先確認新規則需要的來源、證據與真人驗證是否存在。

初始掃描時正式課程驗證為 BLOCKED；本輪補齊來源與 evidence 後，現在的判定是：**機器檢查可交接，但仍待真人驗證**。

## BLOCKER

### [VALIDATION] 初始掃描發現正式來源與證據交接缺口（已處理）

- 初始掃描時 `_lessons/office-ai/` 與 `_validation/evidence.json` 均不存在。
- 現已建立 19 份來源、19 份 content review、19 份 fidelity review、1 份 technical review 與 `evidence.json`。
- 來源明確標記 `legacy-reconstructed-draft`，不把來源重建誤稱為獨立審查或真人通過。
- 仍需獨立 reviewer 與真人 cold follow-along 才能解除 pending。

## MAJOR

### [LEARNER_PATH] 四個概念候選頁缺少明示的起始狀態與 checkpoint

受影響頁面：

- `ch1/CH1-1.html`
- `ch1/CH1-2.html`
- `ch6/CH6-2.html`
- `ch6/CH6-3.html`

這些頁面有產出物與練習，但目前使用「產出物」或「結訓產出物」標籤，沒有在第一個學員動作前明確說出起始材料、第一個動作、完成物用途與失敗時回到哪裡。需先由正式正文審查判斷是否為概念型適用例；若適用，補成決策矩陣／分類結果／短 rationale 的完整任務契約，不增加沒有教學價值的步數。

### [PLATFORM / VALIDATION] 平台實跑證據不足

- 19 個單元頁的 `data-platform-version` 都是 `2026-04-v3`，`data-built-at` 都是 `2026-07-15`。
- 以 2026-09-22 計算，頁面老化 69 天；依 `course-refresh` 的時間規則屬 `OK`，但這只代表尚未超過 90 天，不代表 Google 文件、通用 LLM 或 NotebookLM 的實際路徑已重跑。
- `CH5-1` 的 Google 文件語音輸入仍需在指定帳號、瀏覽器與權限條件下實測；其他平台文字也要依課程實際承諾標記適用或不適用。

## MINOR

### [TECH_LINT] 舊課視覺警告 21 條

執行 `python3 docs/lint-page.py courses/office-ai/ --summary --by-bucket`：

- BLOCKER：0
- ERROR：0
- WARN：21
- `migration-debt`：19 頁使用 V4 字階外的 `.76rem`、`1.35rem`
- `motion`：2 頁有 hover 同時變化超過 2 個屬性

這些問題不阻擋本輪內容來源整理；正式正文與證據建立後，再由 typography fixer 或小範圍 CSS 修補處理。

## 技術與素材證據

- HTML：20 頁；單元頁 19 頁。
- `lint-page.py`：0 BLOCKER、0 ERROR、21 WARN。
- 相對連結：117；斷鏈：0。
- 頁面引用的本地資產連結：12；缺失：0。
- 密碼 gate：20 / 20 頁均存在。
- `audit-course-substance.py`：目前可做機器頁面檢查；抽查頁面皆為 `MACHINE_CHECKED`，語意審查仍 `PENDING`。

## Activity Identity Audit

目前 HTML 已能辨識多數活動角色，例如：

- `CH1-4`：Together 建立背景／要求／格式，Check 做人工核對，Solo 改寫成請假交接。
- `CH2-3`：控制版、Repair、人工驗證後，再轉移到議價情境。
- `CH3-2`：先保留疑似重複列計算，再由學員判斷去重並比較兩個公式總額。
- `CH5-1`：Together 轉錄與權限檢查，Check 對原音核對，Solo 自行朗讀新句子再校對。

這些是 HTML 層的初步觀察，尚未綁定正式正文、素材 hash 或獨立 reviewer，因此暫不視為通過證據。

## Shared Copy Audit

移除 `style`、`script` 與導航後，19 個單元頁的教學段落、步驟、檢查與產出說明沒有發現跨頁完整重複段落。章節返回導覽文字的重複屬允許的導航文案。

## 既有修復紀錄

`_repair/2026-07-15/REPAIR-REPORT.md` 已記錄上一輪 0 lint、0 斷鏈與條件式通過，但它沒有正式 `_lessons` source、`evidence.json` 或真人測試紀錄；本輪不沿用其 PASS，只把它當作背景與可回查歷史。

## 本輪已執行結果

1. 建立本輪 backup 與 restore script，保留 2026-07-15 舊備份。
2. 從現有 learner-facing HTML 重建 19 個可追溯 Markdown source，保留輸入、判斷、完成物、檢查、修復與素材引用。
3. 建立並套用 `office-ai.style-guide.md`，統一主詞、動作、對象、條件、結果與平台誠實標記。
4. 為 `CH1-1`、`CH1-2`、`CH6-2`、`CH6-3` 補上概念型任務契約，並同步 source 與 HTML。
5. 建立 `_review/` 與 `_validation/evidence.json`，執行 validator：`MACHINE_READY_PENDING_HUMAN`，錯誤 0。
6. 以 learner-only context 執行兩階段 `independent-ai` 模擬：19 個 stage-1 logs、9 個 stage-2 logs；結果只用於人工分流，沒有解除真人／平台／sequence pending。

## 下一步

1. 由獨立 reviewer 逐單元複核內容充分性、語句主詞受詞、重複與完成物用途。
2. 實跑 `CH1-2` NotebookLM 與 `CH5-1` 語音輸入等明示平台路徑，記錄帳號／權限／版本／結果。
3. 執行入口、完整跟做、理解、遷移與三課 sequence 驗證，逐筆回填 evidence。
4. 視需要處理 21 條既有 lint migration-debt 警告，完成瀏覽器 fidelity 檢查。
