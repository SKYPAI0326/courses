---
slug: uiux-designer
unit_id: B4-overlay-single-action
title: 讓確認彈窗能開啟、取消、確認與交換
course_type: skill-operation
duration: 7h
prerequisites: [B3-transition-motion-purpose]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：完整Overlay開關／確認、可取消規則與在已開彈層內Swap的實際路徑。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 讓確認彈窗能開啟、取消、確認與交換

本堂把第08堂Dialog變成真正Overlay：詳情留在背景，取消回原畫面，確認看到完成結果。另做一條Menu→Help的Swap分支，實際比較「切整張頁」與「交換彈層」。

## 開始前，先找到材料與起點

前堂已能由List進Detail。第08堂的Overlay / Confirm與Screen / List Done都在同一檔，前者必須是真Frame。缺元件先回第08堂重建；這堂不借用只有圖片的Dialog。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/B4-overlay-single-action/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/B4-overlay-single-action/reference/EXPECTED-CHECK.html)記錄實際結果。

## Overlay與Navigate的差別

Navigate to替換整張畫面；Open overlay把一個Frame疊在原畫面上，背景還在。Close overlay關掉當前彈層。Swap overlay從彈層裡的熱區觸發，會用另一個彈層取代目前彈層，保留原設定；在一般畫面觸發時行為接近Navigate，不能叫做已測Overlay交換。

| 熱區 | Action | Destination／結果 |
|---|---|---|
| Detail的Button / Complete | Open overlay | Overlay / Confirm |
| Confirm的Button / Cancel | Close overlay | 原Detail重新可操作 |
| Confirm的Button / Confirm | Navigate to | Screen / List Done，包含成功Toast |
| Menu的「檢視說明」Button | Swap overlay | Overlay / Help |
| Help的「關閉」Button | Close overlay | 回到開Menu前的背景 |

確認主線每個trigger只執行一個動作：Button Confirm使用Navigate切到已完成畫面，成功Toast已經在該畫面裡。這不是「同trigger先Close再Navigate」的付費多動作，也不需要拆成多檔。

## 示範：保留Detail背景，開啟Confirm

1. 在Layers選擇Detail的Button / Complete外框，Prototype設On click、Open overlay、Destination Overlay / Confirm。Confirm應是第08堂的W320、Hug高Frame，包含Title／Body／Actions。
2. 在Overlay設定選Centered／置中，背景遮罩可用黑色25%。確認畫面後面的Detail仍辨認得出，但注意力集中Confirm；不要把Dialog底色也設成黑色遮罩。
3. 開啟Close when clicking outside／點外側關閉，作本例可取消確認的設定。Preview點Complete，Dialog應出現；點遮罩應關閉並回Detail。不可取消的情況才不選這個選項，需有明確理由與回應按鈕。
4. 回編輯畫布，選Confirm內的Button / Cancel，設On click→Close overlay。Preview再開Dialog點取消，背景Detail應維持原內容，不能切回Login。
5. 選Confirm內Button / Confirm，設On click→Navigate to→Screen / List Done→Instant。預覽確認後T01應顯示已完成，Toast寫「任務已完成」。T01 Detail內容尚未變是真實原型限制，若需要再次檢視已完成Detail可新增對應Frame，不假裝是資料庫同步。
6. 從Login完整跑到Confirm，分別試取消、外側關閉、確認三條。每次重新開始，記錄現在在哪個Frame與結果。

**檢查點：**Dialog出現時背景不是空白；取消只關彈層；外側關閉設定與預覽一致；確認到List Done且有文字結果；同一份檔能完成前後步驟。

## 跟著做：在已開啟的Overlay裡Swap

1. 新建Frame `Overlay / Menu`，W280、Vertical、Padding20、Gap12、Hug高，放標題「任務說明」與Button「檢視說明」，命名Button / Help。
2. 複製為 `Overlay / Help`，改Body「先核對內容與期限，再標記完成。」並加Secondary Button「關閉」，命名Button / Close。保持寬280，測長Body自動增高。
3. 在Detail新增Secondary Button「說明」，設On click→Open overlay→Overlay / Menu，Position選Top right，或用Manual設在手機內x98、y96（右邊留24）。Menu與置中的Confirm有不同用途與位置。不要在Detail直接Swap到Help跳過已開Menu狀態。
4. Menu裡的Button / Help設On click→Swap overlay→Overlay / Help。Help裡的Button / Close設Close overlay。每個action的來源與目的地應能在Layers指出。
5. Preview先開Menu，再點檢視說明。你應看到Menu被Help取代、背景仍Detail、位置沿用。再關閉Help應回Detail，而不是回Menu。
6. 若想讓Help回Menu，用Help內「返回選單」Button設Swap overlay→Menu；不要用Back猜彈層歷史，Swap不會像整頁Navigate一樣加入同樣歷史。

## 修復與回歸

| 現象 | 先檢查 | 回修後測什麼 |
|---|---|---|
| Confirm看起來像切頁、背景消失 | Complete的Action | 改Open overlay，確認背景仍Detail |
| 取消跳到List或Login | Cancel的Action | 改Close overlay，不設定Destination |
| 外側點了沒關 | Overlay設定／熱區範圍 | 開啟外側關閉；點超出Dialog尺寸的遮罩 |
| Swap像Navigate | 觸發來自一般Frame | 先Open Menu，再由Menu的Button觸發Swap |
| Swap後位置意外改變 | 對Overlay設定的理解 | 新彈層沿用原位置；調整初始Menu設定 |
| 確認沒有結果 | Confirm Destination／List Done內容 | 指到已完成畫面，檢查T01狀態與Toast |

儲存主線與Swap分支；下一堂在List加入長內容及固定導航，再由第14堂整合測試。

## 自己完成：改變條件再檢查

複製Confirm為「取消編輯」情境：Title「放棄這次修改？」、Body「尚未儲存的內容會保留在此測試畫面。」取消保留Detail，另一動作回List。自己決定外側是否可關閉，並說明。另把Help說明加長兩倍，驗證Swap位置維持與內容不裁切。交出主線三條結果、Swap完整兩步及選擇理由。

## 完成條件與理解檢查

- Open／Cancel／outside／Confirm四種結果都在Preview實際檢查，目的地與表格一致。
- 從已開啟Menu內Swap到Help，關閉後回Detail，沒有把普通Navigate稱為Swap測試。
- 結果畫面有T01已完成與Toast，流程在同一份Figma檔，所有元件可重開。

**想一想：**從Detail的普通Button直接Swap到Help，為什麼不足以證明「彈層交換」？

<details><summary>展開參考答案與理由</summary><p>當來源不是已開啟的Overlay，Swap行為接近Navigate。要先開啟Menu，再從Menu內部熱區Swap到Help，才能驗證替換彈層並保留背景及位置。</p></details>

## 本堂查證來源

- [Figma：建立Overlay與Swap](https://help.figma.com/hc/en-us/articles/360039818254-Create-Overlays-in-your-Prototypes)
- [Figma：Prototype actions](https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
