# 課程資料夾對照表

> ⚠️ **本文件為人工備忘錄，非 SSOT。** Codex L3 audit `7dcf26e4` 指出本檔已與實況脫鉤（如 `ai-workshop` 寫「4 Parts」實為 `session1+` 結構、多課寫「4 Parts」實為 5-6 parts）。
> Phase C 規劃以**機器可讀 course manifest** 取代本檔的「結構描述」職能。在那之前，**請以 `ls courses/<slug>/` 為準**。
> 本檔暫時保留作為「課程清單 + 命名 + 學員/工具/主色」摘要。

## 資料夾結構

```
課程專用網頁/           ← 根目錄：規則、工具、統一入口
├── index.html          ← 統一課程入口
├── CLAUDE.md           ← 專案規範
├── COURSES.md          ← 本檔（課程清單摘要）
├── _outlines/          ← 課程大綱（Markdown）
├── _規範/              ← 設計規範（design-tokens.md = SSOT）
├── _進度/              ← 進度追蹤
├── _pilots/            ← 試產物（lint exclude，不套合規規則）
├── 素材/               ← 教學素材
├── 講義建立/           ← 講義製作器（server.py + index.html）
└── courses/            ← 所有課程（14 門，2026-04-26）
    ├── ai-workshop/
    ├── ccs-foundations/
    ├── digital-marketing-70h/
    ├── gemini-ai/
    ├── gen-ai-140h/
    ├── gen-ai-36h/
    ├── gen-image/
    ├── gtm/
    ├── n8n/
    ├── ntub-gtm-adtech/
    ├── ntub-seo-ga4/
    ├── office-ai/
    ├── prompt-basic/
    ├── simple-ai/
    ├── line-stickers/
    └── career-pivot-mid/
```

## 命名規範

- 課程資料夾：全小寫英文，連字號分隔（kebab-case），統一放在 `courses/`
- 每門課根目錄放 `index.html`（課程總覽頁）
- ⚠️ 既有實況：14 個課程的內部命名實際分多軌（`session/part/module/ch/lessons` 並存），未統一。Phase C 待整理。

## 課程大綱資料夾

`_outlines/` 存放各課程的 Markdown 大綱文件（`{slug}.md`）。
建立新頁面時，Claude 會先讀取對應大綱，自動取得主題色、學員背景、章節結構，無需重複詢問。
範本：`_outlines/_template.md`

---

## 現有課程（14 門）

| 資料夾 | 課程名稱 | 狀態 | 學員 / 工具 / 主色 |
|--------|---------|------|-------------------|
| `ai-workshop/` | AI 實務全攻略（12h/18h） | 完成 | 雙時數版本（index.html + index-12hr.html）；主色霧藍 |
| `ccs-foundations/` | CCS 生成式 AI 認證研習 | 完成 | 扁平 13 頁，含 80 題模擬測驗與提示詞範本庫；主色灰藍綠；**v4 Editorial 範本** |
| `digital-marketing-70h/` | 數位行銷人才培訓（70hr） | 完成 | 10 模組 52 單元，整合 GTM/SEO/GA4/廣告/Email；主色芥末黃 |
| `gemini-ai/` | Gemini 零代碼 AI 實戰課 | 完成 | part1~5（含 PRAC 頁） |
| `gen-ai-140h/` | 生成式 AI 職訓實務應用班（140h） | 完成 | part1~5，56+12 單元，含 ENV-SETUP；主色陶土橘 |
| `gen-ai-36h/` | 生成式 AI 工作應用班（36h） | 完成 | part1~6，140h 上班族濃縮版，零基礎不寫程式；主色灰藍綠 |
| `gen-image/` | 商業用圖片生成 | 完成 | 5 Modules，13 單元，AI 設計流水線 PM 協作；主色奶茶棕；**v4 Editorial 範本** |
| `gtm/` | GTM 實務演練 | 完成 | part1~6，含 checklist.html |
| `n8n/` | n8n 自動化實戰課 | 完成 | landing + lessons/，4 Modules |
| `ntub-gtm-adtech/` | NTUB GTM × 廣告科技 | 完成 | （學員/結構待補） |
| `ntub-seo-ga4/` | NTUB SEO × GA4 | 完成 | （學員/結構待補） |
| `office-ai/` | 辦公室 AI 工具實務應用 | 完成 | part1~5 |
| `prompt-basic/` | 從「問 AI」到「交辦 AI」（6h） | 製作中 | part1~5，公部門行政人員；主色灰藍綠 |
| `simple-ai/` | 創業數位化 × 創業懂行銷（3h） | 完成 | 2 Modules + 扁平 CH，含 prompt-library.html；主色鼠尾草綠 |
| `ipas-ai-beginner/` | iPAS AI 應用規劃師初級認證研習（30h） | 建置中 | chapter-flat 10 章，0 基礎友善，certprep Editorial-strict；主色陶土橘；待 course-register |
| `line-stickers/` | AI 自製 LINE 貼圖（12h 兩階段） | 完成 | Part 1 入門 4h（6 CH）+ Part 2 進階 8h（8 CH），自用導向、全免費工具、含 fill-form 互動表單 + 24 張可列印 handout + 17 張 Codex 角色基準圖；主色陶土橘 |
| `career-pivot-mid/` | 8 小時轉職實戰：市場趨勢 × 就業準備 × 轉職技巧（8h 一日密集）| 完成 | 13 CH（Part 1 盤點 6 + Part 2 實戰 7）+ 2 PRAC + PDP×MBTI 雙測獨立頁，含「年紀沒有幫助」核心心法；主色霧紫 |

> 上述「狀態」「主色」可能未即時反映實況。「結構描述」一律以 `ls courses/<slug>/` 為準。

---

## 檔案命名規則

| 類型 | 格式 | 範例 |
|------|------|------|
| 課程總覽 | `index.html` | — |
| 章節頁 | `CH[章]-[節].html` | `CH1-1.html` |
| 實例演練頁 | `PRAC[章]-[節].html` | `PRAC1-1.html` |
| 模組總覽頁 | `module[N].html` | `module1.html` |
| 課程大綱文件 | `course-outline.docx` | — |

⚠️ 既有實況不全遵守此規則（如 `ai-workshop/session1/`、`gen-ai-140h/ENV-SETUP.html`、`n8n/lessons/`、`simple-ai/prompt-library.html`）。Phase C 將決定「強制統一」或「承認多軌 + 機器 manifest 校驗」。

---

*最後更新：2026-04-26（Codex L3 audit 後重寫，移除過時內容、加 SSOT 警告）*
