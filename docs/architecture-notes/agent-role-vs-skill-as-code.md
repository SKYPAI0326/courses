---
title: 課程製作團隊系統架構決策：Skill-as-Code vs Agent-as-Role
status: Accepted
date: 2026-04-18
decision: 維持 Skill-as-Code 路線（6 skills + 2 subagents + design-tokens SSOT + lint-page.py）
superseded_by: null
consequence: 成本低、可驗證、pre-commit 硬擋；但視覺檢核靠人眼、擬人化展示弱
---

# 課程製作團隊系統架構決策：Skill-as-Code vs Agent-as-Role

## Status

**Accepted** — 2026-04-18
此決策是對 2026-04 前既有路線的**事後理論化**，不是新決策。寫下來是為了未來誘惑出現（例如想仿建擬人化 UI）時能回頭看為什麼當初這樣選。

## Context

2026-04-18 看到網路上一個「AI agent 辦公室」貼文 — 8 個擬人化角色（蜜醬/花花/地瓜/阿梟/咕嚕/啾皮/彩彩/豆芽），配可視化 UI，主打「24/7 不打烊、同時工作、辦公室福利很好」。

外觀吸睛，且帳面上看起來跟我們的「課程製作團隊系統」很像 — 同樣是 8 角色、同樣有 orchestrator、同樣強調並行。但底下架構天差地遠。

寫這份 ADR 的動機：
1. 為「為何走 skill 路線」留下正式存檔，避免日後被擬人化 UI 誘惑而退回
2. 評估「若要加可視化」的三條技術路徑，選一條不倒退的
3. 提煉「從 AI 辦公室可以偷什麼」的具體提議

## Decision

維持 **Skill-as-Code** 範式。不把 skill 改回獨立 agent。不引入 multi-agent framework（CrewAI / LangGraph / AutoGen）。若需要可視化，走既有資產延伸（supervisor skill + Obsidian Dataview），不另立 stack。

## 兩種範式對照

（完整理論對比見 Obsidian 知識庫 `01-維基/概念/Multi-Agent 架構範式對比.md`。以下是跟本系統有關的摘要。）

| 維度 | Agent-as-Role（AI 辦公室） | Skill-as-Code（本系統） |
|------|---------------------------|-----------------------|
| 載體 | 獨立 LLM 實例 | `~/.claude/skills/course-*/SKILL.md` + `~/.claude/agents/course-*.md` |
| Context | 每 agent 獨立（成本 × N） | 共享 context（成本 × 1.2） |
| 規則承載 | Prompt 內嵌 | `docs/lint-page.py` 可執行化 |
| 品質把關 | Agent 互審（主觀） | 10 個檢核點 G1-G4 + pre-commit hook |
| SSOT | 分散 | `_規範/design-tokens.md` 單一來源 |
| 角色邊界 | 職務導向（前端/後端）→ 易重疊 | 功能導向（PM/設計/檢核/運維）→ 層級分明 |
| 可視化 | 擬人化 UI | supervisor skill 文字儀表 |
| 擴展成本 | 加 agent + 改 orchestrator（線性增） | 加 skill + 改 lint（固定增） |

## 為什麼我們選 Skill-as-Code

1. **成本**：個人開發者，無法負擔 8 × agent 的 token 成本。實測 subagent dispatch 已經比單 session 貴 2-3 倍，8 獨立 agent 會貴 8-10 倍。
2. **可驗證產出**：課程產出是 HTML，有明確 schema / SEO / design tokens → 規則可執行化 → 機器檢核比 agent 互審穩。
3. **維護者是一個人**：skill 統一維護 > 8 個 agent prompt 各自漂移。實務上見 `v2.0 架構轉向` — 規則外化才能終結 skill 膨脹。
4. **產出是靜態資產**：HTML 不需要 agent 持續對話，只需一次性產出 + lint。
5. **已有 `lint-page.py` + pre-commit hook**：client-side 硬擋比任何 agent 互審都強（agent 會被 prompt 誘騙放行，lint 不會）。
6. **功能導向角色比職務導向穩**：PM / 設計 / 檢核 / 運維 是階段流水線，層級清楚；前端 / 後端 / 行銷 這種職務切法在課程製作場景會嚴重重疊（寫文案到底算哪個角色？）。

## 反面情境（何時該重新考慮）

這份決策會過期。以下情境出現時要重評：

- 如果課程要變成「AI 家教即時對話」→ 需要獨立 context 與記憶 → 回 agent 路線
- 如果要做「多課程並行協作」而非「單課程製作 SOP」→ agent 並行比 skill 串接有利
- 如果模型成本大幅下降（10×+）→ token 成本不再是 skill 優勢 → 重評

## 仿建「AI 辦公室」可視化的三條路徑

### 選項 A — 擴展 supervisor skill（低成本）

- **現狀**：`/supervisor` skill 已顯示 session、plans、todos、tasks、scheduled。
- **擴充**：加「當前載入的 skill」指示燈、「subagent 執行狀態」面板、「最近 lint 違規」hotspot。
- **成本**：半天改 skill + 測試。
- **限制**：純 CLI，沒動畫；但對 dev 夠用。
- **評估**：**高 CP 值，順路做**。

### 選項 B — Obsidian Dataview 動態頁（中成本）

- **現狀**：Obsidian 已接中控頁 + Dataview + Tasks plugin。
- **作法**：在 `05-中控/` 建「課程系統狀態頁」— DataviewJS 讀 memory / plans / tasks / COURSES.md，顯示 8 角色卡片與當前狀態（靠 frontmatter 的 status 欄位）。
- **成本**：1-2 天，DataviewJS 寫查詢 + CSS 做角色卡片。
- **限制**：Obsidian 內才能看；無動畫（可放靜態 icon）。
- **評估**：適合做「個人看板」，對外展示仍弱。

### 選項 C — 獨立 Web Dashboard（高成本）

- **作法**：Node/Python 服務讀 Claude Code JSONL transcript + `.claude/plans/` + memory，WebSocket 推播前端，前端用 SVG 角色做動畫。
- **成本**：3-5 天 MVP + 持續維護。
- **限制**：多維護一套 stack；Claude Code transcript format 可能隨版本變動。
- **評估**：**除非要商業化 / 教學展示**，否則不值得。

### 推薦路線

**A + B 組合。** A 給 dev 用，B 給個人看板。**不走 C**。

若需要「對客戶炫技用的擬人化介面」，直接用 Gamma / Canva AI 做靜態簡報 > 自己寫 Web。展示型需求不應該反推架構改動。

## 從 AI 辦公室偷什麼（具體提議）

| 可借鑑 | 怎麼用在本系統 | 工作量 |
|-------|-------------|-------|
| 擬人化角色名字 | 給 6 skill + 2 subagent 取擬人名（例：PM = 阿珮、檢核員 = 小嚴、lesson-writer = 小講、web-builder = 小佈）→ 學員好記、簡報好看 | 30 分鐘命名 + 改 skill/agent 首行 |
| 角色卡片介紹頁 | 在 `_規範/課程製作團隊系統手冊.md` 加「團隊成員」章節（已有表格，可擴充成角色卡片 + 照片 emoji） | 1 小時 |
| 可視化狀態（簡化版） | supervisor skill 加「目前哪個角色在工作」指示燈（基於 TodoWrite in_progress + 最近 dispatch 的 subagent） | 半天（選項 A 的一部分） |
| 「AI 辦公室」敘事框架 | 課程教學時用「AI 辦公室」比喻介紹 multi-agent 概念（學員好懂） | 講義一頁 |

## 不借鑑（明確拒絕）

- **獨立 agent 架構**：成本太高、真相源會分散。
- **「24/7 不打烊」話術**：Claude Code 本來就能用 ScheduleWakeup + CronCreate 跑，不是賣點。
- **8 個職務導向角色切法**：前端/後端/行銷這種切法在課程製作場景邊界模糊。
- **擬人化的疲勞 / 情緒敘事**（「工作累了可以去玩彈珠台」）：agent 沒有累，這是誤導敘事。

## 警戒清單（做仿建時不要犯的錯）

1. **不要為了可視化讓架構倒退**：如果為了畫動畫而把 skill 改成 agent，等於賠本。規則重新塞回 prompt 是最糟的回退。
2. **不要把 lint 規則搬回 prompt**：v2.0 才做完「規則外化」（`docs/lint-page.py` 變成 SSOT），不要為了擬人化又塞回 agent prompt。
3. **不要用動畫掩蓋卡住**：UI 必須反映「真的在跑 vs 在等人」的差異。動畫代表「有心跳」，但不代表「有進展」。
4. **不要取代檢核點（G1-G4）**：擬人化只是皮，G 檢核點是骨。任何可視化不得讓人跳過檢核點。
5. **不要為了對外展示而改 dev 流程**：對外用 Canva/Gamma 做靜態圖 > 改動 dev 工具鏈。

## 資產盤點（仿建前先看這裡）

既有 Claude Code 機制（無需新 stack）：

| 資產 | 可用途 |
|------|-------|
| `supervisor` skill | 聚合狀態顯示（基底） |
| `TodoWrite`（in_progress） | 當前任務即時狀態 |
| `mcp__ccd_session__mark_chapter` | 階段切分 |
| `spawn_task` | 子任務標記 |
| `ScheduleWakeup` / `CronCreate` | 排程喚醒（做「下班後自動跑」的假象） |
| `.claude/plans/` + `memory/` + `MEMORY.md` | 狀態持久化 |
| Claude Code JSONL transcript（`.claude/projects/*/`） | 回放歷史執行 |
| Obsidian Dataview + Tasks plugin | 可查詢的儀表板 |
| pre-commit hook + `lint-page.py` | 真實把關機制 |

光靠這些，選項 A + B 都能完成。

## Consequence

**正面**
- 成本：維持低 token（單 session 共享 context）。
- 品質：pre-commit hook 擋下所有 BLOCKER，agent 無法繞過。
- 維護：規則外化後改一處就全系統同步。
- 可重現：lint 是確定性的，同 HTML 同結果。

**負面**
- 視覺檢核靠人眼（lint 擋得住結構，擋不住「排版亂七八糟」— 已記錄於 memory 系統盲點）。
- 對外展示弱：沒有 AI 辦公室那種擬人化 UI，賣給客戶時故事性弱。
- 擴充到全新 platform（非 HTML）時，lint 優勢不轉移，需要為新領域重新設計規則引擎。

**緩解措施**
- 視覺檢核：保留 G3-pilot 人眼驗收關卡，未來考慮 Chrome MCP 截圖 + vision 模型。
- 對外展示：照「從 AI 辦公室偷什麼」表格執行 — 取擬人名字、做卡片、Gamma 簡報，成本低、不動架構。

## 引用

- 系統現況與進度：`~/.claude/projects/-Users-paichenwei/memory/project_course_design_system.md`
- 系統設計文件：`~/.claude/plans/glowing-meandering-jellyfish.md`
- 系統手冊：`/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/_規範/課程製作團隊系統手冊.md`
- SSOT：`/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/_規範/design-tokens.md`
- Lint 引擎：`/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/docs/lint-page.py`
- 通用理論頁：Obsidian `01-維基/概念/Multi-Agent 架構範式對比.md`
