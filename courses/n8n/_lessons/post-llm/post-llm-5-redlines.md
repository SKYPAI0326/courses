---
unit_id: post-llm-5-redlines
title: 10 條紅線 — 用 LLM 改 workflow 不能踩
course: n8n / AI 資料工廠
chapter: 第 5 章 / 8（post-llm 系列：課後用 LLM 改 workflow）
description: 每條紅線含「危險動作 + 為什麼 + 安全替代路徑」+ 章末業務改動需求對照表
audience: 商業培訓非工程師、課後用網頁版 LLM（ChatGPT / Claude / Gemini）改 workflow
prerequisite: 已跑過 Lite Pack 14 個 workflow 至少 1 次；理解 #02 PDF AI 改名範例
delivery: 文字導向 HTML 章節（無印風）
created: 2026-05-07
codex_audit: 961c0ffe
codex_verdict: actionable（已修補）
last_updated: 2026-05-07
---

# 10 條紅線 — 用 LLM 改 workflow 不能踩

> **本章重設計教案** · 對應 `courses/n8n/lessons/post-llm-5-redlines.html`

## 重設計內容

## 第 5 章重設計：紅線 = 危險動作 + 安全替代路徑

### 1. 學員此時的痛點

學員到第 5 章可能是兩種狀態：

- **路線 A**：剛看完第 4 章，看完整流程後想知道「動手前我要避開什麼坑」
- **路線 B**：已經卡在某個錯誤，被第 4 / 7 章引導過來查紅線

不管哪種狀態，他/她最不想看的是「8 條禁忌列表然後沒有了」。心裡的話：

- **不能讓 LLM 改 webhook URL，那我真的需要改 URL 怎麼辦？**
- **不能讓 LLM 改 typeVersion，那升版本怎麼辦？**
- **這頁告訴我『不要做』，那『要做什麼』在哪？**

### 2. 核心要傳遞的 1 個觀念

**紅線 ≠ 禁忌。紅線 = 「LLM 在這做容易錯」+「正確路徑你自己（或在 n8n UI 上）做才安全」。每條紅線都有「替代動線」。**

### 3. 具體 step-by-step（重設計：每條紅線變雙欄）

把現有 8 條紅線從「禁忌+為什麼」改成**「危險動作 + 為什麼錯 + 安全替代路徑（給具體動作）」**三段式。

#### 紅線 1：credential 不能貼給 LLM

- **危險**：把含 `apiKey` / `accessToken` / `password` 的 JSON 貼進 LLM 對話
- **為什麼**：貼上去 = 失去控制權。LLM 服務的對話歷史可能被訓練、被洩漏、或在團隊 plan 被同事看到
- **安全替代路徑**：
  1. n8n UI 開啟 workflow → 右上角 `⋮` → Download → 跳出視窗選「Without credentials」（不是 Default）
  2. 下載的 .json 檔，用 VS Code 或記事本打開，**Cmd+F 搜尋這 4 個字串都要找不到**：`apiKey`、`accessToken`、`password`、`token`
  3. 如果還是找到 → 該欄位手動改成 `"REDACTED"` 再貼 LLM
- **驗收硬指標**：搜尋 4 個字串都 0 個結果

#### 紅線 2：不要讓 LLM 直接產出完整 workflow JSON

- **危險**：對 LLM 說「給我完整 workflow JSON 我直接匯入」
- **為什麼**：LLM 從記憶生成的 JSON 有 90% 機率出現 typeVersion 過時 / 節點 ID 衝突 / connection 引用錯位 — 匯入直接失敗或更糟（成功但靜默跑錯）
- **安全替代路徑**：
  1. **改節點：** 用模板 3 + 在 n8n UI 上區段替換（見第 3 章）
  2. **新增節點：** 在 n8n UI 上手動拖 → 連線 → 內容讓 LLM 改字串
  3. **改 webhook URL：** 在 n8n UI 上點 webhook 節點 → 旁邊有「Copy Test/Production URL」按鈕，**自己 copy 自己貼**，不讓 LLM 寫 URL
  4. **改 trigger 類型：** 在 n8n UI 上手動換新 trigger 節點（拖一個 Google Drive Trigger）→ 把舊 Manual Trigger disable / 刪除
  5. **改 schedule 排程：** 在 n8n UI 上 Schedule Trigger 的 Cron Expression 欄位，自己照 Google「cron 每天 9 點」查到的 expression 貼，不讓 LLM 編
  6. **改 recipient list：** 在 n8n UI 上 Gmail 節點的 To 欄位，自己貼 email，不讓 LLM 從上下文猜
  7. **改 delete/update/drop 操作：** 整個動作先 disable 該節點，跑通其他流程後，最後人工開啟並用紅線 8 dry-run

#### 紅線 3：不要叫 LLM 改 typeVersion

- **危險**：要求 LLM 把節點 typeVersion 從 2 改成 3 來「修升級錯誤」
- **為什麼**：typeVersion 對應到 n8n 裝的版本，LLM 不知道你裝的版本。猜錯就 crash
- **安全替代路徑**：
  1. n8n UI 開啟舊 workflow → 通常頂部會跳「This workflow contains nodes that need to be updated」黃色橫條 → 點「Update」按鈕
  2. UI 自動把節點升級到當前裝的版本（這是 n8n 內建邏輯，比 LLM 準）
  3. 如果升級後仍跑不過，把「升級前 vs 升級後的 parameter」兩段 JSON 貼給 LLM，問「哪個欄位的格式變了」
- **驗收硬指標**：UI 升級後黃色橫條消失，節點不再變灰

#### 紅線 4：節點 deprecation 不要相信 LLM 記憶

- **危險**：n8n UI 上某節點變灰跳「This node is deprecated」，問 LLM「我要換成什麼節點」
- **為什麼**：LLM 訓練資料 cutoff 可能比你裝的 n8n 版本舊。LLM 說「換成 X 節點」可能那節點也被 deprecated
- **安全替代路徑（5-10 分鐘可走完，4 步順序固定）**：

  **第 1 步（30 秒判斷確認真的是 deprecated）**：在 n8n UI 上點該節點 → 點齒輪 ⚙ → 看右側 panel 有沒有 `typeVersion` 欄位（通常會顯示 1 / 2 / 3 等數字）+ 看節點顏色是不是比同列其他節點**深灰**（n8n 對 deprecated 節點的視覺訊號就是降低彩度變灰）。如果 typeVersion = 1 而其他類似節點是 2 / 3，加上顏色變灰 → 99% 確認是 deprecated。

  **第 2 步（2 分鐘 — 在 n8n UI 內找替代）**：n8n UI 左側 / 右上角有 **+ Add Node** 搜尋 box，輸入舊節點名稱（例：`Google Sheets`）。看搜尋結果列表 — 如果有同名節點後面標 **"(new)"** 或標 **"v2"** / **"v3"**，那就是替代節點。直接從搜尋結果拖一個出來。

  **第 3 步（如果第 2 步沒有 (new) / v2 結果，3 分鐘 — 看官方 docs banner）**：到該節點對應的 n8n 官方文件頁，URL pattern 是：

  ```
  https://docs.n8n.io/integrations/builtin/<category>/n8n-nodes-base.<nodename>/
  ```

  例：Google Sheets → `https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/`

  頁面頂端如果該節點 deprecated，會有黃 / 紅 banner 寫 **"This node is deprecated. Use [新節點名] instead."**，連結會直接導去新節點 docs。把新節點名抄回 n8n UI 第 2 步搜尋。

  **第 4 步（fallback，5 分鐘 — 第 1-3 步都沒結果才用 LLM，且只問候選清單）**：把第 1-3 步的事實貼給 LLM，**只要它給「可能的替代節點名 + 為什麼」候選清單**，不要它直接改 workflow：

  ```
  我在 n8n UI 上看到節點 [節點名稱] 被標記 deprecated（typeVersion 1，
  顏色變灰）。我已經在 n8n UI + Add Node 搜尋過沒有 (new) / v2 版本，
  也看了 docs.n8n.io 對應頁沒有 deprecated banner 指明替代。

  請只給我「在 n8n 1.x latest 版本可能可以替代它的節點名稱清單」
  + 每個的「適合什麼場景」一句話描述。
  不要寫 JSON、不要寫程式碼、不要建議改 workflow。
  ```

  拿到候選清單後，回 n8n UI + Add Node 搜尋每個候選，看哪個能拖出來不變灰、能正常設定 → 就用那個。

- **驗收硬指標**：第 1-3 步至少有一步找到替代節點，且該節點在 n8n UI 拖出來不變灰、能正常設定（如果走到第 4 步 fallback，候選清單裡至少 1 個在 UI 內能正常拖出）

#### 紅線 5：LLM 輸出當草稿，不當答案

- **危險**：LLM 給 JSON → 學員直接點 Active 開關上線
- **為什麼**：LLM 給的 JSON 有 90% 機率「看起來合理但跑起來細節錯」
- **安全替代路徑（強制動線）**：
  1. **禁止**：直接在原 workflow 點 Active
  2. **必走**：先 Duplicate 成 -edit → 確認 Active 開關 OFF → 跑 1 筆 → 跑 10 筆 → 全量跑通 → 才換回原 workflow
  3. **驗收硬指標**：你的 workflow 列表，原 workflow 名 + -edit 後綴版同時存在；只有跑通 10 筆後 -edit 版才被合併回原版

#### 紅線 6：保留節點 ID 與 connection 完整性

- **危險**：覆蓋整份 workflow JSON 檔案 / 用文字編輯器手改 connections 區段
- **為什麼**：節點 ID 對不上 → 匯入後節點變灰 / connections 引用錯 → 匯入成功但連線斷
- **安全替代路徑**：
  1. **不要**：用文字編輯器打開 workflow.json 直接改 — 連 1 個逗號錯整份炸
  2. **要**：在 n8n UI 上做所有「結構變動」（新增節點 / 刪除節點 / 重接連線）
  3. **重接連線具體動作**：在 n8n UI 上，把上一個節點右側的小圓點 → 按住滑鼠拖到下一個節點左側的小圓點 → 放開 → 出現一條線就接好了
  4. **驗收硬指標**：n8n UI 上所有節點之間都有實線（不是虛線、不是斷掉的線）

#### 紅線 7：改完先在隔離環境驗

- **危險**：在 production workflow 上直接改 + 跑 → 用真客戶資料當白老鼠
- **為什麼**：n8n 匯入流程預設保留 active 狀態，瞬間就接真實流量
- **安全替代路徑（self-host）**：
  1. n8n UI workflow 列表 → 原 workflow 右側三點 → Duplicate
  2. 改名為 `<原名>-edit`
  3. 點開 -edit 版，右上角 Active 開關確認 OFF（灰色）
  4. 套 LLM 改的內容到這個 -edit 版
  5. 跑 1 筆 → 跑 10 筆 → 通過後 → 把改好的 -edit 版改名為 `<原名>-v2` 並 Active；原版改名為 `<原名>-v1-archived` 並 OFF
- **安全替代路徑（n8n Cloud）**：流程相同，Cloud 也支援 Duplicate（n8n UI 操作一致）
- **驗收硬指標**：workflow 列表上同時看到原版 + -edit 版兩條；切換時 Active 狀態切得乾淨

#### 紅線 8：destructive 操作必先 dry-run

- **危險動作清單**：
  - Gmail / Outlook / Telegram / Slack 節點：發訊到真實收件人
  - Notion / HubSpot / Salesforce 節點：delete / update record
  - Google Drive / Dropbox / S3 節點：delete file / overwrite file
  - SQL 節點：DELETE / UPDATE / DROP
- **為什麼**：LLM 改錯一個欄位 = 真寄信 / 真刪檔 / 真改 CRM

- **執行前 3 件事**（每條至少做 1 件，不一定要做齊 3 件，用來「即使 LLM 真的給你錯的指令，傷害也限縮在可恢復範圍」）：

  1. **目標資料先備份一份**：
     - SQL：`mysqldump -u <user> -p <db> > backup_2026-05-07.sql` / `pg_dump <db> > backup.sql`，檔放專案根
     - Google Sheet：開該 spreadsheet → File → Make a copy → 命名 `<原名>-backup-2026-05-07`
     - Notion / HubSpot / Salesforce：先匯出 CSV（這 3 個服務都有 Export 功能在 settings 或右上角 ⋯）
     - Drive / Dropbox / S3：複製整個目標資料夾到 `<原名>-backup-2026-05-07`

  2. **限制範圍跑 — 在節點 parameter 加 filter 只跑少量**：
     - SQL DELETE：原本 `DELETE FROM users WHERE status='inactive'` → 加 `LIMIT 10` 變 `DELETE FROM users WHERE status='inactive' LIMIT 10`，或改成 `WHERE id IN (1,2,3,4,5)` 鎖定 5 筆測試 ID
     - Notion / HubSpot / CRM update：在前一個節點（通常是 Search / Filter）加 limit = 5，只把 5 筆推給 update 節點
     - Gmail / Telegram 發訊：在前一個 Filter / IF 節點加 `WHERE id IN (...)` 只發 5 筆
     - Drive delete：先在 Drive list 節點加 search query 限縮成只 5 個檔

  3. **跑完手動 spot check 5 筆**：
     - SQL：開 DB client（TablePlus / pgAdmin / DBeaver）查那 5 筆 id 的當前狀態，比對「應該變什麼 vs 實際變什麼」
     - Sheet：直接打開 spreadsheet 看那 5 列
     - CRM：開 Notion / HubSpot UI 找那 5 筆 record 看欄位
     - Drive / Dropbox：用 Finder / 網頁端看那 5 個檔的存在與檔名
     - Gmail / Telegram：去自己（或測試帳號）的收件夾 / Bot 視窗確認 5 筆訊息真的收到 + 內容對

  3 件全做完才能拉開全量。

- **安全替代路徑（具體動作）**：
  1. **disable 該節點**：n8n UI 上點該節點 → 旁邊「⏸」暫停圖示
  2. **跑通其他流程**：執行 Workflow，看 input 進到 disabled 節點前那一步的 output 對不對
  3. **改寫成「等價假動作」**：
     - Gmail：把 To 欄位（原本可能是 `{{$json.email}}`）改成你自己的私人信箱字面值（例：`yourself@gmail.com`）
     - Notion delete：先換成 Notion read（讀同一個 page，不刪）
     - Drive delete：先換成 Drive list（列出資料夾內容，不刪）
     - SQL DELETE：先換成 SELECT 同樣 WHERE 條件（看會 select 出哪幾筆）
  4. **跑 1-3 筆假資料**：看是不是「對的對象 / 對的 WHERE 條件」
  5. **換回真收件人 / 真資料源**：通過後才換回
- **驗收硬指標**：dry-run 階段你的私人信箱收到 1-3 封測試信，**沒有任何真實收件人收到信**；備份 / 限範圍 / spot check 至少做了 1 件

#### 紅線 9：不要把 credentials / .env / webhook secret 貼給 LLM

- **危險**：學員為了讓 LLM「看到完整 context」會直接 paste：
  - credentials JSON（含 `apiKey` / OAuth refresh token / service account JSON）
  - `.env` 內容（postgres 密碼 / `N8N_BASIC_AUTH_PASSWORD` / Telegram bot token / Gemini API key）
  - webhook URL 內含的 secret query param（例 `https://.../webhook/abc?token=xxx`）
- **為什麼**：LLM 對話會被廠商記錄。商業 ChatGPT / Claude / Gemini 各家政策不同，但**「不要假設你貼給 LLM 的東西不會出現在訓練語料 / log analyst 螢幕上」是合理 default**。一次 paste，這個 secret 必須當作已 leaked、立刻 rotate — 不要心存僥倖賭「這只是一次對話、應該沒事」
- **安全替代路徑**：
  1. **想給 LLM 看 workflow 形狀**：用 placeholder 替換實值，LLM 看 shape 不看值：
     - `"apiKey": "AIzaSy..."` → `"apiKey": "__GEMINI_API_KEY__"`
     - `"botToken": "8123456789:AAH..."` → `"botToken": "<YOUR_TG_TOKEN>"`
     - `"password": "Pa55w0rd!"` → `"password": "<YOUR_PG_PASSWORD>"`
     - 紅線 1 的「Without credentials」export 已經幫你做了大部分；這條補的是「.env 或自己手抄到 LLM 對話的字串」
  2. **真的需要 LLM 解 .env 結構**：給檔案 schema 描述（「我有 5 行 KEY=VALUE，KEY 列表是 `N8N_BASIC_AUTH_PASSWORD` / `GEMINI_API_KEY` / `TG_BOT_TOKEN` / `PG_HOST` / `PG_PASSWORD`，要 LLM 解每個 KEY 應該長什麼樣」），**不貼實值**
  3. **webhook URL 也要去 secret**：把 `?token=xxx` / `?secret=yyy` 段截掉再貼，只留 `https://<host>/webhook/<id>` 形狀
  4. **最壞情況不小心 paste 了**：立刻去對應服務 rotate / regenerate secret —
     - Gemini API key → Google AI Studio → API Key → Regenerate
     - Telegram bot token → BotFather → `/revoke` 該 bot 重發
     - Postgres → `ALTER USER <user> WITH PASSWORD '<新密碼>'` + 更新 n8n credential
     - n8n basic auth → 改 `.env` 的 `N8N_BASIC_AUTH_PASSWORD` + 重啟 n8n container

     不要心存僥倖。
- **驗收硬指標**：你貼進 LLM 對話的所有內容 Cmd+F 搜尋 `apiKey`、`token`、`password`、`secret`、`AIzaSy`、`sk-`（OpenAI key 前綴）→ **要嘛 0 個結果，要嘛只搜到 placeholder 字串（`__X__` / `<YOUR_X>`）沒有真實值**
- **與課程 lite-pack 的關係**：上面 placeholder 範例是「貼到 LLM 對話前的脫敏手法」，不是課程 lite-pack 的內部運作機制。lite-pack v1.3 起 Gemini key 改走 `$env.GEMINI_API_KEY` 路徑（key 寫在 starter-kit/.env，workflow JSON 完全不含 key），所以從 n8n UI 匯出 workflow JSON 不會洩漏 — 但「貼進 LLM 對話」的紅線仍然有效，因為你貼出去的東西可能包含 credentials / .env 內容。

#### 紅線 10：不要匯入或執行從外部來路不明的 workflow JSON

- **危險**：尤其含 `n8n-nodes-base.httpRequest` / `n8n-nodes-base.code` / `n8n-nodes-base.executeCommand` / `n8n-nodes-base.readWriteFile` / Send Email 等節點的陌生 workflow，可能在你的 n8n 跑時：
  - 打外部 server（exfiltrate 你的 data）
  - 上傳你的 credentials 到攻擊者控制的 endpoint
  - 刪你的 shared / 本地檔案
  - 用你的名義發 email / 發 Telegram 訊息
- **為什麼**：n8n workflow 是你 n8n 帳號權限的延伸 — 匯入後**你的 credentials 自動是它的 credentials**。陌生 workflow JSON 從技術上等同陌生人寄你一個 .exe 叫你雙擊
- **安全替代路徑**：
  1. **來源限制**：只匯入「課程提供」/「自己親手寫」/「你親自審完每個節點」的 workflow。Reddit / GitHub gist / Discord 隨便撿到的 — 不匯
  2. **匯入前先用 VS Code 打開 JSON 看 nodes 列表**，搜尋這 5 個高風險節點 type：
     ```
     n8n-nodes-base.httpRequest
     n8n-nodes-base.code
     n8n-nodes-base.executeCommand
     n8n-nodes-base.readWriteFile
     n8n-nodes-base.emailSend
     ```
     若有，逐一看它做什麼（HTTP 打哪 / Code 寫什麼 / 讀寫哪個檔）
  3. **第一次跑必設 trigger 為 manual**：別讓它 active schedule / webhook 一匯入就自動跑。在 n8n UI workflow 設定裡把 Active 開關 OFF + Trigger 節點換成 Manual Trigger
  4. **用測試帳號 / 測試 credentials 先試一輪**：在 n8n 裡開一個 "test" credential（用測試 API key、測試 DB），把 workflow credential 切到測試版跑，看它行為符不符合預期，才換回正式 credential
- **驗收硬指標**：匯入前 5 個高風險節點 type 都看過 + 第一次跑時 Active OFF + Trigger 是 Manual + credential 是測試版

### 4. 完整範例 prompt 模板

第 5 章本身不是 prompt 章，但有 1 個追問模板給「LLM 不知道我的 typeVersion」情境：

```
我已經在 n8n UI 上點 Update 自動升級節點到當前版本，
但跑起來還是有問題。
舊版本 parameter（升級前）：[貼舊 JSON]
新版本 parameter（升級後）：[貼新 JSON]
請只指出哪個欄位的格式變了，最小修改是什麼。
不要重寫節點、不要建議換做法。
```

### 5. 範例 LLM 回應

紅線 3 sample（typeVersion 升級後追問）：

```
比較舊版（typeVersion 2）和新版（typeVersion 3）的 parameter：

變動的欄位：`additionalFields.attachmentsBinaryData`
舊版：直接接受字串「="data"」
新版：必須包成物件 { "binaryPropertyName": "data" }

最小修改：把 attachmentsBinaryData 從 "=data" 改成 { "binaryPropertyName": "data" }。
```

### 6. 驗收標準

學員整章讀完應該能：

- [ ] 對每條紅線說出「危險動作 + 替代路徑」（8 條配對）
- [ ] 知道 webhook URL / trigger / schedule / recipient / delete 5 種「LLM 不能碰」的東西，自己在 n8n UI 怎麼處理
- [ ] 印出本章 cheatsheet（建議 A4 雙欄 1 頁）貼螢幕邊
- [ ] 動手前必檢清單（6 條快速版）：
  - [ ] 我用了 export without credentials 並搜尋 4 個字串都找不到
  - [ ] 我**沒有** paste credentials / .env / webhook secret 給 LLM（紅線 9 — secret leak 比 prompt 改錯嚴重一級）
  - [ ] 我在 -edit 版做事，不在 production
  - [ ] 我請 LLM 給「節點區段」不是「整份」
  - [ ] 我有 destructive 節點時，先 disable 或改 dry-run
  - [ ] 我 10 筆樣本跑通才放全量

### 7. 常見錯誤 + 怎麼解

**錯誤 1：「我看到紅線 4 deprecation，去 google 半天找不到答案」**
- 解：商業培訓學員不要花超過 15 分鐘 google。15 分鐘沒解 → 截圖+描述貼課程社群。LLM/google 不是 unique solution

**錯誤 2：「我做了紅線 7 的 Duplicate，但忘了關 Active 開關，差點上 production」**
- 解：Duplicate 完成後**第一個動作就是檢查 Active 開關**（甚至寫便利貼貼螢幕）。下次嚴格走「Duplicate → 開關 OFF → 改名」這個固定動線

**錯誤 3：「Cloud 沒有 Duplicate 按鈕」**
- 解：Cloud 也有，n8n UI 動作一致 — 在 workflow 列表 / 開啟畫面右上角 `⋮`。如果真的找不到，可能是 Cloud 的某個 starter plan 限制（極少見），這時用「Export without credentials → New workflow → Import」三步替代

**錯誤 4：「dry-run 我把 To 改成自己信箱跑了，結果沒收到信」**
- 解：(a) Gmail credential 是否還有效？看節點 credential 欄位是否亮綠 (b) 你自己的信箱是否在垃圾郵件 (c) 是否真的執行了那個 Gmail 節點（看 n8n UI execution 紀錄）

### 8. 回到課程動線

- **動手前**：必看 6 條快速檢查（紅線 1、2、5、7、8、9）
- **動手後出錯**：紅線可能是線索，但具體去第 7 章分流
- **印出 cheatsheet**：本章是「貼螢幕邊」的查詢頁，建議列印

### 8.5 章末對照表：常見業務改動需求 → 對應紅線 → 安全路徑

學員不會用「紅線編號」思考，他/她用「我這次想做 X」思考。這張表把常見業務改動需求映射回紅線編號，1-2 分鐘 quick scan 就能找到該章哪一段：

| 我想做什麼 | 對應紅線 | 安全路徑（去本章哪段看） |
|---|---|---|
| 把測試 webhook URL 換成正式環境 | #2 | 紅線 2 安全替代 step 3（n8n UI Copy Test/Production URL 按鈕，自己 copy 自己貼） |
| 把 schedule trigger 從每 15 分鐘改成每天 8am | #2 | 紅線 2 安全替代 step 5（自己照 google 查到的 cron expression 貼） |
| 把通知信收件人從 me@example.com 改成同事 | #2 | 紅線 2 安全替代 step 6（n8n UI Gmail 節點 To 欄位自己貼，不讓 LLM 從上下文猜） |
| 該節點在新版 n8n 變灰 / 提示 deprecated | #4 | 紅線 4 安全替代 4 步（UI ⚙ 看 typeVersion → UI + Add Node 搜尋 (new) → docs.n8n.io banner → LLM 候選清單 fallback） |
| 想升級節點 typeVersion | #3 | 紅線 3 安全替代（n8n UI 黃色橫條 Update 按鈕，不要叫 LLM 猜版本） |
| workflow 要 SQL DELETE / Notion delete record / Drive 刪檔 | #8 | 紅線 8「執行前 3 件事」（備份 / 限範圍 / spot check 5 筆）+「等價假動作」 |
| 想把整個 .env 貼給 LLM 排錯 | #9 | 紅線 9 安全替代 step 2（給檔案 schema 描述，不貼實值） |
| 不小心把 API key 貼進 ChatGPT 對話了 | #9 | 紅線 9 安全替代 step 4（立刻 rotate / regenerate，不要心存僥倖） |
| 同事 / 網友傳了個 workflow JSON 想匯進來 | #10 | 紅線 10 安全替代 4 步（來源限制 → 看 5 個高風險節點 → Manual Trigger → 測試 credential） |
| 想直接讓 LLM 改 trigger 類型 | #1 / #2 | 紅線 1（不貼 credential）+ 紅線 2 安全替代 step 4（在 n8n UI 上手動換 trigger） |
| 想把 LLM 給的 JSON 直接點 Active 上線 | #5 | 紅線 5 安全替代（Duplicate → OFF → 跑 1+10 → 才合併） |

**列印建議**：把這張表 + 第 7 節「常見錯誤 + 怎麼解」+ 動手前 6 條快速檢查印 A4 一張，雙欄排版貼螢幕邊。每次要動 workflow 前掃 30 秒。

### 9. 對現有 HTML 的具體變更

| 動作 | 原 line | 改成 |
|---|---|---|
| 改寫 | 8 條紅線 cards 結構 | 從「危險+為什麼」二段式改成「危險+為什麼+安全替代」三段式（如上第 3 節） |
| 新增 | 紅線 1 內 | 加 step-by-step（n8n UI 開啟 → ⋮ → Download → Without credentials） + 4 字串搜尋驗收 |
| 新增 | 紅線 2 禁止項目清單 | 對 5 種禁項（webhook URL / trigger / schedule / recipient / delete）各補「正確怎麼做」一條（如上第 3 節） |
| 新增 | 紅線 3 內 | 加 UI 升級具體動作（黃色橫條 → Update 按鈕） + 升級失敗的追問模板 + sample LLM 回應 |
| 改寫 | 紅線 4 內 | 從「4 順位 fallback」改成「5-10 分鐘 4 步可執行版」（UI ⚙ 看 typeVersion → UI + Add Node 搜尋 (new) → docs.n8n.io banner → LLM 候選清單 fallback）。把「問 LLM」從第 1 順位降到 fallback |
| 改寫 | 紅線 5 內 | 從「LLM 輸出當草稿」改成具體強制動線（Duplicate → OFF → 跑 1+10 → 合併） |
| 新增 | 紅線 6 內 | 加 n8n UI 重接連線具體動作（小圓點拖線）+ 截圖描述位置 |
| 新增 | 紅線 7 內 | 加 Cloud 版動線（一致，但備注 starter plan 例外處理） |
| 改寫 | 紅線 8 內 | 「dry-run」翻譯成具體 actions（5 種 destructive 節點各給「假動作」做法）+ 補「執行前 3 件事」（備份 / 限範圍 / spot check 5 筆） |
| 新增 | 紅線 8 之後 | 新增紅線 9（不貼 credentials / .env / webhook secret 給 LLM）+ 紅線 10（不匯入來路不明的 workflow JSON，5 個高風險節點檢查） |
| 新增 | 第 8 節後 | 加 8.5 章末對照表「常見業務改動需求 → 對應紅線 → 安全路徑」（11 列 quick scan） |
| 新增 | 章末 | 加「動手前 6 條快速檢查」cheatsheet（含紅線 9 secret 檢查）+ 列印建議（A4 雙欄） |


---

---

## 設計記錄（Phase A 診斷）

本章原始 HTML 章節的「空話」診斷清單，作為重設計的問題對應表：

### 第 5 章 post-llm-5-redlines — 8 條紅線

**整體判定**：使用者提示這章可能「只列禁忌沒給安全替代」是準的。8 條紅線裡有 4 條（紅線 1、4、5、6）只說了「不要做」沒給「正確要做什麼」（判定 3）。另外**整章都有判定 5**：每條紅線的「為什麼」段落用大量技術名詞（typeVersion、connections、OAuth callback URL）但沒給商業情境 anchor，學員看完能背但不會用。

| # | line | 原文摘要 | 違反 | 為什麼會卡住學員 |
|---|---|---|---|---|
| A5-1 | 167-172 | 紅線 1「不要把 credential 一起貼給 LLM」 + 「永遠用 export without credentials」 | 3 | 「永遠用 export without credentials 選項」一行帶過。學員第一次用，會問「這個選項在 n8n UI 哪裡？我點哪個按鈕？」應該給 step-by-step（甚至 3 張截圖箭頭）：「右上角三點 → Download → 選 Without credentials」（雖然第 3 章 line 254 有寫，但紅線章是「印出來貼螢幕邊」的查詢頁，必須能獨立讀） |
| A5-2 | 175-191 | 紅線 2「不要讓 LLM 直接產出完整 workflow JSON 當最終答案」+ 禁止項目清單（webhook URL / trigger / schedule / recipient list / delete update drop） | 3 | 列了 5 個「不能讓 LLM 自動決定」的東西，**完全沒說正確的做法是什麼**。例如「webhook URL」如果學員真的需要改，要怎麼安全做？答案應該是「在 n8n UI 上手動 copy 新 webhook URL → 在 LLM 對話裡告訴 LLM『URL 我已經自己貼好了，你只要改節點名稱就好』」這種替代路徑 |
| A5-3 | 195-198 | 紅線 3「不要叫 LLM 改 typeVersion」+ 「先在 n8n UI 開啟 → 它會自動處理可升級的部分」 | 3 | 「自動處理可升級的部分」是好的，但學員不知道：(a) UI 在哪裡會出現升級提示？(b) 升級提示長什麼樣？(c) 點什麼按鈕確認升級？需要 step-by-step |
| A5-4 | 202-206 | 紅線 4「節點 deprecation 要查官方 changelog」 | 3, 5 | 「查官方 changelog」對非工程師是巨大門檻——changelog 是英文、密度極高，學員 99% 不會點開讀。應該降級到「截圖傳到課程社群問講師」或「把節點名 google『n8n + 節點名 + deprecated』」這種非工程師可執行的 fallback |
| A5-5 | 210-215 | 紅線 5「不要把 LLM 輸出當答案，要當草稿」 | 1 | 整條只在「重述系列核心立場」，沒給具體動作。如果這真是「紅線」，應該是「LLM 給你 JSON 後**禁止**直接點 Active 開關，必須先在 -edit 複本跑 1 筆 + 10 筆。誰跳這步誰負責」這種可執行禁令 |
| A5-6 | 218-231 | 紅線 6「保留節點 ID 與 connection 完整性」+ 「若確實需要新增或刪除節點，connections 區段必須回到 n8n UI 上手動重接」 | 3, 5 | 「手動重接 connections」是空話：在 n8n UI 上是怎麼重接的？拖線拖到哪？應該配截圖+具體動作：「在 n8n UI 上，把上一個節點右側的小圓點，按住拖到下一個節點左側的小圓點」 |
| A5-7 | 234-247 | 紅線 7「改完先在隔離環境驗」+ 4 步動線 | (尚可，但有缺) | 動線寫了，但**漏了「Cloud 版用戶怎麼辦？」**的處理。Cloud 沒有 self-host 的 Duplicate 一樣動線嗎？實際上有，但應該明說 |
| A5-8 | 251-264 | 紅線 8「destructive 操作必先 dry-run」+ 5 步動線 | (尚可，但是) | 5 步動線「先 disable 或換成 console log 等價假動作」——對非工程師「console log 等價假動作」是術語。應該翻成 actions：「Gmail 節點：把『To』欄位的收件人 expression 整段刪掉，貼上你自己的私人信箱」 |

**第 5 章空話小計：8 條**

---
