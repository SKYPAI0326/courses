# Repair Plan：ai-beginner-practical

## Scope

- slug：`ai-beginner-practical`
- pages：`index.html`、`module1.html`、`CH1-1.html`、`CH2-1.html`、`CH3-1.html`、`CH4-1.html`
- assets：`assets/fallback/unit3-notebooklm-text-fallback.md`、`assets/worksheets/course-capstone-handoff.md`、新增通用啟動卡
- 不修改：課程密碼 hash、外部平台清單、既有 lesson plan 原始內容

## Risk

- 近期待上課：unknown
- backup required：yes
- 真實 NotebookLM 引用：本輪不偽造，保留為 L4b pending

## BLOCKER

### [LEARNER_PATH] 入口與工具起始環境

- 問題：新手看到 gate 或「開啟文字型 LLM」時，不知道授權從哪裡來、畫面要找什麼、工具不可用時停在哪裡。
- 修法：更新 gate 提示為課程提供者授權；新增 `text-llm-minimum-start.md`；在 CH1、CH2、CH4 第一次操作前加入 `environment-contract`；在 CH3 加入 NotebookLM 準備與正式引用界線。
- 驗證：cold-follow contract、所有頁面出現環境契約、資產連結存在。

### [CONTENT_SUBSTANCE] 完整 worked examples

- 問題：CH1 修訂、CH2 訊息／自介、CH4 購物／行程的完整輸入到結果不足。
- 修法：只使用頁面與既有素材中的條件，補完整前後輸出、差異理由、保留條件與待確認事項；不宣稱 NotebookLM 實機引用。
- 驗證：契約測試、逐頁 reviewer、cold follow-along。

### [ARTIFACT_CHAIN] 課後整合

- 問題：四份上游完成物沒有明確欄位契約與回修路徑。
- 修法：在工作表中加入 CH1–CH4 完成物表、必取欄位、替換規則、完成標準、回修位置與工具不可用的待重跑標記。
- 驗證：整合工作表自足閱讀與連結檢查。

## MAJOR

### [RECOVERY] CH3 純文字備援規格

- 問題：摘要輸出規格與正式路徑不一致。
- 修法：統一為一句話、約 200 字、約 300–350 字；明確寫出純文字備援沒有 NotebookLM 正式點擊引用，恢復後從相同提示詞重跑。
- 驗證：不得再出現「約 500 字」。

### [NAV_OPS] 課程終點導航

- 問題：CH4 頁尾只回到 module，沒有直接落到課後整合。
- 修法：新增課後整合連結，保留返回課程單元。
- 驗證：local links／anchor check。

## Execution Order

1. 建立本輪 backup 與 restore script。
2. 先補測試契約需要的共用啟動卡與環境契約。
3. 補四頁核心 worked examples 與 CH3 fallback。
4. 重建課後整合工作表與 CH4 終點導航。
5. 跑契約測試、lint、manifest、連結與官方 preflight／L1-L3。
6. 重新派遣三 persona 模擬學員；若仍指出同一 upstream 缺口，再回修對應角色，不直接改 Gate 為 PASS。

