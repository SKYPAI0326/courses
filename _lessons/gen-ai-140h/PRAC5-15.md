---
slug: gen-ai-140h
unit_id: PRAC5-15
title: 自貼 API KEY 的 AI 工具（自用 demo 版）
course_type: skill-operation
duration: 1.5h 課堂 / 1h 自學
learning_objective: 學員能用提示詞讓 AI 產出單檔 HTML AI 工具（前端輸入 API KEY 暫存於 sessionStorage），部署到 GitHub Pages 形成自用 demo，並明確認識「自用版 vs 可分享版」的邊界
prerequisites: [CH5-5, PRAC5-13]
platform_version: "2026-05"
---

<!--
PRAC5-15 教案（自貼 API KEY 的 AI 工具 — 自用 demo 版）
重點：定位（自用 demo / 不可分享）+ 安全教育 + Google AI Studio 申請 KEY 流程
傻瓜模式 + 安全教育並重
與 PRAC5-3 差異化：PRAC5-3 練「API 串接機制」，本單元練「KEY 不進 repo + 自用部署的邊界認識」
時數：90 分鐘課堂 + 60 分鐘自學
要分享版請看 PRAC5-17（Phase 2 上線後）
-->

## 教學流程（Teaching Flow）

> 🚨 **本單元產出的是「本機/自用 demo」，不適合分享給他人使用。**
> 
> 若想做可分享的版本（朋友打開不用自己貼 KEY 就能用），請看 **PRAC5-17**（Phase 2 完成後上線）。

---

### 你會練到的能力

> **本單元練「KEY 不進 repo 的習慣 + 自用部署的邊界認識」**：
> - 學會在「**寫死 KEY 進程式碼**」與「**讓使用者前端貼 KEY**」這兩個方案中、選對方案
> - 學會在 Google AI Studio 申請 API KEY、設定 referrer 安全限制
> - 學會在自部署網頁上呼叫 AI API 看到真實回應
> - **學會自我克制**：完成自用 demo 後，知道「**我能用、不能分享**」這條界線
> 
> 學完今天，你會在 90 分鐘內擁有一個**只有你自己能用**的 AI 工具（如提示詞優化器、翻譯小幫手）部署在 GitHub Pages。
> 
> **跟 PRAC5-3「API 串接展示頁」不同的是：** PRAC5-3 練「API 串接機制」（fetch 怎麼跑、回應怎麼處理），本單元練「**安全意識為主軸、技術為輔**」—— KEY 怎麼安全地進入網頁、為什麼不能寫死、為什麼不能分享。

---

### 破題 / Hook（3 分鐘）

行政小陳這週做了個人單頁、做了同事姓名遊戲，**信心爆棚**。

她想到一個自己每天都會用的東西：「**我每次寫 ChatGPT 提示詞都覺得寫得太粗、想要有個工具幫我改得更具體**。」

她在群組問：「你們有什麼提示詞優化工具推薦？」朋友丟了幾個 SaaS 連結，每個月要 $10 美金、要訂閱、要登入。

她突然想：「**這種小工具，我自己用 AI 做一個不就好了？而且不用月費**。」

她貼提示詞給 Claude → Claude 給她一個單檔 HTML、頁面有輸入框可以貼她的 Gemini API KEY → 部署到 GitHub Pages → 上班打開、貼 KEY、貼粗略提示詞、按優化 → 看到 AI 給她改寫得更具體的版本。

**問題來了**：她想分享給組長用。**這時候紅燈響起來**：

> 「**這個工具能不能分享給別人？**」

答案是：**不能，至少這個版本不行**。

這 90 分鐘要教你的，**不只是做出工具**（這部分跟前兩個 PRAC 一樣快），**還要教你「為什麼這個工具不能分享」+ 「想分享要怎麼辦」的安全意識**。

---

### 重要 / 自用 vs 可分享的邊界（5 分鐘）

> 💡 **這頁是本單元最重要的觀念。讀完再往下。**

#### 三種 AI 工具的部署形態

| 形態 | 誰來付 AI 帳單？ | 安全嗎？ | 適合什麼？ |
|------|---------------|---------|----------|
| **A. KEY 寫死在程式碼裡** | 你（網頁的擁有者） | ❌ **超不安全** | 永遠不要做 |
| **B. 使用者前端貼 KEY** | 訪客自己付 | ⚠️ **只有自用安全** | 自用 demo（本單元） |
| **C. KEY 藏在後端 proxy** | 你（網頁擁有者） | ✅ 安全 | 可分享給朋友 |

**為什麼 A 永遠不做？**

把 KEY 寫進 HTML / JS → 推到 GitHub Pages → **任何人按右鍵「檢視原始碼」都能看到你的 KEY** → 24 小時內你的 Google AI Studio 額度被刷爆、信用卡被刷錢。**這條死路有人走過，你別重蹈覆轍**。

**為什麼 B 只有自用安全？**

你做的工具部署上 GitHub Pages、頁面有個輸入框讓使用者貼 KEY → 你自己用沒問題（KEY 是你的、你貼進去 sessionStorage 暫存、關掉分頁就沒了）。

**但如果你分享連結給組長**：
- 組長把他自己的 KEY 貼進去 → KEY 在組長的瀏覽器 sessionStorage 裡 → **理論上**只有組長自己能看到
- **但是**：你之後改頁面 JS（例如加一個 bug、或不小心 console.log KEY 把 KEY 印到日誌）→ 組長的 KEY 就可能洩漏
- **而且**：組長不會檢查你的程式碼有沒有 bug、他信任你 → 出事**你扛責任**

> 💡 **規則：自用 demo 自己用 OK，但不要分享連結讓別人貼 KEY。要分享請做 C（Phase 2 的 PRAC5-17 會教）。**

**為什麼 C 才安全？**

PRAC5-17 會教用 **Vercel Functions 代理** —— KEY 藏在 Vercel 後端、訪客看不到、訪客不用自備 KEY、你付 AI 帳單（但 Vercel 免費額度通常夠）。**這才是可以分享的版本**。

> 💡 **今天的本單元學的是 B**。**結束前我們會明確說：完成的工具不能分享連結讓別人貼 KEY**。

---

### 概念 / 提示詞卡（5 分鐘）

兩個範例**任挑一個**跑完整流程。

#### 範例 A — AI 提示詞優化器

```
請用單一 HTML 檔做一個 AI 提示詞優化器。要求：
- 頁面上方放一個 <input type="password"> 讓使用者貼 Gemini API KEY
- KEY 用 sessionStorage 暫存（關掉分頁就消失），絕對不要寫進程式碼
- 下方一個 textarea 讓使用者貼粗糙的提示詞
- 一個「優化」按鈕，按下去呼叫 Gemini API（model: gemini-2.0-flash）
- 把粗糙提示詞改寫得更具體（指定角色、任務、限制、輸出格式）
- 結果顯示在下方另一個 textarea，可一鍵複製
- 頁面醒目位置加紅字警告「此頁僅供你自己使用，請勿分享連結讓他人貼 KEY」
- 介面米白底、簡潔現代
- API 錯誤要顯示具體訊息（不要只說「壞了」）

請先回我「請貼上你的資料」這句話確認你看懂任務（不需要我貼任何資料、直接給我完整 HTML）。
```

> 💡 此處「先回我」是為了確認 AI 真的理解任務 —— 部分情況下 AI 會跳過確認直接給程式碼，這也 OK。

---

#### 範例 B — 翻譯小幫手

```
請用單一 HTML 檔做一個翻譯小幫手。要求：
- 頁面上方 <input type="password"> 讓使用者貼 Gemini API KEY
- KEY 用 sessionStorage 暫存、絕對不寫進程式碼
- 兩個下拉選單：來源語言、目標語言（中英日韓泰越六選一）
- 一個 textarea 讓使用者貼要翻譯的文字
- 「翻譯」按鈕、呼叫 Gemini API（model: gemini-2.0-flash）
- 結果顯示在下方、可一鍵複製
- 加紅字警告「此頁僅供你自己使用，請勿分享連結讓他人貼 KEY」
- 介面米白底、簡潔現代

請直接給我完整 HTML。
```

> 💡 **建議現場示範用範例 A**（提示詞優化器、最實用）。

---

### 操作示範 / AI 對話完整示範（15 分鐘）

**講師現場跑一次範例 A**。用 **Claude Artifacts**（最穩、產出單檔最乾淨）。

#### 對話流程

**[學員]** （複製範例 A 提示詞、貼進 Claude Artifacts）

> [完整貼上述提示詞]

**[Claude Artifacts]**

> 好的，我看懂了。這是一個讓你自己貼 KEY、優化你自己的提示詞、且明確標示為自用 demo 的工具。給你完整 HTML：
> 
> ```html
> <!DOCTYPE html>
> <html lang="zh-TW">
> <head>
>   <meta charset="UTF-8">
>   <title>AI 提示詞優化器（自用版）</title>
>   <style>
>     body { background: #f5f3ee; ... }
>     .warning { background: #fee; color: #c00; padding: 12px; border-radius: 4px; }
>     /* ... */
>   </style>
> </head>
> <body>
>   <div class="warning">
>     ⚠️ 此頁僅供你自己使用，請勿分享連結讓他人貼 KEY
>   </div>
>   <h1>AI 提示詞優化器</h1>
>   <label>你的 Gemini API KEY（在 aistudio.google.com 申請）</label>
>   <input type="password" id="apiKey" placeholder="AIza...">
>   <label>原始提示詞（粗糙版）</label>
>   <textarea id="rawPrompt"></textarea>
>   <button onclick="optimize()">優化</button>
>   <label>優化後（複製這個用）</label>
>   <textarea id="result" readonly></textarea>
>   <button onclick="copyResult()">複製</button>
> 
>   <script>
>     // 從 sessionStorage 還原 KEY（同分頁內）
>     document.getElementById('apiKey').value = sessionStorage.getItem('GEMINI_KEY') || '';
>     document.getElementById('apiKey').addEventListener('input', e => sessionStorage.setItem('GEMINI_KEY', e.target.value));
> 
>     async function optimize() {
>       const key = document.getElementById('apiKey').value.trim();
>       const raw = document.getElementById('rawPrompt').value.trim();
>       if (!key) { alert('請先貼 API KEY'); return; }
>       if (!raw) { alert('請先貼原始提示詞'); return; }
>       const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${key}`;
>       const body = {
>         contents: [{ parts: [{ text: `請把這段粗糙的提示詞改寫得更具體（指定角色、任務、限制、輸出格式）：\n\n${raw}\n\n直接給我改寫後的版本、不要額外說明。` }] }]
>       };
>       try {
>         const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
>         const data = await res.json();
>         if (data.error) {
>           document.getElementById('result').value = `API 錯誤：${data.error.message}`;
>           return;
>         }
>         document.getElementById('result').value = data.candidates[0].content.parts[0].text;
>       } catch (e) {
>         document.getElementById('result').value = `網路錯誤：${e.message}`;
>       }
>     }
> 
>     function copyResult() {
>       const r = document.getElementById('result');
>       r.select();
>       document.execCommand('copy');
>     }
>   </script>
> </body>
> </html>
> ```

> 💡 **關鍵觀察**：
> - KEY 用 `<input type="password">`（輸入時看不到）+ `sessionStorage.setItem` 暫存
> - **程式碼裡沒有任何寫死的 KEY** —— 你 fork 這份 HTML 到 GitHub 是空 KEY 樣本
> - 紅字警告寫在頁面最上面

---

### 操作示範 / Google AI Studio 申請 KEY（15 分鐘）

**這段必教**。學員 80% 沒申請過 API KEY。

#### Step 1 — 開 Google AI Studio

> 動作：開 [aistudio.google.com](https://aistudio.google.com) → 用你的 Google 帳號登入

第一次登入會問「Choose a country」、選台灣、勾兩個 checkbox 同意服務條款 → Continue。

---

#### Step 2 — 申請 API KEY

> 動作：左側選單點 **Get API key**（鑰匙圖示）→ 右側點藍色按鈕 **Create API key**

跳出對話框：

> 動作：**Create API key in new project** → 選擇剛建好的 project（通常叫 `My First Project`）→ Create

**畫面跳到：** 一個 `AIza...` 開頭的長字串。**這就是你的 KEY**。

> 動作：點右邊的「複製」圖示 → KEY 進剪貼簿

> 🚨 **重要：** 這把 KEY 只會顯示一次。**現在馬上**：開一個記事本貼上、或用 1Password 之類密碼管理器存起來。等下要用。

---

#### Step 3 — 設 referrer 限制（額外安全層）

> 💡 **這一步可選但強烈建議做**。會多一層防護：就算 KEY 不小心外流、別人也不能在他自己的網域用你的 KEY。

> 動作：在 Get API key 列表中找到你剛建的 KEY → 點旁邊的 **Edit API key** → 設定頁

設定畫面：

> 動作：
> 1. **API restrictions** 區 → 選 **Restrict key**
> 2. 下拉選 **Generative Language API**（讓這把 KEY 只能呼叫 Gemini API、不能呼叫其他 Google Cloud 服務）
> 3. **Application restrictions** 區 → 選 **HTTP referrers (web sites)**
> 4. **Add an item** → 填 `https://{你的 GitHub 帳號}.github.io/*`（注意是 `/*` 代表整個帳號下所有 Pages）
> 5. Save

**設完後**：這把 KEY 只能在你的 `https://{你的帳號}.github.io/...` 網頁上用、別人拿去自己的網站用會被 Google 擋下。

> ⚠️ **常見錯誤**：referrer 漏寫 `/*`、只寫 `https://chen.github.io` —— Pages 上跑不動。**一定要 `/*`**。

---

### 操作示範 / 部署 + 自我演習（15 分鐘）

#### 部署（5 分鐘）

> 🔁 **走 CH5-5 五步**

| Step | 動作 |
|------|------|
| 1 | New repository → 命名 `prompt-optimizer`（或 `translator`） → Public + README → Create |
| 2 | repo 頁面按 `.` 進 github.dev |
| 3 | 新建 `index.html` → 貼 Claude 給的完整 HTML |
| 4 | Source Control → stage → commit `init` → Commit & Push |
| 5 | Settings → Pages → main → Save → 等 1~3 分鐘 |

拿到 `https://{你的帳號}.github.io/prompt-optimizer/`。

---

#### 自我演習（10 分鐘）— 本單元的高潮

> 💡 **這是本單元最有成就感的一刻**：你的工具實際跑通、看到 AI 真實回應。

1. **開部署網址**：打開 `https://{你}.github.io/prompt-optimizer/`
2. **貼 KEY**：第一個輸入框貼剛申請的 `AIza...` KEY
3. **貼粗糙提示詞**：例如「請幫我寫一個 LinkedIn 自介」
4. **按優化**
5. **看結果**：應該會看到 AI 給你的優化版，例如：

> 「請扮演一位 LinkedIn 個人品牌顧問，目標讀者是台灣科技業招募者。請用第一人稱寫一段 80 字以內的個人自介，包含：(1) 一句話定位 (2) 3 年內最具體成就 (3) 想找的下一份工作類型。語氣專業但親切、不要過度誇張。」

**第一次成功跑通的感覺是無價的**。**這 90 分鐘值了**。

---

### 卡關地圖 / 常見錯誤（10 分鐘）

#### 1. 學員不小心把 KEY 寫死進 HTML

**症狀：** 學員在 github.dev 編輯 `index.html`、把自己的 KEY 直接寫進 JS `const key = "AIza..."`。

**修法：**
- **馬上做：** 把 KEY 從程式碼裡刪掉 → commit & push
- **更重要：** 回 Google AI Studio → **刪除這把 KEY**（Delete API key）→ 重新申請一把（**舊的視為已洩漏**）
- **檢查清單：** 每次 commit 前看一眼 `<input type="password">` 的 value 屬性是不是空的

> 💡 **鐵律**：**每次按 Commit 之前，先按 Cmd+F 搜 `AIza` —— 不應該出現在程式碼任何地方**。

---

#### 2. referrer 限制設錯（漏 /*）

**症狀：** 部署到 GitHub Pages、貼 KEY、按優化 → 看到「API 錯誤：API_KEY_HTTP_REFERRER_BLOCKED」之類訊息。

**原因：** referrer 設成 `https://chen.github.io` 而沒有 `/*`。

**修法：** 回 Google Cloud Console → 把 referrer 改成 `https://chen.github.io/*` → Save → 等 5 分鐘生效。

---

#### 3. KEY 額度用完

**症狀：** 跑了幾次後突然開始錯誤「Quota exceeded」。

**修法：** 
- 等 24 小時、配額會重置（免費版每分鐘 / 每天有上限）
- 或在 Google AI Studio 升級成付費（不建議、課程不教這個）

> 💡 **免費版 Gemini 2.0 Flash 每天約 1500 次請求**，學員自用日常絕對夠。

---

#### 4. 部署後想分享連結給朋友（紅燈警告）

**症狀：** 學員做完工具超興奮、想丟群組分享。

**老師現場攔截：**

> 「**慢著！** 你做的是『**自用 demo**』，**不可以分享連結讓別人貼 KEY**。原因是 [回到本單元開頭那段「自用 vs 可分享」邊界]。」
> 
> 「**要分享給朋友用怎麼辦？** 等 Phase 2 上線 PRAC5-17，教你用 Vercel proxy 把 KEY 藏在後端、訪客不用自備 KEY 就能用 —— **那才是可以分享的版本**。」

---

#### 5. iOS Safari 跑不動

**症狀：** Mac 跑正常、iPhone Safari 打開、按優化沒反應。

**原因：** 某些 iOS Safari 版本對 `fetch` 跨域有額外限制、或對 `execCommand('copy')` 不支援。

**修法：** 回 AI 說「請確保程式碼在 iOS Safari 16+ 也能跑：(1) fetch 加 `mode: 'cors'` (2) 複製改用 `navigator.clipboard.writeText()`」。

---

### 動手做 / 學員自己跑一遍（15 分鐘）

**任務：** 自己跑完整流程、拿到一個能呼叫 Gemini API 的自用 demo。

**最終驗收門檻：**
- ✅ 拿到 `https://...github.io/...` 網址
- ✅ 貼自己的 KEY 跑通、看到 AI 真實回應
- ✅ git 倉庫**不含**任何 `AIza` 開頭的字串（用 github.dev 搜尋一遍）
- ✅ 頁面紅字警告「此頁僅供自己使用」顯示

**講師動作：** 學員做完後**逐一檢查 repo 程式碼有沒有 KEY**（用 Cmd+F 搜 `AIza`），是教學中**最重要的安全 checkpoint**。

---

### 收尾 / 你現在會做什麼 + 不該做什麼（5 分鐘）

#### 你會做的

- ✅ 用提示詞讓 AI 產出含 API KEY 輸入框的工具
- ✅ 在 Google AI Studio 申請 KEY、設 referrer 限制
- ✅ 部署成自用 demo、能呼叫真實 AI API
- ✅ 保持「KEY 不進 repo」的習慣（commit 前先搜 `AIza`）

#### 你**不應該**做的

- ❌ 分享這個版本的連結給朋友 → 要分享請等 PRAC5-17 Phase 2
- ❌ 把 KEY 寫死進程式碼 → 永遠不要
- ❌ 把 KEY 截圖貼給同事「你用這把」 → KEY 是你的、別人用會吃你的配額且出事你扛
- ❌ 不設 referrer 限制 → 設一下、5 分鐘換 10 倍安全

#### 你的下一步

- **每天上班開** `https://{你}.github.io/prompt-optimizer/`、把工作要寫的提示詞先過一輪優化、產能直接拉高
- **改成自己的版本**：把 model 從 `gemini-2.0-flash` 改成 `gemini-2.5-flash`（更強）、或加更多功能（翻譯 + 摘要 + 重寫）
- **等 Phase 2**：PRAC5-17 上線後做 Vercel proxy 版、分享給組長用

---

## 自學包（1 小時）

### 進階變化版（任挑）

#### 變化 A — 加更多任務模式

把單一「優化提示詞」變成多種任務：

> 在原提示詞末尾加：
> 「請加一個下拉選單『任務類型』：優化提示詞 / 翻譯 / 摘要 / 改寫成正式 / 改寫成口語。選不同任務、系統提示詞不同。」

---

#### 變化 B — 加歷史紀錄

> 「請加歷史紀錄功能：每次優化過的提示詞用 localStorage 存（最多 20 筆），下方列出來、可一鍵套用回輸入框。」

> 💡 **記住：** localStorage 存的是「**你的提示詞紀錄**」、**不是 KEY**。KEY 還是用 sessionStorage（關掉分頁就消失）。

---

#### 變化 C — 切換模型

> 「請加模型選擇下拉：gemini-2.0-flash（快、便宜）/ gemini-2.5-flash（強、慢）。選哪個 model 就呼叫哪個 endpoint。」

---

### 自學完成標準

- ✅ 至少完成 1 個變化版
- ✅ 倉庫經得起搜 `AIza` 一片空（沒洩漏）
- ✅ 寫一段話：「**我學完發現自己最容易犯的安全錯誤是什麼**」貼課程討論串

---

## 講師提示

**現場節奏（90 分鐘）：**
- 3' 破題 + 5' 自用 vs 可分享邊界 + 5' 提示詞卡 + 15' AI 對話示範 + 15' Google AI Studio 申請 KEY + 15' 部署 + 自我演習 + 10' 卡關地圖 + 15' 動手做 + 5' 收尾 + 2' Q&A = 90 分鐘

**現場觀察重點：**
- 「自用 vs 可分享」這頁**講師要花時間講透**、不要只念過去 → 學員會在最後想分享、攔得住嗎是本單元成敗
- Google AI Studio 申請 KEY 是學員 80% 第一次做 → 助教 A 全程站旁邊
- referrer 限制設錯是高發點 → 助教 B 要會看 console.log 錯誤訊息
- **commit 前搜 `AIza`** 是講師親自做的最後安全 checkpoint、**不要讓助教代勞**

**最容易翻車的時刻：**
- 學員做完很興奮想分享 → 講師現場攔截：「**這個版本不能分享**」+ 重申「**Phase 2 的 PRAC5-17 才是可分享版**」
- 學員把 KEY 寫死進去 → 講師現場示範：刪掉 + 重新申請 + 用 git 看 commit history（會看到舊版的 KEY 已經洩漏在歷史記錄了）→ 此時要刪 repo 重做

**課後素材：**
- 收集學員的「日常用工具」案例（如「我每天用我做的提示詞優化器、產能提升 X 倍」）→ 下次招生最有說服力的素材
- 收集學員寫的「我最容易犯的安全錯誤」反思 → 作為下期課程的 case study

---

## 與 PRAC5-17 的銜接（給講師看）

PRAC5-17 上線後（Phase 2），本單元**收尾段**要加一段：

> 「**完成 PRAC5-15 後**，請繼續 PRAC5-17：學會把這個自用 demo 升級成可分享版（用 Vercel proxy 把 KEY 藏在後端）。**這才是你能丟群組炫耀的版本**。」

並在頁面**置頂連結** PRAC5-17。
