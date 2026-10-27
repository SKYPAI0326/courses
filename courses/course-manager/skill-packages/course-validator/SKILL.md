---
name: course-validator
description: Use when validating a course before release, especially when static checks pass but actual pages, learner journeys, evidence manifests, or follow-home usability may still be weak.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# 課程驗證

這是內容、HTML 忠實度、實際操作、獨立試學與發布就緒度的唯一驗證入口。用正式正文、學員頁、素材與真實完成品判斷，不用作者摘要、欄位齊全或 lint 結果代替學習證據。通用格式檢查可在本機以 Python 標準函式庫執行；需要語意判斷或實際操作時，必須保留執行者與過程紀錄。

`$BASE = $COURSE_WEB_ROOT`；未明確設定時停止。

必讀 `$BASE/_規範/learner-action-contract.md`、`course-content-substance.md`、`../course-handout-designer/references/quality-gate.md`。資料格式與範例見 [evidence-format](references/evidence-format.md)。

## 呼叫

```bash
bash "$SKILLS_ROOT/course-validator/scripts/course-validator.sh" <slug> [preflight|all|status|report]
```

COURSE_WEB_ROOT 可指定專案根目錄以在隔離環境測試。`status` 唯讀；`all`／`report` 更新 `_validation/FINAL-REPORT.md` 與機器 manifest，保留語意與真人待驗項目。

- exit 0：本次機器檢查及已聲明證據未見確定性錯誤；實際狀態以報告為準，仍可能 PENDING_HUMAN。
- exit 1：核心檔案缺失、素材失效、證據過期、審查失敗或範圍不完整。
- exit 2：參數／格式錯誤；不解讀為通過。

既有 L0／L1-L3／L4a／L4b／L5 是 [資料與外部 consult 的可選專項](references/legacy-data-layers.md)，只在適用及已授權時執行，不能以該流程 OK／分數代替正式證據。

## 驗證層級

依序累積證據，不得用較低層級宣稱較高成熟度：

1. `STATIC_VALIDATED`：契約、來源、雜湊、結構與確定性規則已核對。
2. `EXECUTION_VALIDATED`：指定工具、頁面與素材已實際操作，結果可重現。
3. `INDEPENDENT_AI_VERIFIED`：未參與製作與驗證的 AI，在隔離情境中只看學員可見材料，完成指定範圍並交出可驗證成果。
4. `HUMAN_VERIFIED`：有明確真人參與者、觀察者、同意紀錄與 session 證據的實測已通過。

Gate 狀態與證據成熟度是兩件事。Gate 可在符合該階段必要證據後自動 PASS；`HUMAN_VERIFIED` 不能由作者、validator 或 AI 代填。

## 執行

1. 核對正式正文、單元清單、來源和素材。若尚無 evidence.json，腳本可掃描 HTML 並回報機器結果及缺件；補全格式前不能用作完整課程驗收。
2. 由 reviewer 閱讀內容，記 content；HTML 後記 fidelity。每筆引實際位置與紀錄檔，綁定來源、頁面與所用素材 hash。程式只驗格式、範圍和版本，不自動理解教學語意。
3. 依 quality-gate 分別做入口、完整跟做、理解、遷移、序列與適用平台實測。實際執行者、允許看到的材料、逐步動作、提示來源、卡點、修復、產物與驗收結果據實保存。作者自驗、獨立 AI、真人分別標記。
4. 執行相應 HTML lint 和必要程式／平台動作。腳本不能自行訪問外部帳號；沒有實測就保留待驗。
5. 修正後檢查所有受影響證據的版本；舊 hash 不沿用。綜合報告指向原始紀錄，不靠 status.jsonl 中任一 OK 就宣稱可交付。

## 獨立 AI 試學

G4 必須試走 `representative_unit`，G5 必須試走 `full_course`。試走 AI 必須使用新的隔離情境，且不能是任何課程作者、頁面製作者、reviewer 或 validator。

試走前只交付學員實際會取得的頁面與素材，並記錄各自 SHA-256。不得提供課程契約、研究摘要、作者備忘錄、教學設計稿、答案鍵、檢核規則或任何製作對話。執行過程寫入 `course-trial-record.schema.json` 對應紀錄，至少包含：

- canonical G0 requirements SHA-256、target profile、baseline／prerequisite 聲明、allowed tools／inputs 與 governed runner authority。
- 從哪個入口開始，以及是否看懂成果與找到材料。
- held-out task 的封閉結構 `changed_conditions`；data 數值、threshold 數值或 context constraint 必須讓 runtime 重算出不同 rule result 與 outcome。Action operation 要綁 typed input subject 與 condition rule，decision 要等於重算結果，observable 要以 typed output SHA-256 記錄 expected-vs-actual；自由文字或 domain-token padding 不成立。demonstration／guided-practice／answer-key／held-out 的 input/output bytes 全部不可重用。
- 依時間順序發生的具體動作、判斷與可觀察結果；每個 in-scope G0 child capability／G2 criterion 綁定真實 PASS action ID 與完成品 evidence ID。
- 每次提示的來源；來源只能是學員頁、學員素材或完全沒有提示。
- 卡點、失敗代碼、是否恢復，以及實際採用的修復動作。
- 完成品路徑、雜湊、完整性、可驗證性與驗收結果。

只有「製作證據＋通過的獨立試學紀錄」可以讓 G4 或 G5 PASS。沒有製作證據、完成品不完整、無法驗證、曾讀取內部材料或試走者與製作團隊重疊，一律 BLOCK。

AI 試走成熟度只能是 `INDEPENDENT_AI_VERIFIED`。AI 完成時間不能證明課程時數合理，也不能代替真人可讀性或目標學員獨立完成證據；`human_duration`、`human_readability`、`target_learner_independence` 保持 `PENDING_HUMAN`，直到另有符合 target profile 的真人證據。

## Accessibility evidence

G4/G5 必須安全消費符合 `course-accessibility-report.schema.json` 的實際 report 檔，並核對 pilot／production 宣告的 evidence ID、path、SHA-256、claim scope 與實檔完全一致。report 記 exact page IDs/paths、standard/version/level、applicable criteria、automated/manual checks、tools、user agents、assistive technology，以及 finding severity/status/resolution。

`basic_accessibility_smoke` 僅能聲明 keyboard、focus、reading-order、horizontal-overflow 的 basic smoke，四項須逐頁通過。每筆 check 要有 unique check ID 並綁單一 page、criterion、method。`wcag_2_2_aa` 必須涵蓋完整 governed page × WCAG 2.2 A/AA criterion Cartesian results；manual 與 automated 各自 exact 涵蓋全部頁面。任何 NOT_TESTED、FAIL 或 unresolved HIGH/SERIOUS/CRITICAL finding 都是 BLOCK。G4 只涵蓋 exact representative page；G5 必須 exact 涵蓋 entry、每一 learner unit page 與 completion。不得把 G4 或 basic smoke 推廣為全課 WCAG conformance，也不得只信 report 內的 PASS 字樣。

失敗回送依原因決定：來源或工具行為不符回 G1；順序或難度失衡回 G2；解釋或練習不足回 G3；介面、版面或單元素材問題回 G4；跨單元與全課整合回 G5；存取、部署或發布環境回 G6。修正後以新 hash 重做受影響範圍，不沿用舊試走結論。

## 責任回饋

內容、推理或練習缺失回 designer；呈現遺失回 builder；驗證規則未攔截的缺口由 validator 修正；規則本身衝突才修共通來源。缺素材由總籌指定實作者，不新增同義契約。`course-reviewer` 只保留相容入口，不持有第二套品質矩陣。

G3 驗證讀取正式 lesson record、正文與 editorial evidence，核對結構、來源 hash 及實際引用位置。validator 不得替作者發明缺少的情境、教學事實、示範答案、素材、操作步驟或修復方式；發現缺口就附路徑退回 course-designer，不能為了讓欄位齊全而改寫正文。

真人與平台驗證未完成時可以交付明確階段成果。只有符合 learner-action-contract.md 的全部適用證據才可回報 HUMAN_READY。

## HTML 結構保護驗收

驗收必讀 `$SKILLS_ROOT/course-html-contract/SKILL.md`；未設定 `SKILLS_ROOT` 時停止。validator 不改學員頁；除既有 lint、素材與證據外，必須執行共用結構檢查器，確認 `.lesson-section`、`.body-text`、`.step-list`、`.prac-box` 都是 `.lesson-body` 後代，且沒有內容節點在 hero 與 lesson-body 之間或 wrapper 外。

任何 outside／wrapper 斷裂、未配對標籤、syntax-only／layout-only 卻出現文字或 href 變更，都要保留為 BLOCK／PENDING，不得被 lint PASS 或作者摘要掩蓋。

驗收同時執行 `python3 "$SKILLS_ROOT/course-html-contract/scripts/validate-course-structure.py"`（需要 ancestor、body count、重複 id、第一個 section 與 CSS media query 檢查），再要求代表頁 browser smoke：`1440px` 桌面頂端／修改區塊／中段／底部，以及 `390px`、`430px` 手機。核對 content width、水平捲軸、sticky header、卡片／表格／程式碼區塊、導覽與 localStorage scroll state；清除舊 state 後重整。未完成項目只能標 `PENDING`／`BLOCK`，不可宣告 HUMAN_READY。
