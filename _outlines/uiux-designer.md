---
slug: uiux-designer
name: 介面元素與設計 × UI/UX 原型製作與資料打包
color: "#c9963a"
audience: 接近零基礎、需要從介面設計一路完成原型、交付包與基礎網站部署的成人學員
institution: 弄一下工作室
duration: 99h
tools: Figma, Adobe Photoshop, VS Code, Chrome, HTML, CSS, 基礎 JavaScript, Git, GitHub, 雲端部署平台
prac: true
course_type: skill-operation
pilot: false
platform_version: Figma、Adobe Photoshop、VS Code、Chrome 與部署平台版本須於各單元 G2 依官方來源查證
source_images: /Users/paichenwei/Downloads/1788509783989.jpg, /Users/paichenwei/Downloads/1788509797593.jpg
governing_matrix: courses/uiux-designer/_design/99h-coverage-matrix.md
time_ledger: courses/uiux-designer/_design/99h-time-ledger.md
g1_status: DRAFT_GATE1
---

# 介面元素與設計 × UI/UX 原型製作與資料打包｜99h 大綱草稿

**狀態**：Gate 0 已通過；本檔為 Gate 1 草稿，尚未鎖定正式時數，也尚未進入教案或 HTML 製作。  
**行政基準**：課程 9「介面元素與設計」42h＋課程 6「UI/UX 原型製作與資料打包」57h。  
**切分原則**：依內容邊界、首次能力與可驗收完成物切單元，不將 ChatGPT 的 16-stage 硬性一對一映射成 16 個行政單元。

## 課程定位（Positioning）

為接近零基礎的學員建立一條可驗收的數位介面產出鏈：先完成色彩、字型、格線、Auto Layout 與元件系統，再把手機介面組成可真跑的互動原型，完成測試修正、Figma／Photoshop 資料打包、基礎網站、Git/GitHub 版本紀錄與雲端部署。

本課程不是完整 UX 研究、品牌識別、前端工程或後端開發課；只涵蓋兩張正式課綱圖片明列的介面元素、UI/UX 原型、資料打包、網頁入門與雲端部署。基礎 JavaScript 僅保留完成最小網頁成果所需的範圍。

## 受眾畫像（Audience Profile）

- **職業／情境**：希望建立數位設計、行銷視覺、UI 原型或基礎網頁作品的成人學員。
- **技術底子**：能操作一般電腦與瀏覽器；不預設 Figma、Photoshop、HTML、Git 或 GitHub 經驗。
- **現有工具棧**：一般電腦、瀏覽器、可使用的 Figma／Adobe Photoshop、VS Code 與 GitHub 帳號。
- **痛點 3 條**：
  1. 能看出畫面好不好看，卻無法建立一致的色彩、字型、格線與元件規則。
  2. 會建立靜態畫面，卻不知道如何讓觸發、Overlay、滾動與轉場服務任務流程。
  3. 無法把 Figma／Photoshop 素材、版本、網頁原始檔與部署成果整理成可交付的完整包。

## Brand Brief（品牌調性）

- **tone_register**：技術友善
- **mood_keywords**：扎實、清楚、可驗證
- **differentiation**：不把工具功能清單當作課程，而是用一條可測試、可交付、可部署的設計產出鏈串起兩門行政課程。

## 學習成果（Outcomes）

1. **建立**可套用的色彩、字型、格線與 Auto Layout 規則，並以長文字、項目增刪與手機寬度變化驗證版面。
2. **製作並維護** Component、Variants、Properties、Button、Form、List、Toast、Dialog 與 Navigation，讓主元件修改能同步 Instances。
3. **組成並說明**一條從線框、畫面清單到手機介面與 Prototype Flow 的任務路徑。
4. **製作並修正**包含觸發、轉場、Overlay、Swap、滾動、置頂、漂浮按鈕與 Smart Animation 的互動原型。
5. **執行並記錄**固定任務測試，依錯誤分類修正原型，留下可回溯的測試紀錄與版本差異。
6. **整理並交付** Figma／Photoshop 素材、Handoff 清單、基礎 HTML/CSS／最小 JavaScript 網站、Git/GitHub 版本紀錄與可公開開啟的雲端部署成果。

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  A1: []
  A2: [A1]
  A3: [A2]
  A4: [A3]
  A5: [A4]
  A6: [A5]
  A7: [A6]
  A8: [A5, A6, A7]
  B1: []
  B2: [B1, A4]
  B3: [B2]
  B4: [A8, B2]
  B5: [A3, A8, B2]
  B6: [B2, B3, B4, B5]
  B7: [B3, B6]
  B8: [A3, B6, B7]
```

## 試跑包交付規格（Verification Assets）

每個單元 G2 必須提供：

- 可直接開始的來源檔、Figma 起始檔或 HTML 起始專案，不把找檔當成核心學習。
- 講師短示範材料、學員起始材料、完成參考、錯誤狀態與修復提示。
- 固定任務腳本、預期畫面／檔案狀態、Checkpoint 與 Acceptance criteria。
- Figma 單元提供 Frame、Component、Variant 或 Prototype 的可檢查起始狀態。
- Photoshop／輸出單元提供可追蹤素材、格式／倍率規格與 Handoff 清單。
- Web／Git／部署單元提供可重建 HTML/CSS、最小 JavaScript、相對路徑、Git/GitHub 操作紀錄與乾淨環境驗收。

## 單元矩陣

### Part A：介面元素與設計（42h）

| Unit | 單元標題 | 學習目標 | 預估時數 |
|---|---|---|---:|
| A1 | 視覺基礎：色彩與字型 | 建立色彩角色、Typography scale 與長文字驗證規則 | 5h |
| A2 | 格線與版面基準 | 建立桌機／手機格線、欄、間距與安全邊界 | 6h |
| A3 | Auto Layout 與內容壓力 | 讓手機介面通過長文字、增刪項目與寬度變化 | 6h |
| A4 | Component 基礎與 Instance | 從重複畫面抽取可維護的主元件與 Instances | 5h |
| A5 | Variants、Properties 與狀態 | 建立狀態、屬性與不使用 Detach 的同步規則 | 6h |
| A6 | Button 與 Form | 建立按鈕層級、表單輸入、錯誤與修正狀態 | 6h |
| A7 | List 與內容變化 | 建立列表、空狀態、長文字與增刪規則 | 4h |
| A8 | Toast、Dialog 與 Navigation | 建立回饋、彈窗與導航元件的視覺／狀態規則 | 4h |
| **Part A 合計** |  |  | **42h** |

### Part B：UI/UX 原型製作與資料打包（57h）

| Unit | 單元標題 | 學習目標 | 預估時數 |
|---|---|---|---:|
| B1 | 線框、原型、工具與手機介面入口 | 將任務轉成畫面清單、手機 Frame 與 Prototype 入口 | 7h |
| B2 | 觸發事件與互動連結 | 建立 Click／Tap、Navigate to、Back 與無死路 Flow | 6h |
| B3 | 常見轉場與動效目的 | 依任務目的選擇轉場並說明速度、方向與回饋 | 6h |
| B4 | Overlay 與 Swap | 製作 Dialog、Menu、Bottom sheet 與狀態切換 | 7h |
| B5 | 滾動、置頂導覽與漂浮按鈕 | 處理 Overflow、Fixed、Sticky、遮擋與不同內容高度 | 6h |
| B6 | Prototype 任務測試與修正 | 依固定腳本記錄問題、修正並回歸測試 | 6h |
| B7 | Smart Animation、Figma／PS 發布與輸出 | 修復 matching layers 並整理格式、倍率、版本與交付包 | 6h |
| B8 | 網頁入門、Git/GitHub 與雲端部署 | 以最小 HTML/CSS／JavaScript 路徑完成版本化與公開部署 | 13h |
| **Part B 合計** |  |  | **57h** |

## 時數與版本狀態

- 詳細分鐘帳本：`courses/uiux-designer/_design/99h-time-ledger.md`
- 42h／57h／99h 目前為設計回算，需在代表單元試跑後再鎖定。
- Git/GitHub 是必要交付流程；JavaScript 維持最小路徑。
- 單元可因真實教學證據合併或重配，但不得漏掉正式課綱項目或增加總時數。
