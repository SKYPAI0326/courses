# n8n Starter Kit · 弄一下工作室

《AI 資料工廠》課程的 n8n 本機環境試跑包。在自己電腦跑一個免費、無執行次數限制的 n8n，並能直接讀寫本機資料夾。

## 最小執行流程

### 第一次啟動

1. 先安裝 **Docker Desktop** 並確認已啟動（左上角應看到鯨魚圖示）
   - Mac：<https://www.docker.com/products/docker-desktop/>（依 Intel / Apple Silicon 下載對應版本）
   - Win：同網址；安裝完需啟用 WSL2（Docker Desktop 安裝精靈會引導）
2. 雙擊 `start.command`（Mac）或 `start.bat`（Windows）
3. 第一次會自動把 `.env.example` 複製為 `.env` 並打開讓你編輯，**請改 `POSTGRES_PASSWORD`** 為強密碼後存檔
4. 再次雙擊 `start.command` / `start.bat`，等約 30 秒（首次需下載 image，可能花 1-5 分鐘）
5. 瀏覽器自動打開 <http://localhost:5678>，建立你的 Owner Account（信箱 + 密碼，n8n 內建）

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
| `start.command` / `start.bat` | 一鍵啟動 |
| `stop.command` / `stop.bat` | 停止服務（資料保留） |
| `update.command` / `update.bat` | 升級 n8n image |
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
docker compose logs n8n --tail 50
docker compose config
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

- **改埠號**（5678 被佔用時）：編輯 `n8n-compose.yml` 的 `ports: - '5678:5678'`，把第一個 5678 改成其他（如 `'5680:5678'`），重啟後改用 <http://localhost:5680>
- **改本機掛載資料夾**：編輯 `n8n-compose.yml` 的 `- ./shared:/files/shared`，把 `./shared` 改成你要掛的路徑
- **改時區 / 密碼 / Webhook URL**：編輯 `.env`，重啟容器（雙擊 stop 再 start）

## Sustainable Use License 提醒

n8n Community Edition 採 [Sustainable Use License (SUL)](https://docs.n8n.io/sustainable-use-license/)：
- ✅ 允許你內部商業使用、用 n8n 接顧問案
- ❌ 禁止把 n8n 包成 SaaS 對外販售、white-label 給客戶

工作坊範圍內的使用都在允許範圍內，安心用。
