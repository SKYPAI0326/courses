# _gates.md — uiux-designer 品質檢核存證

> 一門課一份、append-only。每個 Gate 結束時追加問答、證據與決定；不刪除舊條目。

**課程 slug**：uiux-designer  
**負責人**：課程製作流程  
**建立**：2026-09-07  
**目前 Gate**：G1 大綱定位草稿  
**目前狀態**：`G1_DRAFT_REVIEW`

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

---

## 備忘（非 Gate 但值得留存）

- 目前工作樹沒有可安全局部修正的舊 outline、lesson plan、Gate 或 HTML；基線報告判定為 `REBUILD_FROM_NEW_BASELINE`。
- `uiux-designer/_review/CH1-1-ZERO-BEGINNER-TRIAL.md` 與兩份 PDF 素材暫作歷史試跑材料候選，不能代表新 99h 課程已通過真人試跑。
