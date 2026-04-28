# Workflows · n8n 預製演練 workflow JSON

《AI 資料工廠》課程各 Module 的可匯入 workflow JSON。學員卡關時可拿這裡的標準範本對照、或直接匯入跑一遍當作 baseline。

## 命名規則

```
m{module}-{topic}-{purpose}.json
```

範例：
- `m1-webhook-hello-world.json`
- `m2-reference-practice.json`
- `m3-folder-watch-demo.json`
- `m3-ai-rename-demo.json`
- `m4-google-form-to-n8n-demo.json`

## 對應課程單元

| Workflow JSON | 對應單元 | 用途 |
|---------------|---------|------|
| `m1-webhook-hello-world.json`（待補） | `m1-1-launch.html` | 第一個能跑通的 webhook |
| `m2-reference-practice.json`（待補） | `m2-1-reference.html` | 節點間欄位引用練習 |
| `m3-folder-watch-demo.json`（待補） | `m3-1-watch.html` | Watch Folder 觸發 |
| `m3-ai-rename-demo.json`（待補） | `m3-2-rename.html` | Gemini PDF 改名 |
| `m4-google-form-to-n8n-demo.json`（待補） | `m4-1-remote.html` | Form → Webhook → n8n |

> 目前先建立資料夾與命名規則入口；workflow JSON 將分批補齊，每補一支就更新此表並在對應單元頁加「下載練習 workflow」連結。

---

## ⚠️ 匯出 / 分享前必做

公開分享 workflow JSON 前，請先確認兩件事：

1. **不匯出 credentials**：n8n 的 workflow export 預設**不會帶出 credential 內容**（只保留 credential 的 ID/name reference），這部分 n8n 已幫你擋了一層。credentials 需由學員匯入後自行建立並重新指定。詳見官方 [Export and import workflows](https://docs.n8n.io/workflows/export-import/)。
2. **檢查節點參數有沒有寫死敏感字串**：真正風險是 HTTP Request 節點的 URL / Body / Header 裡硬寫死 API key、token、Webhook URL query string，或 Set / Code 節點裡留下的 password / secret。這些不在 credential 系統內，所以會跟著 workflow JSON 匯出。

### 檢查指令

```bash
grep -Ei '"apiKey"|"token"|"password"|"secret"|Authorization|Bearer|x-api-key|credential' your-workflow.json
```

若有命中，請逐筆確認是「範例值 / 占位符（如 `YOUR_API_KEY`）」還是「真實密鑰」。真實密鑰要：
- 移到 n8n **Credentials** 頁集中管理
- 把節點參數改為從 credential 讀取
- 重新匯出並再跑一次 grep

### 流程

1. 在 n8n UI 開啟 workflow → 右上角選單 `⋯` → **Download**
2. 跑上面 grep 檢查
3. 改檔名為 `m{module}-{topic}-{purpose}.json` 後放入本資料夾
4. 在本 README 表格補一行對應說明

### 學員端匯入後必做

匯入本資料夾的 workflow JSON 後，**credential reference 會是空的**，學員需要：

1. 自行在 **Credentials** 頁建立對應的 credential（Gemini API key、Google OAuth、LINE Channel token 等）
2. 開啟 workflow，把每個需要 credential 的節點重新指定到剛建立的 credential
3. 再執行測試

這樣的設計是為了「強迫學員理解 credential 機制 + 保護分享方的真實密鑰」。

---

## 不要放在這裡的東西

- 任何含有 API key / token / password 的 workflow JSON
- 含真實客戶資料的 workflow（範例資料用 `sample-data/` 內的虛構資料）
- 未經當事人同意的對話、信件
- 把 SaaS 商品包裝對外販售的 white-label workflow（違反 n8n SUL）
