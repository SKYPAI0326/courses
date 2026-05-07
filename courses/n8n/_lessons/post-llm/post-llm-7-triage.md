---
unit_id: post-llm-7-triage
title: 錯誤分流 — 從訊息字串到復原動線
course: n8n / AI 資料工廠
chapter: 第 7 章 / 8（post-llm 系列：課後用 LLM 改 workflow）
description: LLM 給的 workflow 匯不進去？3 類錯誤分流 SOP + 各自復原動線
audience: 商業培訓非工程師、課後用網頁版 LLM（ChatGPT / Claude / Gemini）改 workflow
prerequisite: 已跑過 Lite Pack 14 個 workflow 至少 1 次；理解 #02 PDF AI 改名範例
delivery: 文字導向 HTML 章節（無印風）
created: 2026-05-07
codex_audit: 6ffbb482
codex_verdict: actionable（已修補）
last_updated: 2026-05-07
---

# 錯誤分流 — 從訊息字串到復原動線

> **本章重設計教案** · 對應 `courses/n8n/lessons/post-llm-7-triage.html`

## 重設計內容

## 第 7 章重設計：錯誤分流 — 從訊息字串到復原動線

### 7.0 開始錯誤分流前 — 30 秒環境檢查（cross-link 第 8 章）

拿到「LLM 給的 workflow 匯不進去 / 跑出錯」之前，**先做 30 秒環境檢查**（詳細在第 8 章 8.X 表）。如果環境本身就錯（在 production 動 / Active 開著被 trigger / 在 Cloud 但用 Cloud 不支援的節點），錯誤分流會帶你走錯方向、修也修不對：

- ✅ 我在 `*-edit` workflow（不是 production）
- ✅ Active 是 OFF（手動跑而非 trigger 自動跑）
- ✅ 在 local n8n（如果 LLM 給的有 executeCommand / readWriteFile 等 cloud 不支援節點）

30 秒檢查全綠才進下面的錯誤分流。

### 1. 學員此時的痛點

學員到第 7 章 100% 是「卡關狀態」進來的。心理：

- **匯入跳紅字了**（n8n UI 跳「Could not parse」一類視窗）
- **匯入過了但跑紅燈了**
- **跑綠燈但結果不對（檔名 null、寄錯人）**
- **我和 LLM 已經來回 5 輪了還沒解，是不是該放棄**

最不需要的是：又一個流程理論。最需要的是：「我看到這個訊息字串 = 我立刻知道下一步打開哪個東西」。

### 2. 核心要傳遞的 1 個觀念

**錯誤訊息是 grep key。看到字串對到類別 → 跑 5 步 checklist → 沒解就走逃生口（社群求救），不要硬磕。**

### 3. 具體 step-by-step

#### 入口：30 秒分流動線

1. **找錯誤訊息所在位置**
   - 匯入失敗：n8n UI 中央的對話框 / 視窗
   - 跑紅燈：紅色框框節點下方的紅字
   - 跑綠燈但結果錯：肉眼比對 input/output（這類沒有「訊息字串」，看樣態 1-3）
2. **複製訊息全文**（Cmd+C）
3. **對照分流表**（30 秒）：
   - 字串含 `parse` / `JSON` / `Unexpected token` / `node type not found` / `unknown parameter` / `connections` → **類別 1**
   - 字串含 `Credential` / `401` / `403` / `invalid_grant` / `invalid_client` / `token expired` / `API key` / `OAuth` → **類別 2**
   - 沒有訊息或全綠燈但結果錯 → **類別 3**
4. **跳到對應 checklist**

#### 類別 1：JSON / workflow 格式錯（n8n 進不去）

**典型訊息字串樣本**：
- `Error parsing workflow: Unexpected token < in JSON at position 0`
- `Could not import workflow: Invalid format`
- `node type not found: n8n-nodes-base.googleSheets`
- `unknown parameter "options" for node "Code"`

**小心：類別 1 vs 第 8 章 Cloud 限制的訊號差異**

`unknown parameter` / `node type not found` 容易和「節點本身是 Cloud 不支援的本地節點」混淆。動修法前 30 秒分辨：

| 訊號 | 類別 1（n8n 版本 / 節點欄位差） | 第 8 章 Cloud 限制（節點根本不可用） |
|------|--------------------------------|--------------------------------|
| 錯誤訊息 | `unknown parameter X` / `parameter Y is required` | `Node type 'n8n-nodes-base.executeCommand' is not available` |
| n8n UI 反應 | 節點顯示，但設定面板有黃色驚嘆號 | 節點變灰且不能 add，搜尋找不到 |
| 通常解法 | 改 typeVersion / 補欄位 / 走類別 1 動線 | 走第 8 章「local 才能跑」評估 → 換節點或留 local |

**5 步 checklist**（依序跑，前一步沒解才跑下一步）：

1. **檢查是不是「整份覆蓋」而非「在 UI 替換節點」**
   - 動作：你貼到 n8n UI 的內容，是直接覆蓋 workflow.json 檔，還是用 n8n UI 的「右鍵 Paste 節點」貼？
   - 復原：用 n8n UI 的「右鍵 Paste 節點」貼，不要直接覆蓋整份檔案
2. **檢查 markdown code fence**
   - 動作：你從 LLM 複製 JSON 時，開頭有沒有 ` ```json ` 三個反引號？
   - 復原：把開頭的 ` ```json ` 和結尾的 ` ``` ` 拿掉，只保留 `{` 開頭的純內容
3. **檢查 typeVersion 是不是 LLM 編的**（**僅在你動了整份 JSON 時才需要**）
   - 動作：打開你**自己之前 export 的同一份 #02 .json 檔**（不是「同類」workflow），用 VS Code 搜尋同名 node type（例：`"type": "n8n-nodes-base.code"`），抄它的 typeVersion 數字
   - 復原：把抄到的數字回填 LLM 給你的 JSON
4. **用 jsonlint.com 找壞行**
   - 動作：複製 LLM 給的 JSON 整段 → 貼到 https://jsonlint.com → 點 Validate
   - 復原：jsonlint 會標哪一行有逗號 / 引號錯，把那行貼給 LLM 用模板 4 修（不重寫整份）
5. **節點 deprecation**
   - 動作：訊息含 `node type not found` 時，跑紅線 4 的 4 順位 fallback（google → n8n UI 搜尋 → 課程社群 → 不直接信 LLM）

**驗收硬指標**：跑完任一步後，重新匯入 / 重新替換節點 → 5 個節點全顯示且不變灰

#### 類別 2：credential 錯（認證掉了）

**典型訊息字串樣本**：
- `Credential not found`
- `401 Unauthorized — Invalid or expired token`
- `403 Forbidden`
- `invalid_grant: Token has been expired or revoked`

**5 步 checklist**：

1. **緊急優先：你是不是不小心把含 credential 的 JSON 貼出去過？**
   - 動作（這條最急，先做）：
     - **Google credential**：打開 https://myaccount.google.com/permissions → 找到 n8n 那個 entry → Remove
     - **Notion credential**：打開 https://www.notion.so/profile/integrations → 找到你給 n8n 的 integration → Regenerate token
     - **OpenAI credential**：打開 https://platform.openai.com/api-keys → 找到該 key → Revoke
     - **其他服務**：google「服務名 + revoke API key」
   - 重發新 token → 回 n8n credentials 設定頁 → 該 credential 條目用新值更新
2. **n8n UI 上節點 credential 欄變空白**
   - 動作：點該節點 → 右側 panel 找 Credential 那欄（通常在 Settings tab 旁邊有獨立 Credential tab，看版本）→ 點下拉選你之前建好的 credential
   - 驗收：欄位顯示綠色勾勾或 credential 名稱（不是空白）
3. **每個有問題節點重選一次（即使顯示是對的）**
   - 動作：點下拉 → 選同一個 → Save。讓 n8n 重新 bind credential reference
4. **self-host 額外檢查 OAuth callback URL**
   - 動作：n8n self-host 要在每個 OAuth credential 設定裡填 callback URL（例：`https://your-domain.com/rest/oauth2-credential/callback`）
   - 復原：去 n8n credential 設定 / OAuth 服務 console，兩邊 callback URL 對齊
5. **Cloud 用戶：self-host 加密的 credential 不能直接搬**
   - 動作：Cloud 上要重新建 credential，不能匯入 self-host 加密過的

**驗收硬指標**：節點上 credential 欄顯示綠色 + 重跑該節點不再 401/403

#### 類別 3：邏輯錯（最難，最常見）

匯入過、credential 對，但結果不對。3 種樣態：

**樣態 1：紅燈卡在中段節點**
- 訊息常見：`Cannot read property 'X' of undefined` / `Item is empty` / `[Object object] is not iterable`
- 意思：某節點試圖讀一個不存在的欄位

**樣態 2：全綠燈但資料量縮水**
- 200 筆 input 變 50 筆 output → filter 條件錯 / 迴圈邏輯錯 / 上游 split 錯

**樣態 3：全綠燈但寄錯/存錯**
- 寄信寄到錯收件人 / 檔案存到錯資料夾 / 欄位對應顛倒

**5 步 checklist**：

1. **用 output panel 比對 dot path**
   - 動作：點紅燈節點 → 右側 panel 切到「Input」 tab → 看 input 進來時的 JSON 結構
   - **怎麼讀 JSON 樹**：
     - 找你以為 LLM 引用的欄位（例：`customer.email`）
     - 在 input panel 上，看是不是真的有 `customer` 這個 key + 它底下有 `email`
     - 如果 input 裡實際是 `contact.mail`（不是 `customer.email`），就是 LLM 假設錯
2. **用「optional chaining」躲開不存在欄位**
   - 動作：把 expression `{{ $json.customer.email }}` 改成 `{{ $json.customer?.email }}`（在 `customer` 後面加一個小問號）
   - 翻譯：問號的意思是「如果 customer 這欄不存在，整個 expression 就回 `undefined` 不要炸紅燈」
   - 復原：在 n8n 任何欄位裡看到 `{{ $json.X.Y }}` 都可以加問號變 `{{ $json.X?.Y }}`
3. **檢查上游節點是不是換了**
   - 動作：你最近換過 trigger（例：Manual → Google Drive Trigger）？換 trigger 後**所有下游節點引用的欄位路徑都要重接**
   - 復原：在 n8n UI 上每個下游節點的 expression 欄位，hover 上去看「左側是哪個 trigger 出來的欄位」 → 重新從新 trigger 的 output 拖
4. **用模板 4 精準回報（不貼整份）**
   - 動作：只貼紅燈節點 + 上一節點 output + 紅燈訊息 三件套
5. **如果 LLM 修法看起來要動 5 個以上欄位 → 退步驟 1**
   - 動作：回頭看 4 格便箋，是不是 input 那格寫太模糊。需求重拆

**進階：optional chaining 只是止血，根因不會自己消失**

在 Code 節點加 `?.` 讓 workflow 不再炸紅燈，但**輸出可能是錯的或缺的**（例如 `aiResponse?.category` 在 LLM 沒回 category 時變 undefined，下游 Sheet 寫入會出現空欄）。三步根因動線：

1. **看 input panel** — 是什麼讓欄位 missing？（LLM 回應結構變、prompt 改了沒同步、PDF 解析空白）
2. **回到第 3 章模板 5 追問 LLM** — 「我的 prompt 對 X 種 input 應回 Y 結構，但實際回了 Z（貼 sample），請問是 prompt 缺什麼還是 input 本身就無法生 Y？」
3. **決定該補 fallback 還是該修 prompt** — 如果某類 input 真的拿不到 Y（例如圖片化 PDF 抽不到文字），就在 Code 節點補 `|| '未分類'` 之類 fallback；如果只是 prompt 沒寫清楚就回去改 prompt。

把「optional chaining 是止血不是根治」記住 — 跑完不炸不等於跑對。

**樣態 2 額外檢查**：
- 在每個節點右側 panel 看「Items」數量（顯示 1 of 200 或類似）→ 在哪個節點 200 變 50？那個節點的 filter 條件就是錯的

**樣態 3 額外檢查**：
- 對著真實 output 結果（收件人是誰、檔存在哪）對照便箋上寫的目標 output → 哪個欄位的值錯就是哪個欄位的 expression 錯

#### 卡 30 分鐘的逃生口

**規則**：同問題跑了 3 輪 checklist + LLM 來回超過 5 次還沒解 → **停**

**逃生動線**（求救訊息範本）：

```
【n8n 求救】

我的情境：
- 改 [#XX 哪份 workflow]
- 為了 [改造目的，例：合約改處理發票]
- 環境：[self-host / Cloud]

我跑到第 [X 步驟] 卡關。
看到的錯誤訊息（截圖附上）：
[截圖 1]

我已經跑過 checklist 哪幾條：
- [類別 X] 第 1 條：[結果]
- [類別 X] 第 2 條：[結果]
- ...

我跟 LLM 來回 [N] 次的核心對話（截圖）：
[截圖 2]

我已經試過但沒成功的修法：
- [修法 A]：[結果]
- [修法 B]：[結果]
```

**這份範本的 2 個價值**：
- 給社群 / 講師：他們不用追問就知道你做過什麼，省 3-5 輪來回
- 給「明天的你」：很多問題睡一覺起來看自己整理的訊息會立刻發現

### 4. 完整範例 prompt 模板

第 7 章主要不是 prompt 章，但類別 1 第 4 條「請 LLM 輸出 connections 表格」缺 prompt：

```
（僅在你改了整份 JSON 或新增/刪除節點時用）
請幫我把這份 workflow JSON 裡的 connections 區段輸出成表格：
| 來源節點名稱 | 目標節點名稱 | 來源節點是否在 nodes 陣列 | 目標節點是否在 nodes 陣列 |

不要改 JSON、不要建議修法。只輸出表格。

[貼 JSON]
```

### 5. 範例 LLM 回應

connections 表格 sample 回應：

```
| 來源 | 目標 | 來源在 nodes? | 目標在 nodes? |
|---|---|---|---|
| Manual Trigger | Read PDF | ✓ | ✓ |
| Read PDF | Extract PDF Text | ✓ | ✓ |
| Extract PDF Text | Code: AI 改名 | ✓ | ✓ |
| Code: AI 改名 | Write | ✓ | ✗（找不到 "Write" 節點，只有 "Write File"）|
```

學員看到 `✗` 就找到問題了：connections 引用的是「Write」但 nodes 裡實際是「Write File」 — 名字對不上。

### 6. 驗收標準

學員跑完一次錯誤排查後過關：

- [ ] 我能對應錯誤訊息字串到 3 個類別之一
- [ ] 我能在 30 秒內找到對應的 5 步 checklist
- [ ] 我能填出求救訊息範本（卡關時用）
- [ ] 我知道「3 輪 + 5 次對話沒解 = 停」這個停損規則

### 7. 常見錯誤 + 怎麼解

**錯誤 1：「我看到一個我看不懂的訊息字串，3 個類別都不像」**
- 解：(a) 把訊息字串原文 google 加上「n8n」 (b) 還是不懂 → 用求救範本貼社群 (c) 不要硬猜類別

**錯誤 2：「我跑了類別 1 第 1 條改用『右鍵 Paste 節點』貼，但 n8n UI 沒有 Paste 選項」**
- 解：要先在 n8n UI 點到 workflow 編輯畫面（不是 workflow 列表）→ 在編輯區的空白處右鍵才會跳 Paste

**錯誤 3：「我做了類別 2 第 1 條撤銷 token，但其他 3-4 個 workflow 也用同一個 credential，全都壞了」**
- 解：這是預期行為。撤銷 token 後該 credential 對應的所有 workflow 都要回 credential 設定頁更新成新 token。**這正是為什麼紅線 1 嚴格禁止 credential 外洩** — 出事一次連坐多個 workflow

**錯誤 4：「樣態 2（資料量縮水）— 我每個節點都看了 Items 數量，都沒變化，但最後就是少了 100 筆」**
- 解：可能是 trigger 端的 Limit 參數（例：Google Drive Trigger 預設可能只取 100 筆）。檢查最上游 trigger 節點的 Limit / Pagination 設定

### 8. 回到課程動線

- **解了**：→ 回去第 6 章原本卡的 step 繼續
- **沒解，跑完 3 輪 + 5 次對話**：→ 走逃生口貼社群 / 講師
- **想預防下次再遇到**：→ 第 5 章紅線 1、2、6 重看

### 9. 對現有 HTML 的具體變更

| 動作 | 原 line | 改成 |
|---|---|---|
| 改寫 | 197-203 類別 1 第 4 項 | 「<同類 workflow>」改成「你自己之前 export 的同一份 .json 檔」（明確指本份 workflow） |
| 新增 | 類別 1 第 4 項 | 補 connections 表格 prompt 模板 + sample 回應（如上第 4-5 節） |
| 改寫 | 224-238 類別 2 第 1 條 | 「Google / Notion / OpenAI console 撤銷」改成 3 個直連 URL + 一行操作（如上第 3 節類別 2 第 1 條） |
| 新增 | 類別 2 第 2 條 | 補「在 n8n UI 哪裡找 Credential 欄」step-by-step（節點 → 右側 panel → Settings 旁邊 tab） |
| 改寫 | 271-275 類別 3 第 1 項 | 補「output panel 怎麼讀 JSON 樹」step-by-step + dot path 對 vs 不對 sample |
| 改寫 | 273 optional chaining | 翻譯成「中間加問號」非工程師說法（如上第 3 節類別 3 第 2 條） |
| 改寫 | 287-296 逃生口 | 加「求救訊息範本」可複製版（如上第 3 節） |
| 新增 | 章末 | 加「3 個類別比例」一句話：實務上 100 個錯誤大概是「類別 1 占 30%、類別 2 占 20%、類別 3 占 50%」 — 學員預期管理 |


---

---

## 設計記錄（Phase A 診斷）

本章原始 HTML 章節的「空話」診斷清單，作為重設計的問題對應表：

### 第 7 章 post-llm-7-triage — 3 類錯誤分流 SOP

**整體判定**：這章相對乾淨，分流決策樹有具體訊息字串對照（這是好的）。但 checklist 內部的具體性掉鏈：類別 1 第 4 項說「打開 Lite Pack zip 裡的 workflows/<同類 workflow>.json」——學員會卡在「『同類』是什麼意思？我要找哪個檔？」（判定 1、5）。類別 3 樣態 2「靜默地過濾掉了」是判定 2（沒給「怎麼發現靜默丟資料」的具體檢查動作）。

| # | line | 原文摘要 | 違反 | 為什麼會卡住學員 |
|---|---|---|---|---|
| A7-1 | 197-203 | 類別 1 checklist 第 4 項「typeVersion 是不是 LLM 自己編的？打開 Lite Pack zip 裡的 workflows/<同類 workflow>.json」 | 1, 5 | 「同類 workflow」對非工程師很模糊。「我在改 #02，要去翻哪份來抄 typeVersion？」應該明說「翻 #02 自己的 workflow JSON（你之前 export 出來的那份），不要找『同類』」 |
| A7-2 | 200 | 「請 LLM 輸出表格『每個 connection 的來源節點名稱 / 目標節點名稱 / 是否存在於 nodes 陣列』」 | 1 | 「請 LLM 輸出表格」沒給 prompt 範例。學員照抄這句話貼給 LLM 不會得到正確結果 |
| A7-3 | 224-238 | 類別 2 credential checklist 第 1 項「立刻去 Google / Notion / OpenAI console 撤銷舊 token / 重發新 token」 | 1, 3 | 「Google console 撤銷 token」具體在哪？對非工程師：Google 沒有一個叫「console」的東西，他/她可能找半天找不到「Google Cloud Console」「Google Account Permissions」哪個才是。應該為 3 個最常用的服務（Google、Notion、OpenAI）各給一個直連 URL + 一句操作描述 |
| A7-4 | 234 | 「不要試圖在 JSON 裡用文字找 credential 對應位置」+「正確做法：在 n8n UI 上每個有問題的節點，credential 欄重新選一次」 | 3 | 「重新選一次」的動作具體：「點節點 → 右側 panel 找 Credential 那欄 → 點下拉箭頭 → 選你之前建好的那個」。沒給這個 step-by-step，學員會在 panel 找不到 Credential 欄（n8n 的 panel 有 4-5 個 tab） |
| A7-5 | 271-275 | 類別 3 checklist「在紅燈節點的上一個節點，看 output panel 的 JSON 結構」+「LLM 假設欄位叫 customer.email，實際可能是 contact.mail」 | 1, 5 | 「看 output panel 的 JSON 結構」對非工程師是黑盒——看了之後怎麼判斷哪個欄位是被引用的？應該給「兩段對比 sample：dot path 對 vs 不對」+「在 panel 上滑鼠 hover 哪個欄位會出現複製按鈕」 |
| A7-6 | 273 | 「在 n8n expression 裡用 ?. 避免欄位不存在時整個 expression 炸掉。範例：{{ $json.customer?.email }}」 | 5 | 「optional chaining」對非工程師完全是黑話。雖然有給範例 expression，但學員看到 `?.` 不知道在哪輸入、會不會在 Code 節點和 Set 節點都通用。應該翻譯成情境語：「如果你不確定 LLM 引用的欄位一定存在，就在欄位中間加一個小問號 `?.`，例如把 `customer.email` 改成 `customer?.email`，這樣欄位不存在時節點會走過、不會卡紅燈」 |
| A7-7 | 287-292 | 「卡了 30 分鐘還沒解 — 逃生口」段 | (尚可) | 整段方向對，但「正確的逃生動線：把當前 workflow 截圖 + 你已經跑過的 checklist 項目 + 完整錯誤訊息，一次整理好」——「整理好」具體要列哪些欄位？應該給一個「求救訊息範本」可直接複製：「我在試 [情境]，跑步驟 4 卡 [錯誤訊息]，類別 [N] checklist 我跑過 [項目]，結果都不行。截圖：[附件]」 |

**第 7 章空話小計：7 條**

---
