---
name: course-ops
description: 課程網頁運維工程師。處理 SEO meta 注入、連結驗證、sitemap 生成、批次密碼關卡注入、效能稽核、部署就緒檢查。在 G4 收尾後、部署前執行。
---

# 運維工程師 (Course Operations)

> 角色定位：課程網頁的「最後一哩路」技術品質確保。不碰教學內容（那是 reviewer 的事），只處理技術完整性與搜尋可見性；本 skill 的 READY 只代表運維檢查通過，不替代學習內容與冷讀 Gate。

## 觸發

```
/course-ops <slug> [seo|links|sitemap|search-index|gates|audit|all]
```

- `slug`：課程 slug（如 `gen-ai-36h`），或 `all` 掃描全部課程
- 子命令省略時預設 `all`

## 硬邊界

- **做**：inject / validate / generate / audit / report
- **不做**：內容品質判斷、教學邏輯檢核、視覺排版評估（那是 course-reviewer）
- **不改**：教案 .md、Style Guide、大綱

## 專案基準路徑

所有相對路徑以下列目錄為根（稱作 `$BASE`）：

```
$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/
```

📖 **系統手冊**：`$BASE/_規範/課程製作團隊系統手冊.md`（8 角色流程、G1–G5 Gate 檢核、四課型證據契約）

**本 skill 操作的路徑**：
- 掃描目標：`$BASE/courses/{slug}/**/*.html`
- 產出：`$BASE/courses/{slug}/sitemap.xml`、各 HTML 的 `<meta>` 注入
- 工具：`$BASE/inject_gate.py`（密碼關卡腳本）
- 設計規範：`$BASE/_規範/design-tokens.md` § 8 Metadata 規格

---

## 子命令詳細規格

### 1. `seo` — SEO Meta 注入

**目的**：確保每個 HTML 頁面都有正確的 `<meta>` 和 OG 標籤。

**執行步驟**：

1. Glob `courses/{slug}/**/*.html` 列出所有頁面
2. 逐頁檢查 `<head>` 是否已含：
   - `<meta name="description" content="...">`
   - `<meta property="og:title" content="...">`
   - `<meta property="og:description" content="...">`
3. 若缺少，從頁面內容推導：
   - `description`：讀 `.lesson-tagline` 或 `.page-subtitle` 文字
   - `og:title`：讀 `<title>` 標籤
   - `og:description`：同 description
4. 用 Edit 工具注入缺失的 meta 到 `<head>` 內（`<meta charset>` 之後）
5. 產出報告：每頁狀態（已有 / 已注入 / 無法推導）

**模板**：
```html
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
```

### 2. `links` — 連結驗證

**目的**：找出所有斷裂的內部連結。

**執行步驟**：

1. Glob `courses/{slug}/**/*.html` 列出所有頁面
2. Grep 每頁的 `href="` 和 `src="` 屬性值
3. 過濾：只驗證**相對路徑**（跳過 `http://`、`https://`、`#`、`javascript:`）
4. 對每個相對路徑，從該 HTML 的所在目錄解析實際路徑
5. 用 Glob 確認目標檔案存在
6. 產出報告：
   - OK：`{file}:{line} → {target} ✓`
   - BROKEN：`{file}:{line} → {target} ✗ (file not found)`

### 3. `sitemap` — Sitemap 生成

**目的**：重建全站 `sitemap.xml`（位於 `$BASE/sitemap.xml`，非單一課程）。

**工具**：`docs/build-sitemap.py`（冪等，全站重建）

**執行步驟**：

```bash
cd "$BASE" && python3 docs/build-sitemap.py
```

腳本會：
- 掃描 `$BASE/index.html` + `$BASE/courses/**/*.html`
- 自動排除 `_backup*` / `_pilots` / `.git`
- 依頁型設 priority（root=1.0 / index=0.9 / module=0.8 / lesson=prac=0.7 / page=0.5）
- 從檔案 mtime 取 `lastmod`
- 寫入 `$BASE/sitemap.xml`

**驗證**：
```bash
grep -c '<loc>' sitemap.xml           # 應 = 全站 HTML 數 + 1（站首頁）
grep "courses/{slug}/" sitemap.xml    # 該課程所有頁應出現
```

**注意**：本專案採「全站單一 sitemap」架構（非每課程一份），因為 GitHub Pages `courses/` repo 只需要一份。

### 3.5 `search-index` — 搜尋索引重建

**目的**：重建 `$BASE/search-index.json`，供 `search.html` 使用。

**工具**：`docs/build-search-index.py`

```bash
cd "$BASE" && python3 docs/build-search-index.py
```

**何時跑**：
- 任何 HTML 新增、修改、刪除後
- 新課程註冊後（`course-register` 跑完時順便跑一次）
- 通常由 `course-lesson-writer` Step 7 自動跑，但手動重跑也 OK（冪等）

**新課程注意**：若 slug 不在 `docs/build-search-index.py` 的 `COURSE_LABEL` dict，索引會用 slug 本身當顯示名。註冊新課程時**同步更新 COURSE_LABEL dict**（5 秒工作）。

### 4. `gates` — 批次密碼關卡注入

**目的**：對課程所有 HTML 頁面注入 JS SHA-256 密碼關卡。

**工具**：`inject_gate.py`（位於課程網頁根目錄）
- 路徑：`/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/inject_gate.py`
- 腳本內建所有課程的 sessionStorage key + SHA-256 hash 對照表
- 已注入的頁面（含 `id="_gate"`）自動跳過，可安全重複執行

**執行步驟**：

1. 確認腳本存在：`ls inject_gate.py`（從課程網頁根目錄）
2. 確認目標課程在腳本的 `COURSES` dict 中有對應條目：
   - 用 Grep 搜尋 `inject_gate.py` 中的 `"{slug}":` 字串
   - **若不存在**：**停止並 ERROR**（不繼續、不靜默跳過）。訊息：
     ```
     ❌ ERROR: {slug} 未在 inject_gate.py 的 COURSES dict 中註冊。
        Gate 注入會靜默跳過此課程，造成密碼關卡失效。
        先執行 /course-register {slug} 完成註冊，再重跑 /course-ops {slug} gates。
     ```
   - 這是硬邊界：course-ops **不替你註冊**，註冊是 course-register 的職責
3. 執行注入：
   ```bash
   cd "/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁" && python3 inject_gate.py
   ```
   - 腳本會自動遞迴掃描 `courses/` 下所有 HTML，按 `COURSES` dict 對應注入
   - 若只需單一課程，腳本目前不支援 slug 參數（會跑全部，但已注入的自動跳過，效能可接受）
4. 驗證注入結果：Grep `id="_gate"` 確認目標課程的每頁都已注入
   ```bash
   grep -rL '_gate' courses/{slug}/**/*.html
   ```
   - 有輸出 = 還有頁面未注入（異常）
5. 產出報告：注入成功 / 已存在（跳過）/ 異常的頁數

**注意**：
- `pilot: true` 的試飛課程**不在 COURSES dict 中**，不會被注入（正確行為）
- 新課程上線前，需先更新 inject_gate.py 的 COURSES dict（密碼用 `echo -n "密碼" | shasum -a 256` 計算）
- 密碼對照表見 `_規範/課程密碼對照表.md`（gitignore，不推送）

### 5. `audit` — 規則合規稽核

**工具**：`docs/lint-page.py`（單一真相源）

```bash
cd "$BASE" && python3 docs/lint-page.py courses/{slug}/
```

報告規則與嚴重度分級都由 lint 產出，本 skill **不重述規則**。改規則去改 `lint-page.py`。

可選旗標：
- `--summary` 只看統計
- `--no-warn` 只顯示 BLOCKER + ERROR

### 6. `all` — 完整運維檢查

依序執行：`audit` → `links` → `seo` → `gates` → `search-index` → `sitemap`

<!-- anchor:course-pdf-sync -->
若 `$BASE/courses/course-manager/registry/pdf/catalog.json` 存在，交付前執行 PDF 唯讀檢查：

```bash
python3 /Users/paichenwei/.agents/skills/course-pdf/scripts/run.py --root "$BASE/courses" sync --course {slug}
```

當 slug 是 `all` 時省略 `--course`。只回報有登錄的成品；沒有 PDF 不新增交付要求。報告分列來源狀態與最近建置結果；STALE／UNVERIFIED／BLOCKED 不能宣稱 PDF 已同步。若當次交付包含 PDF，需交 `course-pdf` 完成適用驗收；其餘運維與教學 Gate 保持各自責任。此命令不帶 `--create-pdf`，不產製或替換 PDF。


每步驟完成後輸出該段落報告，最後輸出綜合摘要：

```
=== Course Ops Report: {slug} ===
Audit:   {N} errors, {N} warnings
Links:   {N} broken / {N} total
SEO:     {N} injected / {N} already present / {N} failed
Gates:   {N} injected / {N} skipped
Sitemap: Generated ({N} URLs)
Verdict: READY TO DEPLOY / ISSUES FOUND
```

---

## 輸出格式

所有報告使用 Markdown 表格，方便使用者閱讀。嚴重度排序：ERROR > WARN > INFO > OK。

報告結尾固定附上：
- 執行時間戳
- 掃描頁數
- 下一步建議（有問題時列出具體修復指示）

---

## 設計規範引用

本 skill 的 SEO meta 模板和 metadata 規格遵循：
`_規範/design-tokens.md` § 8 Metadata 規格

---

## 注意事項

- `pilot: true` 的課程可跳過 `gates` 和 `sitemap`（試飛不需要）
- 外部連結（https://）不驗證可達性（避免網路依賴），只驗證格式正確
- 本 skill 不負責部署推送（git push 由使用者決定）

## HTML 編輯保護契約（必讀）

HTML 作業前讀 [SKILL.md](/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md)，依該契約宣告變更類型，執行 DOM／文字保護、共用結構檢查、代表頁 RWD／scroll state 驗證及回復規則；驗收與授權狀態據實回報。

本角色責任：HTML 操作限 syntax-only／layout-only；SEO、連結與 gate 注入使用明確 DOM anchor。非講義頁沿用其現有 wrapper。
