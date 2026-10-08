# 實跑缺口回寫計畫

2026-10-08；使用者「執行」核准；task_scope: content-change。單人 source-first 修補，未委派。先備份，再修教案／提示詞，作者內容審查後轉製HTML，最後結構／保真／UI與證據。

目標：CH4 第一輪原限制／第二輪新增限制，過程紀錄與主管交付分開，新增可完整複製的一頁模板、精簡提示及人工拒答／過長備援；CH1 自行計數與已安排但完成未知的實際修句；CH3 真引用→原文→判支持→人工修句與來源定位保存。完整允許文字差異在本目錄 SOURCE-CHANGES.json，產頁前產出；不修改原可選生活教案附錄。

修改檔：CH1/CH3/CH4的教案與HTML、四份既有repair/compare/change提示詞、新增各章完整實跑修復示例與CH4模板／精簡提示／兩例人工交付稿；evidence、gates、progress、current-status更新。

插入點：HTML parser定位既有 .lesson-body 下唯一 #workplace-practice，沿用既有外層、導航、CSS、所有欄位與v2 key。增加區塊只在該section內；頁尾驗收CH3「具體修訂」允許核對正確無差異，CH4區別過程與交付，明列為允許文案同步。既有hero/Gate/script/footer不動。

Activity Identity：CH1單來源日期／狀態／字數；CH3多來源支持程度／權威／適用範圍；CH4硬限制／排序／敏感性，各章各自選一案，不將新示例列額外交付。Shared Copy Audit：四提示詞→教案pre→HTMLpre逐字核對；新素材下載與完整複製；選做舊例、保存欄與其他章逐字保留。

驗收：源數字與原平台證據對照、新素材完整可讀、正式教案原子不漏；parser結構與外部片段不變、lint/substance、桌面1440及手機390/430、實際copy與download、保存台欄位/storage不變。機器可用不代表真人、原平台通過不延伸到新提示詞。無commit/push/publish授權。

回復：_backup/2026-10-08-pre-field-repairs/restore.py（預設dry-run，--apply只恢復既有檔，新資產保留）。

## 一次例行修正
原CH1主標的br在備份版已存在，lint B-v3-1阻擋。補允許syntax-only：只將主標br換空格，文字與主標class不變，沿用既有max-width軟斷，不改CSS／wrapper。本批唯一lint修正，失敗時停下診斷。
