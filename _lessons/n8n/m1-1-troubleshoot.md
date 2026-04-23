---
slug: n8n
unit_id: m1-1-troubleshoot
title: 常見錯誤排查手冊
course_type: skill-operation
duration: 10 min
learning_objective: 能對照 8 大常見錯誤的症狀自助定位錯誤層級，並套用對應修復步驟，卡死時知道貼哪 3 行診斷給講師
prerequisites: []
style_guide: _outlines/_style_guide_template.md
platform_version: Docker Desktop 4.x / n8n latest (Docker image n8nio/n8n)
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱跑完 `start.command`，等了 30 秒，瀏覽器跳出來顯示 ERR_CONNECTION_REFUSED。

「卡了。」他打開課程頁，點進 1.1.3。

「你想知道的不是『怎麼修這個錯』，而是**怎麼找出錯在哪一層**。」雯姊在旁邊說。

本單元 10 分鐘，目標不是讓你背 8 個解法，而是讓你建立**分層診斷的思維**——以後遇到沒見過的錯誤，也能自己定位。

### 概念 / Concepts

- **分層診斷思維** — 從最外層往內查：使用者瀏覽器 → 網路 → 容器 → Docker Engine → 作業系統。每層都有自己的診斷指令，逐層排除
- **症狀 vs 原因** — 同一個症狀（localhost:5678 連不上）可能對應不同原因（容器沒起 / 埠被佔 / 防火牆擋）。先收集症狀，再下結論
- **三行診斷** — 卡住時跑這三個指令，輸出貼給講師最有效率：

```
docker ps                          # 看容器是否在跑
docker compose logs n8n --tail 50  # 看 n8n 最近的錯誤日誌
docker compose config              # 驗證 compose 設定是否解析正確
```

### 操作示範 / Demo — 8 案排錯目錄

依你看到的症狀找對應案號跳查。每案結構：症狀 → 診斷 → 修復。

---

#### 案 1：Docker Desktop 沒開 / 啟動中卡住

**症狀**：跑 `start.command` / `start.bat` 跳出對話框「Docker Desktop 未啟動」；或鯨魚圖示顯示 Starting 一直不變綠燈

**診斷**：
- 看選單列 / 通知列鯨魚圖示狀態：Running（綠）/ Starting（黃）/ Stopped（紅）
- 點開 Docker Desktop 主視窗看 Dashboard 是否載入
- 終端機跑 `docker info`，應看到一大段系統資訊（不是錯誤）

**修復**：
- 紅燈 → 手動點 Docker Desktop 啟動
- 黃燈卡 5 分鐘以上 → Docker Desktop 選單「Restart」
- 還是卡 → Quit Docker Desktop → 重開
- 仍不行 → Mac 重開機 / Win 重啟並確認 WSL2 是 v2

---

#### 案 2：5678 埠被佔用

**症狀**：start 腳本跳錯 `Bind for 0.0.0.0:5678 failed: port is already allocated`；或 localhost:5678 開出來不是 n8n 而是別的服務

**診斷**：

Mac / Linux 終端機：
```
lsof -i :5678
```

Win PowerShell：
```
netstat -ano | findstr :5678
```

會列出佔用 5678 的程式 PID。

**修復**：

兩種解法二選一：

**解法 A：關掉佔用程式**
- Mac：`kill -9 PID`（PID 換成上面查到的數字）
- Win：工作管理員 → 詳細資料 → 找到 PID 對應程式右鍵結束工作

**解法 B：改 n8n 用其他埠**

編輯 `n8n-compose.yml`，把：

```
    ports:
      - '5678:5678'
```

改成（例如改用 5680）：

```
    ports:
      - '5680:5678'
```

冒號**前面**的數字是你電腦對外的埠，**後面** 5678 是容器內 n8n 的埠（不要動）。改完雙擊 `stop` 再 `start`，之後改用 <http://localhost:5680> 連線。

---

#### 案 3：Apple Silicon platform mismatch 警告

**症狀**：Apple Silicon Mac 跑容器看到黃色警告 `The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)`

**診斷**：
- 跑 `docker info` 看 `Architecture` 欄位，Apple Silicon 應顯示 `aarch64`
- 警告的 image 是 x86 架構，沒有原生 ARM 版本

**修復**：
- 本課程的 `n8nio/n8n` 與 `postgres:16` 都有原生 ARM 版本，**不會**出現此警告
- 若你跑其他 image 看到此警告，影響不大（Rosetta 自動翻譯，效能稍降約 30%）
- 想抑制警告 → 在 compose 服務下加 `platform: linux/amd64` 明示用 x86，或找原生 ARM 版本的 image

---

#### 案 4：Win WSL2 未啟用 / 版本太舊

**症狀**：Docker Desktop 啟動後一直 Starting 不變綠燈；或安裝時跳錯「WSL2 installation is incomplete」

**診斷**：

PowerShell（系統管理員）跑：

```
wsl --status
```

預期看到 `預設版本: 2`。看到 `預設版本: 1` 或找不到指令就要修。

**修復**：

依序試：

1. **強制升級 WSL 核心**：

   ```
   wsl --update
   ```

2. **設定預設版本為 2**：

   ```
   wsl --set-default-version 2
   ```

3. **沒裝過 WSL**：

   ```
   wsl --install
   ```

   完成會要求重啟。

4. **跳「需要啟用虛擬化」**：到工作管理員 → 效能 → CPU 看「虛擬化」是否「已啟用」。沒啟用要進 BIOS 開（重開機按 F2/Del/Esc，找 `Intel VT-x` / `AMD-V` / `SVM Mode` 啟用 → 存檔重啟）

---

#### 案 5：容器在跑但 localhost:5678 連不上

**症狀**：`docker ps` 看到 n8n 容器 status 是 `Up`，但瀏覽器開 localhost:5678 顯示 ERR_CONNECTION_REFUSED 或一直轉

**診斷**：

```
docker compose logs n8n --tail 50
```

看是否有 startup error。常見是 PostgreSQL 連線失敗。

```
docker compose ps
```

確認 postgres 與 n8n 兩個容器都是 `Up (healthy)`，不是 `Restarting` 或 `Up (unhealthy)`。

**修復**：
- postgres 顯示 `Restarting`：通常是密碼設定衝突。停服務 → 刪 volume `docker compose down -v`（**會清資料，請確認**）→ 重新 `start.command`，會用 `.env` 的密碼重建
- n8n 日誌出現 `getaddrinfo EAI_AGAIN postgres`：postgres 還沒就緒，等 30 秒重整 `docker compose restart n8n`
- 兩容器都正常但網頁仍連不上：檢查防火牆是否擋 5678（macOS 系統設定 → 網路 → 防火牆 / Win 防火牆設定）

---

#### 案 6：macOS `start.command` 被 Gatekeeper 擋

**症狀**：雙擊 `start.command` 跳出「無法打開"start.command"，因為它來自未識別的開發者」

**診斷**：這是 macOS Gatekeeper 第一次擋未簽署的執行檔，**不是檔案壞了**。

**修復**：

1. 開「**系統設定 → 隱私權與安全性**」
2. 捲到「**安全性**」區塊
3. 看到「`start.command` 已被阻擋使用」
4. 按「**強制打開**」→ 輸入密碼確認
5. 再次雙擊 `start.command` 就會跑

`stop.command` / `update.command` 第一次也會被擋，做同樣處理即可。之後同檔不會再擋。

---

#### 案 7：本機資料夾掛載權限錯誤（macOS）

**症狀**：Module 3 跑 Watch Folder 觸發失敗；或 n8n 日誌出現 `EACCES: permission denied` 對 `/files/shared` 的存取

**診斷**：
- 在 `n8n-starter-kit/shared/` 放一個測試檔，看 n8n 容器能不能讀
- macOS 可能在背景擋住 Docker Desktop 對某些資料夾的存取（Files & Folders 權限）

**修復**：

1. 開「**系統設定 → 隱私權與安全性 → 檔案與資料夾**」
2. 找「Docker Desktop」（沒看到的話往下找「完整磁碟存取權」）
3. 確認你的 `n8n-starter-kit` 所在資料夾的權限有勾選
4. 不確定就把整個「桌面」「文件」「下載」都勾起來
5. 重啟 Docker Desktop

如果問題在 Docker Desktop 設定本身，去 Docker Desktop → Settings → Resources → File sharing 確認 `n8n-starter-kit` 的父目錄在白名單

---

#### 案 8：升級後 workflow 不見

**症狀**：跑 `update.command` 之後重新登入 n8n，發現之前建的 workflows 全消失，回到「Create your first workflow」狀態

**診斷**：
- 跑 `docker volume ls` 確認 `n8n-starter-kit_n8n_data` 還在
- 還在但 workflow 不見：可能不小心建了新的 Owner Account，n8n 把你導向新帳號的空間
- 不在了：之前用過 `docker compose down -v`（`-v` 會刪 volumes）

**修復**：

- volume 還在 → 確認登入的 Owner email 跟之前一樣（n8n 1 個 instance 1 個 owner）
- volume 不在了 → 救不回來；以後**只用 `stop.command`**（背後是 `docker compose down`，不刪 volume），不要手動跑 `down -v`

**預防**：
- 升級用 `update.command`（拉 image + 重啟，不碰 volume）
- 停服務用 `stop.command`（不刪資料）
- 想全部清掉重來才手動跑 `docker compose down -v`

---

### 動手 / Hands-on

**任務**：故意製造一個埠衝突，依案 2 的步驟修復

**步驟**：
1. 確認 n8n 已停止（雙擊 `stop.command` / `stop.bat`）
2. 開另一個終端機跑 `python3 -m http.server 5678`（會在 5678 起一個假伺服器佔用埠）
3. 雙擊 `start.command` / `start.bat`
4. 應該會跳錯 `port is already allocated`
5. 依案 2 解法 B 修：把 compose 改成 `5680:5678`
6. 雙擊 start，應該成功啟動
7. 開 <http://localhost:5680> 應看到 n8n
8. 修完後關掉 python 假伺服器（Ctrl+C），把 compose 改回 `5678:5678`

### 檢核 / Verification

學完本單元的指標：

- [ ] 看到 ERR_CONNECTION_REFUSED 能說出**至少 2 個**可能原因（容器沒起 / 埠被佔 / 防火牆擋）
- [ ] 知道遇到不熟錯誤時要跑哪 3 行診斷指令
- [ ] 知道 `docker compose down` 與 `down -v` 的差別
- [ ] 動手做完埠衝突修復練習

四項全過，1.1 完成，可以進 1.2 Cloudflare Tunnel。

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：skill-operation（排錯導向）

- 不需要學員自備 credential
- 講師端準備：
  - 一份「**錯誤範例展示包**」：預先製作的 5678 埠佔用腳本、模擬權限錯誤的測試檔等，讓學員能在受控環境練排錯
  - 8 案的截圖/螢幕錄影：每案的症狀畫面，以便講義頁與簡報使用
  - 「三行診斷」貼紙或速查卡（實體或數位），課程結束後給學員帶走

---

## 商業情境案例（Case）

**角色**：阿凱（27 歲，行銷專員，已裝完 Docker Desktop 並跑過 `start.command`）
**公司**：弄一下行銷工作室
**任務**：阿凱跑 start 後瀏覽器顯示 ERR_CONNECTION_REFUSED，要在不打擾講師的前提下自己定位錯誤
**本單元要他學會**：建立分層診斷思維（不是死記解法），知道 8 大常見錯誤的症狀對照，能跑三行診斷指令收集資訊

---

## 動手練習題（Hands-on Exercise）

**題目**：依「動手 / Hands-on」的 8 步驟，模擬製造一個 5678 埠衝突，並依案 2 解法 B 完成修復

**預期成果**：
- 練習過程中拍下「跳錯訊息」「修改後的 compose 檔」「成功跑起來的 localhost:5680」三張截圖
- 寫下「以後遇到埠衝突，我會先做 _____，再 _____」的兩步流程

**完成標準**（self-check）：
- [ ] 能在終端機看到 `port is already allocated` 錯誤
- [ ] 改完 compose 檔後 `start.command` 成功啟動
- [ ] localhost:5680 看到 n8n 主介面
- [ ] 練習完後把 compose 改回 5678:5678 並停掉假伺服器

---

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：學員看到任何錯誤訊息就直接舉手問講師，沒先跑三行診斷
   **原因**：覺得錯誤訊息太長看不懂，習慣性求助
   **解法**：本課程強制把「三行診斷」做成貼紙貼在試跑包資料夾旁；卡住時**先跑三行存下輸出**，再決定是自查還是問人。多數情況看 logs 第一行就找得到答案

2. **錯誤現象**：學員為了「修錯」直接跑 `docker compose down -v`，結果把 workflows 全清掉
   **原因**：沒注意 `-v` 旗標的意義，只想著「重來一次」
   **解法**：本單元案 8 已強調；加上講師示範時刻意讓學員看「down」與「down -v」的差異——前者只停容器，後者連 volumes 一起刪

3. **錯誤現象**：Win 學員跑 `wsl --status` 顯示一切正常，但 Docker Desktop 還是卡 Starting
   **原因**：WSL 核心版本太舊，`--status` 沒抓到問題
   **解法**：直接跑 `wsl --update` 強制升級，多數情況解決；仍不行的可能是企業電腦群組原則擋住，需找 IT

---

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：「分層診斷思維」中，看到 ERR_CONNECTION_REFUSED 應該**先**檢查哪一層？
- [ ] A. 防火牆設定
- [ ] B. n8n 設定檔內容
- [ ] C. Docker 容器是否在跑（用 `docker ps`）←（正確答案，從外層症狀切入最內層執行狀態，先確認容器在不在跑）
- [ ] D. 重新安裝 Docker Desktop

**Q2（應用驗證）**：雯姊跑 `update.command` 後發現 workflows 全部消失。可能原因與下次該怎麼做？
- 預期答案要點：
  - 可能原因：之前曾跑過 `docker compose down -v`（-v 旗標會刪 volumes 連同資料）
  - 下次預防：只用 `stop.command`（不加 -v）停服務；想清掉重來才手動跑 `down -v`
  - 一旦 volumes 被刪資料無法救回；建議重要 workflows 用 n8n 內建 Export 功能定期備份成 JSON
