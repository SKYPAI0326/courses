# Repair Plan：CH1-1 網頁實務工作台

日期：2026-09-18
狀態：已獲使用者以「進行修正」核准設計後執行

## 問題判定

CH1-1 的學習成果需要保留「提示詞 → 回答 → 判斷 → 修改」的可回看證據，但不需要學員下載 Markdown、複製整份文字表格、另開編輯器再回到 LLM。現行 U1-START 把檔案格式操作放在第一個 AI 動作之前，造成不必要的學習摩擦。

## 修法

1. 在 CH1-1 內置「第 1 單元實務工作台」，作為預設學習路徑。
2. 表單直接承接五題提示詞、回答貼上、觀察判斷、一次修改與個人轉移練習。
3. 使用瀏覽器 `localStorage` 暫存，讓學員可中斷後回到同一頁繼續；明示資料只留在目前瀏覽器，不是雲端同步。
4. 提供匯出 Markdown、列印與清除本機資料；Markdown 改為離線備援／交付格式，不再是起始材料。
5. 不指定其他 LLM 平台；學員仍從外部 LLM 複製回答貼回對應欄位，符合平台中立邊界。

## 會修改的檔案

- `CH1-1.html`
- `CH1-1-LESSON-PLAN.md`
- `COURSE-BLUEPRINT.md`
- `COVERAGE-LEDGER.md`
- `_validation/test_cold_follow_contract.py`
- `_validation/test_ui_practicality_contract.py`
- 新增 `_validation/test_workbench_contract.py`
- `../search-index.json`（重建）

## 不做的事情

- 不連接或自動讀取任何外部 LLM 對話內容。
- 不刪除原有五個案例、完整示範、檢核與離線備援。
- 不把表單資料上傳伺服器，不建立帳號或雲端同步功能。

## 驗收條件

- 第一個操作是「開始填寫」而非下載／複製 Markdown。
- 表單能覆蓋原工作表要求的五題、一次修改、個人三段紀錄與完成檢查。
- 可以重新整理頁面後恢復已填內容。
- 可以產出可交付的 Markdown，且列印版可讀。
- `lint-page.py`、course substance、cold-follow、UI practicality、workbench contract、連結與 L1–L3 全數重跑。
