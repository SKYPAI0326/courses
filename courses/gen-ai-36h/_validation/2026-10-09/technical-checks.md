# 靜態與功能檢查紀錄

日期：2026-10-09。執行者：工具（tool-run）。範圍：本課 28 份來源／HTML、33 個可見 HTML 頁與本課素材和功能程式。以下結果是在修正 PRAC5 虛構收件人用詞並重轉製後重跑。

| 命令／方法 | 實際結果 |
|---|---|
| `python3 _tools/verify-course.py` | PASS：28 頁來源至 HTML 段落／表格／程式區塊、站內連結、原密碼腳本／導覽、首頁標題、24 月資料及 JS 語法 |
| `node _tools/test-course-functions.cjs` | PASS：報價邊界、營收合計／年增率、路由／去重、JSON 驗證、儲存失敗及匯出跳脫 |
| `node _tools/test-form-controller.cjs` | PASS：DOM 模擬的保存／載入、損壞匯入、備份恢復、容量不足匯出與個人 HTML 值；真實瀏覽器待驗 |
| `python3 docs/lint-page.py courses/gen-ai-36h --summary`（於網站根目錄） | 掃描 33 頁；BLOCKER 0、ERROR 0、WARN 37（字體及用字類） |
| 共用 HTML 結構檢查（`_repair/2026-10-09/structure-final.txt`） | 33 頁 checked，blocked 0；只驗靜態結構 |
| `git diff --check` | 無空白格式錯誤 |

工具僅檢查可確定條件。平台操作、真實裝置版面與學員能否理解仍待另外驗收。
