# AI Triage Report: office-ai

- generated_at: `2026-09-22`
- actor: `independent-ai`
- simulated_not_human: `true`
- purpose: 排序使用者最後要真人檢測的項目；不代表真人通過。

## Priority findings

### 1. CH1-1, CH1-2, CH1-3 · sequence · PENDING · confidence=medium
- stage: `stage2`
- citations: CH1-1 / 產出物 · 任務適配判斷表, CH1-2 / 產出物 · 工作模式判斷卡, CH1-3 / 最低完成線
- observation: 三頁都寫出前一頁能力與下一步用途，但沒有實際真人產物鏈可供逐檔核對；模擬只能確認敘事上的銜接。
- risk: 正式 sequence 證據需要真人保存三個連續產物並核對下游輸入。
- repair / human action: 真人以 CH1-1→CH1-2→CH1-3 連續跟做，保存每頁完成物與下頁使用位置。

### 2. CH1-2 · platform · PENDING · confidence=low
- stage: `stage2`
- citations: CH1-2 / 本節任務, CH1-2 / 範例演練
- observation: 頁面明確要求通用 LLM 與 NotebookLM 兩種模式、來源上傳與引用回查；文字無法確認指定帳號是否能看到相同入口與引用格式。
- risk: 未實跑可能造成來源上傳、引用或權限路徑與頁面不一致。
- repair / human action: 真人以指定帳號上傳 meeting-transcript-sample.txt，完成同題雙模式比較並記錄引用與錯誤恢復。

### 3. CH5-1 · completion · PENDING · confidence=low
- stage: `stage1`
- citations: 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 情境： 開完會，一堆錄音要變成文字稿, 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 延伸應用： 接下來交給 AI 整理
- observation: 文字頁面寫出步驟、權限與備援，但目前無法由文字模擬實際瀏覽器、麥克風與 Google 文件狀態。
- risk: 文字模擬無法證明外部平台、權限或真實素材能成功執行。
- repair / human action: 由真人實跑指定平台與備援路徑，回填 platform evidence；未完成前保留 PENDING。

### 4. CH5-1 · platform · PENDING · confidence=low
- stage: `stage2`
- citations: CH5-1 / 開始前與完成物, CH5-1 / 延伸應用
- observation: 頁面列出 Google 文件語音輸入、麥克風權限、30–60 秒音訊與共用示範稿備援；模擬無法取得瀏覽器、作業系統與麥克風狀態。
- risk: 指定帳號或組織政策可能停用語音輸入，造成第一個動作無法完成。
- repair / human action: 真人實跑一種方案，記錄權限、原音、轉錄、校對與備援結果。

### 5. CH6-3 · completion · PENDING · confidence=medium
- stage: `stage1`
- citations: 持續學習：課程結束後，怎麼跟上 / 本節任務： 把一個低風險工作變成 30 天計畫, 持續學習：課程結束後，怎麼跟上 / 延伸應用： 30 天養成習慣，整門課濃縮成幾句話
- observation: 頁面提供四週欄位與成功指標，但 30 天後的真實成效與習慣維持不能由一次模擬證明。
- risk: 若沒有真人紀錄，完成物只代表計畫草稿，不代表實際習慣或成效。
- repair / human action: 真人完成第一週基準並在第 30 天回填耗時、錯誤率或品質比較；未完成前保留 PENDING。

### 6. CH6-3 · content · PENDING · confidence=medium
- stage: `stage2`
- citations: CH6-3 / 本節任務, CH6-3 / 結訓產出物 · 30 天應用計畫
- observation: 頁面給出任務、頻率、基準、人工查核點、成功指標與四週安排；但一次模擬無法驗證計畫是否能被持續執行。
- risk: 若沒有真人紀錄，完成物只代表計畫草稿，不代表實際習慣或成效。
- repair / human action: 真人完成第一週基準並在第 30 天回填耗時、錯誤率或品質比較。

### 7. CH6-3 · transfer · PENDING · confidence=medium
- stage: `stage1`
- citations: 持續學習：課程結束後，怎麼跟上 / 本節任務： 把一個低風險工作變成 30 天計畫, 持續學習：課程結束後，怎麼跟上 / 延伸應用： 30 天養成習慣，整門課濃縮成幾句話
- observation: 頁面提供 30 天計畫與自我檢查，但一次閱讀不能觀察四週後是否真的執行與比較成果。
- risk: 真實遷移需要跨週紀錄時間、錯誤率或品質；一次模擬不能替代。
- repair / human action: 由真人在四週後回看計畫並保存成效；目前保留 PENDING。

### 8. CH1-1 · completion · PASS · confidence=high
- stage: `stage1`
- citations: AI 能幫我做什麼？先搞清楚它的強項與罩門 / 本節任務： 先判斷哪些工作適合交給 AI, AI 能幫我做什麼？先搞清楚它的強項與罩門 / 延伸應用： 接下來這門課，會帶你練什麼
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 9. CH1-1 · content · PASS · confidence=high
- stage: `stage2`
- citations: CH1-1 / 本節任務, CH1-1 / 產出物 · 任務適配判斷表
- observation: 第一階段沒有把新契約當成卡片標籤；可從四個情境、規則與判斷表完成分類。
- risk: AI 仍可能高估初學者是否能把自己的三項工作分類。
- repair / human action: 真人抽查一項自選工作，要求說出分類理由。

### 10. CH1-1 · entry · PASS · confidence=high
- stage: `stage1`
- citations: AI 能幫我做什麼？先搞清楚它的強項與罩門 / 本節任務： 先判斷哪些工作適合交給 AI
- observation: 頁面先給四個情境、判斷規則與完成表格；學員不需猜材料或分類標準。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 11. CH1-1 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: AI 能幫我做什麼？先搞清楚它的強項與罩門 / 本節任務： 先判斷哪些工作適合交給 AI, AI 能幫我做什麼？先搞清楚它的強項與罩門 / 延伸應用： 接下來這門課，會帶你練什麼
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 12. CH1-1 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: AI 能幫我做什麼？先搞清楚它的強項與罩門 / 本節任務： 先判斷哪些工作適合交給 AI, AI 能幫我做什麼？先搞清楚它的強項與罩門 / 延伸應用： 接下來這門課，會帶你練什麼
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 13. CH1-2 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 本節任務： 為同一份資料選對工作模式, 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 延伸應用： 現在換你試試看
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 14. CH1-2 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 本節任務： 為同一份資料選對工作模式
- observation: 頁面清楚把自由生成、指定來源、引用與人工回查分成可觀察欄位。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 15. CH1-2 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 本節任務： 為同一份資料選對工作模式, 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 延伸應用： 現在換你試試看
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 16. CH1-2 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 本節任務： 為同一份資料選對工作模式, 通用 LLM 與 NotebookLM：生成與依據來源的差異 / 延伸應用： 現在換你試試看
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 17. CH1-3 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 基礎操作指南：從註冊到打出第一句話 / 情境： 第一次打開 AI 工具，不知道怎麼開始, 基礎操作指南：從註冊到打出第一句話 / 延伸應用： 換題獨立完成
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 18. CH1-3 · content · PASS · confidence=high
- stage: `stage2`
- citations: CH1-3 / 情境, CH1-3 / 最低完成線
- observation: 入口給出已開啟的新對話與帳號條件；Solo 有新題目、兩輪輸出、快速檢查與回復。
- risk: 實際帳號註冊或介面漂移仍不在本次模擬範圍。
- repair / human action: 真人只需抽查新對話、送出、追問與關鍵資訊保留。

### 19. CH1-3 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 基礎操作指南：從註冊到打出第一句話 / 情境： 第一次打開 AI 工具，不知道怎麼開始
- observation: 頁面給出帳號、新對話與三步操作，並在 Solo 指出期限與動作不能遺失。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 20. CH1-3 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 基礎操作指南：從註冊到打出第一句話 / 情境： 第一次打開 AI 工具，不知道怎麼開始, 基礎操作指南：從註冊到打出第一句話 / 延伸應用： 換題獨立完成
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 21. CH1-3 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 基礎操作指南：從註冊到打出第一句話 / 情境： 第一次打開 AI 工具，不知道怎麼開始, 基礎操作指南：從註冊到打出第一句話 / 延伸應用： 換題獨立完成
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 22. CH1-4 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 有效溝通第一步：把話講清楚，AI 才聽得懂 / 情境： 同一份會議資訊，產出規格不同, 有效溝通第一步：把話講清楚，AI 才聽得懂 / 延伸應用： 現在換你試試看
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 23. CH1-4 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 有效溝通第一步：把話講清楚，AI 才聽得懂 / 情境： 同一份會議資訊，產出規格不同
- observation: 頁面用同一份資料示範三要素，並在兩個 checkpoint 指出格式與事實檢查。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 24. CH1-4 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 有效溝通第一步：把話講清楚，AI 才聽得懂 / 情境： 同一份會議資訊，產出規格不同, 有效溝通第一步：把話講清楚，AI 才聽得懂 / 延伸應用： 現在換你試試看
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 25. CH1-4 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 有效溝通第一步：把話講清楚，AI 才聽得懂 / 情境： 同一份會議資訊，產出規格不同, 有效溝通第一步：把話講清楚，AI 才聽得懂 / 延伸應用： 現在換你試試看
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 26. CH2-1 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 進階指令技巧：角色扮演 ＋ 給範例 / 情境： 1.4 學了「講清楚」，這節再上兩招, 進階指令技巧：角色扮演 ＋ 給範例 / 延伸應用： 換角色獨立完成
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 27. CH2-1 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 進階指令技巧：角色扮演 ＋ 給範例 / 情境： 1.4 學了「講清楚」，這節再上兩招
- observation: 頁面說明角色改變判準、範例控制風格，並明示未知日期要標待補。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 28. CH2-1 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 進階指令技巧：角色扮演 ＋ 給範例 / 情境： 1.4 學了「講清楚」，這節再上兩招, 進階指令技巧：角色扮演 ＋ 給範例 / 延伸應用： 換角色獨立完成
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 29. CH2-1 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 進階指令技巧：角色扮演 ＋ 給範例 / 情境： 1.4 學了「講清楚」，這節再上兩招, 進階指令技巧：角色扮演 ＋ 給範例 / 延伸應用： 換角色獨立完成
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 30. CH2-2 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 調整風格與語氣：同一件事，三種說法 / 情境： 寫給主管、同事、客戶，語氣天差地遠, 調整風格與語氣：同一件事，三種說法 / 延伸應用： 現在換你試試看
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 31. CH2-2 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 調整風格與語氣：同一件事，三種說法 / 情境： 寫給主管、同事、客戶，語氣天差地遠
- observation: 頁面固定共同事實，再逐步改受眾與語氣，checkpoint 要求事實一致。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 32. CH2-2 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 調整風格與語氣：同一件事，三種說法 / 情境： 寫給主管、同事、客戶，語氣天差地遠, 調整風格與語氣：同一件事，三種說法 / 延伸應用： 現在換你試試看
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 33. CH2-2 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 調整風格與語氣：同一件事，三種說法 / 情境： 寫給主管、同事、客戶，語氣天差地遠, 調整風格與語氣：同一件事，三種說法 / 延伸應用： 現在換你試試看
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 34. CH2-3 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 反覆修正與優化：AI 第一次答錯，怎麼救 / 情境： 對外信件，AI 為了讓你滿意會替你闖禍, 反覆修正與優化：AI 第一次答錯，怎麼救 / 延伸應用： 帶走四份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 35. CH2-3 · content · PASS · confidence=high
- stage: `stage2`
- citations: CH2-3 / 範例演練, CH2-3 / 送出前 · 人工驗證卡
- observation: 控制版、Repair 與人工驗證各有輸入、規則、輸出與風險對照；不是只叫學員多問幾次。
- risk: 模擬無法判斷學員是否能辨識法律措辭的細微風險。
- repair / human action: 真人抽查 Repair 前後一個句子，說明它如何避免越權承諾。

### 36. CH2-3 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 反覆修正與優化：AI 第一次答錯，怎麼救 / 情境： 對外信件，AI 為了讓你滿意會替你闖禍
- observation: 頁面提供事實編號、控制規則、三輪結果與議價 Solo，能觀察修正前後差異。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 37. CH2-3 · fidelity · PASS · confidence=high
- stage: `stage2`
- citations: CH2-3 / 產出 2.3-A, CH2-3 / 產出 2.3-B
- observation: 模板與案例中的控制規則、事實編號與修正路徑在 learner-facing page 中可見。
- risk: 實際 prompt 複製時的格式差異未由模擬驗證。
- repair / human action: 真人複製一份控制版與 Repair 模板，核對輸出仍保留事實編號。

### 38. CH2-3 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 反覆修正與優化：AI 第一次答錯，怎麼救 / 情境： 對外信件，AI 為了讓你滿意會替你闖禍, 反覆修正與優化：AI 第一次答錯，怎麼救 / 延伸應用： 帶走四份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 39. CH2-3 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 反覆修正與優化：AI 第一次答錯，怎麼救 / 情境： 對外信件，AI 為了讓你滿意會替你闖禍, 反覆修正與優化：AI 第一次答錯，怎麼救 / 延伸應用： 帶走四份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 40. CH3-1 · completion · PASS · confidence=high
- stage: `stage1`
- citations: AI 輔助文書撰寫：週報、活動紀錄、公告 / 情境： 隨便問寫得不差 ——問題在你看不見的地方, AI 輔助文書撰寫：週報、活動紀錄、公告 / 延伸應用： 帶走四份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 41. CH3-1 · content · PASS · confidence=high
- stage: `stage2`
- citations: CH3-1 / 範例演練, CH3-1 / 延伸應用
- observation: 頁面展示不可回查、微誇大、來源編號與 Repair，並要求保存人工核對版；第二階段沒有找到列表代替因果鏈的缺口。
- risk: 頁面承認 AI 可能把需人工確認欄全填無，真人仍要核對灰區。
- repair / human action: 真人抽查一條工作日誌，回到來源編號確認狀態與數字。

### 42. CH3-1 · entry · PASS · confidence=high
- stage: `stage1`
- citations: AI 輔助文書撰寫：週報、活動紀錄、公告 / 情境： 隨便問寫得不差 ——問題在你看不見的地方
- observation: 頁面示範來源誤掛與狀態誇大，並給控制口徑、Repair 與來源編號。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 43. CH3-1 · fidelity · PASS · confidence=high
- stage: `stage2`
- citations: CH3-1 / 控制版真跑, CH3-1 / Repair 真跑
- observation: 弱指令、控制口徑與 Repair 的差異均在頁面上完整呈現。
- risk: 模擬不能證明真實模型會重現相同錯誤。
- repair / human action: 真人用範例資料重跑弱指令與控制版，保存差異。

### 44. CH3-1 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: AI 輔助文書撰寫：週報、活動紀錄、公告 / 情境： 隨便問寫得不差 ——問題在你看不見的地方, AI 輔助文書撰寫：週報、活動紀錄、公告 / 延伸應用： 帶走四份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 45. CH3-1 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: AI 輔助文書撰寫：週報、活動紀錄、公告 / 情境： 隨便問寫得不差 ——問題在你看不見的地方, AI 輔助文書撰寫：週報、活動紀錄、公告 / 延伸應用： 帶走四份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 46. CH3-2 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 聰明整理表格：AI 整理得了結構，算不準總額 / 情境： 整理得了結構，算不準總額, 聰明整理表格：AI 整理得了結構，算不準總額 / 延伸應用： 帶走四份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 47. CH3-2 · content · PASS · confidence=high
- stage: `stage2`
- citations: CH3-2 / 核心要點, CH3-2 / 人工驗證卡
- observation: 頁面反覆把結構整理與數字計算分開，提供重複列判斷、公式比較與人工總額檢查。
- risk: 模擬不能證明學員會真的拿計算機或試算表核算。
- repair / human action: 真人抽查一個重複列案例，保存兩個公式總額與判斷理由。

### 48. CH3-2 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 聰明整理表格：AI 整理得了結構，算不準總額 / 情境： 整理得了結構，算不準總額
- observation: 頁面把結構整理與算術分開，控制版與兩個 checkpoint 都要求人工驗總額。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 49. CH3-2 · fidelity · PASS · confidence=high
- stage: `stage2`
- citations: CH3-2 / 範例演練, CH3-2 / 延伸應用
- observation: 完成物與錯誤修復在頁面中沒有被壓成只有列表的摘要。
- risk: 仍需真人確認表格操作結果與頁面可讀性。
- repair / human action: 真人完成表格後保存控制版、公式結果與人工核對。

### 50. CH3-2 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 聰明整理表格：AI 整理得了結構，算不準總額 / 情境： 整理得了結構，算不準總額, 聰明整理表格：AI 整理得了結構，算不準總額 / 延伸應用： 帶走四份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 51. CH3-2 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 聰明整理表格：AI 整理得了結構，算不準總額 / 情境： 整理得了結構，算不準總額, 聰明整理表格：AI 整理得了結構，算不準總額 / 延伸應用： 帶走四份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 52. CH3-3 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 情境： 摘得了重點，卻多算一個數字, 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 延伸應用： 帶走三份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 53. CH3-3 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 情境： 摘得了重點，卻多算一個數字
- observation: 頁面示範擅自推算與漏掉限制，並提供摘要格式、來源標記與 Repair。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 54. CH3-3 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 情境： 摘得了重點，卻多算一個數字, 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 延伸應用： 帶走三份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 55. CH3-3 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 情境： 摘得了重點，卻多算一個數字, 長文變重點：AI 摘得了重點，會自己「多算一個數字」 / 延伸應用： 帶走三份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 56. CH4-1 · completion · PASS · confidence=high
- stage: `stage1`
- citations: AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 情境： 很專業的大綱，夾帶你沒給的東西, AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 延伸應用： 帶走兩份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 57. CH4-1 · entry · PASS · confidence=high
- stage: `stage1`
- citations: AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 情境： 很專業的大綱，夾帶你沒給的東西
- observation: 頁面先清理未知欄位，再用控制 prompt 與 Solo 檢查來源或待補標記。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 58. CH4-1 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 情境： 很專業的大綱，夾帶你沒給的東西, AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 延伸應用： 帶走兩份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 59. CH4-1 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 情境： 很專業的大綱，夾帶你沒給的東西, AI 生成簡報大綱：一份很專業的稿，夾帶你沒給的東西 / 延伸應用： 帶走兩份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 60. CH4-2 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 內容自動生成：把重點展開成內容，它會順手加料 / 情境： 一句重點，被撐成一段加料, 內容自動生成：把重點展開成內容，它會順手加料 / 延伸應用： 帶走一份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 61. CH4-2 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 內容自動生成：把重點展開成內容，它會順手加料 / 情境： 一句重點，被撐成一段加料
- observation: 頁面以同一大綱對照弱指令與控制版，明確示範加料與最小修正。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 62. CH4-2 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 內容自動生成：把重點展開成內容，它會順手加料 / 情境： 一句重點，被撐成一段加料, 內容自動生成：把重點展開成內容，它會順手加料 / 延伸應用： 帶走一份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 63. CH4-2 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 內容自動生成：把重點展開成內容，它會順手加料 / 情境： 一句重點，被撐成一段加料, 內容自動生成：把重點展開成內容，它會順手加料 / 延伸應用： 帶走一份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 64. CH4-3 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 尋找合適配圖：AI 給的是「建議」，不是圖 / 情境： 隨便問給罐頭裝飾圖, 尋找合適配圖：AI 給的是「建議」，不是圖 / 延伸應用： 從描述到圖片
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 65. CH4-3 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 尋找合適配圖：AI 給的是「建議」，不是圖 / 情境： 隨便問給罐頭裝飾圖
- observation: 頁面清楚說明文字 AI 只給建議，並用 Solo 與人工卡檢查是否貼題。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 66. CH4-3 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 尋找合適配圖：AI 給的是「建議」，不是圖 / 情境： 隨便問給罐頭裝飾圖, 尋找合適配圖：AI 給的是「建議」，不是圖 / 延伸應用： 從描述到圖片
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 67. CH4-3 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 尋找合適配圖：AI 給的是「建議」，不是圖 / 情境： 隨便問給罐頭裝飾圖, 尋找合適配圖：AI 給的是「建議」，不是圖 / 延伸應用： 從描述到圖片
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 68. CH5-1 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 情境： 開完會，一堆錄音要變成文字稿
- observation: 文字頁面寫出步驟、權限與備援，但目前無法由文字模擬實際瀏覽器、麥克風與 Google 文件狀態。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 69. CH5-1 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 情境： 開完會，一堆錄音要變成文字稿, 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 延伸應用： 接下來交給 AI 整理
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 70. CH5-1 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 情境： 開完會，一堆錄音要變成文字稿, 會議錄音轉文字：先把聲音變成字，AI 才接得上 / 延伸應用： 接下來交給 AI 整理
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 71. CH5-2 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 情境： 漂亮的紀錄，把「再看看」寫成「決議」, 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 延伸應用： 帶走兩份模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 72. CH5-2 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 情境： 漂亮的紀錄，把「再看看」寫成「決議」
- observation: 頁面提供逐字稿、控制版、錯誤對照與發送前核對卡，完成物用途明確。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 73. CH5-2 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 情境： 漂亮的紀錄，把「再看看」寫成「決議」, 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 延伸應用： 帶走兩份模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 74. CH5-2 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 情境： 漂亮的紀錄，把「再看看」寫成「決議」, 會議紀錄自動化：它會把「原則同意」寫成「已決議」 / 延伸應用： 帶走兩份模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 75. CH5-3 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 行政任務優化：郵件寫得體，細節它替你填 / 情境： 得體的郵件，細節是它填的, 行政任務優化：郵件寫得體，細節它替你填 / 延伸應用： 帶走模板
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 76. CH5-3 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 行政任務優化：郵件寫得體，細節它替你填 / 情境： 得體的郵件，細節是它填的
- observation: 頁面用控制版、Solo 與寄出前卡檢查合理填充，缺值處理可觀察。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 77. CH5-3 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 行政任務優化：郵件寫得體，細節它替你填 / 情境： 得體的郵件，細節是它填的, 行政任務優化：郵件寫得體，細節它替你填 / 延伸應用： 帶走模板
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 78. CH5-3 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 行政任務優化：郵件寫得體，細節它替你填 / 情境： 得體的郵件，細節是它填的, 行政任務優化：郵件寫得體，細節它替你填 / 延伸應用： 帶走模板
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 79. CH6-1 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 建立你的 AI 工作流程：把零散技巧串成一套 / 情境： 零散技巧，該串成一套了, 建立你的 AI 工作流程：把零散技巧串成一套 / 延伸應用： 現在換你試試看
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 80. CH6-1 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 建立你的 AI 工作流程：把零散技巧串成一套 / 情境： 零散技巧，該串成一套了
- observation: 頁面給流程卡欄位、五步演練與第二次重跑，能看出上游輸入和人工責任。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 81. CH6-1 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 建立你的 AI 工作流程：把零散技巧串成一套 / 情境： 零散技巧，該串成一套了, 建立你的 AI 工作流程：把零散技巧串成一套 / 延伸應用： 現在換你試試看
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 82. CH6-1 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 建立你的 AI 工作流程：把零散技巧串成一套 / 情境： 零散技巧，該串成一套了, 建立你的 AI 工作流程：把零散技巧串成一套 / 延伸應用： 現在換你試試看
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 83. CH6-2 · completion · PASS · confidence=high
- stage: `stage1`
- citations: 安全與限制：哪些能交給 AI，哪些絕對不行 / 本節任務： 先判斷資料能不能原樣貼入 AI, 安全與限制：哪些能交給 AI，哪些絕對不行 / 延伸應用： 現在換你試試看
- observation: 頁面以文字、範例與可觀察完成線描述產出，模擬上可沿路完成。
- risk: 若完成物只停留在敘述而未留下可驗收產物，學習成果會被高估。
- repair / human action: 真人冷讀時保存完成物，若無法保存則回修完成物名稱、格式、用途或檢查句。

### 84. CH6-2 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 安全與限制：哪些能交給 AI，哪些絕對不行 / 本節任務： 先判斷資料能不能原樣貼入 AI
- observation: 頁面給四個資料情境、三種去識別化處理與停止上傳的回復規則。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 85. CH6-2 · transfer · PASS · confidence=high
- stage: `stage1`
- citations: 安全與限制：哪些能交給 AI，哪些絕對不行 / 本節任務： 先判斷資料能不能原樣貼入 AI, 安全與限制：哪些能交給 AI，哪些絕對不行 / 延伸應用： 現在換你試試看
- observation: 頁面提供新情境、Solo 或換題練習；模擬學員可依規則把表面情境換掉，沒有只改人名。
- risk: 若換題時仍需教師補充，代表規則尚未能獨立遷移。
- repair / human action: 真人改用未示範的同類情境冷做，若需要額外提示，補上判準或轉移練習。

### 86. CH6-2 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 安全與限制：哪些能交給 AI，哪些絕對不行 / 本節任務： 先判斷資料能不能原樣貼入 AI, 安全與限制：哪些能交給 AI，哪些絕對不行 / 延伸應用： 現在換你試試看
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

### 87. CH6-3 · entry · PASS · confidence=high
- stage: `stage1`
- citations: 持續學習：課程結束後，怎麼跟上 / 本節任務： 把一個低風險工作變成 30 天計畫
- observation: 頁面提供四週欄位與成功指標，但 30 天後的真實成效與習慣維持不能由一次模擬證明。
- risk: 若入口缺少材料或第一步，初學者會依賴教師補充。
- repair / human action: 保留入口契約與第一個動作；若人工測試發現仍需提示，補回該頁的起始材料或回復位置。

### 88. CH6-3 · understanding · PASS · confidence=high
- stage: `stage1`
- citations: 持續學習：課程結束後，怎麼跟上 / 本節任務： 把一個低風險工作變成 30 天計畫, 持續學習：課程結束後，怎麼跟上 / 延伸應用： 30 天養成習慣，整門課濃縮成幾句話
- observation: 核心判斷有白話規則、示範結果與錯誤原因；模擬學員能用頁面語句重述何時交給 AI、何時人工把關。
- risk: AI 可以模擬重述，但不能證明真人真的理解或能在沒有提示時解釋。
- repair / human action: 由真人以自己的話回答理解題；若漏掉限制，回修該頁的理由、反例或核對段落。

## Reading rule

先處理 FAIL／BLOCKER／MAJOR，再處理 PENDING、平台、sequence 與低信心項目；PASS 只代表目前 AI 模擬找不到確定性缺口。真人結果仍須另建 `human` evidence。
