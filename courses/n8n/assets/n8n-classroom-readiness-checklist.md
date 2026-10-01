# AI 資料工廠｜課前環境門檻回傳表

**用途**：學員在課前 T-7 天完成一次，T-1 天再確認 Docker smoke test。講師依結果分成 PASS、CONDITIONAL、BLOCK，避免把整堂課耗在個別電腦的 BIOS、WSL2 或公司權限問題。

**課程核心**：Docker Desktop + Compose + n8n Community Edition。Gemma 4 + Ollama、Cloudflare Tunnel、Gemini API、Telegram 都是延伸能力，不是 Docker 入場門檻；核心課不要求 GPU。

## 1. 判定規則

| 結果 | 定義 | 課堂安排 |
|---|---|---|
| PASS | 核心規格、虛擬化、權限、網路與 Docker smoke test 全部有證據 | 用自己的電腦實作 |
| CONDITIONAL | 規格大致符合，但 Docker／WSL2／權限尚未完成驗證 | 觀摩或使用借用機／遠端備援 |
| BLOCK | OS/CPU 不支援、虛擬化被鎖、無法重開機／安裝，或 RAM／磁碟低於最低值 | 課前由 IT 解鎖、升級或更換設備 |

## 2. 核心硬性門檻

- **macOS**：依 Docker 官方「目前與前兩個主要版本」規則；本課建議至少 macOS 14，Apple Silicon／Intel 必須下載對應安裝包。
- **Windows**：64-bit Windows 10 22H2 build 19045 或 Windows 11 23H2 build 22631 以上；WSL 2.1.5 以上；CPU 支援 SLAT；BIOS/UEFI 硬體虛擬化已啟用。
- **資源**：總 RAM 至少 8GB、核心流程至少 20GB 可用磁碟；16GB RAM／30GB 可用空間較適合課堂批次檔案。
- **權限**：可安裝或由 IT 預先安裝 Docker Desktop，可重開機，可接受防火牆／安全性提示；公司管理設備需先取得 IT 同意。
- **網路**：課前可連 HTTPS 443 下載 Docker image、試跑包與教材；主機 `5678` 埠未被占用。

## 3. 回傳證據

### 所有學員

- OS 版本與 CPU 架構截圖。
- 總 RAM 與可用磁碟截圖。
- Docker Desktop 啟動畫面，或 IT 已安裝的確認訊息。

### Windows 額外提供

在 PowerShell 執行並貼上結果：

```powershell
wsl --version
wsl --status
wsl -l -v
docker version
docker compose version
```

工作管理員 → 效能 → CPU 另截圖確認「虛擬化：已啟用」。若顯示停用，請依課程頁進 UEFI，尋找 `Intel Virtualization Technology / VT-x` 或 `AMD SVM Mode`；選項被鎖或無法重開機時直接標 BLOCK。

### macOS 額外提供

在終端機執行：

```bash
sw_vers -productVersion
docker version
docker compose version
docker run --rm hello-world
```

另確認「關於這台 Mac」的晶片欄位，以及第一次啟動 Docker 是否能輸入 Mac 密碼／通過 Gatekeeper。

## 4. T-1 天最後確認

- Docker Desktop 顯示 running。
- `docker version` 有 Client 與 Server 兩段版本資訊。
- `docker compose version` 有版本號。
- `docker run --rm hello-world` 顯示成功訊息。
- 下載並解壓 `n8n-starter-kit`，不必等到課堂才下載。

若任一項失敗，回報「作業系統、錯誤畫面、上面哪一個指令失敗」三項資訊；不要只寫「Docker 不能用」。

## 5. 延伸能力（不阻擋核心課）

- Gemma 4 + Ollama：另預留至少 10GB 模型空間；模型大小與速度依 RAM／CPU／GPU 而異。
- Cloudflare Tunnel：需額外確認公開入口與安全設定；核心 localhost 流程先通過再做。
- Gemini API／Telegram：需個別 credential 與資料政策確認，不影響 Docker/n8n 入場判定。

## 6. 官方文件

- [Docker Desktop for Mac 安裝與需求](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Docker Desktop for Windows 安裝與需求](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Desktop Windows 權限需求](https://docs.docker.com/desktop/setup/install/windows-permission-requirements/)
- [Docker Desktop WSL2 backend](https://docs.docker.com/desktop/features/wsl/)

> 官方支援條件會隨 Docker Desktop 與作業系統版本變動；開課前由講師再核對官方頁面一次。
