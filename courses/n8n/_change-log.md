# n8n 課程變更日誌

記錄每次依 `CLAUDE_CODE_FIX_BRIEF.md` 或其他外部刺激所做的內容修正，方便日後若工具政策再變時對照查找。

## 2026-05-01（第九發） — m1-2-tunnel.html 主流程重整：Quick Tunnel + http2 升為主路徑

**驅動事件**：使用者壓測時連續 4 次卡關（綁卡 → 沒網域 → QUIC 被擋 → macOS Gatekeeper），每次我都用「補釘」式修法疊加在原本的「完整 Tunnel」主流程上。使用者明確指出講義變得「零散、補釘式、看見補釘但不知所以然」，要求講義主流程必須是清晰單一動線。

**根因**：原 m1-2-tunnel.html 把「完整 Tunnel + Zero Trust + 自有網域」當主流程是過度樂觀——對 90%+ 課程學員（沒網域、不想綁卡、ISP 擋 QUIC）這條路根本走不通。Quick Tunnel + http2 才是真正可走的最低門檻路徑，但它原本被寫成「替代路徑」「沒網域看這個」的次要選項。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| 整檔重寫 m1-2-tunnel.html | 主流程改為 3 步驟（5 分鐘）：(1) 安裝 cloudflared (2) 雙擊 tunnel-quick 拿 URL (3) 5 動作連續完成 webhook 測試 |
| Verify 重寫 | 三件事齊備：cloudflared URL active / webhook 200 / n8n 節點變綠+Output 有資料 |
| Troubleshoot 改寫 4 條 | QUIC retry loop / 404 webhook not registered / URL 失效 / 找不到 cloudflared |
| 完整 Tunnel 降為折疊式進階 | 原 Step 1-7 全部移到 `<details>`，標題「⚙️ 進階：完整 Tunnel + 自有網域（要長期穩定 URL 才看）」，含兩層門檻說明 + 7 步驟 + QUIC 擋的提醒 |
| ngrok 維持備用方案 | 簡化為 4 步驟，標明「cloudflared 完全不通時才用」 |
| hero meta-bar 更新 | 從「7 個步驟 / 15-20 分鐘」改為「主流程 3 步驟 5 分鐘 / 進階 30 分鐘」 |

**飛輪轉化**：講義主流程必須走「90%+ 學員實際能完成的最低門檻」路徑，不是「最完整、最理想、但少數人才走得動」的高門檻路徑。次要選項放折疊或進階段落，主視覺路徑只能有一條。寫主流程前先問：「90% 學員實際能跨過嗎？」答否就降階為進階。

---

## 2026-05-01（第八發） — Cloudflared QUIC 在台灣家用 ISP 被擋，預設改 HTTP/2

**驅動事件**：學員第一次跑 `tunnel-quick.command` 卡在連續 retry loop：`failed to serve tunnel ... control stream encountered a failure ... Retrying connection in up to 4s/8s/16s`。改用 `cloudflared tunnel --url http://localhost:5678 --protocol http2` 立刻通，台北邊緣節點 tpe01 正常 register。

**根因**：cloudflared 預設用 QUIC（UDP 7844）。台灣家用 ISP / 公司網路 / 部分 VPN 會擋 UDP 7844（防 P2P 流量）。cloudflared 雖有 auto fallback 機制但不可靠，學員容易卡死在 retry loop。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| tunnel-quick 預設加 --protocol http2 | `assets/n8n-starter-kit/tunnel-quick.command` + `tunnel-quick.bat` |
| tunnel-quick.command 加偵測 | 30 秒內未取得 trycloudflare.com URL 且 logs 含 retry 關鍵字 → 跳對話框建議改 ngrok |
| 重新打包 zip | `assets/n8n-starter-kit.zip` 15 KB |
| 飛輪規則新增 | `_規範/飛輪規則.md` 加「Cloudflared 預設 HTTP/2 而非 QUIC」原則 |

**飛輪轉化**：未來 starter-kit 凡涉及 cloudflared / 其他 QUIC 協議工具，預設值要選「最高機率 work」的 protocol，不靠 auto fallback。腳本內建錯誤偵測 → 跳對話框引導，不靠學員看 logs 判讀。

---

## 2026-05-01（第七發） — Cloudflare 自有網域門檻 + Quick Tunnel 主替代路徑

**驅動事件**：學員過了 Cloudflare 綁卡關卡，進入 Public Hostname 設定步驟，發現 Domain 下拉選單**必須選自已託管在 Cloudflare 的網域**。學員沒自有網域，下拉選單空的，又卡住。

**根因**：原 m1-2-tunnel 講義假設學員手上有自有網域，沒誠實揭露這個前提。實際上 90% 課程學員是「想體驗自動化」而非「要部署生產系統」，買網域對他們是 over-kill。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| Step 1 揭露框升級 | `m1-2-tunnel.html` 步驟 1 揭露框從「綁卡單一門檻」改為「綁卡 + 自有網域兩層門檻」並指向新 Quick Tunnel 替代 |
| 新增 Quick Tunnel 替代段落 | `m1-2-tunnel.html` 在 ngrok fallback 之前加綠色突出 context-box，介紹 `cloudflared tunnel --url http://localhost:5678` 一行指令路徑（**仍是 Cloudflare 官方功能**，比 ngrok 更貼近主路徑） |
| 新增 tunnel-quick 啟動腳本 | `assets/n8n-starter-kit/tunnel-quick.command`（Mac，含 cloudflared 安裝檢查 + n8n 啟動檢查 + GUI 對話框錯誤處理）+ `tunnel-quick.bat`（Windows） |
| README 加新檔案說明 | `assets/n8n-starter-kit/README.md` 檔案用途表加 tunnel-quick 條目 |
| 重新打包 zip | `assets/n8n-starter-kit.zip` 14 KB（含新增 11 個檔案） |

**設計選擇 — 為何 Quick Tunnel 優於 ngrok 作為主推薦**：

1. 仍是 Cloudflare 官方功能 → 學員不用學新工具（cloudflared 已在 Step 3 裝過）
2. 不需註冊任何帳號 → 比 ngrok 還少一步
3. 不需綁卡 → 比完整 Tunnel 少一個門檻
4. 支援 HTTPS → 解決 secure cookie 問題（雖然 localhost 已關 secure cookie，但部署時可重新啟用）

**飛輪轉化**：未來凡是「需要公開 URL」的教學單元，預設應給三層路徑：(1) 不需網域不需帳號的 Quick Tunnel/類似工具；(2) 需要帳號但免費的方案；(3) 完整生產級方案。揭露框必須在註冊步驟前出現，不是註冊後才出現。

---

## 2026-04-30（第六發） — Cloudflare Zero Trust 綁卡門檻誠實揭露

**驅動事件**：學員依 m1-2-tunnel.html 步驟 1 註冊 Cloudflare Zero Trust，卡在「需要付款方式才能使用免費的 Zero Trust」。原講義文案「個人開發/教學用途在免費方案內可用（依 Cloudflare 當前規則）」過於模糊，學員到綁卡那一刻才知道。

**根因**：Cloudflare 2024 年起的 anti-abuse 政策要求 Zero Trust 免費方案首次設定時綁信用卡（不扣款，但學員會卻步）。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| Step 1 加誠實揭露框 | `lessons/m1-2-tunnel.html` 步驟 1 加 ⚠️ 黃色提示框，明確寫「需綁信用卡 + 不會扣款 + 不綁卡看 ngrok fallback」 |
| 飛輪規則新增 | `_規範/飛輪規則.md` 加「外部 SaaS 政策變動誠實揭露規則」+ 5 大 SaaS 已知門檻清單 + 每季回檢機制 |

**飛輪轉化**：未來所有外部 SaaS 註冊步驟前必有 ⚠️ 誠實揭露框；fallback 路徑單一不雙路；每季回檢所有 SaaS 政策。

---

## 2026-04-30（第五發） — port 5678 衝突自動偵測

**驅動事件**：學員第二次解壓 zip（macOS 自動命名為 `n8n-starter-kit 2/`），雙擊 start.command 跑出 `Bind for 0.0.0.0:5678 failed: port is already allocated`。原本的 `n8n-starter-kit/` 那一輪 n8n container 還在跑佔 port。

**根因**：start.command 啟動前沒有偵測 port 5678 是否已被舊 container 佔用。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| start.command 加 port 衝突偵測 | `assets/n8n-starter-kit/start.command` 啟動前用 `docker ps --filter publish=5678` 偵測，若有跳對話框「停掉並重啟」一鍵清理舊 container（自動跑 `docker stop` + `docker rm`） |
| start.command 改 capture exit code | 移除 `set -e`，改用 `COMPOSE_OUTPUT=$(... 2>&1)` capture，up 失敗時可解析錯誤類型（含 fallback：自動清理失敗 → 提示打開 Docker Desktop GUI 手動處理） |
| 重新打包 zip | `assets/n8n-starter-kit.zip` 12 KB |
| 講義 troubleshoot 加新條目 | `lessons/m1-1-launch.html` 加「port is already allocated」單一動作 troubleshoot |
| README 同步 | `assets/n8n-starter-kit/README.md` 加新錯誤對照 |

**飛輪轉化**：未來 starter-kit 啟動腳本起手式必含「port 衝突自動偵測 + 對話框一鍵清理」邏輯，不再叫學員開終端機跑 `lsof` / `kill`。

---

## 2026-04-30（第四發） — postgres 密碼認證失敗自動偵測 + troubleshoot 哲學重整

**驅動事件**：學員 docker compose 起來後 n8n logs 反覆出現 `password authentication failed for user "n8n"` + `Last session crashed`。根因：postgres image 第一次啟動把 .env 密碼寫進 db user table，之後改 .env 不會自動同步。學員多次重下 zip 後，postgres_data volume 還是舊密碼建的。

**使用者明確指示**：「不要讓我嘗試補釘，我會每一次都重新下載，因為課程進行時，不會有一套你在學員旁邊提供補釘。」此前我給的「立即解 sed / 手動編輯 yaml + 永久修」雙路徑指引模式被駁回。

**修補哲學重整**：troubleshoot 段落必須是「**重下 zip + 雙擊 start.command**」單一動作，可預測錯誤由啟動腳本主動偵測 + GUI 對話框引導，不再叫學員開終端機跑指令。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| start.command 加自動偵測 + 對話框 | `assets/n8n-starter-kit/start.command` 啟動超時時 grep logs 是否含 `password authentication failed`，若是跳 GUI 對話框「重置並重啟」一鍵處理 |
| 等候迴圈加進度回報 | start.command 每 10 秒 echo「⏳ 已等候 N 秒...」避免學員以為腳本掛了 |
| .env.example 加密碼警告 | 註明「密碼一旦設定不要再改，否則需 reset volume」 |
| 重新打包 zip | `assets/n8n-starter-kit.zip`（12 KB） |
| 講義 3 條 troubleshoot 全簡化 | `lessons/m1-1-launch.html` 砍掉 sed 一行 / 手動編輯 yaml 等 patch 指引，全部改寫成「重下 zip 覆蓋 + 雙擊」單一路徑 |
| README 同樣簡化 | `assets/n8n-starter-kit/README.md` 同上原則 |
| 飛輪規則加新原則 | `_規範/飛輪規則.md` 加「課程修補哲學：學員旁邊沒有 Claude」 — 設計責任移到 starter-kit 本身 |
| Memory feedback | `~/.claude/projects/.../memory/feedback_no_patch_for_students.md` 跨 session 持久化此原則 |

**飛輪轉化**：未來所有 course-designer / course-reviewer / build-course-page / 講義 troubleshoot 任務，每寫一條錯誤指引必過「能不能簡化成『重下 + 雙擊』單一動作？」門檻；做不到才允許跳「請聯絡講師」對話框。

---

## 2026-04-30（第三發） — N8N_SECURE_COOKIE=false 補設（學員開 localhost:5678 被擋）

**驅動事件**：學員 docker compose 啟動成功後，開 localhost:5678 顯示「Your n8n server is configured to use a secure cookie, however you are either visiting this via an insecure URL, or using Safari」，登入頁直接擋住。

**根因**：n8n 預設 `N8N_SECURE_COOKIE=true`，要求 HTTPS 才能登入；localhost 是 HTTP 被擋。試跑包 compose.yml 沒設 false。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| compose 加環境變數 | `assets/n8n-starter-kit/n8n-compose.yml` n8n service environment 加 `- N8N_SECURE_COOKIE=${N8N_SECURE_COOKIE:-false}` |
| .env.example 加說明 | `assets/n8n-starter-kit/.env.example` 加 `N8N_SECURE_COOKIE=false` 區段，附 localhost vs Tunnel 切換說明 |
| 重新打包 zip | `assets/n8n-starter-kit.zip`（11 KB / 內含修補後 compose） |
| 講義 troubleshoot 加新條目 | `lessons/m1-1-launch.html` 加新 ts-item 列在第一條，附「重下 / 手動編輯」雙路徑 + 瀏覽器建議避開 Safari |
| README 加新 troubleshoot | `assets/n8n-starter-kit/README.md` 「卡關時」段最前面加新錯誤對照 |
| 飛輪規則新增 | `_規範/飛輪規則.md` 加「n8n localhost 啟動必設 N8N_SECURE_COOKIE=false」 |

**飛輪轉化**：未來新建 n8n self-host starter-kit，**起手式 compose 必含** `N8N_SECURE_COOKIE=${N8N_SECURE_COOKIE:-false}`；Tunnel 章節（m1-2-tunnel）必須在 HTTPS 切換時把這個改回 true。教案建議 localhost 階段用 Chrome / Firefox / Edge 而非 Safari。

---

## 2026-04-30（第二發） — Docker Compose 自訂檔名 -f 修補（學員雙擊 start.command 卡關）

**驅動事件**：學員雙擊 `start.command` 跑出 `no configuration file provided: not found`。

**根因**：`docker compose` 預設只認 `compose.yaml` / `docker-compose.yml`，不認課程使用的自訂檔名 `n8n-compose.yml`。試跑包 6 個 .command/.bat 都漏了 `-f n8n-compose.yml` 參數。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| sed 批次補 `-f n8n-compose.yml` | `assets/n8n-starter-kit/{start,stop,update}.{command,bat}` 共 6 個 |
| 重新打包 zip | `assets/n8n-starter-kit.zip`（內含修補後 6 個 script + 同步更新的 README） |
| 講義 troubleshoot 加新條目 | `lessons/m1-1-launch.html` 第一條 `ts-item` 加「`no configuration file provided: not found`」+ sed 一行 patch 解 |
| README 加新 troubleshoot | `assets/n8n-starter-kit/README.md` 「卡關時」段加新錯誤對照 + 卡關 3 行指令也補 `-f` |
| 飛輪規則新增 | `_規範/飛輪規則.md` 加「Docker Compose 自訂檔名規則」 |

**驗證**：zip 解壓後 `start.command` 內容包含 `docker compose -f n8n-compose.yml up -d` ✓

**飛輪轉化**：未來建立 starter-kit 用自訂 compose 檔名時，所有 `docker compose` 指令必須加 `-f <檔名>`；對應錯誤訊息 `no configuration file provided` 第一個假設就是這個。詳見飛輪規則。

---

## 2026-04-30 — 試跑包下載動線修補（學員實際演練卡關觸發）

**驅動事件**：使用者依 m1-1-launch 教案演練，發現「下載解壓雙擊」步驟做不到——個別 9 個檔案連結需點 9 次、無 zip 包、macOS 下載 .command 被 quarantine + 失執行權限。

**問題分級**：評估報告 § 3「試跑包 ✓ 已具備」失準——是「檔案就位」但缺「打包成 zip」「macOS 解壓指引」兩層交付動線。

**修補項目**：

| 動作 | 檔案 |
|------|------|
| 打包 zip | 新建 `assets/n8n-starter-kit.zip`（10 KB / 11 entries 含 shared/） |
| 講義改下載區塊 | `lessons/m1-1-launch.html` — 主按鈕改「⬇ 下載 n8n-starter-kit.zip」+ macOS chmod/xattr details + 個別檔備援 |
| README 加 macOS 指引 | `assets/n8n-starter-kit/README.md` — 第一次啟動段加 `chmod +x` + `xattr -d com.apple.quarantine` 一次性指令 |
| 飛輪規則新增 | `_規範/飛輪規則.md` — 加「試跑包交付完整性規則」（L1 檔案 / L2 打包 / L3 可執行）三層驗證 |
| 評估報告更新 | `_reviews/n8n-evaluation-2026-04-30.md` § 3 加修補註記 |

**驗證**：zip 解壓後 `.command` 檔保留執行位元 `-rwxr-xr-x` ✓；m1-1-launch.html lint 0 BLOCKER 0 ERROR；sitemap 471 URL。

**飛輪轉化**：未來評估「課程可落地實現」必須走完整學員動線（下載 → 解壓 → 執行 → 看到 n8n 主介面），不是只看 `ls` 結果。詳見 `_規範/飛輪規則.md`。

---

## 2026-04-28 — 依 CLAUDE_CODE_FIX_BRIEF.md 全面修正

**驅動文件**：`CLAUDE_CODE_FIX_BRIEF.md`（同目錄）
**驗證**：lint-page.py 0 BLOCKER 0 ERROR；search-index 469 筆；sitemap 469 URL
**核對來源**：依 brief「已核對來源」段所列官方頁面

### Phase A · P0 文字修正

| Brief # | 修改主題 | 影響檔案 | 改動方向 |
|---------|---------|---------|---------|
| #1 | Make operations → credits | `index.html`、`module1.html`、`m1-1-glossary.html`、`module4.html` | Make 改用 credits 描述計費單位（1,000 credits/月，AI 模組另計），不再寫死 1,000 ops |
| #2 | Gemini 額度依模型查表 | `m1-3-prompt.html`、`m3-2-batch.html`、`m3-2-rename.html`、`m3-3-generate.html`、`m4-3-ai.html`、`module3.html` | 不再寫死 1,500 次/15 RPM；改為「依官方 Rate limits 頁面為準」+ Flash-Lite 例值 + 控速建議 |
| #3 | Google Maps $200 → SKU quota | `m4-2-api.html` | 點出 2025-03 改制；建議 budget alert + 旅遊範例改 CWA + OpenStreetMap |
| #4 | Docker image 鎖版本 | `n8n-compose.yml`、`n8n-starter-kit/README.md`、`m1-1-launch.html`、`m1-1-overview.html`、`m1-1-setup.html`、`m1-1-troubleshoot.html` | 從 `n8nio/n8n:latest` 鎖到 `n8nio/n8n:2.17.8`（2026-04-27 stable，依 Docker Hub 驗證）。Docker Hub 沒提供 minor-only tag，鎖 patch；要升級時手動更新。footer-meta 也同步更新 |
| #5 | 「完全免費」加授權條件 | `index.html`、`module1.html`、`m1-1-overview.html`、`m1-2-tunnel.html`、`module4.html`、`m4-1-remote.html`、`n8n-starter-kit/README.md` | 首頁/招生敘事一行帶過 SUL + Docker Desktop 商用條款；README 寫詳細版；分服務分別定義（n8n / Make / Gemini / Cloudflare / Docker） |

### Phase B · 演練支援與安全

| Brief # | 主題 | 影響檔案 |
|---------|------|---------|
| #6 | sample-data / workflows 入口 | 新增 `assets/sample-data/README.md` + invoice / daily-report / forms 三類示範素材；新增 `assets/workflows/README.md`（含 Reset Credentials SOP） |
| #7 | 預期輸出區塊 | 首批 3 頁試做：`m1-1-launch.html`、`m2-1-reference.html`、`m4-3-ai.html`；沿用既有 expect-box / verify-box 樣式，不新增 CSS |
| #8 | Webhook / Tunnel 安全提醒 | `m1-2-tunnel.html`、`m4-1-remote.html`、`m4-2-api.html` 各加一個紅色 context-box 列四項：隨機 path / Header Auth / Credentials / 不公開含 cred 的 JSON |
| #10 | ngrok 改短期測試替代 | `m1-2-tunnel.html` 移除「完全免費」字樣，改「ngrok free plan 短期測試替代」 |

### Brief 沒寫但補強的項目

1. **Workflow JSON 匯出檢查 SOP**：`assets/workflows/README.md` 寫了 export 前 grep 檢查節點參數的硬寫密鑰（n8n workflow export 預設不含 credential 本體，但節點參數欄位裡寫死的 token 會被帶出）
2. **lint + index + sitemap 同步**：本檔末尾紀錄一次完整驗收
3. **Docker 版本誤判修正**：原 plan 寫 n8n 主線是 1.x、2.0 未 GA；實查 Docker Hub 後確認 2.17.8 為 2026-04-27 stable，已照實鎖 patch
4. **變更紀錄**：建立此 `_change-log.md`，後續工具政策再變時補新 entry

### 已知殘留（屬刻意保留，非問題）

- `m4-2-api.html:238` 仍出現「\$200」字樣，但屬於「不再是固定 $200/月 credit」的解釋文字，是 brief 允許保留的「說明舊說法已改」備註

### 待辦（後續延伸）

- B2 預期輸出剩餘 5 頁：`m1-2-tunnel`、`m3-2-rename`、`m3-3-generate`、`m4-1-remote`、`m4-3-docs`（首批驗收 OK 後再批次推）
- 補齊 `assets/workflows/` 內的實際 JSON（首次預定 m1-webhook-hello-world.json）
- 工具政策每季回頭檢查（Make credits、Gemini quota、Maps SKU、n8n 版本）
- **設計系統小修**：B3 紅色安全提醒框目前用 inline `border-left:4px solid #b54a4a`，建議抽成 `.security-box` class 並寫進 `_規範/design-tokens.md`，與既有黃系 `.step-tip.warning` 區分（Codex review #7，本次先不動樣式系統）

---

## 2026-04-28 — Codex L3 review 跟進（同日）

**驅動**：CALL_ID `a82908d7`，consult mode 248s。Codex 找到 3 個必修 + 4 個建議修，採納 #1–#6（樣式抽 class #7 留 backlog）。

| Codex 條目 | 修正範圍 |
|-----------|---------|
| P0 #1 — `assets/workflows/README.md` 對 n8n export 行為描述錯誤 | 完全重寫安全段。改寫實情：n8n workflow export 預設不帶 credential 本體（官方文件），真風險是節點參數欄位硬寫死的 token；改用 grep 命令檢查節點 JSON |
| P1 #2 — `m4-2-flow.html` 漏網（line 165 / 176 / 232 / 233） | 「無限次數」→「不按 SaaS credits 限制」；「Make 有次數限制／n8n 無限次數」→「Make 受 credits 限制／n8n 自架不按次計費」；「1,000 ops」→「1,000 credits」；「每則 LINE 只耗 1 op」→「一般模組動作大致 1 credit/次（依 Make 當前計費）」 |
| P1 #3 — `index.html:159` stat | 「不計／執行次數」→「自架／不按次計費」 |
| P1 #4 — `assets/n8n-starter-kit/README.md` 開頭版本說法 | 「2.17.8（2026-04 stable）」→「2.17.8（2026-04-27 依 Docker Hub tags 驗證可用）」，避開 n8n stable 是 moving tag 的風險 |
| P1 #5 — `m1-3-prompt.html` 「每日數千 RPD」 | 拿掉，只留「Flash-Lite 曾列每分鐘約 15 RPM 為控速參考」+「實際 RPM/TPM/RPD 以官方為準」 |
| P2 #6 — starter-kit README SUL 段 | 把 n8n SUL（用途限制）與 Docker Desktop（組織規模/條款）拆成兩條獨立判斷，不再綁在「個人/教學/小型團隊」一句話 |
| Codex 自己漏抓我順手補的 | `module4.html:204` 「無限次跑大量迴圈」→「自架不按次計費跑大量迴圈」；`module4.html:339` Q3「Make 免費版單次執行 5 分鐘上限」→「依 Make 當前條款；自架由你的機器資源決定」 |

**Verdict**：actionable（Codex 指出真實事實錯誤與漏網，可執行）

```
python3 codex_bridge.py --mark-verdict a82908d7 --verdict actionable
```

### 驗收紀錄

```
$ python3 docs/lint-page.py courses/n8n/ --summary
═══ 摘要 ═══
掃描：46 頁
BLOCKER：0 條（0 檔）
ERROR：  0 條
WARN：   116 條
✅ 無 BLOCKER。

$ python3 docs/build-search-index.py
✓ 已寫入 search-index.json（469 筆）

$ python3 docs/build-sitemap.py
✓ 已寫入 sitemap.xml（469 筆 URL）

$ rg -n "operations|1,500 次|15 requests|\$200|n8nio/n8n:latest|n8n latest|完全免費|無次數上限|ngrok.*完全免費" courses/n8n/ --type-add 'web:*.{html,md,yml,yaml}' --type web | grep -v CLAUDE_CODE_FIX_BRIEF
courses/n8n/lessons/m4-2-api.html:238  ← 已改寫後的解釋字樣，符合 brief 允許殘留條件
```
