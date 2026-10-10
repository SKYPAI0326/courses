# Part5｜四課建置狀態與完整映射
每課用同一個教學 Scenario 接續，排程停用、Limit=1，僅處理虛構資料。保留每階段截圖與同鍵輸出。不能把教師過去成功紀錄當成自己的證據。

| 課程／階段 | 進入時已有 | 本課新增 | 離開前查表 |
|---|---|---|---|
| CH5-1 S1 | 四分頁與表頭 | 新列觸發→ProcessingLog | 一筆測試來源對一筆紀錄 |
| CH5-2 S2 | S1 成功 | 覆核 Filter、四路 Router | 四分類各一筆；待覆核／unknown 不寫出；草稿可仍空 |
| CH5-3 S3 | S2 成功 | 查重、Drafts、成功狀態回寫 | 新 inquiry 一筆草稿；完全相同鍵再送無新增 |
| CH5-4 S4 | S3 兩測通過 | 人工製造寫入失敗、定位與恢復 | 上游紀錄不重寫，同鍵至多一份草稿 |

<a id="s1-to-s2"></a>
## S1→S2：把原寫入移到分支，不在尾端一直加模組

先保存 S1，截圖保留兩個模組及設定。Make 排程維持停用。下面的「覆核」「分類」都是設在連線上的 Filter，不是額外的寫入模組。

```text
S1：Watch New Rows → 原 Add a Row（ProcessingLog，route=測試）

S2：Watch New Rows →〔覆核 Filter〕→ Router
     ├─〔category=inquiry〕→ 原 Add a Row（改為業務）
     ├─〔category=complaint〕→ 新 Add a Row（客服）
     ├─〔category=partnership〕→ 新 Add a Row（合作）
     └─〔category=other〕→ 新 Add a Row（待處理）
```

1. 在 S1 兩個模組之間的連線按右鍵，選 **Add a router**。原 Add a Row 應出現在 Router 後的第一條分支。不要在原 Add a Row 後面才接 Router；若位置錯，先回已保存的 S1 重做插入。
2. 保留原 Add a Row 的 ProcessingLog 目標與 source_key／category 映射。把 route 從「測試」改為「業務」，draft_status 從「不需要」改為「待建立」；status 仍為「已記錄」。在 Router→這個模組的連線設 category 等於 inquiry。
3. 從 Router 的新增路徑入口再接三個 Google Sheets Add a Row，全部寫 ProcessingLog；依[四路設定表](part5-rebuild-guide.html#review-filter)填分類條件、route 與 draft_status。不要讓四條路最後再接一個共用 Add a Row。
4. 在 Watch New Rows→Router 連線設[九欄覆核 Filter](part5-rebuild-guide.html#review-filter)。從左往右查一次：Router 前沒有寫入模組；Router 後共有四個 ProcessingLog 寫入；此時沒有 Drafts 或回寫模組。
5. 保留 S1 舊紀錄，先記下各表筆數；依 CH5-2 每次追加一列測路由。觀察的是「本次新增一列」，不把 S1 舊列也當成本次重複。inquiry 只能新增一筆業務紀錄；待覆核列應零新增。若多出 route=測試 的新紀錄，表示原 S1 寫入仍留在分流前，回步驟 1 修正連線。

S2 不需要刪除表格中的 S1 證據，也不需把完整 Blueprint 覆蓋到自己的流程。完整 Blueprint 可用來對照最終結構；這段練的是從自己的成功版接續改接。

<a id="s2-to-s3"></a>
## S2→S3：查重放在第一次寫入之前

先保存 S2。將 Google Sheets **Make an API Call** 插在 Watch New Rows 與 Router 之間，先設定讀取 ProcessingLog A 欄；四條分支及其中的 Add a Row 保留原位置。插入後逐一核對下圖的兩條入口 Filter，不假設原 Filter 會自動移到正確連線。

```text
Watch New Rows
  →〔九欄覆核 Filter〕→ 讀取 ProcessingLog A 欄
  →〔來源鍵未出現 Filter〕→ Router → 各分類的 ProcessingLog 寫入
                                            ├ inquiry／partnership：再寫 Drafts → 回寫紀錄 E 欄
                                            └ complaint／other：到紀錄為止
```

將原九欄設定放在 Watch New Rows→讀取模組；在讀取模組→Router 設防重。兩者的完整填法見[重建指南](part5-rebuild-guide.html#duplicate-filter)。然後才按下方 S3-2／S3-3 接草稿與回寫。四條路的分類 Filter 仍各留一條；不要把舊的「九欄覆核」留在防重位置而漏掉來源鍵檢查。

全部接好後，用指南的 S3 新鍵做第一次測試，再原樣追加做第二次。第一次對應一筆新紀錄／一份草稿；第二次停在防重連線，兩張表的筆數不變。若第一次就停在防重，先查同鍵是否曾寫入；若分類前已新增紀錄，先修連線再測，不重送同鍵掩蓋問題。

## S3-1 防重
跟著[重建指南](part5-rebuild-guide.html#duplicate-filter)步驟 5 操作：在四路前讀 ProcessingLog A 欄的已處理鍵，攤平後檢查是否不包含目前來源鍵；以目前模組編號選欄位，不直接抄範例編號。Scenario 開 Sequential processing，避免本課測試重疊。

先用新鍵查，應通過；將同一鍵寫過後再查，應停止。找不到任何輸出時，查看是覆核 Filter 擋住還是防重已找到舊鍵。保留舊紀錄，改用一筆新的測試資料驗正常路徑，不改重複案例的提交時間來繞過測試。

## S3-2 草稿映射
依[重建指南步驟 6–7](part5-rebuild-guide.html)，在 inquiry 與 partnership 分支原有 ProcessingLog 寫入之後接 Drafts 的 Add a Row。下表以 inquiry 為例：

| 目標 | 欄位 | 值／映射 |
|---|---|---|
| ProcessingLog | source_key | 提交時間 + `\|` + email 小寫去前後空白 + `\|` + 主旨去前後空白 |
| ProcessingLog | category／route／status | inquiry／業務／已記錄 |
| ProcessingLog | draft_status／error | 待建立／留空 |
| Drafts | source_key | 與上游同一來源鍵 |
| Drafts | recipient | learner@example.com，只存教學地址，不連寄信服務 |
| Drafts | subject | 原主旨 |
| Drafts | body | 人工查核草稿：接上來源 summary，再接 next_action；未知不補值 |
| Drafts | status | 未寄出 |

合作路改 category=partnership、route=合作，其餘相同。complaint／other 保留只有紀錄，draft_status=不需要，不接 Drafts。

## S3-3 回寫與檢查
在 Drafts Add a Row 之後接 Update a Cell，目標是 ProcessingLog 的 E 欄。列號選前面「新增 ProcessingLog」模組輸出的 Row number，不要選 Drafts 的列號；值寫已建立。填完先跑一筆 inquiry，再看同鍵紀錄的 E 欄是否更新、Drafts 是否剛好一列。

保存成功起點，接著用同樣來源鍵再追加，查重應阻擋，不再寫第二筆。若草稿已存在卻仍待建立，先查回寫列號，不重新建立草稿。完全相同鍵的錯誤資料不應藉改時間重送來假裝恢復。

## S4 正常起點清單
確認四分頁、S3 成功與防重證據、來源鍵及排程停用，再跟 CH5-4 故障操作。不能做平台操作時，用上述表手動走一次並標「設計演練、平台未實跑」；手動表不算 Make 已完成。
