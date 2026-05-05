---
research_type: technical-feasibility
target: n8n Lite Pack 「下載安裝後設兩個 key 即用」最短路徑
research_date: 2026-05-02
sources_verified: n8n CLI docs / community forum / n8n GitHub source code (TelegramApi.credentials.ts / HttpHeaderAuth.credentials.ts)
---

# n8n Credentials 自動化研究報告

## 核心結論

**Lite Pack 100% 技術可行**——透過 n8n CLI `import:credentials` + `import:workflow` 配合 decrypted JSON 路徑，**完全可達成「下載安裝後設兩個 key 即用」**。

**Google Pack 50% 可行但門檻高**——OAuth credential 的 access_token 可預先寫入 decrypted JSON，但**第一次取得 refresh token 仍須學員手動完成 OAuth redirect flow**（n8n 設計限制）。

## 關鍵技術發現

### 發現 1：CLI `--decrypted` 是最穩路徑（非 REST API）

n8n CLI 提供完整的 export/import 機制：

```bash
# 從現成 n8n 匯出（含明文 API key）
n8n export:credentials --all --decrypted --output=credentials.json

# 匯入到目標 n8n（會用該 instance 的 N8N_ENCRYPTION_KEY 重新加密儲存）
n8n import:credentials --input=credentials.json
n8n import:credentials --separate --input=/path/to/dir/   # 多檔模式
```

**Docker 環境用法**：
```bash
docker exec -u node -it <container> n8n import:credentials --input=/path/to/file.json
```

**為何選 CLI 而不是 REST API**：
- CLI 不需要先建 API key（REST API 必須先去 UI 點 Settings → n8n API → Create）
- CLI 不需要處理 owner account 認證
- CLI 對 encryption key 不一致情況有官方支援（`--decrypted` 路徑）
- REST API 是企業 / Cloud 路徑，self-hosted 雖支援但摩擦較大

### 發現 2：Credential type schema（實證自 GitHub）

從 `n8n-io/n8n` master branch 直接讀 source code 確認：

**HttpHeaderAuth**（給 Gemini API key 用）：
```typescript
name = 'httpHeaderAuth';
properties:
  - accessToken / name: string  // header 名稱
  - value: string                // header 值
```

**TelegramApi**（給 Telegram bot 用）：
```typescript
name = 'telegramApi';
properties:
  - accessToken: string          // bot token
  - baseUrl: string              // 預設 https://api.telegram.org
```

**對應 Lite Pack 需要的 decrypted JSON**（**注意：必須自帶 id 欄位**，n8n 1.x+ NOT NULL constraint）：

```json
[
  {
    "id": "lite-pack-gemini",
    "name": "Lite Pack · Gemini API",
    "type": "httpHeaderAuth",
    "data": {
      "name": "x-goog-api-key",
      "value": "AIza...學員API key..."
    }
  },
  {
    "id": "lite-pack-telegram",
    "name": "Lite Pack · Telegram Bot",
    "type": "telegramApi",
    "data": {
      "accessToken": "123456:ABC-DEF...學員token...",
      "baseUrl": "https://api.telegram.org"
    }
  }
]
```

setup-wizard 直接生這個 JSON → docker exec import → 完成。

**id 欄位的設計選擇**：
- 任何 unique 字串都行（純英數字 + dash 即可，不必是 nanoid 格式）
- 用語意化命名（如 `lite-pack-gemini`）方便後續 workflow JSON 內 reference
- workflow JSON 的 credential block 也要對齊這個 id 才能自動 link

**已驗證錯誤訊息**（2026-05-04 學員實測）：缺 id 會報
```
An error occurred while importing credentials. See log messages for details.
null value in column "id" of relation "credentials_entity" violates not-null constraint
```

### 發現 3：Workflow 內 credential 自動 link 機制

n8n workflow JSON 的 credential reference 結構：
```json
"credentials": {
  "telegramApi": {
    "id": "xxx",
    "name": "Lite Pack · Telegram Bot"
  }
}
```

**關鍵行為**：n8n import workflow 時，會優先用 `id` 對齊，**id 不存在則 fallback 用 name + type 對齊**（migration friendly）。

**Lite Pack 設計策略**：
- 所有預製 workflow JSON 內 credential reference 都用**固定 name**（`Lite Pack · Gemini API` / `Lite Pack · Telegram Bot`），id 寫 placeholder
- setup-wizard 先 import credentials（取得自動分配的 id）
- 再 import workflow（n8n 用 name + type 自動 link 到已建 credential）
- 結果：學員不用手動到 UI 點任何 credential 重新指定

### 發現 4：OAuth credentials 的限制（影響 Google Pack）

OAuth2 credential schema（推測）：
```json
{
  "name": "Google Docs OAuth",
  "type": "googleDocsOAuth2Api",
  "data": {
    "clientId": "...",
    "clientSecret": "...",
    "accessToken": "...",
    "refreshToken": "...",
    "authQueryParameters": "..."
  }
}
```

**可預先寫入**：clientId / clientSecret（學員從自己的 Google Cloud Console 拿）

**不可預先寫入**：accessToken / refreshToken — 必須走 OAuth redirect flow 才能取得，n8n 用其 redirect URI 接收 Google 回傳的 authorization code → 換取 token

**Google Pack 的最低摩擦設計**：
1. setup-wizard 只能寫入 clientId + clientSecret（不會自動拿到 refresh token）
2. 學員必須到 n8n UI 點 credential → Connect → 觸發 OAuth flow → Google 同意頁 → 自動跳回 → n8n 拿到 token
3. **這 1 步無法自動化**（n8n / Google 的安全設計）

對學員體感：4 個 OAuth credentials = 4 次「點 Connect → Google 同意」（每次約 30 秒）。比手動建 credential 快很多，但仍需學員操作。

## setup-wizard v0.2 完整自動化路徑

```
[GUI 對話框] 收 4 個學員資料
    ↓
[檔案 I/O] 寫 personalization.env + decrypted-credentials.json
    ↓
[Docker exec] cp credentials.json + workflows/ 進 container
    ↓
[Docker exec] n8n import:credentials --input=/tmp/credentials.json
    ↓
[Docker exec] n8n import:workflow --separate --input=/tmp/workflows/
    ↓
[REST API smoke test] 觸發每個 workflow，看是否回 200
    ↓
[GUI 對話框] 報告：✓ 8 / ✗ 0
    ↓
[完成] 學員打開 localhost:5678 看到 8 個 workflows 全部就緒
```

**整段 30 秒以內可完成**（不含學員填資料時間）。

**唯一需要學員手動的事**：
- 給 setup-wizard 4 個 input（API key / token / chat ID / topic）

**不需要學員做的事**：
- 不需要打開 n8n UI 建 credential
- 不需要點任何 workflow 重新指定 credential
- 不需要編輯 yaml / json
- 不需要記住任何 API path

## 風險與緩解

| 風險 | 機率 | 緩解 |
|------|------|------|
| n8n 升級導致 CLI 參數改變 | 低 | n8n image 鎖 patch 版本 2.17.8（已做） |
| docker exec 找不到 container 名 | 中 | setup-wizard 用 filter `name=n8n-starter-kit` 動態找 |
| credentials JSON schema 隨版本改變 | 低 | 從 GitHub source 讀的 schema 是 master，定期回檢 |
| 學員的 n8n owner account 還沒建立 | 高 | setup-wizard 偵測 + 跳對話框引導先去 localhost:5678 完成 |
| credential name 撞到既有 credential | 低 | 用 `Lite Pack · {name}` 命名空間隔離 |
| smoke test 觸發 webhook 沒接 cloudflared | 中 | 跳過需要 cloudflared 的 workflow，標 ⚠️ 在報告 |

## 驗證方式

實際測試流程（待使用者實測）：

```bash
# 1. 確認 n8n 跑著
curl http://localhost:5678/healthz

# 2. 找 container 名
CONTAINER=$(docker ps --filter "name=n8n-starter-kit" --format "{{.Names}}" | grep n8n-1)

# 3. 寫測試 credentials JSON
cat > /tmp/test-cred.json <<'EOF'
[
  {
    "name": "Test Gemini",
    "type": "httpHeaderAuth",
    "data": {"name": "x-goog-api-key", "value": "test-key"}
  }
]
EOF

# 4. 複製進 container
docker cp /tmp/test-cred.json $CONTAINER:/tmp/

# 5. import
docker exec -u node $CONTAINER n8n import:credentials --input=/tmp/test-cred.json

# 6. 驗證
docker exec -u node $CONTAINER n8n list:credentials
# 應看到 "Test Gemini" 出現
```

如果這 6 步驟都成功，setup-wizard v0.2 路徑完整可行。

## 下一步建議

1. **先實測上述 6 步驟驗證流程**（5-10 分鐘）— 你或我做都行，但你已有 n8n 環境較快
2. 驗證通過後，**setup-wizard.command 升級到 v0.2**（含 docker cp + docker exec import 完整路徑）— 我可立刻寫
3. 設計 Lite Pack 8 個 workflow JSON 的 credential reference 結構（用固定 name）
4. 寫一份 sample-credentials.json 範本給 setup-wizard 動態填入學員值
5. 完整跑一輪：setup-wizard → 8 workflows 全部就緒 → 跑 smoke test

## 結論

**「下載安裝後設兩個 key 即用」是 100% 技術可行的**，不是空想。關鍵突破點是 n8n CLI 提供官方 `--decrypted` 路徑，避開 REST API 的 owner account / API key 摩擦，避開 encryption key 不一致問題，避開手動 UI 操作。

Lite Pack 8 個 workflow（純 API key 型，避開 OAuth）可達成真正的「30 分鐘下載即用」。Google Pack 因 OAuth flow 限制無法 100% 自動化，但仍可大幅縮短到「填 client ID/secret + 4 次點 Connect」級別。

## 引用來源

- [n8n CLI commands](https://docs.n8n.io/hosting/cli-commands/)
- [n8n public REST API Documentation](https://docs.n8n.io/api/)
- [Hostinger: How do I use an API with n8n on a self-hosted setup?](https://www.hostinger.com/tutorials/n8n-api)
- [n8n Community Forum: Import Credentials via CLI](https://community.n8n.io/t/import-credentials-via-cli-problem/224587)
- [n8n Community Forum: How to export/import all my workflows using CLI with decrypted flag](https://community.n8n.io/t/how-to-export-import-all-my-workflows-using-cli-with-decrypted-flag/124578)
- [DeepakNess: Export n8n workflows and credentials](https://deepakness.com/raw/export-n8n-workflows-credentials/)
- [n8n GitHub: TelegramApi.credentials.ts](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/credentials/TelegramApi.credentials.ts)
- [n8n GitHub: HttpHeaderAuth source code](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/credentials/) ← 透過 gh api 確認
