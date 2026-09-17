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
**狀態**：`MACHINE_READY_PENDING_HUMAN`
**教案**：`../_lessons/uiux-designer/B4-overlay-single-action.md`
**講義**：`uiux-designer/part2/CH4-overlay-single-action.html`

已將 Probe B 的實測邊界轉為可從零執行的 7h 教案與 HTML：Overlay／Swap 概念、Demo／Together／Solo／Checkpoint、修復路徑、Quiz、素材包與證據表均已納入。HTML 以 Chrome localhost 預覽，`lint-page.py` 結果為 0 BLOCKER／0 ERROR／0 WARN；Overlay 完成圖、Swap 分支與起始材料的 HTML 連結可直接讀取。原始 Markdown／TXT 保留作為版本化來源，避免瀏覽器擋住直接開啟文字檔造成學員卡點。

冷啟動紀錄：`uiux-designer/_validation/autonomous-run/COLD-FOLLOW-ALONG-B4.md`。跨平台邊界：`uiux-designer/_validation/autonomous-run/CROSS-PLATFORM-MATRIX.md`。本單元仍不能標記 `HUMAN_PASS`；Photoshop、真人跟做、分享權限與公開部署維持未驗證。

### B5 長內容、固定導覽與漂浮按鈕

**日期**：2026-09-17
**狀態**：`MACHINE_READY_PENDING_HUMAN`
**教案**：`../_lessons/uiux-designer/B5-scroll-fixed-floating.md`
**講義**：`uiux-designer/part2/CH5-scroll-fixed-floating.html`
**素材**：`uiux-designer/assets/B5-scroll-fixed-floating/START-HERE.html`、`reference/EXPECTED-CHECK.html`

已將 B5 的長清單情境、402×874 Frame、Overflow Before／After、`Vertical` 示範、Chrome 上滑、固定 Header、Floating Action、十二筆 Solo 變化與 B6 交接條件寫入學員頁。Probe B B-06 只確認 Overflow menu 的選項；固定與滾動的聯合效果、不同帳號差異與真人冷讀仍待人工回歸。B5 不得因頁面可開啟就標記 `HUMAN_PASS`。

### B4 → B5 → B6 → B7 四單元產物鏈

**日期**：2026-09-16
**狀態**：`MACHINE_PASS_PENDING_HUMAN`
**證據**：`uiux-designer/_review/ARTIFACT-CHAIN-B4-B6-B7.md`

B5 先接手 B4 的可預覽原型，產出長清單、Overflow、固定／漂浮層的檢查紀錄；B6 再接手 B4／B5 的 `case_id` 與任務條件，產出固定任務測試、問題分類、單一變因修正與回歸紀錄；B7 接手 B6 的回歸版本，產出 PNG／PDF／Inspect 與 Handoff 清單；B8 接手 Handoff 包，完成本機 HTML／CSS／最小 JavaScript 與 Git 路徑。五頁均已在 Chrome localhost 檢查並通過 lint，但 Swap、固定／滾動聯合行為、GitHub push／公開部署與 Photoshop 尚未完成，因此整門課仍不放行。

### 零基礎講義與文案閘門追加結果

**日期**：2026-09-16
**狀態**：`MACHINE_READY_PENDING_HUMAN`
**審查**：`uiux-designer/_review/COURSE-HANDOUT-AUDIT-2026-09-16.md`

- 入口頁已重建為「工作情境 → 成果 → 學習節奏 → 兩階段課綱 → 工具準備」；A3／B4 等製作編號、機器試點與教師驗證資訊已移出學員視線。
- A3 已重建為可冷讀單元：起始材料、白話概念、完整示範、6 步跟做、2 個 Checkpoint、單一變因練習、錯誤回修、驗收與 B4 接手條件均已出現。
- A1 已補上正式教案、起始材料、完成檢查表與 7 段學員頁；入口 → A1 → A2 已在 Chrome 點擊驗證。A1 的 Figma Color styles／Text styles 實測與真人冷讀仍待下一個 Gate。
- A4 已補上主元件／Instance 的學員頁、教案、起始材料與完成檢查表；Chrome 入口與頁面連結已驗證，狀態為 `MACHINE_READY_PENDING_HUMAN`。Variants、Property 與真人冷讀仍留在下一個 Gate。
- `uiux-designer/_design/COPY-RISK-GATE.md` 已把跨專案清單轉成 `BLOCK／REVIEW` 兩級規則；本輪掃描結果為 `0 BLOCK / 0 REVIEW`。後續若出現 REVIEW，仍要逐行人工判讀，不以自動掃描取代冷讀。
- 入口 → 視覺基礎 → 格線與版面 → Auto Layout 的連結已在 Chrome 點擊驗證；A1 已完成來源教案同步，A1／A2 真人冷讀仍待完成。
- A2 已完成正式教案、起始材料、完成檢查表與 7 段學員頁；入口 → A1 → A2 → A3 → A4 已在 Chrome 點擊驗證。Figma Layout guide／Columns／Offset／Gutter 與 360 px 縮窄已在 Probe A 的 A-13／A-14 完成機器實測；A1／A2 真人冷讀與跨帳號重跑仍待完成。
- A3 已修正導覽：上一堂連回 A2、下一堂連到 A4；A4 → A5 → A6 已依頁面產出逐段開放，A6 → A7 暫停在總覽，不能以不存在的連結假裝課程已連續完成。
- A5 已完成正式教案、起始材料、完成檢查表與 7 段學員頁；A4 → A5、A5 → A6 已在 Chrome 點擊驗證。Probe A 的 A-06／A-07 支援 Variant 建立、Property value 與 Instance 切換；A5 真人冷讀與跨帳號重跑仍待完成。
- A6 已完成正式教案、起始材料、完成檢查表與 7 段學員頁；A5 → A6、A6 起始材料／檢查表／總覽已在 Chrome 點擊驗證。Probe A 的 A-15／A-16 支援 Button component／variant 與 Form 視覺圖層；輸入互動、多欄位與真實驗證流程仍未測試，A6 真人冷讀與跨帳號重跑仍待完成。
- A7 已完成正式教案、起始材料、完成檢查表與 7 段學員頁；A6 → A7、A7 起始材料／檢查表／總覽已在 Chrome 點擊驗證。Probe A 的 A-17～A-19 支援兩個視覺列、長標題 Auto height 與空狀態圖層；動態增刪、資料切換與多列聯合滾動仍未測試，A7 真人冷讀與跨帳號重跑仍待完成。
- A8 已完成正式教案、起始材料、完成檢查表與 7 段學員頁；A7 → A8、A8 起始材料／檢查表／總覽已在 Chrome 點擊驗證。Probe A 的 A-20～A-22 支援 Toast、Dialog、Navigation 視覺層；自動出現、Overlay、關閉、置頂與 Prototype 連結仍未測試，A8 真人冷讀與跨帳號重跑仍待完成。
- B1 已完成正式教案、起始材料、完成檢查表與學員頁；A8 → B1、B1 起始材料／檢查表／總覽已在 Chrome 點擊驗證。Probe B B-01 支援 402×874 Frame 與手機 Prototype 入口材料；登入 Navigate action、轉場、Overlay、滾動與多 action 仍由 B2–B5 分別驗收，B1 真人冷讀與跨帳號重跑仍待完成。
- B2 已完成正式教案、起始材料、完成檢查表與學員頁；B1 → B2、B2 起始材料／檢查表／總覽已在 Chrome 點擊驗證。Probe B B-02／B-04／B-05 支援 Add action、Navigate to、Instant 與 Starter 多 action 邊界；B2 真人冷讀與跨帳號重跑仍待完成。
- B3 已完成正式教案、起始材料、完成檢查表與學員頁；B2 → B3 → B4、B3 起始材料／檢查表／總覽已在 Chrome 點擊驗證。Probe B B-05 支援 Animation 選單的 Instant、Dissolve、Smart animate、Move in、Move out、Push、Slide in、Slide out；Smart animate 匹配與完整動態效果仍待人工回歸，B3 真人冷讀與跨帳號重跑仍待完成。
- 目前 16 個單元頁均有對應檔案，但仍不能代表 99h 正式放行；B5 的固定／滾動聯合行為、Photoshop、GitHub、真人冷讀與公開部署仍未放行。

---

## 備忘（非 Gate 但值得留存）

- 目前工作樹沒有可安全局部修正的舊 outline、lesson plan、Gate 或 HTML；基線報告判定為 `REBUILD_FROM_NEW_BASELINE`。
- `uiux-designer/_review/CH1-1-ZERO-BEGINNER-TRIAL.md` 與兩份 PDF 素材暫作歷史試跑材料候選，不能代表新 99h 課程已通過真人試跑。

### 2026-09-17 內容循環檢查追加

- B6、B7、B8 已補齊情境五問、完成物、操作示範、同步跟做、單一變因練習、Checkpoint、修復路徑與下一站交接；B6 上一堂修正為 B5，B7 下一堂修正為 B8，B8 導回課程總覽。
- 50 頁 lint 為 0 BLOCKER／0 ERROR／0 WARN；文案風險掃描為 0 BLOCK／0 REVIEW；16 個單元頁的 continuity audit 均為 0 warning；185 個相對連結為 0 missing。
- Chrome localhost 已實走入口 → B6 → B7 → B8 與 B8 → 總覽；`web-starter` 按鈕已確認狀態、disabled 與回饋文字同步更新，瀏覽器錯誤／警告為 0。
- 目前狀態更新為 `MACHINE_READY_PENDING_HUMAN`。這代表機器階段的內容、路徑與本機互動已通過，不代表 Figma／Photoshop／GitHub／部署或真人冷讀已放行。完整記錄見 `uiux-designer/_review/ITERATIVE-RELEASE-CHECK-2026-09-17.md`。

### 2026-09-17 學員入口 30 秒修復

- 發現 B6、B7、B8 的頁首曾連到內部 `_design/COURSE-BLUEPRINT.md`；起始材料也晚於第一個操作。這些問題不會被單純的「連結存在」掃描抓到。
- 已建立 `uiux-designer/_tools/learner-entry-smoke.py`，並在備份後把三頁返回導覽改為課程總覽，把 B6／B7／B8 起始材料移到第一次操作前。
- 語意入口掃描 PASS；learner／asset／web-starter 相對連結 171 個、0 missing；Chrome B6 → B7 → B8 → 課程總覽 PASS。
- 入口 `BLOCK` 已解除，可進行聚焦人工試讀；整體 Gate 仍為 `MACHINE_READY_PENDING_HUMAN`。

### 2026-09-17 內容證據掃描修復

- 共用 `audit-course-substance.py` 已改為遞迴發現 `part1/`、`part2/`、`part3/` 的正式頁面，避免根目錄掃描造成 0 頁假綠。
- 最新證據清單：16 pages、0 BLOCK、0 REVIEW、16 READY_FOR_HUMAN、0 missing_assets；檔案為 `uiux-designer/_validation/L5-evidence-manifest.json`。
- B4 已補上起始材料與取得順序；B6、B7、B8 的起始材料仍在第一次操作前可見。
- 這只解除機器可驗證的內容證據阻塞；人工試讀可從 B4 → B5 → B6 開始，整體仍為 `MACHINE_READY_PENDING_HUMAN`。
