# 正式建置、審核與驗證

來源是_source/chapters/五章、_source/supplements/36份（23案例＋13參考）、_source/playground/六新例。從來源改稿，先審背景、觀念、完整示範、操作、判讀與章節關係。

1. review-playground.py比對29例來源、素材、提示詞與人工審閱指紋，生成RECOMMENDATIONS.md；正文變動回待審。新增方向先推薦與使用者討論，選定才產製。manual-content-review.json由實際審閱者完成，不能批次自動更新指紋冒充重審。
2. render-five-chapters.py轉製正式核心、既有正文、首頁與舊址轉向；自動呼叫build-playground.py建六新頁、29例目錄與ZIP。保留既有殼層並逐項核對文字、提示詞、連結。
3. validate-playground.py只檢查49個正式頁面，排除備份/檢閱快照，核對結構、錨點、素材、TXT/ZIP和專案lint。
4. verify-course-browser.cjs以本機32194伺服器測五章、29例分類方塊與案例卡片、129個複製區、舊址與三種寬度；verify-core-tools.cjs測新增核心參考品；verify-playground-tools.cjs測六新工具A/B、CSV、例外和閱讀寬度。測試使用隔離剪貼簿writer，不宣稱系統剪貼簿寫入通過。
遊樂園入口單獨修改時，用 `python3 _tools/build-playground.py --landing-only`，只重建 playground/index.html，不改講義或 ZIP。遊樂園保留自己的殼層，不繼承課程首頁的開始按鈕與折疊參考。`verify-playground-cards.cjs` 檢查五分類、29案例跳轉與返回、鍵盤焦點，以及1440／768／390／430寬度。

5. 測試完成後計算新指紋，更新_validation/，不能只換hash沿用舊PASS。實際Gemini、真人學習與課堂時數分開驗證。

課程首頁來源是 `_source/course-entry.json`。`python3 _tools/build-course-entry.py` 只重建 index.html；完整建置於遊樂園轉製後套用相同入口。`python3 _tools/verify-course-entry.py` 核對入口、13份參考與分類錨點、原殼層、隔離的錨點展開程式及重建保真；這些檢查不代表新版瀏覽器畫面已通過。首頁修繕證據與備份在 `_repair/2026-10-08/course-entry/`。

restore-playground.py預設只核對本輪檔案，--apply才回復；後續指紋變動即拒絕，避免覆蓋其他工作。本輪備份在_backup/2026-10-08-playground-pre。

verify-five-chapters.cjs、restore-five-chapters.py是遊樂園前的歷史證據；build-five-chapters.py、prepare-supplement-narratives.py是一次性來源遷移，不能覆蓋現行正文。_review/是舊快照，正式編輯只在主目錄。


## 已審查的冷色配色與表格

`_source/coldtone-styles.json` 定義49個正式入口與教材頁的共用配色、提示詞／生成結果卡片，以及頁型特定表格樣式。`render-five-chapters.py` 的序列化階段按 canonical URL 套用，首頁與遊樂園建置共用此流程。既有作者參考工具可用 `python3 _tools/coldtone_styles.py` 重套；`--check` 驗證沒有樣式漂移。只新增 head style，不改正文、原腳本、導航或密碼。

`_source/render-shells/` 保留現行轉製所需殼層，`_source/page-inventory.json` 與 `CONTENT-REVIEW.md` 保留既有轉製基線，正式重建不再依賴未提交的 `_backup` / `_repair` 輸入。新產出的驗證結果仍放 `_repair`。


## 全課程共用視覺樣式（2026-10-11）

`_source/coldtone-styles.json` schema 2 的 `shared_styles` 定義唯一配色、提示詞排版與生成結果卡片；49個正式入口／教材頁的 `pages` 以 `ref` 引用。頁面特殊圖表修正以 `append_css` 保留，原有工具表格設定維持原範圍。`coldtone_styles.py` 解析共用引用，只更新 head 內指定 style 節點，不改正文或腳本；既有建置器會套用相同解析結果。正文與互動來源維持原責任層。

後續調整共用字體、連結與配色時，修改 `shared_styles` 後套用到相依頁面並驗證，不再只更新少數代表頁。這次樣式統一的49頁名單、備份、內容保護及代表頁瀏覽器證據保存在 `/private/tmp/gemini-theme-unification-20261011-u7_x_asi/`；未進行push。
