# 診斷 D：M6 GA4／M7 GTM（2026-11-01）

範圍：`module6.html`、`m6-1`～`m6-5`、`module7.html`、`m7-1`～`m7-4`。只讀，未改任何頁面。
正文抽取：`<h1` 至 `<nav class="nav-footer"`（module 頁取整頁正文），已去除 script／style／密碼閘。
碼密度＝課程自創碼（狀態標籤、檔名、Part 編號、A/B/C 軌、D/T/S、模組代碼）÷ 中文字數 × 1000。

## 跨頁先講的三件事

1. **共同案例斷線**：M6／M7 十頁「山徑咖啡」出現 0 次。練習包 GA4 段用「日日沖煮」（電商、purchase），GTM 段用課程頁「預約體驗」（generate_lead／`cta_name=trial_booking`／`page_type=course_landing`），m7-4 dataLayer 範例商品是「數位行銷課程」。M10 品牌包卻寫「M7 量測設計」並用 `comparison_open／booking_start／booking_complete` 事件鏈，三套事件命名互不相認，M10 接不上 M7 的完成物。
2. **M6 先於 M7 的前提沒處理**：m6-1 標題是「安裝完代碼後，還要做這五件事」，但安裝代碼的實作在 m7-2；m6-1 要 A 軌用 DebugView 重現事件、用「GTM Preview」查證；m6-3「事件尚未驗證？先回 M6-1」；m6-4 漏斗要求「事件也已存在」。真實環境軌在 M6 期間其實沒有已安裝、已驗證的事件可用。
3. **同一份完成物的建立點互相矛盾**：m6-5 說本模組交付物是 measurement-decision.md；m7-1 又寫「先建立 measurement-decision.md」；m6-1 說「進入 M7 時…帶入 measurement-decision.md」。練習包 Part 3 的模板有一半是 GTM／Consent 欄位，M6 學員填不了。

---

## Module 6

### module6.html｜GA4 數據分析：從報表到決策
- 完成物：未列模組完成物；單元卡 6-5 提 measurement-decision.md。
- 承接：開場沒有接 M5 SEO（m6-1 有提 Search Console 連結，但總覽沒說 SEO 之後為何看 GA4）；結尾只有單元卡。
- 與單元頁一致性：
  - 6-3 卡寫「客層與興趣分析」，m6-3 正文沒有客層段落。
  - 6-4 卡寫「使用者需求分析」，是 User lifetime 的誤譯（見 m6-4）。
  - AI 接口四條與單元頁的防護說法相反：「請它解讀異常數據並提出可能原因」「識別哪些用戶群組的轉換率最高」把判讀交給 AI；第 4 條「協助撰寫 A3 報告書草稿」，m6-5 沒有 A3 草稿任務。
- 疑似過時：「轉換率最高」（GA4 2024 起改叫 key event／關鍵事件率，轉換只留給 Google Ads）。
- 噪音：自創碼 2（M6、measurement-decision.md）；「AI 接口」標籤是課程自創說法。
- 建議：保留結構小修：卡片描述對齊正文，AI 接口改成「AI 協助整理，判讀由你做」。

### m6-1-setup｜GA4 建置：帳號架構與介面導覽｜完成物 ga4-setup-check.md
- 承接：開頭沒有接 M5，也沒說這個模組要回答什麼行銷問題，直接進帳號架構。結尾說「進入 M7 時…帶入 measurement-decision.md；這是 readiness 交接」，用代碼和英文詞交接。斷點：「安裝完代碼後」預設已安裝，但安裝在 m7-2 才教。
- 偏題：無明顯偏題；「AI 接口 · GA4 建置自我檢核」的表格大量在講 Google Ads conversion、跨網域，對建置頁偏重。
- AI 比重：一段 prompt 要 AI 依描述整理檢核表與紅綠燈，性質是清單整理，比重適中；但參考輸出的表格欄位寫法（🟢🟡）與練習要求的「已驗證／待處理／不適用」三值不一致。
- 疑似過時：
  - 「路徑：管理 → 資源設定 → 資料保留」：現行選單疑似是「資料收集和修改 → 資料保留」；也疑似已拆成事件資料／使用者資料兩種保留期。
  - 「預設只保留 2 個月的事件數據（探索分析用）」：需確認是否仍正確，以及有沒有說清楚標準報表不受影響。
  - 「定義內部流量 → 填入辦公室 IP」：沒提還要到「資料篩選器」啟用（測試→有效），只定義不會排除。
  - 「廣告 … 歸因模型比較、觸達程度報告」：2023 年底已移除多數歸因模型，「觸達程度報告」名稱存疑。
- 練習：三軌共同設定檢核，單人完成＋「互評者隨機抽兩項」（同儕互評）；A 軌要真實帳號，B 軌 Demo、C 軌離線都有路徑。C 軌案例「日日沖煮」不是共同品牌。
- 噪音：
  - 必要術語：Account／Property／Data Stream、G-XXXXXXXX、purchase、generate_lead、DebugView、Tag Assistant、Search Console。
  - 自創碼：PLATFORM VERIFIED×2、PENDING×3、readiness×1、ga4-setup-check.md×3、measurement-decision.md×1、A／B／C 軌×9、M7×2，約 21 個／1,932 字＝**10.9／千字**（M6 最高）。
  - 「key event」英文 6 次與「關鍵事件」5 次混用。
  - 提示詞開頭「我正在檢查 GA4，請把…」（含「請」）。
- 建議：保留結構小修：補「本頁先看介面與設定，代碼安裝到追蹤工程模組才做」的說明，狀態標籤改成中文三值，PLATFORM VERIFIED／PENDING 拿掉。

### m6-2-traffic｜流量分析：流量從哪來、值不值得｜完成物：無（只有 UTM 規則草案的參考輸出）
- 承接：開頭沒有接 m6-1（沒提要用剛建好的資源或 Demo）；結尾一句心法，沒接到 m6-3。
- 偏題：無；UTM 與流量來源都在 GA4 主線上。
- AI 比重：一段 prompt 請 AI 產出團隊 UTM 命名規則與 Sheet 欄位，性質是文件起草，有「待確認」防護，適中。
- 疑似過時：
  - 六種來源表把「Paid Search」「Organic Social」當主列，學習目標卻寫「Paid / Social」。GA4 預設管道分組現在有 Paid Social、Organic Video、Cross-network、Unassigned 等，需確認清單是否該更新。
  - UTM 只列 5 欄：GA4 另支援 utm_id、utm_source_platform、utm_creative_format、utm_marketing_tactic，需確認是否要提。
  - 範例「utm_campaign=summer2025」年份已過。
- 練習：**沒有練習區塊**。練習包 Part 1A（流量來源表＋「保留、調查、降低」任務）正好對應本頁，但頁面沒有連過去；也沒有離線路徑。
- 噪音：自創碼 0。必要術語：utm_source／medium／campaign／content／term、Session source／medium、Auto-tagging。提示詞開頭「請幫我設計…」。
- 建議：保留結構小修：補練習區塊並接練習包 Part 1A，換成共同品牌情境。

### m6-3-audience｜受眾與行為報告：了解你的用戶｜完成物：無（AI 分群的參考判讀）
- 承接：開頭「流量數字告訴你多少人來了」，有接 m6-2，寫得好；結尾一句心法，沒接 m6-4。斷點：取數步驟「事件尚未驗證？先回 M6-1」用代碼，而且 M6-1 本身沒有讓事件被驗證的手段。
- 偏題：「AI 接口 · 受眾分群 + 投放建議」偏向廣告投放模組（CPA、毛利、素材、預算、停止條件），超出 GA4 分析。大綱和總覽卡要的「客層分析」缺席。
- AI 比重：**過重**。導語寫「讓 AI 自動分群並給投放建議」，學員自己的判讀步驟只有取數；後段雖有防護，但核心分析交給了 AI。
- 疑似過時：
  - 「Reports → Acquisition → Traffic acquisition」：現行導覽疑似多一層「生命週期」或「業務目標」集合。
  - 「Admin → Audiences」：疑似是 Admin → 資料顯示 → 目標對象。
  - prompt 寫「各來源轉換率」，與 key event 改名衝突。
  - 同頁 UI 用英文（Reports／Admin），m6-1 用中文（管理 → 資源設定），介面語言前後不一。
- 練習：沒有正式練習；取數三步驟要真實帳號或 Demo，沒有離線路徑（練習包沒有受眾資料）。
- 噪音：自創碼 PENDING×2、M6-1×1（約 1.6／千字）；「key event」英文 3 次；`PENDING` 以程式碼樣式出現在學員正文。提示詞開頭「請依以下…幫我分…」。
- 建議：重寫後半：AI 段改成「AI 協助整理你挑出的分群條件」，投放建議移到廣告模組；補客層段或改總覽卡。

### m6-4-explore｜探索分析：回答標準報告回答不了的問題｜完成物：漏斗演練結果（最大流失點、裝置差異、單一變因測試）
- 承接：開頭沒有接 m6-3（m6-3 已介紹使用者路徑探索，本頁又講一次路徑分析）；結尾沒接 m6-5。
- 偏題：無；「使用者需求」一型的場景「評估不同廣告渠道的長期 ROI」需要成本資料，略超出 GA4。
- AI 比重：**偏重於計算**。prompt 要 AI 產出「計算表：…計算每步驟流失率」，流失率是學員該自己算的；練習區塊（老師示範／一起做）則由學員自己算，兩者重疊。
- 疑似過時：
  - 「五種探索類型」：GA4 探索現有任意形式、漏斗、路徑、區隔重疊、使用者多層檢視、同類群組、使用者生命週期等，需確認數量。
  - 「使用者需求（User Lifetime）」：中文介面疑似是「使用者生命週期」，此處誤譯。
  - 「評估課程報名流程的轉換」用語與 key event 改名衝突。
- 練習：D／T／S 漏斗演練，用練習包 Part 1B；「兩人互相檢查分母」是兩人互查，其餘單人。真實、Demo、離線三路都有。
- 噪音：自創碼 Part 1B×1、D／T／S 標籤 3（約 2.6／千字）。「老師示範：」寫在學員頁，是教法字眼外洩。必要術語：page_view／view_item／add_to_cart／begin_checkout／purchase、Funnel／Path／Segment Overlap／Free Form。提示詞開頭「請幫我設計…」。
- 建議：保留結構小修：更正類型數與譯名；AI 段拿掉計算，改成檢查步驟定義；D／T／S 改成單人可執行的步驟。

### m6-5-decision｜數據→決策：報告 × 假設 × 閉環｜完成物 measurement-decision.md（模組交付物）
- 承接：開頭「看懂數字只是開始」，有承接；取數第 3 步寫「從 M6-4 的 Explore 漏斗報告…沒建漏斗？先跑 M6-4 的演練」，用代碼。結尾「接下來進入 M7：GTM」「M10-3 會檢查」，用代碼。
- 偏題：「A3 報告書」整節講格式，但本頁不要求交 A3，交的是 measurement-decision.md。A3 最終報告是 M10 的完成物，兩邊重複；學習目標「整理成…一頁簡報」沒有對應練習。
- AI 比重：一段數據摘要 prompt，請 AI「識別最值得優先優化的 2-3 個問題點」，把優先排序交給 AI，**略重**；有「未知／待補」防護。
- 疑似過時：
  - 「進入 Reports，從…摘要或詳細報表取得…關鍵事件率」：報表名稱需確認。
  - 「左側導覽可被管理者客製；找不到時查 Report library」：寫法正確，只需確認位置。
- 練習：取數 3 步驟要真實或 Demo 帳號，離線軌沒有寫清楚要用練習包哪些數字（Part 1A 有參與率、Part 1B 有漏斗，可以組合）。交付單人完成。模板（練習包 Part 3）一半是 GTM 欄位，M6 學員填不了。
- 噪音：自創碼 M6-4×2、M7×1、M10-3×1、measurement-decision.md×1、Part 3×1（約 3.5／千字）。提示詞以「以下是我的 GA4 數據摘要」開頭，再接「請幫我：」。
- 建議：重寫交付段：決定 A3 留在這裡或交給 M10；M6 交付物改成只含 GA4 欄位的決策紀錄，GTM 欄位留給 M7 補。

### M6 模組小結
- 主線一句話：從 GA4 報表讀出有來源的觀察，轉成待驗證假設與一個決策。主線清楚，但每頁各自結束，頁與頁之間沒有句子接起來（m6-2→m6-3 例外）。
- 頁序：大致合理。m6-1 預設已安裝代碼、事件已驗證，與「M6 先於 M7」衝突；路徑分析在 m6-3、m6-4 各講一次。
- 與其他模組重複：
  - m6-1 的 key event／Google Ads conversion 與 m7-2 驗收後步驟重複。
  - DebugView／24–48 小時等待說法在 m6-1、m7-2 重複。
  - A3 與 M10 A3 Final Report 重複。
  - m6-3 投放建議與廣告模組（M8）重疊。
- 總覽頁一致性：客層、使用者需求譯名、AI 接口四條、A3 草稿四處不一致。
- 練習分布：只有 m6-1、m6-4 有正式練習；m6-2、m6-3 沒有；m6-5 的交付沒有離線數字來源。

---

## Module 7

### module7.html｜GTM：數據追蹤工程
- 完成物：AI 任務列寫 measurement-decision.md，沒有明確的模組完成物區塊。
- 承接：開場「你看到的 GA4 數據，是由追蹤代碼收集來的」，有接 M6，寫得好；接著第二句就是「先建立 Consent default／update」，英文技術詞進到總覽開場。
- 與單元頁一致性：四張單元卡與正文一致。大綱寫「含 GTM 課程連結」，頁面沒有連到 `courses/gtm/`。AI 接口三條中，「從共同量測練習包完成 measurement-decision.md」「把核准的事件契約交給開發」不是 AI 任務。
- 噪音：Consent×3、default／update×2、measurement-decision.md×1；M6 總覽有提共同起點／練習包，M7 總覽沒有連練習包。
- 建議：保留結構小修。

### m7-1-concept｜GTM 核心概念：四元素心智模型｜完成物 measurement-decision.md（配對＋故障 trace 判讀）
- 承接：開頭沒有接 M6，直接進四元素；練習段寫「若已完成 M6-1，就從 ga4-setup-check.md 帶入…把 GA4 readiness 標為 PENDING」，用代碼加英文狀態。結尾「CONFIG REVIEW PASS／PLATFORM VERIFIED」。
- 偏題：
  - 「兩個容易混淆的觸發器」與 7 步流程裡的 Step 3、Step 5（consent default／update），把 consent 實作提前到概念頁。
  - 練習 S「答案必須包含 default 太晚與 denied 時事件仍觸發」考的是 consent 順序，不是四元素。概念頁的檢核變成同意模式除錯。
- AI 比重：一段 prompt 請 AI 設計 Tag／Trigger／Variable 配置，有「待查、不可猜選擇器」防護，適中。練習 T 寫「不准讓 AI 補欄位」，口吻過硬。
- 疑似過時：
  - 「把 GTM 提供的兩段程式碼分別貼入 <head> 和 <body>」：仍正確，可順手確認。
  - 「Consent Initialization…Google tag 使用 Initialization」：說法正確，只需確認文件連結。
- 練習：D／T／S，「兩人一組把預約體驗拆成…」是分組，其餘單人；有離線路徑（練習包 Part 2）。
- 噪音：
  - 必要術語：Container／Tag／Trigger／Variable、Consent Initialization、Initialization - All Pages、Preview、Tag Assistant、{{Click Text}}、GTM-XXXXXXX。
  - 自創碼：CONFIG REVIEW PASS、PLATFORM VERIFIED、PENDING、readiness、ga4-setup-check.md、measurement-decision.md×3、Part 2、M6-1、M7、D／T／S，約 14 個／1,800 字＝**7.8／千字**。trace 4 次、Consent 英文 12 次、default／update 5 次、dataLayer 10 次。
  - 「老師示範：」寫在學員頁。
  - 提示詞開頭「請幫我設計…」。
- 建議：重寫練習段：概念頁只練四元素配對（用共同品牌的預約按鈕），consent 故障 trace 移到 m7-2。

### m7-2-ga4-setup｜GA4 × GTM 整合：同意先於量測｜完成物 measurement-decision.md（三種同意情境＋故障修復）
- 承接：「兩軌都續寫 M7-1 的 measurement-decision.md」用代碼；結尾交付判準，沒接到 m7-3。
- 偏題：無，但 consent 篇幅壓過 GA4 × GTM 安裝本身；九步驟中四步是 consent。
- AI 比重：一段 prompt 請 AI 做分階段驗收清單，性質是清單整理，適中；實際操作由九步驟承擔，比例合理。
- 疑似過時：
  - 「舊介面的 GA4 Configuration tag 已由 Google tag 取代」：正確，可確認措辭。
  - 增強型評估表寫 scroll「判斷內容完讀率」，與 m6-3「不能證明逐字讀完」**自相矛盾**。
  - 「GTM 右上角 → 預覽」：確認位置。
  - Basic／Advanced 說法：確認現行文件。
- 練習：老師示範／T 一起做／S 獨立驗收；「T 一起做」未寫明分組；有離線路徑。S 任務與 m7-1 S 幾乎相同（default 太晚＋denied 仍觸發），**重複考同一題**。
- 噪音：
  - 必要術語：analytics_storage／ad_storage／ad_user_data／ad_personalization、page_view／session_start／first_visit、G-XXXXXXXXXX、Enhanced Measurement 事件名。
  - 自創碼：PLATFORM VERIFIED、PENDING×2、CONFIG REVIEW PASS、measurement-decision.md×4、Part 2、M7-1、T／S 標籤，約 12 個／2,003 字＝6.0／千字。Consent 英文 22 次、default／update 16 次、trace 6 次（全課最高的英文詞密度）。
  - 步驟編號出現兩個「1」（「1 先選練習軌」「1 確認政策」）；示範段缺 D 標籤。
  - 提示詞開頭「請幫我做…」。
- 建議：保留結構小修：故障 trace 只在本頁考一次，Consent／default／update 改中文「預設同意狀態／同意更新」。

### m7-3-events｜自訂事件追蹤：按鈕、表單、捲動、連結｜完成物 measurement-decision.md（C 軌標 CONFIG REVIEW PASS）
- 承接：開頭「增強型評估涵蓋不了所有業務行為」，有接 m7-2，寫得好；結尾心法又回到「先有 Consent default／update」，沒接 m7-4。
- 偏題：「AI 接口」的 C 軌完成結果，又是 consent 故障 trace（default 太晚、denied 仍觸發 generate_lead），不是按鈕或表單事件。本頁主題是自訂事件，完成物卻沒有驗收四種自訂追蹤。
- AI 比重：**過重**。第 3 步原句「AI 給的設定步驟照做完，一定要先開 GTM Preview」，等於讓 AI 決定設定、學員照做。prompt 要 AI 輸出「GTM 內 4 步驟…每步要填的實際值」。
- 疑似過時：
  - 「Wait for Tags／Check Validation」：確認現行選項名。
  - 事件命名規則沒提長度上限（40 字元），需確認是否補。
  - 「Enhanced Measurement 的約 90% scroll」：正確。
- 練習：A 真實／C 離線兩軌，單人；B 軌缺席，未說明。
- 噪音：
  - 必要術語：Click ID／Classes、Form ID、Scroll Depth Threshold、cta_name、button_location、link_url、link_domain、form_submit、file_download、phone_click（自訂例）。
  - 自創碼：CONFIG REVIEW PASS×3、PENDING、measurement-decision.md×3、Part 2／Part 3×3、A／C 軌×5，約 15 個／1,816 字＝**8.3／千字**（M7 最高）。dataLayer 10 次。
  - 提示詞開頭「請幫我寫…」。
  - 參考輸出標題是追蹤「立即購買」按鈕，結果段卻是「預約體驗」，同一段換了兩個案例。
- 建議：重寫 AI 段與完成物：以共同品牌的按鈕與表單產出事件規格，AI 只檢查規格缺漏；consent 結果移除。

### m7-4-advanced｜進階追蹤：同意、Data Layer 與 GTM 除錯｜完成物 Data Layer 實作契約（MODULE 7 CORE CHECKPOINT）
- 承接：Consent 區明寫「這不是第一次設定 Consent：M7-2 已要求…」，用代碼；結尾「完成並重跑證據後，才進入下一個模組」，沒說下一個模組是廣告，也沒接 Meta Pixel 與廣告投放的關係。
- 偏題：「進階覆核：三種同意情境都要通過」是 m7-1／m7-2／m7-3 的第四次重複。Server-side tagging 說明框屬延伸，可留。
- AI 比重：一段 prompt 請 AI 設計 dataLayer 契約與工程需求單，參考輸出先報缺口，性質是起草，適中。
- 疑似過時：
  - Meta 段只談 Pixel，沒提 Conversions API；事件管理工具中「Pixel」疑似已改稱「資料集」，需確認。
  - dataLayer.push 範例前沒有先清空 ecommerce 物件（`ecommerce: null`），需確認官方是否仍建議。
  - 「GA4 後台 → 管理 → DebugView」：疑似是管理 → 資料顯示 → DebugView。
  - 「Meta Pixel Helper Chrome 擴充套件」：確認仍維護。
  - 「CONSENT MODE V2」：確認命名。
- 練習：只有 AI 段的 Data Layer 契約，單人；沒有離線資料（練習包沒有電商 dataLayer 或 schema），參考輸出只能回報缺口。範例商品「數位行銷課程」與共同品牌無關。
- 噪音：
  - 必要術語：Purchase／Lead／ViewContent／AddToCart／InitiateCheckout／Search、transaction_id／value／currency／items、view_item／add_to_cart／begin_checkout／purchase／refund、Fired／Not Fired。
  - 自創碼：M7-2×2（約 0.7／千字），但 dataLayer 21 次、Consent 15 次、Preview 10 次。
  - 提示詞開頭「請幫我設計…」。
  - 頁面中英混排嚴重，篇幅 2,752 字，是本區最長。
- 建議：重寫：刪掉第四次 consent 覆核，除錯表與 m7-2 合併，補共同品牌的電商或預約 dataLayer 練習資料。

### M7 模組小結
- 主線一句話：用 GTM 規劃、實作並驗證事件，讓 GA4 收到可信的資料。實際讀起來的主線變成「同意模式先於量測」，四頁都在考 consent 順序。
- 頁序：概念→整合→自訂事件→進階，大致合理；但 consent 在 m7-1 就實作，m7-4 又「進階覆核」，主題被拆散。
- 模組內重複：
  - 故障 trace 判讀當獨立驗收出現 3 次（m7-1 S、m7-2 S、m7-3 C 軌結果），m7-4 又做一次三情境覆核。
  - 「DebugView 看不到事件」排查在 m7-2、m7-4 重複。
  - 「AJAX 表單由 callback 推 dataLayer」在 m7-3、m7-4 重複。
  - 「增強型評估與自訂事件重複」在 m7-2、m7-3、m7-4 重複。
- 與其他模組重複：Meta Pixel 標準事件與廣告模組（Meta Ads）可能重疊；key event 標記與 m6-1 重複。
- 總覽頁一致性：單元卡一致；缺大綱要求的 GTM 課程連結；AI 接口條目不是 AI 任務。
- 共同案例：完成物 measurement-decision.md 裡的事件（generate_lead／trial_booking）與 M10 品牌包的 `comparison_open → booking_start → booking_complete` 不同，M10 執行包引用「M7 量測設計」會對不上。

---

## 自創碼與必要術語總表

| 頁 | 自創碼數 | 中文字數 | 每千字 | 主要自創碼 |
|---|---:|---:|---:|---|
| m6-1 | 21 | 1,932 | 10.9 | A／B／C 軌、PLATFORM VERIFIED、PENDING、ga4-setup-check.md |
| m6-2 | 0 | 1,361 | 0 | — |
| m6-3 | 3 | 1,922 | 1.6 | PENDING、M6-1 |
| m6-4 | 4 | 1,562 | 2.6 | Part 1B、D／T／S |
| m6-5 | 6 | 1,695 | 3.5 | M6-4、M7、M10-3、measurement-decision.md |
| m7-1 | 14 | 1,800 | 7.8 | CONFIG REVIEW PASS、PLATFORM VERIFIED、readiness、D／T／S |
| m7-2 | 12 | 2,003 | 6.0 | measurement-decision.md×4、PENDING、CONFIG REVIEW PASS |
| m7-3 | 15 | 1,816 | 8.3 | CONFIG REVIEW PASS×3、Part 2／3、A／C 軌 |
| m7-4 | 2 | 2,752 | 0.7 | M7-2（但 dataLayer／Consent 英文詞量最大） |

**建議改中文的自創碼**：
- 證據層級：PLATFORM VERIFIED → 平台已驗證；PENDING → 待驗證；CONFIG REVIEW PASS → 設定審查通過。
- 交接與案例：readiness → GA4 準備狀況；「課堂 trace」→ 課堂除錯紀錄。
- 練習軌：A／B／C 軌 → 自有帳號／官方示範帳號／離線案例。
- 檔名：ga4-setup-check.md、measurement-decision.md → 給中文名稱，或首次出現時說明用途、之後用中文稱呼。
- 引用：Part 1B／2／3 → 練習包的「漏斗資料」「GTM 設定草案」「繳交模板」。
- 教法標籤：D／T／S 與「老師示範／一起做」→ 改成學員可單人執行的步驟。

**應保留的必要術語**（學員要在介面輸入或辨認）：
- 事件名：page_view、purchase、generate_lead、view_item、add_to_cart、begin_checkout 等。
- 參數名：utm_*、transaction_id、value、currency、items、cta_name。
- 同意類型：analytics_storage 等四項。
- 觸發器名稱：Consent Initialization、Initialization - All Pages。
- 工具名：DebugView、Tag Assistant、Preview。
- 報表名：Traffic acquisition、Pages and screens、Report library。

**Consent default／update、key event** 是概念名詞，可改中文並在首次出現時附英文。

**介面語言**：m6-1 用中文路徑，m6-3、m6-5 與 m6-1 的 AI 輸出表用英文路徑，需統一，或兩者並列。

**提示詞開頭**：9 段 prompt 中 6 段以「請幫我」開頭，m6-3 以「請依…」、m6-1 以「我正在檢查…請把…」開頭，m6-5 以「以下是我的數據摘要」起頭後接「請幫我：」。全部不符合動詞開頭規則。
