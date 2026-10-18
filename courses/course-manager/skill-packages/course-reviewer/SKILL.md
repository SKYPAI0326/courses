---
name: course-reviewer
description: Use as a compatibility entry when an existing workflow asks for course review; dispatches review work to course-validator without defining a second quality standard.
allowed-tools: Read, Glob, Grep, Bash
---

# 課程審查相容入口

這個 skill 保留舊有 `/course-reviewer` 呼叫方式，但不再維護第二套檢核矩陣。所有內容、HTML 忠實度、可操作性與試學判準，以 `course-validator` 為唯一標準。

## 接收舊呼叫

```text
/course-reviewer lesson <path>
/course-reviewer html <path>
/course-reviewer site <slug>
```

收到呼叫後，先載入同層 `../course-validator/SKILL.md` 與其 `references/evidence-format.md`，再按下列方式轉送：

- `lesson`：執行 content 驗證，讀正式課程正文與素材，不讀作者摘要代替正文。
- `html`：先確認 content 證據，再執行 fidelity、technical 與 learner-path 驗證。
- `site`：執行全課範圍、連續單元、完整跟做與 release readiness 驗證。

## 相容輸出

舊流程需要 Issue List 時，可以把 validator issue 轉成下列顯示格式，但不得改變嚴重度、責任角色、回送 Gate 或證據狀態：

```markdown
### [BLOCKER] explanation_gap
- 位置：_lessons/demo/unit-1.md:42
- 問題：示範直接給答案，學員看不到判斷過程。
- 回送：G3 / course-designer
- 證據：courses/demo/_validation/content-unit-1.json
```

相容輸出中的 `PASS` 只表示該次驗證通過。它不等於獨立 AI 已完成試學、真人已學會，或課程已獲准發布。

## 邊界

- 不自行編輯課程正文或 HTML。
- 不另外定義品質分數、固定段數、卡片數或風格偏好。
- 不把作者角色切換稱為獨立驗證。
- 不讓 lint、格式齊全或文字摘要取代實際跟做與完成品驗證。
- 發現缺口時，使用 validator 的失敗代碼與 Gate 路由回交唯一責任角色。
