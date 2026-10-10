# Make 人工重建與失敗恢復指南

這條流程已在教學工作區用虛構資料跑過 T01–T07。可參考[去識別的實跑 Blueprint](reference-make-blueprint.json)；匯入後仍須選自己的 Google 連線、填自己的試算表 ID，並在自己的工作區重新測試。Scenario 排程先維持停用，沒有寄信模組。

## 先完成一筆新列到一筆紀錄

1. 依[表格配置](part5-sheet-layout.md)建立四個分頁及表頭。`ReviewedQueue` 第一筆測試資料放第 2 列，中途不留空列。
2. Make 建立 Scenario，第一模組選 Google Sheets → Watch New Rows；選 `ReviewedQueue`、標題列 `A1:I1`、Limit `1`。首次測既有列時，Choose where to start 選 All；下次正式收新資料時依課堂起點重設，避免把舊資料當新資料。
3. 接 Google Sheets → Add a Row，寫到 `ProcessingLog`。先按 Run once，確認一筆新列確實寫成一筆紀錄，再加其他條件。

## 加覆核、防重與四路分流

4. Watch New Rows 後先設 Filter：`review_status = 已覆核`，九欄有值，email 符合基本格式，`category` 只允許 `inquiry`、`complaint`、`partnership`、`other`。未覆核或錯分類應在 Filter 停住，紀錄表不得新增。
5. 以 `submitted_at|小寫且去前後空白的 email|去前後空白的 subject` 組成 `source_key`。接 Google Sheets → Make an API Call，GET `spreadsheets/你的試算表ID/values/ProcessingLog!A1:A1000`。API 回傳的 `body.values` 是陣列；在 Router 前設 Filter，檢查 `flatten(4.body.values)` **不包含**目前的 `source_key`。教學版一次處理一列並開啟 Sequential processing；若多人同時寫入或表格超過 1000 列，需重新設計防重，不能把此範例當成並行保證。

看不懂 `flatten` 時，先把它想成「把紀錄表 A 欄的已處理鍵攤平成一張名單」。新鍵已在名單上，就停在這裡。實跑 Blueprint 的來源鍵映射如下：

```text
{{1.`0`}}|{{lower(trim(1.`2`))}}|{{trim(1.`3`)}}
```

`1.0` 是提交時間、`1.2` 是 email、`1.3` 是主旨。手動新建模組時編號可能不同，應從 Make 的欄位選單點選欄位，不直接照抄數字。
6. Router 建四條路，各自檢查一個 category。每路的 Add a Row 都寫 `source_key,category,route,status,draft_status,error` 到 `ProcessingLog`。詢問與合作的初始 `draft_status=待建立`；客服與其他為 `不需要`。`status=已記錄`。
7. 詢問與合作分支再用 Add a Row 寫 `Drafts`：`recipient` 只放虛構測試信箱，`status=未寄出`；內容留「人工查核」提醒。成功後以 Google Sheets → Update a Cell，把剛才紀錄列的 E 欄改成 `已建立`，例如業務路徑的 Cell 填 `E{{2.rowNumber}}`。客服與其他不建立草稿，也不接寄信模組。

`ProcessingLog` 的 A–F 欄依序填來源鍵、分類、路徑、`已記錄`、草稿狀態、錯誤文字。`Drafts` 的 A–E 欄依序填來源鍵、虛構收件地址、主旨、草稿本文、`未寄出`。寫完一筆後，先到表格確認值，再看 Make 畫面上的綠勾；只有綠勾但欄位放錯，仍要回到映射修正。

## 七案測試與恢復

8. 依[T01–T07 案例](part5-test-cases.csv)每次追加一筆測試新列，逐案核對輸入、執行紀錄、`ProcessingLog` 與 `Drafts`。T06 用同一來源鍵再提交，兩張輸出表都不得新增。
9. T07 在停用排程的教學 Scenario 中，暫時把詢問路的 Drafts 目標表改為不存在的測試表名，再追加一筆虛構詢問。確認 `ProcessingLog` 留一筆 `待建立`、Drafts 無該鍵，Make 出現未完成執行。開啟 Incomplete executions 該筆 Details，在失敗執行的模組內修回 `Drafts`、Save，再按 Run once；主流程也恢復正確目標供未來使用。這會從草稿寫入與狀態回寫繼續。不要從 Watch New Rows 再跑整筆。
10. 恢復後檢查同一來源鍵只有一份 `未寄出` 草稿，`ProcessingLog` 仍只有一列且 `draft_status=已建立`，未完成執行狀態為 Resolved。本次教學工作區 T07 由錯誤到恢復共重試兩個操作，沒有重寫上游紀錄。實際授課仍需用當天帳號與資料重做。

遇到寫入失敗先保留原始資料、確認最後成功節點，再查下游是否已留下結果。若草稿已存在，不應再執行會新增草稿的步驟。每次重跑前確認排程停用，處理完未完成執行再決定是否啟用。

[Make Google Sheets 模組說明](https://apps.make.com/google-sheets-modules)；[Make 陣列函數](https://help.make.com/array-functions)。

官方區分暫時錯誤 Retry 與設定錯誤手動修正，見 [Manage incomplete executions](https://help.make.com/manage-incomplete-executions)。
