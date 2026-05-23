---
slug: gemini-notebooklm-workshop
unit_id: CH0
title: 兩工具切換決策入口（含跨來源預告）
course_type: skill-operation
duration: 25 min
learning_objective: 能用兩工具信任模式對比答對 ≥5/6 切換決策題，能說出 3 條免費版紅線，能帶著 decision checkpoint 意識進入後續案例
prerequisites: [office-ai-cases]
style_guide: _outlines/gemini-notebooklm-workshop.style-guide.md
platform_version: 2026-Q2（Gemini 免費版 / NotebookLM 免費版）
---

<!--
CH0 v2（覆寫 v1，2026-05-23）。功能：建立「兩工具信任模式分流」+「decision checkpoint 機制」+「跨來源整合預告」+「3 條免費版紅線」。
v1 的「5 失敗模式 / 3 條通用資安紅線 / AI 運作原理」office-ai-cases 已教，本檔不重講。
本課 8h 工作坊（2 天 × 4h）整個教學設計依賴 CH0 把「信任模式」講清楚，後面 CH1-1 ~ CH2-1 每 CH 開場 3 min decision checkpoint 都會回頭問。
-->

## 教學流程（Teaching Flow · 25 min）

### 1. 破題 / Hook（4 min）

上次 office-ai-cases 6h 你已經學過 AI 運作 / Token / Hallucination / Prompt 5 大骨架 / 5 失敗模式 / 風險 4 條。**這些本課不重講。**

本課 8h 重點只有一條：**什麼時候不能直接問 Gemini、要先去 NotebookLM 取證**。

延續上次的故事——

> 業務副理小李上次用 ChatGPT 寫客戶提案，被客戶抓出「業績成長 38%」是 AI 自己編的、實際只成長 12%。
>
> 這週小李改用 Gemini 寫，結果同一個問題又出現。他來問：「我都加了『不要編造』的 prompt 了，怎麼還會這樣？」
>
> 答案是：**不是 prompt 問題，是工具選錯了**。要數字、要追溯來源的場景，**從一開始就不該丟 Gemini**。

這 25 min 把「兩工具信任模式」與「6 題切換決策」講清楚，後面 5 個案例（會議 / 知識庫 / 競品 / 彙報壓力測試 / 跨來源綜合）每個開場 3 min 都會回頭問你切換決策。

### 2. 信任模式對比 / Trust Model（8 min）

核心觀念一句話：

- **Gemini 的信任模式 = 生成優先**。沒給資料時它會「合理推估」、看起來像答案、其實是編的。強在生成 / 改寫 / 推演。
- **NotebookLM 的信任模式 = 來源優先**。沒上傳來源時它直接拒答。強在引用 / 限定範圍 / 降幻覺。

#### Demo A：同一問題丟 Gemini（沒給資料）

<div class="dialog-box">
  <div class="dialog-label">小李在 Gemini</div>
  弄一下精選商行 12 月電商業績是多少？
</div>

<div class="expected-output">
  <div class="expected-label">Gemini 大概會回</div>
  <div class="expected-body">
    <p>依產業平均推估，12 月（雙 12 + 年末檔期）電商業績通常較 11 月成長 15-25%。</p>
    <p>若以一般中型電商月營收 200-500 萬計算，弄一下精選商行 12 月可能落在 <strong>230-625 萬</strong>區間。建議參考前 3 個月趨勢做更精準推估。</p>
  </div>
  <div class="expected-note">實際輸出每次略有差異。重點是：Gemini 在沒資料時會給「聽起來合理」的數字。這就是 hallucination 風險的來源——它不是不知道、是預設要給有用回答。</div>
</div>

#### Demo B：同一問題丟 NotebookLM（沒上傳 source）

<div class="dialog-box">
  <div class="dialog-label">小李在 NotebookLM（無 source）</div>
  弄一下精選商行 12 月電商業績是多少？
</div>

<div class="expected-output">
  <div class="expected-label">NotebookLM 大概會回</div>
  <div class="expected-body">
    <p>我無法回答這個問題。我只能從你上傳的來源資料找答案。</p>
    <p>目前這個 notebook 沒有任何來源。請上傳相關文件（如訂單明細、月報表）後再問。</p>
  </div>
  <div class="expected-note">實際輸出每次略有差異。重點是：NotebookLM 的核心設計是「不上傳就不答」。這是降幻覺的保險，也是它的核心邊界。</div>
</div>

#### Demo C：上傳 100 筆訂單 CSV 再問 NotebookLM

<div class="dialog-box">
  <div class="dialog-label">小李在 NotebookLM（已上傳 ecom-orders-100.csv）</div>
  弄一下精選商行 12 月電商業績是多少？Top 3 SKU 是哪幾個？
</div>

<div class="expected-output">
  <div class="expected-label">NotebookLM 大概會回</div>
  <div class="expected-body">
    <p>依 ecom-orders-100.csv 統計，12 月電商業績為 <strong>NT$ 245,800</strong>，含 100 筆訂單。</p>
    <p><strong>Top 3 SKU：</strong>SKU-A（佔 18%）/ SKU-B（佔 12%）/ SKU-C（佔 8%）。</p>
    <p>【引用：訂單明細第 1-100 筆】</p>
  </div>
  <div class="expected-note">實際輸出每次略有差異。重點是：有來源 → 有引用 → 可追溯。這是 Gemini 換不到的價值。</div>
</div>

<div class="callout-box">
  <strong>信任模式 takeaway</strong>：Gemini 像隨叫隨到的萬能助理，缺資料會自己腦補；NotebookLM 像龜毛圖書館員，沒書就說沒書。**你要的是哪一種，先決定再開工。**
</div>

### 3. 6 題切換決策樹 / Decision Tree（7 min）

下面 6 題情境，每題選「**Gemini / NotebookLM / 兩個都不行（用 Excel）**」，與旁邊同學對答案，3 min 後講師揭曉。

| # | 情境 | 你選 |
|---|------|------|
| 1 | 把 30 分鐘跨部門會議逐字稿轉成 1 頁行動清單 | ? |
| 2 | 從公司 20 份 SOP 找「年假怎麼請」、要能引用條文 | ? |
| 3 | 把 100 筆業績 CSV 算出 Top 3 客戶 | ? |
| 4 | 改寫提案信讓語氣更專業 | ? |
| 5 | 把 5 篇分析師報告整理成 1 頁主管簡報、要標來源 | ? |
| 6 | 算「12 月預算執行率超過 110% 的部門」 | ? |

**講師揭曉答案**：

| # | 答案 | 為什麼 |
|---|------|--------|
| 1 | **Gemini** | 生成新內容（行動清單）+ 非結構文字 + 不需逐字追溯來源 |
| 2 | **NotebookLM** | 限定 20 份 SOP 找答案 + 要引用條文 = 信任模式必須 source-first |
| 3 | **Gemini**（但要驗證加總） | 生成 + 摘要 OK，但**算數要回 Excel 對加總** |
| 4 | **Gemini** | 改寫 / 潤稿是它最強項，沒有追溯需求 |
| 5 | **NotebookLM** | 5 篇來源 + 要標來源 = source-first 場景，且引用是 NotebookLM 招牌 |
| 6 | **兩個都不行** | 算數學 + 邊界判斷（>110%）= 用 Excel 樞紐，AI 容易算錯小數點 |

對答案標準：≥ 5 題對 = 過。第 6 題最常被誤選 Gemini，記住「算數 + 邊界規則」優先回試算表。

**進階版 2 題（課後素材包附錄、不在課堂跑）**：

- 進階 1：用 5 篇 NotebookLM 來源建主管簡報初稿（生成）→ 主管追問「第 3 條第二句的引用」（追溯）。請排切換順序。
- 進階 2：客戶來信問「我們去年合作金額」，你手上有 ERP 匯出檔。請排切換順序。

### 4. Decision Checkpoint + 跨來源預告 + 3 條免費版紅線（4 min）

#### Decision Checkpoint 機制（1 min）

從 CH1-1 開始，**每個 CH 開場 3 min 我會回頭問你**：「這個案例為什麼用 Gemini 不用 NotebookLM？」或反過來。問題就在這 6 題的延伸。

意思是這 25 min 學的「信任模式 + 切換決策」會被反覆練習 5 次。**離場前能答對 ≥ 5/6 題就足夠進下一單元。**

#### 跨來源預告（1 min）

本課 5 個案例（CH1-1 / CH1-2 / CH1-3 / CH1-4 / CH2-1）的**壓軸是 CH2-1 跨來源綜合彙報**——把 NotebookLM 多來源取證 + Gemini 跨源整合推到極致。

從 CH0 就開始留意：「**這個案例做出來的東西，CH2-1 能怎麼用？**」每個案例的「結果驗證卡」最後一欄就是這條伏筆。

#### 3 條免費版紅線 + 3 大現實阻力（2 min）

不重講通用資安（office-ai-cases CH0 已教，客戶名 / 員工身分 / 機密合約不能丟免費版這條一句帶過）。**本課只講「免費版會在哪邊撞牆 + 回部門會撞到的 3 大現實阻力」**：

**3 條免費版紅線（技術層）**：

| # | 紅線 | 撞牆位置 |
|---|------|---------|
| 1 | **Gemini 免費版 context 限制** | 約 32K token（中文約 16K 字 / 30 頁 A4）。貼整本 PDF 會被截斷，但 Gemini **不會明說已截斷**，會照常作答 → 你以為它讀完了、其實只讀前段。**對策**：超過 30 頁的文件改用 NotebookLM。 |
| 2 | **NotebookLM 免費版 source 上限** ⚠ | 每個 notebook **source 上限約 50 個 / 單檔上限約 200MB**（2026-Q2 實際值以官方為準，可能微調）。超過要分 notebook 建。**對策**：CH1-2 三層知識庫設計時會教如何拆 notebook。 |
| 3 | **隱私邊界（一句帶過）** | 客戶名 / 員工身分 / 機密合約**不能丟免費版**——office-ai-cases CH0 已詳細講過，本課不重展開。課堂全用 sample data。 |

**3 大現實阻力（職場層）**——比免費版限制更會擋住學員回部門用 AI：

| # | 阻力 | 怎麼辦 |
|---|------|--------|
| A | **公司資安可能完全禁止上傳真實資料到免費版** | 不確定就**立刻停下來問公司資安**。實在不能上：(1) 用 sample 模擬建 notebook 練流程 (2) 用內部 wiki 公開段（FAQ / 政策）當第一個 source (3) 需要真資料就升級 💰 NotebookLM Plus / 公司核可內部 AI。CH1-2 / CH2-1 會具體示範對策。 |
| B | **公司 SOP / 政策沒有版本管理** | 你會不知道哪份是「最新核可」。對策：用「**最後修改日期 + 修改人**」當代替（檔名加 `_LMD-2025-12`），不確定就標 ⚠「**本 source 版本未明，僅供查詢參考**」。NotebookLM 不是公司文件管理系統，**只是把混亂變成可搜尋的混亂**。 |
| C | **主管不買單 NotebookLM 引用** | 主管追問會問：「**這是不是我們 ERP 的數字？**」NotebookLM 引用 = 外部行業參考、不等於公司正式系統來源。對策：彙報時**明確標「公司內部系統來源」vs「外部行業參考」**——前者用 ERP / CRM / 採購系統的編號，後者用 NotebookLM 引用位置。CH1-4 會深入教 ERP 接回。 |

<div class="callout-box">
  <strong>⚠ 數值校正 + 阻力預告</strong>：3 條紅線的具體數字（32K context、50 source、200MB）是 2026-Q2 當時值，平台會調，回家用前先看官方。3 大現實阻力中**阻力 A 在 CH1-2 細講對策、阻力 B 在 CH1-2 細講對策、阻力 C 在 CH1-4 細講 ERP 接回**——這些不是課程加分項，是學員回部門能不能真的用得起來的關鍵。
</div>

### 5. 檢核 / Verification（2 min）

**離場自查卡（離場前打勾）**：

- [ ] 我能用一句話說 Gemini 信任模式（生成優先 / 沒資料會編）vs NotebookLM 信任模式（來源優先 / 沒上傳不答）
- [ ] 6 題切換決策樹我至少答對 5 題
- [ ] 我知道 CH1-1 ~ CH2-1 每個 CH 開場 3 min 會 decision checkpoint 問我切換決策
- [ ] 我有意識到 CH2-1 跨來源綜合彙報是壓軸，要留意每個案例的輸出能否餵給 CH2-1
- [ ] 我能說出 3 條免費版紅線中的至少 2 條（32K context / 50 source / 隱私邊界）
- [ ] 我能說出 3 大現實阻力中的至少 1 條（資安禁上傳 / SOP 沒版本 / 主管要 ERP 數字），並知道課程後段哪個 CH 會教對策

打勾 ≥ 5 條 = 過，可進 CH1-1。

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：skill-operation

### 連線設定（Credential）所需

- Gemini 免費版（任一 Google 帳號）
- NotebookLM 免費版（同 Google 帳號可登）
- 學員需在開課前 1 週確認公司網路可登入兩個平台
- 不需付費版

### Sample Dataset

- `ecom-orders-100.csv`（100 筆訂單、含 SKU / 金額 / 日期，與 CH1-4 共用）— Demo C 上傳 NotebookLM 用

### Prompt 集

- 3 套對比 prompt（Demo A / B / C 同一問題、不同工具 / 來源狀態）
- 6 題切換決策題（基礎版 + 預期答案揭曉表）
- 2 題進階切換題（課後素材包附錄、不在課堂跑）

### 帶走項

- 兩工具信任模式對比 1 頁速查表
- 6 題切換決策樹 + 預期答案（含為什麼）
- 進階 2 題（課後練習）
- 3 條免費版紅線速查（含 ⚠ 數值需校正提醒）

---

## 商業情境案例（Case）

**主角**：小李（32 歲業務副理 · 弄一下精選商行）

**任務銜接**：上次 office-ai-cases 用 ChatGPT 出包了「業績成長 38%」幻覺，這次小李換 Gemini 又踩同樣坑。他來問課堂：「不是加了『不要編造』prompt 就好嗎？」

**本單元要他學會**：

1. 認清這不是 prompt 問題、是工具選錯了——**有些場景從一開始就不該丟 Gemini**
2. 用「信任模式」一詞分辨兩工具差異（不只是「功能不同」）
3. 用 6 題決策樹判斷自己當下任務該用哪個
4. 帶著「decision checkpoint 機制」進入後續 5 個案例、知道每 CH 開場會被回頭問
5. 認識 3 條免費版會撞牆的紅線（context / source 上限 / 隱私邊界）

---

## 動手練習題（Hands-on Exercise）

**題目**：以小李的處境為基底，跑兩個動手：

**動手 ①**：6 題切換決策樹（同上方第 3 段）。與旁邊同學 3 min 對答案，講師揭曉。

**動手 ②**：拿你自己手上下週要做的 1 件事（例：寫週報 / 算業績 / 找 SOP / 整理競品 / 補主管追問），先自己判斷該用 Gemini 還是 NotebookLM，**寫一行為什麼**。CH1-1 開場會被點到分享。

**預期成果**：

- 動手 ① ≥ 5/6 題對
- 動手 ② 能說出選擇的「信任模式判斷依據」（生成 vs 追溯、有來源 vs 沒來源）

**完成標準**（self-check）：

- [ ] 6 題對 ≥ 5 題
- [ ] 至少 1 題能說出「為什麼這題不用另一個工具」
- [ ] 找到第 6 題（兩個都不行）的關鍵：算數 + 邊界判斷優先回 Excel
- [ ] 動手 ② 寫出 1 行「信任模式判斷依據」

---

## 常見錯誤 3 條（Common Pitfalls）

### 1. 以為加「不要編造」prompt 就能讓 Gemini 不幻覺

**錯誤現象**：學員從 office-ai-cases 帶走 prompt 技巧，加了「如果你沒有相關資料，請說『沒有資料』」結尾，以為這樣 Gemini 就不會編。實際跑下去發現 Gemini 還是給了「合理推估」。

**原因**：Gemini 的預設訓練目標是「給出有用回答」，這個傾向比 prompt 指令還強。**信任模式是設計層的事，prompt 改不動。**

**解法**：要追溯來源的任務**從一開始就改用 NotebookLM**。不是 prompt 寫得更好就能解、是工具選錯了。

---

### 2. 以為 NotebookLM 上傳就一定準

**錯誤現象**：上傳 20 份 SOP 後問「年假怎麼請」，NotebookLM 給答案 + 引用，學員看到引用就相信、不點開原文核對。結果引用的是「特休」段落、不是「年假」段落，回答方向錯了。

**原因**：NotebookLM 引用機制基於「文字片段相似度」，不保證引用段落真的回答了問題。**有引用 ≠ 引用正確**。

**解法**：(1) **點開引用段落原文核對**（不要只看摘要）(2) 確認上傳的 SOP 是最新版（檔名日期 / 問人資）(3) CH1-2 三層知識庫會教如何用「source selection」降低錯引機率。

---

### 3. 把整本 200 頁 PDF 直接貼進 Gemini 對話框

**錯誤現象**：學員想偷懶、把整本員工手冊 PDF 內容貼進 Gemini 問問題，Gemini 照常作答，看起來很順、但答案常常和手冊內容對不上。

**原因**：Gemini 免費版 context 約 32K token（中文約 16K 字 / 30 頁 A4）。**超過會被截斷、但它不會明說已截斷**——你以為它讀完了、其實只讀了前 30 頁。

**解法**：(1) 超過 30 頁的文件**改丟 NotebookLM**（NotebookLM 上限約 200MB / 50 source、容得下整本手冊）(2) 若一定要用 Gemini，先用 Excel / Word 拆段、一次貼一段問 (3) 💰 Gemini Advanced 有 1M context，付費版可吃整本——但本課不依賴付費版。

---

## 檢核題 2 條（Quiz）

**Q1（信任模式驗證）**：以下哪個說法**最準確**描述 Gemini 與 NotebookLM 的核心差異？

- [ ] A. Gemini 比 NotebookLM 聰明、回答更詳細
- [ ] B. Gemini 是「生成優先 / 沒資料會推估」，NotebookLM 是「來源優先 / 沒上傳不答」 ←（**正確答案**）
- [ ] C. NotebookLM 適合中文、Gemini 適合英文
- [ ] D. Gemini 是免費版有 hallucination，付費版就不會

**Q2（應用驗證）**：

**情境**：你是凱倫（30 歲財務專員、弄一下精選商行）。主管要你「**列出 2026 Q1 三家子公司的營收佔比**」。你手上只有 2 家子公司財報 + 1 份產業分析報告，第 3 家公司資料還在等。下面 4 個做法，哪個**最危險**？為什麼？

- A. 用 NotebookLM 上傳已知 2 家財報 + 產業分析，問「請依現有來源整理佔比，缺的標『資料未到』」
- B. 用 Gemini 問「2026 Q1 一般中型企業三家子公司營收佔比通常落在多少」
- C. 跟主管講「第 3 家資料還沒到，先給你前兩家、缺的補上後再合併」
- D. 用 Excel 自己依 2025 Q4 比例 × 季節調整係數推估第 3 家

**預期答案要點**：

- **最危險：B**。Gemini 會給看起來合理的「業界平均佔比」（例如 50% / 30% / 20%），主管可能**直接拿去用、看起來像答案**——但這些數字**和弄一下精選商行的子公司毫無關係**，是純編造。對應「信任模式錯配」：要的是具體公司數字、卻用了生成優先的工具。
- A 是正解：信任模式對齊（要追溯 → NotebookLM）+ 明示資料缺口
- C 是最穩做法：誠實回報
- D 是「用 Excel 自己估」，邏輯透明、可解釋，至少能跟主管說清楚怎麼估的
- 加分：能說出「**最危險的不是錯得最離譜的、而是看起來最像答案、最容易被主管拿去用的**」
