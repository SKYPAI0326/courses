---
name: course-handout-designer
description: Use when explicitly requested to design a standalone learner handout. Normal course lesson production uses course-designer, which references this skill's shared teaching contracts.
---

# 完整講義設計方法

把主題、大綱或破碎草稿寫成學員可獨立閱讀與完成任務的講義。正常流程由 course-designer 使用本方法；單獨呼叫時由本次執行者負責同一份正式正文，不產生第二份教學版本。

`$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁`

## 依任務讀取

- 多單元課程或有前後依賴的單課：讀 [course-spine](references/course-spine.md)，使用既有 Blueprint；獨立單課在教案內記起點、診斷、補救及目標即可。
- 所有單元：讀 [lesson-type-contract](references/lesson-type-contract.md)，選 `concept`、`skill-operation`、`programming` 或 `integration-capstone`。
- 任務事實、正式正文及狀態：`$BASE/_規範/learner-action-contract.md`。
- 充分性、示範、有效重練與去重：`$BASE/_規範/course-content-substance.md`。
- 句意、指涉與銜接：`$BASE/_規範/llm-prose-risk-gate.md`。
- 涉及素材：讀 [asset-discoverability-gate](references/asset-discoverability-gate.md)。

## 設計與撰寫

1. 找出學員需要的前置能力，提供可觀察的起點診斷與補救。由能力增量決定單元必要性，不以工具、檔案或時數堆疊章節。
2. 在既有大綱或教案內部區列出核心方法與所需證據。初稿後補入正文位置與實際引用；改變範圍需附理由，不藉刪除核心項目通過檢查。
3. 用 `$BASE/_規範/lesson-plan-template.md` 寫正式正文。從問題與用途引入，先解釋必要概念，帶讀完整例子，再讓學員逐步自行判斷與檢查，最後確認結果與使用條件。
4. 所有必要表格、公式、程式、原始資料、推理與完成範例都完整供應。自然段落承擔解釋，清單列舉、表格比較、步驟標示順序；不要求每項證據各占卡片。
5. 缺素材就指定實際製作者（可由同一執行者完成），核對檔案、權限及備援；不能以「教師示範」「此處放案例」或日後提供代替。
6. 同材料可以重練；依共通判準檢查支援減少、提取、判斷與回饋。只有換標題或名字的重印退回重設。

## 審查與交付

依 [quality-gate](references/quality-gate.md) 做正文、語意、依賴與練習審查；獨立審查需要不同執行者時沿用當次授權，否則明示作者自審。正文通過內容審查後可轉 HTML；完整冷跟做及三課序列驗收另行記錄，不能冒充已完成，也不阻擋未依賴真人結果的草稿與試作。

交付一份正式正文與可引用的內部設計／證據表即可，無須為三種資訊分別複製三份正文。隱藏內部設計與教師筆記後仍須能讀懂、完成及自我檢查。檔案路徑、內容審查 hash、實測範圍與未驗部分交給 course-run／reviewer／validator。

## HTML 交接保護

本 skill 只負責完整學員正文與講義設計，不直接改既有 HTML。交給 `build-course-page` 前，明確標示本次是 `content-change`（依已核准正文轉製）或 `syntax-only`／`layout-only`；若 brief 要求不改文字，交接時要求 builder 遵守 `/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md`，保留既有 `.lesson-body` wrapper，不把內容缺口留給排版補寫。

