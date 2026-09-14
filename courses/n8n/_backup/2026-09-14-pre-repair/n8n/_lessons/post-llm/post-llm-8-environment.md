---
unit_id: post-llm-8-environment
title: 環境互鎖 + 真實驗收
course: n8n / AI 資料工廠
chapter: 第 8 章 / 8（post-llm 系列：課後用 LLM 改 workflow）
description: 改 workflow 前先確認自己在哪跑（local / -edit / Active）+ 改完真實驗收（不只 Code 綠燈）
audience: 商業培訓非工程師、課後用網頁版 LLM（ChatGPT / Claude / Gemini）改 workflow
prerequisite: 已跑過 Lite Pack 14 個 workflow 至少 1 次；理解 #02 PDF AI 改名範例
delivery: 文字導向 HTML 章節（無印風）
created: 2026-05-07
codex_audit: 6ffbb482
codex_verdict: actionable（已修補）
last_updated: 2026-05-07
---

# 環境互鎖 + 真實驗收

> **本章重設計教案** · 對應 `courses/n8n/lessons/post-llm-8-environment.html`

## 重設計內容

## 第 8 章重設計：環境互鎖 + 真實驗收

### 8.0 為什麼這章排在錯誤分流（第 7 章）之後 — 但要先做

教學順序：先教錯誤分流（第 7 章）讓你能自救，**但實機操作時請先做本章 8.X 環境檢查再進第 7 章分流**。理由：環境錯時，第 7 章分流會帶你走錯方向（例如你以為是 typeVersion 對不上，實際是在 Cloud 上而 LLM 給的是 local 才有的節點；或你以為節點壞了，實際是 production workflow 的 Active 開關被觸發跑掉）。建議**列印第 8 章 8.X 表貼螢幕邊**，每次坐下動 workflow 前 30 秒掃過去。

### 1. 學員此時的痛點

學員看到第 8 章是「我跑完了，現在呢」狀態。心理：

- **我知道我跑通 1 個改造，但下一個改造也會嗎？**（驗收）
- **我同事用 n8n Cloud，我教他怎麼避坑**（環境差異）
- **我想再試別的 workflow，給我下一個練習**

### 2. 核心要傳遞的 1 個觀念

**「我學會了」=「我能在沒有 step-by-step 的狀態下，獨立完成下一個改造任務」。第 8 章是檢驗這個獨立性的關卡，不是收尾雞湯。**

### 3. 具體 step-by-step

#### 8.X 環境檢查 4 項（每次動 workflow 前 30 秒掃過）

每項都要具體到「看 n8n 哪裡 / 看到什麼字串算對 / 看到什麼字串要警覺」。建議列印貼螢幕邊。

| 檢查項 | 在 n8n UI 哪裡看 | 看到什麼算對 | 看到什麼要警覺 |
|--------|----------------|----------|------------|
| Local vs Cloud | 瀏覽器網址列 | `localhost:5678/workflow/...`（local） | `*.app.n8n.cloud/workflow/...`（cloud — 注意 LLM 給的節點是否 cloud 支援） |
| -edit vs production | 工作區左上角 workflow 名稱 + 瀏覽器 tab title | `02-pdf-ai-rename-edit`（結尾有 `-edit`） | `02-pdf-ai-rename`（無 `-edit` = 是 production，動到要立刻 Cmd+Z 退） |
| Active 開關 | 工作區右上角藍色 toggle | **灰色 OFF**（schedule/trigger 不會自動跑） | **藍色 ON**（一動到就會被 trigger 觸發 — 對 -edit 要關，對 production 看你需求） |
| 上次 Execution 時間 | 工作區右側 Executions 分頁第一筆 timestamp | 跟你預期執行時間一致（手動跑就是剛才） | 比預期早 / 你沒跑卻有新 execution = trigger 自己跑了，回去查 Active 開關 |

**Local vs Cloud anti-pattern**：學員跨環境（公司 VPS 一個 n8n、家裡 Docker 又一個）時，看到 `n8n.yourcompany.com` 這類自架域名要當 self-host 處理（不是 Cloud），記下「我這個域名背後實際是 self-host 還是 Cloud」，否則 LLM 對話應對會走錯。

**-edit vs production anti-pattern**：Duplicate 出 `-edit` 後左上角名稱會顯示新名稱，但**有些版本 tab title 還停在舊名**幾秒鐘才刷新，這時不要急著動，重新整理一次再開始。

**Active 開關 anti-pattern**：第一次 Duplicate -edit 完，新 workflow 預設 Active OFF，但學員容易不小心打開（n8n UI 右上角 toggle 一點就反）。每次坐下繼續做之前 30 秒看一眼 toggle 顏色。

**Executions 時間 anti-pattern**：你回家後隔天再來，看 Executions 第一筆是凌晨某個時間，且不是你跑的 — 表示有 schedule trigger 在自動跑。回頭查 Active 開關 + trigger 節點設定，否則你跑出的數會跟自動跑的混在一起。

#### 4 個關鍵差異點 + LLM 對話應對

| 差異點 | Self-host | n8n Cloud | LLM 對話應對 |
|---|---|---|---|
| Credential 儲存 | 你電腦/VPS，自己備份 | n8n 雲端，n8n 加密 | LLM 給你「整份匯入」建議時，Cloud 用戶要追問「credential 部分我要重建嗎」 |
| 節點可用性 | 全部 community node 可用 | 部分受限 | LLM 建議 Read Binary File / Execute Command / LocalAI 等本地節點時，Cloud 用戶要說「我在 Cloud，這節點不能用，請改成 Google Drive Read File 等雲端節點」 |
| 檔案路徑 | `/files/` 等本機絕對路徑 OK | 不能直接讀本機 | LLM 給的 path（例：`/files/pdf-inbox/`），Cloud 用戶要說「我在 Cloud，請改成 Google Drive 路徑或 S3 bucket」 |
| Execution 配額 | 無上限（吃自己資源） | 月配額 | 全量跑前先估算（例：200 張 × 每張呼叫 1 次 Gemini = 200 次 execution），看是否超 plan 上限 |

#### 5 條真實驗收（每條配自評動作）

**第 1 條：能用 4 格便箋拆解一個改造需求**
- 自評動作：選一個你還沒做的 Lite Pack workflow（例：#04），花 5 分鐘填 4 格便箋，然後對著手機錄音講 1 分鐘
- 過關：4 格全填具體值（input 有 4-6 個欄位名）+ 講話沒打結

**第 2 條：能在不貼 credential 的前提下把 JSON 給 LLM**
- 自評動作：從 n8n UI export 任一 workflow → 用 VS Code 搜尋 4 個字串（apiKey/accessToken/password/token）
- 過關：4 個字串全部 0 個結果

**第 3 條：能讓 LLM 只回節點區段、不重寫整份**
- 自評動作：對 LLM 貼模板 3，要求改某個節點 → 看 LLM 回的 JSON 第二行
- 過關：第二行是 `"parameters":`（不是 `"name":` 或 `"nodes":`）

**第 4 條：能用三件套格式回報錯誤**
- 自評動作：故意製造一個錯誤（把 #02 的 Code 節點 prompt 字串隨便刪掉幾行）→ 跑紅燈 → 用模板 4 回報
- 過關：LLM 給的回應指出「具體哪一行哪個欄位」（不是「建議重新檢查」）

**第 5 條（硬指標）：把 #02 改成處理某種非合約類文件並跑通 10 筆**
- 自評動作：選一種文件類型（發票 / 收據 / PO / 申請表 4 選 1），照第 6 章 walkthrough 跑完整六步
- 過關 3 條：(a) 10 張全綠燈 (b) 10 張的 newFilename 全部符合便箋格式 (c) 0 張 null 欄位
- **強烈建議**：跑通後到課程社群貼 Finder 截圖（10 張改名後的 PDF）— 這也是給未來其他學員的參考

#### 進階練習 2 題（不給答案，給「過關條件」）

**練習 1：把 #04-daily-ai-report 的輸出端從 Google Sheet 改成 Notion Database**
- 過關 5 條（不給做法，自己用 6 步流程解）：
  - (a) 4 格便箋有「目標 Notion Database 的 schema」具體欄位名
  - (b) 用「示範形狀法」在 n8n UI 上拉 Notion 節點 → 隨便填 → 複製 JSON → 貼給 LLM 當形狀範本（不讓 LLM 從記憶生成）
  - (c) 整套流程用 -edit 版做，不動原 #04
  - (d) 跑通 5 筆測試 daily report
  - (e) 在 Notion Database 看到 5 筆有結構的 record（不是 5 條空白 row）

**練習 2：把 #11-csv-clean-score 的評分維度從通用版改成你業務的特定維度**
- 過關 5 條：
  - (a) 4 格便箋有「你業務的特定維度」清單（至少 3 個維度）
  - (b) 對比原 #11 的通用維度，明確標出哪些保留 / 哪些換掉 / 哪些新增
  - (c) 只改 Code 節點裡的 prompt + 評分邏輯，不改 trigger / 不改輸出端
  - (d) 跑通 10 筆真實 CSV 樣本
  - (e) 抽查 3 筆 output 的評分結果，肉眼看分數合不合理

### 4. 完整範例 prompt 模板

#### 環境感知 prompt prefix（每次對話開頭加）

```
我用 n8n [Cloud / self-host with Docker / self-host with Cloudflare Tunnel]，n8n 版本 [latest / 1.x.x]。
我的工作流程是 [改造目的]。

[後面接其他 prompt 模板]
```

這樣 LLM 一開始就知道你的環境，不會建議 Cloud 用戶用 Read Binary File。

### 5. 範例 LLM 回應

環境感知 prompt 的 sample 回應：

```
明白，你在 n8n Cloud 上，所以我會避免建議：
- Read/Write Files 節點（用 Google Drive 替代）
- Execute Command 節點（不可用）
- 本機絕對路徑（用 Google Drive folder ID 或 S3 bucket）

進行你的改造需求 [...]
```

### 6. 驗收標準

整本系列（8 章）讀完 + 動完後過關：

- [ ] 我知道我在哪個環境（Cloud / self-host）
- [ ] 我能說出 4 個關鍵差異 + 對應的 LLM 應對
- [ ] 我能用 5 條自評動作驗證自己學到了什麼
- [ ] 我做完第 5 條硬指標（10 張跑通）
- [ ] 我選了 1 個進階練習開始試（即使還沒跑完）

### 7. 常見錯誤 + 怎麼解

**錯誤 1：「我看了 5 條驗收，但我跑不通第 5 條」**
- 解：去第 7 章看分流。如果還是不行，貼求救範本到課程社群。第 5 條是硬指標 — 不過關不能說「我學會了」

**錯誤 2：「我練習 1 完了，但 Notion Database 跑出來欄位都對不上」**
- 解：(b) 那條沒做好。回到 n8n UI 拉 Notion 節點 → 隨便填 → 複製出來給 LLM。這個「示範形狀法」是非工程師繞開 typeVersion 雷區的關鍵

**錯誤 3：「我在 Cloud 上想做練習 1，但卡在 Notion API 設定」**
- 解：Notion API 設定屬於另一個課題（不是本系列範圍）。可以查 Notion 官方文件 / google「Notion integration setup」 / 課程社群求救

### 8. 回到課程動線

- **跑完 5 條驗收**：分享到課程社群，看其他人的進度
- **想再進階**：練習 1 + 2 → 再挑 #03 / #05 / #07 等其他 workflow 自己改
- **遇到新錯誤**：回第 7 章分流 / 第 5 章紅線

### 9. 對現有 HTML 的具體變更

| 動作 | 原 line | 改成 |
|---|---|---|
| 新增 | self-host vs Cloud 對照表前 | 加 30 秒環境判別法（看網址列 3 種模式） |
| 新增 | 4 個差異點對照表後 | 加「LLM 對話應對」一欄（Cloud 用戶看到 LLM 建議什麼節點要怎麼追問） |
| 改寫 | 213-216 callout | 砍掉空話 callout，換成具體例：「LLM 建議 Read Binary File / Execute Command / LocalAI — Cloud 用戶要說『請改成 Google Drive Read File』」 |
| 改寫 | 237-243 5 條驗收 | 每條配「自評動作」(具體 5 分鐘可做) + 「過關標準」(可量化驗收) |
| 改寫 | 256-265 進階練習 2 題 | 各加「過關 5 條」清單（不給答案但給驗收標準） |
| 新增 | 章末 | 加「環境感知 prompt prefix」模板（每次對話開頭加，LLM 會自動避坑） |
| 保留 | 274-277 系列結語 | 保留，雞湯但無害 |


---

<a id="phase-c"></a>

---

## 設計記錄（Phase A 診斷）

本章原始 HTML 章節的「空話」診斷清單，作為重設計的問題對應表：

### 第 8 章 post-llm-8-environment — 環境互鎖與自我驗收

**整體判定**：對照表內容紮實，4 個差異點寫得清楚。但**自我驗收的 5 條清單**和**進階練習 2 題**整體是判定 1+2（給目標但沒給「自評通過的具體標準」）。第 5 條叫「硬指標」但仍模糊：「跑通 10 筆樣本」——10 筆全綠燈算？還是包含 output 內容檢查？

| # | line | 原文摘要 | 違反 | 為什麼會卡住學員 |
|---|---|---|---|---|
| A8-1 | 167-211 | self-host vs Cloud 對照表 | (具體度尚可) | 這部分相對好。唯一可加：「我怎麼知道我在哪個？」——應該在表前加 30 秒判別法：「打開 n8n UI 看左下角，如果是 `https://yourdomain.app.n8n.cloud` 就是 Cloud；如果是 `localhost:5678` 或 `xxx.cloudflare.com` 就是 self-host」 |
| A8-2 | 213-216 | callout「改 workflow 前，先確認你跑在哪個環境。同一份 LLM 改寫建議，在 self-host 與 Cloud 上適用程度不同」 | 1 | 廢話 callout，整段重述前段標題。砍掉或換成具體例：「LLM 給你的建議裡如果出現『Read Binary File』、『Execute Command』、『LocalAI』 — 這三個節點 Cloud 跑不了，要追問 LLM『我在 Cloud 上，這三個節點不能用，請改用 Google Drive Read File』」 |
| A8-3 | 222-225 | 「進一步閱讀」連結到 post-cloud-n8n.html | 4 | 該頁是否存在？是否在學員看到的 8 頁範圍？如果是「補充教材」，應該明說「這頁是選讀，不影響主線」 |
| A8-4 | 237-243 | 5 條驗收清單，第 1-4 條「能用 4 格便箋拆解」「能在不貼 credential 前提下…」「能下指令讓 LLM 只回傳節點區段」「能用最小可重現訊息格式回報錯誤」 | 2 | 4 條都寫成「能 X」但**沒給自評動作**。應該每條配「自我測試題」：「給你看一個亂改 workflow 的 prompt，你能不能指出哪一格 4 格便箋是空的？」這種可在 5 分鐘內驗的小測 |
| A8-5 | 242 | 第 5 條「能把 #02-pdf-ai-rename 改成處理某種非合約類文件」+「跑通 10 筆樣本」 | 2 | 「跑通 10 筆」具體：(a) 10 筆都綠燈 (b) 10 筆 output 的檔名格式都符合 (c) 沒有 null 欄位。應該明列驗收 3 條，學員自己核對 |
| A8-6 | 256-265 | 練習 1「把 #04 的輸出端從 Sheet 改成 Notion」+ 練習 2「把 #11 評分維度改成你業務的特定維度」 | 1, 2 | 兩題只給題目和一句提示。商業培訓學員大多不會做「不給答案的題目」——他們會打開 LLM 直接問，但沒有題目的「正解動線」就無法自我驗收。應該給「過關條件」清單（不給答案，但給「你做出來的東西要符合哪 3 條才算過」） |
| A8-7 | 274-277 | 系列結語「這套流程的核心不是 prompt 技巧，是『縮小範圍、逐步驗收』的工作紀律——第一次走完 6 步可能要花一個下午，第五次就會變成 30 分鐘的例行作業」 | (尚可，雞湯但無害) | 不算空話，是收尾。可保留 |

**第 8 章空話小計：6 條**（A8-7 不計）

---
