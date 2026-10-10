# Part5｜四課建置狀態與完整映射
每課用同一個教學 Scenario 接續，排程停用、Limit=1，僅處理虛構資料。保留每階段截圖與同鍵輸出。不能把教師過去成功紀錄當成自己的證據。

| 課程／階段 | 進入時已有 | 本課新增 | 離開前查表 |
|---|---|---|---|
| CH5-1 S1 | 四分頁與表頭 | 新列觸發→ProcessingLog | 一筆測試來源對一筆紀錄 |
| CH5-2 S2 | S1 成功 | 覆核 Filter、四路 Router | 四分類各一筆；待覆核／unknown 不寫出；草稿可仍空 |
| CH5-3 S3 | S2 成功 | 查重、Drafts、成功狀態回寫 | 新 inquiry 一筆草稿；完全相同鍵再送無新增 |
| CH5-4 S4 | S3 兩測通過 | 人工製造寫入失敗、定位與恢復 | 上游紀錄不重寫，同鍵至多一份草稿 |

## S3-1 防重
跟著[重建指南](part5-rebuild-guide.md)步驟 5 操作：在四路前讀 ProcessingLog A 欄的已處理鍵，攤平後檢查是否不包含目前來源鍵；以目前模組編號選欄位，不直接抄範例編號。Scenario 開 Sequential processing，避免本課測試重疊。

先用新鍵查，應通過；將同一鍵寫過後再查，應停止。找不到任何輸出時，查看是覆核 Filter 擋住還是防重已找到舊鍵。保留舊紀錄，改用一筆新的測試資料驗正常路徑，不改重複案例的提交時間來繞過測試。

## S3-2 草稿映射
依重建指南步驟 6–7，在 inquiry 與 partnership 分支原有 ProcessingLog 寫入之後接 Drafts 的 Add a Row。下表以 inquiry 為例：

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
