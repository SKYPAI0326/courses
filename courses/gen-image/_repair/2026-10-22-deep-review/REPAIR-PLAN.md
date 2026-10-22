# Gen Image Deep Review Repair Plan

> **執行方式：** 單一主代理、原地修復；不派遣新 agent、不 commit、不 push、不發布。

**Goal:** 修復 Deep Review Judge 接受的 8 項問題，使既有課程承諾、離線路徑、交件保存、來源、資產證據、導覽與機器證據重新一致。

**Architecture:** 保留既有課程能力架構與 41 頁版面。內容根因由正式 lesson 與 HTML 同步修復；共用交件保存行為集中在一個小型 learner-facing JS；離線 PRAC4 重用已存在且已列入課程資產的三張品牌系列圖；所有證據以修復後新 hash 重建。

**Tech stack:** HTML/CSS/vanilla JavaScript、Markdown、Python 標準函式庫驗證腳本、現有 course-validator 與瀏覽器 smoke test。

**Spec:** `/private/tmp/deep-review-gen-image-20261022-1832/pilot-record.yaml`

## Global constraints

- 任務範圍是 `content-change + interface repair`；只改本計畫列出的檔案。
- 保留 `.lesson-body`、主要 wrapper、DOM 順序責任與現行冷色調設計。
- 不新增第三方依賴，不修改 workshop、備份或 legacy 圖片。
- 不降低大綱既有 capstone 成果；CH5-1 必須補齊 A→L2→B/C→局部修改→QA→release gate 與三張系列交付。
- 真人、第三方平台與獨立試學證據保持 PENDING；不由作者代填。
- 使用者已要求直接執行；本計畫採 native 單代理，不新增派遣。

## Review focus

- 平台完全不可用時，PRAC4 是否仍能以實際三張系列完成相同驗收。
- learner output 重整後是否保存，並能下載成可帶入下一單元的紀錄。
- CH5-1 的必要交件是否與 outline、Module 5 和正式 source 完全一致。
- source-first 重建是否會重新帶回真實目的地與未驗證日期。
- 所有新驗證紀錄是否真的綁定修復後 hash，而不是只更新 hash 宣告。

## Finding ownership

| Finding | Owner Gate | Root cause | Repair |
|---|---|---|---|
| B-01 | G5 full_course_integration | CH5-1 後期被縮成單張體驗，但 outline／module 承諾未同步 | 補齊 capstone 必要產物、步驟與 rubric，不降低承諾 |
| B-02 | G4 asset_missing | offline workbook 未提供 PRAC4 對應三張系列 | 用 v16/v17/v18 建立可執行 PRAC4 離線段落 |
| B-03 | G4 interface_block | contenteditable 只有畫面輸入，沒有保存／匯出 | 新增共用 localStorage 保存、複製與 JSON 下載 |
| A-01/B-04 | G5 validation | 10/16 evidence 早於後續修復 | 修復後重建 technical/content/fidelity evidence 與 validator manifest |
| A-02 | G1 source_mismatch | 10/17 HTML 語意修正未回寫 lesson | 同步 CH5-1 虛構旅遊案例與 capstone 正文 |
| A-03 | G4 asset_missing | v64 在 manifest/provenance 凍結後加入 | 登錄 v64；保留未使用 v63 並明示狀態 |
| A-04 | G4 interface_block | 靜態 raw Markdown 不支援 heading fragment | 移除 `.md#fragment`，連結文字保留可搜尋段名 |
| A-05 | G5 navigation | index 只連 lesson，沒有 module1–5 入口 | 在各 module 標題加入「模組總覽」連結 |

### Task 1: Backup and restore proof

**Files:**
- Create: `_backup/2026-10-22-pre-deep-review-repair/**`
- Create: `_tools/restore-2026-10-22-pre-deep-review-repair.sh`
- Create: `_repair/2026-10-22-deep-review/BACKUP-SHA256.txt`

- [x] 備份本計畫所有既有目標檔案並記錄 SHA-256。
- [x] 執行 restore script syntax check。
- [x] 在隔離目錄執行 restore proof，要求所有 hash 相同。

### Task 2: Add failing regression checks

**Files:**
- Create: `_tools/test-deep-review-repair.py`

- [x] 建立行為契約檢查：capstone 一致性、PRAC4 offline trio、交件保存 UI、source/HTML 語意、v64 provenance、零 Markdown fragment、41/41 可達、evidence hash freshness。
- [x] 執行並確認在修復前因上述缺口失敗。

### Task 3: Repair capstone and source fidelity

**Files:**
- Modify: `../../_lessons/gen-image/CH5-1.md`
- Modify: `CH5-1.html`
- Modify: `module5.html` only if exact wording needs fidelity alignment

- [x] 將 CH5-1 必交改為完整三張系列交付鏈，保留 release STOP 規則。
- [x] 將正式 source 的案例 D 同步為虛構「島嶼慢旅」、合成地景與教學佔位。
- [x] 逐段核對 source→HTML 的新 capstone 與案例 D。

### Task 4: Repair PRAC4 offline recovery

**Files:**
- Modify: `assets/downloads/offline-candidate-workbook.md`
- Modify: `PRAC4.html`
- Modify: `../../_lessons/gen-image/PRAC4.md`

- [x] 加入 OFFLINE-PRAC4 三張系列（v16/v17/v18）與同 DNA／同骨架／單一變因驗收步驟。
- [x] 將 PRAC4 fallback 指向可搜尋的 workbook 段名。

### Task 5: Persist and export learner records

**Files:**
- Create: `assets/learner-record.js`
- Modify: `PRAC2.html`, `PRAC3.html`, `PRAC4.html`, `CH5-1.html`
- Modify: `../../_lessons/gen-image/PRAC2.md`, `PRAC3.md`, `PRAC4.md`, `CH5-1.md`

- [x] 每頁以 pathname + 欄位 index 保存 contenteditable 內容。
- [x] 提供「複製交件紀錄」與「下載 JSON」按鈕，檔名含單元 ID。
- [x] 頁面文字明示跨頁／跨裝置前先下載備份。
- [x] 瀏覽器 RED→GREEN：輸入唯一字串、重整仍存在、下載檔包含該字串。

### Task 6: Repair asset evidence

**Files:**
- Modify: `_repair/2026-10-17-image-refresh/IMAGE-MANIFEST.tsv`
- Modify: `_repair/2026-10-17-image-refresh/ASSET-PROVENANCE.tsv`
- Modify: `_repair/2026-10-17-image-refresh/IMAGE-PROMPT-SET.md`

- [x] 登錄 v64 的用途、生成方式、修改說明與 checksum。
- [x] 把 v63 明示為未引用的已製作候選，不刪除檔案。
- [x] 重跑 `_tools/verify-image-refresh.py`。

### Task 7: Repair links and navigation

**Files:**
- Modify: `index.html`
- Modify: 目前含 `.md#fragment` 的 8 個核心 HTML（由 regression test 精確列出）

- [x] 移除 Markdown fragment，保留可搜尋的段落名稱。
- [x] 在 M1–M5 區塊加入 module landing page 入口。
- [x] 入口 crawl 必須達到 41/41。

### Task 8: Rebuild evidence and verify

**Files:**
- Modify: `_tools/build-validation-evidence.py`
- Create: `_validation/deep-review-repair-self-check.md`
- Modify/regenerate: `_validation/evidence.json`, `_validation/validation-result.json`, `_validation/L5-evidence-manifest.json`, `_validation/FINAL-REPORT.md`, `_validation/fidelity-review.md`, `_validation/machine-checks.md`
- Create: `_repair/2026-10-22-deep-review/REPAIR-REPORT.md`

- [x] 將修復後 content/fidelity 紀錄如實標為 author-self-check，不冒充 independent-ai。
- [x] 跑 regression、image verifier、HTML structure、lint、substance audit、local links、`git diff --check`。
- [x] 在 1440／820／430／390 驗證代表頁與交件保存／下載行為。
- [x] 重建 current hash evidence；舊 hash 不沿用。
- [x] 報告 changed files、檢查結果、未驗風險與 restore 路徑。

## Self-review

- Spec coverage：8 項 accepted findings 全部有唯一 owner 與對應 task。
- Scope：沒有 workshop、發布、Git staging、額外平台研究或真人證據。
- Recovery：所有既有目標先備份；新檔由 restore script 移除。
- Completion boundary：若結構、browser、hash 或 restore 任一失敗，維持 BLOCK，不宣告完成。
