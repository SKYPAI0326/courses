# Course Blueprint

- **Course**：AI 入門即戰力：零基礎的 AI 入門應用
- **Audience**：第一次系統使用 LLM 的成人學習者，能使用瀏覽器與複製貼上
- **Workplace outcome**：學員能把一項模糊的工作或生活需求改寫成提示詞，取得可編輯的文字、摘要或規劃初稿
- **Duration and sequence**：4 個 skill-operation 單元，各 3 小時，共 12 小時
- **Lesson types**：CH1-1、CH2-1、CH3-1、CH4-1 皆為 skill-operation；CH3-1 固定使用 NotebookLM
- **Free baseline and paid-tool boundaries**：其他 LLM 不指定平台；學員使用可取得的免費或既有服務。NotebookLM 為課程固定平台，課前確認當期免費使用界線與介面
- **Shared environment**：課程提供瀏覽器可開啟的 NotebookLM、純文字來源檔、提示詞工作表與離線備援內容
- **Capstone deliverables**：四份完成物組成個人 AI 實務包；課後再以一份真實需求整合交付物驗收遷移：LLM 對話紀錄、日常文書包、NotebookLM 閱讀包、生活應用卡、`course-capstone-handoff.md`

## Learner Task Contract Matrix

以下四列是依 `../_規範/learner-action-contract.md` 凍結的唯一學員路徑事實；各單元教案與 HTML 必須引用同一組檔名、完成物、第一個結果與回修位置。

| lesson | 角色／問題與後果 | 起始材料與備援 | 完成物／下一位使用者與用途 | 第一動作／第一結果 | 失敗回復 |
|---|---|---|---|---|---|
| CH1-1 | 第一次使用文字型 LLM 的成人學習者；模糊提問會得到泛泛或漏條件的答案，之後無法重做。 | `assets/worksheets/unit1-practice-sheet.md` + 任一可輸入文字的 LLM；工具不可用用 `assets/fallback/unit1-dialogue-simulator.md` 判讀，恢復後重跑。 | `unit1-practice-sheet-complete.md`；未來的自己在 CH2／CH4 沿用五欄提示詞與版本紀錄。 | 複製工作表副本並填姓名日期；看見五題欄位與可貼回答的位置。 | `U1-START` 取得材料；`U1-ASK` 修回答；`U1-REVISE` 修單一變因；安全停止在已保存副本。 |
| CH2-1 | 需要把同一件事交代給不同讀者；讀者、目的與語氣不清會造成誤解與來回重寫。 | `assets/templates/unit2-communication-scenarios.md`／HTML 素材頁 + 任一文字型 LLM；工具不可用先標待重跑。 | `unit2-communication-pack-complete.md`；未來的自己或實際收件者使用，CH4 再個人化一個情境。 | 複製素材包建立完成物；看見 Email／訊息／自我介紹三區與檢核表。 | `U2-START` 重取素材；`U2-PROMPT` 補四段；`U2-EMAIL`／`U2-MESSAGE` 修事實；`U2-ITERATE` 修版本。 |
| CH3-1 | 需要把長文整理成可回查的重點；若把模型補寫當原文，可能誤判日期、條件或下一步。 | NotebookLM + 閱讀包、來源索引與 1 份新聞／公告／書籍節錄；平台不可用用 `assets/fallback/unit3-notebooklm-text-fallback.md`，但無正式引用。 | `unit3-notebooklm-reading-pack-complete.md` + 含 3 份來源的 NotebookLM 筆記本；未來的自己或工作夥伴回查，CH4 可轉用。 | 開啟閱讀包與來源索引，建立筆記本並加入三份來源；來源列表看見三個可辨識名稱。 | `U3-SOURCE` 修來源；`U3-SUMMARY` 修摘要；`U3-ANNOUNCE` 補欄位；`U3-CITE` 回查引用；安全停止在閱讀包。 |
| CH4-1 | 處理真實生活任務；泛問會讓工具猜時間、預算與限制，造成排太滿、超預算或越過專業判斷。 | 30 張提示詞卡、生活應用卡、冷氣共同素材與任一文字型 LLM；不可用先填欄位，恢復後重跑。 | `unit4-lifestyle-application-card.md`；未來的自己下次替換時間／預算重做，課後交 `course-capstone-handoff.md`。 | 複製應用卡並選一張主卡，填目標／時間／預算／偏好／限制；看見主卡與至少一項限制。 | `U4-SELECT` 補欄；`U4-PROMPT` 補四段；`U4-CHECK-1` 找漏條件；`U4-REVISE` 單一變因；`U4-SAVE-2` 補保存。 |

## 30 秒入口與因果檢查

- 四個單元 learner-facing HTML 的第一個操作前，必須呈現上表中的角色、問題、起始材料、完成物、下一位使用者、第一動作與第一結果。
- 任何段落轉換都要把上一個可觀察結果接到下一個目的；`Demo`、`Together`、`Solo`、`Check`、`Stage` 只作導航。
- 三課 micro-sequence 為 `CH1-1 → CH2-1 → CH3-1`：CH1 的五欄方法在 CH2 變成四段式文書提示詞，CH2 的讀者／語氣／格式判斷在 CH3 變成來源閱讀問題。

## Artifact Dependency Graph

| lesson | input artifact | learner transformation | output artifact | next use | capstone component |
|---|---|---|---|---|---|
| CH1-1 | `assets/worksheets/unit1-practice-sheet.md` | 用五欄提示詞框架完成五個日常對話與一次修改 | `unit1-practice-sheet-complete.md` 填寫版 | CH2-1、CH4-1 沿用提示詞欄位 | LLM 對話紀錄 |
| CH2-1 | CH1-1 的五欄框架 + `assets/templates/unit2-communication-scenarios.md` | 依對象、語氣與長度改寫文字 | `unit2-communication-pack-complete.md` | CH4-1 取一個實際情境做個人化 | 日常文書包 |
| CH3-1 | `assets/sources/` 內課程來源檔 | 加入 NotebookLM、提問、摘要、抽取與條列 | `unit3-notebooklm-reading-pack-complete.md` | CH4-1 將來源整理方法轉到自己的文件 | NotebookLM 閱讀包 |
| CH4-1 | 前三單元的提示詞欄位 + `assets/prompts/unit4-lifestyle-prompts.md` | 改寫一項生活任務並完成結果 | `unit4-lifestyle-application-card.md` | 課後整合任務取一項真實需求 | 生活應用卡 |

## Core Operation Inventory

| operation_id | lesson | why learner cannot infer it | input/state | action | visible result | verification | repair |
|---|---|---|---|---|---|---|---|
| OP-01 | CH1-1 | 學員容易把搜尋問題與對話任務混在一起 | 一個日常需求 | 把需求拆成情境、任務、資料、條件、格式 | 可複製提示詞 | 五欄都有具體內容 | 回到工作表逐欄補值 |
| OP-02 | CH1-1 | LLM 輸出可能太長或不合用 | 第一版回答 | 使用長度、語氣、格式修改指令 | 第二版回答更符合用途 | 對照前後版本 | 只改一個條件後重問 |
| OP-03 | CH2-1 | 同一內容要依讀者改寫，不是複製貼上 | 請假或回覆情境 | 指定讀者與語氣，產出三版本 | 三份可編輯文字 | 每版讀者與語氣不同 | 補上讀者、場合與長度 |
| OP-04 | CH3-1 | NotebookLM 的來源、提問與引用有固定順序 | 課堂必做 3 份來源；另有 6 份延伸來源 | 建立 notebook、加入來源、提出可回到原文的問題 | 回答附來源引用 | 點引用可回到原文位置 | 用純文字備援檔重做輸入；恢復後重跑正式引用 |
| OP-05 | CH3-1 | 摘要、抽取與條列是三種不同任務 | 一段長文件 | 依輸出目的提出不同提示詞 | 一句、200 字、500 字、重點與行動 | 保留要求的欄位與長度 | 先縮小來源或改用單一任務 |
| OP-06 | CH4-1 | 生活需求需要個人條件，不能直接照抄範本 | 30 套提示詞卡 | 只改預算、時間、偏好等主要條件 | 一份個人化規劃或比較結果 | 條件有出現在輸出 | 回到提示詞，補上缺少的條件 |

## Environment Contract

| tool/version date | account role | permission | free/paid | starting file/data | success output | fallback | interface-change lookup |
|---|---|---|---|---|---|---|---|
| 任一可用 LLM／課前確認 | 學員自己的一般使用者 | 能輸入文字並複製輸出 | 依學員可取得的服務；不要求付費 | 各單元提供的 Markdown 工作表／提示詞資產與瀏覽器中的對話畫面 | 一段可複製、可保存的回答 | 各單元指定的 Markdown 備援內容完成判讀；工具恢復後重跑正式版本 | 依正在使用的服務搜尋「新對話」「複製回答」「重新生成」等當期功能名稱 |
| NotebookLM／課前實機驗證 | 學員自己的 Google 帳號 | 能開啟、建立空白 notebook、加入 1 份純文字來源、看見來源名稱與回答引用 | 以課前確認的免費界線為準，不要求付費 | 課程提供的 `assets/sources/` 來源檔 | 5 分鐘內完成「建立→加入→提問→點開引用」最小路徑 | 保存工作表與來源索引，先用 `assets/fallback/unit3-notebooklm-text-fallback.md` 練習；平台恢復後重跑正式引用 | 以當期功能名稱搜尋「建立筆記本」「加入來源」「查看引用」，不依賴固定按鈕位置 |

## 課堂最低完成線

| 單元 | 3 小時內必做 | 延伸 |
|---|---|---|
| CH1-1 | 五題對話、一次單一變因修改、保存實務紀錄 | 自己的工作／生活問題 |
| CH2-1 | 1 封 Email、1 則訊息、3 版自我介紹；至少兩份前後版本 | 其他情境卡 |
| CH3-1 | 3 份必做來源、三類閱讀產出、引用回查 | 4 篇新聞與 2 份公告 |
| CH4-1 | 1 張主卡、第一版、一次修訂、應用卡 | 其餘 29 張提示詞卡 |

## 課後整合驗收

使用 `assets/worksheets/course-capstone-handoff.md`，學員選一個下週真的會遇到的需求，留下背景、任務、資料、條件、格式、第一版、單一變因修訂、修正版與待確認事項。這份交付物是課後遷移證據，不取代四個單元的核心完成物。

## Coverage Ledger policy

`COVERAGE-LEDGER.md` 先凍結核心原子，再於每個代表頁完成後填入實際證據。未完成的後續單元素材標記為 `PLANNED`，不得在 HTML 產製前宣稱 `READY`。

## Micro-sequence

第一個可測試的三課鏈為 CH1-1 → CH2-1 → CH3-1：CH1-1 產出的五欄提示詞框架，會在 CH2-1 改寫文書；CH2-1 的「讀者／語氣／格式」判斷，會在 CH3-1 轉成 NotebookLM 的來源提問格式。CH3-1 的實際來源包與閱讀完成物，再交給 CH4-1 作為生活應用的查詢與整理參考。
