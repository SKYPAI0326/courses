# simple-ai 章節下載連結修復報告

日期：2026-08-25

## 完成內容

- 8 個 CH 頁面共加入 12 個來源素材 .txt 下載連結。
- index.html、module2.html、CH2-4.html 的 6 個 PDF 下載 anchor 補上 target="_blank" rel="noopener" download。
- 重建 handbook.html、《創業 AI 實戰手冊》PDF 與 A4 雙面精選 PDF。
- 備份：_backup/2026-08-25-download-links/
- 還原：_tools/restore-2026-08-25-download-links.sh

## 驗證證據

| 檢查 | 結果 |
|---|---|
| .txt 檔案存在且非空 | PASS：12/12 |
| HTML anchor 屬性與本機 href | PASS：22 個素材／PDF anchor，無缺檔或屬性錯誤 |
| 本機瀏覽器點擊 CH1-2 素材 | PASS：收到 download event；檔名 ch1-2-meeting-transcript.txt；Downloads 檔案與來源 SHA-256 相同 |
| 本機瀏覽器點擊 index PDF | PASS：收到 download event；檔名 創業-AI-實戰手冊.pdf；Downloads 檔案與來源 SHA-256 相同 |
| 另開分頁屬性 | PASS：每個 anchor 的 target="_blank"、rel="noopener" 已由 DOM 讀取確認 |
| 整課 lint | PASS：14 頁，BLOCKER 0、ERROR 0（WARN 20） |
| PDF 生成 | PASS：手冊 65 頁、精選 2 頁 |

## 行為說明

target="_blank" 與 download 同時存在時，瀏覽器會以下載事件優先，通常不新增可見分頁；本次實測結果也是「另開分頁屬性存在、點擊直接下載」。若未來要同時保留可見 PDF 分頁，需另提供不含 download 的「開啟檔案」按鈕。

PDF 內嵌素材連結目前由本機 file:// 來源生成，屬本機建置證據，不宣稱在其他裝置上可直接使用；學員應使用課程 HTML 頁面的相對下載連結。
