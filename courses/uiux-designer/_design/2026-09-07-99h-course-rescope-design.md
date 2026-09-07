# UI/UX 99 小時課程修正設計

日期：2026-09-07  
狀態：設計規格，尚未進入課程大綱、教案或 HTML 製作

## 1. 設計決策

本設計以使用者提供的兩張正式授課課綱圖片為新基準：

- `/Users/paichenwei/Downloads/1788509783989.jpg`：介面元素與設計，42 小時
- `/Users/paichenwei/Downloads/1788509797593.jpg`：UI/UX 原型製作與資料打包，57 小時

總時數固定為 99 小時。舊文件中「Photoshop 42h＋UI/UX 57h」的版本降級為歷史脈絡，不得控制新課程的範圍、時數或 Gate。

圖片與 ChatGPT 交接文字的角色不同：

- 課綱圖片是正式內容邊界與行政時數來源。
- ChatGPT 交接文字是課程重組、教學順序、工具範圍與交接治理的設計建議。
- 兩者若衝突，以正式課綱的課程名稱、主題與時數為準；教學順序則可依技能依賴重排，但不得漏項或增加未核准的課程成果。

## 2. 修正目標

把兩個行政課程重組成一條適合接近零基礎學員的可完成產出鏈：

`介面結構 → 視覺與版面 → Design System → Components → 完整頁面 → Prototype → 測試修正 → Asset/Handoff → HTML/CSS/基礎 JavaScript → Git/GitHub → 雲端部署`

重組後仍須能回溯到兩個正式課程：

- 42h 必須完整覆蓋色彩、字型、格線、Auto Layout、Component、Button、Form、List、Toast、Dialog、Navigation、Variants。
- 57h 必須完整覆蓋線框／原型／工具介紹／手機介面／元件與動畫互動，以及觸發事件、轉場、Overlay、Swap、滾動、置頂導覽、漂浮按鈕、Smart Animation、Figma／PS 發布與輸出、網頁入門、雲端部署。

## 3. 不變與可變邊界

### 不變

- 行政總時數：42h＋57h＝99h。
- 兩個正式課程名稱與內容項目不得漏列。
- 受眾：接近零基礎，不能預設 Figma、Photoshop、前端或 Git 經驗。
- 工具範圍：Figma、Adobe Photoshop、VS Code、Chrome、HTML、CSS、基礎 JavaScript、Git、GitHub。
- 不納入 React、Vue、Next.js、TypeScript、Tailwind、後端框架、資料庫，除非另行核准。
- 每個新能力都要有概念、操作位置、具體值、預期結果、驗證與 Debug。

### 可變

- 行政課綱的教學順序。
- 42h 與 57h 內的單元切分方式。
- 哪些單元合併或拆分，但每個單元必須有獨立可驗收完成物。
- 案例、素材與專題主題。
- 先講解或先實作的微節奏，只要符合零基礎可跟做與 Gate 證據要求。

## 4. 建議技能依賴架構

這 16 個 Stage 是教學架構候選，不是行政課程名稱，也不代表已完成時間分配。

### A. 基礎與介面結構

0. UI/UX、工具與產出物基本語言
1. Wireframe 與介面結構
2. Visual Foundation：色彩、字型與視覺層級
3. Layout System：格線、Auto Layout 與手機版面

### B. UI Design System

4. Component Foundation
5. Component System：Variants 與狀態
6. Core UI Components：Button、Form、List
7. Navigation & Feedback：Toast、Dialog、Navigation
8. Page Composition：把元件組成完整畫面

### C. Prototype

9. Prototype Foundation：Flow、觸發與基本連結
10. Overlay & Scroll Interaction：Overlay、Swap、滾動、置頂與漂浮控制
11. Motion & Advanced Interaction：轉場、Smart Animation 與動畫目的
12. Prototype Test & Revision：固定任務、錯誤紀錄與回歸修正

### D. Delivery & Web

13. Asset & Handoff：Figma／Photoshop 發布、輸出與資料打包
14. Web Foundation：HTML、CSS、相對路徑與手機寬度
15. Design → Web → Deploy：基礎 JavaScript、Git/GitHub 與雲端部署

## 5. 42h／57h 的分配原則

下一階段才建立逐單元分鐘帳本；本設計先鎖定分配規則：

- 42h 主要承載 Stage 2–8 的視覺、版面、元件與頁面組成能力。
- 57h 承載 Stage 0–1 及 Stage 9–15 的工具入口、線框／原型、互動、發布、網頁與部署能力。
- 若某個主題同時出現在兩門課，必須標示「首次教學」與「後續重用」，不得重複把同一套操作計入兩次。
- Photoshop 只在正式課綱指定的 Figma／PS 發布與輸出脈絡中出現；不得重新推導為 42h Photoshop 專修課。
- 每一小時需由可觀察活動支撐：判斷、操作、錯誤修復、遷移或可重用產物。

時間帳本驗收條件：

1. 每一單元的分鐘加總等於該單元時數。
2. Part 42h 與 Part 57h 分別加總正確。
3. 全課加總為 99h。
4. 找檔、登入、下載、保存、等待與重複點選不支撐主要時數。
5. 每 3 小時至少有一次可觀察檢核；不足 3 小時的單元至少一次。

## 6. 單元設計契約

每個單元必須包含：

1. Learning objectives
2. Usage scenario
3. Core concepts
4. 控制項位置與精確操作
5. Teacher micro-demonstration
6. Follow Along
7. Checkpoint
8. Common mistakes
9. Debug
10. Guided Practice
11. Independent Challenge
12. Acceptance criteria

Teacher demonstration 定義為短、可立即跟做的示範，不是講師獨自完成整個工作流後學員照抄。每個核心操作都要留下學員可查看的預期畫面、檔案狀態或驗證結果。

## 7. 產出與驗收

課程最終至少應形成：

- 可維護的 Wireframe 與手機介面
- Design System、元件、Variants 與必要狀態
- 可真跑的互動 Prototype
- Prototype 測試紀錄與修正版
- Figma／Photoshop Asset 與 Handoff 清單
- 基礎 HTML/CSS/JavaScript 網頁
- Git/GitHub 版本紀錄
- 可公開開啟的雲端部署成果

驗收不只檢查畫面是否存在，還要檢查：

- 零基礎學員能否依講義獨立完成。
- 長文字、項目增刪與手機寬度變化是否仍可用。
- 元件修改能否同步到 Instances，且不以 Detach 逃避問題。
- Prototype 是否能依固定任務完成、回饋錯誤並修正。
- 交付包能否讓另一個人找到正確版本與正確輸出。
- 網頁是否能在手機寬度載入、圖片路徑正確且可公開開啟。

## 8. 修正流程與 Gate

### Gate 0：範圍確認

建立正式內容矩陣，逐項對照兩張課綱圖片；舊 Photoshop 42h 版本標示為歷史，不刪除、不作新基準。

### Gate 1：99h 大綱與依賴

產出新的 outline、Stage／單元矩陣、依賴鏈、學習成果與時間帳本。此 Gate 不寫完整教案與 HTML。

### Gate 2：代表單元教案

先選一個最能代表零基礎難度與整合風險的單元，完成素材、步驟、錯誤修復與驗收條件。

### Gate 3：代表頁與真人跟做

確認頁面能讓學員從起始狀態走到完成物，再決定是否展開同一 Part 的其他單元。

### Gate 4：逐 Part 製作

依核准順序製作 42h 與 57h 內容；每個單元完成教案、講義、素材、lint、文字錨點與跟做驗收後才進下一個。

### Gate 5：整合驗收

從 UI 元素一路驗收到 Prototype、Handoff、網站與部署，確認產出鏈沒有斷裂。

## 9. 目前工作區處理原則

目前工作區內只確認到 `uiux-designer/_review/CH1-1-ZERO-BEGINNER-TRIAL.md` 與部分素材，未確認到完整的舊 outline、Gate、lesson plan 或 HTML。因此在 Gate 0 前：

- 先定位正確舊版本或備份。
- 不覆蓋現有檔案。
- 不把殘留的 CH1-1 試跑檔案誤當成完整課程基線。
- 若找不到舊基線，就以本規格建立新的 99h 版本，並在狀態檔明確記錄「重建」而非「局部修正」。

## 10. 下一步

下一個可執行工作是 Gate 0：建立 42h／57h 正式內容 coverage matrix，逐項核對圖片、ChatGPT 交接規格與可驗收完成物；完成後再進入 Step 3 的 99h 時間分配。

本規格不授權直接製作教案、講義、HTML 或部署檔案。
