---
slug: uiux-designer
unit_id: A6
title: Button 與 Form
course_type: skill-operation
duration: 6h
learning_objective: 能沿用 A5 的狀態欄位建立 Button component set，加入 Primary 與 Disabled 視覺狀態，並用 Label、Input、Helper 圖層組成一個可檢查的表單區塊，記錄尚未測試的互動邊界。
prerequisites: [A5]
style_guide: _outlines/uiux-designer.style-guide.md
platform_version: Google Chrome；Figma 網頁版 Starter／Free（本堂以 Button component 與 Form 視覺圖層為範圍）
---

<!--
教案 A6 · Button 與 Form

本單元承接 A5 的 Variant property 經驗。學員建立 320×48 的 Button / Primary component，加入 Disabled Value；再以 Form / Email / Label、Input、Helper 的圖層結構整理一個表單區塊。Probe A 的 A-15／A-16 已確認 Button component set 與 Form 視覺分組可在 Starter／Free 建立。

本堂不宣稱輸入互動、多欄位增刪、真實表單驗證或錯誤流程已完成；這些項目要在後續測試 Gate 補測。
-->

## 教學流程（Teaching Flow）

> **課型：skill-operation**。順序：接手成果 → 概念 → 示範 → 同步操作 → 變因練習 → 驗收與交接。
> **本節完成物：** `Button / Primary` component set、`Form / Email` 視覺圖層組、Primary／Disabled 狀態截圖與表單邊界紀錄。

### 破題 / Hook

阿凱已經有 Default／Error 的標題狀態，現在要完成登入區塊的下一個畫面：使用者需要一個可以辨認的主要按鈕，也要看得出輸入欄位、標籤和錯誤輔助文字的關係。按鈕狀態和表單內容若各自命名，下一個人就很難確認哪些圖層可以重用。

這一堂先把可在 Figma 免費版確認的範圍做好：Button 具備 Primary／Disabled 兩個視覺 Value；Form 用固定的 Label、Input、Helper 層級保存結構。輸入互動與多欄位狀態留在未驗證清單，不能用名稱代替證據。

**起始材料：** `courses/uiux-designer/assets/A6-button-form/START-HERE.html`。
**前置成果：** A5 的 component set、Property／Value 截圖與可切換 Instance；缺少時先回 A5。
**交付位置：** 同一個 Figma 檔保留 Button component set、Form 圖層與完成檢查表。

### 概念 / Concepts

#### Button component set

Button component set 保存同一個按鈕的多個視覺狀態。本堂的 Property 使用 Figma 目前預設欄位，Value 是 `Primary` 與 `Disabled`。

#### Button 狀態

Primary 表示主要行動的視覺樣式；Disabled 表示目前不能執行的樣式。這兩個名稱要出現在 Property Value，不靠圖層顏色猜測。

#### Form 圖層結構

Form 的視覺結構由 Label、Input、Helper 組成。Label 說明欄位用途；Input 是輸入區的容器；Helper 放置提醒或錯誤文字。本堂整理圖層與間距，不測試真實輸入事件。

#### 可驗證邊界

畫面上看得到的名稱、尺寸、狀態值與層級可以檢查；按鍵觸發、欄位驗證與多欄位資料流需要 Prototype 或實作測試，不能從靜態圖層推論。

### 示範 / Demo

示範固定 A5 的 Figma 檔，在 `Screen / List Top` Frame 建立 Button 與 Form 的視覺材料。

1. 在 Frame 內畫出 320×48 Rectangle，命名 `Button / Primary`。
2. 選取 Rectangle 執行 `Create component`，確認右側出現 Component 與 Properties。
3. 執行 `Add variant`，將第二個 Value 設為 `Disabled`；保留第一個 Value `Primary`。
4. 在同一個 Frame 建立文字層 `Form / Email / Label`，內容為「電子郵件」。
5. 建立 320×48 矩形層，命名 `Form / Email / Input`；把它放在 Label 下方。
6. 複製一個文字層命名 `Form / Email / Helper`，內容為「請輸入有效的電子郵件」。
7. 截圖 Button 的兩個 Value 與 Form 的三個圖層，並在檢查表標記「互動尚未測試」。

示範完成時，學員能從 Layers 指出 Button component set 的兩個 Value，也能按順序找到 Label、Input、Helper。只看到三個形狀，卻沒有結構化命名，不能算完成。

### 同步操作 / Together

| 步驟 | 學員動作 | 預期結果 | 快速檢查與修復 |
|---|---|---|---|
| 1 | 開啟 A5 檔與 A6 起始材料，選取 `Screen / List Top`。 | Frame 尺寸與 A5 狀態來源可讀。 | 沒有 A5 檔先回 A5，不在 A6 猜測來源。 |
| 2 | 建立 320×48 Rectangle，命名 `Button / Primary`。 | Layers 有可讀的按鈕圖層。 | 尺寸不符時直接讀右側 W/H，不用畫布目測。 |
| 3 | 執行 `Create component`、`Add variant`，設定 `Property 1` 的兩個 Value 為 `Primary`、`Disabled`。 | Layers 有兩個狀態，右側 Properties 可讀。 | Value 出現警告時，回 Property 欄修改，不改 Layers 名稱。 |
| 4 | 建立 `Form / Email / Label` 文字層與 `Form / Email / Input` 矩形層。 | Label 在 Input 上方，兩個名稱可從 Layers 找到。 | 只看到文字時，先建立矩形再重新命名。 |
| 5 | 複製文字層為 `Form / Email / Helper`，輸入指定提醒文字。 | Helper 位於 Input 下方，文字沒有被裁切。 | 文字裁切時回文字層檢查寬度與 Auto height。 |
| 6 | 截圖 Button Properties、兩個 Value、Form 三個圖層。 | 有按鈕狀態與表單結構兩類證據。 | 截圖要包含 Layers 名稱；空白畫布不能代替。 |
| 7 | 填寫完成檢查表，標記輸入互動與多欄位行為為未測試。 | 交接資訊不會把靜態結果誤寫成互動功能。 | 先保存檔案，再記錄未測試邊界。 |

**Checkpoint：** 步驟 3 後確認 Button 兩個 Value；步驟 5 後確認 Form 三層順序；兩項都通過才進入變因練習。

### 變因練習 / Solo

複製 `Form / Email` 結構，只改一個主要變因：把 Helper 文字換成「電子郵件格式不正確，請重新輸入」。保留 Label、Input 名稱、Button Properties、320×48 尺寸與層級順序。

請記錄：

1. Helper 長句是否仍在 Input 下方可讀。
2. Button 的 Primary／Disabled Value 是否未被改名。
3. 哪一個尺寸或文字框需要回修。

不要把 Helper 的文字改色當成互動錯誤驗證；本堂只能記錄視覺狀態。

### 驗收 / Verify

#### 完成條件

- Figma 檔包含 `Button / Primary` component set，Property 內有 `Primary`、`Disabled` 兩個 Value。
- Button 基準尺寸為 320×48，兩個狀態都能在 Layers／Properties 讀取。
- Form 圖層依序包含 `Form / Email / Label`、`Input`、`Helper`。
- Helper 長句沒有被裁切，Label、Input、Helper 的相對位置可重讀。
- 完成檢查表記錄 Figma 連結、截圖、變因修正與「輸入互動／多欄位尚未測試」邊界。

#### 常見錯誤與修復

| 現象 | 原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| Button 沒有第二個 Value | 尚未執行 Add variant，或選到外層 Frame。 | Button component 與 Properties。 | 步驟 3，重新建立 Variant。 |
| Disabled 變成圖層名稱警告 | 把 Layers 名稱當成 Property Value。 | Property 1 的 Value 欄。 | 步驟 3，改成 `Property 1=Disabled`。 |
| Form 圖層順序混亂 | Label、Input、Helper 建立在不同父層或命名不一致。 | Layers 層級與名稱。 | 步驟 4／5，逐層移回同一個 Frame。 |
| Helper 被裁切 | 文字框寬度或高度模式不適合長句。 | Helper 文字層。 | 步驟 5，調整寬度與 Auto height。 |

#### 檢核題

1. Button 的 `Disabled` 是 Property、Value，還是另一個 component set？
2. 看到 Label、Input、Helper 三層時，哪些證據仍不足以證明輸入互動已完成？

#### 交接給 A7

保留 Button component set、Form 三層圖層、Helper 長句與未測試邊界。A7 會沿用同一套命名與內容壓力，處理 List、空狀態與項目增刪；A7 不會重新建立 Button 的 Property。

## 授課前驗證待辦

- [x] 在 Figma Starter／Free＋Chrome 實測 Button component、Add variant、`Property 1=Disabled`；證據在 `PROBE-A.md` 的 A-15。
- [x] 在同一個 Probe A Frame 建立 Form Label／Input 圖層；證據在 `PROBE-A.md` 的 A-16。
- [ ] 用乾淨 Draft 重跑一次，並補測輸入互動與多欄位排列的實際邊界。
- [ ] 真人冷讀完成，確認學員能從 A5 交接物走到 A6 檢查表。
- [ ] 通過前維持 `MACHINE_READY_PENDING_HUMAN`，不得標示 `READY`。
