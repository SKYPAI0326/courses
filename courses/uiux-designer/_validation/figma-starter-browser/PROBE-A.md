# Probe A：介面系統與內容壓力

**課程**：`uiux-designer`  
**Run ID**：`20260916-figma-starter-browser-001`  
**測試日期**：2026-09-16  
**工具**：Google Chrome（Figma 網頁版）  
**方案**：Figma Starter／Free  
**工作檔**：`Codex Figma Starter Audit - Probe A`  
**工作檔 URL**：`https://www.figma.com/design/tSpQYGtYKwGLT9YtIFk9uC/Codex-Figma-Starter-Audit---Probe-A?node-id=1-15&t=dayHaBLEXHGo96a6-0`  
**整體判定**：`CONDITIONAL`（核心介面操作已通過；完整 Form／List 行為與跨狀態版面仍待 Probe A 補測）

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

## 已驗證的核心能力

- Frame 尺寸、命名與手機畫板骨架可在 Starter／Free 瀏覽器版完成。
- Auto Layout、Component、Variant、Instance 的建立與狀態切換可完成。
- 長中文內容可在固定寬度下換行，並以 Auto height 讓容器隨內容增高。
- Assets 可以從同一個檔案找到並插入自建 component。
- 以 Layers 命名建立 `Button / Primary`、`List / Error helper` 等可教學的結構化命名。

## 失敗、限制與修復路徑

### 1. Variant 名稱不是任意標籤

第一次把 variant 命名成 `Error` 時，Figma 顯示名稱格式警告。可靠教法是保留 Figma 自動建立的 property，從右側 `Property 1` 管理 `Login Heading`／`Error` 值；不要把「顯示在 Layers 的名稱」當成完整 property 語法。課程必須提供一次錯誤示範與修復檢查。

### 2. 文字輸入應優先走右側 Content

直接對畫布上的 `[contenteditable]` 輸入或重填，可能因焦點仍在舊文字層而產生重複字串。實際修復方式是選取文字層，再使用右側 `Content` textarea 重新填入，最後以畫布換行與右側文字內容雙重確認。這個失敗案例應寫入講義的「卡住時怎麼修」段落。

### 3. Instance 的主版面控制是唯讀狀態

插入 instance 後，Auto Layout 控制顯示 disabled；這不是測試失敗，而是主元件／instance 的責任邊界。課程應明確教「回主元件修改，再觀察 instance 同步」，避免學員誤以為免費方案壞掉。

### 4. Button 目前只驗證視覺模式

本輪在既有 component variant 內建立 `280 × 48` Rectangle，驗證按鈕尺寸與結構命名；尚未完成獨立 Button component、Form 欄位行為、List 增刪與多列 Auto Layout 壓力。這些功能不能在正式教案中宣稱已通過。

## 尚待補測

- Form：輸入欄、label、錯誤提示、長錯誤訊息的多欄位排列。
- List：多列資料、增刪一列、空狀態／錯誤狀態之間的版面穩定性。
- Dialog、Toast、Navigation 與 Prototype 觸發；移至 Probe B 的互動測試。
- 匯出、分享權限、Inspect、Git/GitHub 與公開部署；移至 Probe C。

## Probe A 結論

Probe A 不阻擋後續課程設計，但目前只能放行「Frame → Auto Layout → Component／Variant／Instance → 長中文內容」核心路徑。Button、Form、List 仍以限定情境處理，直到補測完成前，G1 維持 `G1_BLOCKED_BY_FIGMA_VALIDATION`，不鎖定正式時數與完整講義。

