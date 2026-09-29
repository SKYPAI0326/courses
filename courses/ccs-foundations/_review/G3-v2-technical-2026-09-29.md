# CCS Foundations G3 v2 技術驗收紀錄

- 日期：2026-09-29
- 範圍：9 個新版本頁面（CH1-1 至 CH1-4、PRAC1、CH2-1 至 CH2-4）。
- 舊版 HTML 與 index.html 未修改；新頁只在 v2 檔案間互連。
- 搜尋索引與 sitemap 暫不重建，待課程負責人決定是否切換導覽後再處理。

## 機器檢查

| 檢查 | 結果 |
|---|---|
| `docs/lint-page.py`，9 頁逐頁檢查 | PASS；0 BLOCKER、0 ERROR、0 WARN |
| `validate-course-structure.py` | PASS；9/9，單一 `.lesson-body`、section 後代與 HTML/CSS 結構正常 |
| `audit-course-substance.py` | PASS；9/9，頁面標題、H1、正文及本地連結存在，0 缺失素材 |
| `course-validator.sh ... content --unit` | PASS；9/9，來源內容紀錄有效 |
| 可見正文對照 | PASS；9/9，詳見 G3 v2 頁面保真紀錄 |
| 未追蹤 HTML 尾端空白檢查 | PASS；9/9，`git diff --check --no-index` 無空白錯誤 |
| 舊版頁面／首頁範圍 | 保留；未修改舊頁或 index.html，未提交或發布 |

## 瀏覽器檢視

- 狀態：PENDING。
- 原因：桌面端嘗試直接預覽本機 HTML 時，瀏覽器安全政策只允許 HTTP(S)，拒絕 `file://`。政策亦禁止改以其他介面或本機服務繞過，因此沒有取得 1440px、390px、430px 的畫面證據。
- 待補項目：桌面 1440px 頂端／中段／底部、手機 390px 與 430px；檢查水平捲軸、表格與導覽可用性、sticky header 遮擋、長標題與 footer 換行，以及 progress localStorage 首次載入／重新整理行為。

## 交付狀態

九頁的機器檢查與文字保真已完成；G3 尚未完全放行，因 RWD 瀏覽器 smoke 未完成。未更新首頁連結、搜尋索引或 sitemap。尚未執行真人冷讀、平台操作或授課驗收。

## 2026-09-29 後續更新

- 本技術驗收紀錄完成後，課程負責人決議將首頁切換至今日 9 小時新版；舊 CH5-1 至 CH5-4 HTML 與 Markdown 另行封存，CH4 舊頁的下一步改回首頁。搜尋索引與 sitemap 仍未重建。
- 隨後將舊版 `CH1-1.html` 納入 syntax-only 修復：兩組比較卡 16 個裝飾點的錯置巢狀改為 `<span class="compare-dot" aria-hidden="true"></span>`。`check_content_unchanged.py` 顯示文字與 href 不變；課程結構批次檢查現為 `checked=22 blocked=0`。
- 本更新不改動 9 個 v2 頁面的內容保真結果；瀏覽器 RWD smoke、真人冷讀與平台／授課驗收仍為 `PENDING`。
