# Gemini AI 課程完整度修復實作計畫

> **執行方式：** 使用 `superpowers:executing-plans`，由目前執行者在本課目錄逐項完成；不派遣代理，不提交或推送。

**Goal:** 讓零基礎學員看得見完整課程地圖，沿核心實作路徑從工作需求、提示詞與生成工具走到查核、修復、保存和獨立交付，同時保留並定位原有 40 個單元。

**Architecture:** `_source/fragments/*.fragment` 是 10 個核心單元的正式內容來源；`_source/CURRICULUM-MAP.md` 描述全部 40 個單元；`_source/lesson-map.json` 保持 10 站核心渲染／導覽 manifest；既有 40 個單元 HTML 保留原始正文。先盤點與備份，再修來源和導覽、轉製核心頁、更新完整目錄，最後跑內容、結構、連結與版面驗證。

**Tech Stack:** Markdown、JSON、HTML/CSS/JavaScript、Python 標準函式庫、課程 lint／substance／structure validator、瀏覽器 smoke。

**Spec:** `_repair/2026-10-06/RE-REVIEW-DESIGN.md`

## Global Constraints

- 僅修改 `courses/gemini-ai`；不碰全站搜尋索引或其他課程。
- 原有 40 個單元正文全部保留；沒有明確核准，不刪除、合併或把原文改寫成摘要。
- 10 個核心單元以 fragments 為正式來源；轉製後比對內容，不直接另造競爭正文。
- HTML 使用 parser 定位節點，所有課程內容維持在既有 `.lesson-body` 後代；保留頁面殼層、互動與有效連結。
- 6 小時、真人學員完成、AI Studio 帳號內模型呼叫皆未經本次靜態編修驗證；保持 `PENDING`。
- 每次改正式頁前完成本次範圍備份及 restore script；不提交、不 push、不部署。

## Review Focus

1. **首頁仍藏住大部分原課：** 測首頁初始狀態能直接看到核心路徑及完整六部目錄，全部 40 個單元都有可用入口。
2. **核心路徑漏掉舊課目標：** 用 40 單元對照矩陣檢查每個原有成果落在核心、延伸或參考位置，且分流理由明確。
3. **提示詞只是長文字複製區：** 抽查 CH1-2、CH1-3 和一個完整案例，確認學員能解釋提示詞段落、修改條件、預測變化並核對輸出。
4. **原始內容再次被預設收合：** 自動檢查首頁目錄與課程頁原文區塊的初始可見狀態；頁面中不以封閉的 legacy detail 作唯一內容入口。
5. **結構／source fidelity／手機版回歸：** 全部 HTML 跑結構與 lint；抽查更新後 HTML 含來源 fragment 的正式內容；於 1440px、390px、430px 檢查寬度、導覽、表格和水平溢出。

---

### Task 1: 建立本輪基準與完整單元盤點

**Files:**
- Create: `_repair/2026-10-06/re-review/SCAN.md`
- Read: `index.html`, `part1/`–`part6/`, `_source/OUTLINE.md`, `_source/LESSON-PLANS.md`, `_source/lesson-map.json`, `_source/fragments/`

- [x] **Step 1: 記錄首頁與單元的數量、標題、原始正文容器及目前收合狀態。** 使用 Python `html.parser` 讀取首頁目錄與 40 個 lesson HTML，記錄每頁 title、`details#legacy-reference` 是否存在／是否有 `open`、核心片段標記、外部素材連結及上一頁／下一頁連結。
- [x] **Step 2: 把現有 40 頁與修訂主線逐項對照。** 為每頁填入原始學習用途、目前首頁標記、建議角色（核心／前置橋接／延伸實作／參考）、前置能力、工作產物或判斷、重複或缺漏；不以檔名推定教學功能。
- [x] **Step 3: 對 10 個核心 fragment 做內容缺口檢查。** 對照 learner-action contract 的起始材料、成果、第一步、結果、示範、操作、檢查、修復與再用欄位；另標示提示詞只提供成品、沒有解說的段落。
- [x] **Step 4: 保存可重現基準。** 將 41 份 HTML、10 個核心 fragments、`OUTLINE.md`、`LESSON-PLANS.md`、`lesson-map.json`、`assets/materials/README.md` 的相對路徑與 SHA-256 寫入 `baseline.json`；在 `SCAN.md` 列出未測平台／真人項目。
- [x] **Step 5: 對照既有掃描與新基準。** 保留既有 `_repair/2026-10-06/` 文件，不覆寫舊 SCAN 或舊 hash；有差異時在本輪 SCAN 說明。

### Task 2: 建立本輪備份與還原腳本

**Files:**
- Create: `_backup/2026-10-06-re-review/`（保留相對路徑）
- Create: `_backup/2026-10-06-re-review/manifest.json`
- Create: `_tools/restore-2026-10-06-re-review.sh`
- Create: `_repair/2026-10-06/re-review/RESTORE-TEST.md`

- [x] **Step 1: 從 Task 1 的 manifest 清單複製所有預計修改的 HTML、fragment、課程地圖與素材說明。** 備份覆蓋首頁、40 個 lesson HTML、10 個核心 fragments、`OUTLINE.md`、`LESSON-PLANS.md`、`lesson-map.json`、`README.md`，以及可能同步調整的提示詞素材。列入清單的 `lesson-map.json` 只備份、不修改；其他無關 CSV／JSON、repair evidence 與工具參考 HTML 不複製、不改寫。將可能同步調整的 `assets/materials/prompt-timer.txt`、`prompt-budget.txt`、`prompt-meeting.txt` 一併備份。
- [x] **Step 2: 建立備份 manifest。** 每個檔案記錄相對路徑、SHA-256 與 byte size；再次計算來源 hash，逐項確認與備份相同。
- [x] **Step 3: 建立 restore script。** 腳本先驗證 manifest 的備份 hash 全數正確，再將列明檔案複製回課程根目錄；拒絕空 manifest、絕對路徑、`..` 路徑或備份外來源。
- [x] **Step 4: 驗證腳本語法並做隔離還原測試。** 執行 `bash -n _tools/restore-2026-10-06-re-review.sh`。把測試用 restore script、manifest 與備份複製到 `/private/tmp` 下的隔離課程副本；改動副本中的首頁，對副本執行還原，再以 manifest 核對 SHA-256；不在正式課程目錄測試回滾。
- [x] **Step 5: 將還原命令與結果記到 RESTORE-TEST.md。** 未通過前停止內容修改。

### Task 3: 建立可追溯的完整課程地圖

**Files:**
- Create: `_source/CURRICULUM-MAP.md`
- Modify: `_source/OUTLINE.md`
- Modify: `_source/LESSON-PLANS.md`
- Keep: `_source/lesson-map.json` as the 10-item core route manifest

- [x] **Step 1: 以 40 個既有頁面為逐列基礎建立 CURRICULUM-MAP.md。** 每列寫頁面、原標題、原有內容用途、能力前置、核心／延伸／參考分類、工作輸出或判斷，以及入口連結；原目標沒有實作證據時標 `CONTENT GAP`，不得標成已涵蓋。
- [x] **Step 2: 檢查核心分流與原頁面正確性。** 核心保留工作上可重用的需求拆解、提示詞、預算、KPI、生成式 AI 語意判讀、保存與獨立交付。排會、圖表、報告、prompt library、自由演練及發布逐項依材料完整度、能力前置與工作成果分類，不為 6 小時假設強塞進核心。遇到日期／時區、費用、API 金鑰、模型輸出或部署等易變技術承諾，先查對應官方來源；能確認錯誤才列文字修正，其餘標明版本與 `PENDING`，不猜測。
- [x] **Step 3: 寫明課程進程和跨 Part 轉場。** 說明 Part 1 需求／提示詞與首次生成、Part 2 規則和計算、Part 3 資料與視覺判讀、Part 6 語意 AI 實作、Part 4 保存／交付，以及 Part 5 分流實作的先修關係；若按學習依賴跳過原 Part 編號，首頁同步解釋原因。
- [x] **Step 4: 將 10 站修訂為可追溯的核心序列。** 每站寫前一站產物、本次能力增量、完成物與驗收；說明其餘 30 頁如何延伸或補足原目標，不聲稱 10 站等於涵蓋全部 40 頁。
- [x] **Step 5: 對照 JSON 與教案。** `lesson-map.json` 保持正好 10 個核心頁並與核心路線一致；`CURRICULUM-MAP.md` 涵蓋正好 40 個 lesson HTML；`LESSON-PLANS.md` 中提示詞教學與平台實跑狀態不超出現有證據。
- [x] **Step 6: 檢查完整性。** 以 Python 比較課程地圖、首頁單元 href 和實際 40 個 HTML 路徑；任何缺頁、重複頁或失效連結都先修正再進下一步。

### Task 4: 教會學員形成、修改和查核提示詞

**Files:**
- Modify: `_source/fragments/part1-CH1-2.fragment`
- Modify: `_source/fragments/part1-CH1-3.fragment`
- Modify: `_source/fragments/part2-PRAC2-1.fragment`
- Modify: `_source/fragments/part6-CH6-1.fragment`
- Modify: `_source/fragments/part6-PRAC6-1.fragment`
- Modify: `assets/materials/prompt-timer.txt`, `prompt-budget.txt`, `prompt-meeting.txt` only if their copied text must be kept synchronized with the fragment
- Test: `part1/CH1-2.html`, `part1/CH1-3.html`, `part2/PRAC2-1.html`, `part6/PRAC6-1.html`

- [x] **Step 1: In CH1-2, show one incomplete timer request and explain why it fails.** Use the existing timer task; identify missing input, behavior rule, exception, output and test. Do not create a new fictional work case.
- [x] **Step 2: Build the request into an annotated prompt.** Label the actual sentence for context/task, input, rules, exceptions, output format and acceptance test. Explain each label in plain Traditional Chinese immediately before the learner uses it.
- [x] **Step 3: In CH1-3, connect the prompt to generation and iteration.** Point to the exact prompt file and inline copy block; tell the learner which one clause to change, what behavior should change, what should remain unchanged, and which tests to rerun. Any sample model output is marked as an expected/reference example unless accompanied by actual run evidence.
- [x] **Step 4: Add one purposeful prompt-reading checkpoint to budget and meeting work.** Learners explain what the constraint/exception clause prevents, predict the result for provided data, then compare with the generated result; retain full copyable prompts and do not split copies into contradictory versions.
- [x] **Step 5: Reconcile prompt files with inline canonical prompts.** Compare normalized text and preserve one canonical prompt per task; all downloads, copy buttons and named links must point to that version.
- [x] **Step 6: Run the prompt-literacy evidence check.** A reader must be able to identify prompt parts, modify one real condition, state the expected effect, run known-answer tests and find a repair path. If a platform or model call has not run, record it as pending rather than replacing it with a fabricated output.

### Task 5: Repair all 10 core lessons against the teaching evidence chain

**Files:**
- Inspect and modify only fragments that fail the content matrix: `_source/fragments/part1-CH1-1.fragment`, `part1-CH1-2.fragment`, `part1-CH1-3.fragment`, `part2-CH2-1.fragment`, `part2-PRAC2-1.fragment`, `part3-PRAC3-3.fragment`, `part4-CH4-1.fragment`, `part4-PRAC4-3.fragment`, `part6-CH6-1.fragment`, `part6-PRAC6-1.fragment`
- Render: the 10 corresponding core lesson HTML using parser-context edits; do not run `_tools/build-lessons.py` because it regenerates sources/materials rather than HTML
- Modify: `_source/OUTLINE.md`, `_source/LESSON-PLANS.md`, `_source/lesson-map.json` when a verified source fact or title changes

- [x] **Step 1: Review each core page from the learner-content fragment, not its hidden author notes.** Record current evidence and exact missing span in `SCAN.md` for situation, reason, required concept, worked input, reasoning, intermediate result, artifact, learner action, checkpoint, recovery, transfer and next-page bridge.
- [x] **Step 2: Patch only confirmed gaps in each fragment.** Every added paragraph must explain a concrete concept or connect a prior result to the next action; every operational item must identify action, visible result, check and recovery. Preserve valid formulas, data, prompts, instructions and existing answer keys.
- [x] **Step 3: Check Demo/Together/Solo roles.** For each activity record material, artifact, learner decision, new cognitive work and support level in CURRICULUM-MAP.md; merge no content in this pass, but mark exact duplicate candidates for later review.
- [x] **Step 4: Render only the 10 core pages.** Use a parser-context replacement of the existing formal core section from its fragment, retaining each page wrapper, navigation, metadata, and original body; assert the target is unique and the DOM parent chain is unchanged. Do not run `_tools/build-lessons.py`, which overwrites authoring sources/materials and does not render learner HTML.
- [x] **Step 5: Compare fragment and rendered learner text.** Confirm every new concept, prompt annotation, answer, operation and recovery appears in its HTML in the same sequence, inside the existing `.lesson-body`; no fragment is silently truncated.
- [x] **Step 6: Run targeted substance and structure checks before expanding to all pages.** Execute course substance audit and HTML structure validator on each changed page; fix any wrapper, duplicate-id, missing-asset or evidence-chain defect before continuing.

### Task 6: Restore full-course discoverability and clarify the learner routes

**Files:**
- Modify: `index.html`
- Modify: `part1/`–`part6/` lesson HTML for original-content visibility and course-route links; retain all 40 originals
- Modify: `_source/OUTLINE.md`, `_source/lesson-map.json` if route labels or prerequisites change

- [x] **Step 1: Replace the collapsed catalog presentation.** Make the full six-part course catalog visible from the initial index view, with each unit classified from CURRICULUM-MAP.md. Keep the 10-station outcome checklist as a separate core route and state that it is not the full 40-unit catalog.
- [x] **Step 2: Remove hidden-only access to the original lesson bodies.** In core and extension pages, ensure the original instructional body is reachable from a visible, descriptive section/link at first load; no unit may exist only inside a closed `details#legacy-reference`. Preserve all original content except exact, source-backed technical corrections recorded in `technical-corrections.json`.
- [x] **Step 3: Add learner-facing bridges around the non-numeric core route.** Explain why the core path moves from Part 3 to Part 6 and then Part 4; add links to the relevant extension units rather than implying those pages were completed.
- [x] **Step 4: Align unit labels, verified claims and page navigation.** Check each course card title, unit role, previous/next link and return-to-map link against the curriculum map; extension pages link back to their nearest core prerequisite and describe when to use the extension. Repair only technical statements explicitly listed in CURRICULUM-MAP.md and supported by an official source; otherwise preserve the original text and mark that guidance pending review.
- [x] **Step 5: Use HTML parser edits and preserve DOM contracts.** Before each batch record target element and parent chain; after edits assert unique IDs, one `.lesson-body`, all lesson sections under that body, and valid hero/body/nav/footer order.
- [x] **Step 6: Verify all source originals remain unchanged except listed corrections.** Compare backed-up original-body text snapshots with post-edit text for all 40 lessons; differences are allowed only for exact navigation/visibility changes or individually logged, source-supported corrections from Step 4. Preserve every other original sentence and example.

### Task 7: Run full technical and learner-path verification; report limits

**Files:**
- Create or update: `_repair/2026-10-06/re-review/VERIFICATION.md`
- Create: `_repair/2026-10-06/re-review/REPAIR-REPORT.md`
- Update: `_validation/FINAL-REPORT.md` and evidence manifests only with fresh hashes and actual results

- [x] **Step 1: Run complete-page syntax and link checks.** Structure validator checked 45 pages with 0 blocked. Lint scanned 45 pages with 0 blocker/error and 82 non-blocking warnings (40 missing `data-built-at`, 40 legacy font-token notices, 2 motion notices).
- [x] **Step 2: Run content and source checks.** All 10 core pages passed substance checks with 0 blocks and 0 missing assets; continuity checks reported 0 warnings and require human learner review. The author cold-read the learner-facing sequence and recorded it as `author-self-check`, not `LEARNER_READ`.
- [x] **Step 3: Validate links and inventory.** Static audit found 0 broken local links/fragments, all 40 catalog entries resolve, the 10-station route is complete, all 10 core fragments match rendered text and links, the materials ZIP matches source files, and all original lesson body text reverses to its baseline after the exact source-backed allowlist is reversed.
- [x] **Step 4: Re-run source-to-HTML fidelity and evidence freshness.** `verify-static.py` wrote fresh page hashes and fidelity results; browser results and screenshots were regenerated after the CH6-2 privacy edit. Fresh checksums are in `_repair/2026-10-06/re-review/re-review-evidence.json`.
- [x] **Step 5: Run representative browser smoke.** 11 browser checks passed with 80 viewport/position observations at 1440px, 390px and 430px; no horizontal overflow or page errors. CH6-2's changed Publish guidance was inspected at desktop and both phone widths. Screenshots are under `_repair/2026-10-06/evidence/`.
- [x] **Step 6: Perform author-only cold read without teacher notes.** Followed the 10-page learner route and listed assets. No critical prerequisite break was found; account/UI variability and unmeasured lesson duration remain open. Status is `author-self-check`, not `LEARNER_READ`.
- [x] **Step 7: Preserve external validation as pending.** No AI Studio model run, human completion, transfer or 6-hour duration is claimed. Final status remains `MACHINE_READY_PENDING_HUMAN`.
- [x] **Step 8: Write the report.** Results and limitations are in `VERIFICATION.md`, `REPAIR-REPORT.md`, and `_validation/FINAL-REPORT.md`; restore command is documented. Course implementation was left uncommitted until the user separately authorized pushing.

## Execution Decision

The user selected direct execution with “執行”; Tasks 1–7 are complete. The implementation is `MACHINE_READY_PENDING_HUMAN`; learner and platform evidence remain pending as documented above. The verified local backup is ignored by the repository and can restore this working copy.
