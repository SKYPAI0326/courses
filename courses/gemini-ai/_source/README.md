# 正式來源與歷史來源

有效課程為五章核心、29個遊樂園案例與13份延伸參考。chapters/CH1.md～CH5.md、supplements/*.md、playground/PG01.md～PG06.md是唯一正文來源。既有23個案例保留supplements來源與原網址，不另複製成第二版。

OUTLINE.md、CURRICULUM-MAP.md、lesson-map.json與playground/catalog.json描述同一架構。catalog包含來源、不同完成物及分項審核狀態；作者核對、Gemini生成與真人跟做分開。

fragments與_review/prompt-controls-2026-10-08為歷史快照，不再作正式建置輸入。修改正文後執行python3 _tools/render-five-chapters.py，會讀主目錄來源並同步遊樂園及首頁。同步TXT、README及ZIP，重測複製、連結、版面和工具行為。舊單次build/prepare腳本只供追溯，不可覆蓋現行正文。
