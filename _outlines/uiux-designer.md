---
slug: uiux-designer
name: 介面元素與設計 × UI/UX 原型製作與資料打包
audience: 零設計與程式基礎，能使用瀏覽器與下載檔案的成人學員
duration: 99h
course_type: skill-operation
revision: 2026-11-02
governing_matrix: courses/uiux-designer/_design/99h-coverage-matrix.md
time_ledger: courses/uiux-designer/_design/99h-time-ledger.md
blueprint: courses/uiux-designer/_design/COURSE-BLUEPRINT.md
status: REPAIRED_CONTENT_PENDING_PLATFORM_AND_HUMAN
---

# 介面元素與設計42h＋UI/UX原型製作與資料打包57h

依正式課綱圖片的12項介面主題及原型／資料打包主題，完成工作室待處理清單。沿用既有16單元與99h行政配置；2026-10-09補強首次方法、實際素材、完整任務、獨立遷移與部署路徑，不把篇幅或機器PASS當成已經授課驗證。

課程能力與起點唯一來源見Blueprint；時數配置見time-ledger。元件／外觀在A首次教，互動／測試在B重用。Git／GitHub是已核准必要交付流程，JS只服務最小網站，不擴張後端或正式登入。

| 單元 | 正式講義名稱 | 本堂能力 |
|---|---|---|
| A1 | 讓畫面看得清楚：色彩、字型與閱讀順序 | 依用途建立視覺規則，說明對比與非顏色線索，並在長句下檢查閱讀層級 |
| A2 | 用格線安排手機與桌面版面 | 計算跨欄寬度，從桌面雙區轉成手機閱讀順序 |
| A3 | 讓文字變長時，容器與按鈕一起排好 | 建立真正的Auto Layout階層，以文字／容器不同尺寸模式處理長句、增刪與寬度變化 |
| A4 | 改一次來源，讓多個按鈕一起更新 | 驗證主元件同步、個別Override及錯誤修復，讓來源與使用處關係可觀察 |
| A5 | 把主次按鈕與狀態做成可選的元件 | Type×State八種Variant（Default／Hover／Pressed／Disabled）、Label文字屬性、Show icon開關與Icon換圖示屬性 |
| A6 | 完成表單與錯誤修正 | 文字欄四狀態元件；勾選、單選、下拉、開關控制項與選用時機；登入與新增任務表單的錯誤／修正狀態 |
| A7 | 把任務做成會增高、可增刪的清單 | 完整Row父子層級、清單增刪與空狀態，並建立真實Detail畫面供原型串接 |
| A8 | 設計能讓人知道下一步的回饋、彈窗與導覽 | 依情境選擇回饋，建立能包子層的Dialog與Actions，設計Nav選中規則 |
| B1 | 把需求變成流程與線框 | 從訪談整理需求摘要與範圍，推出畫面清單，在設計檔畫含錯誤分支的流程圖，再畫線框並指定Prototype入口 |
| B2 | 連好登入、清單、詳情與返回 | 建立同檔多步基本Flow，檢查熱區、目的地與返回，分辨方案限制及故障 |
| B3 | 用轉場說明畫面去向，再做一段 Smart Animate | 依用途選轉場與引數，製作同名同層級的前後狀態並診斷Smart Animate配對 |
| B4 | 讓確認彈窗能開啟、取消、確認與交換 | 完整Overlay開關／確認、可取消規則與在已開彈層內Swap的實際路徑 |
| B5 | 讓長清單能捲動，導覽與漂浮按鈕不擋內容 | 建立視窗／長內容關係，實測Vertical、Fixed、Sticky及遮擋，在完整Flow使用長列表 |
| B6 | 用任務測試找出問題，修正後再測一次 | 以任務卡、隔開再測與走查清單單人完成測試，記錄問題、修正並回歸；測試與修正一路做出的自選題目App |
| B7 | 把設計整理成能重開、能量測的交付包 | 免費Design量測／Figma輸出、真實PSD操作與透明PNG，以及可重開的完整handoff |
| B8 | 把設計做成網站，留下版本與公開網址 | 從完整可執行程式理解與修改網站，實作獨立Git基準／差異／遠端與公開部署更新 |

## 2026-11-02 改寫

依 `_規範/講義改寫SOP.md` 重寫16頁學員正文（`courses/uiux-designer/_review/2026-11-02/`）：每頁統一骨架、規格值集中規格表、跨頁以內容稱呼；介面名稱依2026-11-02官方文件裁定；新增「練習線」——每堂以 `assets/shared/SIGNUP-DATA.csv` 做報名確認App（360×800），B6整合作品即測試與修正該App；補課綱缺口（輸入框變體、警告／錯誤提示、Bottom sheet、工具分工）；全課單人可完成。

第二輪擴充（同日，依三位獨立審查員建議）：練習線改為學員自選題目（預約／點餐／會員，`assets/shared/practice/`，含訪談紀錄與12筆資料）；補Variables（顏色與4／8間距）、Constraints與Min／Max／Wrap響應式、元件區與巢狀圖示、按鈕State與Show icon／Icon屬性、表單控制項、圖片填色與載入狀態、頂部標題列與觸控尺寸、B1需求訪談→需求摘要→畫面清單→流程圖、元件Hover／Pressed互動、成功提示After delay自動關閉、B6測試計畫與10條走查、B7標註元件／2x與SVG／作品集頁；Git安裝與GitHub註冊移至課前準備，B8自動產生資料改選做。紀錄：`courses/uiux-designer/_review/2026-11-02/改寫規格書-round2.md`。

第三輪修正（同日，依審查員 D 前五項）：B2 加三題關鍵畫面（預約時段選擇含長服務佔多時段、點餐數量與徽章、會員點數餘額與紀錄）與「串成完整流程」；文字樣式改 5 種並統一 Noto Sans TC、Disabled 拆兩變數、文字欄與任務列與提示元件化；A6 控制項規格表、多行欄、必填與 B2 表單互動；需求初稿前移到 A1、B1 改為深化並補缺頁；B6 加三份虛構觀察紀錄（`assets/B6-prototype-task-test/reference/OBSERVATIONS.html`）、六小時排程與檢查方法；評分表加兩項「解決需求」。時數帳本 A2 300 分、A6 420 分。紀錄：`改寫規格書-round3.md`。

## 學習與環境邊界

Starter同檔可有多個基本互動；同一trigger堆疊多actions與條件邏輯才是付費範圍。本課不用。免費主線從Design面板量測與Export，不要求Dev Mode。Photoshop需要授權工作站；GitHub Pages需要自己的帳號、公開示範repo與管理權限。

核心作品包含Login→List Long→Detail→Confirm取消／確認→List Done與Toast；有T02、空狀態、Swap、Smart Animate、Sticky、Horizontal分支。B6在360×800新情境驗收整合能力。B7交出Figma／PSD來源、輸出、規格與測試；B8提供完整下載專案、程式說明、Git基準／更新與公開網址。

公開網址、Starter實際編輯全路徑、Photoshop桌面操作与真人跟做需實際證據，本次無證據者保留PENDING，不沿用舊Probe推論。修訂證據見courses/uiux-designer/_validation/evidence.json與本輪修復報告。
