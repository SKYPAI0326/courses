# 研究 B：SEO／GA4／GTM／Email 與第一方數據 現行做法查證

- 查證日：2026-11-01（全部以當日 web 讀取的頁面為準）
- 範圍：M5 SEO、M6 GA4、M7 GTM、M9 Email 與第一方數據
- 判讀標記：表內「官方說法要點」只寫官方頁面讀到的內容；「意義」欄是分析推論。官方頁未寫的日期或介面位置一律標「未標示」「介面位置未證實」。
- 「來源日期」= 頁面標示的發布日或最後更新日；頁面無標示時寫「頁面未標示（2026-11-01 讀取）」。

---

## M5 SEO

| 模組 | 項目 | 對行銷人的意義（一句話） | 官方說法要點（≤40字） | 來源 URL | 來源日期 | 台灣／繁中可用性 | 介面位置是否有官方說明 |
|---|---|---|---|---|---|---|---|
| M5 | AI 摘要（AI Overviews）與 AI 模式（AI Mode）在台灣上線 | 台灣使用者的 Google 搜尋結果頁已出現 AI 回答，點擊行為會跟著改變 | AI 摘要支援地區含台灣、語言含繁體中文；只在部分搜尋出現 | https://support.google.com/websearch/answer/14901683?hl=en ；https://blog.google/products/search/ai-mode-expands-languages-locations/ ；https://technews.tw/2025/10/08/ai-mode-is-now-available-in-taiwan/ | 說明頁未標示（2026-11-01 讀取）；AI Mode 全球擴張 2025-10-07；台灣繁中 AI 模式上線報導 2025-10-08 | AI 摘要：官方說明頁列出台灣與繁中。AI 模式：Google 官方部落格只寫「35+ 語言、40+ 國家」沒列清單，台灣上線依據是台灣媒體報導 Google 的宣布 | 未提供（使用者端功能） |
| M5 | 參考數據：AI 摘要出現時點擊率下降 | 可以用來說明「排名第一不再等於拿到點擊」，但數據來自美國 | Pew：有 AI 摘要的造訪點擊傳統結果約 8%，沒有 AI 摘要時約 15% | https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/ | 2025-07-22 | 美國 900 位成人、2025 年 3 月的瀏覽資料，台灣沒有對應數據 | 不適用 |
| M5 | Google 對 AI 搜尋功能的網站主指引（含 llms.txt） | 不需要另外做「AI SEO」專用檔或標記，基本 SEO 做好就有資格出現 | 出現在 AI 摘要／AI 模式沒有額外要求；不需新增機器可讀檔、AI 文字檔或特殊標記 | https://developers.google.com/search/docs/appearance/ai-features | 2025-12-10 | 全球適用 | 有：流量算在成效報表的「網頁」搜尋類型（英文頁寫 Web search type） |
| M5 | Search Console「生成式 AI 成效報表」與「Search 生成式 AI 控制」 | 可以單獨看網站在 AI 摘要／AI 模式的曝光，也可以選擇退出，但退出就沒有這些功能帶來的流量 | 報表只有曝光、沒有點擊；控制選項有納入、排除、沿用上層，不影響排名、不影響 AI 訓練；2026-08-31 起全球可用 | https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports ；https://support.google.com/webmasters/answer/16984139 ；https://support.google.com/webmasters/answer/16908024 | 部落格 2026-06（搜尋摘要寫 06-03）；兩份說明頁都寫 2026-08-31 全球推出 | 說明頁寫「all websites worldwide」；繁中介面譯名未證實 | 有：控制在「設定 > Search generative AI」（官方英文路徑 Settings > Search generative AI）；報表只給直連網址 search.google.com/search-console/performance/search-analytics/ai，選單路徑未證實 |
| M5 | 垃圾內容政策：大規模內容濫用、網站聲譽濫用、過期網域濫用，以及核心更新節奏 | 「用 AI 大量產文衝排名」「租別人高權重網站放內容（寄生 SEO）」都明確違規；核心更新一年 2～4 次 | 不論怎麼產生，大量低價值內容都算違規；用生成式 AI 也不例外。第三方內容沒有足夠的主站監督就算聲譽濫用 | https://developers.google.com/search/docs/essentials/spam-policies ；https://developers.google.com/search/blog/2024/03/core-update-spam-policies ；https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history | 政策頁 2026-08-28；政策公告 2024-03-05；狀態頁列出 2024-03、08、11、12，2025-03、06、12，2026-03、05 共 9 次核心更新 | 全球適用 | 不適用 |
| M5 | 結構化資料：常見問題（FAQ）與操作說明（HowTo）複合式結果停用 | FAQPage 標記已經不會產生搜尋結果的展開問答，不要再當成點擊率技巧教 | FAQ 複合式結果 2026-05-07 起不再出現在搜尋結果，說明文件 2026-06-15 移除；HowTo 2023 年已縮減並淘汰 | https://developers.google.com/search/docs/appearance/structured-data/faqpage ；https://developers.google.com/search/blog/2023/08/howto-faq-changes | FAQ 異動紀錄 2026-05-08／2026-06-15；HowTo 公告 2023-08-08（2023-09-14 更新） | 全球適用 | 不適用 |
| M5 | INP 取代 FID 成為核心網頁體驗指標 | 頁面速度檢查要看「互動到下一次繪製」，FID 已退場 | 2024-03-12 起 INP 取代 FID；良好 ≤200ms，不佳 >500ms，用實際使用者資料的第 75 百分位計算 | https://web.dev/blog/inp-cwv-march-12 ；https://web.dev/articles/inp | 2024-03-12；INP 說明頁 2025-09-02 更新 | 全球適用 | 不適用（PageSpeed Insights／Search Console 的報表位置本次未查） |

## M6 GA4

| 模組 | 項目 | 對行銷人的意義（一句話） | 官方說法要點（≤40字） | 來源 URL | 來源日期 | 台灣／繁中可用性 | 介面位置是否有官方說明 |
|---|---|---|---|---|---|---|---|
| M6 | 「轉換」改名為「關鍵事件」（key events） | GA4 裡要說「關鍵事件」，「轉換」只留給 Google Ads 用 | 關鍵事件是 GA 的概念；可以從關鍵事件建立 Google Ads 轉換，但 Ads 轉換不會出現在 GA 標準報表 | https://support.google.com/analytics/answer/13128484?hl=en | 頁面未標示（2026-11-01 讀取）；官方頁沒寫改名日期 | 繁中介面的確切譯名未證實（見未證實清單） | 有：管理 > 資料顯示 > 事件，按星號標記（英文路徑 Admin > Data display > Events） |
| M6 | GA4 內建 AI：Ask Advisor（Gemini）與首頁「產生的洞察」 | 可以用對話方式問數據，但目前繁中介面的資源用不到 | Ask Advisor 用 Gemini 分析資源資料，可能出錯；目前只限介面語言為英文的資源 | https://support.google.com/analytics/answer/16675569?hl=en ；https://support.google.com/analytics/answer/9164320?hl=en | 新功能頁：Generated insights 2026-02-10；Ask Advisor 說明頁未標示 | Ask Advisor：只限英文介面。產生的洞察：官方沒寫語言限制，繁中可用性未證實 | 有：資源右上角 Ask Advisor 圖示，或搜尋框；產生的洞察在首頁 |
| M6 | 歸因模型與跨通路功能現況 | 教歸因只需要教「資料驅動」和「最後點擊」，另加 2026 年的轉換歸因分析（Beta） | 首次點擊、線性、時間衰減、根據位置 2023 年移除，剩資料驅動、最後點擊、外部歸因 | https://support.google.com/google-ads/answer/13427716 ；https://support.google.com/analytics/answer/9164320?hl=en | 移除公告 2023-04-06；轉換歸因分析與跨通路預算（Beta）2026-01-16 | Beta 功能官方寫「可能不適用於您的資源」 | 部分有：轉換歸因分析在「廣告」工作區；跨通路預算位置未證實 |
| M6 | 同意模式與行為建模 | 使用者拒絕 Cookie 後，GA4 報表數字可能含模型推估，要會判讀 | 需每天 ≥1,000 筆拒絕事件且持續 ≥7 天；模型資料不進 BigQuery 匯出、目標對象、區隔 | https://support.google.com/analytics/answer/11161109?hl=en | 頁面未標示（2026-11-01 讀取） | 全球適用；小流量網站多半達不到門檻（推論） | 有：管理 > 資料顯示 > 報表識別資訊 > 混合（英文 Admin > Data display > Reporting identity > Blended） |
| M6 | 資料保留期與 BigQuery 匯出限制 | 「保留 2 個月」只影響探索報表，標準報表不受影響；要長期分析原始資料就用 BigQuery | 保留設定只影響探索與漏斗報表；標準資源每日批次匯出上限 100 萬事件，串流匯出無上限但另計費 | https://support.google.com/analytics/answer/7667196?hl=en ；https://support.google.com/analytics/answer/9358801 | 頁面未標示（2026-11-01 讀取） | 全球適用 | 有：管理 > 資料設定 > 資料保留（英文 Admin > Data Settings > Data Retention） |
| M6 | 新的「AI Assistant」預設管道群組，加上 ChatGPT 的 UTM | ChatGPT／Gemini／Claude 帶來的流量現在有獨立管道，可以直接回答「AI 搜尋帶來多少流量」 | 2026-05-13 起預設管道群組多了 AI Assistant，medium 是 ai-assistant；OpenAI 說明中心寫 ChatGPT 會加上 utm_source=chatgpt.com | https://support.google.com/analytics/answer/9164320?hl=en ；https://help.openai.com/en/articles/12627856-publishers-and-developers-faq | GA4 2026-05-13；OpenAI 頁面日期未取得 | GA4 全球；OpenAI 頁面這次 WebFetch 回傳 403，UTM 說法來自搜尋結果顯示的官方頁摘錄 | 有：在預設管道群組報表裡；細部路徑未證實 |

## M7 GTM

| 模組 | 項目 | 對行銷人的意義（一句話） | 官方說法要點（≤40字） | 來源 URL | 來源日期 | 台灣／繁中可用性 | 介面位置是否有官方說明 |
|---|---|---|---|---|---|---|---|
| M7 | Consent Mode v2：四個主要參數、基本與進階模式、適用地區 | v2 多了 ad_user_data、ad_personalization；歐洲流量是強制，台灣網站是選配，但會影響模型推估 | 基本模式在同意前完全不載入代碼；進階模式先載入、送無 Cookie 訊號供建模。EU 政策涵蓋 EEA、英國、瑞士 | https://developers.google.com/tag-platform/security/concepts/consent-mode ；https://support.google.com/google-ads/answer/16724512?hl=en | 開發者頁 2026-07-30；政策頁未標示 | 依 Google 政策頁，強制要求只列 EEA／英國／瑞士；台灣不在列舉中（台灣法規是否要求取得 Cookie 同意，本次沒有查證） | 未證實（GTM 同意設定的選單路徑本次沒有查到官方文字） |
| M7 | Google tag gateway for advertisers（原名第一方模式） | 用自家網域載入 Google 代碼、傳送衡量資料，減少被阻擋造成的資料流失；只對 Google 代碼有效 | 用自家 CDN、負載平衡器或網頁伺服器部署 Google 代碼；官方建議和伺服器端代碼一起做 | https://developers.google.com/tag-platform/tag-manager/gateway ；https://support.google.com/tagmanager/answer/4620708?hl=en | 2025-05-08 改名並全面開放；Cloudflare 2025-03 Beta；Akamai 2026-01-29；GCP 正式版 2026-06-01；CloudFront 2026-06-03 | 全球；需要自有網域和 CDN 或雲端 | 部分有：版本資訊寫可在 GTM 與 Google 代碼設定中引導設定；確切選單路徑未證實 |
| M7 | 伺服器端代碼（server-side tagging） | 資料先送到自己控制的伺服器，再決定要轉給誰；需要雲端主機與維運成本 | 在自己的 GCP 專案或其他環境執行；伺服器容器和網頁容器用一樣的代碼、觸發條件、變數 | https://developers.google.com/tag-platform/tag-manager/server-side/intro ；https://support.google.com/tagmanager/answer/4620708?hl=en | 2026-07-30；2026-05-01、2026-06-22 有改善 Ads 轉換衡量的更新 | 全球 | 未提供費用說明；設定指南有 Cloud Run 連結 |
| M7 | Google 代碼與 GTM 的關係變動 | GTM 裡 Google Ads／Floodlight 會自動先載入 Google 代碼；2026-10 起 gtag config 會進入 dataLayer，萬用自訂事件觸發條件可能誤觸發 | 2025-04-10 起自動載入完整 Google 代碼設定；2026-10-08 起 config 以 gtag.config 事件出現；2026-10-12 起可用 destination 代碼直送 | https://support.google.com/tagmanager/answer/4620708?hl=en | 2025-03-10（2025-04-10 生效）；2026-07-09；2026-10-08；2026-10-12 | 全球 | 版本資訊未寫選單路徑 |
| M7 | Meta 轉換 API（CAPI）、去重、CAPI Gateway | Pixel 搭配伺服器端 CAPI 送同樣的事件是 Meta 的建議做法，事件 ID 要一致才不會重複計算 | 建議 Pixel 與 CAPI 送同樣的事件；eventID 對 event_id、事件名稱也要一致，48 小時內去重；Gateway 把 Pixel 事件轉送到 CAPI | https://developers.facebook.com/docs/marketing-api/conversions-api/best-practices ；https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events ；https://developers.facebook.com/docs/marketing-api/gateway-products | 頁面未標示（2026-11-01 讀取） | 全球 | 部分有：官方寫可在事件管理工具一鍵為 Pixel 設定 CAPI；Gateway 管理介面在 /hub/；事件管理工具內的選單路徑未證實 |

## M9 Email 與第一方數據

| 模組 | 項目 | 對行銷人的意義（一句話） | 官方說法要點（≤40字） | 來源 URL | 來源日期 | 台灣／繁中可用性 | 介面位置是否有官方說明 |
|---|---|---|---|---|---|---|---|
| M9 | Gmail 寄件者規範（含 RFC 8058 一鍵退訂）與 2025-11 加強執法 | 每天寄 Gmail 約 5,000 封以上就要 SPF＋DKIM＋DMARC＋一鍵退訂，否則可能被暫時或永久退信 | 大量寄件者需 SPF 與 DKIM、DMARC（可 p=none）、網域對齊、一鍵退訂；垃圾郵件率要低於 0.3%，建議低於 0.1% | https://support.google.com/a/answer/81126?hl=en ；https://support.google.com/a/answer/14229414?hl=en ；https://www.rfc-editor.org/rfc/rfc8058 | 2024-02-01 生效；一鍵退訂 2024-06-01；2025-11 加強執法；RFC 8058 是 2017-01 | 寄到 Gmail 就適用，跟寄件者在哪個國家無關 | 不適用（DNS 與寄信平台設定）；退信原因可在 Postmaster Tools 查看 |
| M9 | Yahoo 與 Microsoft Outlook 寄件者規範 | 三大信箱商的門檻已經一致，教 Email 一定要先教寄件網域驗證 | Yahoo：大量寄件需 SPF＋DKIM＋DMARC、一鍵退訂、2 天內處理退訂。Outlook：每天 >5,000 封要完整符合 SPF／DKIM／DMARC | https://senders.yahooinc.com/best-practices/ ；https://substrate.office.com/ip-domain-management-snds/Postmaster/Policies | Yahoo 2024-02 起執行；Microsoft 2025-05-05 生效 | 全球 | 不適用；Outlook 不合規先進垃圾郵件匣，問題持續就以 550 5.7.515 退信 |
| M9 | Apple 郵件隱私權保護（MPP）讓開信率失真 | Apple Mail 使用者的開信會被灌水，開信率不能當主要成效指標，要改看點擊與轉換 | 「保護郵件活動」預設在背景下載遠端內容，並用兩層轉送隱藏 IP，讓寄件者無法得知郵件活動 | https://www.apple.com/legal/privacy/data/en/mail-privacy-protection/ | 頁面未標示（2026-11-01 讀取） | 台灣 iPhone／Mac 使用者適用；台灣 Apple Mail 使用比例本次沒有查證 | 有：iOS 設定 > App > 郵件 > 隱私權保護（英文 Settings > Apps > Mail > Privacy Protection） |
| M9 | Chrome 第三方 Cookie 不淘汰，Privacy Sandbox 主要 API 退場 | 「Chrome 即將淘汰 Cookie」已經不成立；Topics、Protected Audience、Attribution Reporting 不用再教 | 2025-04 宣布維持現行 Cookie 選擇、不推出獨立提示；2025-10-17 宣布因採用率低，淘汰 Topics 等 API；CHIPS、FedCM 保留 | https://privacysandbox.google.com/blog/privacy-sandbox-next-steps ；https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies | 2025-04-22；2025-10-17 | 全球 | 使用者端：Chrome「隱私權和安全性」設定（官方英文 Privacy and Security Settings） |
| M9 | 台灣個人資料保護法 2025 修正：個資會、事故通報、個資保護長 | 修法已公布但還沒施行；可以教方向（設個資會、事故要通報），不能說「已經上路」 | 114-11-11 修正公布；主管機關改為個資會（§1-1）、事故通報（§12）、個資保護長（§18）；施行日由行政院定 | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021 | 修正日期 2025-11-11（114 年）；資料庫標示「部分或全部條文尚未生效」 | 台灣法規 | 不適用 |
| M9 | LINE 官方帳號 2026-11-01 調價 | 今天起中、高用量月費各漲 200 元；課程裡的方案價格要更新 | 中用量 800→1,000 元、高用量 1,200→1,400 元（未稅），免費則數 200／3,000／6,000 不變；高用量加購採階梯計價 | https://tw.linebiz.com/column/LINEOA-2026-Price-Plan/ ；https://tw.linebiz.com/service/account-solutions/line-official-account/ | 公告 2026-09-01；生效 2026-11-01 | 台灣專屬 | 未證實（公告只寫要在 10/27 前改方案，沒寫後台選單路徑） |

---

## 未證實／查不到（不寫進建議）

1. **llms.txt：Google 人員的口頭說法**：Mueller 說「purely speculative」（SEJ，2026）、「no AI system currently uses llms.txt」（Bluesky，2025-06）；Illyes 說「Google 不支援也沒有計畫支援」只有一篇二手來源。可以寫進教材的只有官方頁面那句「不需要 AI 文字檔」（見 M5）。
2. **AI 模式在台灣的上線日**：2025-10-08 這個日期來自台灣媒體報導（technews 等）；Google 官方部落格的擴張文章沒有列出語言清單。Google 台灣官方部落格原文本次沒有開啟。
3. **AI 摘要廣告在台灣是否上線**：只查到美國上線、之後擴大到 12 國的二手報導，國家清單未證實。
4. **GA4 繁中介面的「key events」譯名**：官方英文頁用 key events；繁中介面實際字樣（例如「關鍵事件」或「重要事件」）本次沒有開繁中說明頁核對。教材用詞要先實機確認。
5. **GA4「產生的洞察」與 Ask Advisor 在繁中介面能否使用**：Ask Advisor 官方寫只限英文；產生的洞察沒有寫語言限制。
6. **跨通路預算（Beta）在 GA4 的介面位置**：新功能頁沒寫。
7. **AI 搜尋占全站流量的比例**：Ahrefs「2026-03 AI 聊天機器人約占 0.28%」、Similarweb「ChatGPT 占生成式 AI 流量 52.7%」都只讀到二手轉述，原始報告沒有開啟。
8. **Google tag gateway「轉換提升 14%」**：廠商轉述的 Google 內部數據；官方頁只寫「drive conversion uplift」，沒有數字。
9. **Consent Mode 在瑞士的執行嚴格度**：二手來源說法互相矛盾。官方只寫 EU 使用者同意政策涵蓋 EEA、英國、瑞士。
10. **台灣法規是否要求網站在使用 Cookie 前取得同意**：本次沒有查證，不能說 Consent Mode 在台灣是法遵義務。
11. **個資會的實際成立日與修正條文施行日**：法規資料庫顯示「尚未生效、施行日未定」。行政院是否已經訂出施行日，本次沒有查到。
12. **Microsoft 要求 DMARC 至少 p=none**：只有二手來源；官方頁只寫要「完整符合 SPF、DKIM、DMARC」。
13. **Search Console Insights 是否已經不需要連結 GA**：只有二手時間線，官方說法本次沒有查證。
14. **LINE OA PLUS 的內容**：公告提到中、高用量會「免費升級 OA PLUS」，具體功能本次沒有查。
15. **2026-05 之後是否還有核心更新**：Search Status Dashboard（2026-11-01 讀取）列到 2026-05 核心更新，之後只有 2026-06、08、09 三次垃圾內容更新。只能說「截至讀取日」。
16. **Safari ITP／Firefox 追蹤保護的現況**：沒有查，所以不能用來支撐「Cookie 後時代」的說法。

## 與課程現有說法可能衝突的地方

> 以下根據任務給的課程說法舉例比對；課程頁面原文本次沒有讀。

| 課程現有說法（舉例） | 可能的衝突 | 依據 | 建議方向（分析推論） |
|---|---|---|---|
| 把開信率當成效指標 | Apple MPP 預設在背景下載遠端內容，Apple Mail 使用者的開信會被灌水 | Apple MPP 隱私頁 | 開信率降為輔助的寄送健康度訊號；主要指標改成點擊率、轉換與退訂／檢舉率（Gmail 垃圾郵件率 <0.3%） |
| 「Cookie 後時代」「Chrome 將淘汰第三方 Cookie」 | Chrome 2025-04 已宣布不淘汰；Topics／Protected Audience／Attribution Reporting 2025-10-17 宣布退場 | Privacy Sandbox 官方部落格兩篇 | 改成「同意管理＋第一方數據＋伺服器端衡量」的框架，不要用 Chrome 淘汰時程當理由；Privacy Sandbox API 不要再當替代方案教 |
| 用 FAQ 結構化資料爭取搜尋版位 | FAQ 複合式結果 2026-05-07 起已不顯示；HowTo 更早就淘汰 | FAQPage 文件異動紀錄、2023 部落格 | 頁面上的 FAQ 內容可以留（內容層面），但不要宣稱標記能帶來展開版位；結構化資料改教仍有效的類型（類型清單本次沒有逐項查證） |
| GA4 用「關鍵事件」一詞 | 方向正確；但 Google Ads 仍叫「轉換」，兩者不能混用 | GA 說明 13128484 | 保留「關鍵事件」，補一句「匯入 Google Ads 後才叫轉換」；繁中介面字樣要先實機確認（未證實第 4 項） |
| 若課程仍教 FID 或「首次輸入延遲」 | 2024-03-12 起已由 INP 取代 | web.dev | 換成 INP 與門檻 200ms／500ms |
| 若課程仍教首次點擊、線性、時間衰減、根據位置歸因 | 2023 年已從 GA4 與 Google Ads 移除 | Google Ads 說明 13427716 | 只教資料驅動與最後點擊；進階可以提 2026 轉換歸因分析（Beta） |
| 若課程建議建立 llms.txt 或「AI 專用標記」來上 AI 摘要 | Google 官方：不需要 AI 文字檔或特殊標記 | AI features 頁（2025-12-10） | 改教可抓取、可索引、內部連結與內容品質；成效用 Search Console 生成式 AI 報表看 |
| 若課程用 AI 大量產文做 SEO 練習 | 大量低價值內容不論怎麼產生都算大規模內容濫用 | 垃圾內容政策頁（2026-08-28） | 練習要加上「人工加值、原創資訊」的檢查點 |
| 若課程說 GA4 資料保留設成 2 個月會讓報表只剩 2 個月 | 保留設定只影響探索與漏斗報表 | GA 說明 7667196 | 修正說明，長期原始資料改用 BigQuery（標準資源每日 100 萬事件上限） |
| 若課程寫 LINE 官方帳號中用量 800、高用量 1,200 元 | 2026-11-01 起改為 1,000／1,400 元（未稅） | LINE Biz 官方公告 | 更新價格並註明生效日 |
| 若課程說個資法已經要求企業通報事故、或個資會已經成立 | 2025-11-11 修正已公布，但法規資料庫顯示尚未生效 | 全國法規資料庫 | 寫成「已修法公布、施行日由行政院訂定」，教材上線前再查一次 |
| 若課程說 Consent Mode 是所有網站的法定義務 | Google 政策強制範圍是 EEA、英國、瑞士；台灣法規要求本次沒有查證 | Google Ads 政策頁 16724512 | 寫成「歐洲流量必須做；台灣網站建議做，用來建模與準備未來法規」，法律部分不要下定論 |
