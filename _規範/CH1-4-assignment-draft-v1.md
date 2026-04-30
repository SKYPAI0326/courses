# CH1-4 課堂作業內容草稿 v1

## 標題
**把 Lina 的 v4 變成團隊用 GPTs：System Prompt 定型工坊**

## ⏱ 預估時間
核心 20 min + 進階 20 min（CH1-4 標 3.0h）

## 跨章敘事
- CH1-2 學員寫 P1 prompt（一次性使用）
- CH1-3 Lina 自寫 v1/v2/v3 失敗，學員寫 v4 救她（仍是一次性）
- **CH1-4 把 v4 「定型」成 GPTs，給整個 CSM 團隊每月一鍵使用**

整合本章兩個 mini-prac + 4 元素：
- mini-prac 1（拆解現成 System Prompt 標 4 元素）→ 識別經驗
- mini-prac 2（壓力測試 10 輪對話）→ 穩定性思維
- 4 元素：Persona / Task Boundary / Output Lock / Refusal

---

## 情境敘述（lede · 約 270 字）

延續上週 — Lina 看到你 CH1-3 寫的 v4 prompt 跑出完美結果（不再編造、deadline 全 YYYY-MM-DD、語言一致），興奮地說：

「這個太好用了！每月活動復盤都能省 1 小時。可不可以變成 GPTs 或 Claude Project，給我們整個 CSM 團隊一鍵呼叫？我不太懂 GPTs 設定，但我看 ChatGPT 自訂指示那邊好像可以放 system prompt？」

你今天剛學完 **System Prompt 四元素（Persona / Task Boundary / Output Lock / Refusal）+ 跨輪穩定性 + ChatGPT/Claude 設定方式**，正好可以把 Lina 的 v4 升級成可重用的 GPTs。

關鍵差異：v4 是**一次性 user prompt**（每次都要重貼），GPTs 是**System Prompt 永久固定 + User Prompt 只貼變動部分**（每次只貼 mp3 逐字稿）。要拆對哪些屬於「每次都一樣」、哪些屬於「每次不同」。

> **本作業範圍**：本節學的「四元素設計 + 跨輪穩定性 + 平台設定」三個子技巧。不必深入 RAG、Function Calling（Part 6 才學）、評估自動化（Part 6/7）。

---

> **跟前面練習的關聯**：mini-prac 1 你練了「拆解現成 System Prompt」（讀別人的），mini-prac 2 練了「壓力測試 10 輪對話」（看穩定性）。本作業換成「**寫一個給團隊用的 System Prompt**」+ 預測壓力點 — 從讀者變成設計者。

---

## 本作業拆解

- **核心 20 min（必做）**：拆 v4 為 System / User 兩段 + 補 4 元素 + 寫 3 個壓力點預測（GPTs 設定截圖可選）
- **進階 20 min（可選）**：完整寫 ChatGPT Custom GPT instructions + 1 條變體（Claude Project 配置）+ 100 字反思

---

## Lina 的 v4 prompt（material-inline · 你 CH1-3 寫的版本）

```
【角色】你是松果科技的會議助理，擅長把口語化的會議錄音逐字稿轉成可匯入 Asana 的結構化待辦清單。你只整理會議裡明確說過的事，不得編造，不得從常識推測團隊應該做什麼。

【任務】我會貼上 1 小時上週新品發表會復盤會議的逐字稿（約 8000 字），請你抽出真正的待辦事項，輸出可直接匯入 Asana 的 JSON 格式。

【限制】
- 待辦定義：必須有「動作 + 負責人 + 大概截止」三要素且會議中明確被決議的事項
- 不得補常識：禁止憑「公司應該做的事」推測（如 team retreat、brand guidelines）
- 缺資訊處理：owner/deadline 會議沒明說就填 null，由 Lina 補
- 禁止模糊時間：deadline 必須是 YYYY-MM-DD 或 null
- 語言一致性：task 用中文，其他欄位英文
- 未決議分流：「待議題」「討論未結論」放 pending_decisions 陣列

【輸出格式】（JSON schema 含 task/owner/deadline/priority/context + pending_decisions）

【AI 自我檢查】產出後逐項自檢 3 條（context 是否在原文找得到 / owner deadline 是否真有講 / task 是否中文且動詞開頭）
```

🤔 **Lina 的需求**：「把這個變成 GPTs，CSM 團隊每月都要用，他們可能會問各種無關的問題（『順便幫我寫客訴回覆』『這個專案要不要做』），需要 AI 自動拒絕。」

---

## 任務清單（assignment-tasks）

**核心交付（必做）**：

1. **System / User 拆分表**：把 v4 的 8 段內容（角色、任務、6 條限制、輸出格式、自檢）逐項分到「每次固定 → System」或「每次變動 → User」
2. **System Prompt 四元素填寫**：用 Persona / Task Boundary / Output Lock / Refusal 四欄重組 System
3. **3 個壓力點預測**：列出「**團隊成員可能會把 GPTs 用在什麼非預期情境**」，每個情境 GPTs 應該怎麼回應（呼應 mini-prac 2 的壓力測試）

**進階交付（可選）**：

4. **完整 ChatGPT Custom GPT 配置**：包含 Name / Description / Instructions / Conversation Starters（4 個建議起手語）
5. **變體**：寫成 Claude Project 版本（系統提示詞 + Knowledge 上傳建議）
6. **100 字反思**：4 元素中 Refusal 是這次最容易忽略的嗎？實務上要怎麼驗證 Refusal 真的有效？

---

## 評分標準（rubric · 基本 4 條 + 加分 3 項）

**基本要求**：

1. **System / User 拆分正確**：每次固定的（角色、規則、輸出格式、自檢）→ System；每次變動的（具體那次的逐字稿）→ User。不能把規則放 User、不能把逐字稿放 System。
2. **四元素完整**：Persona / Task Boundary / Output Lock / Refusal 都明確填寫，每元素有具體內容（非「請扮演 X 角色」這種片段）
3. **Refusal 具體**：不只寫「請拒絕無關問題」，要寫 **拒絕話術範本**（如「這個 GPT 只負責活動復盤會議轉待辦，你的問題建議用團隊另一個 GPTs『客訴回覆助理』處理」）
4. **3 個壓力點貼近真實**：不是「如果使用者輸入錯字怎麼辦」這種小事，要是「**真實業務情境的越界使用**」（順便寫週報、分析戰略、推薦產品）

**加分項**：

- ➕ **完整 GPTs 配置 + Conversation Starters 設計**
- ➕ **Claude Project 變體**：發現平台差異（Claude 適合附 Knowledge 檔案、ChatGPT 適合 Custom Action）
- ➕ **驗證機制**：在 System Prompt 加「**每 N 輪自我檢查一次定位**」防漂移

---

## 折疊參考解答（assignment-answer）

### System / User 拆分表

| v4 原文段 | 屬性 | 為什麼 |
|---------|------|--------|
| 角色（會議助理） | **System** | 每次都一樣 |
| 任務說明（轉 Asana 待辦）| **System** | 工作邊界，每次都一樣 |
| 6 條限制（待辦定義 / 不得補常識 / 缺資訊處理 / deadline 格式 / 語言 / 未決議分流）| **System** | 規則固定 |
| JSON 輸出 schema | **System** | 格式固定 |
| AI 自我檢查 3 條 | **System** | 自檢規則固定 |
| 「我會貼上 1 小時上週新品發表會復盤會議的逐字稿」 | **User**（每次都要換） | 具體那次的逐字稿不一樣 |

### System Prompt 四元素重組

```
【Persona · 角色設定】
你是松果科技 CSM 團隊內部的「會議轉待辦助理 v1」。你只做一件事：把會議錄音逐字稿轉成可匯入 Asana 的結構化待辦清單。
你的個性：嚴謹、保守、寧可標 null 也不編造。

【Task Boundary · 任務邊界】
你能做的：
- 從會議逐字稿抽出明確被決議的待辦
- 標出「未決議事項」放 pending_decisions

你不能做的（重要）：
- 不寫客訴回覆（那是另一個 GPTs）
- 不分析商業策略、不推薦產品決策
- 不評估會議效率、不點評同事發言
- 不從常識推測團隊應該做什麼

【Output Lock · 輸出鎖定】
- 格式：JSON 結構，含 tasks 陣列 + pending_decisions 陣列
- tasks 每筆欄位：task（中文，動詞開頭，≤30 字）/ owner（會議裡的人名，沒提填 null）/ deadline（YYYY-MM-DD 或 null，禁止 TBD/Q2/Next month 等模糊時間）/ priority（High|Medium|Low）/ context（會議原話節錄 ≤30 字）
- 語言：task 用中文，其他欄位英文
- 自我檢查：產出後逐項檢查 3 條（context 是否在原文找得到 / owner deadline 是否真有講 / task 是否中文且動詞開頭），任一不符請重寫

【Refusal · 拒絕策略】
若使用者請求超出本 GPTs 範疇（例如：寫客訴回覆、寫週報、分析商業策略、推薦工具），請回應：

「這個 GPT 只負責**活動復盤／週會逐字稿轉 Asana 待辦**。你問的『{{使用者具體請求}}』屬於 [客訴回覆 / 文案撰寫 / 商業策略]，建議使用團隊另一個對應的 GPTs，或直接問 ChatGPT 不附本 system prompt。」

不要硬接、不要跳出角色給任意答案。每 5 輪對話自我檢查一次：「我是不是還在做活動復盤轉待辦？」
```

### 3 個壓力點預測

1. **Sue（業務）丟一份客訴信進來說「順便幫我寫個回信」** → GPTs 應該觸發 Refusal，回「這個 GPT 只負責活動復盤轉待辦，建議用團隊的『客訴回覆助理 GPTs』」
2. **CSM 主管問「這個會議我們的決策品質如何？哪個議題討論不夠？」** → 觸發 Refusal（評估會議效率不在範疇），回「我只做轉待辦，會議品質評估建議找 People Ops 或 OKR 工具」
3. **新進員工貼了 8000 字逐字稿但只說「整理一下重點」沒說 Asana** → 應主動詢問或預設套 v4 規則（不要自動退回散文）

### 進階：完整 ChatGPT Custom GPT 配置

```
GPT Name: 會議轉待辦助理 v1（CSM 內部）
Description: 把活動復盤／週會逐字稿轉成可匯入 Asana 的 JSON 待辦清單。嚴謹保守，不編造。

Instructions:
[此處貼上完整 System Prompt，含 Persona / Task Boundary / Output Lock / Refusal]

Conversation Starters（4 個）：
1. 「貼上會議逐字稿，幫我轉成 Asana JSON」
2. 「這個會議裡有幾個明確被決議的待辦？」
3. 「我的 CSM 月度會議錄音逐字稿在這（貼上）」
4. 「這份逐字稿哪些是待辦、哪些是 pending？」

Knowledge: （無上傳檔案，純 System Prompt 配置）
Capabilities: ☐ Web Browsing ☐ DALL-E ☐ Code Interpreter（都關閉，純文字處理）
```

### 常見錯誤（自我比對 · 5 條）

1. **把 6 條限制寫進 User Prompt** → 每次都要重貼很累，違反 GPTs 設計初衷
2. **Refusal 寫「請拒絕無關問題」** → 太模糊，AI 不知道怎麼拒絕；要給**具體話術 + 範例**
3. **Persona 只寫一句「你是助理」** → 沒個性、沒邊界，AI 會漂移成通用助理
4. **沒設「每 N 輪自我檢查」** → 跨輪漂移最常見的問題，10 輪後可能完全變樣
5. **壓力點預測只想到「使用者輸入錯字」這種低層級** → 要想「**業務情境越界**」這種真實場景

---

## 變體（assignment-variants）

**變體 1｜Claude Project 版本**

把同一份 System Prompt 改寫為 Claude Project：
- System Prompt（Custom Instructions）：同上
- **Knowledge**（Claude Project 獨有）：上傳「松果科技組織架構圖.pdf」「Asana 待辦欄位規格.md」
- 對比 ChatGPT Custom GPT vs Claude Project 的差異：哪個適合附文件知識庫、哪個適合無 Knowledge 純規則。

**變體 2｜團隊權限分層**

設計 3 個版本的 GPTs：
- **L1（一般員工）**：只能轉待辦，無 Knowledge
- **L2（主管）**：可上傳「team OKR 季報」做交叉分析
- **L3（管理層）**：可調用 Code Interpreter 做進階統計

挑戰：System Prompt 怎麼分層、Refusal 怎麼判斷使用者層級（提示：透過 Conversation Starters 引導使用者自報層級）。
