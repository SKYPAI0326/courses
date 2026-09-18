# Course Blueprint

- **Course**：AI 入門即戰力：零基礎的 AI 入門應用
- **Audience**：第一次系統使用 LLM 的成人學習者，能使用瀏覽器與複製貼上
- **Workplace outcome**：學員能把一項模糊的工作或生活需求轉成可檢查的工作說明，留下可編輯文字、可回查證據或有取捨依據的決策初稿
- **Duration and sequence**：4 個 skill-operation 單元，各 3 小時，共 12 小時
- **Lesson types**：CH1-1、CH2-1、CH3-1、CH4-1 皆為 skill-operation；CH3-1 固定使用 NotebookLM
- **Free baseline and paid-tool boundaries**：其他 LLM 不指定平台；學員使用可取得的免費或既有服務。NotebookLM 為課程固定平台，課前確認當期免費使用界線與介面
- **Shared environment**：課程提供瀏覽器可開啟的 NotebookLM、純文字來源檔、提示詞工作表與離線備援內容
- **Capstone deliverables**：四份完成物組成個人 AI 實務包；課後再以一份真實需求整合交付物驗收遷移：LLM 對話紀錄、日常文書包、NotebookLM 閱讀包、生活應用卡、`course-capstone-handoff.md`

## Learner Task Contract Matrix

以下四列是依 `../_規範/learner-action-contract.md` 凍結的唯一學員路徑事實；各單元教案與 HTML 必須引用同一組檔名、完成物、第一個結果與回修位置。

| lesson | 角色／問題與後果 | 起始材料與備援 | 完成物／下一位使用者與用途 | 第一動作／第一結果 | 失敗回復 |
|---|---|---|---|---|---|
| CH1-1 | 第一次使用文字型 LLM 的成人學習者；模糊提問會得到泛泛或漏條件的答案，之後無法重做。 | 頁內實務工作台 + 任一可輸入文字的 LLM；瀏覽器不能暫存時用 `assets/worksheets/unit1-practice-sheet.md`，工具不可用用 `assets/fallback/unit1-dialogue-simulator.md` 判讀，恢復後重跑。 | 工作台填寫紀錄匯出為 `unit1-practice-sheet-complete.md`；未來的自己用任務卡重做，CH2 只承接五欄定義，不重播 CH1。 | 開啟工作台並填姓名日期；看見第 1 題欄位、進度變化與本機暫存狀態。 | `U1-START` 開啟工作台；`U1-ASK` 修回答；`U1-GAP` 補一個缺少條件並比較；不能暫存時匯出／列印，工具不可用時安全停止在備援判讀。 |
| CH2-1 | 需要把同一件事交代給不同讀者；讀者、目的與語氣不清會造成誤解與來回重寫。 | CH2-1 頁面日常溝通工作台、`assets/templates/unit2-communication-scenarios.md`／HTML 素材頁 + 任一文字型 LLM；Markdown 只作離線備援，工具不可用先在工作台標待重跑。 | 工作台匯出的 `unit2-communication-pack-complete.md`；未來的自己或實際收件者使用，完成包可直接編輯與交接。 | 開啟工作台並填第一個 Email 情境；看見 Email／訊息／自我介紹三區與檢核表。 | `U2-START` 開啟工作台；`U2-PROMPT` 補四段；`U2-EMAIL`／`U2-MESSAGE` 修事實；`U2-AUDIENCE` 做讀者轉換；不能暫存時匯出／列印。 |
| CH3-1 | 需要把長文轉成可回查的證據；若把模型補寫當原文，可能誤判日期、條件或下一步。 | CH3-1 頁面 NotebookLM 閱讀紀錄台 + NotebookLM + 來源索引與 1 份新聞／公告／書籍節錄；平台不可用用 `assets/fallback/unit3-notebooklm-text-fallback.md`，先練習主張與來源狀態，恢復後重跑正式引用。 | 紀錄台匯出的 `unit3-notebooklm-reading-pack-complete.md` + 含 3 份來源的 NotebookLM 筆記本；內含來源地圖、主張／證據狀態台帳、公告影響卡、書籍三層筆記與跨來源比較。 | 開啟紀錄台填筆記本與來源，再建立筆記本並加入三份來源；接著挑一個主張貼回，標記支持、部分支持或來源未提及。 | `U3-SOURCE` 修來源；`U3-CLAIM` 拆主張；`U3-CITE` 回查引用；`U3-COMPARE` 比較兩份來源；平台不可用時標待重跑並匯出。 |
| CH4-1 | 要在真實生活任務中做選擇；若只問「哪個最好」，工具會猜條件並掩蓋取捨、缺資料與人工確認。 | CH4-1 頁面生活決策工作台、30 張提示詞卡、生活應用 Markdown 備援、冷氣共同素材與任一文字型 LLM；不可用先填決策條件與缺資料，恢復後重跑。 | 工作台匯出的 `unit4-lifestyle-application-card.md`；內含決策問題、選擇標準／優先順序、方案比較、取捨、缺資料、下一步與人工確認；課後交 `course-capstone-handoff.md`。 | 開啟工作台並選一個近期決策，填決策問題、至少三項標準與優先順序；看見第一個「已知／缺資料／要確認」區分。 | `U4-FRAME` 定義決策；`U4-TRADEOFF` 寫取捨；`U4-MISSING` 標缺資料；`U4-BOUNDARY` 守住人工／專業界線；`U4-SAVE` 匯出，不能暫存時列印。 |

## 30 秒入口與因果檢查

- 四個單元 learner-facing HTML 的第一個操作前，必須呈現上表中的角色、問題、起始材料、完成物、下一位使用者、第一動作與第一結果。
- 任何段落轉換都要把上一個可觀察結果接到下一個目的；`Demo`、`Together`、`Solo`、`Check`、`Stage` 只作導航。
- 三課 micro-sequence 為 `CH1-1 → CH2-1 → CH3-1`：CH1 的任務定義在 CH2 變成讀者／目的／語氣／格式轉換，CH2 的讀者判斷在 CH3 變成「誰需要知道哪個主張、證據在哪裡」。

## Artifact Dependency Graph

| lesson | input artifact | learner transformation | output artifact | next use | capstone component |
|---|---|---|---|---|---|
| CH1-1 | 頁內實務工作台；離線時 `assets/worksheets/unit1-practice-sheet.md` | 用五欄提示詞框架完成五個日常對話、找出一個缺少條件並重問，再完成個人任務卡 | 工作台填寫紀錄，匯出為 `unit1-practice-sheet-complete.md` 或列印 PDF | CH2-1 承接五欄定義；CH4-1 不重播 CH1 流程 | LLM 對話紀錄 |
| CH2-1 | CH1-1 的五欄框架 + 頁面日常溝通工作台 + `assets/templates/unit2-communication-scenarios.md` | 依讀者、目的、語氣與格式把同一件事轉成不同用途文字 | 工作台匯出 `unit2-communication-pack-complete.md` | 供實際收件者編輯使用；CH4-1 只取情境資料，不重播文書流程 | 日常文書包 |
| CH3-1 | CH3-1 頁面 NotebookLM 閱讀紀錄台 + `assets/sources/` 內課程來源檔 | 建立來源地圖，將回答拆成主張、證據狀態與引用位置，再做跨來源比較 | 紀錄台匯出 `unit3-notebooklm-reading-pack-complete.md` | CH4-1 將已知、未知與證據邊界帶入生活決策 | NotebookLM 證據閱讀包 |
| CH4-1 | CH4-1 頁面生活決策工作台 + `assets/prompts/unit4-lifestyle-prompts.md` + 冷氣共同素材 | 把生活問題轉成選擇標準，建立方案比較、取捨與下一步 | 工作台匯出 `unit4-lifestyle-application-card.md` | 課後整合任務交付一份有條件與待確認事項的決策卡 | 生活決策卡 |

## Core Operation Inventory

| operation_id | lesson | why learner cannot infer it | input/state | action | visible result | verification | repair |
|---|---|---|---|---|---|---|---|
| OP-01 | CH1-1 | 學員容易把搜尋問題與對話任務混在一起 | 一個日常需求 | 把需求拆成情境、任務、資料、條件、格式 | 可複製提示詞與工作台欄位 | 五欄都有具體內容 | 回到工作台逐欄補值；不能暫存時改用離線工作表 |
| OP-02 | CH1-1 | 第一版回答可能漏掉會影響結果的條件 | 第一版回答 | 找出一個缺口，補入重問指令並比較前後 | 第二版能對應新增條件 | 新條件在輸出中可見，仍未知處被標記 | 回到 U1-GAP，一次只補最關鍵的條件 |
| OP-03 | CH2-1 | 同一內容要依讀者、目的與場合轉換，不是複製貼上 | Email、訊息或自我介紹第一版 | 指定新讀者、對方下一步與輸出格式，產出轉換版 | 可交接的不同用途文字 | 每版讀者、目的與保留事實可說明 | 回到 U2-AUDIENCE，補新讀者與事實邊界 |
| OP-04 | CH3-1 | NotebookLM 的來源、提問與引用有固定順序 | 課堂必做 3 份來源；另有 6 份延伸來源 | 建立 notebook、加入來源、提出可回到原文的問題 | 回答附來源引用 | 點引用可回到原文位置 | 用純文字備援檔重做輸入；恢復後重跑正式引用 |
| OP-05 | CH3-1 | 長文中的一句話可能同時含有多個主張，不能只看摘要是否順 | 三份課堂來源與 NotebookLM 回答 | 拆主張、標證據狀態、點引用回查，再比較不同來源是否一致 | 主張／引用／支持狀態台帳、公告卡、跨來源比較 | 每個重要主張都能回到來源或標「來源未提及」 | 拆短句、改標部分支持或未知，回 U3-CLAIM／U3-CITE |
| OP-06 | CH4-1 | 生活決策不是把條件塞進範本，而是要明確排序標準並看見取捨 | 冷氣共同素材或一項真實生活決策 | 建立標準與優先順序，做方案比較，標缺資料並寫下一步 | 有取捨依據與人工確認位置的決策卡 | 方案能依標準比較，未知資料沒有被補成事實 | 回到 U4-FRAME／U4-MISSING，補標準或待查問題 |

## Environment Contract

| tool/version date | account role | permission | free/paid | starting file/data | success output | fallback | interface-change lookup |
|---|---|---|---|---|---|---|---|
| 任一可用 LLM／課前確認 | 學員自己的一般使用者 | 能輸入文字並複製輸出 | 依學員可取得的服務；不要求付費 | 各單元頁面內工作台、提示詞資產與瀏覽器中的對話畫面 | 一段可複製、可保存的回答回填工作台 | 各單元指定的 Markdown 備援內容完成判讀；工具恢復後重跑正式版本 | 依正在使用的服務搜尋「新對話」「複製回答」「重新生成」等當期功能名稱 |
| NotebookLM／課前實機驗證 | 學員自己的 Google 帳號 | 能開啟、建立空白 notebook、加入 1 份純文字來源、看見來源名稱與回答引用 | 以課前確認的免費界線為準，不要求付費 | CH3-1 頁面紀錄台、課程提供的 `assets/sources/` 來源檔 | 5 分鐘內完成「紀錄→建立→加入→提問→點開引用」最小路徑 | 在紀錄台標記待重跑並匯出，先用 `assets/fallback/unit3-notebooklm-text-fallback.md` 練習；平台恢復後重跑正式引用 | 以當期功能名稱搜尋「建立筆記本」「加入來源」「查看引用」，不依賴固定按鈕位置 |

## 課堂最低完成線

| 單元 | 3 小時內必做 | 延伸 |
|---|---|---|
| CH1-1 | 五題對話、一次缺條件比較、完成任務卡並匯出實務紀錄 | 更多自選工作／生活問題 |
| CH2-1 | 1 封 Email、1 則訊息、3 版自我介紹；至少兩份讀者／場合轉換 | 其他情境卡 |
| CH3-1 | 3 份必做來源、三類閱讀產出、引用回查 | 4 篇新聞與 2 份公告 |
| CH4-1 | 1 張主卡、第一版、方案比較、取捨與缺資料、應用卡 | 其餘 29 張提示詞卡 |

## 課後整合驗收

使用 `assets/worksheets/course-capstone-handoff.md`，學員選一個下週真的會遇到的需求，留下背景、任務、資料、條件、格式、第一版、缺口或取捨的判讀、後續版本與待確認事項。這份交付物是課後遷移證據，不取代四個單元的核心完成物。

## Coverage Ledger policy

`COVERAGE-LEDGER.md` 先凍結核心原子，再於每個代表頁完成後填入實際證據。未完成的後續單元素材標記為 `PLANNED`，不得在 HTML 產製前宣稱 `READY`。

## Micro-sequence

第一個可測試的三課鏈為 CH1-1 → CH2-1 → CH3-1：CH1-1 產出的任務定義，會在 CH2-1 變成收件者／語氣／格式決策；CH2-1 的讀者判斷在 CH3-1 轉成「誰需要知道哪個主張、證據在哪裡」。CH3-1 的證據與未知狀態再交給 CH4-1，成為生活決策的資料邊界與待確認清單。
