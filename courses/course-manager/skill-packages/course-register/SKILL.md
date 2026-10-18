---
name: course-register
description: 課程上線註冊。新課程完成 HTML 後，透過此 skill 一鍵完成：生成密碼 hash、登錄 inject_gate.py、更新 COURSES.md、更新密碼對照表、（選用）加入統一入口頁卡片、執行密碼注入。銜接 course-web-builder 與 course-ops gates 之間的缺口。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# 課程註冊 Skill

## 角色定位

你是「課程製作團隊系統」中的**註冊員**。課程 HTML 都建好了，但還不算「上線」——因為密碼沒註冊、`inject_gate.py` 不認識這課、COURSES.md 可能沒條目、密碼對照表沒更新。註冊完成只代表上線所需的技術登錄完成，不代表教學內容、冷讀或學員遷移驗收已通過。

**你解決的是**：`course-web-builder` 產完 index.html 之後、`course-ops gates` 執行密碼注入之前，**中間缺的那一塊**。

**DoD 輸出**：課程完成「5 項註冊動作」：
1. 密碼對照表 `_規範/課程密碼對照表.md` 有條目
2. `inject_gate.py` 的 `COURSES` dict 有條目（key + hash）
3. `COURSES.md` 有課程清單條目（若無）
4. `courses/index.html` 統一入口頁有對應卡片（若該頁存在）
5. 執行 `python3 inject_gate.py` 實際注入密碼關卡

**負面清單**：
- 不改 HTML 內容（那是 lesson-writer / web-builder）
- 不跑 SEO / sitemap（那是 course-ops）
- 不碰大綱或教案

## 專案基準路徑

```
$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/
```

📖 **系統手冊**：`$BASE/_規範/課程製作團隊系統手冊.md`（8 角色流程、G1–G5 Gate 檢核、四課型證據契約）

**本 skill 讀寫的檔案**：
- `$BASE/inject_gate.py`（修改 COURSES dict）
- `$BASE/_規範/課程密碼對照表.md`（加條目）
- `$BASE/COURSES.md`（加條目，若無）
- `$BASE/index.html`（統一入口頁，在**專案根目錄**；加卡片，若存在）
  - 注意：GitHub Pages 的 URL `https://skypai0326.github.io/courses/index.html` 對應的是 repo 根目錄的 index.html（因 repo 名稱為 `courses`）
- `$BASE/courses/{slug}/index.html`（讀取以取得課程名稱、色彩等）
- `$BASE/_outlines/{slug}.md`（讀取 metadata）

## 呼叫格式

```
/course-register <slug>              # 互動模式：問密碼、執行 5 步
/course-register <slug> <password>   # 直接給密碼
/course-register <slug> --check      # 只檢查狀態，不動手
```

## 執行步驟

### Step 1：驗證前置

讀取以下檔案，缺一不可（否則停止並回報）：

1. `$BASE/_outlines/{slug}.md` — 取 `name`, `color`, `audience`, `duration`
2. `$BASE/courses/{slug}/index.html` — 確認課程網站已建

若大綱或 index.html 缺：停止，提示「請先跑 `/course-pm` 和 `course-web-builder`」

### Step 2：檢查當前註冊狀態

對 5 個註冊點各跑一次 grep：

| 檢查項 | 指令（從 `$BASE` 執行） | 已完成的表現 |
|-------|------|-------------|
| inject_gate.py | `grep -c '"{slug}":' inject_gate.py` | > 0 |
| 密碼對照表 | `grep -c '{slug}' _規範/課程密碼對照表.md` | > 0 |
| COURSES.md | `grep -c '{slug}/' COURSES.md` | > 0 |
| **統一入口頁卡片** | `grep -c 'courses/{slug}/' index.html` | > 0 |
| Gate 已注入（課程首頁）| `grep -c 'id="_gate"' courses/{slug}/index.html` | = 1 |
| Gate 已注入（全部頁）| `find courses/{slug} -name "*.html" \| wc -l` vs `grep -rl 'id="_gate"' courses/{slug}/ \| wc -l` | 兩數相等 |

⚠️ 注意：統一入口頁是 **`$BASE/index.html`**（專案根目錄），不是 `courses/index.html`。GitHub Pages URL `/courses/` 的首段 `courses` 是 repo 名稱。

產出狀態表，標註 ✅ / ❌。

**若為 `--check` 模式**：只輸出狀態表，不執行任何修改。停止。

### Step 3：取得密碼

若未提供密碼參數：

1. 推薦預設格式：`{slug 簡稱}{年}`（如 `promptbasic2026`）
2. 用 AskUserQuestion 問使用者要用預設還是自訂

### Step 4：計算 SHA-256 Hash

```bash
echo -n "{password}" | shasum -a 256 | awk '{print $1}'
```

記錄結果為 `$HASH`。

### Step 5：推導 sessionStorage Key

依既有慣例產生（多為 `{縮寫}_auth`）：

| slug 樣式 | 建議 key |
|----------|---------|
| `prompt-basic` | `promptbasic_auth` 或 `pbasic_auth` |
| `n8n-pro` | `n8npro_auth` |
| `gen-ai-XXh` | `genXX_auth` |

先 Glob 現有 `inject_gate.py` 檢查有無撞 key，有則加後綴。

### Step 6：更新 `inject_gate.py`

用 Edit 在 `COURSES = {` dict 尾端（最後一條 `"gen-ai-36h"` 後）追加新行：

```python
    "{slug}":          ("{key}",  "{hash}"),
```

對齊既有格式（欄位用空白對齊）。

### Step 7：更新 `_規範/課程密碼對照表.md`

兩處各加一行：

**表格區**（「各課程密碼」表）：
```
| {slug} | {課程名稱} | `{password}` | `{key}` |
```

**Hash 區**（供技術驗證）：
```
{slug}  {password}  {hash}
```

### Step 8：更新 `COURSES.md`（若無條目）

在適當位置加一行（對照既有格式）：
```
| `{slug}/` | {課程名稱}（{duration}） | 製作中 | {受眾}，主色 {color} |
```

若已有條目：跳過此步。

### Step 9：更新 `$BASE/index.html`（統一入口頁）

1. 確認 `$BASE/index.html` 存在（正常情況下都存在，repo 根目錄）
2. Read 檔案，找到大綱的 `course_type` 或主題判斷卡片應該插入的分組（AI 應用與培訓 / 自動化工具 / 數位行銷 & 數據分析）
3. 找到該組最後一張 `<a class="course-card">` 結束的 `</a>`，在後面加新卡片
4. 更新該組的 `<div class="section-count">N 門</div>`，數字 +1
5. 卡片結構模板：

```html
    <a class="course-card" href="courses/{slug}/index.html">
      <div class="card-band band-{1-5}"></div>
      <div class="card-body">
        <div class="card-meta">
          <div class="card-tag">{主題標籤} · {子標籤}</div>
          <div class="card-status status-open">開放中</div>
        </div>
        <div class="card-title">{課程名稱}</div>
        <div class="card-desc">{一句話描述課程特色}</div>
      </div>
      <div class="card-footer">
        <div class="card-info">{N} Parts</div>
        <div class="card-info">·</div>
        <div class="card-info">{duration}</div>
        <div class="card-arrow">進入課程 <span aria-hidden="true">→</span></div>
      </div>
    </a>
```

**band 顏色對照**：band-1 陶土橘 / band-2 芥末黃 / band-3 鼠尾草綠 / band-4 霧藍 / band-5 灰藍綠。依大綱 color 反推對應 band 編號。

### Step 10：執行密碼注入 + 重建索引與 sitemap

```bash
cd "$BASE"
# 10a. 注入 gate
python3 inject_gate.py

# 10b. 更新 build-search-index.py 的 COURSE_LABEL dict（Edit 加一行）
#     "{slug}": "{簡短顯示名}",
# 否則 search-index.json 會以 raw slug 顯示

# 10c. 重建全站索引 & sitemap（冪等）
python3 docs/build-all.py
```

驗證：
```bash
grep -c 'id="_gate"' courses/{slug}/index.html            # = 1
grep -rL 'id="_gate"' courses/{slug}/**/*.html            # 無輸出
grep -c "courses/{slug}/" sitemap.xml                     # = 該課程頁數
```

### Step 11：產出註冊報告

```markdown
## 課程註冊完成：{slug}

**課程名稱**：{name}
**密碼**：{password}
**sessionStorage Key**：{key}
**SHA-256 Hash**：{hash}

### 註冊項目狀態

| # | 項目 | 狀態 |
|---|------|------|
| 1 | 密碼對照表 | ✅ |
| 2 | inject_gate.py COURSES dict | ✅ |
| 3 | COURSES.md 條目 | ✅ / SKIPPED（已存在）|
| 4 | 統一入口頁卡片 | ✅ / N/A（index.html 不存在）|
| 5 | 密碼關卡注入 | ✅ ({N} 頁) |

### 下一步建議

- 驗證：開瀏覽器測試 `courses/{slug}/index.html`，輸入密碼 `{password}` 確認可進入
- 部署：`git add . && git commit -m "feat: register {slug}" && git push`
- 運維檢查：`/course-ops {slug} all` 跑 SEO/連結/sitemap
```

---

## 錯誤處理

| 情境 | 應對 |
|------|------|
| 大綱不存在 | 停止，提示先跑 course-pm |
| `courses/{slug}/` 不存在 | 停止，提示先跑 course-web-builder + lesson-writer |
| key 已被占用 | 自動加後綴（如 `pbasic2_auth`），在報告中標註 |
| hash 計算失敗 | 停止並回報 shasum 指令問題 |
| inject_gate.py 執行錯誤 | 保留其他步驟成果，只報告 gate 注入失敗 |

## 執行原則

1. **冪等性**：重跑 skill 不應破壞既有設定。Step 2 先檢查狀態，已完成的步驟自動跳過
2. **密碼對照表不推送**：`_規範/課程密碼對照表.md` 已在 .gitignore，密碼只在本地
3. **不自動決定密碼**：一定要讓使用者確認密碼值（除非 `--non-interactive` 模式）
4. **註冊後要跑一次注入**：Step 10 是必要的，不能只改 dict 不注入

## 與其他角色的交接

```
course-web-builder 產完 index.html
      ↓
**course-register ← 本 skill（填補缺口）**
      ↓
course-ops {slug} all（SEO/連結/sitemap/audit）
      ↓
部署推送
```

## HTML 編輯保護契約（必讀）

HTML 作業前讀 [SKILL.md](/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md)，依該契約宣告變更類型，執行 DOM／文字保護、共用結構檢查、代表頁 RWD／scroll state 驗證及回復規則；驗收與授權狀態據實回報。

本角色責任：HTML 操作限 gate 注入或必要 layout-only；保留 gate count 檢查與失敗回復。
