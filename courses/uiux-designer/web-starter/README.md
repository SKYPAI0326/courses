# 工作室待處理清單：可修改網站

本課完整專案：index.html提供畫面、styles.css提供樣式、app.js處理示範任務與確認，my-screen.html是把自己設計的清單畫面做成網頁的練習範本，assets/status-badge.png是整理交付包那一堂的透明PNG參考。

解壓後直接雙擊index.html，用Chrome／Edge開啟。修改時以VS Code Open Folder開啟這個資料夾，Save後回瀏覽器Reload。不需npm、資料庫或伺服器。

## 試一次完整流程

登入→第一筆任務詳情→標記完成→取消（仍在詳情）→再次確認→已完成清單與Toast。回待處理捲到最底部，確認最後一列不被導覽遮住。已完成詳情的Button不能再次提交。重新整理回預設資料。

## 與設計稿的關係

色碼、字級、Button高48、Dialog寬320、長任務列、固定Navigation與漂浮Button對應前面幾堂的規格。示範登入不驗證真實帳密，資料只留在目前頁面記憶體，沒有後端或長期儲存；Figma的Swap與Smart Animate測試分支沒有全部轉成網站。

## 修改與交付

先修改標題、主要色與T02長標題，把瀏覽器視窗拉到360～430的手機寬度與桌面寬度各看一次。用自己透明徽章替換assets/status-badge.png，保持相對路徑與檔名一致。README追加你的Figma／repo／網站連結、已測專案與簡化範圍。

Git安裝與GitHub註冊見課前準備頁；第一筆commit、diff、GitHub repository與Pages的完整步驟見做網站那一堂。先建立基準再提交有意義的修改。公開前只保留示範資料。
