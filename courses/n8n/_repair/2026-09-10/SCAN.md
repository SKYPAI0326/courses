# n8n Learner-Path Scan

**日期**：2026-09-10  
**角色**：挑剔零基礎學員 cold follow-along review  
**範圍**：n8n 目前 HTML（排除 `_backup/`）  
**平台實跑**：本次未執行；僅做頁面、連結、資產與自學路徑檢查。

## 判定

- n8n 自學路徑：BLOCK
- Make＋n8n 整合：BLOCK（另需與 Make canonical payload 對齊）
- Make 單課：CONDITIONAL PASS

## 主要風險

1. 總覽頁沒有把摘要頁與實作頁組成清楚的必修順序。
2. M1-3 JSON 的核心操作仍保留講師替代路徑，缺固定 payload、起始 workflow 與中途 Checkpoint。
3. M4-1 跨服務流程缺帳號／權限／資料契約前置檢查，也缺無外部服務時的等價跟做路徑。
4. M3-2、M4-2 與 M0 安裝頁缺明確起始狀態或中途檢查。
5. M0 參考工作流頁未在主路徑上清楚標示閱讀／設計參考界線。
6. Make 與 n8n 使用不同 canonical payload，尚無 Bridge 頁或轉換表。

## 工具限制

指定的 `docs/audit-course-substance.py` 目前不存在；本次以 `lint-page.py`、copy continuity script、人工閱讀與 cold follow-along 盤點替代，不能將此結果視為平台實跑證據。
