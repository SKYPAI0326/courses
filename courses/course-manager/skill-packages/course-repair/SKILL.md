---
name: course-repair
description: Use for reversible diagnosis and repair of an existing course while keeping its history separate from the new-course G0-G6 production flow.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# 既有課程修復

這個 skill 只處理已存在的課程。它保留原課程身分與既有交付歷史，依 `scan → plan → backup → fix → verify` 修復。問題分類與回送規則讀 [new-system-routing.json](references/new-system-routing.json)。

既有課程可以沿用 `course-validator` 的內容、忠實度、操作、獨立試學與發布證據格式；修復紀錄不冒充從 G0 開始完成過的新課 Gate 歷史。

## 先判斷是否仍是修復

發現下列任一情況，停止 repair 並建立新的 G0 contract：

- 重新定義主要學員或其起始能力。
- 重新定義課程要交付的核心成果或驗收方式。
- 重做整門課的能力架構、主序列或課程邊界。

局部更新來源、難度、解釋、練習、素材、介面、單元整合、存取或部署仍屬 repair。每個 finding 只有一個 owner Gate；需要重驗的層級可以有多個。

## 呼叫

```text
/course-repair <slug> scan
/course-repair <slug> plan
/course-repair <slug> backup
/course-repair <slug> fix
/course-repair <slug> verify
/course-repair <slug> report
/course-repair <slug> all
```

`scan` 與 `plan` 唯讀。第一次修改只能發生在 `fix`，而且 backup、restore proof 與核准的 plan 必須先存在。

## Scan

先讀專案指示、大綱、正式 lesson、學員 HTML、素材 manifest 與既有驗證紀錄。不要以檔名或 lint 結果推定品質。

實際找出：

- 學員入口、材料、第一個動作、預期結果、快速檢查或修復路徑是否中斷。
- 示範、引導練習與獨立練習是否只是改標籤或重做相同流程。
- 各單元是否帶來不同成果、判斷與產物依賴。
- 核心素材能否從學員路徑取得、開啟並理解用途。
- 平台、介面或來源是否已改變；不確定時保留未知並回 G1 驗證。
- HTML 是否遺失正式 lesson 的解釋、範例、表格、prompt、檢查與修復內容。

每個 finding 使用 routing policy 中的代碼，記錄位置、證據、owner Gate、影響範圍與建議下一步。

## Plan

在 `courses/{slug}/_repair/{date}/REPAIR-PLAN.md` 寫出精確範圍：會改哪些檔、解決哪個 finding、誰負責、如何驗證、哪些內容會合併或刪除。一次修唯一責任層，避免同一缺口同時在 lesson、HTML 與 validator 疊加補丁。

若計畫包含刪除、合併、成果改寫或會改變課程意義的動作，先讓使用者核准 plan。純確定性修復仍要保留計畫與回復證據。

## Backup

在第一次修改前：

1. 把計畫內每個目標依相對路徑複製到 `courses/{slug}/_backup/{date}-pre-repair/`。
2. 產生 `courses/{slug}/_tools/restore-{date}-pre-repair.sh`。
3. 記錄原始 SHA-256，執行 shell syntax check，並在隔離位置證明還原後雜湊相同。

任何一項缺失就停止，不進入 fix。

## Fix

依最早 owner Gate 修正根因：

- G1：重查外部來源與真實工具行為。
- G2：修單元順序、難度、依賴或評量架構。
- G3：由 course-designer 修正式 lesson 與可讀文案，再做 content review。
- G4：修素材、HTML 忠實度、介面、RWD 或無障礙，重做代表範圍試走。
- G5：修跨單元產物鏈、導覽與全課整合，重做 full-course trial。
- G6：由 course-ops 建立新的精確發布提案與授權；修復本身不發布。

每批只改計畫內少量檔案，保留自然完整的課程敘事。不要把正常段落改成名詞清單、待辦事項、內部編碼檔名或沒有前因後果的操作要求。

## Verify

先確認修改範圍與 plan 相同，再重跑 affected scope。內容改動至少重做 content；HTML 改動重做 fidelity、render 與 learner path；操作或成果改動重做獨立試學；跨單元改動重做 full-course trial；發布檔改動進入 G6 proposal。

驗證輸出沿用 `course-validator` 的 evidence format，記錄新檔案雜湊、實際執行者、動作、提示、卡點、完成品與結果。舊 hash 的 PASS 不得沿用。

`REPAIR-REPORT.md` 列出 changed files、finding、驗證結果、未解風險與 restore 路徑。只有計畫內問題已修復、必要實測通過且可回復時才能結案。

## 邊界

- 不修改未列入 plan 的檔案，不使用 `git add -A`。
- 不因 lint 綠燈、欄位齊全或文案變長而宣稱可用。
- 不讓 course-refresh 寫入 metadata；其報告只作重查線索。
- 不把 repair PASS 寫成新課 G0–G6 全歷史。
- 涉及正式發布、密碼、索引、部署或外部平台變更時，交 course-ops 取得新的 manifest 授權。
