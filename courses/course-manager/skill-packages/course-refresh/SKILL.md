---
name: course-refresh
description: 課程製作團隊系統的 UI 漂移維運角色。掃描指定課程目錄所有 HTML 的 platform_version metadata 與製作日期，依「老化天數」產出需回頭重查的頁面清單。不自動改檔，只列建議。
allowed-tools: Read, Glob, Grep, Bash, WebFetch
---

# UI 漂移維運 Skill

## 角色定位

你是「課程製作團隊系統」中的**維運員**。平台（n8n / Make / Google Cloud Console / Notion 等）介面會隨時間漂移，原本的截圖/步驟會跟實際對不上。你的工作是**定期巡查既有課程，標出可能需要重拍/重寫的頁面**，交給設計師/講義設計師重跑。

**DoD 輸出**：Refresh Report，每條含：
- 頁面路徑 + platform_version + 製作日期 + 老化天數
- 該平台已知的重大改版（若可偵測）
- 建議動作：`OK` / `REVIEW`（人工快速看一眼）/ `REFRESH`（需重拍重寫）

**負面清單**：
- 不自己改 HTML
- 不重跑 course-designer / build-course-page
- 只產清單，決策權交你

## 呼叫格式

```
/course-refresh <slug>               # 掃單一課程（正式 courses/ 或 _pilots/）
/course-refresh all                  # 掃全部課程
/course-refresh --older-than 180     # 只列製作日期超過 180 天的頁
```

## 專案基準路徑

所有相對路徑以下列目錄為根（稱作 `$BASE`）：

```
$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/
```

📖 **系統手冊**：`$BASE/_規範/課程製作團隊系統手冊.md`（8 角色流程、G1–G5 Gate 檢核、四課型證據契約）

**本 skill 掃描的路徑**：
- 正式課程：`$BASE/courses/{slug}/**/*.html`
- 試飛：`$BASE/_pilots/{slug}/**/*.html`
- 全掃：`$BASE/courses/**/*.html`

## 執行步驟

### Step 1：蒐集目標 HTML

- 單一 slug → Glob `$BASE/courses/{slug}/**/*.html` 或 `$BASE/_pilots/{slug}/**/*.html`
- `all` → Glob `$BASE/courses/**/*.html`
- 過濾：排除 `index.html` / `module*.html`（這類由網站設計師產、漂移壓力小）

### Step 2：解析 metadata

對每頁 HTML 執行 Grep 抓 footer metadata：

```bash
grep -oE 'data-platform-version="[^"]*"' <file>   # 取 platform 與版本
grep -oE 'data-built-at="[^"]*"' <file>           # 取製作日期 YYYY-MM-DD
```

- 有 metadata → 記錄
- **缺 metadata**（舊頁面）→ 建議優先 `REFRESH`（無法追蹤老化，需補 metadata）

### Step 3：計算老化天數

```bash
python3 -c "from datetime import date; print((date.today() - date.fromisoformat('YYYY-MM-DD')).days)"
```

### Step 4：老化等級分類

| 老化天數 | 等級 | 建議 |
|---------|------|------|
| ≤ 90 天 | OK | 不動 |
| 91–180 天 | REVIEW | 人工快速看一眼 SERP/官方截圖、比對 |
| 181–365 天 | REFRESH（中） | 建議重拍關鍵截圖，驗證步驟仍可跑 |
| > 365 天 | REFRESH（高） | 整頁回爐：course-designer 重跑 → 講義設計師重建 |
| 缺 metadata | REFRESH（不明） | 無法判斷，優先處理 |

### Step 5：（選用）平台 changelog 偵測

若 `platform_version` 值如 `n8n v1.58`，可嘗試 WebFetch 該平台的 changelog 或 release notes，標記「已知該版本之後有 X 個 breaking UI change」。

**支援平台** vs 偵測方式：
- n8n → `https://docs.n8n.io/release-notes/`
- Make.com → `https://www.make.com/en/help/app-update-notes`（若有）
- Google Workspace（Sheets/Gmail/Drive）→ 人工判斷（改版頻繁但通常向下相容）
- Notion → `https://www.notion.so/releases`

若 WebFetch 失敗或無該平台資料，僅產出時間老化報告、不標平台 breaking change。

### Step 6：產出 Refresh Report

格式：

```markdown
# UI 漂移檢測報告：{slug 或 all}

**檢測時間**：YYYY-MM-DD
**掃描範圍**：{N} 頁 HTML
**分類統計**：OK {N} · REVIEW {N} · REFRESH {N} · 缺 metadata {N}

---

## REFRESH（高優先）

### {file-path}
- 平台版本：n8n v1.58
- 製作日期：2025-10-01（老化 196 天）
- 平台已知 breaking：n8n v1.62 改版 Webhook 節點介面
- 建議動作：回爐重做 Section 03 步驟截圖

### ...

## REVIEW（中優先）

...

## OK

{僅摘要：N 頁、平均老化 XX 天、最老那頁 XX 天}

## 缺 metadata（無法判斷老化）

- {file-path}（無 data-platform-version 或 data-built-at）
- ...
建議：補 metadata 後重跑本 skill
```

## 執行原則

1. **不跑任何 write 操作**——本 skill 唯讀，只產報告
2. **WebFetch 失敗視為 no-op**，不阻擋報告產出
3. **老化天數計算不含時差**——都用 date，不用 datetime
4. **批次使用 Grep / Glob 代替逐檔 Read**——全站掃描可能有幾百頁，逐檔 Read 會爆 context
5. **報告長度控制**——若 REFRESH 超過 20 條，只列前 10 條 + 剩餘條數摘要

## 與其他 skill 的串接

- 看完報告決定要重做哪頁後，依頁面的 slug + unit_id → 叫 `/course-designer <slug> <unit-id>` 重跑完整教案／學員路徑 → 講義設計師重建 HTML → 重新做入口、冷讀、理解與遷移驗證
- 若只是截圖漂移、教案本身沒變，可跳過 designer 直接改 HTML；只要學員操作、判斷、產物或修復路徑有變，就必須回到完整教案並重跑相應驗證

## Step 7：批次升 metadata（auto-bump）

當使用者對某些 `REVIEW` 或 `OK-但希望重新計時` 的頁做完人工審閱後，呼叫 `docs/bump-metadata.py` 把 `data-built-at` 更新為今天（老化歸零）。若平台實際升版（例 n8n v1.58 → v1.62），同時帶 `--platform-version` 旗標批次更新。

### 使用時機

- **僅重新計時**（平台未升版、內容驗過）：只升 `built-at`
- **平台真升版**：同時升 `platform-version`（需使用者確認新版本字串）
- **refresh 完教案後**：重建 HTML 時 lesson-template 的新 `built-at` 會自動帶入，**不需再跑這個腳本**

### 操作步驟（由總籌呼叫）

```bash
# 1. Dry-run 確認要動哪些檔
python3 docs/bump-metadata.py courses/<slug>/CH1-1.html courses/<slug>/CH1-2.html --dry-run

# 2. 確認後拿掉 --dry-run
python3 docs/bump-metadata.py courses/<slug>/CH1-1.html courses/<slug>/CH1-2.html

# 3. 平台升版的話
python3 docs/bump-metadata.py courses/<slug>/ --platform-version "n8n v1.62" --dry-run
python3 docs/bump-metadata.py courses/<slug>/ --platform-version "n8n v1.62"

# 4. git commit（pre-commit hook 會跑 lint；但 metadata 欄位 lint 只 WARN 不擋）
```

### 安全邊界

- **禁止**用 bump 跳過真實 refresh：若頁面內容該改卻懶得改而去 bump built-at，屬於技術債偽裝成通過
- **禁止**對缺 metadata 的頁硬塞：先回 lesson-template-v3.html 補欄位，再重建頁，而非手動插 metadata
- bump 完要 `git diff` 抽樣看一兩檔，確認未誤改其他內容

## 預期使用頻率

- 每季一次手動跑 `/course-refresh all` 做全域巡查
- 每次正式上課前跑 `/course-refresh <該課 slug>` 做課前健檢
- 學員反映「步驟跟實際對不上」時立即針對該頁跑檢測

介面老化只觸發重查；確認實際漂移後，由 course-repair 修正文／HTML，並使受影響 evidence.json 紀錄重新驗證。不能按日期直接推定內容錯誤。
