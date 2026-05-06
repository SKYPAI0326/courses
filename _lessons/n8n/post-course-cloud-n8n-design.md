---
slug: n8n-post-course-cloud
title: 課後補充：n8n Cloud 決策 FAQ 與典型案例
kind: post-course-supplement
audience: 結業學員（已完成 9.5h 主課程、能跑 Docker self-host、會 Cloudflare Tunnel）
est_length: 單頁 HTML，正文約 1800-2400 字（lint 後 350-450 行 HTML）
format_proposal: 單頁 HTML（lesson-template-v3 套版，與 m0-cloud-vs-selfhost.html 同層 sibling，置於 courses/n8n/lessons/post-cloud-n8n.html）
depth: shallow
cross_link: [n8n-post-course-llm-copilot]
parent_course: n8n
position: post-course（結業後選讀，不在 Module 1-4 主動線、不在 m0 BONUS 內）
upstream_dependency: m0-cloud-vs-selfhost.html（決策訊號層延伸，必須讀完對比頁再讀本頁）
honesty_anchor: _outlines/n8n.md § 文案誠實度規則（三大主張禁用清單）
---

## 設計取捨記錄

### 為什麼要淺

學員不需要學第二套 n8n。他們已經會用 n8n（Docker 版），workflow 設計能力、Expression 語法、IF/Switch 邏輯這些**通用能力**已經在主課程練熟。Cloud 跟 self-host 介面 95% 一致，**重講一次節點怎麼用是雜訊**。

學員真正需要的是「**判斷訊號**」：
1. 我的業務樣態，值不值得每月付 $20-50？
2. 真的要付，要從 self-host 搬過去，會踩到什麼？
3. 有沒有「混搭」的中間解？

把這份教材做深 = 變成第二套 n8n 教學 = 學員看完更困惑。所以**深度是 FAQ + 案例，不是教學**。

### 為什麼不能重講對比頁

`m0-cloud-vs-selfhost.html` 已經做完三件事：
- 11 維度成本/能力對比表
- self-host 隱私 Layer 1 / Layer 2 分層
- 9 個學員情境決策表（CLOUD / SELF-HOST / 兩者都行 / 混搭 標籤化）

它的角色是「**對比**」（兩條路鋪開、優劣攤平），讀者立場是「我還沒選邊」。

本頁的角色是「**決策**」，讀者立場是「我已經結業、跑著 self-host、現在想知道**要不要也開個 Cloud 帳號**」。**讀者不一樣、問題不一樣、輸出不一樣**。

### 兩頁分工 elevator pitch（單句）

| 頁 | Elevator Pitch |
|----|----------------|
| `m0-cloud-vs-selfhost.html` | 課前/課中讀：兩條路客觀對比，幫你選**主路徑** |
| `post-cloud-n8n.html`（本頁） | 課後讀：你已經自架了，幫你判斷**要不要再開 Cloud** + 真要開時 5 個典型場景跟搬遷 checklist |

如果讀者搞不清楚自己該讀哪一頁，視為兩頁的失敗。本頁 hero 區第一段必須出現一句「如果你還沒決定主路徑，先去讀 m0-cloud-vs-selfhost」的 escape hatch link。

### 與 LLM Copilot 教材的弱互鎖

只有「從自架轉 Cloud 的 checklist」第 5 條提一句：
> credential 重設這步可以用 LLM 協助逐個確認 — 把 self-host 的 credential 名稱清單貼給 ChatGPT/Claude，請它對照 Cloud 端的 OAuth flow 差異列出。詳見 [LLM Copilot 教材]。

**不展開、不教 prompt、不複製 LLM Copilot 任何內容**。互鎖只是「讓有需要的學員知道有那份教材」，不是合教。

---

## 使用者決策樹

讀者進來時的心智狀態：「我有 self-host 在跑，但聽說 Cloud 也不貴，要不要試？」

用 5 題 yes/no 引導，3 分鐘內收斂出「**該試 / 不用試 / 混搭**」三類結論：

```
[Q1] 為什麼想試 Cloud？以下任一觸發都算合理動機：
     • self-host 過去 3 個月下線超過 1 次（停電、Docker 壞掉、忘了開電腦）
     • 公司 IT policy 禁裝 Docker / 終端受限、共用電腦無法 24×7 開機
     • 團隊 ≥ 3 人需要同時編輯同一份 workflow
     • 想把維運責任外包，不再自己升級 / 備份 / 監控
      ├─ 至少符合一條 → 繼續 Q2
      └─ 都不符合 → 你不需要 Cloud，self-host 對你的需求夠了。看「不適合 Cloud 的場景」確認你不在那邊。

[Q2] workflow 裡有沒有「24×7 必須準時跑」的（每天早上 7:00 寄報、每 5 分鐘 polling 監控）？
      ├─ YES → 繼續 Q3
      └─ NO  → 你不需要 Cloud，研究 cron 補跑機制 / Mac 不睡眠設定就好。

[Q3] 處理的資料有沒有「客戶 NDA / 員工 PII / 合約 / 商業戰略」？（隱私 gate — 先過這關才有計價討論意義）
      ├─ YES → 不要上 Cloud（Cloud 端 execution log 會留 prompt + payload，違反 m0 Layer 2 原則）
      └─ NO  → 繼續 Q4

[Q4] 24×7 workflow 有沒有「碰本機檔案」？（讀本機資料夾 PDF、寫本機 CSV、跟本機 Ollama 講話）
      ├─ YES → 不能整段搬。繼續 Q5 看混搭。
      │       ⚠ 提醒：self-host 下線時本機段也不能處理，Cloud 只能保住入口，不能保證全流程完成。
      └─ NO  → 強候選。繼續 Q6 看月配額。

[Q5] 能不能「拆」？把 24×7 那段切成「Cloud 觸發 → Webhook 打回 self-host 處理本機檔」？
      ├─ YES → 混搭路線（Cloud 跑 trigger + 雲端段 / self-host 跑本機段）→ 繼續 Q6 估 Cloud 端配額
      └─ NO  → 留 self-host，補可用性（UPS / 雲 VPS 自架 / 加重啟監控）

[Q6] 估算每月 Cloud 端 execution 數會不會超過 Starter 2.5K？（粗估：每天 ~80 次以內 = 安全）
      ├─ YES → Pro $50（10K）或評估 self-host 補回
      └─ NO  → Starter $20 可考慮上 Cloud（價格／配額以 n8n.io/pricing 官方頁為準，本頁數字 2026-05 採集）
```

**設計意圖**：5-6 題已經比 m0 對比頁 9 行決策表更窄，只處理「結業學員 + 已 self-host」這個切片，不重做「我該不該學 self-host」那層問題。

---

## 5 個 FAQ

### Q1. 免費版可以做完課程的 14 個 workflow 嗎？

n8n Cloud 沒有「永久免費版」，只有 14 天 trial。trial 額度官方文件數字不一致（不同版本標 1000 / 2500 不等），但**至少夠把 1-2 個 workflow 拉進來壓測**（每個 workflow 跑個 2-3 次測試 ≈ 50 次 execution）。**對應建議**：要試就在 trial 內把「最想搬上 Cloud 的 1-2 個」匯入測，14 天到期前決定要不要付費，不要 14 個全搬。

### Q2. 公司不准裝 Docker 但要做自動化？

這是 Cloud 最合理的場景：受限終端、IT policy 禁止本機跑容器、共用電腦不能 24×7 開機。**對應建議**：直接 Cloud Starter $20/月起步，本課程的 workflow JSON 大部分（不碰本機檔的那 7 個：05/06/07/08/09/12/14 + 部分變體）可直接 import。**不要硬鑽 Docker policy 例外**，跟 IT 吵 1 個月省 $240，划不來。

### Q3. Cloud 跟自架可以混用嗎？

可以而且常見。常見模式：Cloud 端跑「24×7 排程觸發 / Webhook 入口 / SaaS 串接」，self-host 跑「本機檔處理 / 本地 LLM / 大批量」。兩端用 Cloudflare Tunnel + Webhook 互打。**對應建議**：先規劃哪些步驟「必須在本機」（碰檔案、碰 Ollama），其餘上 Cloud；介面層用 Webhook + 共用 secret 認證。**不要**把同一個 workflow 拆兩半跨 Cloud/self-host 跑（debug 會很痛）。

### Q4. Cloud 資料留在歐洲 / 美國，台灣公司用合適嗎？

n8n Cloud 部署區域為 EU（預設）/ US，無亞太區。對台灣一般中小企業（行銷自動化、客戶通知、報表彙整）通常**不違法**，但有兩種情境要小心：(1) 處理「個資相關」資料前，需先盤點**法遵、合約與告知同意**（個資法 §21 賦予主管機關得限制國際傳輸的權力，遇上規範或客戶合約限制則受影響）；(2) 客戶合約有「資料境內處理」明文要求。**對應建議**：碰個資或合約綁境內 → 不上 Cloud，self-host on 台灣 NAS / VPS；單純內部營運自動化 → 通常無妨，但建議跟法遵或法務確認一次再簽年費。

### Q5. 自架 workflow 直接匯入 Cloud 會不會炸？

部分會。**會炸的節點**：Read/Write Files（本機路徑）、Execute Command（OS 指令）、本機 Webhook URL（localhost）、本地 LLM 節點（Ollama@localhost）。**會半成功**：Webhook trigger（URL 會換成 Cloud domain，需重新通知上游）、Schedule trigger（時區可能不同）。**幾乎都通**：Gmail / Sheets / Notion / HTTP Request / IF / Switch / Code 等純雲端節點。**對應建議**：搬之前先用 self-host 端的 workflow editor 做「節點普查」，把上面四類「會炸節點」標出來，預估改造成本再決定。改造率超過 30% 就重寫，不要硬搬。

### Q6. Cloud 上跑 LLM API 計費跟 self-host 有差嗎？

LLM API key 是你自己的（OpenAI / Gemini / Anthropic），帳單寄到你信箱，跟 n8n 跑哪邊**無關**。Cloud 只計算 n8n execution 數（一個 workflow 跑一次 = 1 execution），不抽 LLM token 費。**對應建議**：算總 TCO 時，Cloud 月費 + LLM API 月費要分開估；不要把 self-host「省下的 $20」直接視為淨節省，因為你的時間維運 + 電費 + 升級成本至少抵掉一半。

**註**：n8n 另有自家的 **AI Workflow Builder credits**（用 n8n 內建 AI 助理「自然語言生 workflow」才會消耗，跟你 workflow 內呼叫 OpenAI / Gemini API 是兩件事），算 TCO 時要分開看，不要跟 LLM token 費混為一談。

---

## 3 個典型案例

### 案例 A：3 人小行銷團隊 — 每天客戶 IG 留言彙整 → Notion 看板

**場景**：早 9 點自動把昨日 5 個品牌 IG 留言抓回來分類，丟到 Notion 看板給客戶查。客戶分散在三個地點、需 24×7 不關機。

**為何 Cloud 比自架合理**（引用決策樹 Q1/Q2/Q5）：
- 過去 3 個月團隊筆電真的當機過
- 24×7 排程，員工帶筆電出差不能斷
- 純雲端串接，不碰本機檔

**Workflow 草圖**：Schedule (每日 09:00) → Meta Graph API (5 brands) → Code (留言聚合 + 情緒分類) → Notion (寫看板) → Slack (通知)

**月配額預估**：每天 1 次執行 × 30 天 = 30 executions/月。**Starter $20 對單一客戶量過剩，但 Cloud 沒更便宜方案**；可把「每月配額 < 100」的**同公司內部品牌（同法人資料）**合併攤提，5 個品牌共用 = 150 executions / 月 / $20。

**風險提醒**：⚠ **不要拿來做多客戶（不同法人）共用** — n8n Starter 只有 1 個 shared project、無 RBAC，credential / execution log / workflow visibility 全部跨客戶可見，違反客戶資料邊界，即使「客戶不可知」也是違規操作。多客戶要嘛升 Pro 用 multi-project，要嘛各自獨立 Cloud 帳號。本頁不推薦多客戶共用作為攤提手段。

---

### 案例 B：個人接案者 — 客戶傳訊 → 自動產報價單草稿（混搭路線）

**場景**：個人 SOHO，客戶在 LINE / Email 描述需求，希望系統自動產出報價單草稿（PDF 存本機 + email 發回客戶確認）。本人經常出差、筆電會關機，但「報價單樣板 + 過往案例庫」在本機。

**為何 Cloud + self-host 混搭**（引用決策樹 Q3/Q4）：
- 入口（LINE webhook、Email parser）需要 24×7 在線 → Cloud
- 報價單樣板 + 案例庫在本機（保密 + 檔案大）→ self-host
- 兩段用 Webhook + Cloudflare Tunnel 互打

**Workflow 草圖**：
- **Cloud 端**：LINE Webhook → Code (parse 需求關鍵字) → HTTP Request (打 self-host Tunnel URL，附 **Bearer token 或 HMAC shared secret**) → 等回應 → LINE Reply
- **self-host 端**：Webhook (收 Cloud 觸發) → Read File (本機案例庫) → Gemini API (生草稿) → Write PDF (本機) → Gmail (寄客戶) → HTTP Response (回 Cloud)

**月配額預估**：每筆客詢 = Cloud 端 1 次 webhook execution（self-host 端不吃 Cloud quota）。每月 200 筆 = **200 executions/月** → Cloud Starter $20 + self-host 電費 $5 = 約 $25/月。**註**：若你還另設「Cloud 端完成通知 callback workflow」（self-host 跑完再打 Cloud 一次），才會接近 400 executions。

**風險提醒**：兩端同一個 workflow 跨 Cloud / self-host 跑，**debug 會比單機痛**。建議：(a) 兩端用 **Bearer token 或 HMAC shared secret** 互認（避開 JWT 簽章驗證對非工程師太硬）；(b) Cloud 打 self-host 時帶**必填欄位檢查模板**（self-host 端用 IF 節點檢查欄位齊全，缺了就 reject 並回 400，不要靜默吞）；(c) 錯誤往 Telegram / Slack 推不要回吞。

---

### 案例 C：教育工作者 — 工作坊報名表 → 自動寄資料 + 加講師行事曆（純 Cloud）

**場景**：個人講師，每月 2-3 場工作坊，學員填 Google Form 報名後自動寄歡迎信 + 課前提醒 + 加講師 Google Calendar。沒有本機檔處理需求。

**為何 Cloud 比自架合理**（引用決策樹 Q1/Q5/Q6）：
- 個人筆電不可能 24×7 開（會出國、會睡覺）
- 月 execution 數低（2-3 場 × 30 學員 × 3 通知 = ~270/月，遠低於 5K）
- 處理資料是「公開報名資訊」，無 NDA / PII 敏感性

**Workflow 草圖**：Google Form Trigger → Filter (確認付款) → Gmail (歡迎信) → Wait (課前 24h) → Gmail (提醒) → Google Calendar (建活動)

**月配額預估**：~300 executions/月，Cloud Starter $20 大幅有餘額；其實 trial 14 天就能跑完一場工作坊驗證，**不滿意可不續**。

**風險提醒**：Google API quota 跟 n8n Cloud quota 是**兩回事**，Gmail API 每日 1B quota 用不完但 OAuth 「app verification」沒做時 100 次/天上限會卡。寄信前測 send limit。

---

## 從自架轉 Cloud 的 checklist

搬之前先核對 6 條，每條給「能否自動修」「該不該搬」訊號：

1. **Credential 重設** — Cloud 不認 self-host 加密的 credential，所有 OAuth / API key 要重新走授權流程。Google 系列要重綁、Notion / Slack token 要重貼。**LLM 可協助這步**：把去敏感的 **credential 名稱與節點清單**交給 LLM，請它產出每個服務的「重授權清單 + 範圍 + 注意事項」（詳見 [n8n-post-course-llm-copilot] 教材）。

2. **節點可用性差異** — 開啟 self-host workflow 全部展開，搜尋「Read Binary File / Write Binary File / Read/Write Files / Execute Command / FTP / SSH / Local File Trigger」這幾類節點。有 → 不能搬整段，要拆混搭或重寫。

3. **檔案路徑改造** — 本機路徑（`/files/shared/...`）要全換成雲端儲存（Google Drive / S3 / Dropbox 節點）。Webhook 接收的 binary 也要改成「上傳到雲端中轉」流程。

4. **Webhook URL 變動** — self-host 端 URL 是 `https://your-tunnel.trycloudflare.com/webhook/xxx`，搬到 Cloud 變成 `https://your-instance.app.n8n.cloud/webhook/xxx`。**所有外部上游（Make 場景、Google Form 觸發、第三方平台）的 callback URL 都要改一遍**，漏改一個就沉默掉。

5. **Execution 配額預估** — 開 self-host 端的 Executions 紀錄，看過去 30 天總數。**乘 1.2（經驗值，測試 + retry buffer）；若你有頻繁 polling / 高 retry 率 / 大量手動測試，改用 1.5 更保守**。對照 Cloud plan：< 2.5K 上 Starter / 2.5K-10K 上 Pro / > 10K 評估 self-host 留下或拆混搭。

6. **時區與排程節點** — Cloud 預設 UTC，self-host 通常是課程設的 Asia/Taipei。**校對動線**：(a) 在 Cloud 介面 Workflow Settings → Timezone 改 Asia/Taipei、(b) 逐一打開所有 Schedule Trigger 與 Cron 節點、(c) 用節點下方「**next run time**」對照台灣時間驗證（不只看 cron 表達式字串，要確認下一次跑的實際時間）。**早 9 點變半夜 1 點**這種錯誤特別常見。

---

## 不適合 Cloud 的場景

至少 3 個負面案例，遵守誠實度規則：

1. **處理客戶 NDA / 員工 PII / 合約檔案** — Cloud 端 execution log 預設保留 prompt + payload，違反 m0 Layer 2 原則。要嘛 self-host + 本地 LLM，要嘛不自動化（人工處理）。
2. **每月 execution 數穩定 > 50K** — Cloud Pro $50/月 10K、再上去走 Enterprise（無公開定價、年約）。同等量級 self-host on VPS（$15-30/月）+ 你的時間維運通常更划算。
3. **核心流程依賴本地 LLM（Ollama / llama.cpp）** — Cloud 連不到你 localhost。要不換 Gemini / OpenAI（重做隱私評估），要不留 self-host。
4. **客戶合約明文要求「資料境內處理」** — n8n Cloud 部署在 EU/US，無亞太區。除非客戶接受 SCC / 資料處理協議，否則不能上。
5. **個人興趣專案、預算 = 0** — Cloud 沒永久免費，14 天 trial 後就要付。self-host on 自家筆電 $0 軟體費，興趣專案不要為它付月費。

---

## 交付形式建議

### 主推：單頁 HTML（lesson-template-v3 套版）

**理由**：
- 結業選讀，學員查閱頻率低，**不值得做多頁分章**；單頁 Ctrl+F 找答案最快
- 既有 m0-cloud-vs-selfhost.html 已是單頁長文設計，本頁與它**同層 sibling**，視覺與資訊密度一致
- HTML 比 PDF 容易維運（n8n Cloud 定價半年改一次）

### 互動決策樹？— 不建議

5-6 題 yes/no 做成 JS 互動小工具技術上 30 行 inline JS 可成，但：
- 加維運成本（n8n 改 plan 結構時要改 JS state）
- 課程體系一致性低（其他課沒有互動工具）
- Ctrl+F + ASCII 流程圖足以替代

**例外**：未來若整理出「Cloud / self-host / 混搭」三類學員實際付費路徑數據（≥30 樣本），可考慮做成 Typeform-like 互動診斷，但**這是 Phase 2，不在本次交付**。

### Cheatsheet PDF？— 不建議

PDF 會跟 HTML 真相源不同步。改採 HTML 內 `print.css` @media print 規則，學員需要時直接瀏覽器列印單頁 = PDF。

### 視覺與字型

照 `_規範/design-tokens.md` + `lesson-template-v3.html`，主題色繼承 n8n 課程綠 `--c-main: #5a7a5a`，**禁止漸層、禁止深色 mode、禁止破格**（這是課程系統，不是 web-design-engineer 產線）。lint 要過 `python3 docs/lint-page.py post-cloud-n8n.html`。

---

## 驗收標準

學員看完本頁應該能：

1. **5 分鐘內判斷自己該不該付月費** — 跑完決策樹 5-6 題，得到「該試 / 不用試 / 混搭」三類結論之一
2. **知道哪 3 種場景值得 Cloud** — 能複述案例 A/B/C 其中至少 2 個的關鍵特徵（24×7 / 不碰本機檔 / 量級可控）
3. **知道遷移時要檢查什麼** — 能背出 6 條 checklist 的至少 4 條（credential 重設、節點可用性、檔案路徑、Webhook URL、配額、時區）
4. **不會產生「Cloud 比較好 / self-host 比較好」的單向結論** — 本頁是決策工具，不是站隊宣傳

### 反向驗收（出現這些 = 失敗）

- 學員看完問「那我到底該不該付 $20」 → FAQ + 決策樹失能
- 學員把本頁拿去當「n8n Cloud 教學」 → 深度沒守住
- 學員看完發現有任何一句重複了 m0 對比頁 → 雷區踩到

---

## 製作工序建議

給後續落地的 course-designer / course-lesson-writer：

### Step 1：教案 .md（course-designer 階段）

把本提案的「決策樹 / FAQ / 案例 / checklist」按 lesson-template 結構切段：
- Hero 區：一句定位（**結業後選讀，幫你判斷要不要再開 Cloud 帳號**）+ 跟 m0 對比頁的 escape hatch
- Section 01：決策樹（ASCII 流程圖 → HTML `<pre>` 或結構化 `<ol>`）
- Section 02：5-6 個 FAQ（手風琴 details/summary 或扁平 H3 + body）
- Section 03：3 個典型案例（卡片排版，沿用 m0 的 `.scenario-list` 樣式）
- Section 04：搬遷 checklist（6 條編號清單，第 1 條附 LLM Copilot 互鎖）
- Section 05：不適合 Cloud 的場景（5 條負面 bullet）
- 結語 + nav-footer 回 index

### Step 2：HTML 排版（course-lesson-writer 階段）

- 複製 `_規範/lesson-template-v3.html`，**不要從 m0-cloud-vs-selfhost.html 複製**（避免結構汙染、避免 lint 規則漂移）
- 主題色 `--c-main: #5a7a5a`、tag 標 `補充 · POST-COURSE`
- 文字嚴守誠實度規則：禁止「Cloud 一鍵搬家」「免費版夠用」「無腦上手」
- nav-footer 連回 `index.html` + `m0-cloud-vs-selfhost.html`（不放在主動線 module1-4 navigation 裡）

### Step 3：lint + 索引更新

```bash
python3 docs/lint-page.py courses/n8n/lessons/post-cloud-n8n.html
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
```

### Step 4：登錄與密碼關卡

過 `course-register` 流程的 inject_gate.py（n8n 課程已有共用密碼，不需新生 hash），加入到 `index.html` 的「補充章節」區（與 m0-cloud-vs-selfhost.html 並列），不放主 module navigation。

### Step 5：course-reviewer 檢核要點

- 全頁有沒有重複 m0 對比頁的 11 維對比 / Layer 1/2 / Docker 細節
- 文案有沒有違反誠實度規則三大主張禁用清單
- 決策樹 5-6 題能不能在 3 分鐘讀完
- 3 個案例「為何 Cloud 合理」是否確實引用決策樹（不要憑空合理化）
- LLM Copilot 互鎖只能出現 1 次，超過 1 次 = 弱互鎖變強互鎖，不通過

---

## 設計者備註（非交付內容，給後續維運）

- 本頁壽命估約 12-18 個月。n8n Cloud 定價、plan 結構、區域可用性是**會變動**的；維運週期建議每 6 個月跑 `course-refresh` 對照官網一次
- 若未來 n8n 推出亞太區 / 永久免費版 / 改成按 user 計費，本頁需要重寫 FAQ Q1/Q4 + 案例 C 的配額估算
- 本提案不寫 cloud plan 的「節點限制」「user 數限制」「workflow 數限制」這類規格細節 — **那是 n8n.io 官方 pricing 頁的工作**，本頁職責是決策訊號，不是 spec sheet 鏡像
