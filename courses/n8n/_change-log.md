# n8n 課程變更日誌

記錄每次依 `CLAUDE_CODE_FIX_BRIEF.md` 或其他外部刺激所做的內容修正，方便日後若工具政策再變時對照查找。

## 2026-04-28 — 依 CLAUDE_CODE_FIX_BRIEF.md 全面修正

**驅動文件**：`CLAUDE_CODE_FIX_BRIEF.md`（同目錄）
**驗證**：lint-page.py 0 BLOCKER 0 ERROR；search-index 469 筆；sitemap 469 URL
**核對來源**：依 brief「已核對來源」段所列官方頁面

### Phase A · P0 文字修正

| Brief # | 修改主題 | 影響檔案 | 改動方向 |
|---------|---------|---------|---------|
| #1 | Make operations → credits | `index.html`、`module1.html`、`m1-1-glossary.html`、`module4.html` | Make 改用 credits 描述計費單位（1,000 credits/月，AI 模組另計），不再寫死 1,000 ops |
| #2 | Gemini 額度依模型查表 | `m1-3-prompt.html`、`m3-2-batch.html`、`m3-2-rename.html`、`m3-3-generate.html`、`m4-3-ai.html`、`module3.html` | 不再寫死 1,500 次/15 RPM；改為「依官方 Rate limits 頁面為準」+ Flash-Lite 例值 + 控速建議 |
| #3 | Google Maps $200 → SKU quota | `m4-2-api.html` | 點出 2025-03 改制；建議 budget alert + 旅遊範例改 CWA + OpenStreetMap |
| #4 | Docker image 鎖版本 | `n8n-compose.yml`、`n8n-starter-kit/README.md`、`m1-1-launch.html`、`m1-1-overview.html`、`m1-1-setup.html`、`m1-1-troubleshoot.html` | 從 `n8nio/n8n:latest` 鎖到 `n8nio/n8n:2.17.8`（2026-04-27 stable，依 Docker Hub 驗證）。Docker Hub 沒提供 minor-only tag，鎖 patch；要升級時手動更新。footer-meta 也同步更新 |
| #5 | 「完全免費」加授權條件 | `index.html`、`module1.html`、`m1-1-overview.html`、`m1-2-tunnel.html`、`module4.html`、`m4-1-remote.html`、`n8n-starter-kit/README.md` | 首頁/招生敘事一行帶過 SUL + Docker Desktop 商用條款；README 寫詳細版；分服務分別定義（n8n / Make / Gemini / Cloudflare / Docker） |

### Phase B · 演練支援與安全

| Brief # | 主題 | 影響檔案 |
|---------|------|---------|
| #6 | sample-data / workflows 入口 | 新增 `assets/sample-data/README.md` + invoice / daily-report / forms 三類示範素材；新增 `assets/workflows/README.md`（含 Reset Credentials SOP） |
| #7 | 預期輸出區塊 | 首批 3 頁試做：`m1-1-launch.html`、`m2-1-reference.html`、`m4-3-ai.html`；沿用既有 expect-box / verify-box 樣式，不新增 CSS |
| #8 | Webhook / Tunnel 安全提醒 | `m1-2-tunnel.html`、`m4-1-remote.html`、`m4-2-api.html` 各加一個紅色 context-box 列四項：隨機 path / Header Auth / Credentials / 不公開含 cred 的 JSON |
| #10 | ngrok 改短期測試替代 | `m1-2-tunnel.html` 移除「完全免費」字樣，改「ngrok free plan 短期測試替代」 |

### Brief 沒寫但補強的項目

1. **Workflow JSON 匯出檢查 SOP**：`assets/workflows/README.md` 寫了 export 前 grep 檢查節點參數的硬寫密鑰（n8n workflow export 預設不含 credential 本體，但節點參數欄位裡寫死的 token 會被帶出）
2. **lint + index + sitemap 同步**：本檔末尾紀錄一次完整驗收
3. **Docker 版本誤判修正**：原 plan 寫 n8n 主線是 1.x、2.0 未 GA；實查 Docker Hub 後確認 2.17.8 為 2026-04-27 stable，已照實鎖 patch
4. **變更紀錄**：建立此 `_change-log.md`，後續工具政策再變時補新 entry

### 已知殘留（屬刻意保留，非問題）

- `m4-2-api.html:238` 仍出現「\$200」字樣，但屬於「不再是固定 $200/月 credit」的解釋文字，是 brief 允許保留的「說明舊說法已改」備註

### 待辦（後續延伸）

- B2 預期輸出剩餘 5 頁：`m1-2-tunnel`、`m3-2-rename`、`m3-3-generate`、`m4-1-remote`、`m4-3-docs`（首批驗收 OK 後再批次推）
- 補齊 `assets/workflows/` 內的實際 JSON（首次預定 m1-webhook-hello-world.json）
- 工具政策每季回頭檢查（Make credits、Gemini quota、Maps SKU、n8n 版本）
- **設計系統小修**：B3 紅色安全提醒框目前用 inline `border-left:4px solid #b54a4a`，建議抽成 `.security-box` class 並寫進 `_規範/design-tokens.md`，與既有黃系 `.step-tip.warning` 區分（Codex review #7，本次先不動樣式系統）

---

## 2026-04-28 — Codex L3 review 跟進（同日）

**驅動**：CALL_ID `a82908d7`，consult mode 248s。Codex 找到 3 個必修 + 4 個建議修，採納 #1–#6（樣式抽 class #7 留 backlog）。

| Codex 條目 | 修正範圍 |
|-----------|---------|
| P0 #1 — `assets/workflows/README.md` 對 n8n export 行為描述錯誤 | 完全重寫安全段。改寫實情：n8n workflow export 預設不帶 credential 本體（官方文件），真風險是節點參數欄位硬寫死的 token；改用 grep 命令檢查節點 JSON |
| P1 #2 — `m4-2-flow.html` 漏網（line 165 / 176 / 232 / 233） | 「無限次數」→「不按 SaaS credits 限制」；「Make 有次數限制／n8n 無限次數」→「Make 受 credits 限制／n8n 自架不按次計費」；「1,000 ops」→「1,000 credits」；「每則 LINE 只耗 1 op」→「一般模組動作大致 1 credit/次（依 Make 當前計費）」 |
| P1 #3 — `index.html:159` stat | 「不計／執行次數」→「自架／不按次計費」 |
| P1 #4 — `assets/n8n-starter-kit/README.md` 開頭版本說法 | 「2.17.8（2026-04 stable）」→「2.17.8（2026-04-27 依 Docker Hub tags 驗證可用）」，避開 n8n stable 是 moving tag 的風險 |
| P1 #5 — `m1-3-prompt.html` 「每日數千 RPD」 | 拿掉，只留「Flash-Lite 曾列每分鐘約 15 RPM 為控速參考」+「實際 RPM/TPM/RPD 以官方為準」 |
| P2 #6 — starter-kit README SUL 段 | 把 n8n SUL（用途限制）與 Docker Desktop（組織規模/條款）拆成兩條獨立判斷，不再綁在「個人/教學/小型團隊」一句話 |
| Codex 自己漏抓我順手補的 | `module4.html:204` 「無限次跑大量迴圈」→「自架不按次計費跑大量迴圈」；`module4.html:339` Q3「Make 免費版單次執行 5 分鐘上限」→「依 Make 當前條款；自架由你的機器資源決定」 |

**Verdict**：actionable（Codex 指出真實事實錯誤與漏網，可執行）

```
python3 codex_bridge.py --mark-verdict a82908d7 --verdict actionable
```

### 驗收紀錄

```
$ python3 docs/lint-page.py courses/n8n/ --summary
═══ 摘要 ═══
掃描：46 頁
BLOCKER：0 條（0 檔）
ERROR：  0 條
WARN：   116 條
✅ 無 BLOCKER。

$ python3 docs/build-search-index.py
✓ 已寫入 search-index.json（469 筆）

$ python3 docs/build-sitemap.py
✓ 已寫入 sitemap.xml（469 筆 URL）

$ rg -n "operations|1,500 次|15 requests|\$200|n8nio/n8n:latest|n8n latest|完全免費|無次數上限|ngrok.*完全免費" courses/n8n/ --type-add 'web:*.{html,md,yml,yaml}' --type web | grep -v CLAUDE_CODE_FIX_BRIEF
courses/n8n/lessons/m4-2-api.html:238  ← 已改寫後的解釋字樣，符合 brief 允許殘留條件
```
