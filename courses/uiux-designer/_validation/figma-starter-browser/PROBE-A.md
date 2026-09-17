# Probe A：介面系統與內容壓力

**課程**：`uiux-designer`  
**Run ID**：`20260916-figma-starter-browser-001`  
**測試日期**：2026-09-16  
**工具**：Google Chrome（Figma 網頁版）  
**方案**：Figma Starter／Free  
**工作檔**：`Codex Figma Starter Audit - Probe A`  
**工作檔 URL**：`https://www.figma.com/design/tSpQYGtYKwGLT9YtIFk9uC/Codex-Figma-Starter-Audit---Probe-A?node-id=1-15&t=dayHaBLEXHGo96a6-0`  
**整體判定**：`CONDITIONAL`（核心介面操作已通過；Form 互動、List 動態增刪與跨狀態版面仍待補測）

## 測試目的

確認零基礎學員在免費瀏覽器方案中，能否從空白檔建立手機介面骨架，並完成可重用的 Component、Variant、Instance、長中文內容與按鈕／錯誤輔助列。每個結果都以實際 Figma 畫面或面板狀態為依據；尚未測到的功能保留為待測，不由敘事推定可用。

## 實測步驟與結果

| Step | 操作 | 實際觀察 | 判定 |
|---|---|---|---|
| T1-S1 | 完成登入與首次開通；在使用者確認後填入顯示名稱 `Codex Figma Test` | 進入 Figma workspace；此步會修改帳號顯示名稱，已取得使用者確認 | `MACHINE_PASS` |
| T1-S2 | 以 Starter 選項完成 onboarding | 工作區與檔案頁顯示 `Free`；左側顯示 `2 free pages left`，確認不是付費專業方案 | `MACHINE_PASS` |
| A-01 | 使用 Frame 工具建立畫板，再將 Width 設為 `402`、Height 設為 `874` | 右側尺寸欄接受數值並更新畫板 | `MACHINE_PASS` |
| A-02 | 將 Frame 命名為 `Mobile / Login & List` | Layers 中可看到可讀、可分組的命名 | `MACHINE_PASS` |
| A-03 | 在 Frame 上開啟 Auto layout | 右側 `Toggle auto layout` 顯示已勾選，方向為 Vertical；尺寸維持可辨識的固定值 | `MACHINE_PASS` |
| A-04 | 建立文字 `登入`，以 `Shift+A` 將文字包成 Auto Layout | 畫布及 Layers 可看到文字被包在自動排版容器中 | `MACHINE_PASS` |
| A-05 | 對 Auto Layout 容器執行 `Create component` | Assets 顯示 `Created in this file 1 component`；右側出現 component 設定 | `MACHINE_PASS` |
| A-06 | 執行 `Add variant`，將第二個狀態命名為 `Error` | 直接以單一詞命名時出現「variant names must be of the form Prop=Value」警告；重新選取後，右側 Property 1 的值顯示 `Error`，警告消失 | `MACHINE_PASS_WITH_REPAIR` |
| A-07 | 從 Assets 開啟本檔 component 詳情並執行 `Insert instance`；在 `Property 1` 切換狀態 | 可插入 instance；combobox 提供 `Login Heading` 與 `Error`，切換後顯示 `Error`。Instance 的 Auto Layout 主版面控制呈 disabled，符合 instance 受主元件控制的限制 | `MACHINE_PASS` |
| A-08 | 在文字選取後，以右側 `Content` textarea 輸入長中文；選 `Auto height`，將水平固定寬度設為 `200` | 長字串在畫布中換行，垂直高度變為 Hug（觀察到 H=`30`）；內容可重開確認 | `MACHINE_PASS_WITH_REPAIR` |
| A-09 | 在 component variant 內建立 Rectangle，設定 `280 × 48`，命名 `Button / Primary` | 看到矩形按鈕視覺模式；其所在 component variant 內可被保留和重用。因為已在 component set 內，右側不再提供獨立 Create component，故本步只作視覺按鈕模式，不宣稱獨立 Button component API | `CONDITIONAL` |
| A-10 | 複製長中文文字層，命名 `List / Error helper` | Layers 中出現第二個可辨識的錯誤／清單輔助列，作為空狀態與錯誤狀態後續補測的基礎 | `MACHINE_PASS` |
| A-11 | 在 Design 面板開啟 Typography styles，建立 `A1/type-test` 並套用到目前文字層 | Starter／Free 顯示 `Create new text style`、名稱欄與 `Create style`；完成後 Typography 面板可讀到 `A1/type-test · 12/Auto` | `MACHINE_PASS` |
| A-12 | 在 Fill 面板開啟 `New style or variable`，建立 `A1/color-test` | Starter／Free 顯示 Style／Variable 選擇與 `Create style`；完成後 Fill 區可讀到 `A1/color-test` | `MACHINE_PASS` |
| A-13 | 選取 `Screen / List` Frame，加入 Layout guide，將類型改為 `Columns`、欄數設為 `4`、Gutter 設為 `16` | Starter／Free 的 Design 面板提供 Layout guide；可在設定浮層切換 Grid／Columns／Rows，Columns 可讀取 Count、Stretch、Offset、Gutter；關閉浮層後仍可回到 Layout guide 設定 | `MACHINE_PASS` |
| A-14 | 將 `Screen / List` Frame 寬度由 `402` 改為 `360`，保留 4 columns Layout guide 與內容 | 右側 Width 顯示 `360`、Height 維持 `874`；畫布上的四欄格線仍存在，`清單畫面` 文字留在 Frame 內，沒有被格線或邊界裁切 | `MACHINE_PASS` |
| A-15 | 建立 `320×48` Rectangle，命名 `Button / Primary`，執行 `Create component`、`Add variant`，把 `Property 1` 的第二個 Value 改為 `Disabled` | Starter／Free 顯示 `Button` component set，右側可看到 `Add variant`、`Properties`，Layers 可讀到 `Primary` 與 `Disabled` 兩個狀態 | `MACHINE_PASS` |
| A-16 | 在同一個畫面建立 `Form / Email / Label` 文字層與 `Form / Email / Input` 矩形層 | Layers 同時顯示 Label 與 Input 的結構化名稱；這證明表單的視覺分組可建立，尚未測試真實輸入互動或多欄位行為 | `MACHINE_PASS_PARTIAL` |
| A-17 | 在 `Screen / List` 內建立 `300×40` Rectangle，命名 `List / Item / Row 01`，複製後命名 `List / Item / Row 02` | Layers 同時顯示兩個清單列；複製動作可留下第二列，沒有把它誤寫成資料庫或互動行為 | `MACHINE_PASS` |
| A-18 | 建立 `List / Item / Title` 長中文文字，切成 Fixed width `180` 與 Auto height | 右側 Width=`180`、Height=`30`；文字換行且圖層名稱可讀，可作為 A7 長文字壓力案例 | `MACHINE_PASS` |
| A-19 | 建立文字 `目前沒有清單項目`，命名 `List / Empty / Message` | Layers 可讀到空狀態提示；此步只證明視覺層可建立，沒有宣稱資料切換或動態顯示已完成 | `MACHINE_PASS_PARTIAL` |
| A-20 | 在 `Screen / Login` 內建立 `260×48` Rectangle，命名 `Toast / Success` | Layers 可讀到 Toast 視覺層；尺寸可在右側讀取，沒有宣稱自動出現或消失 | `MACHINE_PASS_PARTIAL` |
| A-21 | 在同一畫面建立 `260×150` Rectangle，命名 `Dialog / Confirm` | Layers 可讀到 Dialog 視覺層；此步只證明內容容器，不包含 Overlay 開關或關閉行為 | `MACHINE_PASS_PARTIAL` |
| A-22 | 建立文字 `首頁    清單    設定`，命名 `Navigation / Header` | Layers 可讀到 Navigation 視覺層；目前只測位置與文字結構，沒有測試置頂、滾動或 Prototype 連結 | `MACHINE_PASS_PARTIAL` |

## 已驗證的核心能力

- Frame 尺寸、命名與手機畫板骨架可在 Starter／Free 瀏覽器版完成。
- Auto Layout、Component、Variant、Instance 的建立與狀態切換可完成。
- 長中文內容可在固定寬度下換行，並以 Auto height 讓容器隨內容增高。
- Assets 可以從同一個檔案找到並插入自建 component。
- 以 Layers 命名建立 `Button / Primary`、`List / Error helper` 等可教學的結構化命名。
- Color style 與 Text style 的建立入口及命名流程可在目前 Starter／Free 方案完成；A1 可將色彩角色與文字樣式列入實作主線。
- Layout guide 可在 Starter／Free 的 Frame 上建立；Columns 模式可設定欄數與 Gutter，A2 可把格線基準列入實作主線。此測試只證明面板與設定可用，不代替學員對齊檢查。
- Button 可在 Starter／Free 建立為 component set，並加入第二個 Variant；A6 可教 `Button / Primary`、`Property 1=Disabled` 的視覺狀態。Form 可建立 Label／Input 的結構化圖層，A6 只能把它當成視覺組合，不能宣稱已完成輸入互動。
- List 的兩個視覺列、長中文標題與空狀態提示可在同一個 Frame 建立；A7 可教命名、複製與 Auto height 壓力。動態增刪、真實資料切換與多列聯合滾動仍不在本輪證據內。
- Toast、Dialog、Navigation 的基本視覺層與命名可在 Starter／Free 建立；A8 可教狀態文字、內容容器與導覽位置。出現時機、Overlay、關閉、置頂與 Prototype 連結要在 Part B 測試。

## 失敗、限制與修復路徑

### 1. Variant 名稱不是任意標籤

第一次把 variant 命名成 `Error` 時，Figma 顯示名稱格式警告。可靠教法是保留 Figma 自動建立的 property，從右側 `Property 1` 管理 `Login Heading`／`Error` 值；不要把「顯示在 Layers 的名稱」當成完整 property 語法。課程必須提供一次錯誤示範與修復檢查。

### 2. 文字輸入應優先走右側 Content

直接對畫布上的 `[contenteditable]` 輸入或重填，可能因焦點仍在舊文字層而產生重複字串。實際修復方式是選取文字層，再使用右側 `Content` textarea 重新填入，最後以畫布換行與右側文字內容雙重確認。這個失敗案例應寫入講義的「卡住時怎麼修」段落。

### 3. Instance 的主版面控制是唯讀狀態

插入 instance 後，Auto Layout 控制顯示 disabled；這不是測試失敗，而是主元件／instance 的責任邊界。課程應明確教「回主元件修改，再觀察 instance 同步」，避免學員誤以為免費方案壞掉。

### 4. Button 與 Form 的可教範圍

本輪另外建立 `320 × 48` Rectangle，命名 `Button / Primary`，在元件外執行 `Create component`，再加入第二個 Variant 並設定 `Property 1=Disabled`。因此 A6 可以教獨立 Button component set 與視覺狀態。Form 只建立 `Form / Email / Label` 與 `Form / Email / Input` 的圖層結構；輸入互動、多欄位排列與真實錯誤回饋仍未測到，不能在 A6 宣稱已完成。

## 尚待補測

- Form：輸入互動、錯誤提示與長錯誤訊息的多欄位排列。
- List：目前已補測兩個視覺列、長文字與空狀態圖層；多列 Auto Layout 的動態增刪、資料切換與空／錯誤狀態之間的版面穩定性仍待補測。
- Dialog、Toast、Navigation 的出現時機、Overlay、關閉、置頂與 Prototype 觸發；移至 Probe B 的互動測試。
- 匯出、分享權限、Inspect、Git/GitHub 與公開部署；移至 Probe C。

## Probe A 結論

Probe A 目前放行「Frame → Auto Layout → Component／Variant／Instance → 長中文內容」以及限定範圍的 Button component set、Form／List 視覺圖層與 Toast／Dialog／Navigation 視覺結構。互動、動態資料與其他行為仍待補測；G1 維持 `G1_BLOCKED_BY_FIGMA_VALIDATION`，不把限定測試擴寫成未驗證功能。
