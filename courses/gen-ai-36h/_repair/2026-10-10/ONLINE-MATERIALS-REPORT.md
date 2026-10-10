# 線上素材修復報告

日期：2026-10-10。狀態：**教材來源與入口已修復；本機機器檢查和響應式入口驗收完成；等待推送及線上驗證；真人冷讀待安排。**

## 變更

- 三組職場案例已補足可追溯的聊天、狀態表、政策版本、報價、會議紀錄、決策依賴和逐來源核對答案。
- 新增四個響應式 HTML 素材入口，標明學員任務、閱讀順序、完成物、來源下載和延後開啟的教師答案。新增 PRAC2 可複製交接表。
- 11 個課程頁的資產連結與鏡像教案已同步，指向已排版入口；原始來源仍可下載。
- 原 `START-HERE.md` 改為短純文字轉介，包含線上 HTML 頁絕對網址，避免原始 Markdown 表格再次冒充學員入口。

## 驗證

- renderer：11 頁完成；
- HTML lint：15 頁 BLOCKER 0、ERROR 0；
- 資產／相對連結：15 頁 broken links 0、missing assets 0；
- 跨文件數字／時間／版號一致性：通過；
- 四個入口：1440、390、430px 瀏覽器版面通過；
- 真人試走、個人平台帳號驗證、GitHub Pages 部署後檢查：PENDING。

逐頁紀錄見 `../../_validation/2026-10-10/online-materials-render-evidence.json`、`../../_validation/2026-10-10/online-materials-substance-audit.json` 和 `../../_validation/2026-10-10/online-materials-lint.txt`。修復前 58 個目標檔及 5 個新增檔的還原映射，留在本機 ignored backup 目錄，由本機 restore script 還原；兩者不納入網站教材。
