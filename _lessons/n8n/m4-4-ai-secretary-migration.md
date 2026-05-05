---
slug: n8n
unit_id: m4-4-ai-secretary-migration
title: AI 秘書工作流：從 Make 遷移到 n8n
course_type: skill-operation
duration: 100 min
learning_objective: 能在 n8n 完整重建 Make 上的「AI 秘書」工作流（Gmail Trigger + Aggregate + Gemini + Router 4 路分發），並決策哪些步驟適合留 Make / 移到 n8n / 改用 local LLM
prerequisites: [m1-1-launch, m1-2-tunnel, m1-3-json, m1-3-prompt, m2-1-reference, m2-3-switch, m3-2-batch, m4-3-ai]
style_guide: _outlines/_style_guide_template.md
platform_version: n8n latest (Docker image n8nio/n8n) / Gemini 2.5 Flash / Make Cloud (對照組)
---

<!--
M4-4 是課程設計團隊系統 v2 + Codex L3 兩輪審核（CALL_ID 63c0b5f7 / 348da75a）後新增的 P0-NEW 單元。

設計目的：
  解決原本 m4-3-ai 是「假本機」場景（Webhook + Gemini API + Docs 全雲端）的問題。M4-4
  是「Make 進階使用者轉 n8n」承諾的真正兌現點：拿學員既有的 Make AI 秘書 scenario，
  在 n8n 完整 1:1 重建，並誠實展示哪些步驟資料離開本機、哪些可改用 local LLM。

定位：M4 整合實戰的最終單元，所有前面 Module 技能的綜合驗收。

教學鋪陳：
  破題：跑 Make 版 AI 秘書 → 觀察 ops 消耗 + 機密路徑（5 min）
  概念：Make ↔ n8n 對等度與 4 大邏輯落差（10 min）
  操作 Phase A：在 n8n 重建 Gmail Trigger + Aggregate + Gemini（30 min）
  操作 Phase B：JSON 解析 + Split Out + IF 4 路分發（30 min）
  操作 Phase C：4 通道輸出 + Continue On Fail（15 min）
  威脅模型 + 變體：local LLM 思路（5 min）
  檢核 + 常見錯誤（5 min）
-->

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱在 Make 上養著一條叫「02_AI 秘書 進階」的工作流——每 15 分鐘抓一次 Gmail 未讀，餵 Gemini 分析每封信的優先級和情緒，再用 4 路分發送 Telegram、Gmail、Google Docs、ntfy.sh 通知。這條已經跑了三個月，每月用掉約 2,800 ops，還在 Make Pro $9 方案的安全範圍。

直到上禮拜，雯姐丟給他一個資料夾——裡面是 60 份 NDA 合約 PDF，要求阿凱一一摘出條款編號、簽約方、有效期，整理成 Google Sheet。

阿凱第一反應是：把 Make 那條 AI 秘書改一改不就行？打開 Module 編輯器的瞬間他愣住了：**Make 沒有「讀本機資料夾 PDF」的 module**。Google Drive 也得先把那 60 份 NDA 上傳到雲端——但雯姐特別交代過：「這些是合約，不要丟到雲端硬碟。」

到這一刻為止，他面前出現一個簡單但要命的事實：

> 「我的 Make 工作流邏輯沒問題，但平台限制讓我做不下去。」

這正是這 100 分鐘的目標：把那條 AI 秘書 Make scenario 在 n8n 完整重建一次，**而且學會在哪些步驟可以選擇用 local LLM 完全脫離雲端**。重建完成後，你不只多了一份可帶走的 n8n workflow JSON，而是真的具備「把雲端 SaaS 自動化轉成本機可控資料管線」的能力。

### 概念 / Concepts

- **遷移對等度（Migration Parity）** — 兩個工具做同一件事的「功能相似度 vs 心智模型相似度」差距。Make ↔ n8n 對等度多在 65–95% 之間，**不存在 1:1 一鍵搬家**
- **資料形狀轉換（Item Shape Transformation）** — Make 的 Aggregator 把 N items 打包成 1 array；n8n 預設就是 items 流，要主動 Aggregate 才能把多 items 合併餵單一 AI 節點
- **分發式路由 vs 分支式路由** — Make 的 Router 4 路 boolean filter 是「**所有路徑都檢查、條件成立就觸發**」（分發式）；n8n 的 Switch node 是「**單值匹配走唯一一條**」（分支式）。要做 Make 那樣的多 boolean 並行觸發，n8n 要用 IF × 4 並排，不是 Switch
- **資料路徑威脅模型（Data Path Threat Model）** — 工作流每一個節點都是一次「資料離開或留下」決策。Gmail API 抓信代表資料仍在 Google；Gemini API 呼叫代表資料送到 Google Cloud inference；只有「本機 PDF 讀取 → local LLM 處理 → 本機檔案輸出」全程不離本機
- **錯誤忽略對等差異** — Make 的 `onerror: Ignore` 是模組級「視為成功繼續」；n8n 的 `Continue On Fail` 會讓節點輸出空 array 或 error 物件，後續節點要處理 undefined 形狀的可能性

### 操作示範 / Demo

#### Phase A：跑 Make 原版 + 開新 n8n workflow（5 min）

##### 步驟 A1：在 Make 跑一次原版 scenario，做兩件事觀察

打開 Make 上的「02_AI 秘書 進階」scenario：

1. 按右下角 **Run once** 跑一次完整流程
2. 在右上角 **History** 看本次執行細節
3. **觀察 1**：每個 module 後面的數字代表「該模組消耗的 ops」。記錄總 ops（一般 ≈ 5–15 ops，看抓到幾封信）
4. **觀察 2**：點開 Gmail Search 模組，看 Output 面板。**信件 fullTextBody 已經以明文形式經過 Make 的 EU/US 伺服器中轉**——就算你把 Make 帳號設定資料中心區域，信件內容也至少存在於 Make 的執行 log 裡（依保留政策 1–7 天）

**這個觀察很重要**。後面我們會比對 n8n 版本：信件從 Gmail API 直接到你電腦，不經過任何第三方伺服器中轉。

##### 步驟 A2：在 n8n 開新 workflow

n8n 主介面 → 左上角「+ Create Workflow」→ 命名為 `M4-4 AI 秘書遷移`。

進入空白編輯器。我們將依以下藍圖逐節點建構：

```
[Gmail Trigger] → [Aggregate] → [HTTP Gemini] → [Code: Parse JSON]
                                                       ↓
                              [Split Out: tasks] → [IF×4 並排路由]
                                                       ↓
              ┌──────────────┬──────────────┬──────────────┬─────────────┐
              │              │              │              │             │
        [Telegram]      [Gmail Send]   [Google Docs]    [HTTP POST]
        if to_tg=true   if to_email    if to_doc       無 filter
                        =true          =true           （與 Make 對齊）
```

11 個節點，4 路分發。Make 對應原版有同樣 11 步邏輯，但結構排列不同。

#### Phase B：Trigger + Aggregate + Gemini（30 min）

##### 步驟 B1：Gmail Trigger node

1. 點 canvas「+」→ 搜尋 `Gmail` → 選 **Gmail Trigger**
2. **Credential**：建立 `Gmail OAuth2 API`（用課程提供的 Google Cloud Console OAuth Client；若還沒有，跳到「常見錯誤 1」處理）
3. 設定面板：
   - **Event**：`Message Received`
   - **Filters → Has the words**：留空（抓全部）
   - **Filters → Read Status**：`Unread`
   - **Limit**：`5`
   - **Simplify**：**關閉**（重要！我們需要 fullTextBody）
4. 設 Schedule 觸發：右上 **Add Trigger** 旁的 settings → **Pull every** `15 minutes`

⚠️ **與 Make 差異**：Make 的 Gmail Search Module 是 Action 型（手動觸發或 Scheduler 觸發後跑一次抓 N 封）；n8n Gmail Trigger 是 **Polling Trigger**，自帶輪詢機制，不需另外加 Schedule 節點。心智模型不同。

**預期看到什麼**：點 **Execute Step**，下方 Output 面板出現 5 個 items（5 封未讀），每個 item 含 `id` / `threadId` / `subject` / `from` / `textPlain` / `textHtml` 等欄位。**注意 n8n 用 `textPlain` 不是 Make 的 `fullTextBody`**——這是文檔級的命名差異，後面 prompt 餵給 Gemini 時要對應改 expression。

##### 步驟 B2：Aggregate node（5 items → 1 array）

這一步是 Make ↔ n8n 心智模型最大落差。Make 用 BasicAggregator 把 5 items 顯式打包成 1 array 給 AI；n8n 預設不會 aggregate，AI 節點會跑 5 次（每 item 各一次）。

我們要讓 Gemini 一次看到 5 封信，做兩種寫法擇一：

**寫法 1：原生 Aggregate node**

1. 加節點 → `Aggregate`
2. 設定：
   - **Aggregate**：`All Item Data (Into a Single List)`
   - **Put Output in Field**：`array`
   - **Include**：`Selected Fields` → 填 `id, subject, from, textPlain`
3. Execute → 1 個 item 含 `array: [{id, subject, from, textPlain}, ...]`

**寫法 2：Code node（更彈性，推薦給有寫過 JS 的學員）**

1. 加節點 → `Code` → 選 **Run Once for All Items**
2. 程式碼：

```javascript
const compact = items.map(item => ({
  id: item.json.id,
  subject: item.json.subject,
  fromEmail: item.json.from?.value?.[0]?.address || item.json.from,
  fullTextBody: item.json.textPlain || item.json.snippet
}));

return [{ json: { array: compact } }];
```

⚠️ **與 Make 差異**：Make BasicAggregator 用 GUI 點選欄位，n8n 用 Code node 寫一行 `items.map`。**對非工程使用者，原生 Aggregate node 比 Code 友善**，但欄位名稱與資料形狀靠 GUI 點選會略卡。Code node 給有 JS 基礎的人最直接。

##### 步驟 B3：HTTP Request Gemini（取代 n8n 內建 Gemini node）

⚠️ **這裡我們刻意不用 n8n 內建的 Google Gemini node**，原因 Codex L3 審核也指出：要完全控制 model、response schema、safety、thinking budget，**HTTP Request 比 Gemini AI Chain 子節點更穩**。

1. 加節點 → `HTTP Request`
2. 設定：
   - **Method**：`POST`
   - **URL**：`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={{ $credentials.geminiApiKey }}`（用 credential type `Generic Auth → Custom`，存 API Key）
   - **Body Type**：`JSON`
   - **JSON Body**：（沿用 Make 原版 4 區 prompt 結構）

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "<Role>\n你現在是我的「全能數位秘書」。你的任務是分析郵件，並將結果精確地填入「四個功能分區」的 JSON 結構中。\n</Role>\n\n<Task>\n分析 <Source_Emails> 裡的每一封信，並為每封信生成以下 10 個欄位的指令：\n1. routing (開關區)：to_tg / to_email / to_doc 三個 boolean。\n2. meta (情報區)：priority 1-5 / category / sentiment。\n3. payloads (文案區)：tg_brief 30 字內 / email_report / doc_archive。\n4. action (溯源區)：source_link 拼接 https://mail.google.com/mail/u/0/#all/{id} / sender_info 格式 \\\"姓名 <信箱>\\\"。\n</Task>\n\n<Output_Rules>\n1. 僅輸出純 JSON 字符串。\n2. 嚴禁使用 ```json``` 標籤。\n3. 必須以 { 開始、} 結束。\n4. 統一使用繁體中文（台灣）。\n</Output_Rules>\n\n<Source_Emails>\n{{ JSON.stringify($json.array) }}\n</Source_Emails>"
        }
      ]
    }
  ]
}
```

3. **Response Format**：`JSON`
4. **On Error**：`Continue On Fail`（重要！對應 Make `onerror: Ignore`）

⚠️ **與 Make 差異**：Make 的 Gemini module 內建 4 區 schema 對應 UDT，n8n HTTP Request 沒有 schema 約束機制——必須在 prompt 裡用 `<Output_Rules>` 強制 LLM 遵守，並在下一步用 Code node 防禦式解析。**這是課程隱性教學重點**：n8n 給你更多控制權，代價是你要自己寫 JSON Schema 驗證或在 prompt 裡寫嚴格規則。

#### Phase C：JSON Parse + Split Out + IF 4 路（30 min）

##### 步驟 C1：Code node 解析 AI 字串包 JSON

Gemini 回應的 body 結構長這樣（路徑深）：

```
$json.candidates[0].content.parts[0].text
```

而 `text` 是個**字串**，內容才是 JSON 物件。要解析出來：

1. 加節點 → `Code` → **Run Once for All Items**
2. 程式碼：

```javascript
const raw = $input.first().json.candidates?.[0]?.content?.parts?.[0]?.text || '';

let parsed;
try {
  // 容錯：去掉可能的 ```json 包裹（雖然 prompt 已禁，但保險）
  const cleaned = raw.replace(/```json\s*/i, '').replace(/```\s*$/, '').trim();
  parsed = JSON.parse(cleaned);
} catch (e) {
  return [{ json: { tasks: [], _error: 'JSON parse failed', _raw: raw } }];
}

// 防禦：tasks 必為 array
if (!Array.isArray(parsed.tasks)) {
  return [{ json: { tasks: [], _error: 'tasks not array', _parsed: parsed } }];
}

return [{ json: parsed }];
```

⚠️ **與 Make 差異**：Make 的 JSON Parse + UDT 提供 GUI 定義 schema，欄位錯了會 onerror=Ignore 跳過；n8n 沒有對應的 friendly UI，**所有錯誤防禦都得寫進 Code node**。對非工程使用者門檻較高，但好處是完全可控。

##### 步驟 C2：Split Out node 攤開 tasks 陣列

對應 Make 的 BasicFeeder。

1. 加節點 → `Split Out`
2. 設定：
   - **Field to Split Out**：`tasks`
3. Execute → 5 個 items 出現（每個是 1 個 task 物件）

##### 步驟 C3：IF × 4 並排路由（不是 Switch！）

這一步是 Make ↔ n8n 心智模型最容易出錯處。Make 的 Router 4 路 + 各路 boolean filter 是「**4 路同時檢查、各自獨立決定是否觸發**」（一個 task 可能同時觸發 to_tg 和 to_doc）。

n8n 的 Switch node 無法做這件事——Switch 是「單值匹配走唯一一條」，會強制 task 只能進一條分支。

正確做法是 **4 個 IF 節點並排**：

1. 從 Split Out 拉 4 條線出來，分別接到 4 個 IF 節點
2. **IF #1（to_tg）**：條件 `{{ $json.routing.to_tg }}` `is equal to` `true`
3. **IF #2（to_email）**：條件 `{{ $json.routing.to_email }}` `is equal to` `true`
4. **IF #3（to_doc）**：條件 `{{ $json.routing.to_doc }}` `is equal to` `true`
5. **IF #4（HTTP ntfy）**：對應 Make 第 4 路無 filter——**直接跳過 IF**，從 Split Out 直接拉到 HTTP node

#### Phase D：4 通道輸出 + Continue On Fail（15 min）

##### 步驟 D1：Telegram Send Message

1. IF #1 的 **true** 輸出 → 加節點 `Telegram` → `Send a Text Message`
2. **Credential**：建 Telegram Bot API（用 BotFather 拿 token）
3. 設定：
   - **Chat ID**：`1062913956`（沿用 Make 原版；正式部署時改成你自己的）
   - **Text**：

```
🚨 【{{ $json.meta.category }}】 (優先度: {{ $json.meta.priority }})

📝 秘書摘要：
{{ $json.payloads.tg_brief }}

🔗 一鍵跳轉：
{{ $json.action.source_link }}
```

##### 步驟 D2：Gmail Send Email

1. IF #2 的 **true** 輸出 → 加節點 `Gmail` → `Send a Message`
2. **Credential**：沿用 Phase B 的 Gmail OAuth
3. 設定：
   - **To**：`sky8697@gmail.com`（沿用 Make 原版；正式部署時改）
   - **Subject**：`【秘書通報】{{ $json.meta.category }} - {{ $json.action.sender_info }}`
   - **Email Type**：`Text`
   - **Message**：

```
您好，我是數位秘書。
偵測到一封郵件需要您的關注：

案情摘要：
{{ $json.payloads.email_report }}

相關連結：{{ $json.action.source_link }}
```

##### 步驟 D3：Google Docs Create Document

1. IF #3 的 **true** 輸出 → 加節點 `Google Docs` → `Create a Document`
2. **Credential**：建 Google Docs OAuth（n8n credential 引導跑完）
3. 設定：
   - **Title**：`{{ $json.meta.category }}_{{ $now.toFormat('yyyyMMdd-HHmmss') }}`
   - **Folder**：選你 Google Drive 的「數位秘書」資料夾（n8n 會給你 Tree picker）
4. 加下一個節點 → `Google Docs` → `Update a Document`（n8n 中 Create 與 Update 是兩個 operation，必須串接）：
   - **Document URL**：`={{ $node["Create a Document"].json.documentId }}`
   - **Action to perform**：`Insert Text`
   - **Text**：

```
數位秘書：郵件分析歸檔報告

分析類別：{{ $('Split Out').item.json.meta.category }}
情緒偵測：{{ $('Split Out').item.json.meta.sentiment }}
處理建議：
{{ $('Split Out').item.json.payloads.doc_archive }}

原始發件人：{{ $('Split Out').item.json.action.sender_info }}
原始信件連結：{{ $('Split Out').item.json.action.source_link }}
```

⚠️ **與 Make 差異**：Make 的 Google Docs `createADocument` module 一步到位（建 + 寫入 + 設 folder），n8n 必須拆 Create + Update 兩節點。心智模型複雜度上升，但好處是中間可以插入其他處理（例如 Copy 模板再 Replace）。

##### 步驟 D4：HTTP POST ntfy.sh

1. **直接從 Split Out** 拉一條線（不經 IF #4）→ 加節點 `HTTP Request`
2. 設定：
   - **Method**：`POST`
   - **URL**：`https://ntfy.sh/workalarm_for_classtest001`（沿用 Make 原版測試 topic）
   - **Body Type**：`Raw`
   - **Body Content Type**：`text/plain`
   - **Body**：`🔴 數位秘書：緊急客訴警報！\n內容摘要：{{ $json.payloads.tg_brief }}`
   - **Send Headers**：開
   - **Headers**：`Priority` = `5`
   - **On Error**：`Continue On Fail`

⚠️ **教學重點**：對應原 Make scenario 的「教學遺漏」——第 4 路無 filter 但 body 用 `tg_brief` 跟 `routing.to_tg` 沒對齊。**這在 n8n 重建時要不要修？** 我們的決策是「**1:1 重建保留原邏輯**」，但在教案註明這是設計缺陷。讓學員自行決定要不要在實戰部署時加 filter。

##### 步驟 D5：整條工作流啟用 Error Workflow（取代 onerror Ignore）

n8n 沒有節點層級的 onerror=Ignore；最接近的等效是：

1. 對 Code node（JSON Parse） + HTTP Gemini 節點，個別設 **On Error**：`Continue On Fail`
2. 全工作流加一個 **Error Trigger** + 簡單記錄到 log file：右上角 settings → **Error Workflow** → 選一個專門記錯誤的子 workflow（這課程提供 `error-logger.json` 範本，本單元不展開）

### 變體 / 進階思路（local LLM）

**這一段不展開實作，但必講。** 若要兌現「機密資料留本機」承諾，能怎麼改？

| 步驟 | 雲端版本 | local 版本 |
|------|---------|-----------|
| Gmail Trigger | Gmail API（信件路徑：Google → 本機） | 改用 IMAP node 連自架 mail server / 或不抓 Gmail，改 watch 本機 PDF 資料夾 |
| Gemini 分析 | HTTP 打 Gemini API（信件 → Google Cloud） | 改用 Ollama / llama.cpp（HTTP 打本機 `http://localhost:11434/api/generate`） |
| Telegram 通道 | Telegram API（Telegram 伺服器） | 改 ntfy.sh self-host 或本機 webhook |
| Google Docs | Google Docs API（Google 雲） | 改寫 Markdown 到本機資料夾 |

**威脅模型決策**：
- **完全本機**：上述全部換 local 版本 → 真正零雲端，代價是 Telegram/Docs 通知不存在，要改用其他通知方式
- **去識別化雲端**：信件原文留本機跑 local LLM 摘要（去名 / 去金額 / 去公司），只把摘要送雲端 → 平衡可用性與隱私
- **全雲端**：本單元 Phase B-D 的版本 → 最方便，但對 NDA / 機密信件不適用

**選項決策表會在下一個 hands-on 中讓學員自己挑**。

### 動手 / Hands-on

跟著步驟 A1 → D5 走完，最終要有一條 11 節點的 n8n workflow 跑得通。

### 檢核 / Verification

到 n8n 介面確認以下 6 件事都成立：

- [ ] workflow 整條跑得通（按 Execute Workflow 不報錯）
- [ ] 5 封 Gmail 未讀變成 5 個 task 進 Split Out
- [ ] Telegram bot 收到至少一則「🚨」開頭訊息
- [ ] Gmail 收到至少一封「【秘書通報】」開頭通報
- [ ] Google Drive 「數位秘書」資料夾新增至少一份歸檔 Doc
- [ ] ntfy.sh 訂閱端收到至少一則 push 通知

六個全過，M4-4 完成，可以匯出 workflow JSON 帶走。

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：skill-operation

- Credential 所需：
  - Gmail OAuth2 API（同 m1-1-launch / m4-3-ai 既有 credential）
  - Gemini API Key（free tier，學員自行申請：[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)）
  - Telegram Bot API token（學員自行用 BotFather 建立）
  - Google Docs OAuth2 API（同 m4-3-docs 既有 credential）
- 試跑包提供：
  - `m4-4-ai-secretary-migration.json`（n8n workflow JSON 範本，11 節點）
  - 對應 Make 原版 scenario：學員自帶或使用 `assets/make-blueprints/02_AI秘書_進階.blueprint.json`（教學參考用，不轉檔）
- 講義頁需提供：
  - Make ↔ n8n 對等度逐節點對照表（11 列）
  - 4 個 Phase 的進度視覺化（Phase A trigger / B aggregate+AI / C parse+route / D output）
  - 威脅模型決策表（雲端 vs 去識別化 vs 全本機）
  - workflow JSON 下載連結（顯眼位置）
- 講師端準備：
  - 預先在自己 n8n 跑通整條工作流，確認 5 封信能正常分流
  - Telegram bot / Gemini API key 至少一份 demo 用 credential（避免學員卡在 credential 拿不到）
  - 備援：若 Gemini free tier 額度滿，提供 Cloudflare Workers AI 替代範例（Phase B 步驟 B3 改寫）

---

## 商業情境案例（Case）

**角色**：阿凱（27 歲，行銷專員）+ 雯姊（35 歲，工作室負責人）

**公司**：弄一下行銷工作室

**任務**：阿凱已在 Make 上養著一條 AI 秘書工作流（每月 2,800 ops），跑得很穩。但雯姊近期接了客戶 NDA 合約批次處理案，60 份 PDF 要抽條款，**禁止上傳雲端**。阿凱需要把 Make 邏輯遷移到 n8n，並且為「機密 NDA 處理」場景設計 local LLM 變體。

**本單元要他學會**：
1. 在 n8n 1:1 重建 Make AI 秘書 scenario，知道每個節點對應做法
2. 識別 Make ↔ n8n 4 大邏輯落差（資料形狀、分發 vs 分支、JSON Parse、錯誤處理）
3. 對工作流每一步做威脅模型分析，知道哪些步驟資料離開本機
4. 為「機密信件」use case 設計 local LLM 變體（不展開實作，但能說出做法）

---

## 動手練習題（Hands-on Exercise）

**題目**：

雯姊指派你做一個專屬「合約 NDA 批次處理」工作流。要求：
1. 從本機資料夾 `/n8n-shared/contracts-inbox/` 讀 60 份 PDF
2. 抽出每份的「條款編號 / 簽約方 / 有效期」
3. 整理成 Google Sheet
4. **重要**：合約原文不能上傳雲端（包括 Gemini API 都不行）

**預期成果**：

n8n workflow 截圖一張，包含：
- Read Binary Files node（從本機讀 PDF）
- HTTP Request 打**本機 Ollama** 而不是 Gemini API
- Code node 解析 JSON 結果
- Google Sheets Append node（**可以**送雲端，因為已是去識別化摘要）

不需要實際跑通——能畫出工作流結構 + 解釋每個節點為何如此選擇即可。

**完成標準**（self-check）：

- [ ] 工作流第一個節點是 Read Binary Files / Local File Trigger，不是 Google Drive
- [ ] AI 處理節點是 HTTP Request to `http://localhost:11434/api/generate`，不是 Gemini API
- [ ] 能口述：為何這個 use case 不能用 Gemini？（答：Gemini Free Tier 會用資料改善產品；NDA 不可上傳）
- [ ] 能口述：Google Sheets 那一段為何可以？（答：寫入的是去識別化欄位，不是合約原文）

---

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：Gemini API 回應 400 錯誤 `Invalid argument: contents.parts.text exceeded maximum length`
   **原因**：5 封信打包後總 tokens 太大（每封 1500-3000 tokens × 5 = 可能 15K+ tokens）；Gemini 2.5 Flash 雖然支援 1M tokens 但有 prompt 長度上限
   **解法**：在 Aggregate 後加一個 Code node 截斷每封信 fullTextBody 到 2000 字以內（取 snippet + 前 1500 字）；或改 Gmail Trigger limit 從 5 降到 3

2. **錯誤現象**：Code node 解析 JSON 報錯 `SyntaxError: Unexpected token '`' in JSON at position 0`
   **原因**：Gemini 雖然 prompt 禁了 ```json``` 包裹，但仍偶爾「不聽話」回傳 ```json{...}```；課程提供的 Code node 已加 cleaned 處理
   **解法**：檢查你的 Code node 是否完整複製了 `cleaned = raw.replace(/```json\s*/i, '').replace(/```\s*$/, '').trim()`；若仍報錯，把 `_raw` 內容貼到 ChatGPT 問「這個 JSON 哪裡壞了」做最後排查

3. **錯誤現象**：Telegram / Gmail / Docs 三條 IF 都沒觸發，但 ntfy.sh 一直在發
   **原因**：Gemini 回的 JSON 裡 `routing.to_tg` 等欄位不是 `true`/`false` 而是字串 `"true"`；IF node 比對 `is equal to true` 時嚴格比對 boolean，會 fail
   **解法**：在 prompt 加強「所有 boolean 必為 JSON 原生 true/false 不可加引號」；或在 Code node Parse 後加一行強制轉型 `parsed.tasks.forEach(t => Object.keys(t.routing).forEach(k => t.routing[k] = t.routing[k] === true || t.routing[k] === 'true'))`

---

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：Make 的 Router 4 路 + 各路 boolean filter 的「分發式」邏輯，在 n8n 中正確做法是？

- [ ] A. 用一個 Switch node，4 條 routing rule 各對應一條輸出
- [ ] B. 用一個 IF node，串接 4 個 IF in chain
- [ ] C. **4 個 IF node 並排，從 Split Out 拉 4 條線分別接，每個 IF 獨立判斷**（正確）
- [ ] D. 用 Merge node 之後 Switch

**Q2（應用驗證）**：阿凱要把 AI 秘書工作流改成處理 60 份 NDA 合約 PDF，雯姊強調「合約不能上雲」。請判斷下列每個節點的「資料路徑」是否符合需求：

| 節點 | 阿凱的設計 | 是否符合「資料留本機」？|
|------|----------|---------------------|
| Read Binary File（讀本機 PDF） | n8n 直接讀 `/n8n-shared/contracts-inbox/` | ? |
| Extract from PDF | n8n 內建 PDF parser | ? |
| HTTP 打 Gemini API 抽條款 | 雲端 LLM 分析 | ? |
| Google Sheets append（去識別化結果） | 寫摘要到 Sheet | ? |

**預期答案要點**：
- 第 1 條：✅ 符合（純本機）
- 第 2 條：✅ 符合（n8n 內建 parser 跑在本機容器）
- 第 3 條：❌ **不符合**（合約原文送 Google Cloud）→ 應改 Ollama / llama.cpp
- 第 4 條：⚠️ **看內容**——若寫入欄位是去識別化的「條款編號 / 有效期」可接受；若寫入完整條款內容仍是上雲，不可

關鍵能力：**判斷「資料離開或留下」的邊界，不是看工具，是看「送什麼資料、送去哪」**

---

## 設計師備註（給後續維護者）

- 本教案以 Codex L3 兩輪審核（CALL_ID 63c0b5f7 / 348da75a）結論為設計依據
- 與 m4-3-ai 的差異：m4-3-ai 是「Webhook + Gemini + Docs」的 happy path；M4-4 是「Make 既有 scenario → n8n 重建」對照型，含威脅模型誠實揭露
- 與其他單元前置依賴：依賴 m1-3-prompt（Prompt 設計）、m2-1-reference（多節點欄位引用）、m2-3-switch（IF/Switch 概念）、m3-2-batch（Loop / Aggregate 概念）、m4-3-ai（Gemini 整合基礎）
- 後續可能演進：M4-5 「local LLM + Ollama 整合實戰」（Phase 變體擴展為完整單元，預估 60-90 min）
- 課程文案修正連動：本單元的「威脅模型」段落是大綱 Brand Brief / index.html 三大主張修正後的對齊基準
