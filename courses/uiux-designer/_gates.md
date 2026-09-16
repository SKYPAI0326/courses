# _gates.md — uiux-designer 品質檢核存證

> 一門課一份、append-only。每個 Gate 結束時追加問答、證據與決定；不刪除舊條目。

**課程 slug**：uiux-designer  
**負責人**：課程製作流程  
**建立**：2026-09-07  
**目前 Gate**：G1 大綱定位草稿  
**目前狀態**：`G1_BLOCKED_BY_FIGMA_VALIDATION`

---

## G0 正式範圍確認（課綱圖片 → coverage matrix）

**日期**：2026-09-07  
**證據**：

- `/Users/paichenwei/Downloads/1788509783989.jpg`
- `/Users/paichenwei/Downloads/1788509797593.jpg`
- `uiux-designer/_design/99h-coverage-matrix.md`
- `uiux-designer/_design/BASELINE-STATUS.md`

### 已確認

- □ 42h「介面元素與設計」12 個正式項目全部列入 coverage。
- □ 57h「UI/UX 原型製作與資料打包」9 組正式主題全部列入 coverage。
- □ 42h／57h／99h 總時數邊界已固定。
- □ 舊「Photoshop 42h＋UI/UX 57h」只保留歷史，不控制新範圍。
- □ Component、手機介面、Dialog、Navigation、Photoshop 輸出與網頁已標示首次教學／後續重用邊界。

### 使用者決策

- **Git/GitHub**：必要流程，納入 57h 的版本與交付驗收；不擴張成獨立 Git 課程。
- **基礎 JavaScript**：維持最小路徑，只教完成網頁成果所需的能力；不擴張成程式設計課。
- **16-stage**：作為依賴參考；依正式課程內容、能力邊界與完成物切分，不硬性一對一切成 16 個單元。

**結論**：`PASS`  
**放行範圍**：建立 Gate 1 的 outline 草稿與 99h 時間帳本。  
**禁止事項**：尚未通過 Gate 1 前，不建立教案、講義或 HTML。

---

## G1 大綱定位（PM → 設計師放行）

**日期**：2026-09-07  
**狀態**：`DRAFT_GATE1_REVIEW`  
**證據**：

- `_outlines/uiux-designer.md`
- `uiux-designer/_design/99h-time-ledger.md`
- `uiux-designer/_design/99h-coverage-matrix.md`

**目前草稿決策**：

- Part A：8 個內容單元，42h，負責介面元素與設計。
- Part B：8 個內容單元，57h，負責原型、互動、測試、資料打包、網頁、Git/GitHub 與部署。
- B6「Prototype 任務測試與修正」是支撐「原型應用」的教學活動，不另宣稱第三門行政課程。
- B8 的 JavaScript 僅為最小網頁路徑；Git/GitHub 為必要交付流程。

### 必須由使用者確認的 G1 問題

- Q1：16 個候選單元中，哪一個最需要再縮小或拆開？為什麼？
- Q2：接近零基礎學員是否能在同一條路徑中完成介面設計、Prototype、Handoff、Git/GitHub 與部署？哪一段風險最高？
- Q3：六項學習成果中，哪一項仍需要更具體的驗收證據？
- Q4：是否接受「依正式內容切分，不硬性切 16-stage；每單元以一份可驗收完成物為邊界」作為本課的單元原則？

**結論**：□ 放行 / □ 退回（等待使用者回答 Q1–Q4）  
**放行限制**：G1 未通過前，不進入代表單元教案。

### Figma 實務環境追加確認

**日期**：2026-09-07
**使用者確認**：Figma Starter 免費方案、瀏覽器版。
**證據**：`uiux-designer/_design/FIGMA-STARTER-BROWSER-AUDIT.md`

**決定**：`BLOCKED`
**原因**：目前只有方案與平台資訊，尚無三組最小實測的操作、失敗與成品證據；99h 時數、16-stage 對應與任何付費功能都不得視為已放行。

**下一步**：先完成 Probe A／B／C；再依 `PASS`、`CONDITIONAL`、`BLOCK`、`NOT_RUN` 重畫 coverage、時間帳本與單元邊界。

### Codex-first 自主執行授權

**日期**：2026-09-16

**使用者決策**：第一階段由 Codex 統籌 Skills、檔案製作、Computer Use、跨平台測試與自動修補；真人人工驗證延後到機器可交付版本完成後。

**執行狀態**：`MACHINE_PHASE_AUTHORIZED`

**判定邊界**：Codex 可標記 `SIMULATED_PASS`、`MACHINE_PASS`、`MACHINE_READY_PENDING_HUMAN`；不得自行標記真人 `HUMAN_PASS`。外部分享、公開發布、刪除與不可逆帳號設定仍需在動作前確認。

**證據位置**：`uiux-designer/_validation/autonomous-run/`

### Figma Probe A 第一輪結果

**日期**：2026-09-16  
**狀態**：`CONDITIONAL`  
**實際環境**：Chrome → Figma Starter／Free → `Codex Figma Starter Audit - Probe A`  
**證據**：`uiux-designer/_validation/figma-starter-browser/PROBE-A.md`

已通過 Frame、Auto Layout、Component、Variant、Instance、長中文換行與基本按鈕／錯誤輔助列結構。Variant 命名與直接編輯文字各發現一個可重現的失敗／修復路徑，已寫入紀錄。Form、List 的多列行為及 Probe B／C 尚未完成，因此 G1 仍維持 `G1_BLOCKED_BY_FIGMA_VALIDATION`。

### Figma Probe B 第一輪結果

**日期**：2026-09-16  
**狀態**：`CONDITIONAL`  
**證據**：`uiux-designer/_validation/figma-starter-browser/PROBE-B.md`

Starter 可完成單一 `On click → Open overlay`，Chrome Preview 已看到 `確認完成` Overlay。第二個 action 會出現方案限制；`Navigate to` 的 `Smart animate` 與 Vertical overflow 選項已在實際面板確認。免費主線需改為「一檔一核心互動」或拆檔，不能宣稱完整多步驟原型已通過。

### Figma Probe C 第一輪結果

**日期**：2026-09-16  
**狀態**：`CONDITIONAL`  
**證據**：`uiux-designer/_validation/figma-starter-browser/PROBE-C.md`

PNG／PDF 匯出與 Dev Mode CSS Inspect 已取得實際檔案證據；Share 權限、GitHub push 與公開部署沒有在機器階段代替使用者執行。三組 Probe 都已有實檔與操作紀錄，但仍不能將 G1 改為真人放行。

### B4 代表單元機器產製與冷啟動

**日期**：2026-09-16
**狀態**：`MACHINE_PASS_PENDING_HUMAN`
**教案**：`../_lessons/uiux-designer/B4-overlay-single-action.md`
**講義**：`uiux-designer/part2/CH4-overlay-single-action.html`

已將 Probe B 的實測邊界轉為可從零執行的教案與 HTML：8 個段落、Demo／Together／Solo／Checkpoint、修復路徑、Quiz、素材包與證據表均已納入。HTML 以 Chrome localhost 預覽，`lint-page.py` 結果為 0 BLOCKER／0 ERROR／0 WARN；Overlay 完成圖與起始材料的 HTML 連結可直接讀取。原始 Markdown／TXT 保留作為版本化來源，避免瀏覽器擋住直接開啟文字檔造成學員卡點。

冷啟動紀錄：`uiux-designer/_validation/autonomous-run/COLD-FOLLOW-ALONG-B4.md`。跨平台邊界：`uiux-designer/_validation/autonomous-run/CROSS-PLATFORM-MATRIX.md`。本單元仍不能標記 `HUMAN_PASS`；Photoshop、真人跟做、分享權限與公開部署維持未驗證。

### B4 → B6 → B7 三單元產物鏈

**日期**：2026-09-16
**狀態**：`MACHINE_PASS_PENDING_HUMAN`
**證據**：`uiux-designer/_review/ARTIFACT-CHAIN-B4-B6-B7.md`

B6 已接手 B4 的 Host／Overlay 與核心 action，產出固定任務測試、問題分類、單一變因修正與回歸紀錄；B7 再接手 B6 的 `case_id` 與回歸版本，產出 PNG／PDF／Inspect 與 Handoff 清單。三頁均已在 Chrome localhost 檢查並通過 lint。B8 網站／GitHub／部署與 Photoshop 尚未執行，因此整門課仍不放行。

---

## 備忘（非 Gate 但值得留存）

- 目前工作樹沒有可安全局部修正的舊 outline、lesson plan、Gate 或 HTML；基線報告判定為 `REBUILD_FROM_NEW_BASELINE`。
- `uiux-designer/_review/CH1-1-ZERO-BEGINNER-TRIAL.md` 與兩份 PDF 素材暫作歷史試跑材料候選，不能代表新 99h 課程已通過真人試跑。
