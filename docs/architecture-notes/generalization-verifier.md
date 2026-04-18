---
title: Generalization Verifier — 系統泛化驗證
status: Proposed
date: 2026-04-18
decision: n8n 12h 課程上線時作為「真正不同類型」壓測，驗證系統不是只能做 AI 課程
consequence: 發現寫死的假設再抽成參數；不要提前泛化
---

# Generalization Verifier

## 問題

目前系統（skills + subagents + lint-page.py + templates）都在「AI 應用課程」這一類型下磨合：

- `_outlines/*.md` 都是 AI/Gen-AI 主題
- `_規範/design-tokens.md` 的顏色範例是 AI 課程情境
- `lesson-template.html` 的內容結構假設「有工具截圖、有 prompt 範例」

**風險**：看起來可重複使用，但其實只在 AI 課程類型下可行。n8n/自動化課程上線時會暴露假設。

## 驗證清單（n8n 12h 課程上線時逐項檢查）

### 1. Outline → Lesson 流程
- [ ] `/course-pm` 生成 n8n 課程大綱，frontmatter 所有欄位能填（無「AI 專用」欄位卡住）
- [ ] `/course-designer` 生成 n8n 單元教案，9 frontmatter + 6 sections 結構仍合理
- [ ] 若某 section（如「試跑包需求」）在 n8n 情境不適用 → 記錄哪些 section 應該改成**條件性**

### 2. Lint 規則
- [ ] `lint-page.py` 跑 n8n 講義頁 0 false-positive
- [ ] 若誤報 → 檢查是否規則寫死 AI 課程假設（如「必須有 prompt-block」）
- [ ] 規則應該是**結構性**（必須有 H1、必須有 main）而非**內容性**（必須提 AI）

### 3. Design tokens
- [ ] n8n 課程主題色（例：橙/紅）不破版
- [ ] 圖示資產（icon、emoji）不綁死 AI 語意
- [ ] `COMMON_WORDS` 黑名單（integrity checker）沒把 n8n 術語誤判

### 4. Subagent 泛化
- [ ] `course-lesson-writer` 讀 n8n 教案能正確產 HTML
- [ ] 若卡在「找不到 prompt 範例」→ subagent prompt 內寫死了 AI 假設，要抽
- [ ] `course-web-builder` 建 n8n index.html 導覽結構正常

### 5. Gate 流程
- [ ] G1→G4 檢核問題對 n8n 課程仍適用
- [ ] 若某題（如「AI 工具選型」）不適用 → Gate Q 應該用**抽象問法**（「核心工具選型」）

## 執行方式

不寫自動化腳本。n8n 課程真正上線時：

1. 跑 `/course-run n8n-12h`
2. 一路做下去，遇到任何「為了這門課我得改系統」的時刻，記錄到本檔的「發現清單」
3. 全部完成後回顧：哪些是**真正泛化漏洞**（改系統）、哪些是**課程特化**（不改系統，該課程自己處理）

## 發現清單（待填）

*此處留空，等 n8n 課程實際上線後補。*

## 不做的事

- **不預先泛化**：YAGNI。等 n8n 真的出問題再抽，不要憑空想像。
- **不跑假資料 E2E 測試**：假資料驗不出真正的類型差異。
- **不改 AI 課程既有頁**：只看新課程，不回溯修舊的。

## 觸發時機

n8n 12h 課程啟動時（預計日期待定）。在課程製作團隊系統手冊 v2.1 時整合本檔發現。
