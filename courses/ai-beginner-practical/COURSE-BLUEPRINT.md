# Course Blueprint

- **Course**：AI 入門即戰力：零基礎的 AI 入門應用
- **Audience**：第一次系統使用 LLM 的成人學習者，能使用瀏覽器與複製貼上
- **Workplace outcome**：學員能把一項模糊的工作或生活需求轉成可檢查的工作說明，留下可編輯文字、可回查證據或有取捨依據的決策初稿
- **Duration and sequence**：4 個 skill-operation 單元，各 3 小時，共 12 小時
- **Lesson types**：CH1-1、CH2-1、CH3-1、CH4-1 皆為 skill-operation；CH2-1 內含 PRAC2-1 Gamma 實作，CH3-1 使用 NotebookLM
- **Free baseline and paid-tool boundaries**：其他 LLM 不指定平台；學員使用可取得的免費或既有服務。Gamma 與 NotebookLM 為指定操作平台，課前逐人確認生成／建立、編輯與保存，不要求付費升級
- **Shared environment**：課程提供瀏覽器可開啟的 NotebookLM、純文字來源檔、提示詞工作表與離線備援內容
- **Capstone deliverables**：四份完成物組成個人 AI 實務包；課後再以一份真實需求整合交付物驗收遷移：LLM 對話紀錄、日常文書與提案包、可回查工作文件、個人方案決策卡、`course-capstone-handoff.md`

## Learner Task Contract Matrix

以下四列是依 `../../_規範/learner-action-contract.md` 凍結的唯一學員路徑事實；各單元教案與 HTML 必須引用同一組檔名、完成物、第一個結果與回修位置。

| lesson | 角色／問題與後果 | 起始材料與備援 | 完成物／下一位使用者與用途 | 第一動作／第一結果 | 失敗回復 |
|---|---|---|---|---|---|
| CH1-1 | 教育／服務／業務或自己的單位；模糊提問與無據承諾使短文不能直接採用。 | assets/workplace/tasks三案完整原文與prompt／repair、自己LLM與保存台；不能保存用離線表，無LLM讀作者參考標待重跑。 | unit1-practice-sheet-complete.md：自己的短文、完整prompt／第一版、唯一修正、新版核對與待確認；CH2承接讀者轉換。 | 選一案，代入完整材料與五欄prompt送出；看見一份短文後貼回personalPrompt，不先填五題。 | U1-START／ASK／DIAG／GAP／SAVE；未知先標待確認，匯出重開；無LLM不勾正式完成。 |
| CH2-1 | 需要把同一件事交代給不同讀者；讀者、目的與語氣不清會造成誤解與來回重寫。 | CH2-1 頁面日常溝通工作台、`assets/templates/unit2-communication-scenarios.md`／HTML 素材頁 + 任一文字型 LLM；Markdown 只作離線備援，PRAC2-1完整企劃、提示詞與Gamma；工具不可用保存已完成資料、標待補。 | 工作台匯出的 `unit2-communication-pack-complete.md`；未來的自己或實際收件者使用，完成包可直接編輯與交接；另有PRAC2-1十頁大綱、Gamma與重開驗證的十頁PDF，供指定主管閱讀。 | 開啟工作台並填第一個 Email 情境；看見 Email／訊息必做區與檢核表；自我介紹、額外轉換區為選做。 | `U2-START` 開啟工作台；`U2-PROMPT` 補四段；`U2-EMAIL`／`U2-MESSAGE` 修事實；`U2-AUDIENCE` 做讀者轉換；不能暫存時匯出／列印。 |
| CH3-1 | 教務／服務／各單位承辦人；不同版本若當核准或把首次回覆當結案，會造成錯誤承諾。 | CH3保存台、NotebookLM、assets/workplace/documents同案例三文件；不可用人工定位並標平台待重跑。 | unit3-notebooklm-reading-pack-complete.md與自己的筆記本；所選一份FAQ／交接／待辦、第一版、三引用回查、修訂與未解問題。 | 選一組原文建立自己的筆記本，加入3來源並看見可辨名稱與原文。 | U3-SOURCE／CLAIM／CITE／COMPARE／REPAIR／SAVE；無平台時不勾正式引用。 |
| CH4-1 | 教育／行政／各單位承辦人；忽略容量、角色工時或未知設定會使方案不可行。 | CH4保存台、assets/workplace/decisions完整brief與compare／change；自己的LLM。生活材料可替代，不再交共同案例。 | unit4-decision-card.md：實際提示詞、第一版、單一變因修訂、兩方案三標準、列式、取捨與下一步。 | 讀所選brief，接在compare提示詞後；送出文字有兩方案與三標準。 | U4-FRAME／TRADEOFF／MISSING／CHANGE／DECIDE／SAVE；不可用先人工列式，標模型待重跑。 |

## 30 秒入口與因果檢查

- 四個單元 learner-facing HTML 的第一個操作前，必須呈現上表中的角色、問題、起始材料、完成物、下一位使用者、第一動作與第一結果。
- 任何段落轉換都要把上一個可觀察結果接到下一個目的；`Demo`、`Together`、`Solo`、`Check`、`Stage` 只作導航。
- 三課 micro-sequence 為 `CH1-1 → CH2-1 → CH3-1`：CH1 的任務定義在 CH2 變成讀者／目的／語氣／格式轉換，CH2 的讀者判斷在 CH3 變成「誰需要知道哪個主張、證據在哪裡」。

## Artifact Dependency Graph

| lesson | input artifact | learner transformation | output artifact | next use | capstone component |
|---|---|---|---|---|---|
| CH1-1 | 頁內實務工作台；離線時 `assets/worksheets/unit1-practice-sheet.md` | 自選一份工作材料，用同一完整五欄prompt產短文，只修一項，保存第一版／新版／核對與待確認；不重填拆解表 | 工作台填寫紀錄，匯出為 `unit1-practice-sheet-complete.md` 或列印 PDF | CH2-1 承接五欄定義；CH4-1 不重播 CH1 流程 | LLM 對話紀錄 |
| CH2-1 | CH1-1 的五欄框架 + 頁面日常溝通工作台 + `assets/templates/unit2-communication-scenarios.md` | 依讀者、目的、語氣與格式把同一件事轉成不同用途文字 | 工作台匯出 `unit2-communication-pack-complete.md`，以及PRAC2-1的十頁大綱、Gamma、PDF與短交接 | 供實際收件者與提案主管閱讀；CH3可延伸來源支持，CH4只取情境資料 | 日常文書與提案包 |
| CH3-1 | 個人NotebookLM＋同情境三來源 | 回查三個重要主張、判權威／範圍與未解問題，修訂一份工作文件 | unit3-notebooklm-reading-pack-complete.md | 接手者可回查；CH4只取已核對背景／未知，無前章成品依賴 | 可回查工作文件 |
| CH4-1 | 自選完整兩方案brief＋個人LLM | 先檢硬限制、排序三標準，比較取捨；只改一項條件再計算 | unit4-decision-card.md | 給主管／未來自己條件式核定；課後用真需求遷移 | 個人方案決策卡 |

## Core Operation Inventory

| operation_id | lesson | why learner cannot infer it | input/state | action | visible result | verification | repair |
|---|---|---|---|---|---|---|---|
| OP-01 | CH1-1 | 學員容易把搜尋問題與對話任務混在一起 | 一個日常需求 | 把需求拆成情境、任務、資料、條件、格式 | 可複製提示詞與工作台欄位 | 五欄都有具體內容 | 回到工作台逐欄補值；不能暫存時改用離線工作表 |
| OP-02 | CH1-1 | 第一版回答可能漏掉會影響結果的條件 | 第一版回答 | 找出一個缺口，補入重問指令並比較前後 | 第二版能對應新增條件 | 新條件在輸出中可見，仍未知處被標記 | 回到 U1-GAP，一次只補最關鍵的條件 |
| OP-03 | CH2-1 | 同一內容要依讀者、目的與場合轉換，不是複製貼上 | Email、訊息或自我介紹第一版 | 指定新讀者、對方下一步與輸出格式，產出轉換版 | 可交接的不同用途文字 | 每版讀者、目的與保留事實可說明 | 回到 U2-AUDIENCE，補新讀者與事實邊界 |
| OP-04 | CH3-1 | 文件來源與回查先於交付 | 所選同案例3文件 | 自己建立筆記本、加入原文、送一種成品提示詞 | 自己的來源列表與第一版 | 三份可讀，首個引用回原文 | 重新加入原文，保存錯版；平台恢復後重跑 |
| OP-05 | CH3-1 | 版本日期不足以證明核准；引用只支持部分句子 | 所選三來源、第一版 | 三主張點引用，分清適用範圍、權威、未完成與未知，修訂 | 一份成品及引用回查、未解問題 | 重要主張可查，矛盾未被刪掉，下一步可做 | U3-CITE／COMPARE／REPAIR，保留人工確認 |
| OP-06 | CH4-1 | 硬限制先於偏好，容量與假設工時不等於成效 | 完整brief兩方案或有資料生活選題 | 核對容量／角色工時、三標準排序、只改一限制 | 條件式決策卡及前後版 | 列式正確、未合格不選、缺資料與設定核定保留 | U4-MISSING／CHANGE／DECIDE，兩者不可行就不硬選 |

## Environment Contract

| tool/version date | account role | permission | free/paid | starting file/data | success output | fallback | interface-change lookup |
|---|---|---|---|---|---|---|---|
| 任一可用 LLM／課前確認 | 學員自己的一般使用者 | 能輸入文字並複製輸出 | 依學員可取得的服務；不要求付費 | 各單元頁面內工作台、提示詞資產與瀏覽器中的對話畫面 | 一段可複製、可保存的回答回填工作台 | 各單元指定的 Markdown 備援內容完成判讀；工具恢復後重跑正式版本 | 依正在使用的服務搜尋「新對話」「複製回答」「重新生成」等當期功能名稱 |
| NotebookLM／課前實機驗證 | 學員自己的 Google 帳號 | 能開啟、建立空白 notebook、加入 1 份純文字來源、看見來源名稱與回答引用 | 以課前確認的免費界線為準，不要求付費 | CH3-1 頁面保存台與 `assets/workplace/documents/` 同案例三來源 | 5 分鐘內完成「紀錄→建立→加入→提問→點開引用」最小路徑 | 在紀錄台標記待重跑並匯出，先用 `assets/fallback/unit3-notebooklm-text-fallback.md` 練習；平台恢復後重跑正式引用 | 以當期功能名稱搜尋「建立筆記本」「加入來源」「查看引用」，不依賴固定按鈕位置 |

## 課堂最低完成線

| 單元 | 3 小時內必做 | 延伸 |
|---|---|---|
| CH1-1 | 一份個人工作短文、實際首版／修正版及單一缺口核對；匯出實務紀錄 | 更多自選工作／生活問題 |
| CH2-1 | 1 封 Email、1 則訊息、一次 Email 讀者轉換；PRAC2-1 的十頁大綱、Gamma、十頁PDF與短交接 | 三版自我介紹、第二次轉換、其他情境卡 |
| CH3-1 | 一組同情境三來源、一種工作成品、三真引用回查、具體修訂、匯出重開 | 原新聞／公告／書籍三類完整閱讀作業及其他來源 |
| CH4-1 | 一個自選決策、兩方案三標準、硬限制列式、單一變因修訂與保存 | 原京都／冷氣／30張生活提示詞選題 |

## 課後整合驗收

使用 `assets/worksheets/course-capstone-handoff.md`，學員選一個下週真的會遇到的需求，留下背景、任務、資料、條件、格式、第一版、缺口或取捨的判讀、後續版本與待確認事項。這份交付物是課後遷移證據，不取代四個單元的核心完成物。

## Coverage Ledger policy

### 2026-10-09 課前工具與跟做修訂

授課前由講師提供並逐人確認可用入口，讓每人送出一句話、複製回答、保存並重開；未準備好者先處理入口，不把工具取得當成已會的技能。CH3 先示範加入第一份文字來源，再由各人加入自己案例的另外兩份；先做一筆引用核對，再核對自己的三句。

CH2 必做以 Email、短訊息與一次 Email 讀者轉換為準，人工修正可收尾，保留模型版與人工版。CH4 使用具體案例與方案名稱，成品以一頁可讀、算式與待確認完整驗收，450漢字只供模型縮稿提示。Gamma 可用本頁文字下載區保存來源、大綱與貼入文字；自帶企劃用小標題／支持原句定位，不捏造P編號。

四章維持各三小時，Gamma仍在CH2後半。上述時間與零基礎理解尚待真人試跑，詳見本次修訂待驗清單；不新增學員表格。

`COVERAGE-LEDGER.md` 先凍結核心原子，再於每個代表頁完成後填入實際證據。未完成的後續單元素材標記為 `PLANNED`，不得在 HTML 產製前宣稱 `READY`。

## Micro-sequence

第一個可測試的三課鏈為 CH1-1 → CH2-1 → CH3-1：CH1-1 產出的任務定義，會在 CH2-1 變成收件者／語氣／格式決策；CH2-1 的讀者判斷在 CH3-1 轉成「誰需要知道哪個主張、證據在哪裡」。CH3-1 的證據與未知狀態再交給 CH4-1，成為工作／生活方案決策的資料邊界與待確認清單。

## PRAC2-1 補充契約與環境

PRAC2-1 是 CH2 三小時內的獨立演練頁，不另增加第五個單元時數。學員獨立選 A 報表改善、B 文件交接或完整個人企劃，第一步讀 P01／P10 說出主管與核准請求。完整企劃、共用提示詞、來源對照、恢復文字與實跑PDF已提供於 assets/workplace/gamma/。完成自己的十頁大綱、Gamma貼入文字、可編輯Gamma、重開驗證的十頁PDF與quick-check短交接。

OP-07：保留來源事實與狀態，依主管決策取捨十頁資訊，確認Gamma十張，至少修一項具體問題後匯出全部卡片、重開PDF。來源錯回企劃；多頁回文字分段；改事實回核對大綱；截字回原卡片；僅一頁回全部卡片匯出。採購零元不等於總成本零、預計不等於完成、待確認不等於損失。

Gamma 環境日期：授課帳號 Agent 於2026-10-07已實跑A／B。每人需自己的可建立、編輯與匯出帳號；額度／權限依課前確認，不要求升級。無法生成時保存大綱與貼入文字並標「Gamma待補」，不算正式完成。經典生成器提供替代路徑，未實跑；真人90分鐘節奏與冷跟做仍待驗證。

CH2配置：文字90分鐘＋Gamma90分鐘，共180分鐘；若Gamma真人試跑需120分鐘，前段須重排60分鐘。所有時間均為教學規劃，不是實測成效。


## 2026-10-11 全課逐步操作補強

保持四章各3小時，每人獨立選案。各章「先看」與正式操作分開；完整材料先於輸入，步驟交代位置、用意、預期結果與修復。CH1提供三案已填起稿prompt並教本機儲存、下載及重開；CH2示範客戶→主管真正讀者轉換及工作短訊息；Gamma使用新的完整企劃，分清來源、大綱、貼入文字、可編輯文件及PDF；CH3來源→第一版→引用核對→修訂；CH4原限制→同標準驗算→只改一限制→一頁PDF。已有工作台鍵與選做資料保留，不新增全班共同作業或重抄記錄。

本次驗收以 _repair/2026-10-11-step-by-step/REPAIR-REPORT.md 為準；不能沿用舊hash的PASS。平台帳號實跑與真人節奏須依新正文另驗，不能把作者文字審查當成已證明教學可用。
