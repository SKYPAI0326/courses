# Gemini AI 課程路線同步修復紀錄

## 結果

本次完成新版課程路線同步：7 個課堂核心單元、32 個課後補充單元（29 個延伸、3 個參考），另有 1 個時區歷史頁保留原始檔但不列入新版目錄。此結果只代表路線與入口同步完成，課程內容仍未完成重寫或學員驗收，不可視為可直接授課或發布給學員。

七站順序為 CH1-1、CH1-2、CH1-3、CH2-1、PRAC2-1、CH4-1、PRAC4-3。首頁、manifest、前後站、進度完成數和目錄角色已依此順序同步。CH1-3 頁面標題與課程地圖也已對齊「依需求選擇提示詞類型」。首頁進度儲存鍵升為 v2，避免舊版 10 站完成狀態套用到新路線。

## 變更範圍

- 更新 _source/OUTLINE.md、LESSON-PLANS.md、CURRICULUM-MAP.md、lesson-map.json，讓五階段說明、七站學習目標與 40 頁教材分流一致。
- 更新 index.html 的必修清單、完成數、目錄標籤與連結；PRAC2-2 從新版入口移除，原檔保留。
- 更新九個單元頁的導覽或補充角色；另同步 CH1-3 頁面身份標題。教學正文與完整提示詞維持原內容；只有核准的 CH6-1 補充定位句及 PRAC4-3 總站數文字改動。
- 更新靜態與瀏覽器驗證器，依 manifest 驗證七站路線，將結果輸出到日期資料夾；不讀寫全站搜尋索引或 sitemap。
- 修改前備份 19 個檔案；_backup/2026-10-07-stage3-route-pre-sync/SHA256SUMS 全數驗證通過。還原入口為 _tools/restore-2026-10-07-stage3-route-pre-sync.sh。

## 驗證結果

- 靜態檢查：45 頁，內部連結、錨點、來源片段、素材 ZIP、首頁 39 頁目錄及七站標題／導覽符合檢查條件。
- 瀏覽器：11 項互動與導覽檢查、77 個桌機／手機視窗觀察通過；本機舊 v1 完成狀態不會誤算新進度。
- 課程 lint：45 頁，0 blocker、0 error、83 warnings。
- 10 個目標講義頁通過 HTML 結構檢查；逐頁比較確認教學正文與提示詞未被改寫。
- 2026-10-06 既有驗證證據雜湊未變。詳細結果見 route-sync-check.json、link-and-copy-audit.json 與 evidence/browser-results.json。

## 發布阻擋與待辦

瀏覽器實測發現三個未修正的既存頁面腳本錯誤，其中兩個在核心路線：

- CH1-3：頁面程式綁定不存在的計時器控制項（#demoStart 等），載入時出現 null addEventListener 錯誤。
- PRAC2-1：頁面程式將資料列加入不存在的 #calc-rows，載入時出現 null appendChild 錯誤。
- PRAC3-3：補充頁程式將 KPI 列加入不存在的 #kpi-rows，載入時出現 null appendChild 錯。

這三頁的教學內容不在本次路線同步授權範圍內，因此只記錄、不補做修復。CH1-3 和 PRAC2-1 的實際錯誤須在後續內容修復階段處理後再驗收。

尚未執行的工作包括：CH1-1 至 CH1-3 完整學員講義重寫、貪食蛇提示詞在 AI Studio 的生成試跑、核心案例頁型試作、補充教材逐案完整提示詞與操作驗收、學員 agent 冷讀、使用者人工審閱、六小時真人試教，以及 course-ops 的全站搜尋索引／sitemap 更新。平台生成與學員跟做均保持未驗證。本次不 push。

## 回復方式

如需完整還原本次修改，先檢查 _backup/2026-10-07-stage3-route-pre-sync/SHA256SUMS，再執行 _tools/restore-2026-10-07-stage3-route-pre-sync.sh。還原會覆蓋本次列入備份的 19 個來源、入口、工具和 HTML 檔案。
