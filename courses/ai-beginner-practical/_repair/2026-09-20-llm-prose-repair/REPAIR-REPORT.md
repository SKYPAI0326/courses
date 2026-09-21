# LLM 慣用文案修正報告

## 結論

四個學員頁面的公式化對比句已完成修正。修正後，頁面文字不再使用「不是 X，而是 Y」「不只 X，而是 Y」作為主要說明套路；內容改成直接交代學員行動、判斷依據與可觀察結果。

## 修改範圍

- `CH1-1.html`：課程目的、錯誤診斷、單一變因比較、任務轉用與完成檢查。
- `CH2-1.html`：提示詞定義、課堂節奏、錯例判斷、讀者轉換與完成物驗收。
- `CH3-1.html`：來源判讀、主張台帳、三類閱讀產物與交付條件。
- `CH4-1.html`：決策卡、旅遊示範、條件敏感性比較、缺資料、取捨與完成檢查。

只改學員看得到的文字節點。保留 HTML 結構、class、錨點、連結、工作台欄位、提示詞原文、操作順序、checkpoint、回復位置與匯出檔名。

## 修正方式

1. 將「不是……而是……」改為直接說明要檢查什麼、怎麼判斷、完成後應留下什麼。
2. 將「不只……」改為具體列出必要的完成條件，避免讓學員只記住抽象對比。
3. 保留必要的功能性界線，例如「引用是查證入口，不是品質保證」與「文字是否漂亮不是驗收條件」；這些句子直接阻止錯誤判讀，具有教學功能。
4. 保留錯例、數字、資料邊界、待確認狀態與人工判斷位置，沒有用文案修整掩蓋課程風險。

## 驗證結果

- 四頁 HTML parser：PASS。
- 四頁 copy continuity audit：0 warning；工具要求人工 review。
- 公式化對比句掃描：四頁皆 0 筆。
- `test_cold_follow_contract.py`：PASS。
- `test_semantic_dedup_contract.py`：PASS。
- `test_all_workbenches_contract.py`：PASS。
- `test_dedup_learning_contract.py`：PASS。
- `test_full_course_repartition_contract.py`：PASS。
- `test_unit1_expansion_contract.py`：PASS。
- `test_ui_practicality_contract.py`：PASS。
- `test_workbench_contract.py`：PASS。
- 全站 `lint-page.py --all --summary`：0 BLOCKER、0 ERROR、2790 WARN。
- 搜尋索引已更新：`search-index.json`，949 筆。
- `git diff --check`：PASS。

## 回復

修正前備份：`_backup/2026-09-20-pre-llm-prose-repair/`

回復腳本：`_tools/restore-2026-09-20-pre-llm-prose-repair.sh`
