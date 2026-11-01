# Part 5 改寫事實清單（gen-ai-36h）

整理日期：2026-11-01。範圍：只讀現有素材，不含 `_review/`。
路徑簡寫：`L/` = `_lessons/gen-ai-36h/`（只取 learner-content 段）；`A/` = `courses/gen-ai-36h/assets/`；`R/` = `courses/gen-ai-36h/_repair/2026-10-09/`；`BP` = `A/reference-make-blueprint.json`。
`A/*.html` 與同名 `A/*.md` 已比對，文字內容一致（差異只在連結與清單編號格式），以下引用 .md。
標記：【實跑】= REPAIR-REPORT／ENVIRONMENT 記載已在教學工作區跑過；【文件】= 只見於教材或指南敘述；【不一致】= 素材之間互相矛盾，改寫前需裁決。

---

## 1. 現有 5 頁結構與學員主要動作

### CH5-1 理解觸發與欄位：先跑最小流程（L/CH5-1.md）
- 小標：自動化從一件看得見的動作開始／示範：一個觸發，一個寫入／跟著做：映射要看值，不只看線／自己試：新列和改舊列不同。
- 完成物：「一筆新列對應一筆紀錄與執行證據」；本課只到階段 S1，「Drafts 仍可為空」。
- 動作：建四分頁 Source、ReviewedQueue、ProcessingLog、Drafts；把示例 CSV 第一筆「小林／詢問方案」貼進 Source 與 ReviewedQueue 第 2 列。
- Make：Watch New Rows（ReviewedQueue、A1:I1、Limit=1、首次起點選 All）→ Add a Row（ProcessingLog，route=測試、status=已記錄、draft_status=不需要）→ Run once。
- 核對 bundle 值；改 Source 舊列 message 再 Run once，應無新 bundle；再追加第二筆「小安／交期問題」，應只新增一筆 complaint 紀錄。
- 明言「第一堂不加AI或寄信」；示例列「不是模型輸出」。

### CH5-2 條件、分流與執行紀錄（L/CH5-2.md）
- 小標：有分類，流程才知道走哪條路／示範：覆核通過後才分流／跟著做：一次新增一列／自己試：阻擋不合格資料／選做：n8n的角色。
- 完成物：「四分類各一筆紀錄與執行核對」（階段 S2）。
- 動作：在 Watch New Rows 與原 Add a Row 之間插入 Router，原 Add a Row 改成 inquiry 分支，再加三路；在 Watch New Rows→Router 連線設九項 AND 覆核 Filter；四條分支各設 category 等於條件。
- 逐筆追加 T01–T04，每次 Run once，查 bundle、路徑與結果表。
- 自己試：追加 review_status=待覆核、category=unknown 兩筆，應被 Filter 擋下、零新增。
- 選做 n8n：不要求安裝 Desktop 版，不用 LINE Notify。

### CH5-3 人工覆核後再接自動化（L/CH5-3.md）
- 小標：分類建議仍需人工決定／示範：從原文整理一筆候選列／跟著做：辨認多重意圖和被引用的舊訊息／自己試：完整性與重複鍵先於路由／完成草稿分支，再交給下一課。
- 動作（AI 段）：把 U07 原文貼給生成式 AI，用固定提示詞產九欄候選（前五欄照抄、review_status 填待覆核）；逐欄比對 `part5-candidate-example`。
- 再對 U01、U02 取 AI 候選並人工判斷；U03–U06 取候選後自行計算來源鍵、檢查完整性、判斷主要意圖；之後才開答案鍵。
- 人工把合格列改為「已覆核」再追加 ReviewedQueue。
- Make 段（S3）：加來源鍵查重、詢問／合作寫 Drafts、成功後回寫 ProcessingLog 草稿狀態；用新鍵跑 inquiry，再追加完全相同九欄，應兩表都不增加。
- 沒有 AI 帳號標 AI `NOT_RUN`；沒有 Sheets／Make 權限另標自動化 `NOT_RUN`。

### CH5-4 流程失敗時：查紀錄，再從失敗處恢復（L/CH5-4.md）
- 小標：綠勾之外，還要能說明失敗在哪／示範：從執行記錄往回查／跟著做：安全暫停並恢復／自己試：寫一份接手說明。
- 前提：要有 S3「正常草稿及防重兩項成功紀錄」。
- 故障三分類：資料不合格在 Filter 擋；連線或權限錯在模組失敗；部分成功要核對下游。附四列「現象／修復位置／重跑前核對」表。
- 動作：停排程 → Scenario settings 開儲存未完成執行 → 詢問路 Drafts 目標表改成不存在名稱 → 執行 T07 → Incomplete executions 的 Details 內修回 Drafts、Save、Run once → 主流程也修回。
- 核對：ProcessingLog 仍一列、draft_status=已建立、Drafts 一份未寄出、未完成執行 Resolved。
- 自己試：寫接手說明（觸發來源、九欄規格、最後成功紀錄、常見錯誤、停止方式、恢復位置）。

### PRAC5 交付人工覆核後分流的流程（L/PRAC5.md）
- 小標：同時驗收業務判斷和 Make 路由／第一關：完成候選列與人工覆核／第二關：按 T01–T07 重建或重跑流程／交付。
- 第一關：N01–N04 逐筆交 AI 產候選（沿用 CH5-3 提示詞），再人工核對主要分類、九欄完整性、正規化來源鍵、補問理由、是否可覆核；之後才看答案。
- 第二關：匯入 Blueprint 後重連帳號與試算表；用 `part5-test-inputs.csv` 逐列追加 T01–T07（追加前移除 test_case 欄）；用新教學表或空白測試副本。
- T05a／T05b 只在停排程的隔離副本測；T07 在 CH5-4 故障設定後才追加。
- 附 T01–T07 預期表；逐案記輸入、execution ID／截圖、結果列、草稿數、判定；未跑填 `PENDING`。
- 交付：N01–N04 分類表與理由、人工覆核標記、T01–T07 執行紀錄、恢復說明。

---

## 2. 試算表結構

### 2.1 分頁（同一份試算表，四個分頁）
出處：A/part5-sheet-layout.md 第 2–3 行；L/CH5-1.md「示範」段。

| 分頁 | 用途 | 出處 |
|---|---|---|
| Source | 「保存原文」；CH5-1 說「留作原始資料對照」；有問題的資料「保留Source列並停止入列」 | sheet-layout；CH5-1；input-contract |
| ReviewedQueue | 「只追加已覆核完整新列，中途不可空白」；Watch New Rows 讀這張 | sheet-layout；BP id1 `sheetId: ReviewedQueue` |
| ProcessingLog | 流程寫入的處理紀錄；也是防重讀取的來源（A 欄） | sheet-layout；BP id2/6/7/8、id4 URL |
| Drafts | 未寄出草稿列（Google 試算表分頁，**不是 Gmail 草稿**） | sheet-layout；BP id9/10 `sheetId: Drafts` |

### 2.2 Source／ReviewedQueue 九欄（A–I 欄）
表頭順序出處：A/part5-sheet-layout.md「submitted_at,name,email,subject,message,category,summary,next_action,review_status」。
欄意出處：A/part5-input-contract.md。誰填出處：L/CH5-3.md 提示詞與「前五欄是來源原文，必須照抄；AI 只能建議分類、摘要和下一步，不能核准自己產出的列」。

| 欄 | 英文欄名 | 中文意思（input-contract 原文） | 誰填 | 允許值 |
|---|---|---|---|---|
| A | submitted_at | 原始提交時間文字 | 原文照抄 | 文字；不可空白。素材格式有兩種：T 測試列 `2026-10-09T09:00`，U／N 原文 `2026-10-01 09:30`（見第 5 節） |
| B | name | 虛構姓名 | 原文照抄 | 不可空白 |
| C | email | 有效格式的測試郵件 | 原文照抄 | Filter 樣式 `^[^@\s]+@[^@\s]+\.[^@\s]+$`（rebuild-guide） |
| D | subject | 主旨 | 原文照抄 | 不可空白 |
| E | message | 原文 | 原文照抄 | 不可空白 |
| F | category | inquiry／complaint／partnership／other之一 | AI 建議，人覆核 | 僅這四個英文固定值（「分類用英文固定值」） |
| G | summary | 不新增事實的一句摘要 | AI 建議，人覆核 | 不可空白 |
| H | next_action | 待人工確認的下一步 | AI 建議，人覆核 | 不可空白 |
| I | review_status | 待覆核／已覆核 | AI 一律填「待覆核」；人改為「已覆核」 | 僅「待覆核」「已覆核」（「覆核用中文固定值」） |

- 「九欄均不可空白。只有已覆核且分類有效才進分流。」（input-contract）
- case_id、source_id 不進九欄：「case_id 與 source_id 存在旁邊的追溯表，不塞進九欄，亦不拿 source_id 代替去重鍵」（A/part5-candidate-example.md）。
- Make 讀欄方式：BP 以欄序號引用，`1.0`=submitted_at、`1.2`=email、`1.3`=subject、`1.5`=category、`1.6`=summary、`1.7`=next_action、`1.8`=review_status（rebuild-guide「`1.0` 是提交時間、`1.2` 是 email、`1.3` 是主旨」；其餘由 BP 映射位置對應）。

### 2.3 ProcessingLog 六欄（A–F）— 全部由流程寫入
出處：sheet-layout「ProcessingLog：source_key,category,route,status,draft_status,error」；rebuild-guide 步驟 6–7；BP id2/6/7/8/11/12。

| 欄 | 欄名 | 意思 | 值 |
|---|---|---|---|
| A | source_key | 來源鍵 | `{{1.0}}|{{lower(trim(1.2))}}|{{trim(1.3)}}`（BP） |
| B | category | 分類 | 映射 `1.5` |
| C | route | 路徑 | 業務／客服／合作／待處理；S1 階段為「測試」（CH5-1） |
| D | status | 處理狀態 | 「已記錄」 |
| E | draft_status | 草稿狀態 | 待建立／不需要；草稿成功後由 Update a Cell 改「已建立」；S1 為「不需要」 |
| F | error | 錯誤文字 | 【不一致】rebuild-guide 說 A–F「依序填…錯誤文字」，stage-handoff 寫「error／留空」；BP 四個 Add a Row 的 values 只有 0–4（A–E），**沒有任何模組寫 F 欄** |

### 2.4 Drafts 五欄（A–E）— 全部由流程寫入
出處：sheet-layout「Drafts：source_key,recipient,subject,body,status；recipient僅測試本人，status=未寄出」；stage-handoff S3-2 表；BP id9/id10。

| 欄 | 欄名 | stage-handoff 寫法 | BP 實際映射 |
|---|---|---|---|
| A | source_key | 與上游同一來源鍵 | 同上組合式 |
| B | recipient | 「learner@example.com，只存教學地址」 | `{{1.2}}`（映射來源 email，不是固定值）【不一致，見第 4 節】 |
| C | subject | 「原主旨」 | `課堂草稿：{{1.3}}` |
| D | body | 「人工查核草稿：接上來源 summary，再接 next_action；未知不補值」 | `你好，感謝來訊。原訊重點：{{1.6}}。建議下一步：{{1.7}}。此為課堂未寄出草稿，請人工查核承諾與聯絡資訊。` |
| E | status | 未寄出 | `未寄出` |

### 2.5 來源鍵（去重鍵）
- 定義：「去重鍵= submitted_at + | + 小寫且去前後空白的 email + | + 去前後空白的 subject。一次處理一列；此教學做法不保證並行時不重複。」（sheet-layout）
- 「提交時間、email與主旨組成來源鍵；重試不改來源鍵。」（input-contract）
- 範例鍵：`2026-10-09T09:00|learner@example.com|詢問方案`（rebuild-guide）；`2026-10-01 09:30|learner07@example.com|服務時間`（candidate-example）。

---

## 3. 四種分類

| 分類值 | 素材中的定義／說明 | Router 條件 | 寫入 ProcessingLog | route | draft_status 初值 | 建草稿？ | 出處 |
|---|---|---|---|---|---|---|---|
| inquiry | 正式定義素材未提及；candidate-example 對 U07 說「詢問資訊，未反映服務不滿」；會議逐字稿稱「詢價」 | category Text: Equal to `inquiry`（BP filter 名「業務：inquiry」） | 是 | 業務 | 待建立 | 是，寫 Drafts，成功後 E 欄改「已建立」 | rebuild-guide 四路表；BP id2→9→11 |
| complaint | 正式定義素材未提及；會議逐字稿稱「客訴」；答案鍵 U06「反映回覆延遲並表達不滿」 | Equal to `complaint`（「客服：complaint」） | 是 | 客服 | 不需要 | 否（「客服人工處理，不建立草稿」答案鍵 U06） | rebuild-guide；BP id6 |
| partnership | 正式定義素材未提及；會議逐字稿稱「合作」 | Equal to `partnership`（「合作：partnership」） | 是 | 合作 | 待建立 | 是，同 inquiry | rebuild-guide；BP id7→10→12 |
| other | 正式定義素材未提及；會議逐字稿：「無法判斷的先進待處理清單」 | Equal to `other`（「待處理：other」） | 是 | 待處理 | 不需要 | 否 | rebuild-guide；BP id8 |

- 四分類以外（如 unknown）或未覆核：在 Router 前的覆核 Filter 停止，ProcessingLog、Drafts 都不新增（CH5-2「自己試」；rebuild-guide）。
- CH5-2：「分類固定值不能同時用『詢價』與inquiry當相同規則，否則Filter可能不匹配。」
- 會議逐字稿出處：A/part5-meeting-transcript.txt（「詢價、客訴、合作與其他四類」）。注意：此檔與 A/part5-form-record.csv **未被現行 Part 5 頁面或 START-HERE 連結**，只出現在 `_backup/2026-10-09-pre-repair/` 舊頁與 manifest。

---

## 4. Make 流程（依執行順序）

### 4.1 Scenario 層級設定（BP `metadata.scenario`）
- 名稱：`gen-ai-36h｜人工覆核後分流｜教學範例`（BP `name`）
- `sequential: true`（= Sequential processing；rebuild-guide、stage-handoff S3-1 要求開啟）
- `dlq: true`（對應「儲存未完成執行」；CH5-4「在Scenario settings開啟儲存未完成執行」。英文介面字樣素材未提及）
- `maxErrors: 3`、`roundtrips: 1`、`autoCommit: true`、`autoCommitTriggerLast: true`、`dataloss: false`、`confidential: false`
- `zone: us1.make.com`
- 排程：教材一律「維持停用」；REPAIR-REPORT「教學 Make Scenario 維持 **Inactive**」。
- BP 共 11 個模組（id 1,4,5,2,9,11,6,7,10,12,8）；REPAIR-REPORT「空白 Scenario 可載入 11 個節點」。
- 錯誤處理模組：BP 無任何 `onerror`／error handler；錯誤處理只靠「儲存未完成執行」＋人工於 Incomplete executions 修復（CH5-4、rebuild-guide 步驟 9）。

### 4.2 模組順序

| 序 | BP id | 模組（介面名） | 設定 | 出處 |
|---|---|---|---|---|
| 1 | 1 | Google Sheets → Watch New Rows（`google-sheets:watchRows`） | Search Method=Enter manually；Spreadsheet ID=`PASTE_YOUR_SPREADSHEET_ID_HERE`；Sheet Name=`ReviewedQueue`；Table contains headers=Yes；Row with headers=`A1:I1`；Limit=`1`；Value render option=Formatted value；Date and time render option=Formatted string | BP id1 `parameters`／`restore`；CH5-1 |
| — | — | 起點 Choose where to start | CH5-1「首次起點選All讀既有測試列；之後正式練習改從現在開始」。BP 未儲存此值（素材未提及於 json） | CH5-1；rebuild-guide 步驟 2 |
| 連線 | 1→4 | 覆核 Filter | 見 4.3 | BP id4 `filter` |
| 2 | 4 | Google Sheets → Make an API Call（`google-sheets:makeAPICall`） | URL=`spreadsheets/PASTE_YOUR_SPREADSHEET_ID_HERE/values/ProcessingLog!A1:A1000`；Method=GET；Headers：`Content-Type: application/json` | BP id4 `mapper`；rebuild-guide 步驟 5 |
| 連線 | 4→5 | 防重 Filter「來源鍵未出現」 | 左 `{{flatten(4.body.values)}}`；運算子 `array:notcontain`（Array operators: Does not contain）；右 `{{1.0}}|{{lower(trim(1.2))}}|{{trim(1.3)}}` | BP id5 `filter`；rebuild-guide「防重 Filter 的位置」表 |
| 3 | 5 | Router（`builtin:BasicRouter`） | 四條路 | BP id5 `routes` |
| 4a | 2 | 路 0：Add a Row → ProcessingLog | 連線 Filter「業務：inquiry」（`1.5` text:equal `inquiry`）；values A=來源鍵、B=`1.5`、C=業務、D=已記錄、E=待建立；Column range `A1:Z1`；Insert data option INSERT_ROWS；Value input option USER_ENTERED | BP id2 |
| 4b | 9 | 路 0：Add a Row → Drafts | A=來源鍵、B=`1.2`、C=`課堂草稿：{{1.3}}`、D=草稿本文模板、E=未寄出；Value input option RAW；Unformatted=true | BP id9 |
| 4c | 11 | 路 0：Update a Cell → ProcessingLog | Cell=`E{{2.rowNumber}}`；Value=`已建立`；Search Method=Enter manually；Value input option=User entered | BP id11；rebuild-guide 步驟 7；stage-handoff S3-3「列號選前面『新增 ProcessingLog』模組輸出的 Row number，不要選 Drafts 的列號」 |
| 5 | 6 | 路 1：Add a Row → ProcessingLog | Filter「客服：complaint」；route=客服、draft_status=不需要；無後續模組 | BP id6 |
| 6a | 7 | 路 2：Add a Row → ProcessingLog | Filter「合作：partnership」；route=合作、draft_status=待建立 | BP id7 |
| 6b | 10 | 路 2：Add a Row → Drafts | 同 id9 | BP id10 |
| 6c | 12 | 路 2：Update a Cell → ProcessingLog | Cell=`E{{7.rowNumber}}`；Value=已建立 | BP id12 |
| 7 | 8 | 路 3：Add a Row → ProcessingLog | Filter「待處理：other」；route=待處理、draft_status=不需要；無後續模組 | BP id8 |

- 沒有寄信模組：「Scenario 排程先維持停用，沒有寄信模組」（rebuild-guide）；「沒有寄信或 Telegram 模組」（REPAIR-REPORT）。草稿是試算表 Drafts 分頁的列。
- 連線：BP 移除帳號連線（各模組 `__IMTCONN__` 參數未填值）與試算表 ID；「匯入後仍須選自己的 Google 連線、填自己的試算表 ID」（rebuild-guide）。四個 Google Sheets 模組類型共用同一 Google 連線（rebuild-guide「使用同一個 Google 連線」）。

### 4.3 覆核 Filter 實際設定

**BP（實跑版，Filter 名「已覆核才讀取」，位於 1→4 連線，11 條全 AND）**：
1. `1.8` text:equal `已覆核`
2. `1.5` text:pattern `^(inquiry|complaint|partnership|other)$`
3–4. `1.0`、`1.1` text:pattern `.+`
5. `1.2`（email）text:pattern `^[^@\s]+@[^@\s]+\.[^@\s]+$`
6–11. `1.3`、`1.4`、`1.5`、`1.6`、`1.7`、`1.8` 各 text:pattern `.+`

**rebuild-guide 教學版（Filter 名「已覆核且九欄完整」，9 條全 AND）**：submitted_at／name／subject／message／summary／next_action 為 Matches pattern `.+`；email 為 `^[^@\s]+@[^@\s]+\.[^@\s]+$`；category 為 `^(inquiry|complaint|partnership|other)$`；review_status 為 Equal to `已覆核`。

【不一致】
- 條數與名稱：BP 11 條、名「已覆核才讀取」；指南 9 條、名「已覆核且九欄完整」。
- 多出的兩條：BP 對 category（`1.5`）與 review_status（`1.8`）除了樣式／等於條件，另各多一條 `.+`；指南沒有這兩條。邏輯效果相同（多出的是重複檢查），但學員照指南建出的不是 BP 的逐條複本。
- 位置隨階段改變：S2 在 Watch New Rows→Router；S3 起在 Watch New Rows→Make an API Call（stage-handoff S2→S3、rebuild-guide）。BP 為 S3 最終狀態。

### 4.4 文件與 BP 的其他差異（改寫時需選定一方）
- Drafts recipient：stage-handoff 寫固定「learner@example.com」；BP 映射來源 email `{{1.2}}`。T 測試列的 email 全是 learner@example.com，所以實跑結果相同；但 U／N 原文 email 為 learner01～learner12@example.com，若直接跑 BP 會把來源 email 寫入 recipient。
- Drafts subject：handoff「原主旨」vs BP「課堂草稿：＋主旨」。
- ProcessingLog error 欄：見 2.3，BP 不寫。
- S1 的 source_key：CH5-1 只說「先以submitted_at、email、subject合成」，未要求 lower／trim；正規化寫法從 S3（rebuild-guide 步驟 5）才出現，stage-handoff S3-2 表則把正規化寫法列為 ProcessingLog source_key。

---

## 5. 練習訊息

### 5.1 T 系列：Make 工程測試列（`A/part5-test-inputs.csv` 九欄＋test_case；說明見 `A/part5-test-cases.csv`）
PRAC5：「T01–T07 是固定的 Make 工程測試列，不是 AI 產出」。

| 代碼 | 擬內容稱呼 | 九欄原文（submitted_at／name／email／subject／message／category／summary／next_action／review_status） | 應有結果 | 特殊情況 |
|---|---|---|---|---|
| T01 | 小林問基礎方案月費那則 | 2026-10-09T09:00／小林／learner@example.com／詢問方案／請問基礎方案月費／inquiry／詢問基礎方案／建立給本人測試草稿／已覆核 | 業務；一份未寄出草稿；「來源鍵與分類正確」 | 與 reviewed-queue 第 1 列完全相同 |
| T02 | 小安反映商品沒準時交付那則 | 2026-10-09T09:05／小安／learner@example.com／交期問題／商品未準時交付／complaint／反映交期／人工客服覆核／已覆核 | 客服；零份；「人工處理標記」 | 同 reviewed-queue 第 2 列 |
| T03 | 小周想談共同活動那則 | 2026-10-09T09:10／小周／learner@example.com／合作邀約／想討論共同活動／partnership／詢問合作／建立給本人測試草稿／已覆核 | 合作；一份未寄出；「僅測試本人」 | 同 reviewed-queue 第 3 列 |
| T04 | 小陳說謝謝教材那則 | 2026-10-09T09:15／小陳／learner@example.com／一般訊息／謝謝教材／other／致謝／記錄待處理／已覆核 | 待處理；零份；「紀錄存在」 | 同 reviewed-queue 第 4 列 |
| T05a | 還沒覆核的月費詢問 | 2026-10-11T10:05／小林／learner@example.com／詢問方案／請問基礎方案月費／inquiry／詢問基礎方案／建立給本人測試草稿／**待覆核** | 覆核 Filter 阻擋；零份 | 刻意無效；只在停排程的隔離副本測（PRAC5） |
| T05b | 分類填錯成 unknown 的月費詢問 | 2026-10-11T10:06／小林／…／詢問方案／請問基礎方案月費／**unknown**／詢問基礎方案／建立給本人測試草稿／已覆核 | 阻擋；零份 | 同上 |
| T06 | 再送一次的小林月費詢問 | 與 T01 九欄完全相同（2026-10-09T09:00…已覆核） | 「重複」；紀錄與草稿不新增 | 重複來源鍵。【不一致】CSV 中 T06 與 T01 無任何大小寫或空白差異；REPAIR-REPORT 卻記實跑 T06「大小寫 email 與主旨前後空白正規化後被擋」。實跑所用 T06 原值素材未提及 |
| T07 | 故障恢復測試那則 | 2026-10-11T10:07／小林／learner@example.com／**故障恢復測試**／請問基礎方案月費／inquiry／詢問基礎方案／建立給本人測試草稿／已覆核 | 原分類（業務）；最多一份有效草稿；「保留錯誤並從失敗步驟重跑」 | 先製造 Drafts 表名錯誤才追加（見第 6 節） |

其他固定列：
- **S3 查重驗證列**（rebuild-guide）：`2026-10-11T11:00,小林,learner@example.com,S3查重驗證,請問基礎方案月費,inquiry,詢問基礎方案,建立未寄出教學草稿,已覆核`；鍵 `2026-10-11T11:00|learner@example.com|S3查重驗證`。第一次應新增一筆紀錄與草稿，原樣再追加應兩表不增加。
- **CH5-1 改舊列練習**：Source 第 2 列 message「請問基礎方案月費」改「請問基礎方案費用」（sheet-layout、CH5-1），應不觸發。
- `A/part5-reviewed-queue.csv` 四列 = T01–T04 九欄（CH5-1 稱「小林／詢問方案」「小安／交期問題」）。

### 5.2 U 系列：未分類原文（`A/part5-unclassified-messages.csv`，欄位 case_id,source_id,submitted_at,name,email,subject,message；答案 `A/part5-classification-answer-key.md`）

| 代碼 | 擬內容稱呼 | 原文（source_id／時間／姓名／email／主旨／內容） | 應有分類（答案鍵） | 特殊情況與答案鍵處理 |
|---|---|---|---|---|
| U01 | 問月費又抱怨沒回覆那則 | SRC-U01／2026-10-01 09:10／陳怡安／learner01@example.com／方案費用與回覆延遲／請問基礎方案月費？上週問過還沒收到資料，能今天回覆嗎？ | complaint（主要） | 多重意圖；next_action「人工先查回覆紀錄與核准價格；確認是否拆成兩件」；「人工判定前不得路由」 |
| U02 | 引用去年週六時間、問今年週末那則 | SRC-U02／2026-10-01 09:12／王小明／learner02@example.com／週末服務時間／引用舊信：去年週六營業到18:00。這次想確認今年週末服務時間。 | inquiry | 引用舊資料；「舊信是引用背景，不是今年證據」 |
| U03 | 邀請參加免費講座、問窗口那則 | SRC-003／2026-10-01 09:15／林可／learner03@example.com／合作講座／我們想邀請你們參加免費講座，請問窗口？ | partnership | 「不得承諾參加」；與 U04 同鍵 |
| U04 | 說自己是重複提交的更正信 | SRC-003／2026-10-01 09:15／林可／learner03@example.com／合作講座／更正：這是重複提交；請以前一封為準。 | 不建立第二列 | 重複：與 U03 同 source_id、同時間／email／主旨 → 同來源鍵；不入 ReviewedQueue |
| U05 | 沒留姓名和 email 的退款查詢 | SRC-U05／2026-10-01 09:20／（空）／（空）／退款進度／我的退款還沒收到，請協助查詢。 | 不填 | 缺欄位；不建立九欄列、不猜姓名或 email；candidate-example：「不使用『未知@example.com』湊九欄」 |
| U06 | 等三天才回覆、表達失望那則 | SRC-U06／2026-10-01 09:25／周芸／learner06@example.com／服務回饋／我等了三天才收到回覆，這個處理方式讓我很失望。 | complaint | CH5-3 要學員「判斷 U06 的主要意圖」；客服人工處理，不建草稿 |
| U07 | 問平日幾點營業那則 | SRC-U07／2026-10-01 09:30／吳立／learner07@example.com／服務時間／請問你們平日幾點營業？ | inquiry | CH5-3 示範題；具體時段未知「不能補時段」；完整九欄參考見 candidate-example（「不是一次實際模型輸出」） |

U07 參考九欄（candidate-example）：`2026-10-01 09:30,吳立,learner07@example.com,服務時間,請問你們平日幾點營業？,inquiry,詢問平日營業時間,查正式營業時間後擬未寄出草稿,待覆核`。
答案鍵 summary／next_action 全表：U01「詢問基礎方案月費，並反映上週詢問尚未獲回覆」；U02「詢問今年週末服務時間」／「查本年度正式營業時間；不要沿用引用舊信的去年時間」；U03「提出免費講座合作並詢問窗口」／「由合作窗口評估並回覆草稿」；U06「反映回覆延遲並表達不滿」／「人工檢查服務紀錄並分派客服」；U07「詢問平日營業時間」／「查正式營業時間後擬未寄出草稿」。所有可建列 review_status＝待覆核。

### 5.3 N 系列：PRAC5 獨立批次（`A/part5-solo-messages.csv`；答案 `A/part5-solo-answer.md`）

| 代碼 | 擬內容稱呼 | 原文（source_id／時間／姓名／email／主旨／內容） | 應有分類 | 特殊情況 |
|---|---|---|---|---|
| N01 | 邀請一起開課、費用日期未談那則 | SRC-N01／2026-10-11 09:00／林晴／learner11@example.com／合作課程／想邀請貴團隊一起開課；費用與日期都尚未討論。 | partnership | 「不承諾費用或日期」 |
| N02 | 付款後沒收到貨、不要再傳廣告那則 | SRC-N02／2026-10-11 09:05／張明／learner12@example.com／訂單延誤／上週已付款仍未收到商品；請查出貨狀態，不要再傳方案廣告。 | complaint | 「來源主張付款與延誤，不等於已由公司查證」；路由不產草稿 |
| N03 | 大寫 email 加空白的「請勿重複處理」補充信 | SRC-N01-COPY／2026-10-11 09:00／林晴／` LEARNER11@EXAMPLE.COM `（前後空白、大寫）／` 合作課程 `（前後空白）／補充上一封：請勿重複處理。 | 不建立第二個輸出 | 正規化後與 N01 同鍵；「source_id 不同不會改變本課去重規則」 |
| N04 | 沒留 email 的團體方案詢問 | SRC-N04／2026-10-11 09:10／陳安／（空）／方案詢問／想瞭解團體方案；請告知可提供哪些資料。 | 分類素材未提及 | 缺 email，「停止入列，保留 Source 與補件要求，不猜地址」 |

### 5.4 未連結的舊素材
`A/part5-form-record.csv`：4 列（林怡君／陳柏安／周雅雯／王志明，2026-09-07，review_status 全為待覆核）。現行 Part 5 頁面與 START-HERE 未連結，只出現在 `_backup/` 舊版頁。

---

## 6. 故障恢復練習（T07）

- **製造方式**：「先停Scenario排程，確認只有一筆虛構測試。在Scenario settings開啟儲存未完成執行。把詢問路的Drafts目標表暫改成不存在的教學表名，再執行T07」（CH5-4）；rebuild-guide 步驟 9 同義。
- **故障當下的預期狀態**：「`ProcessingLog` 留一筆 `待建立`、Drafts 無該鍵，Make 出現未完成執行」（rebuild-guide 步驟 9）；REPAIR-REPORT【實跑】「上游紀錄保留 `待建立`、草稿無新增；Make 留下未完成執行」。
- **錯誤訊息原文**：素材未提及。截圖 `R/make-t07-error.png`（2026-10-09 17:45）用途為「T07 錯誤畫面」（REPAIR-REPORT），本清單未檢視圖片內容。
- **正確恢復步驟**（CH5-4、rebuild-guide 步驟 9–10）：
  1. 開 Incomplete executions 的該筆 Details。
  2. 在該失敗執行內把錯誤模組修回 `Drafts`，Save。
  3. 按 Run once，從失敗步驟（草稿寫入與狀態回寫）繼續。
  4. 主流程也修回正確目標表，供未來新列使用。
  5. 核對：ProcessingLog 仍一列、draft_status＝已建立；Drafts 同鍵一份「未寄出」；未完成執行顯示 Resolved。
  6. 確認恢復路徑後才重新啟動排程。
- **實跑紀錄**【實跑】：「修正表名後從該執行重試兩個下游操作，顯示 Resolved；來源鍵只留一筆紀錄、一份草稿，紀錄改為 `已建立`」（REPAIR-REPORT）；rebuild-guide「本次教學工作區 T07 由錯誤到恢復共重試兩個操作，沒有重寫上游紀錄」。
- **不可重跑整筆的原因**：
  - 「不要從 Watch New Rows 再跑整筆」（rebuild-guide 步驟 9）。
  - 「只改主流程再按 Retry，可能仍用失敗時舊設定」（CH5-4）；「本課表名設定錯誤使用 Details 內修正並保存；單純 Retry 適合暫時連線錯誤」（CH5-4）。
  - 「若草稿已存在，不應再執行會新增草稿的步驟」（rebuild-guide）。
  - 素材未明寫「從頭重跑時防重會擋下、草稿因此永遠建不出來」這類機制說明；只說上游紀錄已寫入、要「從失敗步驟恢復」。
- **CH5-4 故障對照表**（原文）：未覆核被擋→Source人工核對，「不改Filter繞過」；Google寫入無權限→Google連線或目標表，「保留來源鍵，恢復同一教學表權限」；紀錄已寫、草稿失敗→草稿步驟，「查同鍵草稿是否存在，再恢復」；相同來源重複→防重查詢，「不改提交時間避開防重」。
- 官方依據連結：https://help.make.com/manage-incomplete-executions（CH5-4、rebuild-guide）。

---

## 7. 驗證狀態

### 7.1 已在教學工作區實跑【實跑】
- 日期與範圍：「2026-10-09 已用教學工作區實跑 T01–T07：四路分流、未覆核／錯分類阻擋、重複來源鍵阻擋、草稿狀態回寫，以及失敗後從未完成執行恢復。Scenario 排程維持停用。」（R/ENVIRONMENT.md）
- 「Make／Google Sheets 教學工作區全路徑：T01–T07 PASS；去識別 Blueprint 來自實跑Scenario。」（ENVIRONMENT「目前證據」）
- 授權：「使用者已登入並授權教學 Make 工作區試跑。T01–T07以虛構資料完成，Scenario維持停用」（R/PROGRESS.md Ruling）。
- 逐案觀察（REPAIR-REPORT「Part 5 實跑紀錄」）：T01／T03 各建一份未寄出草稿，「新增的完整路徑測試把紀錄 `draft_status` 回寫為 `已建立`」；T02／T04 無草稿；T05 在覆核 Filter 停止；T06 被擋；T07 見第 6 節。
- 實跑設定：「一次處理一列、開啟 Sequential processing 與儲存未完成執行」；「防重讀 `ProcessingLog!A1:A1000`；這個教學範圍不保證大量資料或並行寫入」。
- 證據檔（R/）：
  - `make-flow-verified.png`（2026-10-09 23:31）—「流程畫面」
  - `make-t07-error.png`（2026-10-09 17:45）—「T07 錯誤畫面」
  - `make-blueprint-import.png`（2026-10-09 23:36）—「去識別 Blueprint 試匯入畫面」
- 附註（REPAIR-REPORT）：「初期階段測試留下的兩筆 `待建立` 記錄已註明當時尚未啟用草稿模組；後來已生成草稿的兩筆舊測試紀錄有明示的人工狀態校正註記，未冒稱自動回寫。」

### 7.2 未操作／待驗
- **Blueprint 匯入後重綁另一帳號並完整重跑**：「**匯入後重綁另一個帳號並完整重跑尚未驗證**」（REPAIR-REPORT）；只驗到「空白 Scenario 可載入 11 個節點，並如預期要求重新設定連線」。
- **學員端**：「學員的帳號、連線及當日介面仍須各自重驗」（ENVIRONMENT）；頁面 frontmatter「開課當日須重查介面」。
- **CH5-3 的 AI 段（把原文交給生成式 AI 產九欄候選）**：素材沒有任何實際模型輸出證據；candidate-example 明說參考值「不是一次實際模型輸出」。ENVIRONMENT／REPAIR-REPORT 把「Claude 基本對話…指定帳號實跑」列為 PENDING。
- **N01–N04 經 Make 跑過**：素材未提及（PRAC5 規定 N 列不拿去替代 T 測試）。
- **S1／S2 分階段改接流程（Add a router 插入、S2→S3 插入 API Call）由學員從頭建**：素材未提及實跑證據；實跑紀錄針對最終 T01–T07。
- **真人試走、瀏覽器版面**：PENDING（REPAIR-REPORT「尚未完成的放行證據」1、3）。整課狀態 `MACHINE_READY_PENDING_HUMAN`。
- **官方設定位置核對**：rebuild-guide「設定位置核對（2026-10-11）」列 Filter、Router、單獨測試模組三個官方說明頁；這是文件核對，非實跑。
- **內容審查**：每頁教師段「本次單一 agent 自審；無獨立 reviewer 或真人試走證據」。

### 7.3 需要的帳號／權限
- 「Google Sheets、Make 帳號及可授權的教學用 Google 連線」（ENVIRONMENT）；CH5-1「需要Google帳號、Make帳號與可授權的教學試算表。沒有連線權限時停在表格演練，不能記自動化已完成」。
- 生成式 AI 帳號（CH5-3；沒有時標 AI `NOT_RUN`）。素材未指定哪一家；教學計畫寫 Part 1–2 以 Claude 為共同路徑（R/REPAIR-PLAN.md 第 36 行），Part 5 頁面只寫「生成式 AI」。
- Make 方案等級、操作次數限額：素材未提及（CH5-4 只說每週查「連線、限額、異常與未完成執行」）。

---

## 8. 現有頁面中的人工作業清單

| # | 人工作業 | 原句與出處 |
|---|---|---|
| 1 | 手動把示例列逐格貼進兩張表 | 「從已覆核示例 CSV 只取第一筆『小林／詢問方案』，九欄資料各放一格，分別貼入 Source 與 ReviewedQueue 的第 2 列。」（CH5-1） |
| 2 | 人工核對 bundle 值與映射 | 「核對輸入是inquiry、來源時間2026-10-09T09:00、主旨詢問方案；紀錄的category應仍是inquiry。」（CH5-1） |
| 3 | 手改 Source 舊列做對照 | 「把 Source 第 2 列 message 中的『請問基礎方案月費』改為『請問基礎方案費用』」（CH5-1） |
| 4 | 逐筆追加測試列並每次 Run once | 「依T01到T04逐一加ReviewedQueue新列，每次Run once並查執行中的資料單位（bundle）、路徑與結果表。」（CH5-2） |
| 5 | 手動檢查分類值大小寫／空白 | 「沒有路徑時檢查實際category有無大小寫或空白」（CH5-2） |
| 6 | 手動追加無效列並記錄 | 「追加一筆review_status=待覆核…再測category=unknown…記錄輸入、阻擋條件與結果」（CH5-2） |
| 7 | 先記筆數再比對 | 「先記下 ProcessingLog 筆數，再逐筆追加完整測試列中的 T01–T04」（rebuild-guide） |
| 8 | 逐欄比對 AI 候選與參考值 | 「逐欄比對課程編寫的參考值…記下 AI 哪欄正確、哪欄需修及原文依據」（CH5-3） |
| 9 | 人工判斷多重意圖與拆分 | 「U01 同時問價格、反映回覆延遲；你要判斷主要分類、是否拆分，以及是否交人處理。」（CH5-3） |
| 10 | 學員自行計算來源鍵 | 「再由你自行計算 U03／U04 的來源鍵、檢查 U05 九欄完整性及判斷 U06 的主要意圖。」（CH5-3） |
| 11 | 人工改狀態並追加佇列 | 「才把 `review_status` 改成『已覆核』並追加 ReviewedQueue」（CH5-3） |
| 12 | 人工到 ProcessingLog 查鍵是否已存在 | 「人工核對五個來源值、分類理由、摘要與下一步後，再查 ProcessingLog 是否已有來源鍵」（candidate-example） |
| 13 | 新鍵使用前先人工搜尋 | 「使用前先在 ProcessingLog A 欄搜尋完整新鍵…確認尚不存在」（rebuild-guide） |
| 14 | 保存三份紀錄 | 「保存原文、AI 候選、人工修訂與決定。」（CH5-3） |
| 15 | 每接一個模組就查表 | 「每完成一個動作就查表，不一次接完才看綠勾。」（CH5-3） |
| 16 | 手動重送相同九欄測防重 | 「再追加完全相同九欄，兩張輸出表都不增加。保存兩次執行與表格證據。」（CH5-3） |
| 17 | 手動選欄位建映射、不照抄編號 | 「手動新建模組時編號可能不同，應從 Make 的欄位選單點選欄位，不直接照抄數字。」（rebuild-guide） |
| 18 | 手動複製 Filter 樣式 | 「分類四選一放在同一個 Matches pattern 條件，直接複製表內樣式」（CH5-2） |
| 19 | 從執行記錄人工回查 | 「點最近一次execution，查輸入bundle、最後成功模組與第一個錯誤模組。紀錄來源鍵、stage、錯誤訊息、ProcessingLog與Drafts是否已有行。」（CH5-4） |
| 20 | 手動製造故障並在 Details 修回 | 「把詢問路的Drafts目標表暫改成不存在的教學表名…在這份失敗執行內將錯誤模組修回 Drafts 並 Save」（CH5-4） |
| 21 | 寫接手說明 | 「寫下觸發來源、九欄規格、最後成功紀錄、常見錯誤、停止方式與恢復位置。」（CH5-4） |
| 22 | 逐筆核對 N 列五項 | 「再由你逐筆核對主要分類、九欄完整性、正規化來源鍵、補問或人工接手理由，以及是否可覆核。」（PRAC5） |
| 23 | 追加前手動刪 test_case 欄 | 「新增欄位 test_case 只用於定位，追加前移除該欄」（PRAC5） |
| 24 | 手動建空白測試副本 | 「使用新的教學表或保存原證據後建立空白測試副本，表內只留表頭」（PRAC5） |
| 25 | 手測七案並逐案記錄 | 「逐案記輸入、execution ID／截圖、結果列、草稿數和判定。」（PRAC5） |
| 26 | 草稿內容人工查核 | BP 草稿本文「此為課堂未寄出草稿，請人工查核承諾與聯絡資訊。」；rebuild-guide「內容留『人工查核』提醒」 |

---

## 9. 外部平台名稱與介面用語

### 9.1 Make（可能需保留的英文字樣）
- 物件：Scenario、Blueprint、module、bundle、execution、execution ID、Router、Filter（CH5-1～4、rebuild-guide、PRAC5）
- 執行：Run once、Run this module（部分介面顯示 Run this module only）、Scenario settings、Sequential processing、Incomplete executions、Details、Save、Retry、Resolved、Inactive（rebuild-guide、CH5-4、REPAIR-REPORT）
- 儲存未完成執行的英文介面字樣：素材未提及（BP 欄位為 `dlq: true`）
- Router 插入：右鍵連線 → **Add a router**（stage-handoff）
- Filter：AND（全部符合）、Text operators、Text: Matches pattern、Text: Equal to、**Array operators: Does not contain**（陣列不包含）（rebuild-guide）
- 函數：`flatten`、`lower`、`trim`；映射 `body → values`、Row number／`rowNumber`（rebuild-guide、stage-handoff、BP）
- Watch New Rows 起點：Choose where to start → All（rebuild-guide 步驟 2；CH5-1 寫「首次起點選All」）

### 9.2 Google Sheets 模組（Make 內）
- Google Sheets → **Watch New Rows**：Connection、Search Method（Enter manually）、Spreadsheet ID、Sheet Name、Table contains headers（Yes）、Row with headers、Limit、Value render option（Formatted value）、Date and time render option（Formatted string）（BP id1 metadata）
- Google Sheets → **Add a Row**：Search Method、Spreadsheet ID、Sheet Name、Column range（A-Z）、Values in columns、Insert data option、Value input option、Unformatted（BP id2 metadata）
- Google Sheets → **Update a Cell**：Search Method、Spreadsheet ID、Sheet Name、Cell、Value、Value input option（User entered）（BP id11 metadata）
- Google Sheets → **Make an API Call**：URL、Method（GET）、Headers、Query String、Body（BP id4 metadata）
- 分頁名（英文，需與 Make 設定一致）：Source、ReviewedQueue、ProcessingLog、Drafts
- 試算表 ID 取法：「Google Sheets 網址 `/d/` 與 `/edit` 之間那段」（rebuild-guide）
- 錯誤碼：「若 403 或找不到表，先回連線、試算表 ID 或分頁名修復」（rebuild-guide）

### 9.3 Gmail 與其他
- 主線流程無 Gmail 模組，草稿存在 Sheets 的 Drafts 分頁（rebuild-guide「沒有寄信模組」；REPAIR-REPORT）。
- Gmail、Gemini、Telegram、Google Docs、Webhook、HTTP 只出現在講師延伸的五份「AI 秘書」藍圖（A/part5-existing-blueprints-guide.md），原檔「不隨學員講義附上」，「部分分支會寄信或傳送 Telegram 訊息」。
- n8n（選做）、LINE Notify（已終止，不用）（CH5-2）。
- 官方文件連結（教材已引用）：apps.make.com/google-sheets-modules、help.make.com/array-functions、help.make.com/manage-incomplete-executions、help.make.com/filtering、help.make.com/router、help.make.com/step-6-test-the-module。

---

## 附：改寫前需裁決的不一致（彙整）
1. 覆核 Filter：BP 11 條「已覆核才讀取」vs 指南 9 條「已覆核且九欄完整」（4.3）。
2. Drafts recipient：固定 learner@example.com（handoff）vs 映射來源 email（BP）（4.4）。
3. Drafts subject：原主旨 vs 「課堂草稿：」前綴（4.4）。
4. ProcessingLog error 欄：指南說寫錯誤文字，BP 從不寫（2.3）。
5. T06：CSV 與 T01 完全相同 vs 實跑報告說測了大小寫／空白正規化（5.1）。
6. 提交時間格式：T 列 `2026-10-09T09:00` vs U／N 列 `2026-10-01 09:30`；兩種都進同一來源鍵規則，素材未說明是否需統一。
7. S1 來源鍵未正規化 vs S3 起正規化（4.4）。
