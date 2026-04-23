---
slug: n8n
unit_id: m1-1-launch
title: 啟動 n8n 並完成首次設定
course_type: skill-operation
duration: 15 min
learning_objective: 能用試跑包雙擊腳本啟動 n8n，在 localhost:5678 建立 Owner Account，並跑通一個 Webhook hello-world
prerequisites: [m1-1-install]
style_guide: _outlines/_style_guide_template.md
platform_version: Docker Desktop 4.x / n8n latest (Docker image n8nio/n8n)
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱裝完 Docker Desktop，看到鯨魚圖示在右上角發著綠光，但畫面打開只看到一個空空的 Containers 列表。

「然後呢？n8n 在哪？」他問雯姊。

雯姊把試跑包資料夾傳給他：「下載解壓，雙擊 `start.command`，剩下交給它。」

本單元 15 分鐘，目標是讓 n8n 從「沒裝」變成「localhost:5678 跑得出主介面 + Webhook 節點亮綠燈」。**全程不需要打任何 docker 指令**——一鍵腳本會幫你做。但你需要知道腳本背後做了什麼，這樣以後出問題能自己排查。

### 概念 / Concepts

- **Docker Compose** — 用一份 yaml 檔描述「要跑哪幾個容器、它們怎麼連、用什麼設定」的工具；本課程的 `n8n-compose.yml` 就是這份描述
- **試跑包（Starter Kit）** — 課程預先準備的「整套可跑的設定 + 一鍵腳本」，把 yaml、環境變數範本、雙擊腳本都包好
- **`.env` 檔** — 環境變數設定檔，存密碼、時區、URL 等敏感或會變動的值；Compose 啟動時自動讀取
- **Volume（資料卷）** — Docker 用來持久化資料的機制；你的 n8n workflows 與 credentials 存在 volume 裡，停容器再啟不會消失
- **Owner Account** — n8n 第一次開啟會引導建立的管理者帳號，**只存在你本機**，不需真的去收驗證信

### 操作示範 / Demo

#### 步驟 1：下載試跑包

從課程網頁「下載 n8n-starter-kit」連結拉一份 zip，解壓到你方便管理的位置。建議放在家目錄底下，例如：

- Mac：`~/n8n-starter-kit/`
- Win：`C:\Users\你的名字\n8n-starter-kit\`

**預期看到資料夾內含**：

```
n8n-starter-kit/
├── n8n-compose.yml      ← Docker Compose 配置
├── .env.example         ← 環境變數範本
├── README.md            ← 說明書
├── start.command        ← Mac 啟動
├── start.bat            ← Win 啟動
├── stop.command         ← Mac 停止
├── stop.bat             ← Win 停止
├── update.command       ← Mac 升級
├── update.bat           ← Win 升級
└── shared/              ← 本機掛載資料夾（Module 3 會用到）
```

#### 步驟 2：第一次啟動（會自動建 .env）

**Mac**：在 Finder 進入 `n8n-starter-kit` 資料夾，**雙擊** `start.command`

**Win**：在檔案總管進入 `n8n-starter-kit` 資料夾，**雙擊** `start.bat`

**Mac 第一次雙擊會被擋**：跳出「無法打開，因為來自未識別的開發者」是正常 macOS 安全機制：

1. 開「系統設定 → 隱私權與安全性」
2. 捲到「安全性」區塊，看到「`start.command` 已被阻擋使用」
3. 按「**強制打開**」→ 輸入密碼確認
4. 之後同一檔案不會再被擋

**預期看到什麼**：第一次跑會自動把 `.env.example` 複製為 `.env`，並打開 TextEdit / 記事本讓你編輯，同時跳出提示「請修改 POSTGRES_PASSWORD 為強密碼後存檔」

#### 步驟 3：改 .env 密碼

`.env` 檔內容會像這樣：

```
GENERIC_TIMEZONE=Asia/Taipei
POSTGRES_USER=n8n
POSTGRES_PASSWORD=please_change_me_to_a_strong_password
POSTGRES_DB=n8n
WEBHOOK_URL=http://localhost:5678/
N8N_HOST=localhost
N8N_PROTOCOL=http
```

把 `POSTGRES_PASSWORD` 那行的值改成你自己的強密碼（建議 16 字元以上，混合英數字符），例如：

```
POSTGRES_PASSWORD=NongYiXia_n8n_2026!
```

**注意**：這密碼只用在你本機 PostgreSQL，不需要記住給別人，但不要用 `password` 之類的弱密碼。

存檔關掉編輯器。

#### 步驟 4：再次雙擊 start

回到 `n8n-starter-kit` 資料夾，再次雙擊 `start.command` / `start.bat`

**預期看到什麼**：終端機跳出來，顯示一連串日誌：

```
正在啟動 n8n（首次需下載 image，可能花 1-5 分鐘）...
[+] Pulling 12/12
 ✔ postgres 16 image 下載完成
 ✔ n8nio/n8n latest image 下載完成
[+] Running 3/3
 ✔ Network n8n-starter-kit_default  Created
 ✔ Container n8n-starter-kit-postgres-1  Started
 ✔ Container n8n-starter-kit-n8n-1       Started
等候 n8n 服務就緒...
```

過約 30 秒到 1 分鐘（首次更久），瀏覽器自動開到 <http://localhost:5678>

**如果瀏覽器沒自動開**：手動開瀏覽器輸入 `http://localhost:5678`

#### 步驟 5：建立 Owner Account

n8n 第一次開會引導你建：

- **Email**：可以填假信箱（例如 `me@local.local`），**不會真的寄信**驗證
- **First Name / Last Name**：隨意
- **Password**：自訂（至少 8 字元、含大小寫與數字）

按 Next → 跳過後續行銷問卷（Skip）→ 進入 n8n 主介面

**預期看到什麼**：左側選單有 Workflows / Credentials / Executions / Templates；中央區塊空白或有「Create your first workflow」按鈕

#### 步驟 6：跑 Webhook hello-world 驗證

按「**Create Workflow**」進入空白編輯器：

1. 點 canvas 中央的「+」加節點
2. 搜尋 **Webhook**，選 **Webhook** trigger 節點
3. 節點設定面板：
   - **HTTP Method**：GET
   - **Path**：`hello`（任意名稱）
   - 其他保留預設
4. 按 **Listen for test event**（節點變藍色等候狀態）
5. **複製 Test URL**（會像 `http://localhost:5678/webhook-test/hello`）
6. 開新分頁貼上 URL 按 Enter

**預期看到什麼**：

- 瀏覽器頁面顯示 `Workflow was started`
- 回到 n8n 編輯器，Webhook 節點變綠色，下方 Output 顯示收到的請求資料（headers、query、body）

恭喜，你的 n8n 從零跑到「能接收外部請求」只花了 15 分鐘。

---

#### 進階：手動指令速查（給想懂背後在做什麼的人）

雙擊腳本背後的指令是 docker compose。如果你想直接在終端機操作（cd 到 `n8n-starter-kit/` 後）：

```
docker compose up -d         # 啟動所有服務（背景跑）
docker compose down          # 停止所有服務（資料保留）
docker compose down -v       # 停止 + 刪 volumes（資料全清，謹慎）
docker compose pull          # 拉最新 image
docker compose logs n8n -f   # 看 n8n 即時日誌（Ctrl+C 退出）
docker compose ps            # 看跑中的容器狀態
```

**怎麼開終端機並 cd 到資料夾**：
- **Mac**：在 Finder 對 `n8n-starter-kit` 資料夾按右鍵 → 服務 → 「新終端機（位於資料夾位置）」（要先在系統設定 → 鍵盤 → 鍵盤快速鍵 → 服務啟用）
- **Win**：在檔案總管網址列輸入 `cmd` 按 Enter，會直接以該資料夾為位置開 cmd

### 動手 / Hands-on

跟著步驟 1-6 走完，最終要看到 n8n Webhook 節點亮綠燈 + 收到測試請求

### 檢核 / Verification

到 n8n 介面確認以下 4 件事都成立：

- [ ] 左上角看到「My workflow」（你建的工作流）
- [ ] Webhook 節點是綠色，不是紅色或灰色
- [ ] Output 面板看得到 `headers`、`query`、`body` 的資料結構
- [ ] 左側 Executions 選單能看到剛才的執行紀錄

四個全過，1.1.2 完成，可以進 1.2 Cloudflare Tunnel。

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：skill-operation

- 不需要學員自備 credential
- Node 組成：Webhook trigger（單節點，純驗證）
- 試跑包提供：
  - `n8n-starter-kit.zip`（含本單元提到的所有檔案）
  - 下載連結放在講義頁顯眼位置（建議 Hero 區塊）
- 講義頁需提供：
  - 步驟 5 Owner Account 設定畫面截圖
  - 步驟 6 Webhook 節點設定截圖
  - 「Workflow was started」成功畫面截圖
- 講師端準備：
  - 預先在自己電腦跑過一次，確認試跑包可用
  - 備援：如果學員下載過慢，提供 USB 隨身碟複製

---

## 商業情境案例（Case）

**角色**：阿凱（27 歲，行銷專員）
**公司**：弄一下行銷工作室
**任務**：阿凱要把 n8n 從零跑起來，建立第一個能接外部請求的 Webhook 節點，作為後續 1.2 Cloudflare Tunnel 對外公開的基礎
**本單元要他學會**：用試跑包一鍵啟動、看懂 .env 為什麼要改、知道 Docker volumes 怎麼保存資料、跑通最小驗證流程

---

## 動手練習題（Hands-on Exercise）

**題目**：完成步驟 1-6，最終在 n8n 編輯器看到 Webhook 節點變綠 + Output 顯示收到的請求資料

**預期成果**：n8n 編輯器截圖，包含：
- 一個綠色的 Webhook 節點
- Output 面板顯示 JSON 格式的 headers / query / body

**完成標準**（self-check）：
- [ ] localhost:5678 開得起來且看到 n8n 主介面
- [ ] Owner Account 建立完成（左下角頭像點開能看到自己 email）
- [ ] Webhook 節點 Test URL 用瀏覽器打過去看到 "Workflow was started"
- [ ] 回到 n8n 編輯器，節點變綠色 + Output 有資料

---

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：雙擊 `start.command` 跳出「無法打開，因為來自未識別的開發者」
   **原因**：macOS Gatekeeper 第一次擋未簽署的 .command 檔
   **解法**：開「系統設定 → 隱私權與安全性 → 安全性」捲到底，看到被擋的 `start.command`，按「強制打開」→ 輸入密碼。之後同一檔案不會再被擋。詳見 1.1.3 troubleshoot 案 6

2. **錯誤現象**：start 腳本跑完，瀏覽器打開 localhost:5678 顯示「無法連線」或 ERR_CONNECTION_REFUSED
   **原因**：n8n 容器還在啟動中（首次拉 image 較慢），或 5678 埠被其他程式佔用
   **解法**：等 30-60 秒重試；仍不行去 1.1.3 troubleshoot 案 5（容器在跑但連不上）或案 2（埠被佔用）

3. **錯誤現象**：Owner Account 建好之後，下次重啟 Docker Desktop 發現 workflows 不見了
   **原因**：之前用 `docker compose down -v` 而非 `docker compose down`，`-v` 會刪 volume 連帶刪資料
   **解法**：本課程的 `stop.command` / `stop.bat` 都是用 `down`（不加 -v），只要用這兩個檔停就不會丟資料；想清掉重來才用 `down -v`。詳見 1.1.3 troubleshoot 案 8

---

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：n8n 的 workflows 與 credentials 實際存在哪裡？
- [ ] A. `~/n8n-starter-kit/` 資料夾的某個檔案
- [ ] B. `.env` 檔
- [ ] C. Docker volume `n8n_data`（不在你看得到的硬碟資料夾）←（正確答案）
- [ ] D. PostgreSQL 容器的記憶體

**Q2（應用驗證）**：阿凱想把 n8n 升級到最新版本，但又怕升級後 workflows 不見。他應該怎麼做？
- 預期答案要點：
  - 雙擊 `update.command` / `update.bat`（背後跑 `docker compose pull && up -d`）
  - 升級不會碰 volumes，workflows 會延續
  - 切忌跑 `docker compose down -v`（會刪 volumes）
