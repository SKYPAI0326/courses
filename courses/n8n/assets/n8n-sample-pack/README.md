# n8n Lite Pack 演練素材包 v1.5

> **v1.5 改動**（2026-05-08）：`batch-inbox/` 加 4 個有效繁中商業 PDF（採購訂單 / 結案報告 / 員工手冊 / 產品規格書），讓 #03 batch-error-recovery 的 success 路徑能跑通。先前只有 `not-a-pdf.pdf` 被讀取（其他 .txt / .bin 副檔名被 fileSelector `*.pdf` 過濾掉），processed/ 永遠為空、學員體感像 workflow 壞了。同時移除誤導的 `good-01~04.txt`（副檔名連 read 都不會 read）+ `corrupted.bin` + `empty.txt`。
>
> **v1.4 改動**（2026-05-08）：`batch-inbox/` 預先建好 `processed/` 與 `failed/` 空子資料夾，避免 cp -R 蓋掉 setup-wizard 建的子結構造成 #03 ENOENT。
>
> **v1.3 改動**（2026-05-07）：替換 `pdf-inbox/` 內 doc-001/002/003.pdf 為 TTF 字型 embedded 的繁中商業 PDF（合約 / 業務月報 / 出貨清單）。先前 image-only PDF 導致 n8n Read PDF / pdf-parse 抽不到文字。
>
> **設計原則提醒**：#03 workflow 設計上**只處理 PDF**（fileSelector `*.pdf` + Extract PDF Text node）。其他格式（Word / Excel / 圖片 / 純文字）走 #10 folder-organize（混合格式分類）或自行改 fileSelector + 換 Extract 策略。

對應 14 個 workflow 的測試素材。把對應子資料夾的內容**複製**到你的 starter-kit 內（**不要動原本的 shared 資料夾結構**）：

## 使用方法

1. 解壓本 zip 到任意地方
2. 把各子資料夾內的檔**複製**到 `n8n-starter-kit/shared/<對應資料夾>/`
3. 開 n8n UI → 對應 workflow → Execute

## ⚠ Windows 學員注意（解壓動線）

**請用 Win 內建「解壓縮全部」或 7-Zip 解到「短英文路徑」**，例如：
- ✅ `C:\Users\<你>\Downloads\n8n-sample-pack\`
- ❌ 不要解到 OneDrive / iCloud / 桌面同步路徑（中文路徑也避開）
- ❌ 不要解到 `C:\Users\<你>\OneDrive\桌面\客戶檔\...`

OneDrive / iCloud 同步資料夾跟 Docker bind mount 衝突，會導致 n8n 看不到檔或讀到舊版。

## n8n Docker 路徑前置檢查

複製檔案進 starter-kit 後，先用 n8n UI 確認容器內看得到：
1. 開任一 Read File 節點
2. 路徑填 `/files/n8n-sample-pack/pdf-inbox/doc-001.pdf`（**不是** Mac/Win 本機路徑）
3. Execute Node → 看到綠燈 + binary preview = 容器掛載 OK

如果紅燈說「ENOENT」：你的檔案不在 Docker 看得到的 volume 裡，回去檢查 starter-kit 的 `shared/` 路徑。

## 對照表

| 子資料夾 | 對應 workflow | 用途 |
|---|---|---|
| `pdf-inbox/` | #02 PDF AI 改名 | 3 個檔名無意義 PDF（合約 / 報價單 / 教材內容）測試 AI 改名 |
| `batch-inbox/` | #03 批次錯誤恢復 | 4 正常 + 1 損壞檔 + **2 邊界 case** (`empty.txt` / `not-a-pdf.pdf`) |
| `daily-input/` | #04 定時 AI 日報 | .md + .txt 混合 + **`客戶反饋_Big5.txt`**（測 encoding fallback）|
| `client-inbox/` | #10 客戶資料夾整理 | PDF/PPTX/DOCX/XLSX/PNG/MD mixed + **`未命名文件.docx`**（測 classify by content） |
| `leads-inbox/` | #11 CSV 線索清洗 | 30 筆雜亂 + **`leads-raw-messy.csv`**（測 BOM/全形/CRLF normalize） |
| `knowledge-docs/` | #12 本地知識庫 RAG | 4 份知識文件 |
| `ops-input/` | #13 ops snapshot | 標準 metrics + **`metrics-2026-05-07-spike.csv`**（測異常+缺值容錯） |

**不需要素材的 workflow**（webhook trigger / OAuth credential / 設定驅動）：
- #01 webhook hello world
- #05 Telegram 通知測試
- #06 Webhook → Gemini → 本機檔（POST 觸發）
- #07 Quick Tunnel receiver
- #08 Expression 練習
- #09 Gmail 分類（需 OAuth）
- #14 API monitor（在 workflow 內設定 API list）

完整 workflow ↔ files 對照見 `manifest.json`。

## 🚀 想看到「批次自動化省時感」？

預設小量教學版（不爆 RPM）約 5-15 秒跑完，**體感不明顯**。想看真正的省時效益：

```bash
# Mac 範例：把 12 個 PDF 搬到 #02 inbox 跑
cp scale-up/pdf-inbox-12/* ~/Downloads/n8n-starter-kit/shared/pdf-inbox/
# 跑 #02 約 80 秒（含 throttle，避免撞 Free tier RPM）
# 比手動改 12 個檔的 5-8 分鐘省一個量級
```

`scale-up/` 含 5 個放大版資料夾，詳見 `scale-up/README.md`。

## 失敗時看哪裡（troubleshoot 三步）

跑 workflow 出錯先按這 3 步排查：

1. **AI 改名失敗（#02 / #03 / #10）** — 看新檔名是否含 `/ : ? *` 等 Win 禁字。Code node 已有 `replace([\\/:*?"<>|]/g, '_')`，但邊界 case（trailing space / Windows 保留名 CON/PRN/NUL）不在覆蓋範圍。
2. **讀檔失敗（任何 workflow）** — 先測 `pdf-inbox/doc-001.pdf` 能不能 Execute Read PDF 看到 binary preview。能 → 你的後段有問題；不能 → Docker 掛載 / 路徑 / 權限 問題。
3. **CSV / TXT garbled（#04 / #11）** — 檔案是否仍 UTF-8？打開 `leads-raw.csv` 用 VS Code/TextEdit 看，狀態列應顯示 UTF-8。`客戶反饋_Big5.txt` 是故意 Big5 — 那個是測 encoding fallback。

## 重新產生

如果想客製或補檔，跑這個腳本：

```bash
pip install reportlab python-docx python-pptx openpyxl pillow
python3 build_sample_pack.py
```

build script v1.1 會跑 `validate_pack()` 自動檢查每個檔案的可讀性 + 副檔名 magic number 對齊。
