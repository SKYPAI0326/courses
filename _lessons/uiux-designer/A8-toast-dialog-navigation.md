---
slug: uiux-designer
unit_id: A8-toast-dialog-navigation
title: 設計能讓人知道下一步的回饋、彈窗與導覽
course_type: skill-operation
duration: 4h
prerequisites: [A7-list-content]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：依情境選擇回饋，建立能包子層的Dialog與Actions，設計Nav選中規則。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 設計能讓人知道下一步的回饋、彈窗與導覽

使用者想知道任務是否完成，也需要能取消的確認步驟。本堂做出Toast、Dialog和Navigation三種完整容器，先教何時使用與內容層級，再把它們接到前堂的清單與詳情。真正開關Overlay留到第12堂。

## 開始前，先找到材料與起點

先確認第07堂有List、List Empty、Detail，且Detail有Button / Complete。若缺其中一個，回前堂末段重建；Dialog的取消與確認Button來自第05堂元件，不引用不存在的畫面。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/A8-toast-dialog-navigation/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/A8-toast-dialog-navigation/reference/EXPECTED-CHECK.html)記錄實際結果。

## 先選對回饋方式

Toast短暫告訴你已發生的結果，不要求立刻選擇；Dialog需要人先回應再繼續，例如確認重要操作；Navigation負責目前在哪裡、能去哪裡。不要每完成一件小事都跳確認視窗，也不要把必須回答的問題塞進會消失的Toast。

| 情境 | 元素 | 應出現的內容 |
|---|---|---|
| 任務已移到已完成 | Toast | 「任務已完成」＋成功線索 |
| 準備完成一筆任務、需要先確認 | Dialog | 明確標題、結果說明、取消與確認 |
| 在待處理／已完成間切換 | Navigation | 目前頁突出、另一頁仍可辨認 |
| 帳號格式錯誤 | 欄位Helper | 保留在該欄附近，第06堂做法；不使用Toast掩蓋 |

## 示範：真正可包含子層的Dialog

1. 在手機Frame外新建Frame，命名 `Overlay / Confirm`。建立文字 `Dialog / Title`「確認完成？」24／32，以及 `Dialog / Body`「這筆任務將移到已完成清單。」16／24。
2. 插入兩個Button Instance：Secondary／Default、Label「取消」、名稱 `Button / Cancel`；Primary／Default、Label「確認完成」、名稱 `Button / Confirm`。
3. 同選兩按鈕按Shift+A，命名 `Dialog / Actions`，Horizontal、Gap12、W272、Hug高；兩按鈕各W Fill、H48。這代表每個130寬，因為 `(272−12)÷2＝130`。這組Label正常能讀；換成長Label時先測，不硬壓文字。
4. 將Title、Body、Actions放入Overlay / Confirm；對外框新增Auto Layout，Vertical、Gap16、四邊Padding24、W320、Hug高、白底、圓角8。Title與Body W Fill、Auto height，Actions W Fill。外框可以包住子層，Rectangle不能代替這個父Frame。
5. 檢查閱讀順序：問什麼→造成什麼結果→取消或確認。Dialog內不放Bottom nav，背景畫面會在第12堂透過Overlay保留。

**檢查點：**Layers中Overlay / Confirm確實包住Title、Body、Actions；兩按鈕同高且間隔12；關鍵訊息清楚，不只寫「你確定嗎？」。

## 跟著做：Toast與Navigation

1. 新建成功訊息，T輸入「任務已完成」，16／24；在旁建立小勾號或文字「✓」，Success色。選兩物件按Shift+A，命名 `Toast / Success`，Horizontal、Gap8、水平Padding16、垂直12、深底白字、Hug寬與高。這是容器加訊息，不是只有背景矩形。
2. 複製Screen / List為 `Screen / List Done`，T01改「已完成」，列表標題可保留「任務清單」。把Toast放在畫面頂部內容區，避免蓋住主要操作；第12堂使用它呈現確認結果。原List仍保持T01待處理。
3. 建文字「待處理」與「已完成」，各16／24。用各自小Frame包住，寬201、高64、水平及垂直置中；目前頁用Primary字與底線，另一頁用Text字。底線和文字共同表示選中，不只換色。
4. 同選兩小Frame按Shift+A，命名 `Nav / Bottom`，Horizontal、Gap0、W402、H64、白底。放進Screen / List，x0、y810。用同樣元件放進List Done，選中狀態改已完成。現在不設固定滾動，第13堂才教Fixed。
5. 複製桌面參考，建立 `Nav / Desktop` W1200、H64的上方水平導覽，保留目前頁標示。手機只放短文字，桌面可加入工作室名稱與較完整連結；兩者用途相同，位置及資訊密度不同。
6. 故意把Dialog Body改成長說明「確認後這筆任務會移到已完成清單；如果資料尚未核對，請先取消並返回詳情修正。」檢查Title／Body高與外框Hug，Actions向下排列。

## 放進作品時，保留清楚的回應

目前作品應有Login、List、List Empty、Detail、List Done與Overlay / Confirm。主線是Login→List→Detail→Confirm→List Done，取消應留在Detail。不要因為這堂做了Toast就新建一條與任務無關的流程。

**卡住時：**Dialog子層無法移進背景Rectangle，改用Frame；Actions擠在一起，先檢查272內寬與12間距，再把文字改短或用垂直Actions，不縮到難讀；Navigation選中頁看不出來，補底線與文字；Toast蓋住重要按鈕，調整出現位置或持續方式。不同元素的錯誤要回到對應容器修，不把整張手機放大。

下一堂用這些物件規劃線框與原型流程。儲存可重開的元件與畫面，不能只儲存一張PNG；PNG不包含層級和互動。

## 自己完成：改變條件再檢查

有一筆任務即將被永久刪除，另有一筆只是已儲存。你要各選Dialog或Toast並寫理由，做出合理文字及取消路徑；刪除例僅製作示意，不操作真實資料。再把Confirm改成長標題並將Actions改垂直，保持每個Button W Fill／H48。比較水平與垂直選擇：長文字與窄寬度時哪個更可讀。

## 完成條件與理解檢查

- Toast包含結果文字；Dialog包含標題、說明與取消／確認兩個完整Button。
- Navigation有目前頁標示，手機與桌面資訊配置有清楚理由。
- 長Dialog內容仍完整，List Done與Confirm可供後課接線，沒有拿Rectangle當父容器。

**想一想：**「資料儲存成功」為什麼通常不必用需要按確認才能離開的Dialog？

<details><summary>展開參考答案與理由</summary><p>成功訊息通常只需告知結果，Toast能提供回饋且不中斷主要工作。需要使用者作決定、理解重要後果時才用Dialog；不能讓必要錯誤訊息自動消失。</p></details>

## 本堂查證來源

- [W3C：狀態訊息](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- [Figma：Auto Layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout-in-Figma)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
