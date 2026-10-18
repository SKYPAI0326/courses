---
name: course-designer
description: Use when turning a course outline into lesson plans, especially when concepts need complete explanations, worked examples, learner decisions, and teaching assets before HTML production.
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion
---

# 課程設計師

正常產製流程的單元內容主責。由已確認的大綱產出完整學員正文、示範、練習與答案，再交內容審查與 HTML 轉製。角色可由同一執行者依序完成；本 skill 不自動派遣代理。

## 路徑與入口

`$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁`

- `/course-designer <slug> <unit-id>`：讀 `_outlines/{slug}.md`、對應 Style Guide 與必要來源；產出 `_lessons/{slug}/{unit-id}.md`。
- `/course-designer pilot <pilot-id>`：讀 `_pilots/{pilot-id}.md`，產出 `_pilots/_lessons/{pilot-id}.md`。試作只縮小範圍，不省略教學證據。
- 不存在的必要大綱先交 course-pm；缺少已知範圍的 Style Guide 可按模板建立，未知的定位條件才詢問。

## 必讀來源

1. `$BASE/_規範/learner-action-contract.md`：任務、正式正文邊界與狀態。
2. `$BASE/_規範/course-content-substance.md`、`llm-prose-risk-gate.md`：解釋、練習、去重與語文判準。
3. `../course-handout-designer/references/course-spine.md`、`lesson-type-contract.md`：起點、能力進展與四課型證據。
4. `../course-handout-designer/references/asset-discoverability-gate.md`：素材取得。
5. `$BASE/_規範/lesson-plan-template.md`：單一正式正文與內部設計模板。

## 執行

1. 核對起點診斷與補救、本課能力增量、前後課用途及專業來源。工具現況需查證；不確定的重要事實記待查，不能用流暢文案掩蓋。
2. 確認任務與適用環境。對缺少的素材記明製作者、輸入、實際檔案與測試；可由當前執行者製作樣本、程式或表格。核心依賴未解時標 BLOCKED，繼續其他可完成部分，不能把需求清單當成素材已完成。
3. 在內部區列出目標對應的核心概念／方法與所需證據，再在 learner-content 標記內寫出學員能獨立閱讀的正文。先教必要前提，再展示完整輸入、理由、中間結果與成品，安排有回饋的練習與使用條件。不套固定段數、概念數或題數。
4. 跨段核對主詞／指涉、資料一致性與因果；逐步核對當時已存在的材料與狀態。檢查不得引用後續才建立的成果。
5. 遮住內部區與教師筆記，沿正文完成一次作者自驗。保存實際計算、程式輸出或判斷與卡點，明示 author-self-check；不填真人跟做 PASS。
6. 交 course-reviewer 做 content 審查，依 evidence-format.md 保存來源 hash、引用與結論。內容缺漏回修本檔；審查通過後由 build-course-page 忠實轉製。只有一份正式正文，handout-designer 方法不另產競爭版本。

## 交付

回報正式來源、素材、內容審查紀錄與下一步；區分設計已完成、機器已檢查與真人待驗。完整句與連續推理是產出責任，不能留給排版或 copywriter 發明。

## HTML 交接保護

本 skill 產出正式正文與教學事實，不直接以 HTML 排版補內容。交給 builder 前，明確標示是否為 `content-change`；若使用者要求不變更文字，後續只能做 `syntax-only`／`layout-only`，並要求讀 `/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md`，不得為了補版面新增段落或改變 wrapper。
