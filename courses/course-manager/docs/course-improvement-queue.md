# 整課改善佇列控制器

新增的[統一執行入口](course-loop-runtime.md)負責模型呼叫與新 run 的明確啟用。下列舊 Gemini 佇列仍維持禁止派送，不能以新入口接管；本頁所述不呼叫模型是底層佇列的責任界線。

佇列依課程清單順序派出一張單章工作票，並檢查前章成果的相依版本。它沿用單章loop的判斷、用量與H3，不重新評分，不呼叫AI、不生成教材，也不覆蓋正式檔。

新建佇列可指定[review_policy](course-improvement-review.md)，派票會帶入角色及必要檢查，並拒絕以舊單章格式抵充覆核。單章checks／review期間仍屬in_progress，下游不放行；通過覆核後才可能成為H3暫定參照或complete。既有Gemini清單未遷移、仍不派送。

Gemini清單位於`operations/course-content-scoring/course-queue-gemini-ai/manifest.json`，固定為正式首頁的五個核心章`chapters/CH1.html`至`CH5.html`。14份延伸教材及案例遊樂園不納入改寫。先前part2/CH2-1的試驗保留，不能當成核心CH2已完成。

本次清單的`dispatch_enabled=false`；只初始化佇列，未授權派送。程式沒有解除這個限制的指令，不應手動更改JSON冒充新授權。未來若取得啟動授權，須另記工作邊界並處理啟用，不因本次實作完成就開始修課。

## 查詢與恢復

在course-manager執行：

```bash
python3 scripts/course_improvement_queue.py status --state operations/course-content-scoring/course-queue-gemini-ai/state.json
python3 scripts/course_improvement_queue.py resume --state operations/course-content-scoring/course-queue-gemini-ai/state.json
```

status／resume只讀，依最新的單章狀態顯示相依結果。清單中後章的dependency_blocked表示尚缺前章完成條件，底層可能仍為pending；不代表教材錯誤，也不是給低分。active是最後保存的工作票，dispatch會依單章最新狀態停放或沿用它。

## 章節順序與相依

| 章節 | 主題 | 必要承接 |
| --- | --- | --- |
| CH1 | 用白話做出第一個小工具 | 無前章依賴 |
| CH2 | 把需求寫成可重用的提示詞 | CH1的保存與完整工具交付方式 |
| CH3 | 製作能處理不同資料的工作工具 | CH2的需求與規則表達 |
| CH4 | 追加需求、修正問題並確認結果 | CH3的schedule-v2、兩組資料與測試基準 |
| CH5 | 保存、交付並套用到自己的工作 | CH4的schedule-v3與新規則；CH3的A／B舊備份及測試資料 |

清單同時固定來源路徑／SHA-256、章節用途、單章state位置及相依理由。檢查來源不等於評估章節。各章用量直接讀單章state；佇列沒有第二套可重置額度，也不能把同來源或既有試驗重複匯入。

已授權的佇列可用`dispatch --state FILE`取得最前面可工作的章節票。票含章節、來源、用途、單章state位置及上游版本，action為start_single_unit或resume_single_unit。它不建立單章state、不自動呼叫單章next；對話執行者依工作票啟動／接續單章loop。若同票仍在處理，重送dispatch回原票，不同時派第二章。

## 待補證與接續

章節等待補證、H1／H2或額度受限時，下一次dispatch會停放其票。依賴它的章節不能取得票；不依賴它、且在已授權範圍內的章節可依清單順序繼續。Gemini主線有連續依賴，因此前章若缺必要成果，可能使後續主線都等待；不為了讓佇列繼續而取消依賴。

已取得實際新證據時，由單章入口接收，不能直接把佇列狀態改成完成：

```bash
python3 scripts/course_improvement_loop.py supplement-evidence --state UNIT/state.json --evidence UNIT/evidence-map.json --expected-revision N
```

evidence-map是新證據識別碼到隔離目錄內新檔絕對路徑的JSON物件。只有waiting_evidence可補；使用者限制仍在則拒絕，禁止自行解除「暫不下載」。證據加入後重新派assess或compare，仍由AI判斷Q是否解決；不是一收到檔案就通過。候選、失敗歷史、既有H3與版本用量保留，補證評估不計為新候選或新的修稿失敗。若需要再改稿，仍受原兩版上限限制。

之後佇列再次dispatch，會優先選擇順序靠前且已可接續的章節。若另有正在執行的工作票，先完成／停放它，避免同時開兩章。resume本身不補證、不觸發模型，也不反覆索求材料。

## 人工確認與版本變動

- H1／H2阻擋相依下游；佇列不提供自行解除用途或取捨決策的入口。
- 只有單章主要原因是H3閱讀待確認，且相依列明允許暫定參照時，才可將該候選提供下游使用。工作票保存確切版本，並標示provisional。
- H3仍由已有confirm-h3入口依真實人工回饋登記，佇列不能代填。相同候選取得H3後，下游無須只因回饋紀錄增加而重寫。
- 上游來源、成果或已綁定的參照版本改變時，停下受影響章節及依賴它的後章，要求確認差異；不自動重綁、不把完成狀態沿用到新內容。其他無相依章節不因此被重新改寫。

各章完成後，課程狀態先為waiting_integration_review，不取平均分或直接宣布全課完成。有限的銜接檢查應對照前後章的產物、規則、版本相容性與必要連結，另存報告後用`confirm-integration --state FILE --evidence FILE --expected-revision N --actor NAME`登記。它會確認各章均complete，並綁定當時各章成果版本；程式不驗證報告語意，登記者須依實際檢查使用。若任一章未完成或相依阻塞，拒絕整課結案。此確認不包括發布或正式覆蓋。

## 實作與驗證界線

- [佇列控制器](../src/course_improvement_queue.py)、[CLI](../scripts/course_improvement_queue.py)、[佇列測試](../tests/test_course_improvement_queue.py)。
- 佇列狀態使用既有原子保存與鎖；重啟沿用active及bindings。正式來源與既有單章state只讀。
- `python3 -m unittest tests.test_course_improvement_loop tests.test_course_loop_stages tests.test_course_improvement_queue -q`驗證控制與接續；測試在暫存目錄建立合成單章結果，不代表五章內容已評估或改善。
- 本版沒有全課自動AI服務、平行代理、跨章自動改寫、授權擴充或自動發布。工作票與相依版本只是可靠的接續資訊，不能替代學員產物及操作證據。
