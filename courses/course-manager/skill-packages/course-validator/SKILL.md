---
name: course-validator
description: Use when validating a course before release, especially when static checks pass but actual pages, learner journeys, evidence manifests, or follow-home usability may still be weak.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# 課程驗證

用實際正式正文、HTML 與素材驗證，而非作者摘要。通用流程可在本機以 Python 標準函式庫執行；不依賴外部模型、資料集或代理。

`$BASE = /Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁`

必讀 `$BASE/_規範/learner-action-contract.md`、`course-content-substance.md`、`../course-handout-designer/references/quality-gate.md`。資料格式與範例見 [evidence-format](references/evidence-format.md)。

## 呼叫

```bash
bash /Users/paichenwei/.agents/skills/course-validator/scripts/course-validator.sh <slug> [preflight|all|status|report]
```

COURSE_WEB_ROOT 可指定專案根目錄以在隔離環境測試。`status` 唯讀；`all`／`report` 更新 `_validation/FINAL-REPORT.md` 與機器 manifest，保留語意與真人待驗項目。

- exit 0：本次機器檢查及已聲明證據未見確定性錯誤；實際狀態以報告為準，仍可能 PENDING_HUMAN。
- exit 1：核心檔案缺失、素材失效、證據過期、審查失敗或範圍不完整。
- exit 2：參數／格式錯誤；不解讀為通過。

既有 L0／L1-L3／L4a／L4b／L5 是 [資料與外部 consult 的可選專項](references/legacy-data-layers.md)，只在適用及已授權時執行，不能以該流程 OK／分數代替正式證據。

## 執行

1. 核對正式正文、單元清單、來源和素材。若尚無 evidence.json，腳本可掃描 HTML 並回報機器結果及缺件；補全格式前不能用作完整課程驗收。
2. 由 reviewer 閱讀內容，記 content；HTML 後記 fidelity。每筆引實際位置與紀錄檔，綁定來源、頁面與所用素材 hash。程式只驗格式、範圍和版本，不自動理解教學語意。
3. 依 quality-gate 分別做入口、完整跟做、理解、遷移、序列與適用平台實測。實際執行者、提示、卡點及產物據實保存。作者自驗、獨立 AI、真人分別標記。
4. 執行相應 HTML lint 和必要程式／平台動作。腳本不能自行訪問外部帳號；沒有實測就保留待驗。
5. 修正後檢查所有受影響證據的版本；舊 hash 不沿用。綜合報告指向原始紀錄，不靠 status.jsonl 中任一 OK 就宣稱可交付。

## 責任回饋

內容、推理或練習缺失回 designer；呈現遺失回 builder；未攔截的缺口回 reviewer；規則本身衝突才修共通來源。缺素材由總籌指定實作者，不新增同義契約。

G3 驗證讀取正式 lesson record、正文與 editorial evidence，核對結構、來源 hash 及實際引用位置。validator 不得替作者發明缺少的情境、教學事實、示範答案、素材、操作步驟或修復方式；發現缺口就附路徑退回 course-designer，不能為了讓欄位齊全而改寫正文。

真人與平台驗證未完成時可以交付明確階段成果。只有符合 learner-action-contract.md 的全部適用證據才可回報 HUMAN_READY。

## HTML 結構保護驗收

驗收必讀 `/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md`。validator 不改學員頁；除既有 lint、素材與證據外，必須執行共用結構檢查器，確認 `.lesson-section`、`.body-text`、`.step-list`、`.prac-box` 都是 `.lesson-body` 後代，且沒有內容節點在 hero 與 lesson-body 之間或 wrapper 外。

任何 outside／wrapper 斷裂、未配對標籤、syntax-only／layout-only 卻出現文字或 href 變更，都要保留為 BLOCK／PENDING，不得被 lint PASS 或作者摘要掩蓋。

驗收同時執行 `python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py`（需要 ancestor、body count、重複 id、第一個 section 與 CSS media query 檢查），再要求代表頁 browser smoke：`1440px` 桌面頂端／修改區塊／中段／底部，以及 `390px`、`430px` 手機。核對 content width、水平捲軸、sticky header、卡片／表格／程式碼區塊、導覽與 localStorage scroll state；清除舊 state 後重整。未完成項目只能標 `PENDING`／`BLOCK`，不可宣告 HUMAN_READY。
