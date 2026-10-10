---
slug: uiux-designer
unit_id: A4-component-instance
title: 改一次來源，讓多個按鈕一起更新
course_type: skill-operation
duration: 5h
prerequisites: [A3-auto-layout-pressure]
revision: 2026-10-11
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：驗證主元件同步、個別Override及錯誤修復，讓來源與使用處關係可觀察。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 改一次來源，讓多個按鈕一起更新

登入、詳情與彈窗都需要相同的按鈕。複製一般Frame只會得到幾個互不相干的物件；本堂建立主元件與兩個Instance，實際驗證共同外觀更新與各自文字覆寫。

## 開始前，先找到材料與起點

在第03堂卡片找到含Label的Button / Draft；點外框能看到Auto Layout與H48才算通過。缺少時用文字「登入」按Shift+A，水平內距16、垂直12、綠底白字，先補成完整按鈕。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/A4-component-instance/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/A4-component-instance/reference/EXPECTED-CHECK.html)記錄實際結果。

## 來源與使用處的關係

主元件（Main component）儲存共用的結構與預設外觀；Instance是由它產生的使用處，保持連結。主元件改圓角，兩個Instance應同步；某個Instance的文字改成「下一步」，不應把其他按鈕的文字改掉。這種個別修改叫Override／覆寫。

| 物件 | 做什麼 | 檢查線索 |
|---|---|---|
| 主元件 `Button / Base` | 儲存共同結構：Label、內距、對齊與填色 | 紫色主元件標記、Assets中可找到 |
| `Button / Login` Instance | 登入畫面使用同一套按鈕 | 右側可回到Main component |
| `Button / Complete` Instance | 詳情畫面使用，文字改為標記完成 | 改Label只影響本Instance |
| 一般複製Frame | 不保留元件來源關係 | 修改原Frame後副本不會跟著變 |

**不要先Detach。**Detach instance會中斷與來源的連結；它適合你確定要把物件變成獨立結構的時候，不能拿來解決「選錯層」或不知道去哪裡改共用設定。

## 示範：建立一個能更新的來源

1. 在第03堂 `Login / Card` 中選 `Button / Draft` 外框，確認它包含Label、H48、水平內距16、垂直12與置中對齊。若目前是白字加綠色Rectangle兩個互不相關物件，先用Auto Layout包住Label；不可直接把只有形狀的Rectangle當成完整按鈕。
2. 複製這個按鈕到手機Frame外的空白畫布，保留原版用於比較。將副本命名 `Button / Base`，外框寬度改Hug contents、高48，Label文字採Auto width；之後放入表單的Instance才依父框改W Fill。
3. 右鍵選 Create component，或使用工具列的建立元件入口。選取後應看到紫色標記；Assets搜尋 `Button / Base`應找到本檔元件。
4. 由左側Assets把元件拖到 `Screen / Login` 的卡片中，命名Instance為 `Button / Login`。在Layers將舊Draft移出卡片，避免兩個登入按鈕。若Assets找不到，可在主元件右鍵選Create instance，再將產生的Instance移進卡片。
5. 再建立第二個Instance放在手機外的測試區，命名 `Button / Complete`。進入其Label子層，把文字改為「標記完成」；外框寬度Hug時應變寬，文字與左右內距仍保留16。
6. 選主元件，將Corner radius從4改成12。不要選Login Instance，也不要選Label。兩個Instance應同時更新圓角；Complete的文字仍然是「標記完成」。
7. 記錄來源／兩個Instance修改前後的畫面。再把主元件圓角還原為8，作為本課視覺規格。

**中間結果：**你現在應有1個主元件、2個Instance與1個一般Frame比較樣本。主元件改圓角，兩Instance跟著改，一般Frame不變。這才證明連結有效，只有Assets搜尋結果還不足。

## 跟著做：分清楚要改來源還是使用處

1. 在Login Instance改文字「登入工作室」，在Complete Instance保留「標記完成」。先說出這是共用修改或個別覆寫，再操作。
2. 回主元件把文字字重改為Medium500；兩個未覆寫字重的Instance應同步。這次看的是字重，不用再建立第三份相同元件。
3. 在Layers選Complete Instance，檢視主元件連結。若看到Go to main component，點它應回到 `Button / Base`；若沒有，檢查是否誤用了普通複製Frame。
4. 用同一來源多插入一個Instance，改Label為「取消」。自己記下「來源控制：Padding、圓角；此Instance覆寫：Label」，再在主元件暫改圓角，確認原按鈕與取消按鈕同步、兩者Label各自保留，還原圓角並保存前後值。有同學時可請他依紀錄核對。此時取消還是同樣外觀，主次樣式下一堂處理。
5. 儲存一份修改紀錄：改哪個層、改哪個屬性、哪些物件跟著變、哪些沒有變。元件的價值是可追蹤的更新關係，不是紫色外框本身。

## 不同步時的修復

- 只有一個Instance沒有更新顏色：檢查該屬性是否曾在Instance覆寫。可用Reset overrides恢復，但會一併重設相關覆寫；先記下要保留的文字再重設。
- 兩個都不更新：確認選到主元件，而不是某一個Instance；也確認它們指向同一個來源。
- 更新後Complete文字變回登入：可能重設了所有覆寫。還原文字，下一堂用Text property把Label做成更清楚的可調欄位。
- Instance不能自由加減子層：共用結構應回主元件修改；不要為了新增一層就Detach所有使用處。

主元件留在手機外的元件區，Instance放進手機畫面；下一堂會把來源擴成主次與停用四種狀態。

## 自己完成：改變條件再檢查

建立第三個Instance，文字「返回清單」。先在此Instance覆寫填色，再修改主元件填色：預測哪幾個會更新，實際比對後修回共用規則。交出預測／觀察／修復的三欄紀錄。通過條件是能解釋覆寫造成的差異，不是全部手動改成同色。

## 完成條件與理解檢查

- 主元件有完整Label與Auto Layout，Assets能找到來源。
- 兩Instance能跟著來源的圓角／未覆寫字重更新，個別文字仍保留。
- 能定位一次覆寫造成的不一致，回到正確來源或重設覆寫修復。

**想一想：**為何從一般Frame複製兩個按鈕，無法達成「改一次全更新」？

<details><summary>展開參考答案與理由</summary><p>一般複製只有複本，沒有主元件連結。Instance儲存來源關係；共用屬性修改從主元件傳到未覆寫的使用處。文字等個別覆寫可以保留。</p></details>

## 本堂查證來源

- [Figma：主元件與Instance](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
