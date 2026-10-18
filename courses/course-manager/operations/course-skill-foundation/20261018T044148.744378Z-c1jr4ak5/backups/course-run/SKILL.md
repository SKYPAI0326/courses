---
name: course-run
description: Use when producing a new course across multiple gates, especially before batching lesson pages, inferring user approval, or declaring a course ready from structural checks alone.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 課程流程總籌

依 `$BASE/_規範/課程製作團隊系統手冊.md` 推進新課或恢復工作。讀取現有大綱、`_plan.md`（若有）及 `_gates.md`，以實際產物與版本證據判斷進度，不從 checkbox 自述推定完成。

`$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁`

## 入口

- `/course-run <slug>`：依授權繼續下一個可執行階段。
- `/course-run status <slug>`：唯讀回報階段、已驗範圍、阻塞與下一步。
- `/course-run <slug> G2-part3` 等既有指令可指定範圍，但不能跳過相依證據；Part 數以大綱為準。

## 推進方式

1. G1：由 course-pm 確認受眾起點、能力進展、範圍與成果；先讀既有需求，僅補問影響設計的缺失。已知或已核准資訊不重問。
2. G2：course-designer 使用 handout 方法完成正式正文與必要素材；總籌對每個缺件指定實際製作者、路徑與驗證，可由同一執行者製作。course-reviewer 先做 content 審查，內容不足先修正，不能交給 HTML 現編。
3. G3：先建代表頁；builder／lesson-writer 保真轉製，reviewer 比對正式正文與 HTML、檢查可讀性。依課型與風險驗證試作後再擴大建置；真人驗證另列待辦，不以推測填 PASS。
4. G4：validator 整理技術、完整跟做、理解遷移、平台及連續課證據；ops 完成適用技術檢查。每項證據依 learner-action-contract.md 解讀，技術綠燈不等於可授課。
5. G4.5：已授權範圍內由 register 完成註冊及 gate；試作可以先準備註冊，但不改變教學狀態。
6. G5：合併教學與運維狀態，公開發布依當次授權執行；缺真人證據可交付建置成果與待驗清單，不能稱 HUMAN_READY。

## 執行與存證

- 預設由目前執行者依序切換角色，讀該 skill 並做實際工作；不只提示使用者自己再呼叫下一個指令。
- Agent tool、外部模型及付費服務皆為可選執行方式，須有當次相應授權；沒有時仍可完成本機設計、建置與審查，不建立代理專用的阻塞。
- 以 `_規範/_gates-template.md` 更新 `_gates.md`，引用 `_validation/evidence.json` 與審查紀錄。不存在的真人結果保持 PENDING_HUMAN。
- 改動正文、素材或教法時使相關舊證據失效，只重驗受影響單元與依賴；不以新 Gate 名字繞過舊失敗。
- 機器入口：`bash /Users/paichenwei/.agents/skills/course-validator/scripts/course-validator.sh <slug> all`。回傳碼與待驗狀態見 validator skill。
- 未解的核心內容／素材阻擋相依階段；繼續其他已授權且無相依的工作。

## 回報

說明目前在哪一階段、正式來源與成品位置、已完成哪種驗證、缺什麼及下一個具體動作。不把作者自驗、AI 模擬、平台跑通與真人學會混在一起。

## G3 HTML 語法保護

G3 交給 builder、copywriter、repair、ops 或 register 前，要求其先讀 `/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md` 並宣告 `syntax-only`、`layout-only` 或 `content-change`。若 brief 說不改文字，只允許前兩者；所有內容節點必須留在 `.lesson-body`，不可用第一個 `</div>` 或全域正規表示式插入。G3 驗收需包含 parser 結構檢查、`validate-course-structure.py`（ancestor、body count、重複 id、第一個 section、CSS media query）、lint、content audit 與 `git diff`；wrapper outside 或非預期文字變更直接 BLOCK。之後對代表頁做 browser smoke：桌面 `1440px` 四個位置、手機 `390px` 與 `430px`，確認 content width、水平捲軸、sticky header、導覽與 localStorage scroll state。報告列出 RWD 尺寸、可見文字是否變更、尚未驗證項目與 commit/push 授權；沒有畫面證據就保持 `PENDING`。
