# Gemma 4 + Ollama 單機執行安裝與使用手冊

> **適用平台**：macOS（Apple Silicon／Intel）與 Windows 10 22H2 以上
> **目標**：在自己的電腦上下載 Gemma 4，先完成一次本機對話與 API 驗證，再選擇性接到 Docker 內的 n8n。
> **更新基準**：2026-09-15。模型標籤、容量與安裝畫面會更新；遇到差異時，以文末官方連結為準。

## 0. 先看完成品

完成後，你會留下三個可觀察結果：

1. 終端機可以執行 `ollama run gemma4:e4b`，並得到 Gemma 4 的回答。
2. `http://127.0.0.1:11434/api/chat` 會回傳 JSON，內容位於 `message.content`。
3. 若你使用課程的 Docker n8n，HTTP Request 節點可以透過
   `http://host.docker.internal:11434/api/chat` 取得同一個本機模型的回答。

這份手冊先用公開問題「請用一句話介紹 n8n」驗證。驗證通過後，再換成自己的工作資料；不要一開始就拿客戶合約或個資測試。

## 1. 你現在要解決的情境

你需要摘要、分類或改寫一份不適合送到雲端 AI 的文件。Gemma 4 + Ollama 把模型與推論服務放在你的電腦上，適合先做離線草稿與內部資料處理；但「本機模型」不等於所有資料都自動安全，n8n 日誌、瀏覽器、外部節點與你主動使用的雲端服務仍要另外檢查。

本手冊的最小路徑是：

```text
下載 Ollama → 啟動服務 → 下載 Gemma 4 → CLI 對話
→ API 回應檢查 →（選配）Docker n8n 連線 → 留下驗證證據
```

## 2. 環境契約與準備

| 項目 | macOS | Windows |
|---|---|---|
| 作業系統基線 | macOS Sonoma 14 或更新；Apple Silicon 可使用 CPU／GPU，Intel 以 CPU 為主 | Windows 10 22H2 或更新，Home／Pro 皆可 |
| 帳號權限 | 一般使用者即可；第一次可能需要允許放入 Applications 或建立 CLI 連結 | 一般使用者即可，官方安裝程式預設不要求系統管理員 |
| 下載空間 | Ollama 本體之外，至少預留 10 GB 給 `gemma4:e4b`；模型與快取會再增加 | Ollama 本體至少約 4 GB，另預留 10 GB 以上給模型；大型模型會需要數十 GB |
| 網路 | 只在下載／更新 Ollama 與模型時需要；推論完成後可離線使用 | 同左 |
| 起始材料 | 一個可公開測試的短問題：`請用一句話介紹 n8n。` | 同左 |
| 完成物 | 一次 CLI 回答、一份 API JSON、（選配）n8n 綠色成功節點 | 同左 |

### 模型怎麼選

先用明確標籤，避免 `latest` 在未來換指向時造成課堂結果不同。

| Ollama 標籤 | 官方頁面顯示的模型檔約容量 | 建議用途 |
|---|---:|---|
| `gemma4:e2b` | 約 7.2 GB | 記憶體較緊、先求跑通；文字分類與短摘要 |
| `gemma4:e4b` | 約 9.6 GB | 本手冊的預設基線；一般筆電的文字與圖片理解 |
| `gemma4:12b` | 約 7.6 GB | 16 GB 統一記憶體／VRAM 的較高品質選擇；速度依硬體而異 |
| `gemma4:26b` | 約 19 GB | 較大記憶體或獨立 GPU；不列入初次安裝基線 |
| `gemma4:31b` | 約 20 GB | 工作站級硬體；不列入初次安裝基線 |

容量是下載檔大小，不是保證的最低 RAM。上下文長度、其他開啟的程式與 GPU／CPU 都會影響實際需求。第一次請用 `gemma4:e4b`；若記憶體不足，退回 `gemma4:e2b`。

## 3. 安裝 Ollama（Win／Mac 共用路線）

### 3.1 下載官方安裝包

請開啟官方下載頁：<https://ollama.com/download>

- **macOS**：下載 Ollama 的 macOS 安裝包，開啟 `.dmg`，將 **Ollama.app** 拖到 **Applications／應用程式**，再啟動一次。若跳出「是否建立 `ollama` 指令」或安全性確認，選擇允許。
- **Windows**：下載 `OllamaSetup.exe`，雙擊執行並完成安裝。安裝後 Ollama 會在背景執行，工作列通知區應看得到 Ollama 圖示。

安裝完成後，**關閉並重新開啟終端機**。這一步會讓新的 `ollama` 指令路徑生效。

### 3.2 確認服務已啟動

先確認版本。兩個平台都可以執行：

```text
ollama --version
```

接著確認本機 API：

**macOS Terminal：**

```bash
curl -sS http://127.0.0.1:11434/api/tags
```

**Windows PowerShell：**

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:11434/api/tags
```

看到 JSON（即使目前 `models` 是空陣列）就表示 Ollama 服務已經在 `11434` 連接埠等待請求。

> **沒有回應時**：先從 macOS 選單列或 Windows 工作列啟動 Ollama，等 5 秒後重試。只有在桌面程式沒有啟動時，才在終端機執行 `ollama serve`；不要同時啟動兩個服務。

## 4. 下載 Gemma 4 並完成第一次對話

### 4.1 下載模型

本手冊先下載 E4B 基線：

```text
ollama pull gemma4:e4b
```

下載期間不要關閉終端機或 Ollama。完成後確認模型已存在：

```text
ollama list
```

清單中應出現 `gemma4:e4b`。如果你的電腦記憶體不足，可改用：

```text
ollama pull gemma4:e2b
```

### 4.2 CLI 對話

執行：

```text
ollama run gemma4:e4b
```

看到互動提示後，貼上：

```text
請用一句話介紹 n8n，限 30 個中文字。
```

應該會得到一段回答。輸入 `/bye` 離開。

**Checkpoint A：** 你必須同時看得到 `gemma4:e4b` 已載入，以及一段模型回答；只看到下載完成、不代表推論成功。

若沒有成功，回到本節的 `ollama list`，確認標籤完全相同，再重新執行 `ollama run gemma4:e4b`。

## 5. API 驗證：留下可複製的 JSON 證據

CLI 能回答後，才進行 API 測試。API 測試證明其他程式（例如 n8n）可以呼叫同一個本機模型。

### 5.1 macOS Terminal

```bash
curl -sS http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma4:e4b","messages":[{"role":"user","content":"請用一句話介紹 n8n。"}],"stream":false}'
```

### 5.2 Windows PowerShell

```powershell
$body = @{
  model = 'gemma4:e4b'
  messages = @(
    @{ role = 'user'; content = '請用一句話介紹 n8n。' }
  )
  stream = $false
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Method Post `
  -Uri 'http://127.0.0.1:11434/api/chat' `
  -ContentType 'application/json' `
  -Body $body
```

### 5.3 判讀結果

成功回應的重點結構如下（其他欄位可能隨版本增加）：

```json
{
  "model": "gemma4:e4b",
  "message": {
    "role": "assistant",
    "content": "n8n 是用節點串接工作流程的自動化工具。"
  },
  "done": true
}
```

**Checkpoint B：** 必須找到 `message.content` 且 `done` 為 `true`。若只看到 HTTP 200、沒有 `message.content`，仍視為未完成，先不要接 n8n。

## 6. （選配）讓 Docker n8n 呼叫本機 Gemma 4

這一節只在你的 n8n 跑在 Docker Desktop 時使用。若你只需要單機聊天與 API，到第 7 節即可。

### 6.1 先理解位址差異

在 Docker 容器裡：

- `localhost:11434` 指向 **n8n 容器自己**，通常找不到主機上的 Ollama。
- `host.docker.internal:11434` 指向 **Mac／Windows 主機**，是 Docker Desktop 連回主機的固定名稱。

因此 n8n 要使用：

```text
http://host.docker.internal:11434/api/chat
```

### 6.2 用 n8n HTTP Request 節點測試

在 n8n 新增 **HTTP Request** 節點，設定：

| 欄位 | 值 |
|---|---|
| Method | `POST` |
| URL | `http://host.docker.internal:11434/api/chat` |
| Send Headers | 開啟 |
| Header | `Content-Type: application/json` |
| Send Body | 開啟，JSON |

先用固定測試內容，不要一開始就放工作資料：

```json
{
  "model": "gemma4:e4b",
  "messages": [
    {
      "role": "user",
      "content": "請用一句話介紹 n8n。"
    }
  ],
  "stream": false
}
```

執行節點後，Output 應出現 `message.content`。看到綠色成功狀態後，才把 `content` 改成上一個節點的欄位，例如：

```text
請將以下文字整理成三個重點：
{{$json.text}}
```

> **隱私檢查**：`$json.text` 可能會被記錄在 n8n execution data。若資料包含合約、個資或客戶機密，先確認你的 n8n execution data 保存設定與備份位置。

### 6.3 n8n 連不上時的回復路徑

1. 在主機終端機先重跑第 5 節 API；若主機 API 本身失敗，先修 Ollama。
2. 確認 URL 是 `host.docker.internal`，不是 `localhost`。
3. 確認 Docker Desktop 正在執行，並重試 HTTP Request 節點。
4. 若模型名稱錯誤，執行 `ollama list`，將節點的 `model` 改成清單中的完整標籤。
5. 執行一次後清除測試資料，再換回真實輸入；不要把錯誤回應直接寫入正式資料夾。

## 7. 單機使用的最小工作法

把模型當作「本機服務」使用時，每次任務都走這四步：

### A. 先定義輸出格式

例：

```text
請將下列會議筆記整理成：
1. 已決定事項（最多 3 點）
2. 待辦事項（事項／負責人／期限）
3. 尚未確認的內容
不要補寫原文沒有的資訊。
```

### B. 先用一小段去敏資料

把姓名、電話、公司統編與合約編號換成 `[客戶A]`、`[電話]`、`[合約編號]`，先確認 prompt 與輸出格式，再處理原始檔案。

### C. 檢查「有根據」而不是只看文句流暢

至少抽查三個輸出句子，逐句回到輸入資料確認。Gemma 4 能離線執行，不代表它不會推測或產生錯誤資訊。

### D. 留下版本與模型標籤

在輸出檔或工作紀錄寫下：

```text
執行日期：2026-09-15
Ollama：執行 ollama --version 的結果
模型：gemma4:e4b
輸出是否人工抽查：是／否
```

## 8. 常見問題與修復

| 現象 | 可能原因 | 修復位置 |
|---|---|---|
| `ollama: command not found` | 終端機仍是安裝前的 PATH；macOS 尚未允許建立 CLI 連結 | 重新啟動 Ollama，關閉重開終端機；macOS 重新啟動 App 並允許 CLI 連結 |
| `connection refused 127.0.0.1:11434` | Ollama 桌面程式未啟動 | 從選單列／工作列啟動 Ollama，等待 5 秒再跑 `/api/tags` |
| `model not found` | 標籤拼錯或尚未 pull | 跑 `ollama list`，複製完整標籤；必要時 `ollama pull gemma4:e4b` |
| 執行很慢或記憶體不足 | 模型太大、上下文太長、同時開太多程式 | 改用 `gemma4:e2b`；縮短 prompt；關閉不用的程式；不要同時載入多個大模型 |
| n8n 顯示連線失敗 | 容器內使用了 `localhost` | 將 URL 改為 `http://host.docker.internal:11434/api/chat` |
| n8n 執行逾時 | 首次載入模型需要時間或 prompt 過長 | 先在主機執行一次 `ollama run` 讓模型載入；使用短測試問題；確認 `stream:false` |
| 回應空白 | API 回傳格式與節點取值不一致 | Chat API 讀 `message.content`；Generate API 才讀 `response` |
| 想用 `gemma4:cloud` | 這是 Ollama 的雲端模型路徑，不是單機推論 | 改用 `gemma4:e4b`／`gemma4:e2b`；處理敏感資料時不要使用 `:cloud` |

### 安全停止與清理

- 離開 CLI 對話：輸入 `/bye`。
- 停止背景服務：優先從 Ollama 選單列／工作列退出；不要直接刪除模型資料夾。
- 移除模型（需要時）：

  ```text
  ollama rm gemma4:e4b
  ```

- 只有在確認不再需要模型時才移除；移除後，下一次使用必須重新下載。

## 9. 最終驗收清單

逐項打勾，並把終端機輸出或 n8n execution 畫面留給自己：

- [ ] `ollama --version` 有版本結果。
- [ ] `/api/tags` 能回 JSON。
- [ ] `ollama list` 有 `gemma4:e4b` 或你實際選用的標籤。
- [ ] `ollama run gemma4:e4b` 能回答「請用一句話介紹 n8n」。
- [ ] `/api/chat` 回應含 `message.content` 與 `done: true`。
- [ ] 若使用 Docker n8n，URL 使用 `host.docker.internal`，HTTP Request 節點顯示成功。
- [ ] 已確認輸入資料、n8n execution data、備份與外部節點的資料邊界。
- [ ] 輸出紀錄寫下日期、Ollama 版本與模型標籤。

**通過標準**：前五項全部完成；若要接 n8n，再加上第六、七項。任何一項失敗，都回到該項標示的修復位置，不以「模型有回文字」代替 API 或資料邊界驗證。

## 10. 官方查閱連結

- [Ollama 下載頁](https://ollama.com/download)
- [Ollama Quickstart](https://docs.ollama.com/quickstart)
- [Ollama Windows 文件](https://docs.ollama.com/windows)
- [Ollama macOS 文件](https://github.com/ollama/ollama/blob/main/docs/macos.mdx)
- [Ollama Gemma 4 模型頁](https://ollama.com/library/gemma4)
- [Google Gemma 4 官方介紹](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)

> **版本提醒**：若官方模型頁新增或改名標籤，先更新本手冊第 2、4、5、6、9 節的模型名稱，再發給學員。不要只改下載指令而留下舊的 API 或 n8n 節點範例。
