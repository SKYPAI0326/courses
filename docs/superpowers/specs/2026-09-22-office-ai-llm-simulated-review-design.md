# office-ai LLM 模擬學員檢視設計

**日期**：2026-09-22  
**狀態**：待使用者審閱  
**範圍**：`office-ai` 第一輪；後續可套用其他課程

## 問題與目標

目前 `office-ai` 已完成來源重建、HTML 修復與機器驗證，但 19 個單元仍缺真人入口、完整跟做、理解、遷移、平台實跑與三課 sequence 證據。使用者同時維護多條課程線，人力不足以先逐頁完整冷讀，因此需要一個能廣泛篩查、又不會把 AI 判斷冒充真人結果的流程。

本設計的目標是：

1. 讓 LLM 對全部 19 個單元執行一致的模擬學員檢視。
2. 讓第二個獨立 LLM 只處理第一輪疑點、高風險頁面與平台／sequence 頁面。
3. 將結果寫成 `independent-ai` evidence，與 `author-self-check`、`human` 分開。
4. 自動產生人工優先清單，讓使用者最後只處理高風險或低信心項目。
5. 保持 validator 的狀態語義：LLM 結果不能升格為 `LEARNER_READ`、`PLATFORM_VERIFIED` 或 `HUMAN_READY`。

## 不變的邊界

- 不修改 `course-validator` 對 `human` 的要求，也不把 LLM record 改寫成真人 record。
- 不以作者 source、既有 review 結論或 validator pending 清單作為模擬學員答案的提示。
- 不讓模擬流程自行修改課程 source、HTML 或素材；它只產生 review logs、evidence records 與 triage report。
- 不宣稱 LLM 能測量真實理解、動機、操作速度、平台權限或實際錯誤率。
- `CH1-2`、`CH5-1` 的外部平台實跑仍須真人或明確的實際平台 automation 證據。

## 方案與採用決策

採用 B + C 混合方案：

### 第一階段：全課 LLM simulated learner

對 19 個單元各執行一次 learner simulation。輸入只包含：

- learner-facing HTML 的可見正文與頁面順序；
- 該頁面實際可取得的學員素材；
- 課程大綱中的單元標題與必要的課型資訊。

輸出必須回答：

1. 30 秒入口六題：情境、重要性、第一份材料、完成物、用途／驗收、第一個動作／失敗回復。
2. 從第一個動作到完成物的可跟做路徑；不得用作者補充填空。
3. 完成物是否可觀察、可驗收、可再次使用。
4. 關鍵概念是否有輸入、判斷、結果、理由、錯誤與修復。
5. 同類任務的轉移情境是否能由頁面推導，而非只換名詞。

這一階段產生四類 `independent-ai` records：`entry`、`completion`、`understanding`、`transfer`。每筆 record 綁定當下 source、page 與 asset hash，並明示 `simulated_not_human: true`。

### 第二階段：獨立 AI adversarial review

第二個 prompt 不讀第一階段的完整推理，只讀第一階段的結論、疑點與實際 learner-facing 材料，專門挑戰：

- 是否把標籤、卡片或講師備註當成教學內容；
- 是否有主詞、動作、對象、條件或結果缺失；
- 是否只有列表，缺少輸入到完成物的因果鏈；
- 是否以相同 workflow 換案例名稱造成重複；
- 是否把平台假設、素材取得或完成物用途藏在頁外；
- 第一階段標記 PASS 時，是否有足以升級為 BLOCKER／MAJOR 的反例。

第二階段只對以下範圍執行：

- 第一階段產生 BLOCKER／MAJOR；
- `CH1-2`、`CH5-1` 平台頁；
- 大綱標為 flagship 的頁面；
- 一組連續三單元的 sequence；
- 第一階段信心低或缺少可觀察完成物的頁面。

輸出為 `independent-ai` 的 content／fidelity／platform／sequence review log，不得覆蓋真人證據。

## 證據格式

`evidence.json` 保持 schema version 1。新增 records 時沿用既有允許值：

- `actor: independent-ai`
- `verdict: PASS | FAIL | PENDING`
- layers：`entry`、`completion`、`understanding`、`transfer`、`content`、`fidelity`、`platform`、`sequence`

每筆紀錄至少包含：

- `unit_ids`；
- `log.path` 與 log hash；
- source、page 與該頁所有資產的 hash；
- `method`：模型、prompt 版本、輸入邊界、模擬規則；
- `observations`：學員會看到什麼、會做什麼、在哪裡卡住；
- `limitations`：明確列出不能由 LLM 證明的部分；
- `simulated_not_human: true`。

同一 `layer + unit_ids + actor` 的第二階段紀錄取代第一階段為現行結論，但舊 log 保留，方便稽核差異。

## Prompt contract

Prompt 必須固定以下規則：

1. 以第一次接觸主題的職場初學者身分閱讀；不能假設看過其他課或教師口頭說明。
2. 只能引用 learner-facing 頁面與可取得素材；不可讀內部設計、作者 review、validator report 或答案區以外的隱藏資料。
3. 先寫出「我會做的第一個動作」，再判斷頁面是否讓我看到預期結果；禁止把缺口自行補成合理版本。
4. 每個 PASS 都要有頁面位置、可觀察結果與完成物證據；找不到就 `PENDING` 或 `FAIL`。
5. 每個 FAIL 都要指出現象、造成的學習風險與最小修復方向；不得自行改檔。
6. 不可把「讀起來合理」寫成「真人會做到」；所有結果都帶有 simulated-not-human 限制。

## 人工分流

LLM 完成後產生 `AI-TRIAGE-REPORT.md`，依下列順序排序：

1. BLOCKER：學員無法開始、缺核心素材、無法產出或無法驗收。
2. MAJOR：核心判斷、完整示範、修復、轉移或語意鏈缺失。
3. 平台與權限：實際需要外部帳號、瀏覽器或麥克風。
4. Sequence：前課完成物未能成為後課輸入。
5. 低信心或兩個 LLM 結論不一致。

使用者最後可採風險式檢測：先檢查所有 BLOCKER／MAJOR，再檢查平台頁與一組 sequence，最後抽查 LLM 判定 PASS 的頁面。這會提高開發效率，但若要正式標記 `HUMAN_READY`，仍須補足規範要求的真人證據範圍。

## 失敗與重跑

- source、HTML 或資產修改後，所有受影響的 AI logs 失效；必須重新計算 hash 並重跑對應單元。
- prompt 版本變更時，新增 revision，不覆寫舊結論。
- LLM 無法讀取素材、遇到外部登入或無法判斷平台狀態時，寫 `PENDING`，不得推測 PASS。
- 若兩個 LLM 結論衝突，優先列為人工高風險項目，不以多數票自動通過。

## 驗收標準

本設計完成後，`office-ai` 應具備：

- 19 個第一階段 simulated learner records；
- 所有 BLOCKER／MAJOR 與指定高風險頁面的第二階段 adversarial records；
- 可追溯的 prompt revision、輸入邊界與 source／page／asset hash；
- 一份人工優先 triage report；
- validator 仍正確顯示真人／平台／sequence 的 pending，不因 AI records 錯誤升級。
