# 無網頁講義專案倉庫

盤點日期：2026-10-02

本資料夾集中存放目前沒有 learner-facing HTML 網頁講義的獨立專案。搬移判定以目前工作樹的 `.html/.htm` 檔案與現有課程頁面路徑為準。

## 本次搬入

- `affinity-transfer/`：目前沒有 HTML。
- `ai-short-video-editing/`：目前沒有 learner-facing HTML；相關交接文件已同步更新路徑。
- `universal-portfolio-builder/`：沒有 HTML 網頁講義；完整 PDF 使用指南已移至[集中講義庫](../output/pdf/universal-portfolio-builder/ACCESSIBLE-GUIDE.pdf)。

## 暫不搬入

- `accounting-function-lab/`：設計規格與實作計畫含大量根目錄路徑，需另做路徑遷移後再搬。
- `courses/`：包含驗證暫存結構，用途與共用依賴尚未釐清。
- `.worktrees/`、`_backup/`、`_deliverables/`、`_repair/`、`_skill-audit/`、`_tools/`、`_validation/`、`assets/`、`docs/`、`output/`、`tmp/`：保留原位，避免影響課程建置、驗證、資產與路徑引用。

## 安全紀錄

- 現有課程 HTML 未移動。
- 搬移前後應保持課程 HTML 總數不變。
- 若日後在此倉庫新增 HTML，先重新判定是否應回到正式課程資料夾。
