---
course: uiux-designer
status: DRAFT_GATE1
part_a_hours: 42h
part_b_hours: 57h
total_hours: 99h
---

# UI/UX 99h 時間帳本草稿

本帳本依使用者決策，以正式內容與能力邊界切分單元，不把 16-stage 硬切成 16 個行政單元。分鐘是設計回算，尚未經真人授課鎖定；若試跑不足，回到 Gate 1 重配，不以重複操作補時。

## 計時欄位

- `concept`：概念、用途、判斷規則與錯誤辨識。
- `micro_demo`：講師短示範；必須能立即跟做。
- `follow_along`：學員依明確路徑完成第一次操作。
- `guided_practice`：有材料與限制，但學員需依規則作選擇或修正。
- `independent`：新材料、新限制或新任務的獨立遷移。
- `check_debug`：Checkpoint、錯誤診斷、修復與回歸驗收。

主要直接動手最低定義為 `follow_along + guided_practice + independent + check_debug`；找檔、登入、下載、保存、等待與設備排錯不計入主要直接動手。

## Part A：介面元素與設計（42h）

| Unit | 內容邊界 | 對應正式項目 | 候選能力區段 | concept | micro_demo | follow_along | guided_practice | independent | check_debug | 合計 | 主要完成物 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| A1 | 視覺基礎：色彩與字型 | 42-01、42-02 | Stage 2 Visual Foundation | 45 | 30 | 75 | 60 | 60 | 30 | 300 | 色彩 token 表、Typography scale、長文字檢查 |
| A2 | 格線與版面基準 | 42-03 | Stage 3 Layout System | 50 | 40 | 90 | 80 | 65 | 35 | 360 | 桌機／手機格線規格與套用畫面 |
| A3 | Auto Layout 與內容壓力 | 42-04 | Stage 3 Layout System | 50 | 40 | 85 | 80 | 70 | 35 | 360 | 可承受長文字、增刪項目與寬度變化的手機畫面 |
| A4 | Component 基礎與 Instance | 42-05 | Stage 4 Component Foundation | 40 | 35 | 75 | 65 | 55 | 30 | 300 | 一組主元件與可辨識的 Instances |
| A5 | Variants、Properties 與狀態 | 42-12 | Stage 5 Component System | 50 | 45 | 85 | 80 | 65 | 35 | 360 | 元件狀態矩陣、Variants 與同步驗收 |
| A6 | Button 與 Form | 42-06、42-07 | Stage 6 Core UI Components | 45 | 40 | 85 | 80 | 75 | 35 | 360 | Button／Form 元件、錯誤與修正狀態 |
| A7 | List 與內容變化 | 42-08 | Stage 6 Core UI Components | 30 | 25 | 55 | 55 | 50 | 25 | 240 | 可增刪、空狀態與長文字列表 |
| A8 | Toast、Dialog 與 Navigation | 42-09、42-10、42-11 | Stage 7 Navigation & Feedback | 30 | 25 | 55 | 55 | 50 | 25 | 240 | 回饋、彈窗、導航元件與桌機／手機規則 |
| **Part A subtotal** |  | **12 項** |  | **340** | **280** | **605** | **555** | **490** | **250** | **2520＝42h** |  |

## Part B：UI/UX 原型製作與資料打包（57h）

| Unit | 內容邊界 | 對應正式項目 | 候選能力區段 | concept | micro_demo | follow_along | guided_practice | independent | check_debug | 合計 | 主要完成物 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| B1 | 線框、原型、工具與手機介面入口 | 57-01 | Stage 0–1、Stage 8–9 | 60 | 45 | 110 | 90 | 75 | 40 | 420 | 任務流程、畫面清單、手機 Frame 與 Prototype 入口 |
| B2 | 觸發事件與互動連結 | 57-02 | Stage 9 Prototype Foundation | 45 | 40 | 90 | 75 | 75 | 35 | 360 | 可依固定任務完成的基本 Flow |
| B3 | 常見轉場與動效目的 | 57-03 | Stage 11 Motion & Advanced Interaction | 45 | 40 | 85 | 75 | 80 | 35 | 360 | 兩種有目的的轉場與選擇理由 |
| B4 | Overlay 與 Swap | 57-04、57-05 | Stage 10 Overlay & Scroll Interaction | 55 | 45 | 105 | 90 | 80 | 45 | 420 | Overlay、Change to／Swap 任務型原型 |
| B5 | 滾動、置頂導覽與漂浮按鈕 | 57-06 | Stage 10 Overlay & Scroll Interaction | 45 | 40 | 85 | 75 | 80 | 35 | 360 | 長內容、橫向列表、固定導覽與漂浮操作 |
| B6 | Prototype 任務測試與修正 | 57-01、57-02、57-03、57-06、57-07 的整合支援 | Stage 12 Prototype Test & Revision | 45 | 35 | 70 | 80 | 90 | 40 | 360 | 測試腳本、錯誤清單、修正版與回歸紀錄 |
| B7 | Smart Animation、Figma／PS 發布與輸出 | 57-07、57-08 | Stage 11、Stage 13 Asset & Handoff | 45 | 40 | 80 | 75 | 80 | 40 | 360 | Smart Animate 修復紀錄與 Asset／Handoff package |
| B8 | 網頁入門、Git/GitHub 與雲端部署 | 57-09 | Stage 14–15 Delivery & Web | 90 | 60 | 180 | 150 | 190 | 110 | 780 | HTML/CSS 最小網站、必要 JavaScript、Git/GitHub 紀錄與公開部署 |
| **Part B subtotal** |  | **9 組** |  | **430** | **345** | **805** | **710** | **750** | **380** | **3420＝57h** |  |

## 加總驗證

| 範圍 | 小時 | 分鐘 | 結果 |
|---|---:|---:|---|
| Part A：介面元素與設計 | 42h | 2520 | PASS（設計回算） |
| Part B：UI/UX 原型製作與資料打包 | 57h | 3420 | PASS（設計回算） |
| 全課 | 99h | 5940 | PASS（設計回算） |

## 能力與重複控制

- A4／A5 首次建立元件、Variants、Properties 與狀態；B2／B4 只使用它們完成互動，不重教元件外觀。
- A2／A3 首次建立格線與 Auto Layout；B5 將已完成手機介面遷移到滾動、固定與漂浮限制，不重播版面教學。
- A8 首次建立 Dialog／Navigation 的視覺結構與規則；B4／B5 教 Overlay、置頂與返回行為。
- B6 是正式課綱「原型應用」的品質驗收支援，不宣稱圖片另列一門測試課程。
- B8 的 Git/GitHub 是使用者已核准的必要交付流程；JavaScript 僅保留完成最小網頁成果所需的能力。

## Gate 1 尚待驗證

- 每個 Unit 的分鐘仍需在教案設計時拆成可觀察活動，不得只以表格加總放行。
- B8 的 13h 必須以網站、版本紀錄與公開部署的真實完成物支撐，不能由安裝或等待灌入。
- 代表單元需經零基礎試跑後，才能鎖定設計時數。
