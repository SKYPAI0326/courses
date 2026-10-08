# 本批確定性與瀏覽器實測

2026-10-08，actor tool-run。CH3／CH4與index／module四頁structure及course-structure通過；lint四頁0 BLOCKER／ERROR／WARN；兩章substance各machine_checked、0 missing assets，語意審查由作者紀錄另列。

check-ch3-ch4.py重算兩決策的容量／工時及唯一變因，核對來源關鍵主張、129個正式原子、8原完整pre/table、18素材payload、33／25舊欄及key、Gate與7受保護檔案hash、115 local links。搜尋只生成本課scoped entries，不覆寫根search-index.json；課程Gate不更改，無新增公開sitemap URL。

Chrome本機127.0.0.1:8766最終頁實測18份完整複製逐字一致；主線欄位及勾選可保存，實際下載2章各兩個Markdown，重載前後除匯出時間完全相同，姓名／代號與檢查文字也保留。browser-fixtures明示UI-QA、作者參考與平台待重跑；100%僅填寫計數，不是引用／真人通過。測試結束檢查勾選退回未勾，沒有宣稱已實跑NotebookLM或LLM成品。

1440×960兩章各hero／workplace／workbench／check四位置，主要內容1120px、sticky top=0；390與430各章均無水平捲軸。保存檔案與手機／桌面截圖在本目錄。補上mobile header避免中文標籤末字掉行，共享CSS未修改。手機與導覽最終版瀏覽器核對；human/platform/PENDING為實際缺驗。

可重現：python3 _validation/ch3-ch4-2026-10-08/raw-materials.py；bundled node執行render.mjs；python3 check-ch3-ch4.py；結構與lint命令見structure.log/lint.log。工具獨立實測詳見browser-copy／browser-workbench／browser-viewport／browser-desktop-positions及真下載檔。歷史複製錯誤和匯出元資料漏項已修並重跑，未略過失敗。
