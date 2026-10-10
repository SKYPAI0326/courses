# 講師教學可用性與零基礎閱讀審查

審查日期：2026-10-09。範圍：課程入口、單元頁、CH1–CH4、PRAC2 Gamma 演練，以及相關素材、教案與既有試跑紀錄。本次只新增審查報告，未修改講義。

## 結論

**目前已具備實作課的內容與材料，可以作為講師備課底稿；仍不宜原樣作為零基礎學員的主要跟做講義。** 講師若已準備帳號、素材並熟悉各條路徑，可以帶課，但需要頻繁口頭翻譯術語、指出目前應看的區塊、解釋哪些要求可以忽略。這會增加巡堂負擔，也讓較慢的學員依賴講師。

問題已不只是「概念太多、缺少實作」。現在有工作原文、完整提示詞、前後版、查核與恢復方法。主要問題是把教學設計、保存規格、舊版相容說明及驗證紀錄，一起放進學員當下要讀的文字；部分必要操作則只寫結果，沒有教學員如何取得結果。

目前有一項明確的發放缺口：Gamma 開場要求閱讀的兩份 PDF，本機存在，但沒有進入目前記錄的 `origin/main` 版本。另有工具入口、必做範圍、命名及前後說明不一致等問題。零基礎真人完成時間與理解程度也尚未驗證。

## 已經補強到位，應保留的內容

- 四章各有不同能力：CH1 從單一原文起稿與修正；CH2 依讀者改寫文字，接著完成 Gamma 提案；CH3 核對多份文件與引用；CH4 比較方案並在條件改變後重判。
- 教育行政、服務交接、業務支援等案例，能讓不同單位的學員選擇接近自身工作的任務。沒有自己資料也有完整模擬素材。
- CH1 的設備通知小示範、CH2 的完整 Email 前後版，已呈現「提供什麼資料、得到什麼文字、哪裡需要改」。應保留這種完整示範。
- PRAC2 有完整企劃、十頁大綱提示、Gamma 貼入文字與 PDF 匯出檢查，已形成實際製作流程。
- 已有網頁工作台與匯出功能，並允許部分情況人工修正。因此不應籠統把現版說成仍只有紙上作業；要改善的是紀錄要求與跟做安排。

## 逐章判斷

| 範圍 | 講師可以直接利用的部分 | 零基礎學員主要會卡在哪裡 | 優先調整 |
|---|---|---|---|
| 課程入口／單元頁 | 能看出四章不同成果與十二小時安排 | 摘要大量列規格、檔名與完成線，還沒開始就要理解整套流程 | 每章先說會完成什麼及第一個動作 |
| CH1 | 短小原文、五欄說明、完整錯誤與修正示範 | LLM 取得依賴課前安排；成果要求在多處重述，混入因果保證等進階用語 | 先完成一次送出與貼回，再逐步介紹核對 |
| CH2 | Email 完整示範最清楚，讀者轉換有具體差異 | 任務契約、工作台、概念、選做自我介紹、必答題與 Gamma 互相穿插；人工修正說法矛盾 | 整理成文字任務到 Gamma 的單一順序，同步必做題目 |
| CH3 | 三文件具體，來源矛盾與尚未執行的判斷有工作價值 | 「加入三份來源」缺少從複製文字到可用來源的完整操作橋接；來源、主張、引用、版本效力集中登場 | 先做完一筆引用核對，再讓學員做另外兩筆 |
| CH4 | 限制、數字與改變條件的案例完整，可練實際取捨 | 案例 A／B 與方案 A／B 重名，英文代稱與兩種字數口徑增加辨認負擔 | 改用具體方案名稱，分案呈現計算與修正 |
| PRAC2 Gamma | 前置企劃及後續輸出完整，匯出全部卡片的提醒具體 | 開場示範 PDF 發放缺件；跨工具存檔有跳步；自帶企劃不一定有 P01–P10 編號 | 先修示範發放，再提供一次完整保存及來源對照示範 |

## 問題清單

嚴重度說明：BLOCKER 是必要材料缺件，阻擋相應教學步驟；MAJOR 是容易使學員停住、做錯或不清楚完成標準；MINOR 是局部不清楚或維護問題。優先順序以實際教學影響判斷，不以文字長度單獨判斷。

### B01｜BLOCKER｜素材發放：Gamma 開場參考 PDF 沒有進入發布版本

**位置：** [PRAC2-1.html:131](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/PRAC2-1.html:131>)，開場「先開啟兩份實跑成果」。

**證據：** 125 個相對連結在本機都找到檔案；其中 `case-a-gamma.pdf`、`case-b-gamma.pdf` 不在目前記錄的 `origin/main` 樹中。`git check-ignore -v` 確認兩檔被根目錄 `.gitignore:2` 的 `*.pdf` 排除。追蹤版本為 `4c5f518bd72387cabfde8e2396ab7d9860f4b89f`，未在本次重新 fetch。

**影響：** 用本機檢查素材會通過，但依該 Git 版本發放的課程缺少學員第一步要看的完成品。

**建議：** 明確納入這兩份課堂 PDF，或提供已可取用的替代成品；從實際發放入口確認能開啟十頁。此次外網讀取沒有取得結果，不能把此項寫成已確認線上 404；已確認的是 Git 發放包缺件。

### M01｜MAJOR｜操作橋接：工具準備條件有寫，零基礎的開始步驟仍不完整

**位置：** [CH1-1.html:119](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH1-1.html:119>)、[CH3-1.html:107](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH3-1.html:107>)、[PRAC2-1.html:154](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/PRAC2-1.html:154>)。

**問題：** 最小啟動卡對自學者的取得路徑是搜尋「文字型語言模型」、自行選工具並依登入流程操作。CH3 要求建立筆記本、分別加入三份文字，但沒有一個從本頁複製到平台加入來源的完整小示範。Gamma 要求建立資料夾與保存四種檔案，後續直接寫「保存為自己的10頁大綱.md」，沒有示範如何把回答保存成可重開的檔案。

**影響：** 具備瀏覽器與複製貼上能力，仍不等於已知道如何取得工具、建立文字來源、保存指定檔案。課前逐人準備若未落實，實作會停在入口。

**建議：** 保留工具可自行選擇的原則，另外準備當次授課實際可用的入口卡。上課前逐人確認能送出一句話、複製回答、保存並重開。CH3 示範加入第一份來源，成功後讓各人加入自己的另外兩份；Gamma 示範保存第一份大綱，不再增加學員紀錄表。

### M02｜MAJOR｜閱讀順序：成果與完成要求反覆出現，教學規格搶在操作前

**位置：** [CH1-1.html:115](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH1-1.html:115>)、[CH2-1.html:123](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:123>)、[CH3-1.html:100](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH3-1.html:100>)、[CH4-1.html:110](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH4-1.html:110>)。

**問題：** 同一章的成果、前後版、待確認、保存、匯出重開等要求，在開場、工作台、步驟與結尾多次重述。CH2 開場八列「學員任務契約」還要求先理解下一位使用者、可觀察結果、回復代碼等。工作台說明出現「使用原v2暫存位置，舊紀錄與欄位全部保留」，是維護說明，不能幫新學員決定現在做什麼。

**影響：** 學員必須先整理規格，才能找到實際操作。反覆宣告「每人獨立、不需同學成果」也佔用閱讀空間；保留一次清楚說明即可。

**建議：** 頁首先留「今天要做的作品、需要的材料、第一步」；工作台只說如何貼回與保存；最後集中一次完成檢查。教學契約、版本相容及內部試跑紀錄移到教案或教師備註；學員會遇到的工具失敗與續做方法仍留在對應步驟。必要條件在用到的步驟出現，不把全部條件提前列完。

### M03｜MAJOR｜主線一致性：CH2 選做內容仍進入必答題與主要敘事

**位置：** [CH2-1.html:154](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:154>)、[CH2-1.html:268](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:268>)、[CH2-1.html:378](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:378>)。

**問題：** 三版自我介紹已標選做，但主要段落仍把它與短訊息一起介紹，頁尾第二題又以「你的三版自我介紹都完成了」為前提。學員跳過選做內容，會遇到沒有做過的檢核題。開場任務契約還保留第4單元將這個情境個人化的描述，與目前獨立決策案例的主線不夠一致。

**建議：** 必答題改用已做過的 Email 或短訊息，測試能否辨認新增事實；自我介紹題留在對應選做區。主線讀完及匯出後，直接進入 Gamma，課後素材集中在後方。

### M04｜MAJOR｜完成路徑：CH2 對人工修正的指示前後矛盾

**位置：** [CH2-1.html:266](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:266>)、[CH2-1.html:353](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:353>)、[CH2-1.html:369](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:369>)。

**問題：** 前面允許找不到依據的內容刪除或補限制重跑；後面又說「不能靠手動刪掉日期代替修復」，再次失敗時只要求停下判斷。學員難以分辨是在練提示詞診斷，還是在完成可以使用的 Email。CH3、CH4 已允許一次修訂後人工核對收尾，CH2 沒有同樣清楚的終點。

**建議：** 寫成「先指出多出的日期，再補限制試一次。若仍有錯，依原文手動修正；保存模型版與人工修改後的成品。」保留提示詞修正的學習成果，也讓學員知道如何完成工作。

### M05｜MAJOR｜命名：CH4 的案例與方案共用 A／B

**位置：** [CH4-1.html:305](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH4-1.html:305>)、[CH4-1.html:393](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH4-1.html:393>)。

**原句片段：**「A原上限240分鐘時兩方案都可行，依場次少優先暫定A……B原每角色30分鐘時……暫定B」。

**影響：** 同一段的 A 有時是補訓案例，有時是其中一個方案；學員即使算得對，也可能誤讀應該改選誰。兩案例的數字又同時出現，增加混用機會。

**建議：** 案例用「補訓案」「交接案」；方案用材料中的具體做法命名，例如「兩場方案／三場方案」，不再只用字母。算式與修訂各放在所選案例附近，另一案保持可另行查看。

### M06｜MAJOR｜淺白用語：未解釋的術語與內部代碼佔據操作句

**位置：** [CH1-1.html:127](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH1-1.html:127>)、[CH3-1.html:175](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH3-1.html:175>)、[CH4-1.html:117](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH4-1.html:117>)。

**問題：**「完整brief接在compare提示詞後」「單一變因」「條件式選擇」「主張」「版本權威」「因果保證」等詞，要求初學者先翻譯才知道動作。U1／U3／U4 代碼與英文 worked example 也沒有比「起稿」「查看引用」「缺資料」更直接。

**建議：** 用中文工作名稱作主要標籤，代碼保留給教師定位。先說動作與一個例子，再介紹確實需要的名詞。以下改寫表可作為統一口吻的起點。

### M07｜MAJOR｜來源對照：Gamma 自帶企劃路徑缺少編號調整

**位置：** [PRAC2-1.html:346](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/PRAC2-1.html:346>)、[PRAC2-1.html:359](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/PRAC2-1.html:359>)。

**問題：** 頁面允許帶自己的完整企劃，但大綱提示詞固定要求引用 P01–P10。課程兩份企劃有這些編號，自帶文件可能沒有。提示詞及完成檢查未清楚區分兩種來源，可能造成模型編出定位或學員無法對照。

**建議：** 課程案例沿用 P 編號；自帶企劃則要求「使用原文小標題，必要時附原句」或先明確教如何加段落編號。不要讓學員為了套用模板，額外重寫一份企劃。

### M08｜MAJOR｜進度安排：時間表缺少零基礎試跑證據

**位置：** [CH2-1.html:154](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:154>)、[PRAC2-1.html:118](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/PRAC2-1.html:118>)。

**問題：** CH2 三小時包含 Email、短訊息、一次讀者轉換、來源閱讀、大綱生成與核對、Gamma 生成、至少一次修訂、PDF 重開。授課帳號成功生成兩案，並不證明零基礎者能在後半90分鐘完成。現有待驗文件也明示這個時間與真人理解尚待驗證。

**建議：** 先沿用既定十二小時，不直接新增時數。以真正初學者各自完成一案，記錄首次登入、文字保存、跨工具切換及修正所需時間；再決定壓縮重複紀錄、合併可沿用的文字成果或調整各步時間。觀察由講師記錄，學員不多填測試表。

### N01｜MINOR｜規格負擔：兩種字數算法壓過作品品質

**位置：** [CH4-1.html:303](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH4-1.html:303>)。

CH1 用含數字與標點的非空白字元；CH4 又只計漢字，連標題與表格也計，最後另驗列印一頁。規則本身有寫清楚，但零基礎課為此付出的理解成本偏高。建議主要完成標準先用「一頁可讀、算式與待確認保留」，精確計數交給工具或教師檢查；若必須保留字數上限，應統一說明和計數方式。

### N02｜MINOR｜舊文案未整理：選做標題及殘句仍混亂

**位置：** [CH1-1.html:395](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH1-1.html:395>)、[CH3-1.html:404](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH3-1.html:404>)。

「選做：原概念、案例或課後延伸」只表示歷史來源，沒有告訴學員要解決什麼。「查核由自己進行，不需自己或個人成果」語意不成立，且在多個區塊重複。應按實際用途命名，例如「課後練習：核對新聞中的日期與數字」，刪除或重寫殘句。

舊內容有折疊，CH4 的大量生活卡也嵌套在選做區；本審查沒有把它們全部當成學員必讀。問題是折疊標籤與必要區塊之間的辨識成本，不是要求刪除所有延伸材料。

### N03｜MINOR｜段落密度：CH3 把不同情境塞進同一段

**位置：** [CH3-1.html:372](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH3-1.html:372>)。

一段同時講平台不可用、人工備援、恢復步驟、引用驗收、功能名稱、產品名稱、短來源引用及試跑邊界。應拆成「現在無法使用怎麼辦」「恢復後怎麼繼續」兩段，把命名與測試日期放教師備注。涉及「尚未執行」與「資料沒寫」的差異仍有必要，要用一對具體句子說明，不能為求短而刪除。

### N04｜MINOR｜HTML 結構：CH2 有兩個無效關閉標籤

**位置：** [CH2-1.html:273](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:273>)、[CH2-1.html:274](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/CH2-1.html:274>)。

結構驗證回報兩處 `unmatched closing tag </br>`。應改為合法換行或移除多餘標籤，再驗證。瀏覽器可能會容錯，本次沒有重現它造成顯示異常，不能誇大為學員一定無法使用；但不能宣稱全部靜態檢查通過。

## 可直接採用的淺白改寫

| 現有說法 | 建議寫法 | 保留的意思 |
|---|---|---|
| 把完整brief接在compare提示詞後 | 展開你選的案例，複製全部資料，貼在「比較兩個方案」提示詞下方。 | 材料要完整，順序明確 |
| 只改一個變因／單一變因 | 這一輪只把講師可用時間從240改成228分鐘，其他條件不變。 | 一次改一項，才能比較 |
| 主張核對 | 選三句重要回答，點旁邊的引用，確認原文有沒有支持這句話。 | 回查實質依據 |
| 應改為條件式B | 改選三場方案；上課時間確認後再定案。 | 推薦仍有未確認條件 |
| 第一個可觀察結果是…… | 送出後，你應該看到一份完整短文。 | 說明完成後的畫面與結果 |
| 使用原v2暫存位置，舊紀錄與欄位全部保留 | 按「儲存」，重新整理頁面，確認剛才貼上的內容還在。 | 學員實際需要的保存檢查 |
| 查核由自己進行，不需自己或個人成果 | 請自行核對，不需要其他學員的檔案。 | 獨立完成 |
| 前後結果還可能受模型生成差異影響，不把一次比較當因果保證 | 每次回答可能略有不同。這次記下哪一句變好了，以及你改了什麼指令。 | 不過度解釋一次比較 |

「原文明確支持／部分支持／未提及／矛盾」不是全部刪掉即可。先用一個具體問句帶出區別，例如：公告說18人，會議記錄只是建議20人；先依公告回答18人，把20人列為待確認。學員看過這個判斷，再介紹四種標記。

## 建議修訂順序

1. **先讓課堂能開始。** 補齊實際發放的 Gamma 參考 PDF；確認每人帳號可用；示範來源加入與保存重開；修 CH2 前後矛盾及無效標籤。
2. **重編目前必做路線。** 保留完整案例和提示詞，每章按照「看完成品 → 做第一步 → 看結果 → 核對 → 修一次 → 保存」安排。學員只看自己選案的數字與檢查，其他案例仍可查看。CH2 的必答題同步當前任務。
3. **清理學員文字。** 將版本、試跑狀態、驗收代號及舊作業歷史移到教案；操作句改用中文具體動詞。選做區按用途命名，統一完成檢查，保留必要的事實與未知判斷。
4. **做零基礎真人試跑。** 讓2–3位初學者分別獨立操作，不互相提供文件。先試 CH1 開始段與 Gamma，再試 CH3 來源加入和 CH4 條件變更。講師記錄學員在哪一步停住、讀懂了什麼、能否重開自己的成果及耗時，再修正文與時數。

不建議此時繼續增加案例數量。現有素材足夠，先把每位學員獨立完成一份工作成品的路走順，補強效果更直接。

## 本次驗證與限制

- 已閱讀七個入口／講義頁面的主要文字、教案／大綱、完整材料與關鍵提示詞；選做內容核對了入口、部分步驟及一致性，沒有把所有折疊內容當必讀。
- 五份學習頁面 lint：0 BLOCKER、0 ERROR、5 WARN。警告需結合語意判斷，例如範例 Email 的「您」不直接等於文案問題。
- 五份頁面內容素材機器檢查：未回報缺失素材，語意審查仍待人工判定。這個結果沒有涵蓋 Git 發佈包的 PDF 遺漏。
- HTML 結構檢查：CH1、CH3、CH4、PRAC2 通過；CH2 因兩處 `</br>` 未通過。
- 125 個相對文件連結本機存在；其中兩份 Gamma PDF 不在記錄的遠端追蹤樹。已確認忽略規則；未重新 fetch，也未確認線上 HTTP 狀態。
- 既有平台證據：Gamma 為授課帳戶兩案的生成與匯出；其他章節此前七案中三案末稿符合、四案需人工備援。本批修訂提示詞仍有待重跑項，不能把舊結果當新版本已驗證。
- 本次沒有當前頁面的瀏覽器視覺／點擊檢查，也沒有零基礎真人跟做。因此沒有驗證當前桌面與手機閱讀、剪貼簿功能、其他帳號權限，以及90／180分鐘實際完成時間。

### 審查快照

為避免後續修改混淆，以下為本次主要文件 SHA-256 前12碼：

| 文件 | SHA-256 前12碼 |
|---|---|
| index.html | d266355eec77 |
| module1.html | b87ecb41818a |
| CH1-1.html | 2667f42cb806 |
| CH2-1.html | 1cc74d3a995a |
| CH3-1.html | 1437d6a2682e |
| CH4-1.html | 180dca581959 |
| PRAC2-1.html | aaa7caa9bdab |
