# Repair Plan: ai-beginner-practical

## Scope

- slug：`ai-beginner-practical`
- pages：`module1.html`、`CH1-1.html`、`CH2-1.html`、`CH3-1.html`、`CH4-1.html`
- source-of-truth：`COURSE-OUTLINE.md`、`COURSE-BLUEPRINT.md`、`COVERAGE-LEDGER.md`
- process-state：`_gates.md`、`_plan.md`
- validation：`_validation/` 內本課專用 L0 生成器、測試與真值輸出
- assets：新增全課課後整合任務工作表
- 不包含：其他課程、既有視覺系統重排、資安單元、指定其他 LLM 平台、立即 push

## Risk

- near-term class：unknown
- backup required：yes
- external dependency：NotebookLM 的登入、來源匯入與引用介面需課前實機確認

## BLOCKER

### [VALIDATION] `_validation/L0-generate.py` 與真值表不存在

- 問題：第 4 單元冷氣共同素材有明確可核對的規格、價格與「未提供」欄位，但目前沒有由原始素材計算出的標準答案。
- 修法：新增可重跑的 Python 生成器、L0 JSON、可讀文字輸出與最小契約測試；包含產品數、價格差、能源效率／噪音／保固比較、共同房間條件、缺失欄位與三個人工確認問題。
- 驗證：先讓契約測試在生成器不存在時失敗，再新增生成器使測試通過；執行官方 L0。

## MAJOR

### [ENVIRONMENT] `CH3-1.html`

- 問題：頁面已有 NotebookLM 操作與備援，但第一個操作前沒有獨立的「課前實機確認」清單，講師仍需口頭補充帳號、來源匯入與引用狀態。
- 修法：在第一單元前加入 5 分鐘實機確認：能開啟、建立空白筆記本、加入一份課程純文字來源、看見來源名稱與回答引用；任一項失敗即保存工作表並走離線備援。補充介面不同時以功能名稱判斷，不依賴固定按鈕位置。
- 驗證：L4b 平台 sentinel；頁面 cold follow 能指出成功結果與備援路徑。

### [LEARNER_PATH] `module1.html`、四個 CH 頁與課程藍圖

- 問題：四個單元的內容完整，但 12 小時內的「必做」與「延伸」邊界沒有在課程入口統一呈現；零基礎學員可能把 30 張卡或全部延伸來源都當成課堂必做。
- 修法：入口加入全課最低完成線；每個單元頁補一個短版本單元完成線，明示核心成果與有時間才做的延伸。維持現有示範與練習，不刪除素材。
- 驗證：L5 persona 能在沒有講師口頭補充下說出每單元最低完成物。

### [VALIDATION] `COVERAGE-LEDGER.md`

- 問題：目前只有 CH1-1 代表單元的完整原子與證據，CH2-CH4 的核心操作沒有同一份可追溯的 coverage 補充。
- 修法：保留 CH1 的 frozen ledger，新增 CH2-CH4 與課後整合任務的核心 atom、操作位置、完成物、驗證與修復對照。
- 驗證：每個新增 atom 都能指回 learner-facing HTML 的 section／stage ID，不把「已涵蓋」當成沒有位置的自述。

### [PROCESS] `_gates.md`、`_plan.md`

- 問題：內部狀態仍寫成「只完成 CH1」與「G4/G5 尚未開始」，與目前四頁已製作、已上線、L0/L1-L3 已執行的實際狀態不一致。
- 修法：更新為 G1/G2/G4 已完成、G3 條件通過、G5 進行中；明確記錄 L4a/L4b/L5 仍待安全授權或真人環境驗收。
- 驗證：狀態檔與 `_validation/status.jsonl` 的結果互相一致。

## MINOR

### [LEARNER_PATH] `module1.html` 與新增課後工作表

- 問題：四份單元成果尚未在課程結尾被整合成一次真實任務驗收。
- 修法：新增 20–30 分鐘的「課後整合任務」工作表；學員選一個真實需求，保存背景、任務、限制、輸出格式、第一版、一次修訂與人工確認欄位。此任務作為課後延伸，不增加四個三小時單元的核心負擔。
- 驗證：工作表能單獨開啟；入口連結存在；學員可依四份既有成果完成一份可重做交付物。

### [TECH_LINT] 共用密碼閘門

- 問題：4 個內容頁各有 1 個非 V4 字型警告（`.76rem`、`1.35rem`），來源是注入的 gate CSS。
- 修法：本輪不改課程正文；記錄為共用閘門樣式的後續維運項，避免把全站 gate 改動混入本課修復。
- 驗證：修補後確認仍為 0 BLOCKER、0 ERROR；WARN 數量若未變，需在報告中說明來源。

## Validation Process Gap

專案預期位置缺少 `_規範/course-content-substance.md`、`_規範/learner-action-contract.md` 與 `audit-course-substance.py`，因此本輪可以執行課程專用的靜態與 L0 檢查，但不能把內容實質審查宣稱為完整自動化通過。這項缺口記錄於報告，不在本輪複製未知的規範檔。

## Execution Order

1. 建立本輪 scope 備份與還原腳本。
2. 新增 L0 契約測試並先確認它會因生成器不存在而失敗。
3. 新增 L0 生成器與真值輸出，讓契約測試通過。
4. 修補 NotebookLM 課前實機確認與四頁／入口的核心完成線。
5. 新增課後整合工作表與入口連結。
6. 重跑 lint、連結、搜尋索引、validator preflight、L0、L1-L3。
7. 產出本輪 `REPAIR-REPORT.md`；L4a、L4b、L5 若需外部帳號或真人跟做，保留真實 pending 狀態。
