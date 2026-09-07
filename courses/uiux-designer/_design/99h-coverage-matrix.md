---
course: uiux-designer
status: GATE0_PASS
source_date: 2026-09-07
official_hours: 42h + 57h = 99h
gate0_approved_at: 2026-09-07
---

# UI/UX 99h 正式內容 Coverage Matrix

本文件只做「正式課綱項目 → 教學候選位置 → 可驗收完成物」對照，不做分鐘分配、不宣告任何單元已完成，也不把 ChatGPT 建議自動升格為行政必修。

## 來源角色

| 來源 | 角色 | 控制內容 |
|---|---|---|
| `/Users/paichenwei/Downloads/1788509783989.jpg` | 正式授課課綱 | 課程 9「介面元素與設計」、42h、12 個明列項目 |
| `/Users/paichenwei/Downloads/1788509797593.jpg` | 正式授課課綱 | 課程 6「UI/UX 原型製作與資料打包」、57h、9 組明列主題 |
| `pasted-text.txt`（ChatGPT 交接記錄） | 教學重組提案 | 16-stage 依賴、工具治理、教學節奏與成果鏈；若未在圖片中出現，標為候選／待核准 |
| `uiux-designer/_design/2026-09-07-99h-course-rescope-design.md` | 已核准的本專案設計邊界 | 42h／57h 分工原則、單元契約與 Gate 順序 |

## A. 課程 9：介面元素與設計（42h）

| ID | 正式授課項目 | 候選 Stage | 候選首次教學單元 | 可驗收完成物 | 後續重用位置 | 邊界說明 |
|---|---|---|---|---|---|---|
| 42-01 | 色彩系統 | Stage 2 Visual Foundation | 色彩角色、層級與狀態 | 色彩 token 表與一組可套用介面樣式 | Stage 8 頁面組成、Stage 13 Handoff | 不把個人偏好當成驗收；須有用途與對比判斷 |
| 42-02 | 字型系統 | Stage 2 Visual Foundation | 字級、行高、字重與資訊層級 | Typography scale 與文字樣式表 | Stage 8 頁面組成、Stage 13 Handoff | 須驗證長文字，不只展示短標題 |
| 42-03 | 格線系統 | Stage 3 Layout System | 欄、間距、安全邊界與版面基準 | 桌機／手機格線規格與套用畫面 | Stage 8 頁面組成、Stage 14 Web Foundation | 格線是版面規則，不與單一畫面描圖重複計時 |
| 42-04 | Auto Layout | Stage 3 Layout System | horizontal／vertical、padding、gap、Hug／Fill | 可承受長文字與項目增刪的手機畫面 | Stage 8 頁面組成、Stage 12 Prototype Test | 以內容壓力測試驗收，不以點選功能數量計時 |
| 42-05 | 元件／Component | Stage 4 Component Foundation | 重複介面抽象、主元件與 Instance | 一組可重用主元件與至少一個 Instance | Stage 5–8、Stage 9 Prototype | 首次建立元件；互動使用留給 57h |
| 42-06 | 按鈕／Button | Stage 6 Core UI Components | 目的、層級、尺寸、狀態與文字長度 | Button 元件與狀態矩陣 | Stage 8 頁面、Stage 9 觸發 | 42h 教外觀與狀態；57h 才教互動觸發 |
| 42-07 | 表單／Form | Stage 6 Core UI Components | Label、Input、錯誤、必填與回饋位置 | 可輸入、錯誤與修正狀態的表單組 | Stage 8 頁面、Stage 12 測試 | 不承諾後端驗證；只驗介面狀態與任務可理解性 |
| 42-08 | 列表／List | Stage 6 Core UI Components | 項目結構、密度、增刪與空狀態 | 可增刪、空狀態與長文字的列表元件 | Stage 8 頁面、Stage 10 Scroll | 列表內容變化是 Auto Layout／元件遷移的驗收材料 |
| 42-09 | 回饋與通知／Toast | Stage 7 Navigation & Feedback | 成功、警告、錯誤與出現時機 | Toast 狀態規格與使用範例 | Stage 9 Prototype feedback、Stage 12 測試 | 42h 教回饋設計；57h 才連到任務流程 |
| 42-10 | 彈跳視窗／Dialog | Stage 7 Navigation & Feedback | 目的、內容層級、關閉與背景阻擋 | Dialog 元件、狀態與關閉規則 | Stage 10 Overlay | 42h 教元件結構；Overlay 行為歸 57h |
| 42-11 | 導航選單／Navigation | Stage 7 Navigation & Feedback | 位置、層級、目前頁與手機差異 | 導航元件與桌機／手機規則 | Stage 8 頁面、Stage 10 Scroll | 42h 教視覺與資訊結構；57h 教置頂／滾動行為 |
| 42-12 | 變體／Variants | Stage 5 Component System | 狀態命名、屬性、切換與 Instance 同步 | Button／Input／Navigation 至少一組 Variants 與狀態表 | Stage 9 Change to／Swap、Stage 13 Handoff | 不以 Detach 解決設計問題；須保留 Instance 關係 |

## B. 課程 6：UI/UX 原型製作與資料打包（57h）

| ID | 正式授課項目 | 候選 Stage | 候選首次教學單元 | 可驗收完成物 | 後續重用位置 | 邊界說明 |
|---|---|---|---|---|---|---|
| 57-01 | 線框圖、原型、工具介紹、手機介面、元件與動畫互動的基礎應用 | Stage 0–1、Stage 8–9 | 從任務到畫面清單、手機 Frame、Prototype Flow 與工具分工 | 一條含起點、畫面清單與手機原型入口的任務流程 | Stage 10–12 互動、Stage 13 Handoff | 這是課程 6 的入口與整合基礎；不重教 42h 的元件視覺系統 |
| 57-02 | 觸發事件與互動連結 | Stage 9 Prototype Foundation | Click／Tap、觸發條件、Navigate to、Back | 可依固定任務完成的基本 Flow | Stage 10–12 | 連線數量不等於學習量；必須有任務目的與死路檢查 |
| 57-03 | 常見的互動及轉場效果 | Stage 11 Motion & Advanced Interaction | Instant、Dissolve、Move in／out 與使用目的 | 兩種具目的的轉場與選擇理由 | Stage 12 Prototype Test | 不只展示動畫；須說明速度、方向與任務回饋 |
| 57-04 | 覆蓋層／Overlay 的基礎與進階用法 | Stage 10 Overlay & Scroll Interaction | Dialog、Menu、Bottom sheet、位置、背景與關閉 | 至少兩種 Overlay 模式的任務型原型 | Stage 12 測試、Stage 13 Handoff | 依賴 42-10 的 Dialog 結構；不重複教元件外觀 |
| 57-05 | Swap 搭配 Overlay 技巧 | Stage 10 Overlay & Scroll Interaction | Overlay 內的 Change to／Swap、狀態切換與回復 | 選單／面板／提示的 Swap＋Overlay Flow | Stage 12 測試 | Swap 只在狀態需求成立時使用，不作功能展示 |
| 57-06 | 滾動內容、置頂導覽與漂浮按鈕 | Stage 10 Overlay & Scroll Interaction | Overflow、Scroll with parent、Fixed、Sticky、Ignore auto layout | 長內容頁、橫向列表、固定導覽與漂浮操作 | Stage 12 測試、Stage 14 Web Foundation | 需以不同內容高度與遮擋條件壓力測試 |
| 57-07 | Smart Animation | Stage 11 Motion & Advanced Interaction | Matching layers、名稱／層級、位置、尺寸、透明度、easing | 一個成功 Smart Animate 與一份失敗修復紀錄 | Stage 12 測試、Stage 13 Handoff | 先診斷匹配失敗，再談動畫效果 |
| 57-08 | Figma 與 PS 發布規劃、Figma 與 PS 輸出 | Stage 13 Asset & Handoff | 格式、倍率、透明背景、命名、版本與交付清單 | 可由另一人取用的 Asset／Handoff package | Stage 14 Web Foundation、Stage 15 Deploy | Photoshop 是發布／輸出工具脈絡，不代表 42h Photoshop 專修課 |
| 57-09 | 網頁設計入門與雲端部署 | Stage 14–15 Delivery & Web | HTML／CSS、相對路徑、手機寬度、發布與部署驗收 | 可公開開啟的單頁網站、原始檔與部署紀錄 | Stage 5 整合專題 | 圖片明列網頁入門與雲端部署；Git／GitHub／基礎 JS 仍標為教學方案候選 |

## C. 重疊與首次教學邊界

| 主題 | 42h 首次教學 | 57h 後續重用 | 不重複計時的規則 |
|---|---|---|---|
| Component／Variants | 建立結構、狀態、屬性與 Instance 同步 | 在 Prototype 中 Change to／Swap 並驗證任務流程 | 互動行為是新能力；不得重教元件外觀 |
| 手機介面 | 格線、Auto Layout、長文字與項目增刪 | 將手機畫面接成可操作 Flow，加入滾動／固定元素 | 版面伸縮與互動行為分開記錄 |
| Dialog／Navigation | 視覺結構、資訊層級與狀態 | Overlay、置頂、關閉與返回路徑 | 結構與行為分開計時 |
| Photoshop | 目前圖片只明列 Figma／PS 發布與輸出 | 依交付規格輸出與打包 | 不建立獨立 42h Photoshop Part |
| 網頁 | 圖片未將 HTML／CSS／JS 分拆為行政課名 | 57h 網頁入門與雲端部署 | HTML／CSS／JS 的細分須服務 57h 的完成物 |

## D. ChatGPT 交接文字的候選項目

下列內容對課程設計有幫助，但不是兩張圖片直接列出的行政項目；在 Gate 1 前只能標示為候選，不得直接當成正式必修：

| 候選項目 | 可採用的原因 | 必須防止的漂移 |
|---|---|---|
| 16-stage 依賴 | 能把元件、原型、Handoff 與 Web 排出前後關係 | 不把 16 stages 誤當成 16 個行政課程 |
| Concept → Follow Along → Guided Practice → Independent Challenge | 適合接近零基礎學員逐步完成 | 每個階段仍須有真實新能力，不以活動名稱灌時數 |
| VS Code、Chrome | 支援 HTML／CSS、手機檢查與部署 | 不能脫離 57h 網頁與部署成果獨立擴張 |
| 基礎 JavaScript | 只保留完成最小網頁成果所需的能力 | 圖片未明列；不得擴張成程式設計課，分鐘必須服務 57h 網頁／部署完成物 |
| Git／GitHub | 納入 57h 的必要版本與交付流程 | 圖片未明列，但使用者已核准為必要流程；不得擴張成獨立 Git 課程 |
| Design System、Prototype、網站、部署整合成果鏈 | 能把兩門課串成可展示的產出 | 每個成果都要回溯正式項目與 99h 時間帳本 |

## E. Gate 0 結論（使用者已核准）

### 已確認

- 42h 正式課程的 12 個明列項目全部有候選首次教學位置。
- 57h 正式課程的 9 組明列主題全部有候選首次教學位置。
- Component、手機介面、Dialog、Navigation、Photoshop 輸出與網頁內容已建立首次教學／後續重用邊界。
- 舊 Photoshop 42h 未被列入正式 coverage。

### 使用者決策（2026-09-07）

- Git／GitHub：必要流程，納入 57h 的版本與交付驗收。
- 基礎 JavaScript：維持最小路徑，只教完成網頁成果所需的能力。
- 16-stage：作為依賴參考，不硬性一對一切成 16 個單元；改依正式課程內容、能力邊界與完成物切分。

### 放行限制

本文件已通過使用者 Gate 0。下一步建立 `99h-time-ledger.md` 與 `../_outlines/uiux-designer.md` 草稿；仍不製作教案或 HTML。
