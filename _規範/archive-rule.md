# archive-rule.md — 課程網頁 repo 重新分類規則

> 狀態：**草案，待使用者審核**　｜　制定：Claude Code + Codex 共審（call `1b409309`）　｜　日期：2026-05-16

---

## 1. 目的與原則

repo（GitHub Pages，`SKYPAI0326/courses`，main 分支根目錄即站根）歷經補釘式修改，講義 HTML、教案、大綱、規範、列印 PDF、簡報、驗證產物、iCloud 衝突副本混在一起。本規則重新分類，使 **GitHub 上只保留：網頁講義 + 可下載素材包 + 發布工具鏈 + 製作 SSOT**。

**判定硬準則（Codex 補強）**：凡是 public URL 可存取、被 HTML `href`/`src`/`canonical`/`og` 連結、被 `sitemap.xml`/`search-index.json` 收錄、或被課程製作 skill / CLAUDE.md 明確引用者 —— **不得只因資料夾名稱像草稿就移走**；移走前必先解除這些引用。

**移出檔去向**：repo 旁姊妹資料夾 `../課程製作-內部/`（同 iCloud 路徑，自動備份，不進 git）。

---

## 2. 七類分類學（Codex 修訂版）

| # | 類別 | 處置 | git |
|---|------|------|-----|
| 1 | Public delivery（正式 HTML、正式 assets、可下載 zip） | 留 repo 原位 | tracked |
| 2 | Publish toolchain（建置/注入腳本、SEO 檔） | 留 repo 原位 | tracked |
| 3 | Production SSOT（跨課程重複引用的大綱/教案/規範核心） | 留 repo 原位 | tracked |
| 4 | Course-specific internal SSOT（單課講師指引、修正計畫、稽核報告、章節草稿） | 移姊妹資料夾 | untrack |
| 5 | Source/generator（素材包 source、PPTX/PDF/docx 原檔、源素材） | 移姊妹資料夾 | untrack |
| 6 | Validation/review/refactor 產物 | 移姊妹資料夾 | untrack |
| 7 | Duplicate/sync 副本 | 內容相同→刪；不同→移 quarantine | — |

---

## 3. 留 repo 清單（類別 1–3，不可動）

### 類別 1 — Public delivery
- `courses/**/*.html` 全部單元頁/總覽頁/module 頁，**但排除** courses 內的 `_refactor/ _reviews/ _validation/ _報告/ _講師指引/ _local/` 子資料夾（見類別 4/6）
- `courses/*/assets/`、`courses/*/_assets/` 內被 HTML 連結的正式素材：`.zip` 素材包、`n8n-starter-kit/`、`workflows/`、`datasets/`、課程圖檔、`*.css`、`*.js`
- 根 `index.html`、`search.html`
- `素材/og-default.png`（**修正項**：被 `index.html` 的 `og:image` 用絕對 URL 引用，現被 `.gitignore` 的 `素材/` 誤排除 → 應改為 tracked，見 §6）

### 類別 2 — Publish toolchain
- `docs/*.py`（含 `build-search-index.py`、`build-sitemap.py`、`lint-page.py`、`build-print-pdf.py` 等）、`docs/*.sh`、`docs/hooks/`
- `inject_gate.py`
- 根 `sitemap.xml`、`robots.txt`、`.nojekyll`、`search-index.json`
- `CLAUDE.md`、`COURSES.md`、`.gitignore`

### 類別 3 — Production SSOT
- `_outlines/`（全部 .md，排除 `* 2.md` 副本）
- `_lessons/`（全部 .md，排除 `* 2.md` 副本）
- `_規範/` 核心（Codex 認定跨課程 SSOT）：
  `design-tokens.md`、`lesson-template-v3.html`、`course-index-editorial-strict.html`、`course-index-module-landing.html`、`course-index-lesson-section.html`、`課程製作團隊系統手冊.md`、`飛輪規則.md`、`_gates-template.md`、`lesson-plan-template.md`、`prompt-language-refinement.md`、`設計升級v4-CCS語彙傳播.md`、`G3-人眼驗收清單.md`、`140h-樣本化課程架構.md`（暫留——`courses/gen-ai-140h/CLAUDE.md` 明確引用；長期建議搬入該課程內部）
- `_規範/archive-rule.md`（本檔）

---

## 4. 移出清單（類別 4–6 → `../課程製作-內部/`）

### 類別 4 — Course-specific internal SSOT
| 來源 | 去處 |
|------|------|
| `_規範/CH1-1~CH2-4 assignment-draft-v1.md`（8 檔） | `_規範-內部/` |
| `_規範/140h-課堂作業-CH1-1實作計畫.md`、`140h-課堂即時作業-design.md`、`140h-實作擴充審計-part1.md`、`180h-data-track-system.md`、`Gen AI基礎課程修正計畫.md` | `_規範-內部/` |
| `courses/gen-ai-140h/_講師指引/`、`_報告/`、`_進度/` | `courses/gen-ai-140h/` |
| `courses/n8n/CLAUDE_CODE_FIX_BRIEF.md`、`_change-log.md` | `courses/n8n/` |
| `courses/ipas-ai-beginner/_lessons/`、`_outlines/`、`_local/`、`sources/` | `courses/ipas-ai-beginner/` |

### 類別 5 — Source / generator
| 來源 | 去處 |
|------|------|
| `_sources/`（gen-image / line-stickers / prompt-basic 源素材 .md + images） | `_sources/` |
| `courses/gen-ai-140h/_pdf/`、`courses/office-ai/_pdf/`、`courses/prompt-basic/_pdf/`（列印 PDF） | `_pdf/` |
| `courses/n8n/assets/n8n-sample-pack/`（解壓產物）、`n8n-sample-pack-source/`（含 source 腳本 + PPTX） | `courses/n8n/sample-pack-src/` |
| 全 repo `*.docx`、未打包的 `*.pptx` 原檔 | `_archive/原檔/` |
| `講義建立/`（本地 dev server + portable-kit） | `講義建立/` |

### 類別 6 — Validation / review / refactor
| 來源 | 去處 |
|------|------|
| `courses/gen-image/_refactor/` | `courses/gen-image/_refactor/` |
| `courses/n8n/_reviews/`、`courses/n8n/_local/` | `courses/n8n/` |
| `courses/ipas-ai-beginner/_local/` | `courses/ipas-ai-beginner/` |
| `courses/office-ai-cases/_validation/` | `courses/office-ai-cases/` |
| `_pilots/`（pilot-a/b/c + ccs-foundations-marquee，見 §5-A） | `_pilots/` |
| `_進度/`、`tmp/` | `_archive/` |

### 類別 7 — Duplicate / sync 副本
- 全 repo `* 2.html`、`* 2.md`、`* 2.png` 等 iCloud 衝突副本（已抽驗 3/3 與本尊內容相同）。
- 處置：**逐檔 `diff` 比對**，內容相同 → 直接 `rm`；內容不同 → 移 `_archive/quarantine/` 不刪。
- 已知範圍：`courses/career-pivot-mid/* 2.html`（17）、`_lessons/career-pivot-mid/* 2.md`（11）、`_outlines/* 2.md`（2）、`_sources/gen-image/images/* 2.png`（12）、`courses/gen-image/_refactor/* 2.md`（8）。全部已被 `.gitignore` 排除，刪除零發布風險。

---

## 5. 搬移前必修的連結／收錄問題（關鍵，先修才能搬）

**A. `_pilots/ccs-foundations-marquee/` 的 canonical 漂移**
`courses/ccs-foundations/index.html` 的 `og:url` 與 `canonical` 指向 `_pilots/ccs-foundations-marquee/index.html`。但 `courses/ccs-foundations/` 才是完整正式課程（16 頁，含 CH5；marquee 僅 13 頁、較舊）。
→ **修正**：把該頁 `og:url`/`canonical` 改指 `https://skypai0326.github.io/courses/courses/ccs-foundations/index.html`。修完 `_pilots/` 即可整個移出。

**B. sitemap / search-index 收錄了內部頁**
以下 3 頁因位於 `courses/` 子夾被 `build-*` 腳本掃進索引：
- `courses/gen-image/_refactor/講義-合併.html`
- `courses/n8n/_reviews/lite-pack-cli-verify.html`
- `courses/n8n/_reviews/lite-pack-demo-script.html`
→ **修正**：移出 `_refactor/`、`_reviews/` 後重跑 `build-sitemap.py` + `build-search-index.py`，索引自動清除。

---

## 6. `.gitignore` 調整
- 新增：`_pilots/`、`_sources/`、`講義建立/`、`courses/n8n/sample-pack-src/`（移出後防誤加）
- 新增：`*.pptx`（unzipped PPTX 一律不追；素材以 `.zip` 交付）；若未來確需追某檔，用 `!` 白名單明列
- 修正：`素材/` 改為 `素材/*` + `!素材/og-default.png`（保留 OG 圖為公開 web 資產）

---

## 7. 姊妹資料夾結構
```
01-PROJECTS/
├── 課程專用網頁/          ← git repo（網站本體）
└── 課程製作-內部/          ← 新建，不進 git，iCloud 自動備份
    ├── _規範-內部/
    ├── _sources/
    ├── _pdf/
    ├── _pilots/
    ├── _進度/
    ├── 講義建立/
    ├── courses/           ← 鏡像各課程內部子夾（保留來源可追溯）
    │   ├── gen-ai-140h/{_講師指引,_報告,_進度}/
    │   ├── gen-image/_refactor/
    │   ├── n8n/{_reviews,_local,sample-pack-src}/
    │   ├── ipas-ai-beginner/{_lessons,_outlines,_local,sources}/
    │   └── office-ai-cases/_validation/
    └── _archive/
        ├── 原檔/          ← docx / pptx 原檔
        ├── quarantine/    ← 內容不同的「… 2」副本
        └── tmp/
```

## 8. zip 素材包同步規則（Codex 風險提醒）
repo 只留 `n8n-sample-pack.zip`（學員下載用）；其 source 與生成腳本移至 `課程製作-內部/courses/n8n/sample-pack-src/`。
→ **規定**：每次更新 zip，須在 `sample-pack-src/` 留下 `version`、`sha256`、`生成命令`，否則未來無法重打包。

---

## 9. 不可動清單（移動或刪除會破壞網站／製作流程）
`courses/**/*.html`（正式頁）、`courses/*/assets/` 正式素材、根 `index.html` `search.html` `sitemap.xml` `robots.txt` `.nojekyll` `search-index.json`、`docs/*.py`、`inject_gate.py`、`_outlines/`、`_lessons/`、`_規範/` 核心（§3）。

## 10. 回滾方式
全程於分支 `chore/repo-reorg` 執行；姊妹資料夾在 iCloud，未 `push` 前 `git switch main` + 刪分支即完全復原；被移檔在姊妹資料夾完整保留，可隨時移回。
