---
session_type: standby
session_date: 2026-05-04
trigger: 使用者轉移到 Claude Desktop 繼續驗證工作（為方便截圖）
---

# n8n Classroom Pack · Session STANDBY 紀錄

## 當前進度

**目標**：驗證 n8n CLI `import:credentials` 路徑可行 → 證明 setup-wizard v0.2 整套自動化可實作 → 才能開始做 7 個剩餘 workflow + Lite Pack 完整收尾。

**已完成**：

| Phase | 狀態 | 證據 |
|-------|------|------|
| Phase A · n8n 環境 | ✅ 完成 | container `n8n-starter-kit-n8n-1` running、owner account 建好、localhost:5678 正常 |
| Phase B · Quick Tunnel | ✅ 完成 | tunnel-quick.command 跑出 trycloudflare URL、webhook 測試通連 |
| Phase C · CLI 驗證 | ✅ **實質通過** | 用極簡 JSON（Test1）跑 `Successfully imported 1 credential` — CLI 路徑 100% 可行 |

**當下卡關（Phase C step 5）**：

學員終端機把長 echo 指令斷成 2 行貼上，導致 JSON 字串內含實際換行字元（control character），n8n parser 拒絕。錯誤訊息：

```
An error occurred while importing credentials. See log messages for details.
Bad control character in string literal in JSON at position 196 (line 1 column 197)
```

對應檔案：`/tmp/test-cred.json`，cat 輸出顯示 `Lite Pack` 後面被斷行：
```
[{...,"name":"Lite Pack TEST · Gemini",...},{...,"name":"Lite Pack
  TEST · Telegram",...}]
```

## 立即解（已給使用者）

改用極簡 5 行（每行 ≤ 95 字元，避免終端機斷行）：

```bash
echo '[{"id":"t1","name":"Test1","type":"httpHeaderAuth","data":{"name":"x-api-key","value":"k1"}}]' > /tmp/c.json
cat /tmp/c.json
docker cp /tmp/c.json $CONTAINER:/tmp/c.json
docker exec -u node $CONTAINER n8n import:credentials --input=/tmp/c.json
docker exec -u node $CONTAINER n8n list:credentials | grep Test1
```

預期 `Successfully imported 1 credentials.` + `Test1` 出現在 list。

## 連發累計卡關清單（n8n 課程實測）

| # | 卡關 | 修法 |
|---|------|------|
| 1 | starter-kit zip 不存在 | 打包 zip |
| 2 | docker compose -f 沒帶 | 6 個 script 全補 |
| 3 | secure cookie 擋 | compose 預設 N8N_SECURE_COOKIE=false |
| 4 | postgres 密碼錯 | start.command 自動偵測 + 對話框 |
| 5 | port 5678 衝突 | start.command 啟動前 port 偵測 |
| 6 | Cloudflare 綁卡 | m1-2-tunnel 揭露框 |
| 7 | Cloudflare 要自有網域 | tunnel-quick.command 一鍵替代 |
| 8 | Cloudflared QUIC 被擋 | 預設 --protocol http2 |
| 9 | macOS Gatekeeper 擋 .command | 講義加強提醒 |
| 10 | tunnel-quick 偵測 URL pattern 太寬 | 改 grep 精確 regex |
| 11 | n8n credentials_entity 缺 id NOT NULL | JSON 加 id 欄位 |
| 12 | 終端機 paste 長 echo 斷行 | 改用極簡 ≤95 字元 echo |

## 已產出檔案清單

| 路徑 | 用途 |
|------|------|
| `_reviews/n8n-classroom-pack-design-2026-05-02.md` | 三層設計提案（Lite / Google / 原理文件） |
| `_reviews/n8n-credentials-api-research-2026-05-02.md` | CLI 自動化技術研究報告（含 GitHub schema 驗證） |
| `_reviews/lite-pack-cli-verify.html` | 全鏈路驗證頁（從零到 Phase C 完整動線） |
| `assets/n8n-lite-pack/README.md` | 學員視角使用說明 |
| `assets/n8n-lite-pack/setup-wizard.command` v0.2 | 自動化精靈雛型 |
| `assets/n8n-lite-pack/workflows/01-webhook-hello-world.json` | 第 1 個 workflow 範本（其他 7 個待做） |
| `_規範/飛輪規則.md` | 累計新增 4 條原則（商業培訓哲學 / 主流程低門檻 / 禁 patch 學員 / Cloudflared http2） |
| `~/.claude/projects/-Users-paichenwei/memory/feedback_business_training_vs_self_learning.md` | 商業培訓哲學 memory |

## 下一步（恢復後執行）

1. 確認 Phase C step 5 通過（用極簡 JSON 跑 import 看到 Successfully imported）
2. 通過後進「Phase D」：寫 7 個剩餘 workflow JSON
3. setup-wizard.command 補進 id 欄位的 schema fix（已修但要驗證）
4. 補 setup-wizard.bat（Windows 對應版本）
5. 寫 docs/ 內 8 份原理說明
6. 修飛輪規則加新條目「JSON 寫檔禁用 heredoc 與長 echo」
7. 讓使用者完整跑一輪 setup-wizard.command 真實安裝
8. 上線

## 恢復起手式

使用者下次回 Claude Code 說「繼續 n8n classroom pack」或「繼續 lite pack 驗證」即可。
參考檔案：本檔 + `_reviews/lite-pack-cli-verify.html`（全鏈路驗證頁）。
