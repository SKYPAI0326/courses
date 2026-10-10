# Make 人工重建與失敗恢復指南

這條流程已在教學工作區用虛構資料跑過 T01–T07。可參考[去識別的實跑 Blueprint](reference-make-blueprint.json)；匯入後仍須選自己的 Google 連線、填自己的試算表 ID，並在自己的工作區重新測試。Scenario 排程先維持停用，沒有寄信模組。

## 先完成一筆新列到一筆紀錄

1. 依[表格配置](part5-sheet-layout.md)建立四個分頁及表頭。先把已覆核示例 CSV 的第一筆「小林／詢問方案」各放一份到 `Source`、`ReviewedQueue` 第 2 列，九欄各放一格，其他資料列先不貼。中途不留空列。
2. Make 建立 Scenario，第一模組選 Google Sheets → Watch New Rows；選 `ReviewedQueue`、標題列 `A1:I1`、Limit `1`。首次測既有列時，Choose where to start 選 All；下次正式收新資料時依課堂起點重設，避免把舊資料當新資料。
3. 接 Google Sheets → Add a Row，寫到 `ProcessingLog`。先按 Run once，確認一筆新列確實寫成一筆紀錄，再加其他條件。

## 加覆核、防重與四路分流

4. 先依[階段指南 S1→S2](part5-stage-handoff.html#s1-to-s2)改接：Router 插在 Watch New Rows 與既有 Add a Row 中間，原寫入成為 inquiry 分支。接著設定下方覆核 Filter，再建立其餘三路。未覆核或錯分類應在 Filter 停住，紀錄表不得新增。

<a id="review-filter"></a>
### 覆核 Filter：逐欄填入設定

點 **Watch New Rows→Router 的連線**，Filter 命名「已覆核且九欄完整」。左欄從 Watch New Rows 輸出選欄位，右欄填下表原值；欄位若未出現，先回 S1 確認已讀到表頭及一筆資料。`Matches pattern` 是用字元樣式檢查文字，本課可直接複製指定樣式，不需自行寫程式。

新增條件時全部用 **AND（全部符合）**。分類的四個可用值已合在一條樣式裡，不另外建立 OR 分組。運算子使用 Text operators 下的 Equal to 或 Matches pattern；顯示名稱若因語系不同，先確認其類型及意義再填。

| 左欄：Watch New Rows 欄位 | 運算子 | 右欄：直接填入 | 核對意思 |
|---|---|---|---|
| submitted_at | Text: Matches pattern | `.+` | 至少有文字 |
| name | Text: Matches pattern | `.+` | 至少有文字 |
| email | Text: Matches pattern | `^[^@\s]+@[^@\s]+\.[^@\s]+$` | 基本格式須有 @ 與網域點號，不能有空白 |
| subject | Text: Matches pattern | `.+` | 至少有文字 |
| message | Text: Matches pattern | `.+` | 至少有文字 |
| category | Text: Matches pattern | `^(inquiry\|complaint\|partnership\|other)$` | 完整符合其中一個固定分類 |
| summary | Text: Matches pattern | `.+` | 至少有文字 |
| next_action | Text: Matches pattern | `.+` | 至少有文字 |
| review_status | Text: Equal to | `已覆核` | 人已核准進入流程 |

複製樣式時不加斜線包住、不加引號。category 樣式中的 `|` 表示任一選項；右值應是 `^(inquiry|complaint|partnership|other)$`。九條任一失敗便停止。`.+` 只檢查有文字，純空白或無意義內容仍須人工覆核退回；email 的基本格式檢查也不代表信箱存在或已獲收信同意。

下面兩種 Filter 分開設定：上述九條放在 Router **之前**；Router 後四條連線各只有一個分類條件。

| Router 後的連線 | 左欄 | 運算子 | 右欄 | Add a Row 的 route／draft_status |
|---|---|---|---|---|
| 到業務紀錄 | Watch New Rows 的 category | Text: Equal to | `inquiry` | 業務／待建立 |
| 到客服紀錄 | 同上 | Text: Equal to | `complaint` | 客服／不需要 |
| 到合作紀錄 | 同上 | Text: Equal to | `partnership` | 合作／待建立 |
| 到待處理紀錄 | 同上 | Text: Equal to | `other` | 待處理／不需要 |

先記下 ProcessingLog 筆數，再逐筆追加[完整測試列](part5-test-inputs.csv)中的 T01–T04；去掉第一欄 test_case 後才貼九欄資料。每次只應新增一筆對應路徑。S2 尚未接 Drafts，所以詢問／合作只有「待建立」，Drafts 不增加。T05a 的待覆核、T05b 的 unknown 僅在停排程的隔離教學副本測試，兩者都應在 Router 前停止。若有新紀錄，檢查九條是否全用 AND，以及是否仍留著 Router 前的 Add a Row。

### 查重：CH5-3 才加入

5. 以 `submitted_at|小寫且去前後空白的 email|去前後空白的 subject` 組成 `source_key`。接 Google Sheets → Make an API Call，GET `spreadsheets/你的試算表ID/values/ProcessingLog!A1:A1000`。API 回傳的 `body.values` 是陣列；在 Router 前設 Filter，檢查 `flatten(4.body.values)` **不包含**目前的 `source_key`。教學版一次處理一列並開啟 Sequential processing；若多人同時寫入或表格超過 1000 列，需重新設計防重，不能把此範例當成並行保證。

<a id="duplicate-filter"></a>
從 S2 接續時，先按[階段指南 S2→S3](part5-stage-handoff.html#s2-to-s3)把讀取模組插入 Watch New Rows 與 Router 之間。先前的覆核 Filter 放在 **Watch New Rows→Make an API Call**，下表的新防重 Filter 放在 **Make an API Call→Router**。四條分類 Filter 保留在各分支。只有前兩個檢查都通過才會走入任何寫入模組。

新模組的 URL 欄填上方 `spreadsheets/...` 路徑，將「你的試算表ID」替換為 Google Sheets 網址 `/d/` 與 `/edit` 之間那段；Method 選 GET，不另外寫一份獨立 API 程式。使用同一個 Google 連線。保存後右鍵點這個讀取模組，選 Run this module（部分介面顯示 Run this module only），只測這個 GET 讀取。此時先不要按整條 Scenario 的 Run once，以免在防重與草稿尚未接好前消耗測試列或寫入紀錄。打開讀取模組上方的輸出泡泡，確認 `body → values` 能看到 ProcessingLog A 欄；若 403 或找不到表，先回連線、試算表 ID 或分頁名修復。

| 防重 Filter 的位置 | 填入內容 |
|---|---|
| 名稱 | 來源鍵未出現 |
| 左值 | 在函數選擇中選 `flatten`，括號內映射剛才讀取模組的 `body → values` 陣列；不要貼整段 JSON 文字 |
| 運算子 | **Array operators: Does not contain（陣列不包含）**；不選文字搜尋的同名選項 |
| 右值 | 映射 Watch New Rows 的提交時間，輸入分隔字元 `|`，再接 `lower(trim(email))`、另一個 `|`、`trim(subject)`；完整範例如下 |

左值若讀取模組編號為 4，會是 `flatten(4.body.values)`；不是 4 時，從自己的模組輸出選取 values。下面來源鍵的 1 同樣是 Watch New Rows 的範例編號。

看不懂 `flatten` 時，先把它想成「把紀錄表 A 欄的已處理鍵攤平成一張名單」。新鍵已在名單上，就停在這裡。實跑 Blueprint 的來源鍵映射如下：

```text
{{1.`0`}}|{{lower(trim(1.`2`))}}|{{trim(1.`3`)}}
```

`1.0` 是提交時間、`1.2` 是 email、`1.3` 是主旨。手動新建模組時編號可能不同，應從 Make 的欄位選單點選欄位，不直接照抄數字。

`trim` 去頭尾空白，`lower` 將 email 轉小寫。先在右值按序插入三個來源欄位，email 套入 trim 再套 lower，subject 套 trim，兩個 `|` 是分隔文字。要看到欄位／函數映射，不是把「email」當固定字串。ProcessingLog 的 source_key 也使用完全相同組合。

防重核對示例：若表內 A 欄已經有 `2026-10-09T09:00|learner@example.com|詢問方案`，flatten 之後它仍是一個完整名單項目；再送相同鍵，Does not contain 為否，應停止。若送的是下列新測試列，第一次應通過；寫入後把完全相同九欄再追加一次，第二次應停止，不改時間繞過測試。

```csv
submitted_at,name,email,subject,message,category,summary,next_action,review_status
2026-10-11T11:00,小林,learner@example.com,S3查重驗證,請問基礎方案月費,inquiry,詢問基礎方案,建立未寄出教學草稿,已覆核
```

使用前先在 ProcessingLog A 欄搜尋完整新鍵 `2026-10-11T11:00|learner@example.com|S3查重驗證`，確認尚不存在；若已練過，保留舊證據，在空白教學副本測同一組資料。完成下列草稿與回寫後，再驗「第一次新增一筆紀錄與草稿、第二次兩張表均不增加」。表內的 `source_key` 表頭也是讀取結果之一，因不等於完整測試鍵，不會誤擋本例。

6. S2 已建立的四條 Router 分支直接核對，不重複新增；每路各自檢查一個 category。每路的 Add a Row 都寫 `source_key,category,route,status,draft_status,error` 到 `ProcessingLog`。詢問與合作的初始 `draft_status=待建立`；客服與其他為 `不需要`。`status=已記錄`。
7. 詢問與合作分支再用 Add a Row 寫 `Drafts`：`recipient` 只放虛構測試信箱，`status=未寄出`；內容留「人工查核」提醒。成功後以 Google Sheets → Update a Cell，把剛才紀錄列的 E 欄改成 `已建立`，例如業務路徑的 Cell 填 `E{{2.rowNumber}}`。客服與其他不建立草稿，也不接寄信模組。

`ProcessingLog` 的 A–F 欄依序填來源鍵、分類、路徑、`已記錄`、草稿狀態、錯誤文字。`Drafts` 的 A–E 欄依序填來源鍵、虛構收件地址、主旨、草稿本文、`未寄出`。寫完一筆後，先到表格確認值，再看 Make 畫面上的綠勾；只有綠勾但欄位放錯，仍要回到映射修正。

## 七案測試與恢復

8. 依[T01–T07 案例](part5-test-cases.csv)每次追加一筆測試新列，逐案核對輸入、執行紀錄、`ProcessingLog` 與 `Drafts`。T06 用同一來源鍵再提交，兩張輸出表都不得新增。
9. T07 在停用排程的教學 Scenario 中，暫時把詢問路的 Drafts 目標表改為不存在的測試表名，再追加一筆虛構詢問。確認 `ProcessingLog` 留一筆 `待建立`、Drafts 無該鍵，Make 出現未完成執行。開啟 Incomplete executions 該筆 Details，在失敗執行的模組內修回 `Drafts`、Save，再按 Run once；主流程也恢復正確目標供未來使用。這會從草稿寫入與狀態回寫繼續。不要從 Watch New Rows 再跑整筆。
10. 恢復後檢查同一來源鍵只有一份 `未寄出` 草稿，`ProcessingLog` 仍只有一列且 `draft_status=已建立`，未完成執行狀態為 Resolved。本次教學工作區 T07 由錯誤到恢復共重試兩個操作，沒有重寫上游紀錄。實際授課仍需用當天帳號與資料重做。

遇到寫入失敗先保留原始資料、確認最後成功節點，再查下游是否已留下結果。若草稿已存在，不應再執行會新增草稿的步驟。每次重跑前確認排程停用，處理完未完成執行再決定是否啟用。

[Make Google Sheets 模組說明](https://apps.make.com/google-sheets-modules)；[Make 陣列函數](https://help.make.com/array-functions)。

官方區分暫時錯誤 Retry 與設定錯誤手動修正，見 [Manage incomplete executions](https://help.make.com/manage-incomplete-executions)。

設定位置核對（2026-10-11）：[Filter](https://help.make.com/filtering)、[在兩個模組之間插入 Router](https://help.make.com/router)、[單獨測試模組](https://help.make.com/step-6-test-the-module)。
