# 課程素材

## CH1-1（4 模組基準）

- `CH1-1-reference-4module.sanitized.blueprint.json`：保留已驗證的 Sheets → Gemini → Docs → Email 結構；連線、檔案 ID 與收件人已去敏。
- `CH1-1-import-map.md`：匯入後重綁對照、位置鍵與無權限備援。
- `CH1-1-test-data.csv`：課堂練習資料。
- `CH1-1-expected-result.md`：`result` 內容核對重點。

本目錄只放可供課程使用的去敏資產；原始 Blueprint 不放入課程頁面，也不作為學員直接匯入檔。

## CH1-2（資料契約）

- `CH1-2-contract-input-template.md`：七欄輸入資料契約模板，含四個共同欄位與交接說明。
- `CH1-2-contract-output-template.md`：六欄 Gemini 輸出契約模板，含三個輸出欄位與型別驗收。
- `CH1-2-mapping-template.md`：六欄來源映射表模板，含測試通過／不通過紀錄與交接說明。

CH1-2 的講義會在第一次跟做前提供上述檔案連結；無法下載時，學員可依頁面上的欄位名稱建立同樣表格。

## CH1-3（最小流程）

- `CH1-3-module-cards.md`：Sheets、Gemini、Filter、Docs 四張模組卡，包含角色、輸入、輸出、通過條件與失敗出口。
- `CH1-3-test-data.csv`：一筆待人工確認與一筆一般回饋，欄位對應 CH1-2 輸入契約。
- `CH1-3-gemini-output-fixtures.json`：`needs_review=true`、`false` 與型別錯誤的固定輸出，供無連線練習。
- `CH1-3-run-log-template.md`：成功、待人工確認與型別錯誤的執行紀錄欄位。
- `CH1-3-test-cases-template.md`：三個測試案例與預期分流、文件結果。
- `CH1-3-offline-run-fixture.md`：沒有 Make 連線時，逐步重現固定輸入、Gemini 輸出、Filter 路由與 Docs 預期結果；所有紀錄標示 `SIMULATED`。

CH1-3 的模組卡與固定輸出是離線替代路徑，不宣稱可直接匯入 Make；有連線時，學員依模組卡在 Scenario 中逐項設定。

## CH1-4（LLM 協同設計）

- `CH1-4-requirement-brief.md`：不含敏感資料的需求描述與本次做／不做邊界。
- `CH1-4-prompt-template.md`：可直接貼入免費 LLM 的完整提示詞，含契約、限制、輸出格式與驗證要求。
- `CH1-4-workflow-spec-template.md`：模組、映射、控制／失敗出口、測試四張表。
- `CH1-4-prompt-log-template.md`：提示版本、回答摘要、人的修正與安全檢查。
- `CH1-4-review-checklist-template.md`：逐欄標記保留／修正／拒絕與事實依據。
- `CH1-4-llm-fixed-output.md`：無 LLM 帳號時使用的完整固定回答，內容不是 Make Blueprint。

CH1-4 的提示詞與固定輸出都不要求學員提供 Make token、真實帳號或個資；設計規格必須先經人審核，不能直接當成匯入檔。

## CH1-5（LLM 修改與除錯）

- `CH1-5-sanitized-blueprint.fixture.json`：保留 Filter 修正所需的模組與欄位結構；連線、ID 與個資已替換。這是教學 fixture，不宣稱可直接匯入 Make。
- `CH1-5-sanitization-checklist.md`：交給 LLM 前的秘密、個資、固定 ID 與結構檢查。
- `CH1-5-change-request-template.md`：限定單一主要變因、允許／禁止路徑與驗收條件。
- `CH1-5-test-cases.md`：false 成功、true 停止、文字型別錯誤三筆固定測試；依 `MAKE`／`SIMULATED` 模式填寫實際或模擬結果。
- `CH1-5-diff-log-template.md`：保存差異、人的判斷、測試證據、版本與還原方式。
- `CH1-5-llm-fixed-diff.md`：沒有 LLM 帳號時的固定回答備援，不代表執行成功。
- `CH1-5-prompt-template.md`：可直接複製的最小 diff Prompt，含允許／禁止路徑、測試與還原要求。

CH1-5 的素材先建立安全副本，再交給 LLM 產生最小 diff；不得把原始 Blueprint、credential、token 或真實資料貼入任何模型。

## CH1-6（變體專題與交接）

- `CH1-6-variant-choice.md`：批次彙整／Gmail 來源兩個變體選項，列出保持不變與必須重驗的範圍。
- `CH1-6-variant-spec-template.md`：變體需求、模組責任、欄位映射與 LLM 影響分析模板。
- `CH1-6-handoff-readme-template.md`：handoff-pack-v1 的目錄、執行模式、驗證順序與還原入口。
- `CH1-6-test-matrix.md`：成功、待人工、資料缺值三條路徑；依 `MAKE`／`SIMULATED` 模式填寫證據。
- `CH1-6-demo-record-template.md`：五分鐘展示腳本，先說明模式，再要求每段都有對應證據或明確標示尚未驗證。
- `CH1-6-fixed-output-fixtures.json`：無 Make 連線時的固定輸出與 placeholder；不是 Blueprint，也不代表實際執行成功。
- `CH1-6-batch-input.csv`：三筆去敏批次輸入，含 `record_id`、期間、契約欄位與審核旗標。
- `CH1-6-batch-module-cards.md`：資料集合、Iterator、Aggregator、Gemini、Filter、Docs 的責任與控制條件。
- `CH1-6-batch-intermediate-output.md`：逐筆檢查、聚合輸入與成功／待人工／缺值三條預期路徑。

CH1-6 的變體沿用前置契約與安全出口；正式原版不得覆寫，任何尚未在目標工作區執行的結果都必須標示為待驗證。
