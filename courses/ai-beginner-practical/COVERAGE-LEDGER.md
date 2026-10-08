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
| CH1-A08 | core | gap comparison | E-23,E-24,E-25 | OP-02 / 找一個缺少條件並重問 | SECTION 04 |
| CH1-A09 | core | finished artifact | E-26,E-27,E-28 | OP-01,OP-02 / 保存個人工作短文、唯一缺口修復與前後核對 | SECTION 05 |
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
| CH1-A08 | core | gap comparison | E-23,E-24,E-25 | OP-02 / 找一個缺少條件並重問 | CH1-1.html#lesson-practice 步驟 8 | 晚餐示範與步驟 8 要求指出缺口、補一個條件、重問並比較 | 任一前面完成的回答 | 輸入一個缺少的條件與重問指令 | 能說明新增條件在哪裡生效、仍缺什麼 | 看不出差異時回到 U1-GAP，只補最關鍵的一項 | CH1 → CH2 |
| CH1-A09 | core | finished artifact | E-26,E-27,E-28 | OP-01,OP-02 / 保存實務紀錄 | CH1-1.html#workplace-practice U1-SAVE；#lesson-check | 目前工作主線保存完整五欄prompt與首版、單一修正、新版短文、待確認／確認者及下一步；五題與拆解表選做 | 頁內工作台的填寫內容 | 按工作台「匯出 Markdown」產出 `unit1-practice-sheet-complete.md` 並逐項檢查 | 沒參加課程的人能看懂原始問題、回答、個人任務卡與待查處 | 缺原始提示詞時回到 U1-SAVE 用「複製提示詞」補回，不刪除既有回答 | CH1 → CH2 |
| CH1-A10 | supporting | recovery | E-29,E-30 | OP-01,OP-02 / 備援 | CH1-1.html#lesson-start；#lesson-practice；#lesson-assets | 頁面提供離線備援結果與使用限制，且案例庫已先給正常路徑的示例 | `assets/fallback/unit1-dialogue-simulator.md` | 先用工作模擬材料／作者參考判單一缺口，標待重跑；恢復後重做自己所選一案的首版與修正 | 能指出備援只完成判讀，不能代替自己的一案實際輸出 | 回到 U1-START 或 U1-ASK，依缺失階段重做 | CH1 |

## Freeze rule

Pass 1 與 Pass 2 的 atom ID 與 classification 必須相同。若完整講義發現新增、拆分、合併或降級，先記錄原因與 reviewer verdict，再更新兩個 pass。

## Full-course supplement：CH2–CH4 與課後整合

本節保留 CH1-1 代表單元的原子編號，補上其餘 learner-facing 頁面的核心操作。每個 atom 都對應實際 section／stage ID、學員動作、完成物、驗證與修復位置；這份補充不把四頁的完成線當成內容證據的替代品。

| atom_id | classification | operation_id / evidence | learner action | finished artifact | verification / repair | handout location |
|---|---|---|---|---|---|---|
| CH2-A01 | core | OP-03 / 四段式提示詞 | 從 CH2-1 工作台與素材頁標出背景、任務、限制、輸出格式 | 工作台中的 Email 提示詞 | 四段都有值；缺段回 U2-PROMPT | CH2-1 `#communication-workbench`、`U2-START`、`U2-PROMPT` |
| CH2-A02 | core | OP-03 / Email 事實邊界 | 用固定背景產出主旨、正文、署名 | 1 封 Email 與第一版 | 12,000 元、7 個工作天、貼文數量追問保留；自造內容回 U2-EMAIL | CH2-1 `U2-EMAIL`、`U2-CHECK-2` |
| CH2-A03 | core | OP-03 / 讀者與下一步 | 把 Email 情境換成一則 2–4 句訊息 | 1 則訊息與第一版 | 收件者知道下一步；像 Email 回 U2-MESSAGE | CH2-1 `U2-MESSAGE` |
| CH2-A04 | supporting | OP-03 / 同資料三場合 | 用同一份資料表產出社交、交友、求職三版 | 3 版自我介紹與提示詞 | 圈出共同事實，再遮標題判斷用途；幾乎相同回 U2-INTRO | CH2-1 `U2-INTRO` |
| CH2-A05 | core | OP-03 / 讀者／場合轉換 | 自己的 Email 指定新讀者、對方下一步與輸出格式；第二份選做 | 工作台匯出的轉換前後版本與比較理由 | 寫出原讀者、新讀者、改變位置與保留事實；刪掉關鍵事實回 U2-AUDIENCE | CH2-1 `#communication-workbench`、`U2-AUDIENCE`、`U2-SAVE` |
| CH3-A01 | core | OP-04 / 同情境來源 | 自選A排課或B交接，自己加入同案例3文件 | 個人筆記本與來源名稱 | 三份可讀；失敗U3-SOURCE標待重跑 | CH3-1 #workplace-practice、#notebooklm-log |
| CH3-A02 | core | OP-05 / 主張查核 | 在所選一份成品挑三個重要主張，不另抄三閱讀表 | 三主張支持判斷 | 拆短句、期限與成效分開；失敗U3-CLAIM | CH3-1 #workplace-practice U3-CLAIM |
| CH3-A03 | core | OP-05 / 真引用回查 | 點NotebookLM引用讀原文，存來源名／短摘／支持狀態 | 引用回查與修訂紀錄 | 手寫DA／DB不是平台證據；失敗U3-CITE | CH3-1 #workplace-practice U3-CITE |
| CH3-A04 | core | OP-05 / 跨來源權威與範圍 | A18／20待確認、R教室3／一般5天；B首次回覆／結案、已登記／未回覆 | 一份FAQ／交接／待辦與未解問題 | 來源日期不當核准，未知有角色與下一步；U3-COMPARE | CH3-1 #workplace-practice U3-COMPARE／REPAIR |
| CH3-A05 | supporting | OP-05 / 三層閱讀選做 | 原書籍案例分作者／理解／小實驗，保留完整提示詞與原輸出 | 選做三層筆記 | 不列工作主線必做，不需再交第三份作業 | CH3-1 #lesson-demo、#lesson-practice 選做 |
| CH4-A01 | core | OP-06 / 框架 | 自選完整工作brief或有資料生活需求 | 實際完整提示詞、兩方案與三排序 | 限制／偏好／未知分開；U4-FRAME | CH4-1 #workplace-practice、#lifestyle-workbench |
| CH4-A02 | core | OP-06 / 硬限制與矩陣 | 用自己資料逐方案列式，分角色／週投入與一次性設定 | 第一版兩方案三標準比較 | 容量與分鐘有單位，未合格不可偏好補過；U4-TRADEOFF | CH4-1 #workplace-practice |
| CH4-A03 | core | OP-06 / 未知邊界 | 把出席、成效、設定核定、日期未提供保留在正文 | 同一份建議中的確認問題 | 假設工時不寫已達成節省，0現金不寫無成本；U4-MISSING | CH4-1 #workplace-practice |
| CH4-A04 | core | OP-06 / 單一變因與取捨 | A上限240→228；B文件窗口30→25，其餘不動 | 修訂卡與受影響計算、代價 | A改條件式B；B改條件式A；設定及未知保留；U4-CHANGE／DECIDE | CH4-1 #workplace-practice |
| CH4-A05 | core | OP-06 / 可重開保存 | 匯出實際提示詞、第一版、變因指令、修訂與下一步 | unit4-decision-card.md | 自己重開能找依據與未知；U4-SAVE | CH4-1 #lifestyle-workbench |
| CAP-A01 | supporting | 課後整合 / 遷移驗收 | 用真實需求填五欄、保存第一版、缺口或取捨判讀與待確認事項 | `course-capstone-handoff.md` | 沒看過課程的人能讀懂並重做；缺欄回工作表對應區段 | module1 `#course-capstone`、`assets/worksheets/course-capstone-handoff.md` |

## Supplement freeze rule

本次補充的 atom ID 固定為 `CH2-A01`–`CH2-A05`、`CH3-A01`–`CH3-A05`、`CH4-A01`–`CH4-A05`、`CAP-A01`。若 L4a 或 L5 發現 learner path 斷裂，先在修復報告標註上游來源，再修改 atom 證據，不刪除原子以掩蓋缺口。

## Learner Task Contract evidence map

本表不新增契約；它只把唯一契約的八欄映射到每個 learner-facing 頁面，供 reviewer 與 validator 冷讀時定位。完整的輸入、動作、結果、驗證與修復仍以各 atom 的 Pass 2 證據為準。

| lesson | role/context | problem/consequence | starting material + fallback | finished artifact | next user/use | first action + observable result | recovery position |
|---|---|---|---|---|---|---|---|
| CH1-1 | 文字型 LLM 初學成人；工作／生活小任務 | 模糊提問造成泛答、漏條件，無法重做 | 頁內工作台；瀏覽器不能暫存用 `assets/worksheets/unit1-practice-sheet.md`；LLM 不可用看 `assets/fallback/unit1-dialogue-simulator.md` | 工作台填寫紀錄匯出為 `unit1-practice-sheet-complete.md` | 自己用任務卡重做；CH2 承接五欄定義 | 開啟工作台並填姓名日期；看到第 1 題欄位與進度變化 | `U1-START`、`U1-ASK`、`U1-GAP`；不能暫存時匯出／列印後停止 |
| CH2-1 | 對不同讀者寫日常文字的成人 | 讀者／目的／語氣不清造成誤解與重寫 | 頁面日常溝通工作台、`assets/templates/unit2-communication-scenarios.md` 或 HTML 素材頁；工具不可用標待重跑，Markdown 作離線備援 | 工作台匯出的 `unit2-communication-pack-complete.md` | 自己與實際收件者可編輯、交接 | 開啟工作台填第一個情境；看到 Email／訊息必做區、選做自我介紹與檢核表 | `#communication-workbench`、`U2-START`、`U2-PROMPT`、`U2-EMAIL`／`U2-MESSAGE`、`U2-AUDIENCE` |
| CH3-1 | 教務／服務／各單位承辦人 | 把新會議當核准或回覆當結案 | 個人NotebookLM與同案例三文件；離線人工定位標待重跑 | 一份工作文件、引用回查與匯出紀錄 | 接手人與未來自己能回原文 | 選來源建立自己的筆記本，看三名稱及原文 | #workplace-practice、U3-SOURCE／CITE／COMPARE／SAVE |
| CH4-1 | 有工作／生活決策的成人 | 忽略硬限制或各角色週額度 | 自選兩方案brief與個人LLM；不可用先人工計算 | unit4-decision-card.md | 主管／未來自己看條件與取捨 | 讀完整brief接提示詞，兩方案三排序可辨 | #workplace-practice、U4-FRAME／MISSING／CHANGE／SAVE |

### Contract evidence review rule

每列的八欄都必須能在對應教案與 HTML 找到具體文字、連結、檔名、輸入值、預期結果與回修位置。只有標籤、摘要、頁尾資產清單或講師筆記，不算 Pass 2 證據。

## 2026-10-07 授權擴充與重新凍結

使用者要求以個人工作實作補強，維持12小時；CH2-A04由core改supporting，示範、資料、原欄位與三版輸出保留。CH2-A05最低完成一次Email讀者轉換，第二份保留選做。這是有理由的時間重配，不刪原子或教材掩蓋缺口。作者自審已確認新目標、180分鐘與入口同步；真人節奏未通過。

| atom_id | classification | input / decision | output / verification | repair | location |
|---|---|---|---|---|---|
| PRAC2-A01 | core | A／B／完整個人企劃；主管要核准什麼 | 自己的完整企劃與P01／P10核准請求 | 缺目的回企劃，無個人材料可選A／B | PRAC2-1 #gamma-source |
| PRAC2-A02 | core | 完整企劃＋outline提示詞；事實、狀態與單位 | 十頁大綱，每項關鍵內容有來源；未知不變已完成 | 漏規則回P03，超頁回正式十頁限制 | PRAC2-1 #gamma-outline |
| PRAC2-A03 | core | 已核對大綱＋gamma-text提示詞 | 十段、九個分隔；來源／備註不變正式卡片 | 改事實回大綱，密集先保留核准條件 | PRAC2-1 #gamma-text |
| PRAC2-A04 | core | 十段文字＋生成指令；核對大綱 | 自己的Gamma恰好十張，可編輯 | 額度不足保存待補，介面變動按替代入口 | PRAC2-1 #gamma-generate |
| PRAC2-A05 | core | Gamma初版；選一項影響閱讀／判斷的問題 | 有理由修訂、全部卡片PDF重開十頁 | 密集回原卡片，單頁回全部卡片匯出 | PRAC2-1 #gamma-export |
| PRAC2-A06 | core | 已有成果，依quick-check檢查 | 五欄短交接；來源、理由與待確認可重查 | 缺檔回對應產出，不重抄十頁 | PRAC2-1 #gamma-handoff |

新原子PRAC2-A01至A06的分類凍結為core；完整企劃、共用提示詞與PDF是核心材料。版型轉製必須逐段保留PRAC2-1正式正文與所有表格、錯例、完整指令及恢復路徑。入口／完成／理解／遷移的真人證據另列，不由機器PASS代替。

## 2026-10-08 CH3／CH4個人工作實作調整

CH3-A05改supporting，原三類閱讀不再全部必交；其餘原子轉到同案例三文件與一份有讀者工作成品。CH4原共同冷氣不再必交，兩方案比較落在各人所選brief；增加真正的單一硬限制變化，保留原生活完整例子選做。兩章各180分鐘，v2 key和全部原字段保留；精簡必填而非刪除舊紀錄。作者內容自審PASS，平台引用與真人節奏待驗，無全課完成宣告。
