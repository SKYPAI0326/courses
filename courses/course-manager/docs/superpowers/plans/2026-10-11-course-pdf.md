# course-pdf Implementation Plan

**Goal:** 建立可呼叫的講義轉製技能、來源追蹤與可回復建置流程，先登錄既有成品，不產製 PDF。

**Architecture:** 技能入口安裝至既有課程技能所在的 ~/.agents/skills；原始套件與引擎保存在 course-manager。來源準備、登錄、建置交易與 CLI 分開；既有資料夾管理 CLI 保持其責任。

**Tech Stack:** Python 3、BeautifulSoup、Playwright/Chromium、pypdf、Poppler。本機 Python 3.12 已具備所需套件；盤點模式不依賴渲染器。

**Spec:** ../../skill-design/2026-10-11-course-pdf-design.md

## Global Constraints

- 使用者已核准設計並授權執行；沿用「先不要創造 PDF」。本輪只執行非 PDF 產製驗收。
- 單一 agent 在目前授權工作區執行，保存無關變更；不 commit、push、部署或建立排程。
- HTML 是教學內容來源；教材全文不新增、不摘要、不重寫；暫存轉換不修改正式來源。
- 舊成品無有效來源 manifest 時維持 UNVERIFIED；候選來源不代表已證明一致。
- build/sync 產製需要顯式 --create-pdf；本輪不傳該旗標。
- 候選 PDF 需內容與全頁視覺證據，才可提升；來源變動或驗收失敗保留前版。

## Review Focus

- 共用 CSS／圖片／字型改動要改變指紋；自我 PDF 下載連結不納入輸入 bytes。
- 隱藏教材、重疊 selector、未知互動／動態依賴不能被靜默漏掉。
- 合冊連結、相對素材路徑和重複 id 要依各頁來源重映射。
- 登錄的舊 PDF 不能因為今天計算 HTML hash 就變成 CURRENT。
- 版本提升與回復需檢查來源及成品 hash，交易中斷不能顯示 CURRENT。

## Task 1：來源與登錄

Files: src/pdf_sources.py、src/pdf_registry.py、tests/test_pdf_pipeline.py、pdf-profiles/default.css。

- [x] 寫出失敗驗收：selector 保留文字、未知互動阻擋、CSS 遞迴依賴、自我輸出排除、舊證據状态。
- [x] 實作 load_recipe/prepare/fingerprint/inventory/register/status，確認不執行 PDF 寫入。
- [x] 執行非產製驗收及实际 36 份登錄，保留候選來源的來源類型與不確定性。

## Task 2：轉製及交易

Files: src/pdf_build.py、scripts/pdf_pipeline.py、registry/pdf/recipes/admin-ai-ch01.json。

- [x] 增加失敗驗收：產製旗標、交易衝突、來源漂移、驗收證據與成品 hash 綁定。
- [x] 實作暫存 HTML、離線資產、字型載入、單次合冊渲染、文字/連結驗收與全頁 PNG 清單。
- [x] 實作 verify/promote/rollback，未檢视頁面、缺證據或 fingerprint 漂移不得提升。
- [x] 提供 doctor、inventory、register-existing、plan、status、build、sync、verify、promote、rollback。
- [x] 實際執行 doctor、plan、status 與不帶 --create-pdf 的 sync；不呼叫 PDF 渲染。

## Task 3：技能與聯動

Files: skill-packages/course-pdf/SKILL.md、agents/openai.yaml、references/workflow.md、docs/pdf-pipeline.md、安裝紀錄及實作報告。

- [x] 寫入真實命令與 schema，技能區分來源保護、未驗狀態、產製限制及未配置持續監看的行為。
- [x] 技能以共用引擎 status/sync 作為其他課程技能的聯動介面；不自動改所有既有技能或正式網頁。
- [x] 靜態驗證技能格式，安裝到 ~/.agents/skills/course-pdf；記錄檔案 hash。
- [x] 比較既有 PDF 全庫 hash，確認沒有產製或改寫；回報尚待實際 PDF 試作的驗收項目。

## Execution ledger

2026-10-11：使用者「同意並授權執行作業」授權依設計執行，採單一 agent。原 PDF 禁令繼續有效。這份計畫細化核准設計，未擴張授權；不重複要求確認。

Ruling: 保留未驗證的舊成品；支援新版建置流程，但本輪不以產生課程 PDF 證明渲染品質。
Ruling: 原設計把 office-ai 六章清單稱為舊版的依據不足；目前仍存在 ch1–ch6，改記為硬編來源清單，逐項核對，不能僅靠章數判斷過期。

2026-10-11：Task 1–3 的程式、登錄、安裝與非產製驗收完成。39 項單元檢查、3 份技能格式檢查、HTML 文字/字型/離線預覽通過；實際 PDF 分頁、擷取、合冊連結及畫面驗收尚未執行，沿用不產 PDF 限制。
