# Claude Code 修正說明：n8n 課程總體可用性與資訊更新

本文件提供給 Claude Code 讀取後直接著手修正本課程。請以「維持現有課程架構與視覺風格」為前提，優先修正會造成過時教學、免費工具誤導、實作不可重現的內容。

## 課程位置

```text
/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/n8n
```

## 修正目標

1. 更新 2026 年已變動的工具名稱、計費單位、免費額度與授權說法。
2. 降低學員照做時遇到版本差異、額度超限、免費條件誤解的風險。
3. 補強課程演練的可操作性：範例資料、匯入流程、驗收標準。
4. 保留原本課程定位：Make 使用者進階到自架 n8n，完成本機批次文件處理與雲地協作。

## 優先修正清單

### P0：必修，避免過時或誤導

#### 1. Make operations 改為 credits

目前問題：

- `index.html` 仍寫「Make 免費版每月僅 1,000 次 operations」。
- 2026 年 Make 官方已改以 `credits` 作為計費單位。

需修改位置：

```text
index.html
lessons/module4.html
可能還有其他 lessons/*.html 中提到 operations / 1,000 次執行 的文字
```

建議寫法：

```text
Make Free plan 目前提供 1,000 credits/月。多數一般模組動作仍可理解為一次模組執行約消耗 1 credit，但 AI 相關功能或特殊模組可能依實際用量計算，課程以「把高頻、大量、本機檔案處理交給 n8n」作為設計原則。
```

請用 `rg -n "operations|1,000 次|1000 次|執行次數"` 全站檢查。

官方來源：

- https://www.make.com/en/pricing
- https://help.make.com/introducing-credits-new-billing-unit-live-in-make

#### 2. Gemini 免費額度改成「依模型查表」

目前問題：

- 多處寫「Gemini 免費版 15 requests/分鐘 + 1,500 次/日」。
- 2026 年 Gemini API 免費額度依模型不同，不能固定寫 1,500 次/日。

需修改位置：

```text
lessons/m1-3-prompt.html
lessons/module3.html
lessons/m3-2-rename.html
lessons/m4-3-ai.html
可能還有其他提到 1,500、15 requests、429 的頁面
```

建議寫法：

```text
Gemini API 免費額度依模型而異，且可能調整。設計批次流程時，不要把額度寫死在課程中；請學員在 Google AI Studio 或官方 Rate limits 頁確認目前模型的 RPM / TPM / RPD。工作坊建議使用低成本、免費額度較寬的 Flash / Flash-Lite 類模型，並用 Loop Over Items + Wait 控速。
```

補充目前官方表格中的例子，但不要寫成永久保證：

```text
例如官方 Free Tier 曾列出 Gemini 2.5 Flash-Lite、Gemini 2.0 Flash 等模型各自有不同 RPM / RPD。實際額度以官方頁面與帳號內顯示為準。
```

官方來源：

- https://ai.google.dev/gemini-api/docs/rate-limits

#### 3. Google Maps 每月 $200 免費額度已過時

目前問題：

- `lessons/m4-2-api.html` 寫「Google Maps 每月 $200 免費額度夠用」。
- Google Maps Platform 自 2025-03-01 起已用各 SKU 免費用量上限取代固定每月 $200 credit。

需修改位置：

```text
lessons/m4-2-api.html
```

建議寫法：

```text
Google Maps Platform 已改為依 SKU 提供每月免費用量上限，不再用固定每月 200 美元額度描述。若課程只是示範旅遊推薦，可優先使用免費的 CWA 氣象開放資料；地圖部分若需要 Google Maps，請務必設定 Cloud Billing、API quota 與 budget alert，並確認該 SKU 的免費用量。
```

官方來源：

- https://developers.google.com/maps/billing-and-pricing/march-2025
- https://developers.google.com/maps/billing-and-pricing/pricing-categories

#### 4. n8n Docker image 不要使用 latest

目前問題：

- `assets/n8n-starter-kit/n8n-compose.yml` 使用 `image: n8nio/n8n:latest`。
- 課程教材需要可重現。`latest` 會讓學員拿到不同版本，n8n 2.0 也有 breaking changes。

需修改位置：

```text
assets/n8n-starter-kit/n8n-compose.yml
assets/n8n-starter-kit/README.md
lessons/m1-1-overview.html
lessons/m1-1-setup.html
lessons/m1-1-troubleshoot.html
```

建議做法：

- 改成明確版本，例如 `n8nio/n8n:2.x.x`。實際版本請先查目前本課程要支援的 n8n 穩定版本。
- 若不想鎖死 patch version，可用課程測過的 minor version，但 README 必須寫清楚。
- 全站 footer 或 metadata 中的 `n8n latest` 要改成「課程測試版本：n8n x.x.x」。

驗收：

```text
rg -n "n8n latest|n8nio/n8n:latest|latest \\(Docker image" .
```

應無未處理結果，除非是在解釋不要使用 latest 的段落。

官方來源：

- https://docs.n8n.io/2-0-breaking-changes/
- https://docs.n8n.io/hosting/configuration/task-runners/

#### 5. 免費說法加上授權與條件

目前問題：

- 首頁與多處教材使用「完全免費」「無次數上限」。
- 這對個人教學情境大致成立，但對企業、政府、SaaS 包裝、商業轉售並不完整。

需補充位置：

```text
index.html
assets/n8n-starter-kit/README.md
lessons/m1-1-overview.html
```

建議補充：

```text
本課程的「免費」是指個人、教學、小型團隊在自架 n8n Community Edition、使用免費額度內的雲端服務時可完成演練。n8n Community Edition 採 Sustainable Use License，可用於內部商業流程，但不能把 n8n 包成 SaaS 或 white-label 服務對外販售。Docker Desktop 對個人、教育、小型企業免費；大型企業、政府或超過 Docker 免費條件的組織需自行確認授權。
```

官方來源：

- https://docs.n8n.io/sustainable-use-license/
- https://www.docker.com/products/personal

### P1：建議補強，提升演練成功率

#### 6. 建立範例資料與 workflow 匯入包

目前問題：

- 課程有很多實作，但缺少可直接下載或匯入的標準練習素材。
- 學員卡關時，講師難以判斷是資料問題、節點設定問題，還是工具版本問題。

建議新增資料夾：

```text
assets/sample-data/
assets/workflows/
```

建議內容：

```text
assets/sample-data/
  invoices/
    invoice-sample-001.txt
    invoice-sample-002.txt
  daily-report/
    meeting-note-sample.txt
    customer-feedback-sample.txt
  forms/
    google-form-fields.md

assets/workflows/
  m1-webhook-hello-world.json
  m2-reference-practice.json
  m3-folder-watch-demo.json
  m3-ai-rename-demo.json
  m4-google-form-to-n8n-demo.json
```

注意：

- 若要放 PDF，請使用自製、無版權風險、無個資的測試 PDF。
- 若暫時無法產出完整 workflow JSON，至少先放 `README.md` 說明每個練習需要的測試資料與預期輸出。

#### 7. 每個實作頁補「預期輸出」

優先頁面：

```text
lessons/m1-1-launch.html
lessons/m1-2-tunnel.html
lessons/m2-1-reference.html
lessons/m3-2-rename.html
lessons/m3-3-generate.html
lessons/m4-1-remote.html
lessons/m4-3-ai.html
lessons/m4-3-docs.html
```

建議每頁新增區塊：

```text
完成後你應該看到：
1. n8n 哪個節點亮綠燈
2. Output 面板應有哪些欄位
3. 本機資料夾應生成什麼檔案
4. 若串 Make / Gmail / Google Docs，外部服務應出現什麼結果
```

#### 8. 補安全提醒：Webhook 與 Tunnel 不應裸奔

目前課程主軸會把本機 n8n 暴露到外網。請補充：

- 測試期間可以先用隨機 path。
- 正式使用需加驗證，例如 header token、basic auth、Cloudflare Access 或 n8n credential 驗證。
- 不要把 API key 寫在一般節點文字欄，應用 Credentials 或 `.env`。
- 不要把含 credential 的 workflow JSON 放上公開網路。

優先位置：

```text
lessons/m1-2-tunnel.html
lessons/m4-1-remote.html
lessons/m4-2-api.html
```

### P2：內容品質與教學節奏

#### 9. 將「完全免費」改成「免費額度內可完成」

全站搜尋：

```text
rg -n "完全免費|免費工具|無次數上限|不用付費|免費版" .
```

建議原則：

- n8n 自架：可說「Community Edition 自架無按執行次數計費」。
- Make：可說「Free plan 可完成課程演練，但有 credits、active scenarios、排程間隔與執行時間限制」。
- Gemini：可說「免費額度內可演練，批次需控速」。
- Cloudflare Tunnel：可說「Tunnel 可在免費方案使用，但帳號、網域與安全設定需依 Cloudflare 當前規則」。
- Docker Desktop：不可對所有企業學員說完全免費。

#### 10. 檢查 ngrok 免費替代說法

`lessons/m1-2-tunnel.html` 提到 ngrok「完全免費」。ngrok 免費方案可能有固定限制，建議改成：

```text
若 Cloudflare Tunnel 在現場無法設定，可用 ngrok free plan 作為短期測試替代；正式課程與長期使用仍建議以 Cloudflare Tunnel 或正式網域設定為主。
```

## 建議執行步驟

1. 先用 `rg` 找出所有過時關鍵字。
2. 修 P0 的文字與 starter kit 版本。
3. 補 README 中的「免費條件與授權限制」。
4. 新增 `assets/sample-data/README.md` 與 `assets/workflows/README.md`，先建立可擴充入口。
5. 挑 2-3 個核心實作頁補「預期輸出」，不要一次大改所有頁面造成版面風格不一致。
6. 最後全站搜尋確認沒有舊術語殘留。

## 驗收指令

請在課程根目錄執行：

```bash
rg -n "operations|1,500 次|15 requests|\\$200|n8nio/n8n:latest|n8n latest|完全免費|無次數上限|ngrok.*完全免費" .
```

允許留下的結果只應該是：

- 說明「舊說法已改」的備註。
- 引導學員查官方額度的段落。
- 本文件本身。

## 已核對來源

- n8n Choose your n8n: https://docs.n8n.io/choose-n8n/
- n8n Sustainable Use License: https://docs.n8n.io/sustainable-use-license/
- n8n Task runners: https://docs.n8n.io/hosting/configuration/task-runners/
- n8n 2.0 breaking changes: https://docs.n8n.io/2-0-breaking-changes/
- n8n Desktop App archived: https://github.com/n8n-io/n8n-desktop-app
- Make pricing: https://www.make.com/en/pricing
- Make credits transition: https://help.make.com/introducing-credits-new-billing-unit-live-in-make
- Gemini API rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Cloudflare Tunnel: https://developers.cloudflare.com/tunnel/
- Google Maps March 2025 changes: https://developers.google.com/maps/billing-and-pricing/march-2025
- Google Maps pricing categories: https://developers.google.com/maps/billing-and-pricing/pricing-categories
- Docker Personal: https://www.docker.com/products/personal
- LINE Messaging API pricing: https://developers.line.biz/en/docs/messaging-api/pricing/

## 完成後回報格式

請 Claude Code 完成後回報：

```text
已修正：
- ...

新增：
- ...

仍需人工確認：
- ...

驗收：
- rg 檢查結果
- 是否有啟動本地頁面檢查
```
