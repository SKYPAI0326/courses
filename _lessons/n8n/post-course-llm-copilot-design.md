---
slug: n8n-post-course-llm-copilot
title: 用 LLM 協助改寫與自訂 n8n Workflow — 結業後 Copilot 操作手冊
kind: post-course-supplement
audience: 已完成本機 n8n 課程、手上有 Lite Pack 14 個 workflow、會用 ChatGPT/Claude/Gemini 但不會寫 JS 的結業學員
est_length: 預估正文 14,000-18,000 字 ／ 對應 HTML 系列 6-8 頁（含 1 頁 walkthrough 完整實況）＋ 1 份 prompt 模板 .md（含在下載 zip 裡）
format_proposal: HTML 系列頁（主動線）＋ 下載 zip（prompt 模板 .md ＋ 安全清單 cheatsheet PDF）；不做影片，因為核心是「對著 LLM 收斂提問」的反覆操作，影片難以重現學員自己的卡點
depth: deep
cross_link: [n8n-post-course-cloud]
---

## 1. 設計取捨記錄

這份補充教材要做「深」，但深的方向必須界定清楚，否則會落入「教 prompt 工程」或「教 n8n schema 百科」這兩個都對非工程師沒意義的雷區。

**深在哪：** 做成「LLM 協作改 workflow 的操作型 mini-course」。「深」=「**安全改 workflow 的流程**」：拆需求 → 讀 JSON → 限定修改範圍 → 匯入測試 → 錯誤回報 → 收斂。骨架是流程，不是知識點清單。流程的每一步都有「LLM 在這做什麼／學員在這做什麼／怎麼知道自己做對了」的明確分工，學員照著走就能把任何一個 Lite Pack workflow 改成自己情境的版本。

**不深在哪（明確排除）：**

1. 不教通用 LLM prompt 技巧（few-shot、CoT、role-play 等）。學員要的是把工作做完，不是學 prompt theory。提到 prompt 只在「對應流程某一步、有具體任務」的脈絡。
2. 不做 n8n schema 欄位百科（`parameters` / `typeVersion` / `credentials` 各層全解）。這是讓非工程師誤以為重點是讀懂底層格式，反而推遠他們。需要時才查、能用 LLM 代讀就用 LLM。
3. 不教學員手改完整 JSON。本教材的核心主張：**學員不該手改全文**，學員只在 n8n UI 上做最後修整、JSON 由 LLM 在限定範圍內改、靠匯入結果驗收。
4. 不示範高風險操作：不把 credential 一起貼給 LLM、不讓 LLM 直接從零產出完整 workflow 當答案、不教「整個 workflow 重寫」當常規動作。

**為什麼這樣切：** 對應主課程哲學「商業培訓學員要結果不要原理」「禁止給學員 patch 指令」。學員的勝利條件是「我把 #02-pdf-ai-rename 改成處理發票而且跑通了」，不是「我搞懂了 n8n 的 typeVersion 機制」。教材的成敗也用這個指標驗收。

**為什麼還要「深」而不是只給一張 cheatsheet：** 因為「拆需求 → 限定修改範圍 → 錯誤回報 → 收斂」這套流程本身有反直覺的步驟（特別是「限定修改範圍」與「錯誤回報的最小可重現訊息」），學員第一次做一定會跳步。淺的教材會讓他們直接跟 LLM 說「幫我改 #02 處理發票」，拿到一坨匯不進去的 JSON 就放棄。深的教材逼他們走完六步流程一次，內化之後就能自助。

**framing 與 Codex L3 第二意見的對齊：** Codex 採納版本明確指出「深 ≠ prompt 工程，深 = 安全改 workflow 的 SOP」，且雷區清單為核心價值。本提案完整沿用，並在第 5 節把雷區擴成 6 條紅線（含 credential 處理、不要直接產整份 workflow、版本漂移、節點 deprecation、IDs/連線完整性、把 LLM 輸出當答案 vs 當草稿）。

---

## 2. 學員真實使用情境

非工程師結業學員的真實節奏不是「課後立刻動手改」，而是「過一陣子遇到具體痛點才回來找 workflow」。這份教材必須對應這個節奏，不能假設學員結業時就背熟 14 個 workflow 的細節。下列為 5 個 user story，依結業後時間軸排列。

### Story A — 結業 1 週 ／ 把 #02-pdf-ai-rename 改成處理發票
**背景**：行銷企劃 A，結業時跑通範例（合約 PDF 改名）。回到工作崗位第 4 天接到任務「每月 200 張供應商發票要歸檔到 `/檔案/2026/{月份}/{供應商名}_{金額}.pdf`」。
**動作預期**：開啟 #02 在 n8n 介面，看到 prompt 是針對合約寫的，不會自己改。預期需求：「我要 LLM 幫我把這段抽欄位的指令從『甲乙方+合約金額+簽訂日』改成『供應商統編+品項+稅後金額+發票日期』，並把改名 template 換掉。」
**教材對應**：第 6 節 walkthrough 主案例。

### Story B — 結業 2 週 ／ 把 #04-daily-ai-report 從 Google Sheet 換成 Notion
**背景**：營運專員 B 公司剛全面換到 Notion。原 #04 把摘要寫進 Google Sheet，B 想換成寫進 Notion database。
**動作預期**：對 LLM 說「把寫 Sheet 的節點換成寫 Notion」，預期 LLM 會回「請把 Notion node 的 JSON 給我參考」。學員不知道從哪裡拿到 Notion node 的範本 JSON——這是教材要解決的：**請學員先在 n8n UI 拉一個 Notion 節點、隨便填、複製出來給 LLM 當「目標形狀」**。
**教材對應**：第 3 節步驟 2「讀 JSON」與步驟 3「限定修改範圍」的「示範形狀法」。

### Story C — 結業 1 個月 ／ 把 #11-csv-clean-score 接在 Google Drive 觸發器上
**背景**：知識工作者 C 想把同事每週丟到共享 Drive 的 CSV 自動清洗評分。原 #11 是手動上傳觸發。
**動作預期**：需要把 trigger 從 Manual 換成 Google Drive Trigger，且後續節點引用的 input 路徑變了（不再是 Form upload，而是 Drive 檔案 binary）。這牽涉到「資料形狀變了，引用會壞」——是課程 M2 教過的概念，但學員不會自己抓出有哪些下游引用要跟著改。
**教材對應**：第 3 節步驟 4「匯入測試」與第 7 節「邏輯錯」分流。

### Story D — 結業 1 個月 ／ 把 #09-gmail-categorize 改成只看特定客戶來信
**背景**：小型工作室主理人 D 信箱雜訊太多，希望 #09 只處理 3 個 VIP 客戶域名的信。
**動作預期**：很簡單的修改（加 IF 過濾），但學員可能會直接讓 LLM 「重寫整個 workflow」，拿到一份和原 #09 細節漂移的版本。教材要在這提醒「最小修改原則」——只插入一個 IF，不重寫全圖。
**教材對應**：第 3 節步驟 3「限定修改範圍」、第 5 節紅線 2「不要直接產整份 workflow」。

### Story E — 結業 3 個月 ／ Lite Pack 跨大版本後重跑壞掉
**背景**：學員 E 半年後想重新啟動 #06-webhook-gemini-file，發現 n8n 已升 1-2 個大版本，部分節點 typeVersion 過時，匯入時跳警告。
**動作預期**：學員會被「typeVersion mismatch」訊息嚇到，不知道是「不能用了」還是「升一下就好」。教材要教：先嘗試 n8n UI 的「open & save」自動升級、再把 LLM 當 second opinion，不要一開始就讓 LLM 改 typeVersion 數字。
**教材對應**：第 5 節紅線 3「版本漂移」、第 7 節「schema 錯」分流。

> **共通模式**：學員都不是「想學 n8n」，是「想完成具體任務」。教材每一節都要扣回某個 story，避免變成知識點清單。

---

## 3. 核心動線：安全改 workflow 的 6 步流程

這節是教材的骨架。後面所有章節（prompt 模板、紅線、walkthrough、錯誤分流）都必須對齊這 6 步。完成這 6 步之後，學員就有一份能跑、能驗收、出錯也知道怎麼回報的客製版 workflow。

```
[1 拆需求] → [2 讀 JSON] → [3 限定修改範圍] → [4 匯入測試] → [5 錯誤回報] → [6 收斂]
                                                         ↑___________________↓
                                                          只在 5 出錯時迴圈
```

### 步驟 1：拆需求（學員主導）
**動作**：學員用一句話寫下「我要改成什麼」，再用 3 個追問填滿：input 是什麼／output 是什麼／哪些步驟保留不動。
**LLM 在這做**：不做。這一步刻意排除 LLM，因為 LLM 在需求模糊時會自己腦補，越改越亂。
**學員手動做**：填一張 4 格便箋（教材提供範本）：原 workflow 編號、目標 input、目標 output、必保留的節點。
**驗收訊號**：4 格能對著別人講 1 分鐘還不打結。
**雷區**：跳過這一步直接問 LLM「幫我改 #02 處理發票」是新手最常犯的錯，LLM 拿不到 input/output 的具體形狀，會猜，結果就漂掉。

### 步驟 2：讀 JSON（LLM 主導，學員驗收）
**動作**：把整份 workflow JSON（**移除 credential 後**）貼給 LLM，請它做兩件事：(a) 用一段話描述「這份 workflow 做了什麼」，(b) 列出每個節點的角色與資料流向。
**LLM 在這做**：把 JSON 翻成人話。這對非工程師價值最高——LLM 比學員快 50 倍讀 JSON。
**學員手動做**：用 n8n UI 對照 LLM 的描述。如果 LLM 講錯了（例：說某節點是「傳 Email」其實是「寫 Sheet」），代表這份 workflow 結構特殊，後面要更小心。
**驗收訊號**：學員能用自己的話複述一遍 LLM 的描述。
**雷區**：這一步**不要把 credential 區段一起貼**（見第 5 節紅線 1）。教材要附「credential 移除小工具」的步驟（n8n UI 匯出時就有「export without credentials」選項，預設使用這個）。

### 步驟 3：限定修改範圍（學員 + LLM 協同）
**動作**：把第 1 步的需求 + 第 2 步的節點清單，明確告訴 LLM「只改節點 X、Y、Z，其他不動」，並請 LLM 回傳「修改後的這 3 個節點 JSON 區段」，不是整份。
**LLM 在這做**：產出區段 JSON。
**學員手動做**：先在 n8n UI 上把要改的節點選起來、複製、貼到一個臨時筆記檔當 backup。LLM 改完後，學員手動在 n8n UI 上替換這 3 個節點（用「複製貼上節點」功能，不是改檔案）。
**驗收訊號**：n8n UI 上節點還在原位、連線沒斷、其他節點原樣。
**雷區**：「示範形狀法」——如果改動牽涉換新類型的節點（例 Story B 換 Notion），學員應**先在 n8n UI 拉一個目標節點、複製出來給 LLM 當形狀範本**，不要讓 LLM 從記憶生成節點 JSON（typeVersion 容易錯）。

### 步驟 4：匯入測試（學員主導）
**動作**：在 n8n UI 直接點「Execute Workflow」單步測試，或用 trigger 餵一筆樣本資料。
**LLM 在這做**：不做。
**學員手動做**：用最小樣本（1 個檔／1 列／1 封信）跑一次。看每個節點的 output panel 是否如預期。
**驗收訊號**：所有節點都綠燈、output 結構符合需求。
**雷區**：用大批量測試（例：直接把 200 張發票丟進去）會把錯誤埋在中段，難 debug。**永遠先用 1 筆**。

### 步驟 5：錯誤回報（學員 + LLM 協同）
**動作**：當步驟 4 失敗時，學員要產出「最小可重現訊息」給 LLM。
**LLM 在這做**：根據錯誤訊息提診斷。
**學員手動做**：複製三件事到 LLM——(a) 紅燈節點的錯誤訊息全文，(b) 該節點的 input panel 截圖或 JSON，(c) 該節點當前的 parameter 設定 JSON（同樣移除 credential）。**不要只說「跑不出來」或貼整份 workflow 重來**。
**驗收訊號**：LLM 能指出問題在哪個節點、哪個欄位。如果 LLM 也不確定，代表回報資訊不夠，補資料而不是換 LLM。
**雷區**：**不要把整份 workflow 重貼一次請 LLM 重寫**——這就回到「直接產整份 workflow」的紅線。錯誤回報的價值在「縮小範圍」。

### 步驟 6：收斂（學員主導）
**動作**：迴圈跑步驟 3-5 直到通過。每次迴圈不超過 3 輪，超過代表需求或方向錯了，退回步驟 1。
**LLM 在這做**：在步驟 3 / 5 內被呼叫。
**學員手動做**：每輪結束問自己「我比上一輪更接近目標嗎？」如果答否，停下來重看步驟 1 的便箋。
**驗收訊號**：用真實樣本（10 筆）跑通，output 對。然後**才**用全量樣本跑。
**雷區**：「LLM 越改越複雜」——LLM 傾向加防禦邏輯與分支。如果 LLM 第 3 次回覆比第 1 次長 30%，停下來，要求它「保留最小修改、移除新增的防禦邏輯」。

---

## 4. 每一步的 prompt 模板

不寫成「prompt 大全」。每一步只給一個收斂提問。每個 prompt ≤ 8 行、可直接複製、有明確 placeholder。模板會打包進下載 zip 的 `prompts.md`。

> 設計原則：模板開頭固定一句「我是 n8n 非工程師使用者，請以結果為主、不解釋原理」。這句話顯著降低 LLM 把回應寫成教學文的傾向。

### 模板 1：搭配步驟 1（拆需求自我檢查，**選用**，學員可跳過直接手寫便箋）
```
我要改 n8n workflow #{ID}（{原本做什麼}）。
目標 input：{欄位/格式/來源}
目標 output：{欄位/格式/去處}
保留節點：{節點 1, 節點 2}
請問我的需求有哪一格還沒講清楚？只指出空白，不要幫我補。
```

### 模板 2：搭配步驟 2（讀 JSON）
```
我是 n8n 非工程師使用者，請以結果為主、不解釋原理。
以下是一份 n8n workflow JSON（已移除 credential）。請：
1. 用一段話講它做了什麼。
2. 列出每個節點的角色與資料流向（節點名稱 → 它輸出什麼 → 下一個節點吃什麼）。
不要建議改進、不要寫程式碼。
[貼 JSON]
```

### 模板 3：搭配步驟 3（限定修改範圍）
```
我是 n8n 非工程師使用者，請以結果為主、不解釋原理。
基於剛才那份 workflow，只改節點 {X, Y, Z}，不動其他。
我要的修改：{具體描述，含 input/output 形狀}
{若換新節點類型，附：以下是我從 n8n UI 拉出來的目標節點形狀範本：[貼節點 JSON]}
請回傳「只有這 3 個節點」的 JSON 區段。
不要重寫整份 workflow、不要改其他節點。
```

### 模板 4：搭配步驟 5（錯誤回報）
```
我是 n8n 非工程師使用者，請以結果為主、不解釋原理。
我把節點 {N} 替換成你上一輪給的內容後，匯入跑不過。
錯誤訊息：{紅燈節點訊息全文}
該節點 input：{input panel 內容/JSON}
該節點當前 parameter：{節點 parameter JSON，已移除 credential}
請只指出：問題在哪個欄位、最小修改是什麼。
不要重寫節點、不要建議換做法。
```

### 模板 5：搭配步驟 6（收斂止血，當 LLM 越改越複雜時用）
```
請用一句話比較你最早給我的版本與現在這版，哪些是「為了原始需求必要的」、哪些是「你新增的防禦邏輯」？
請保留必要的、移除新增的，再給我一次。
```

> 教材正文每個模板下方要附「踩雷實例」——把錯誤示範也列出來（例：「常見錯：直接貼『幫我改 #02 處理發票』，沒有附 input/output 形狀，LLM 會自己腦補」）。這比正面範例更有教育價值。

---

## 5. 安全紅線（核心價值章節）

紅線清單是這份教材的核心價值之一。Codex L3 兩輪審核（call_id 765f5530 / f9c18d2c）採納版本明確要求雷區「不可模糊化或淡化」，下列 8 條為強制紅線，每條一句話 + 一行為什麼。

### 紅線 1：不要把 credential 一起貼給 LLM
**為什麼**：n8n workflow JSON 內可能包含 API key、Gmail OAuth token、Notion integration secret 等敏感欄位。即使你「信任」某 LLM 服務，貼上去就失去控制權。**永遠用 n8n UI 的「export without credentials」選項**，並在貼給 LLM 前用搜尋確認沒有 `apiKey` / `accessToken` / `password` 字串殘留。

### 紅線 2：不要讓 LLM 直接產出完整 workflow JSON 當最終答案
**為什麼**：LLM 從零生成的 workflow JSON 有極高機率出現 typeVersion 過時、節點 ID 衝突、connection 引用錯位、參數 schema 漂移等問題，匯入直接失敗或更糟——匯入成功但跑起來資料形狀不對。**永遠以官方 Lite Pack 或 n8n UI 拉出來的範本為基底，LLM 只在限定範圍內改**。

**特別禁止項目**（即使只改一段，這些也不能讓 LLM 自動決定）：webhook URL、trigger 類型、schedule 排程、recipient list（收件人 / 通知對象）、任何 delete / update / drop 類資料庫或 API 操作。任一被誤改 = production 直接出事，沒得救。

### 紅線 3：版本漂移要先用 n8n UI 的自動升級，不要叫 LLM 改 typeVersion
**為什麼**：n8n 升大版時，節點的 typeVersion 與 parameter schema 可能變動。LLM 不知道你裝的是哪一版，直接改 typeVersion 數字會把問題從「警告」變成「跑時 crash」。**先在 n8n UI 開啟 → 它會自動處理可升級的部分 → 跑不通再用 LLM 對照新舊 schema 排查**。

### 紅線 4：節點 deprecation 要查官方 changelog，不要相信 LLM 的記憶
**為什麼**：LLM 訓練資料有 cutoff，可能不知道某節點已被官方改名／拆分／移除（例：n8n 歷史上有過 Gmail node 拆出 Gmail Trigger 的情況）。**遇到「找不到節點」/「節點變灰」時先去 n8n 官方 changelog 與社群論壇查證**，再決定是換新節點、還是用 HTTP Request 直接打 API。

### 紅線 5：不要把 LLM 輸出當答案，要當草稿
**為什麼**：LLM 給的 JSON 區段有 90% 機率「看起來合理」但「跑起來細節錯」。一定要走完步驟 4「匯入測試」+ 步驟 6 收斂迴圈。**沒有跑過真實樣本之前，那只是草稿，不是答案**。

### 紅線 6：保留節點 ID 與 connection 完整性
**為什麼**：n8n workflow JSON 裡，節點之間靠 `id` 與 `connections` 區段串聯。LLM 在區段改寫時容易動到 ID 或漏掉 connection。**步驟 3 要求 LLM「只回傳節點區段」、學員在 n8n UI 上做替換**就是為了避開這個——不要直接覆蓋整份 JSON 檔。

**重要補述**：若學員確實需要新增或刪除節點（不是修改既有節點），connections 區段必須回到 n8n UI 上手動重接，**不要叫 LLM 寫 connections JSON**。UI 上拖線 30 秒就完成，LLM 寫錯一個 ID 你 debug 30 分鐘。連帶提醒：第 7 節「錯誤分流 SOP」的 connections 檢查 checklist，**只有在你改了整份 JSON 或新增／刪除節點時才需要跑**——UI 上區段替換沒動 connections，跳過。

### 紅線 7：改完先在隔離環境驗，不在 production workflow 直接測
**為什麼**：n8n 匯入流程預設保留原 workflow 的 active 狀態，若改的是已開的 production workflow，匯入瞬間就會用未驗證版本接收真實流量／真實檔案。**正確流程**：(a) 在 n8n UI 點 workflow 右上角「Duplicate」複製一份命名 `<原名>-edit`、(b) 把 LLM 改的內容套到複本、(c) 確認複本 trigger 是 OFF（或 Manual）、(d) 跑通再複製回原 workflow。任一步跳過 = 你在用真客戶資料當白老鼠。

### 紅線 8：destructive 操作必先 dry-run
**為什麼**：涉及刪資料（Notion delete page / Drive delete file）、寄信（Gmail / Telegram 發給真實收件人）、更新 CRM（HubSpot / Pipedrive update record）的節點，LLM 改錯一個欄位就是真寄錯人、真刪檔。**正確流程**：(a) 把 destructive 節點先 disable 或換成 console log 等價假動作、(b) 跑通驗證 input／output 資料形狀、(c) 改寫 recipient 為自己的測試帳號、(d) 用 1-3 筆假資料跑、(e) 全程 OK 才換回真收件人 / 真資料源。**寧願多花 5 分鐘做 dry-run，不要省這步**。

> 紅線必須做成獨立 cheatsheet PDF（A4 雙欄一頁），下載 zip 內附，學員可以印出貼螢幕邊。

---

## 6. 完整 walkthrough 案例（最終交付的單元頁範本）

### 為什麼選 #02-pdf-ai-rename
評估三個候選：

| Workflow | 改造張力 | LLM 介入價值 | 雷區覆蓋度 | 結論 |
|----------|----------|--------------|------------|------|
| #02-pdf-ai-rename | 高（改 prompt + 改檔名 template + 不換節點類型） | 高（學員看 prompt JSON 容易花，LLM 簡化價值大） | 中（不太會踩 typeVersion，credential 紅線會踩） | **主案例** |
| #11-csv-clean-score | 高（改評分維度 + 改 trigger） | 高 | 高（換 trigger 觸發引用斷裂，能完整示範雷區） | **次案例（教材附錄略寫）** |
| #04-daily-ai-report | 中（換輸出端） | 高（典型 Story B） | 中 | 留作學員自我練習 |

**主案例選 #02 的理由**：(a) 對應 Story A，是非工程師最高頻情境；(b) 不需換節點類型，能讓學員第一次走完 6 步流程不被 typeVersion 雷區打斷信心；(c) prompt 區段是 JSON 字串，正好示範「LLM 讀自己給自己看的 prompt」這個 meta 操作；(d) 改檔名 template 是純文字操作，驗收訊號清晰（檔名對不對一眼可見）。

**次案例 #11**：放在教材附錄一頁，**只展示**：因為換 trigger 從 Manual → Google Drive，下游節點所有 `{{ $json.file }}` 引用要跟著改成 `{{ $node["Google Drive Trigger"].json.binary.data.fileName }}`。這是 Story C 的核心痛點，用來證明「資料形狀變了，引用會壞」這個 M2 教過的概念在改造時會具體長什麼樣。**不示範完整 6 步流程**，避免重複。

### Walkthrough 章節編排（最終單元頁範本應長這樣）

每個小節對應第 3 節某一步驟，標題明確。本提案只給編排骨架，不寫完整對白，落地時由 course-lesson-writer 補。

1. **設定情境**（300 字）— 行銷企劃 A 接到 200 張發票任務，舊 #02 是合約版。
2. **步驟 1：拆需求**（範本便箋示範一張，含 4 格內容）— 真的填一次，不是空白格。
3. **步驟 2：讀 JSON**（截圖 LLM 對話 1 輪）— 展示 LLM 把 #02 翻成「讀 PDF → 抽欄位 → 改名 → 移檔」這 4 段，並對照 n8n UI 上的節點順序（學員視角）。
4. **步驟 3：限定修改範圍**（截圖 LLM 對話 2-3 輪）— 含 1 次學員回頭追問「你給的 JSON 是整份還是區段？我只要區段」的反例修正。
5. **步驟 4：匯入測試**（n8n 介面截圖 3 張）— 用 1 張樣本發票跑、看 output panel、紅燈截圖。
6. **步驟 5：錯誤回報**（截圖 LLM 對話 1 輪）— 故意安排 1 次錯（例：LLM 用了原 prompt 的「甲方」欄位名沒換成「供應商」），示範錯誤回報的最小可重現訊息怎麼貼。
7. **步驟 6：收斂**（10 張樣本 → 200 張）— 中間穿插「LLM 想加 try/catch 防禦，學員拒絕」的 1 行對話示範。
8. **驗收交付**（300 字）— 改造後的 workflow 截圖 + 200 張處理結果資料夾截圖。

> 篇幅預估：walkthrough 單頁 6,000-7,000 字 + 12-15 張截圖。是整份教材最重的一頁，也是學員最會反覆看的一頁。落地時請 course-lesson-writer 確保「對話截圖」是真的跑出來的，不是模擬——LLM 對話的細微語氣會被學員看出真假。

---

## 7. 錯誤分流 SOP（LLM 給的 workflow 匯不進去時）

當步驟 4 匯入失敗，先用「錯誤訊息屬於哪一類」分流。教材在這節提供決策樹 + 3 類 checklist。

### 分流決策樹（一張圖，落地時請設計師畫成 SVG）
```
匯入失敗 / 跑不通 / 結果不對
    │
    ├─ 訊息含 "Could not parse" / "Invalid JSON" / "Unexpected token"
    │  或 "node type not found" / "unknown parameter" / "connections"   → JSON / workflow 格式錯（類別 1）
    │
    ├─ 訊息含 "Credential" / "Credential not found" / "401 Unauthorized"
    │  或 "403 Forbidden" / "invalid_grant" / "invalid_client"
    │  或 "token expired" / "API key" / "OAuth"                         → credential 錯（類別 2）
    │
    └─ 匯入成功但 output 不對 / 紅燈在某節點中段
       或 全綠燈但「資料量縮水 / 寄錯人 / filter 條件錯」               → 邏輯錯（類別 3）
```

### 類別 1：JSON / workflow 格式錯（n8n 進不去）
**特徵**：n8n 直接拒絕匯入，跳「無效的 workflow」之類視窗，或匯入成功但跳「節點類型不存在」紅字。
**Checklist**：
- [ ] 你是不是「整份覆蓋」而非「在 UI 替換節點」？回去走步驟 3。
- [ ] LLM 給的 JSON 開頭是 `{` 還是 ` ```json`？把 markdown code fence 拿掉。
- [ ] 節點之間的 `connections` 區段有沒有指向不存在的節點 ID？請 LLM 輸出表格：每個 connection 的「來源節點名稱 / 目標節點名稱 / 是否存在於 nodes 陣列」（學員一眼掃完）。
- [ ] **此項僅在你改了整份 JSON 或新增／刪除節點時才需檢查**。UI 上區段替換沒動 connections 的話跳過，回去檢查節點欄位本身。
- [ ] typeVersion 是不是 LLM 自己編的？**怎麼查**：打開 Lite Pack zip 裡的 `workflows/<同類 workflow>.json`，編輯器搜尋同名 node type（例如 `"type": "n8n-nodes-base.googleDrive"`），抄它的 `typeVersion` 數字回填到你的 JSON。
- [ ] 用 jsonlint.com 或 VS Code 開檔看哪一行壞了，把那行貼給 LLM 修，**不要重寫整份**。

### 類別 2：credential 錯（認證掉了）
**特徵**：匯入成功但執行紅燈，訊息含 401 / Credential not found。
**Checklist**：
- [ ] 你是不是不小心把含 credential 的 JSON 貼出去過？三步動線（順序不能跳）：(1) **立刻去 Google / Notion / OpenAI console 撤銷舊 token**、(2) **重發新 token**、(3) **回 n8n UI 上點該節點 → credential 欄 → 重新選新建的 credential**。這比修 workflow 急。
- [ ] LLM 改完的節點，credential reference 是不是空了？n8n UI 上點該節點，credential 欄會顯示「未選擇」，重新指定即可。
- [ ] 不要試圖在 JSON 裡用文字找 credential 對應位置。**正確做法**：匯入後直接回 n8n UI 上每個有問題的節點，credential 欄重新選一次（即使顯示是對的也選一次），讓 n8n 重新綁 credential reference。
- [ ] 是 self-host 還是 Cloud？某些 credential 類型在 self-host 需要額外配 OAuth callback URL。

### 類別 3：邏輯錯（最難，最常見）
**特徵**：匯入成功、credential 也對、但跑出來的結果不是要的。可能長三種樣子：
1. **紅燈卡在中段節點**：訊息常見「Cannot read property 'X' of undefined」「Item is empty」。
2. **全綠燈但資料量縮水**：例如預期 200 筆變 50 筆——多半是 filter 條件錯或迴圈邏輯錯。
3. **全綠燈但寄錯／存錯**：寄信寄到錯的收件人、檔案存到錯的資料夾、欄位對應顛倒——肉眼比對 input／output 才看得出來。
**Checklist**：
- [ ] 在紅燈節點上一個節點，看 output panel 的 JSON 結構。是不是和 LLM 預期的形狀不同？
- [ ] 引用的欄位路徑對不對？在 n8n expression 裡用 `?.` 避免欄位不存在時整個 expression 炸掉。**範例**：`{{ $json.customer?.email }}` 取代 `{{ $json.customer.email }}`，前者沒有 customer 欄位會回 undefined（節點走過），後者直接紅燈。
- [ ] 是不是 Trigger 換了之後，下游引用沒跟著改？（Story C 經典坑）
- [ ] 用步驟 5 的「錯誤回報模板」貼給 LLM，**只貼紅燈那節點+上一節點+紅燈訊息**，不要貼整份。
- [ ] LLM 的修法看起來要動 5 個以上欄位？回頭看步驟 1，需求是不是模糊了。

> 教材在這節要附「我卡了 30 分鐘還沒解，怎麼辦？」逃生口：建議把當前 workflow 截圖 + 問題描述貼到課程社群／講師信箱，**不建議深夜 1 點繼續和 LLM 死磕**。

---

## 8. 執行環境互鎖

弱互鎖到雲端 n8n 教材（slug: `n8n-post-course-cloud`）。本節 4 點對照即可，不展開。

| 對照面向 | self-host（本課主路線） | n8n Cloud |
|----------|--------------------------|-----------|
| **Credential 儲存位置** | 你電腦 / 你 VPS，由你負責備份與機密管理 | n8n 雲端，他們負責加密儲存 |
| **節點可用性** | 全部 community node 可裝（自負風險） | 部分節點受限，community node 受審核 |
| **檔案路徑** | 可指 `./shared/` 或 `/Users/.../folder` 等本機路徑 | 不能直接讀本機檔案，必須走 Drive / S3 等雲端中介 |
| **Execution 配額** | 無上限，但吃你電腦 / VPS 資源（電費、CPU、磁碟） | 依方案有 monthly execution 上限 |

> **改 workflow 前，先確認你跑在哪個環境。** 同一份 LLM 改寫建議，在 self-host 與 Cloud 上適用程度不同。例：LLM 建議「用 Read Binary File 節點讀本機 PDF」——這在 self-host 可行，在 Cloud 必失敗，要改走 Drive 下載再讀 binary。

> 想跑 Cloud？看 [n8n Cloud 結業補充教材](./n8n-post-course-cloud-design.md)（同系列另一份提案，由 PM 規劃中）。

---

## 9. 交付形式建議

**主形式：HTML 系列頁，6-8 頁**

建議頁面切分（依閱讀動線）：

| 頁次 | 標題 | 預估字數 | 對應本提案章節 |
|------|------|----------|----------------|
| 1 | 開場 + 為什麼要學這套流程（含設計取捨摘要 + Story 對照） | 1,500 | 第 1、2 節 |
| 2 | 6 步流程總覽（含主圖 + 每步 1 段） | 1,500 | 第 3 節 |
| 3 | 步驟 1-3 詳解（拆需求、讀 JSON、限定修改範圍）含 prompt 模板 1-3 | 2,500 | 第 3、4 節前半 |
| 4 | 步驟 4-6 詳解（匯入測試、錯誤回報、收斂）含 prompt 模板 4-5 | 2,500 | 第 3、4 節後半 |
| 5 | 安全紅線 6 條（單頁聚焦） | 1,500 | 第 5 節 |
| 6 | Walkthrough：把 #02 改成處理發票（最重一頁） | 6,000 | 第 6 節主案例 |
| 7 | 錯誤分流 SOP（決策樹 + 3 類 checklist） | 2,000 | 第 7 節 |
| 8 | 環境互鎖 + 自我練習（提供 #04 / #11 兩題不給答案） | 1,000 | 第 8 節 + 銜接 |

**閱讀動線**：頁 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 線性，每頁底固定有「上一頁／下一頁」。第 5 頁紅線與第 7 頁分流 SOP 同時設為**側邊永久連結**（學員真正動手時最常翻這兩頁）。

**附帶下載 zip**：
```
n8n-llm-copilot-pack.zip
├── prompts.md          （5 個 prompt 模板，純文字，學員可直接複製）
├── safety-cheatsheet.pdf （A4 一頁，6 條紅線）
├── checklist.md        （錯誤分流 3 類 checklist 純文字版）
└── README.md           （怎麼用這個 pack）
```

**為什麼不做影片**：核心動線是「對著 LLM 收斂提問」的反覆操作，每個學員的需求都不同，影片難以重現具體卡點。HTML 系列頁 + 對話截圖 + 下載 zip 已經涵蓋學習路徑。如未來確實有需求，建議只拍**步驟 5「錯誤回報」3 分鐘短示範**（這是學員最容易跳過、影片最能展示的一步），不拍整套。

**頁面風格**：沿用本課程主色 `#5a7a5a`（n8n 主題色）+ V4 CCS Editorial 視覺語彙，與其他 n8n 單元頁一致。Walkthrough 頁的 LLM 對話截圖建議統一用淺灰底 + 細邊框 + monospace，學員一看就知道「這是對話實況」。

---

## 10. 驗收標準

學員完成這份教材後應能做到（動詞開頭、可驗證）：

1. **能用 4 格便箋拆解一個改造需求**（input / output / 保留節點 / 編號），並能對著別人講 1 分鐘不打結。
2. **能在不貼 credential 的前提下**，把任一 Lite Pack workflow JSON 貼給 LLM 並要求它翻譯成中文流程描述。
3. **能下指令讓 LLM 只回傳節點區段、不重寫整份 workflow**，並在 n8n UI 上正確完成節點替換。
4. **能用「最小可重現訊息」格式回報錯誤**（紅燈訊息 + 上一節點 input + 當前 parameter，三件套），不會貼整份 workflow 重來。
5. **能把 #02-pdf-ai-rename 改成處理某種非合約類文件**（發票、收據、PO、申請表 4 選 1），跑通 10 筆樣本。

> 驗收方式：第 5 條是硬指標，建議課後社群開「結業挑戰」收件，學員把成品截圖貼出來。前 4 條是過程指標，靠教材 walkthrough + 自我練習頁的對照清單由學員自評。

---

## 11. 製作工序建議

給 course-designer / course-lesson-writer 落地時的指引。

### 寫作順序（不要照頁次寫）
1. **第一個寫 walkthrough（頁 6）**——這是教材唯一**必須實機跑過**的內容。先把 #02 真的改一次（用真 LLM、真 n8n、真發票樣本），把對話、截圖、卡點全部留下。其他章節都基於這份實機紀錄反推，避免紙上談兵。
2. **第二寫 6 步流程（頁 2-4）+ prompt 模板**——有 walkthrough 當素材後，6 步骨架是「從實作往回抽象」，比「先寫骨架再找例子」誠實。
3. **第三寫紅線（頁 5）+ 錯誤分流（頁 7）**——這兩節最容易變空話。請一定要在 walkthrough 跑的時候同步記錄「我差點踩了什麼」，紅線就用真實 near-miss 寫，不要憑空列舉。
4. **最後寫頁 1（開場）+ 頁 8（自我練習）**——最虛、最可寫的兩頁，留到最後寫，避免前面被它們拖住。

### 必須實機驗證的章節
- **頁 6 walkthrough**：100% 必須實機跑，含至少 1 次故意安排的錯誤回報示範。
- **頁 7 錯誤分流**：3 類錯誤每類都要有 1 個實際發生過的案例做底稿，不能只列 checklist。

### Codex 是否再審
**建議再審 1 輪**，但只審第 5 節紅線清單與第 7 節錯誤分流 SOP——這兩節是「給結業學員看的安全規範」，是文案誠實度規則延伸到課後階段，性質與大綱誠實度規則接近，Codex L3 第二意見有價值。其他章節（walkthrough、prompt 模板）屬實作教學，課程設計師主導即可，不需 Codex。

> 走 `python3 codex_bridge.py --task consult --section 5,7 --file post-course-llm-copilot.html`。預計 Phase B 手動模式跑 1 輪即可。

### 與其他補充教材的銜接
- **n8n-post-course-cloud**（雲端 n8n 結業補充）：本提案第 8 節弱互鎖過去，由該提案接手講 Cloud 限制與遷移思路。
- **未來可能的 post-course-debug**（卡關自助手冊）：第 7 節錯誤分流可以升級成獨立教材，但**不建議現在做**——先讓這份 LLM Copilot 跑半年，收集學員實際卡點，再決定是否獨立。

### Plan / Todo 邊界
本設計提案落地時，由 course-lesson-writer 接手，**頁 6 walkthrough 是唯一需要 plan 的單位**（因為要實機跑）。其他頁是線性寫作，TodoWrite 一條 「`寫完 8 頁 + 打包 zip`」即可，不需細拆。

---

> 設計提案結束。下一步：交給 course-designer 在大綱框架內審視銜接、由 course-lesson-writer 從頁 6 walkthrough 開始實機落地。
