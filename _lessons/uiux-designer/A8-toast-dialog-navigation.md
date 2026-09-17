---
course: uiux-designer
unit: A8
title: Toast、Dialog 與 Navigation
hours: 4h
lesson_type: skill-operation
prerequisite: A5, A6, A7
platform: Figma Starter／Free + Chrome
status: MACHINE_READY_PENDING_HUMAN
---

<!--
教案 A8 · Toast、Dialog 與 Navigation

本單元承接 A5 的狀態欄位、A6 的 Button／Form 與 A7 的 List／空狀態。學員建立 Toast、Dialog、Navigation 的視覺層與命名，為下一階段 Prototype 準備可辨識的畫面材料。Probe A 的 A-20～A-22 已確認三種視覺層可在 Starter／Free 建立。

本堂的完成條件集中在回饋內容、彈窗內容容器與導覽位置；出現時機、Overlay、關閉、置頂、滾動與 Prototype 連結要在 Part B 另立測試案例。
-->

## 教學流程（Teaching Flow）

> **課型：skill-operation**。順序：接手成果 → 情境 → 概念 → 示範 → 同步操作 → 變因練習 → 驗收與交接。
> **本節完成物：** `Toast / Success`、`Dialog / Confirm`、`Navigation / Header` 三種視覺層與狀態內容表。

## 1. 情境與問題（Hook）

清單完成一個動作後，使用者需要知道結果；要刪除一筆資料時，需要先看清楚確認內容；從登入到清單時，需要知道目前在哪一頁。三種訊息放在同一個灰色矩形裡，下一位工作者無法判斷它的責任與使用時機。

這一堂先把三種視覺責任分開：Toast 傳遞短暫結果、Dialog 承載需要決定的內容、Navigation 顯示目前位置與可去的地方。你會留下可供 B1／B2 建立 Prototype 的畫面材料。

## 2. 先理解三個判斷點（Concepts）

| 元素 | 要處理的訊息 | 本堂證據 |
|---|---|---|
| Toast | 一次動作完成後的短結果 | `Toast / Success`，文字可在元件內補上。 |
| Dialog | 需要使用者確認或取消的內容 | `Dialog / Confirm`，固定 260×150 容器。 |
| Navigation | 目前位置與主要去向 | `Navigation / Header`，含「首頁／清單／設定」。 |

### 邊界規則

- 視覺層先有可讀名稱、尺寸與內容層級。
- 是否自動出現、何時消失、是否阻擋背景，要靠 Prototype 操作驗證。
- 是否置頂、是否跟著滾動，要在後續頁面測試，不從名稱推論。

## 3. 示範（Demo）

示範在 A7 的 `Screen / Login`／`Screen / List Top` 工作區完成。每一個結果都在 Layers 或右側尺寸欄確認。

1. 建立 `260×48` Rectangle，命名 `Toast / Success`。
2. 在 Toast 內加入短文字「已儲存」，讓訊息責任清楚。
3. 建立 `260×150` Rectangle，命名 `Dialog / Confirm`。
4. 在 Dialog 內加入標題「刪除這筆資料？」與按鈕文字「取消／確認」。
5. 建立文字層，輸入「首頁    清單    設定」，命名 `Navigation / Header`。
6. 把 Navigation 放在畫面上方，Dialog 保留內容區，Toast 放在不遮住主要操作的位置。
7. 截圖三個 Layers、尺寸與文字，填入 A8 完成檢查表。

### 示範的判斷

Toast、Dialog、Navigation 的責任不同，尺寸與文字層級要讓接手者一眼分辨。這些材料還沒有互動；互動證據要在 Prototype 頁面取得。

## 4. 跟著做（Together）

| 步驟 | 學員動作 | 預期結果 | 快速檢查 | 卡住時的回修 |
|---:|---|---|---|---|
| 1 | 開啟 A7 檔與 A8 起始材料，選取清單 Frame。 | A7 的 Row、Title、Empty Message 仍可找到。 | Layers 的父層正確。 | 回 A7 檢查檔案與 Frame。 |
| 2 | 建立 260×48 Rectangle，命名 `Toast / Success`。 | Layers 有 Toast，W/H 可讀。 | 右側 W/H 為 260／48。 | 選 Rectangle 重新設定尺寸與名稱。 |
| 3 | 加入「已儲存」文字。 | Toast 內有可讀短結果。 | 文字不遮住邊界。 | 先選文字層，再從右側 Content 重填。 |
| 4 | 建立 260×150 Rectangle，命名 `Dialog / Confirm`。 | Layers 有 Dialog，內容區可辨識。 | 右側 W/H 為 260／150。 | 回到外層 Frame 選取，再建立 Rectangle。 |
| 5 | 加入標題與「取消／確認」文字。 | Dialog 有標題與兩個選項。 | 內容層級不與背景混在一起。 | 逐個文字層命名並重新排列。 |
| 6 | 建立 `Navigation / Header`，輸入「首頁／清單／設定」。 | Layers 有 Navigation，畫面上方可看到文字。 | 位置與文字內容可讀。 | 先選 Text，再改名稱與位置。 |
| 7 | 填寫檢查表，保存三類截圖與邊界紀錄。 | 交接包說明視覺責任與未測行為。 | 有 Layers、尺寸、文字三類證據。 | 逐項補拍，不能只寫「已完成」。 |

> **Checkpoint 1**：你能分別指出 Toast、Dialog、Navigation 的責任、尺寸與文字；每一層都能在 Layers 找到。

## 5. 自己改一個條件（Solo）

只改 Dialog 內容，將標題換成「要移除這個清單項目嗎？」並保留 260×150、Toast、Navigation 與按鈕文字。

1. 只選 Dialog 內的標題文字，透過右側 Content 替換內容。
2. 觀察長標題是否需要兩行，以及容器是否仍能容納文字。
3. 確認 Toast 與 Navigation 名稱、位置沒有被改動。
4. 記錄行數、容器高度與需要修正的位置。

> **Checkpoint 2**：Dialog 長標題沒有被裁切；Toast 與 Navigation 仍可讀；檢查表記下至少一個觀察或修正。

## 6. 卡住時怎麼回修

| 現象 | 可能原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| 三種元素混在一起 | 建立時沒有用責任命名。 | Layers 名稱。 | 回第 2／4／6 步重新命名。 |
| Dialog 內容被裁切 | 容器固定高度，標題沒有換行空間。 | Dialog 與文字層的 Resizing。 | 回第 5 步調整文字與容器。 |
| Toast 遮住主要操作 | 只看畫布位置，沒有檢查主要按鈕。 | Toast 位置與畫面層級。 | 回第 6 步重新放置。 |
| Navigation 文字改到錯的層 | 目前選取了畫面或其他文字。 | Layers 的選取列。 | 回第 6 步重新選 Header。 |

把現象、回修位置與重跑結果寫入<a href="../courses/uiux-designer/assets/A8-toast-dialog-navigation/reference/EXPECTED-CHECK.html">A8 完成檢查表</a>。互動、Overlay、關閉與置頂仍標成未測，不用圖層名稱代替行為證據。

## 7. 驗收與交接（Verify）

- `Toast / Success` 為 260×48，含短結果文字。
- `Dialog / Confirm` 為 260×150，含標題與取消／確認文字。
- `Navigation / Header` 含首頁、清單、設定，位置可辨識。
- Solo Dialog 長標題的行數、容器高度與修正點已記錄。
- 三類截圖、Figma 檔連結與未測試邊界已保存。

### 交給 B1

保留三種視覺層、文字責任與尺寸表。B1 會把任務拆成畫面清單與 Prototype 入口；B2 再測觸發與連結。A8 不提前宣稱 Overlay、關閉、置頂或滾動成立。

### 課前驗證待辦

- [ ] 以乾淨 Draft 重做 Toast、Dialog、Navigation。
- [ ] 由另一位學員依頁面完成一次冷讀。
- [ ] 以不同 Figma 帳號重跑並記錄權限差異。
