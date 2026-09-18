# Coverage Ledger：AI 入門即戰力

## Pass 1 — frozen atom inventory（CH1-1 代表單元）

| atom_id | classification | atom_kind | required_evidence_ids | operation_id/objective_anchor | first teaching location |
|---|---|---|---|---|---|
| CH1-A01 | core | concept comparison | E-01,E-02,E-03 | OP-01 / LLM 與搜尋的差異 | SECTION 02 |
| CH1-A02 | core | prompt framework | E-04,E-05,E-06 | OP-01 / 五欄提示詞 | SECTION 02-03 |
| CH1-A03 | core | worked operation | E-07,E-08,E-09,E-10 | OP-01 / 自我介紹提問 | SECTION 02-1 |
| CH1-A04 | core | worked operation | E-11,E-12,E-13 | OP-02 / 即時問題的限制與改問 | SECTION 02-1 |
| CH1-A05 | core | worked operation | E-14,E-15,E-16 | OP-02 / 晚餐建議 | SECTION 03 |
| CH1-A06 | core | worked operation | E-17,E-18,E-19 | OP-01 / ETF 白話解釋 | SECTION 02-1 |
| CH1-A07 | core | worked operation | E-20,E-21,E-22 | OP-01 / 通知整理 | SECTION 02-1 |
| CH1-A08 | core | revision transfer | E-23,E-24,E-25 | OP-02 / 太長、太正式、再短一點 | SECTION 04 |
| CH1-A09 | core | finished artifact | E-26,E-27,E-28 | OP-01,OP-02 / 保存實務紀錄 | SECTION 05 |
| CH1-A10 | supporting | recovery | E-29,E-30 | OP-01,OP-02 / 無法使用 LLM 時的備援 | SECTION 07 |

## Pass 2 — to complete after representative handout exists

| atom_id | classification | atom_kind | required_evidence_ids | operation_id/objective_anchor | first teaching location | quoted evidence | raw input | learner action | finished artifact | verification | repair | artifact-chain location |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CH1-A01 | core | concept comparison | E-01,E-02,E-03 | OP-01 / LLM 與搜尋的差異 | CH1-1.html#lesson-concept | 「搜尋問題」目標是找到外部資料；「對話任務」目標是讓 LLM 依條件產生初稿 | 阿凱的「去日本旅遊」需求與晚餐需求 | 讀兩種任務說明並指出目標 | 能說明一項需求應先找資料或先交給 LLM 處理 | 對照課堂提供的兩種寫法，回到 SECTION 02 | CH1 → CH2 |
| CH1-A02 | core | prompt framework | E-04,E-05,E-06 | OP-01 / 五欄提示詞 | CH1-1.html#lesson-concept；#lesson-demo | 「情境、任務、資料、條件、格式」表格逐欄給出晚餐例子 | 「幫我想晚餐」與兩人、不吃牛、600 元、30 分鐘條件 | 將模糊需求補成五欄 | 五欄都有具體值且能組成一句提示詞 | 缺欄位時回到 SECTION 02 表格補值 | CH1 → CH2 |
| CH1-A03 | core | worked operation | E-07,E-08,E-09,E-10 | OP-01 / 自我介紹提問 | CH1-1.html#lesson-example-bank 案例 1；#lesson-practice 步驟 2 | 案例 1 同時給出完整輸入、可用輸出、過度承諾錯例與修正指令；步驟 2 要學員對照後實跑 | 頁內工作台第 1 題 | 先讀案例 1，再複製提示詞、送出、貼回回答並填觀察 | 工作台出現自我介紹回答、觀察與可重做修正 | 偏題或過度承諾時追加「列出三類文字協助並標示需要確認的內容」再跑一次 | CH1 |
| CH1-A04 | core | worked operation | E-11,E-12,E-13 | OP-02 / 即時問題的限制與改問 | CH1-1.html#lesson-example-bank 案例 2；#lesson-practice 步驟 3 | 案例 2 示範無即時資料時的完整停損輸出，並對照沒有時間與來源的晴雨錯例 | 頁內工作台第 2 題 | 先讀案例 2，再送出天氣問題並填寫日期、時間、來源或無法判斷的原因 | 工作台保留回答依據與下一步查證方向 | 缺少時間或來源時追加「先說明資料時間與來源；無法取得時不要自行填寫數字」 | CH1 |
| CH1-A05 | core | worked operation | E-14,E-15,E-16 | OP-02 / 晚餐建議 | CH1-1.html#lesson-demo；#lesson-practice 步驟 4 | 完整示範提供模糊輸入、五欄條件、三列輸出表與四條件核對 | 頁內工作台第 3 題 | 送出晚餐提示詞並在工作台圈出兩人、不吃牛、600 元、30 分鐘四個條件 | 表格含三個選項、時間、預算與仍缺條件的說明 | 忽略條件時只補被忽略的條件再跑一次，保留原版作比較 | CH1 |
| CH1-A06 | core | worked operation | E-17,E-18,E-19 | OP-01 / ETF 白話解釋 | CH1-1.html#lesson-example-bank 案例 4；#lesson-practice 步驟 5 | 案例 4 給出一句定義、生活例子、三個待查問題，以及把解釋誤寫成推薦的錯例 | 頁內工作台第 4 題 | 先讀案例 4，再送出提示詞、用自己的話重述 ETF 並填待查問題 | 重述包含一籃子資產與市場交易兩個意思，且沒有商品推薦 | 太專業或開始推薦時追加「只做概念解釋，不推薦商品」 | CH1 |
| CH1-A07 | core | worked operation | E-20,E-21,E-22 | OP-01 / 通知整理 | CH1-1.html#lesson-example-bank 案例 5；#lesson-practice 步驟 6 | 案例 5 給出原文、三個完整條列、五項資訊核對與漏掉時間的錯例 | 頁內工作台第 5 題 | 先讀案例 5，再整理通知成三個條列並在工作台逐項標記五項資訊 | 三個條列保留日期、所有時間、住戶行動與雨天備案，未加入新規定 | 漏掉重要時間時追加「先列出五項資訊，再整理成三個條列」並重跑 | CH1 |
| CH1-A08 | core | revision transfer | E-23,E-24,E-25 | OP-02 / 修改指令 | CH1-1.html#lesson-practice 步驟 8 | 晚餐完整示範與步驟 8 都要求比較第一版與第二版，且每輪只改一個條件 | 任一前面完成的回答 | 輸入縮短、改語氣或改表格其中一項 | 能說明這次改變的條件與保留內容 | 同時改太多時回到 U1-REVISE，只留一個指令 | CH1 → CH2 |
| CH1-A09 | core | finished artifact | E-26,E-27,E-28 | OP-01,OP-02 / 保存實務紀錄 | CH1-1.html#lesson-practice 步驟 9；#lesson-check | 保存步驟與完成驗證明定五題、前後版本、starter／個人三段紀錄、待查項目與檢查方式 | 頁內工作台的填寫內容 | 按工作台「匯出 Markdown」產出 `unit1-practice-sheet-complete.md` 並逐項檢查 | 沒參加課程的人能看懂原始問題、回答、個人轉移與待查處 | 缺原始提示詞時回到 U1-SAVE 用「複製提示詞」補回，不刪除既有回答 | CH1 → CH2/CH4 |
| CH1-A10 | supporting | recovery | E-29,E-30 | OP-01,OP-02 / 備援 | CH1-1.html#lesson-start；#lesson-practice；#lesson-assets | 頁面提供離線備援結果與使用限制，且案例庫已先給正常路徑的示例 | `assets/fallback/unit1-dialogue-simulator.md` | 先用備援完成五題輸入條件與示例判讀，恢復後重做自己的五次對話 | 能指出備援能完成判讀但不能代替五次對話 | 回到 U1-START 或 U1-ASK，依缺失階段重做 | CH1 |

## Freeze rule

Pass 1 與 Pass 2 的 atom ID 與 classification 必須相同。若完整講義發現新增、拆分、合併或降級，先記錄原因與 reviewer verdict，再更新兩個 pass。

## Full-course supplement：CH2–CH4 與課後整合

本節保留 CH1-1 代表單元的原子編號，補上其餘 learner-facing 頁面的核心操作。每個 atom 都對應實際 section／stage ID、學員動作、完成物、驗證與修復位置；這份補充不把四頁的完成線當成內容證據的替代品。

| atom_id | classification | operation_id / evidence | learner action | finished artifact | verification / repair | handout location |
|---|---|---|---|---|---|---|
| CH2-A01 | core | OP-03 / 四段式提示詞 | 從素材包標出背景、任務、限制、輸出格式 | 可貼上的 Email 提示詞 | 四段都有值；缺段回 U2-PROMPT | CH2-1 `U2-START`、`U2-PROMPT` |
| CH2-A02 | core | OP-03 / Email 事實邊界 | 用固定背景產出主旨、正文、署名 | 1 封 Email 與第一版 | 12,000 元、7 個工作天、貼文數量追問保留；自造內容回 U2-EMAIL | CH2-1 `U2-EMAIL`、`U2-CHECK-2` |
| CH2-A03 | core | OP-03 / 讀者與下一步 | 把 Email 情境換成一則 2–4 句訊息 | 1 則訊息與第一版 | 收件者知道下一步；像 Email 回 U2-MESSAGE | CH2-1 `U2-MESSAGE` |
| CH2-A04 | core | OP-03 / 同資料三場合 | 用同一份資料表產出社交、交友、求職三版 | 3 版自我介紹與提示詞 | 圈出共同事實，再遮標題判斷用途；幾乎相同回 U2-INTRO | CH2-1 `U2-INTRO` |
| CH2-A05 | core | OP-03 / 單一變因迭代 | 至少兩份成品各只改一個主要條件 | 前後版本與修改理由 | 寫出改了什麼、保留什麼；刪掉關鍵事實回 U2-ITERATE | CH2-1 `U2-ITERATE`、`U2-SAVE` |
| CH3-A01 | core | OP-04 / 來源建立 | 建立主題筆記本並加入 3 份課堂來源 | 含來源的 NotebookLM 筆記本 | 來源列表有 3 個可辨認名稱；失敗回 U3-SOURCE | CH3-1 `U3-START`、`U3-SOURCE` |
| CH3-A02 | core | OP-05 / 摘要層次 | 對同一篇新聞提出一句話、約 200 字、約 300–350 字 | 三段式新聞摘要 | 主旨一致、286 與 174 保留；太短回 U3-SUMMARY | CH3-1 `U3-SUMMARY` |
| CH3-A03 | core | OP-04 / 引用回查 | 點開至少一個正式引用，回到原文核對數字或限制 | 引用核對紀錄 | 引用能回到原文；對不上拆短句回 U3-CITE | CH3-1 `U3-CITE`、`U3-SAVE` |
| CH3-A04 | core | OP-05 / 公告欄位 | 從公告整理可能影響誰、期限／條件／文件、下一步 | 公告白話重點卡 | 每欄有引用或「來源未提及」；缺欄回 U3-ANNOUNCE | CH3-1 `U3-ANNOUNCE` |
| CH3-A05 | core | OP-05 / 書籍行動 | 從書籍節錄整理 5 個重點、3 個一週行動並區分作者與延伸 | 書籍行動筆記 | 重點可回查、行動有時間／情境；空泛回 U3-BOOK | CH3-1 `U3-BOOK` |
| CH4-A01 | core | OP-06 / 條件進入結果 | 從主卡填目標、時間、預算、偏好、限制 | 個人條件清單 | 目標可看見、限制至少 1 項；缺欄回 U4-SELECT | CH4-1 `U4-SELECT` |
| CH4-A02 | core | OP-06 / 四段式生活任務 | 把條件寫成背景、任務、限制、輸出格式 | 個人化提示詞 | 必填條件逐一圈出；泛問回 U4-PROMPT | CH4-1 `U4-PROMPT` |
| CH4-A03 | core | OP-06 / 共同素材比較 | 只用冷氣素材整理規格，缺資料寫「未提供」 | 比較表與 3 個人工確認問題 | 對照 L0 truth table；發生額外評價回共同素材段落重問 | CH4-1 冷氣比較段、`U4-CHECK-1` |
| CH4-A04 | core | OP-06 / 單一變因轉移 | 保存第一版，只改一個條件，再轉到同一張主卡 | 第一版、修訂指令、修正版 | 只能指出一個主要變因；多項變更回 U4-REVISE／U4-TRANSFER | CH4-1 `U4-SAVE-1`、`U4-REVISE`、`U4-TRANSFER` |
| CH4-A05 | core | OP-06 / 可重做保存 | 將原始需求、提示詞、兩版與檢核放在同一份文件 | `unit4-lifestyle-application-card.md` | 隨機開啟仍找得到兩版與待確認事項；缺段回 U4-SAVE-2 | CH4-1 `U4-SAVE-2` |
| CAP-A01 | supporting | 課後整合 / 遷移驗收 | 用真實需求填五欄、保存第一版、一次修訂與待確認事項 | `course-capstone-handoff.md` | 沒看過課程的人能讀懂並重做；缺欄回工作表對應區段 | module1 `#course-capstone`、`assets/worksheets/course-capstone-handoff.md` |

## Supplement freeze rule

本次補充的 atom ID 固定為 `CH2-A01`–`CH2-A05`、`CH3-A01`–`CH3-A05`、`CH4-A01`–`CH4-A05`、`CAP-A01`。若 L4a 或 L5 發現 learner path 斷裂，先在修復報告標註上游來源，再修改 atom 證據，不刪除原子以掩蓋缺口。

## Learner Task Contract evidence map

本表不新增契約；它只把唯一契約的八欄映射到每個 learner-facing 頁面，供 reviewer 與 validator 冷讀時定位。完整的輸入、動作、結果、驗證與修復仍以各 atom 的 Pass 2 證據為準。

| lesson | role/context | problem/consequence | starting material + fallback | finished artifact | next user/use | first action + observable result | recovery position |
|---|---|---|---|---|---|---|---|
| CH1-1 | 文字型 LLM 初學成人；工作／生活小任務 | 模糊提問造成泛答、漏條件，無法重做 | 頁內工作台；瀏覽器不能暫存用 `assets/worksheets/unit1-practice-sheet.md`；LLM 不可用看 `assets/fallback/unit1-dialogue-simulator.md` | 工作台填寫紀錄匯出為 `unit1-practice-sheet-complete.md` | 自己在 CH2／CH4 重用五欄與版本 | 開啟工作台並填姓名日期；看到第 1 題欄位與進度變化 | `U1-START`、`U1-ASK`、`U1-REVISE`；不能暫存時匯出／列印後停止 |
| CH2-1 | 對不同讀者寫日常文字的成人 | 讀者／目的／語氣不清造成誤解與重寫 | `assets/templates/unit2-communication-scenarios.md` 或 HTML 素材頁；工具不可用標待重跑 | `unit2-communication-pack-complete.md` | 自己、實際收件者；CH4 個人化 | 複製素材包建檔；看到三類成品區與檢核表 | `U2-START`、`U2-PROMPT`、`U2-EMAIL`／`U2-MESSAGE`、`U2-ITERATE` |
| CH3-1 | 需要回查長文的成人 | 把補寫內容當原文會誤判日期／條件／下一步 | NotebookLM、閱讀包、來源索引與三份必做來源；平台不可用看純文字 fallback | `unit3-notebooklm-reading-pack-complete.md` + NotebookLM 筆記本 | 自己或工作夥伴回查；CH4 轉用 | 建立筆記本並加入三份來源；來源列表看見三個名稱 | `U3-SOURCE`、`U3-SUMMARY`、`U3-ANNOUNCE`、`U3-CITE` |
| CH4-1 | 有近期生活任務的成人 | 泛問會猜條件，造成不合用或越界結果 | 30 張提示詞卡、應用卡、冷氣資料與文字型 LLM；工具不可用先填欄位 | `unit4-lifestyle-application-card.md` | 未來自己重做；課後交 capstone handoff | 複製應用卡、選主卡、填五欄；看到主卡與限制 | `U4-SELECT`、`U4-PROMPT`、`U4-CHECK-1`、`U4-REVISE`、`U4-SAVE-2` |

### Contract evidence review rule

每列的八欄都必須能在對應教案與 HTML 找到具體文字、連結、檔名、輸入值、預期結果與回修位置。只有標籤、摘要、頁尾資產清單或講師筆記，不算 Pass 2 證據。
