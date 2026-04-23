---
slug: n8n
unit_id: m1-1-install
title: Docker Desktop 安裝（Mac / Windows 雙平台）
course_type: skill-operation
duration: 25 min
learning_objective: 能依自己的 OS 與 CPU 架構完成 Docker Desktop 安裝，並在終端機跑 docker --version 看到版本號
prerequisites: [m1-1-overview]
style_guide: _outlines/_style_guide_template.md
platform_version: Docker Desktop 4.x
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱的 MacBook 是 M2 晶片，剛剛在 1.1.0 確認自己屬於路徑 B（Mac Apple Silicon）。他打開 docker.com，看到首頁上面有兩個藍色按鈕：「Download for Mac (Apple Silicon)」和「Download for Mac (Intel)」。

「還好有先看 1.1.0，不然我可能會點錯。」他點下 Apple Silicon 版本的 .dmg，旁邊雯姊也點開自己的 Intel iMac 對應版本。

本單元 25 分鐘，目標是把 Docker Desktop 從零裝到「終端機跑 `docker --version` 吐得出版本號」。

### 概念 / Concepts

- **Docker Desktop** — 一個桌面應用，包含 Docker Engine（跑容器的核心）+ 圖形管理介面 + 自動更新機制；裝它就等於同時裝完 Docker 全家桶
- **WSL2（Windows Subsystem for Linux 2）** — Win 上跑 Linux 容器需要的底層；Docker Desktop on Win 預設用 WSL2 作為 Engine 後端
- **虛擬化（Virtualization）** — CPU 提供的硬體支援，讓電腦能跑容器；Mac 預設開啟、Win 多數機種預設開啟（少數需進 BIOS 開）
- **Apple Silicon vs Intel** — 兩種 CPU 架構各自需要對應版本的 Docker Desktop，下錯版本裝完會跑不起來

### 操作示範 / Demo

選你對應的路徑跟著走。3 條路徑互相獨立，看自己的就好。

---

#### 路徑 A：Mac Intel（2020 之前的 Mac）

**步驟 1**：開瀏覽器到 <https://www.docker.com/products/docker-desktop/>

**預期看到什麼**：頁面中央有「Download Docker Desktop」按鈕，下方列出 Mac / Win / Linux 三個分頁

**步驟 2**：點 Mac 分頁 → 選 **「Mac with Intel chip」**（**不是** Apple Silicon）

**預期看到什麼**：開始下載 `Docker.dmg`（約 600MB），下載要 1-3 分鐘看你網速

**步驟 3**：下載完成雙擊 `.dmg` 檔

**預期看到什麼**：彈出一個小視窗，左邊是 Docker 鯨魚圖示，右邊是 Applications 資料夾捷徑，中間箭頭

**步驟 4**：把鯨魚圖示拖曳到右邊 Applications

**預期看到什麼**：開始複製檔案的進度條，約 30 秒完成

**步驟 5**：到 Launchpad（或 Applications 資料夾）找「Docker」雙擊打開

**如果看到 "Docker.app" 是從網際網路下載的，你確定要打開嗎？**：點「打開」，這是 macOS Gatekeeper 第一次驗證

**預期看到什麼**：Docker Desktop 啟動畫面，要求授權 privileged helper（系統權限）

**步驟 6**：輸入 Mac 密碼授權 → 同意 service agreement → 跳過教學

**預期看到什麼**：右上角選單列出現鯨魚圖示，點開應該寫 **Docker Desktop is running**（綠燈）；視窗內顯示 dashboard，左邊有 Containers / Images / Volumes 等選單

**步驟 7（驗證）**：打開「終端機」（Cmd+Space 搜尋「終端機」），輸入：

```
docker --version
```

**預期看到什麼**：吐出類似 `Docker version 27.3.1, build ce12230` 的字串。**版本號數字不重要**，看到 `Docker version` 開頭就過關。

---

#### 路徑 B：Mac Apple Silicon（M1/M2/M3/M4）

**步驟 1**：開瀏覽器到 <https://www.docker.com/products/docker-desktop/>

**步驟 2**：點 Mac 分頁 → 選 **「Mac with Apple chip」**（**不是** Intel）

**步驟 3-7**：與路徑 A 完全相同（拖曳安裝、首次啟動授權、終端機驗證 `docker --version`）

**Apple Silicon 額外注意**：
- 部分 Linux 容器是 x86 架構，在 Apple Silicon 上會用 Rosetta 翻譯，跑起來會有「platform mismatch」黃色警告。**這不是錯誤**，本課程的 n8n 與 PostgreSQL 都有原生 ARM 版本，不會出現這警告
- 如果之後跑其他 image 出現此警告，到 1.1.3 troubleshoot 案 3 看怎麼處理

---

#### 路徑 C：Windows 10/11 + WSL2

**步驟 1（先檢查 WSL2 是否已啟用）**：

打開 PowerShell（**以系統管理員身分執行**：右鍵點開始 → 終端機（系統管理員）/ Windows PowerShell（系統管理員））輸入：

```
wsl --status
```

**預期看到什麼**：

- **已啟用且為 v2**：顯示 `預設版本: 2`（或英文 `Default Version: 2`）→ 跳到步驟 3
- **未啟用 / 顯示找不到指令**：繼續步驟 2

**步驟 2（啟用 WSL2）**：在系統管理員 PowerShell 輸入：

```
wsl --install
```

**預期看到什麼**：自動下載並安裝 WSL2 + Ubuntu 預設發行版，**完成後要求重新啟動電腦**

**重啟之後**：再次跑 `wsl --status` 確認顯示 `預設版本: 2`

**如果 wsl --install 跳出 "需要啟用虛擬化"**：到工作管理員 → 效能 → CPU，看右下角「虛擬化」是否「已啟用」。沒啟用要進 BIOS 開：開機按 `F2`/`Del`/`Esc`（依主機板），找 `Intel VT-x` / `AMD-V` / `SVM Mode` 啟用；不確定怎麼進 BIOS 搜「主機板型號 + 虛擬化 啟用」

**步驟 3**：開瀏覽器到 <https://www.docker.com/products/docker-desktop/>

**步驟 4**：點 Windows 分頁 → 「Download Docker Desktop for Windows」→ 下載 `Docker Desktop Installer.exe`（約 700MB）

**步驟 5**：雙擊 `.exe` 安裝精靈

**預期看到什麼**：精靈第一頁有兩個勾選框：「Use WSL 2 instead of Hyper-V (recommended)」**保持勾選**；「Add shortcut to desktop」依個人喜好

**步驟 6**：按 OK → 等安裝完成（約 3-5 分鐘）→ 提示「Close and restart」按下去重啟

**步驟 7**：重啟後 Docker Desktop 自動啟動

**首次啟動會跳**：service agreement 同意 → 登入帳號（**可跳過**，按右上角 Skip）→ 教學影片可跳

**預期看到什麼**：右下角通知列出現鯨魚圖示，狀態應為 **Docker Desktop is running**（綠燈）

**步驟 8（驗證）**：打開 PowerShell（不需系統管理員）輸入：

```
docker --version
```

**預期看到什麼**：吐出類似 `Docker version 27.3.1, build ce12230` 的字串

---

### 動手 / Hands-on

**任務**：依你在 1.1.0 確認的路徑（A/B/C），完成從下載 → 安裝 → 首次啟動 → 終端機驗證的全流程

**完成標準**：
1. 鯨魚圖示出現在 Mac 右上角選單列 / Win 右下角通知列
2. 狀態為 **Docker Desktop is running**（綠燈），不是 Starting（黃燈）或 Stopped（紅燈）
3. 終端機 / PowerShell 跑 `docker --version` 看到 `Docker version` 開頭的字串

**時間預期**：
- 下載：1-3 分鐘
- 安裝：2-5 分鐘
- 首次啟動 + 授權：1-3 分鐘
- 驗證：30 秒
- 總計約 5-12 分鐘（不含 Win 啟用 WSL2 與 BIOS 設定）

### 檢核 / Verification

打開終端機（Mac）/ PowerShell（Win）依序跑這 3 個指令，每個都要看到合理輸出：

```
docker --version          # 應吐出版本號
docker info               # 應看到一大串系統資訊（Server / Storage / Plugins）
docker run hello-world    # 應看到 "Hello from Docker!" 訊息
```

最後一個 `docker run hello-world` 是 Docker 官方的測試 image，跑起來會自動下載並執行一個迷你容器，印出歡迎訊息。看到 "Hello from Docker!" 表示**Docker Engine + 容器執行**整條鏈路都通了。

如果這 3 個指令任何一個出錯，跳 1.1.3 troubleshoot 對症下藥。

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：skill-operation

- 不需 credential
- 不需 node 設定
- 提供素材：
  - 3 條安裝路徑的截圖序列（Mac Intel / Apple Silicon / Win + WSL2 各 5-7 張關鍵畫面）
  - Docker 官網下載頁的最新位置標註（畫面標出兩個 Mac 下載按鈕的差異）
  - WSL2 啟用的 PowerShell 指令清單
- 講師端準備：
  - 一台示範用的 Mac + 一台示範用的 Win，現場交叉示範
  - 備援：如果現場 Wi-Fi 慢，提供 Docker Desktop 的離線安裝包 USB 隨身碟

---

## 商業情境案例（Case）

**角色**：阿凱（27 歲，行銷專員，Mac Apple Silicon M2）
**公司**：弄一下行銷工作室
**任務**：阿凱要把 Docker Desktop 裝起來，作為跑 n8n 的底層基礎建設
**本單元要他學會**：依自己的 CPU 架構選對下載版本、跑通官方驗證指令 `docker run hello-world`，知道「Docker 已經就位」

---

## 動手練習題（Hands-on Exercise）

**題目**：在你的電腦上，依路徑 A/B/C（你在 1.1.0 確認的）完成 Docker Desktop 安裝，並跑通三個驗證指令

**預期成果**：終端機 / PowerShell 視窗截圖，包含以下三個輸出：

```
$ docker --version
Docker version 27.x.x, build xxxxxxx

$ docker info
（一大段系統資訊）

$ docker run hello-world
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

**完成標準**（self-check）：
- [ ] 鯨魚圖示在選單列 / 通知列且狀態為 running（綠燈）
- [ ] `docker --version` 看到版本號
- [ ] `docker run hello-world` 看到 "Hello from Docker!" 訊息

---

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：Mac 下載到 Intel 版裝在 Apple Silicon 上（或反過來），啟動後鯨魚圖示一直 Starting 或顯示 corrupt
   **原因**：CPU 架構不符，安裝包跟硬體對不起來
   **解法**：到 Applications 把 Docker.app 丟垃圾桶 → 重新到 docker.com 下載對應晶片版本 → 重裝。判斷晶片：Apple → 關於這台 Mac → 晶片欄位

2. **錯誤現象**：Win 跑 `wsl --install` 顯示「需要啟用虛擬化」
   **原因**：CPU 虛擬化（Intel VT-x / AMD-V）在 BIOS 預設關閉
   **解法**：重開機按 `F2`/`Del`/`Esc` 進 BIOS（依主機板），在 Advanced / CPU Configuration 找 `Intel VT-x` / `AMD-V` / `SVM Mode` 啟用 → 存檔重啟 → 再跑 `wsl --install`。完整流程在 1.1.3 troubleshoot 案 4

3. **錯誤現象**：Win Docker Desktop 安裝完啟動，狀態一直 Starting 不變綠燈，過 10 分鐘還在轉
   **原因**：WSL2 後端沒裝好，或 Hyper-V 與 WSL2 衝突
   **解法**：先在 PowerShell 跑 `wsl --update`（強制升級 WSL 核心）→ 重啟 Docker Desktop。仍卡住跑 1.1.3 troubleshoot 案 4

---

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：跑 `docker run hello-world` 看到 "Hello from Docker!" 代表什麼？
- [ ] A. n8n 已經安裝完成
- [ ] B. Docker Engine 與容器執行整條鏈路都正常 ←（正確答案）
- [ ] C. 你的網路連得到 Docker Hub
- [ ] D. WSL2 已啟用

**Q2（應用驗證）**：雯姊用 Win 11，跑 `wsl --install` 顯示「需要啟用虛擬化」，她接下來該做什麼？
- 預期答案要點：
  - 先到工作管理員 → 效能 → CPU 確認「虛擬化」狀態（已啟用 / 已停用）
  - 已停用 → 重開機進 BIOS（按 F2/Del/Esc）找 `Intel VT-x` / `AMD-V` / `SVM Mode` 啟用 → 存檔重啟
  - 再跑 `wsl --install` 應該就過
