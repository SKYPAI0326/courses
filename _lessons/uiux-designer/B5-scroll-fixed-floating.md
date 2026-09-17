---
course: uiux-designer
unit: B5
title: 滾動、置頂導覽與漂浮按鈕
hours: 6h
lesson_type: prototype-operation
prerequisite: B4（已有一個可預覽的 Overlay）
platform: Figma Starter／Free + Chrome
status: MACHINE_READY_PENDING_HUMAN
---

<!--
教案 B5 · 滾動、置頂導覽與漂浮按鈕

本單元把 B4 的可預覽互動放進一個需要閱讀的手機畫面。學員先處理 Frame 的 Vertical overflow，再分別觀察固定導覽與漂浮操作鈕是否留在可見位置。Probe B B-06 已確認 Overflow menu 有 No scrolling、Horizontal、Vertical、Both directions；固定元素與滾動的聯合行為仍需人工回歸。
-->

## 教學流程（Teaching Flow）

> **課型：prototype-operation**。順序：接手 B4 → 長內容問題 → overflow 概念 → 示範 → 同步操作 → 單一變因 → 回修與交接。
> **本節完成物：** 一個可在 Chrome Preview 滾動的手機 Frame、一份固定／漂浮層的檢查紀錄，以及清楚標記的未測邊界。

## 1. 情境與問題（Hook）

阿凱把工作室的任務清單放進手機畫面。清單增加到十筆後，底部任務被截掉；使用者往下讀時，回首頁與新增任務的入口也跟著消失。這一堂要讓畫面能讀完，也要讓兩個重要入口有清楚的停留規則。

你會先做一個「只有長內容」的測試，再加入 `Navigation / Header` 與 `Floating / Action`。每次只改一個條件，才能知道問題來自 overflow 設定、固定圖層，還是漂浮按鈕位置。Preview 的實際滾動結果要獨立記錄；右側面板的選項只能證明設定存在。

開始前請開啟素材包的 `source/FIGMA-FILE-URL.txt`。若你的帳號沒有編輯權，依照表格在自己的 Drafts 建立同名 Frame；不需要 Share、付款或公開權限。

## 2. 三個概念先對齊（Concepts）

| 概念 | 你要判斷的問題 | 本堂證據 |
|---|---|---|
| **Overflow** | 內容超出 Frame 時，Preview 是否能沿指定方向移動？ | Prototype／Design 面板中的 `Vertical` 設定，以及 Preview 實際滾動紀錄。 |
| **固定導覽** | 使用者往下讀時，導覽是否還在可見位置？ | 圖層位置、固定設定截圖與 Preview 觀察。 |
| **漂浮操作鈕** | 新增任務入口是否在不遮住清單的位置保持可用？ | 按鈕位置、遮擋檢查與 Preview 觀察。 |

`Vertical` 選項是機器已確認的介面材料；固定圖層與滾動同時成立的效果，尚未由 Probe B 證明。本堂會把它列為人工回歸項目，不把選項名稱當成成功證據。

## 3. 示範（Demo）

### 3.1 先建立長內容測試卡

```
SCROLL-01｜任務清單閱讀
Frame：Screen / Task list · 402×874
內容：標題、十筆任務、底部說明
預期：手指上滑後看見第 10 筆，沒有水平位移
設定：Overflow → Vertical
尚未測：固定 Header 與 Floating Action 的聯合行為
```

### 3.2 示範最短路徑

1. 複製 B4 的 Host，另存為 `SCROLL-01`；保留 Overlay，不在同一階段增加新的 Prototype action。
2. 把 Host 改名為 `Screen / Task list`，尺寸維持 402×874。
3. 在 Frame 內加入十筆任務，讓內容高度超過 874 px；末筆文字要能在 Layers 找到。
4. 選取真正的手機 Frame，找到 Overflow／Scrolling 選單，先記錄原值，再選 `Vertical`。
5. 開啟 Preview，從同一個起點上滑；在紀錄填寫 Expected「能看到第 10 筆」與 Actual「實際看到什麼」。
6. 再複製一份測試，加入 `Navigation / Header` 與 `Floating / Action`，分別測試固定位置與遮擋範圍。

### 示範的判斷

如果選單顯示 `Vertical`，但 Preview 仍不能上滑，先查選取的物件、內容是否真的超出 Frame，以及 Preview 起點。固定層的設定與滾動結果分開寫；看不到聯合效果時標記 `NOT_RUN`。

## 4. 跟著做（Together）

| 步驟 | 學員動作 | 應看到的結果 | 沒看到時的回修 |
|---:|---|---|---|
| 1 | 複製 B4 Host，建立 `SCROLL-01`。 | 保留 402×874 Frame 與可辨識的起點。 | 回 B4 檢查 Host 與 Flow starting point。 |
| 2 | 在 Frame 內加入十筆任務與底部說明。 | 末筆超出初始視窗，但仍位於 Frame 內。 | 展開 Layers，確認文字沒有落在 Frame 外。 |
| 3 | 選取 Frame，記錄 Overflow 原值。 | 紀錄有 Before 欄位。 | 先選 Layers 中的 Frame row，不要選文字層。 |
| 4 | 將 Overflow 設為 `Vertical`。 | 面板顯示 `Vertical`。 | 重新開啟選單；若只有 `No scrolling`，確認目前選到 Frame。 |
| 5 | 從起點開 Chrome Preview，上滑一次。 | 能看到清單後段或第 10 筆。 | 檢查內容高度、起點與 Preview 視窗。 |
| 6 | 新增 `Navigation / Header`，測試固定設定。 | 有一筆固定層證據與 Preview 觀察。 | 先把 Header 與內容分層，再重新選取 Header。 |
| 7 | 新增 `Floating / Action`，檢查右下角遮擋。 | 按鈕在可見區，沒有蓋住任務文字。 | 移動按鈕或縮小範圍，保留修改前截圖。 |
| 8 | 填寫 `reference/EXPECTED-CHECK.html`。 | Overflow、固定、漂浮三項各有狀態。 | 沒有觀察的項目填 `NOT_RUN`，不要猜測。 |

> **Checkpoint 1**：你能在 Preview 上滑看見長清單後段，並指出 `Vertical` 設定在面板與檢查表的位置。

## 5. 自己改一個條件（Solo）

複製 `SCROLL-01`，只做一個變化：把十筆任務換成十二筆，保持 Frame 尺寸、`Vertical`、Header 與按鈕位置不變。

1. 在檢查表填入 `CASE-B5-01` 與變化說明。
2. 先預測新增兩筆後，最底部內容需要幾次上滑才能看見。
3. 開 Preview 重跑同一條上滑腳本，記錄可見的任務編號與按鈕是否遮住文字。
4. 若 Header 或 Floating Action 在你的帳號中沒有固定效果，保留面板截圖並標記 `MACHINE_PASS_PARTIAL`，把失敗條件寫清楚。

> **Checkpoint 2**：Solo 只改內容數量；Overflow、Frame 尺寸與圖層名稱仍可與 Together 版本比較。

## 6. 卡住時怎麼回修

| 現象 | 可能原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| 選單沒有 `Vertical` | 選到文字層或 Group，不是可滾動 Frame。 | Layers 與 Overflow 面板。 | 回第 3 步。 |
| 面板是 `Vertical`，Preview 不能上滑 | 內容高度沒有超過 Frame，或 Preview 從錯誤起點開啟。 | Frame 內容、Flow starting point。 | 回第 2／5 步。 |
| 上滑後 Header 消失 | Header 仍是內容的一部分，或固定設定尚未人工確認。 | Header 圖層與固定選項。 | 回第 6 步。 |
| 漂浮按鈕蓋住任務文字 | 位置與安全區沒有一起檢查。 | Floating / Action 的位置與 Preview。 | 回第 7 步。 |
| 固定與滾動一起測時結果不一致 | Starter／瀏覽器版本或圖層結構差異。 | 檢查表的邊界欄位。 | 保留證據並標 `NOT_RUN`。 |

修復時保留前一版測試檔與截圖。若無法判斷，先停在 Checkpoint，交給 B6 使用目前的 `case_id` 與失敗描述；不要刪除整個檔案重做。

## 7. 驗收與交接（Verify）

- `SCROLL-01` 有 402×874 Frame、十筆以上內容與明確起點。
- 面板紀錄顯示 Overflow=`Vertical`；Before／After 值可追溯。
- Chrome Preview 實際上滑後看見清單後段，Expected／Actual 分開填寫。
- `Navigation / Header` 與 `Floating / Action` 各有圖層、位置與遮擋檢查紀錄。
- 固定與滾動的聯合結果若尚未由人工觀察，狀態寫 `NOT_RUN` 或 `MACHINE_PASS_PARTIAL`。
- Solo 只改任務數量，沒有順手修改 Frame、Overflow 或按鈕位置。

### 交給 B6

把 `CASE-B5-01`、Preview URL／檔案、Overflow 設定截圖、上滑的 Expected／Actual、固定層狀態與失敗條件交給 B6。B6 會把「第 10 筆是否可見、Header 是否仍可見、按鈕是否遮擋」寫成任務測試步驟。B5 沒有證明的聯合行為，留在 B6 的回歸清單。

### 課前驗證待辦

- [ ] 由另一位學員只看本頁完成一次長清單與 Overflow 設定。
- [ ] 以不同 Figma 帳號重做，記錄 Overflow 選項與固定層差異。
- [ ] 在 Chrome Preview 實際上滑並檢查固定 Header、Floating Action；未觀察項目保持未通過狀態。
