---
slug: n8n
unit_id: m1-1-overview
title: n8n 本機環境建置 · 流程總覽與前置檢查
course_type: skill-operation
duration: 10 min
learning_objective: 能說出自己屬於哪一條 Docker Desktop 安裝路徑（Mac Intel / Apple Silicon / Win + WSL2），並完成前置檢查清單
prerequisites: []
style_guide: _outlines/_style_guide_template.md
platform_version: Docker Desktop 4.x / n8n latest (Docker image n8nio/n8n)
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱這個月做了一檔 PDF 客戶資料抽取的活動，月初才到 12 號，Make 已經跑掉 800 ops，眼看月底還有兩週。他不想升級到 Make 付費版（一個月 $9 起跳，公司還要走採購流程），更不想把客戶 PDF 上傳到第三方 SaaS 處理。

雯姊跟他說：「你裝 n8n 在自己電腦跑，免費、跑幾次都不扣點，PDF 也不用離開你的硬碟。」

阿凱想：「聽起來很好，但 n8n 不是要會寫 code 才能裝嗎？」

不用。本單元的 10 分鐘，目標是讓你看完之後**知道自己接下來要走哪條路**——不是現在就要動手裝，是先把地圖看清楚。

### 概念 / Concepts

- **Docker** — 把一個「整包跑得起來的軟體環境」裝箱送到你電腦上的工具；你不用懂裡面，只要 Docker Desktop 開著，n8n 就能跑
- **Docker Desktop** — Docker 在 Mac / Win 上的桌面版本，有圖形介面（左上角會看到鯨魚圖示），不用打指令也能管容器
- **Docker Compose** — 把「要跑哪些容器、用什麼設定」寫成一份 yaml 檔，一個指令就把整組服務拉起來；本課程的試跑包就是一份寫好的 compose 檔
- **n8n Desktop App（已退役）** — n8n 官方曾經有 .dmg / .exe 的桌面版本，但 2025-08-15 已被官方封存（read-only），不再更新；本課程**不用**這個版本
- **n8n Community Edition** — n8n 的免費自架版本，跑在你自己電腦上，沒有執行次數限制，可以讀寫本機檔案

### 操作示範 / Demo

完整安裝旅程一共 4 步驟，本課程把 1.1 拆成 4 子單元，正好對應 4 步驟：

```
步驟 1：裝 Docker Desktop          ← 1.1.1 install
   ↓
步驟 2：下載試跑包，改 .env 密碼    ← 1.1.2 launch（前半）
   ↓
步驟 3：雙擊 start.command/.bat     ← 1.1.2 launch（後半）
   ↓
步驟 4：開 http://localhost:5678   ← 1.1.2 launch（驗證）
```

中間任何一步卡關 → 跳 1.1.3 troubleshoot 排錯手冊。

**3 條安裝路徑分流**

依你的電腦選一條走：

| 路徑 | 適用 | 大概會花多久 |
|---|---|---|
| **A. Mac Intel** | 2020 之前的 MacBook / iMac | 首次 30-40 分鐘 |
| **B. Mac Apple Silicon** | 2020 之後（M1/M2/M3/M4） | 首次 25-35 分鐘 |
| **C. Windows 10/11 + WSL2** | Win 10 Pro/Home 或 Win 11 | 首次 35-45 分鐘（含 WSL2 啟用） |

**判斷自己是 Intel 還 Apple Silicon**：點左上角 Apple → 「關於這台 Mac」，看「晶片」欄位。寫 `Apple M*` 的選 B，寫 `Intel Core *` 的選 A。

**Win 怎麼判斷**：開「設定 → 系統 → 系統資訊」看 Windows 版本。Win 10 1903 以前的版本不支援 WSL2，需要先升級。

### 動手 / Hands-on

**前置檢查清單**（依清單逐項打勾，全部過了才進 1.1.1）：

- [ ] **作業系統版本**：Mac 11 Big Sur 以上 / Win 10 build 19041 (1903) 以上
- [ ] **磁碟空間**：至少 8 GB 可用空間（Docker Desktop 約 2GB、n8n image 約 1GB、PostgreSQL image 約 500MB、預留資料成長）
- [ ] **記憶體**：至少 4GB 可給 Docker 用（系統設定有 16GB 比較舒服）
- [ ] **CPU 架構**：知道自己是 Intel / Apple Silicon / Win
- [ ] **舊版 Docker**：如果以前裝過 Docker Toolbox / 舊版 Docker Desktop，先到應用程式移除，避免衝突
- [ ] **虛擬化（Win 限定）**：到工作管理員 → 效能 → CPU，確認「虛擬化」顯示「已啟用」；沒啟用要進 BIOS 開（搜尋「主機板型號 + virtualization 啟用」）

**判斷你的時間預算**：

- 已經裝過 Docker Desktop 且還在運作 → 預期 5 分鐘進 1.1.2
- 完全沒裝過 Docker → 預期 30-45 分鐘走完 1.1.1 + 1.1.2
- Win 沒啟用 WSL2 → 額外加 10-15 分鐘

如果現場時間不夠跑完全程，先做完前置檢查清單，把實際安裝放到下課後依 1.1 系列子頁照走。

### 檢核 / Verification

跟旁邊的人（或自己對自己）說一遍：

1. 我這台電腦的安裝路徑是 A / B / C 哪一條
2. 我磁碟剩 _____ GB，超過 8GB 沒問題
3. 我有沒有裝過 Docker（已裝 / 沒裝）
4. 我預期會花 _____ 分鐘走完 1.1 全部子單元

說得出 4 個答案，就過。說不出來表示前置檢查還沒做完。

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：skill-operation（本單元為前置概念，無實作流程）

- 不需 credential
- 不需 node 設定
- 提供素材：
  - 1 張 4 步驟流程圖（可在講義頁用 SVG 或 ASCII 呈現）
  - 1 張 3 路徑分流表
  - 1 份前置檢查清單（可勾選）
- 學員不用啟動任何服務，純判讀

---

## 商業情境案例（Case）

**角色**：阿凱（27 歲，行銷專員）
**公司**：弄一下行銷工作室
**任務**：阿凱想找一個免費、不限次數、可以處理本機 PDF 的自動化工具，替代 Make 的 1000 ops 限制
**本單元要他學會**：在動手裝之前，先看清楚整段安裝旅程有幾步、自己屬於哪條路徑、需要先檢查什麼，避免裝到一半發現磁碟不夠或 Win 沒開虛擬化

---

## 動手練習題（Hands-on Exercise）

**題目**：用你現在這台電腦，完成本單元的「前置檢查清單」6 項檢查，並寫下：
1. 你的安裝路徑（A/B/C 三選一）
2. 你的磁碟剩餘空間
3. 你預期走完 1.1 全部子單元要花的分鐘數

**預期成果**：一張寫滿三個答案的便條紙（或記事 App），可以拍照存檔，作為自己的「準備好了」憑據

**完成標準**（self-check）：
- [ ] 6 項前置檢查全部勾完
- [ ] 知道自己屬於 A/B/C 哪條路徑（不是「應該是 B 吧」）
- [ ] 寫得出預期時間（不是「不知道」）

---

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：學員看到「裝 Docker Desktop」就慌，想跳過直接用 npx n8n
   **原因**：以為 Docker 很複雜，或聽說過 Docker 很吃資源
   **解法**：本課程的 Docker Desktop 啟動之後就跟「開另一個 App」一樣，平時用不到不會打擾你；npx n8n 雖然 30 秒能跑，但**資料不持久**（重啟易消失）、沒有 PostgreSQL 撐批次處理，Module 3 跑大量 PDF 會很痛苦

2. **錯誤現象**：Mac 用戶跳過「判斷 Intel / Apple Silicon」，直接下載官網第一個 .dmg
   **原因**：沒注意到官網有兩個下載按鈕
   **解法**：1.1.1 install 會明確分流；現在先到「關於這台 Mac」看「晶片」欄位，自己確認一次

3. **錯誤現象**：Win 用戶沒檢查虛擬化，到 Docker Desktop 安裝完才被擋下，回頭去 BIOS 開虛擬化又得重開機
   **原因**：BIOS 設定通常在開機按 F2/Del 才能進，臨時找不到資料會卡很久
   **解法**：本單元已列入前置檢查；Win 用戶**現在就**開工作管理員 → 效能 → CPU 看「虛擬化」是否「已啟用」

---

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：本課程**不**使用 n8n Desktop App 的原因是？
- [ ] A. Desktop App 太貴
- [ ] B. Desktop App 不能讀本機檔案
- [ ] C. Desktop App 已被 n8n 官方封存（2025-08-15 改 read-only），不再更新 ←（正確答案）
- [ ] D. Desktop App 不支援 Mac

**Q2（應用驗證）**：阿凱用 MacBook Pro M2，磁碟剩 12GB，從來沒裝過 Docker。他應該選哪條安裝路徑、預期花多少時間？
- 預期答案要點：
  - 路徑 B（Mac Apple Silicon）
  - 磁碟 12GB > 8GB 門檻，過關
  - 預期 25-35 分鐘走完 1.1.1 + 1.1.2（沒裝過 Docker）
