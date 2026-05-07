# n8n Starter Kit · 弄一下工作室

《AI 資料工廠》課程的 n8n 本機環境試跑包。在自己電腦跑一個自架的 n8n，不按執行次數計費，並能直接讀寫本機資料夾。

> **版本**：v1.0.2（2026-05-07）— 補完整「安全設定」章節 + `.env.example` 預留 BASIC_AUTH 三行（前一版 v1.0.1 已將 n8n editor 限制為本機存取）。詳見 [變更紀錄](#變更紀錄)。
>
> **課程測試版本**：n8n `2.17.8`（2026-04-27 依 Docker Hub tags 驗證可用）+ Docker Desktop 4.x。`n8n-compose.yml` 已鎖定此 patch 版本以確保畫面與行為可重現；升級時請重新驗證教材。
>
> **免費條件**：n8n Community Edition 採 [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/)——課程中的自架、教學、內部流程與顧問案通常屬允許用途；不可把 n8n 代管成 SaaS、white-label 或嵌入產品對外販售。Docker Desktop 的免費資格另依 [Docker 條款](https://www.docker.com/products/personal/) 判斷，組織規模與用途請逐項對照。

## 最小執行流程

### 第一次啟動

1. 從課程網頁下載 `n8n-starter-kit.zip`，解壓到方便管理位置（建議 `~/n8n-starter-kit/` 或 `C:\Users\你的名字\n8n-starter-kit\`）
2. 先安裝 **Docker Desktop** 並確認已啟動（左上角應看到鯨魚圖示）
   - Mac：<https://www.docker.com/products/docker-desktop/>（依 Intel / Apple Silicon 下載對應版本）
   - Win：同網址；安裝完需啟用 WSL2（Docker Desktop 安裝精靈會引導）
3. **macOS 解壓後必做（一次性）**：開「終端機」→ `cd ~/n8n-starter-kit/` → 跑下列兩行解開瀏覽器下載的執行限制：
   ```bash
   chmod +x start.command stop.command update.command
   xattr -d com.apple.quarantine start.command stop.command update.command 2>/dev/null || true
   ```
   不跑這兩行的話，雙擊 `.command` 會跳「無法打開」或「找不到應用」。Windows .bat 不需要這步。
4. 雙擊 `start.command`（Mac）或 `start.bat`（Windows）
5. 第一次會自動把 `.env.example` 複製為 `.env` 並打開讓你編輯，**請改 `POSTGRES_PASSWORD`** 為強密碼後存檔
6. 再次雙擊 `start.command` / `start.bat`，等約 30 秒（首次需下載 image，可能花 1-5 分鐘）
7. 瀏覽器自動打開 <http://localhost:5678>，建立你的 Owner Account（信箱 + 密碼，n8n 內建）

### 日常使用

| 動作 | Mac | Windows |
|---|---|---|
| 啟動 n8n | 雙擊 `start.command` | 雙擊 `start.bat` |
| 停止 n8n | 雙擊 `stop.command` | 雙擊 `stop.bat` |
| 升級 n8n | 雙擊 `update.command` | 雙擊 `update.bat` |

## 各檔案用途

| 檔案 | 用途 |
|---|---|
| `n8n-compose.yml` | Docker Compose 配置，定義 n8n + PostgreSQL 兩個容器 |
| `.env.example` | 環境變數範本（時區、密碼、Webhook URL） |
| `.env` | 你的實際設定（首次啟動會從 example 自動複製，**勿提交版控**） |
| `start.command` / `start.bat` | 一鍵啟動 n8n |
| `stop.command` / `stop.bat` | 停止 n8n（資料保留） |
| `update.command` / `update.bat` | 升級 n8n image |
| `tunnel-quick.command` / `tunnel-quick.bat` | 開 Cloudflare Quick Tunnel（不需自有網域、不需綁卡，給 `*.trycloudflare.com` 公開網址） |
| `shared/` | 本機資料夾，會掛到容器內 `/files/shared`（Module 3 Watch Folder 用） |

## Mac 第一次執行 .command 被擋怎麼辦

雙擊 `start.command` 跳出「無法打開，因為來自未識別的開發者」是 macOS 安全機制，不是檔案壞了：

1. 開「**系統設定 → 隱私權與安全性**」
2. 捲到「**安全性**」區塊，會看到「`start.command` 已被阻擋使用」
3. 按「**強制打開**」→ 確認密碼
4. 之後同一檔案不會再被擋

## 卡關時

去課程 **1.1.3 排錯手冊頁**，或在終端機（cd 到本資料夾）執行以下三行貼給講師：

```bash
docker ps
docker compose -f n8n-compose.yml logs n8n --tail 50
docker compose -f n8n-compose.yml config
```

### 常見錯誤：localhost:5678 顯示「Your n8n server is configured to use a secure cookie」

**原因**：你下載的試跑包是 2026-04-30 之前的舊版。

**解法**：去課程網頁 1.1.2 啟動頁重新下載最新 `n8n-starter-kit.zip` 覆蓋整個資料夾，再雙擊 `start.command`。新版本已預設關閉 secure cookie。

**瀏覽器**：用 Chrome / Firefox / Edge（避開 Safari）。

### 常見錯誤：`no configuration file provided: not found`

**原因**：你下載的試跑包是 2026-04-30 之前的舊版。

**解法**：去課程網頁 1.1.2 啟動頁重新下載最新 `n8n-starter-kit.zip` 覆蓋整個資料夾，再雙擊 `start.command`。新版本的腳本已自動指定 compose 檔。

### 常見錯誤：`port is already allocated` / `Bind for 0.0.0.0:5678 failed`

**原因**：之前已啟動過 n8n（可能解壓到不同資料夾啟了多次），舊 container 還佔 5678 port。

**解法**：再雙擊一次 `start.command`，新版會自動偵測並跳對話框問你要不要停掉舊 container，按「停掉並重啟」即可。

### 常見錯誤：`password authentication failed for user "n8n"`

**原因**：你之前啟動過 n8n，postgres 用舊密碼建了資料庫；後來改了 `.env` 密碼，新密碼跟舊資料庫對不上。

**解法**：再雙擊一次 `start.command`，新版腳本會自動偵測這個錯誤，跳對話框問你要不要重置——按「重置並重啟」即可。

## 安全設定

> 本段一次講清楚「在公開 wifi / 共享辦公室 / 咖啡店等場景下，怎麼安全跑這份 starter-kit」。預設組合已經把多數風險擋掉，只要不亂改設定即可。

### 預設安全組合（不需改任何東西）

| 防線 | 怎麼擋 | 設定來源 |
|---|---|---|
| 同網段他人連不到你的 n8n | n8n editor port 綁 `127.0.0.1`（v1.0.1 起） | `n8n-compose.yml` |
| 第一個打開 n8n 的人就是 owner | n8n 內建 Owner Account（首次打開 localhost:5678 會引導建立） | n8n 預設 |
| Postgres 不對外 | compose 沒寫 ports（只在 Docker 內網讓 n8n 連） | `n8n-compose.yml` |
| 環境變數不誤入 git | `.gitignore` 預設排除 `.env` | starter-kit 同層或上層 repo |

照預設走，純 localhost 使用情境下你不需要再改任何設定。

### 三條紅線（千萬不要做）

1. **不要把 `n8n-compose.yml` 的 port 改回 `'5678:5678'`**（沒有 `127.0.0.1:` 前綴）。一旦改回，Docker 會綁到 `0.0.0.0`（全網卡）→ 同網段任何人輸入 `http://你的IP:5678` 就能登入你的 n8n 看 credentials。
2. **不要對外暴露 Postgres port**。compose 沒寫 postgres 的 ports 是故意的；任何「我幫你加 ports: - '5432:5432'」的建議都要拒絕，那等於把資料庫直接擺在網路上。
3. **不要在 Cloudflare Tunnel 開著的時候不設 BASIC_AUTH**。詳見下一段。

### 想從手機 / 別台機器測試？走 Cloudflare Tunnel + BASIC_AUTH

純 localhost 不夠用的場景（例：要從手機觸發 webhook、要 demo 給客戶看、要接外部 API callback），**正確路線**：

1. 雙擊 `tunnel-quick.command`（Mac）或 `tunnel-quick.bat`（Win）→ 給你一個 `https://*.trycloudflare.com` 公開 URL
2. **務必先在 `.env` 設 BASIC_AUTH 三行**（範本已預留為註解，把開頭 `#` 拿掉）：

   ```
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=your_username
   N8N_BASIC_AUTH_PASSWORD=replace_with_strong_password
   ```

3. 重啟容器（`stop.command` → `start.command`）讓設定生效

這樣即使 Tunnel URL 被自動掃描程式探測到（trycloudflare 子網段已知會被掃），攻擊者仍會被 Basic Auth 擋在 Owner Account 之前。**不設 BASIC_AUTH 就開 Tunnel = 把無密碼 n8n 推到全球網際網路**。

### Tunnel 用完記得關

`tunnel-quick.command` 開的 Tunnel 持續到你關 cloudflared process 為止。**Demo 完務必關**（在 Terminal 視窗按 `Ctrl+C`），避免幾天後忘記、Tunnel URL 流外。

### 我怎麼知道現在 n8n 的曝露狀態？

```bash
# Mac/Linux：看 5678 port 綁誰
lsof -nP -iTCP:5678 -sTCP:LISTEN

# 預期（v1.0.1 安全狀態）：TCP 127.0.0.1:5678 (LISTEN)
# 危險狀態：TCP *:5678 (LISTEN) 或 0.0.0.0:5678
```

```bash
# 看 Docker container 的 port binding
docker inspect $(docker ps -q --filter name=n8n) --format '{{json .HostConfig.PortBindings}}'

# 預期（v1.0.1 安全狀態）：{"5678/tcp":[{"HostIp":"127.0.0.1","HostPort":"5678"}]}
# 危險狀態：{"HostIp":"","HostPort":"5678"}（HostIp 空 = 0.0.0.0）
```

## 資料儲存位置

| 項目 | 位置 | 備註 |
|---|---|---|
| n8n workflows + credentials | Docker volume `n8n_data` | 跟著 Docker 走，不在你看得到的硬碟資料夾 |
| n8n 資料庫（PostgreSQL） | Docker volume `postgres_data` | 同上 |
| **本機檔案 / 待處理素材** | `./shared/` | 你直接看得到、可拖檔進去給 Watch Folder 觸發 |

升級或重啟 Docker Desktop **不會丟資料**。
**唯有 `docker compose down -v`（加 `-v` 旗標）會刪 volumes**，`stop.command` 不會碰 volumes。

## 如果想自訂

- **改埠號**（5678 被佔用時）：編輯 `n8n-compose.yml` 的 `ports: - '127.0.0.1:5678:5678'`，把中間的 5678 改成其他（如 `'127.0.0.1:5680:5678'`），重啟後改用 <http://localhost:5680>。**保留 `127.0.0.1:` 前綴**，否則會把 n8n editor 暴露到全網卡（公開 wifi 同網段他人可未授權登入）
- **改本機掛載資料夾**：編輯 `n8n-compose.yml` 的 `- ./shared:/files/shared`，把 `./shared` 改成你要掛的路徑
- **改時區 / 密碼 / Webhook URL**：編輯 `.env`，重啟容器（雙擊 stop 再 start）

## 變更紀錄

### v1.0.2（2026-05-07）

**安全強化（接續 v1.0.1）**：補完整安全設定文件 + 啟用 BASIC_AUTH 通道。

- 新增 README「安全設定」章節：預設安全組合 / 三條紅線（不要做的事）/ Cloudflare Tunnel 對外路線 / 自我檢測指令
- `.env.example`：新增 BASIC_AUTH 三行（`N8N_BASIC_AUTH_ACTIVE` / `_USER` / `_PASSWORD`）預留為註解，學員開 Cloudflare Tunnel 對外時 uncomment 即生效
- `n8n-compose.yml`：BASIC_AUTH 環境變數從 hardcoded `false` 改成讀 `.env`（`${N8N_BASIC_AUTH_ACTIVE:-false}` 等）— 之前學員即使在 .env 改也不會生效

教學體驗：純 localhost 使用零變化；要對外暴露的進階學員多一條安全路線。

### v1.0.1（2026-05-07）

**安全修補**：將 n8n editor 限制為本機存取。

- `n8n-compose.yml`：`ports: - '5678:5678'` → `ports: - '127.0.0.1:5678:5678'`
- 影響：學員瀏覽器仍可正常開 <http://localhost:5678>（教學體驗零差別）；公開 wifi / 共享辦公室 / 咖啡店同網段他人無法連到你的 n8n。
- 已下載 v1.0 舊版的學員：建議先 `docker compose down`，重下本 zip 覆蓋，重新雙擊 `start.command`。Owner Account 與 workflows 存在 Docker volume，不會因為換資料夾而丟。

### v1.0（2026-04-27）

初版：n8n 2.17.8 + PostgreSQL 16，Mac/Win 雙平台啟動腳本，Cloudflare Quick Tunnel 一鍵對外，shared/ 資料夾掛載。


## 授權提醒（兩條獨立判斷）

### 1. n8n Community Edition — Sustainable Use License (SUL)

採 [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/)，**重點是用途**（不是組織規模）：

- ✅ 允許：自架使用、教學、內部商業流程、用 n8n 為客戶接顧問案
- ❌ 禁止：把 n8n 代管成 SaaS、white-label 給其他客戶、嵌入產品對外販售

### 2. Docker Desktop — 免費資格依 Docker 條款

跟 n8n SUL 是**獨立**的兩條規則：

- 個人、教育、小型企業使用通常免費
- 大型企業、政府機關等請依 [Docker Personal 條款](https://www.docker.com/products/personal/) 自行判斷是否需付費訂閱

工作坊範圍內的個人/教學/小型團隊使用，兩條規則通常都在免費範圍內。若你的組織不確定資格，請逐項對照各自的官方文件。
