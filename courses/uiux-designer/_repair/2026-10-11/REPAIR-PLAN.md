# Repair Plan：獨立閱讀與跟做

task_scope: content-change
授權：使用者「執行修正」，限前輪審查發現的獨讀路徑、Photoshop起點、B6計分及T08一致性。
範圍：A1、A4、A5、B1、B2、B3、B6、B7教案及對應HTML；相關起始材料、檢查表、Blueprint、Environment Contract；受影響的舊證據失效標記。
文字完整變更清單：text-changes.json；各目標完整修訂案：proposed-changes.json。
不刪除或合併活動；修改原段落使獨讀可執行。課程順序、section id、外層DOM、CSS、導覽與既有表單欄位不變。B6原評分表改為同五類、同權重100分的20個5分判準，新增評分表與Photoshop入口，連結在首次使用前提供。

## 修復清單
1. BLOCKER：正式正文依賴講師／同學。修教案來源，補可自行走讀、植入／修復故障、重開核對的方法；保留同儕活動並分開真實證據與待補。
2. BLOCKER：Photoshop工作站無取得路徑。新增自有授權官方安裝入口與啟動檢查；教室實際資訊未提供就維持待確認，不虛構教室。無軟體不通過PSD操作。
3. MAJOR：B6評分無逐項標準。每項5或0分且附證據，未測記0與待補；必要路徑未測或有阻斷不得通過。同步可保存表單。
4. MINOR：Blueprint的T01–T07改T01–T08；正文與現有測試表已列T08，予以保留。

## 執行順序與驗收
scan → plan → 雜湊備份／還原腳本 → 來源 → 明確DOM錨點同步 → 表單／材料 → 結構、lint、全文與連結核對、git diff、代表頁browser smoke → 報告。
備份含既有未提交修改；不動其他課程，未授權commit／push。既有證據hash失效須標記待重驗；靜態通過不宣告真人或平台已完成。
search-index僅索引title/meta，本輪正式頁title/meta不變；新增材料由講義連結取得，索引是否納入按公開路徑規則核對，必要時僅同步本課條目。

驗收細修：B6複製入口依Figma官方文件補明；評分限定Frame模擬既有能力。8頁footer的built-at與修訂日期同步2026-10-11，platform-version仍保留原官方查證日期。

入口細修：B2明定EMPTY-TEST測試起點；B7補.fig匯入與PSD重開路徑。全部在原段落與DOM錨點內更新，不新增題目或活動。
