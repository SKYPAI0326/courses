---
slug: uiux-designer
unit_id: B5-scroll-fixed-floating
title: 讓長清單能捲動，導覽與漂浮按鈕不擋內容
course_type: skill-operation
duration: 6h
prerequisites: [B4-overlay-single-action]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：建立視窗／長內容關係，實測Vertical、Fixed、Sticky及遮擋，在完整Flow使用長列表。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 讓長清單能捲動，導覽與漂浮按鈕不擋內容

現在把10筆以上的任務放進手機，讓人可以捲到底。你會區分畫面視窗與超出視窗的內容，分別測Fixed與Sticky，並避免底部導覽與漂浮按鈕遮住最後一列。

## 開始前，先找到材料與起點

前堂主線與Overlay都能點；第07堂長Row能隨內容增高。先選Screen讀402×874，再選List讀超出視窗的內容高。兩個數值不同才有合理滾動起點。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/B5-scroll-fixed-floating/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/B5-scroll-fixed-floating/reference/EXPECTED-CHECK.html)記錄實際結果。

## 先有超出的內容，才需要滾動

Viewport是預覽中看得見的402×874範圍；內容可以更高。把手機Frame本身增高到2000只會做出大畫布，不等於874視窗內能捲動。要保留外框874，讓內部List超過它。

| 物件 | 本課規格 | 滾動行為 |
|---|---|---|
| Screen / List Long | Fixed W402、H874、Clip content | Vertical overflow |
| List / Content | x24、y110、W354、Hug，高度超出874 | Scroll with parent |
| Header / Fixed | x0、y0、W402、H80 | Fixed |
| Nav / Bottom | x0、y810、W402、H64 | Fixed |
| Button / Floating | x330、y730、W48、H48 | Fixed；不蓋住最後一列 |
| Section / Sticky | 清單中某一分類標題 | Sticky：到頂才停住 |

Fixed從開始就保持在視窗同位置；Sticky先跟著內容移動，碰到父容器頂邊後才黏住，且不會超出直接父容器邊界。兩者有不同用途，不能把「畫在頂部」當成已經置頂。

## 示範：建立真正的Vertical overflow

1. 複製Screen / List為 `Screen / List Long`，維持402×874。將List內Row增加到12筆以上，每筆Title可編號「任務04…」，至少兩筆長標題；保持Row Hug、List Vertical／Gap12。
2. 確認List內容高度超過874。在外層Screen啟用Clip content，畫布只顯示視窗內部分；不要把溢位內容刪掉。
3. 選Screen外層→Prototype→Scroll behavior／Overflow，選Vertical。名稱可能顯示Vertical scrolling；關鍵是外層frame，不是把Overflow放在一個沒有超出內容的小Row。
4. 建Flow起點 `SCROLL-01`指到List Long，Preview向下捲。必須真的看見後面任務，且可到最後一筆；右側控制元件寫Vertical只是設定證據。

## 跟著做：Fixed Header、Bottom nav與Floating button

1. 在Screen / List Long內建立 `Header / Fixed`普通Frame，W402、H80、白底，放「待處理清單」標題及適當內縮。移除原來重複的頂部標題，List y110保證初始不被Header遮住。
2. 在Layers選Header→Prototype→Scroll behavior→Position，選Fixed。它應是手機內的子層，而不是手機外獨立物件。列表捲動時Header位置不變。
3. 選Nav / Bottom，同樣Position Fixed。檢查y810、高64，底部導覽不是放在List / Content裡一起捲走。選中頁仍能辨認。
4. 在Frame內建Button / Floating，48×48、Primary綠底、白色「↑」，x330、y730；設Position Fixed。先驗收位置；若加回頂部行為，可用On click→Scroll to→List內第一個Row，須再Preview驗證。
5. 在List最後新增 `Spacer / Bottom` Frame，W Fill、H120。它不顯示文字，只留安全空間，讓最後一列能捲到Nav與FAB上方。120是本例留白起點，需實際看遮擋再調整。
6. 捲到中段及最底部，記錄Header／Nav／FAB位置與最後一列能讀完的位置。不要只拍第一次進入畫面。

這堂手機外層用普通Frame，內部List用Auto Layout；若你改外層為Auto Layout，Fixed物件通常要先用Ignore auto layout（舊名Absolute position）脫離排列，才有獨立位置。找不到Fixed時先檢查父層與Overflow，別盲目換付費方案。

## Sticky小分支：到頂才停住

1. 複製List Long為 `Screen / Sticky Test`，移除Fixed Header來避免兩個頂部物件重疊。保留Vertical overflow與Bottom nav。
2. 在Screen裡放一段內容在y0到180，在y180新建 `Section / Sticky` Frame，高48、寬402，內文「今日任務」。放在可滾動內容同層，而不是嵌進只高48的小父框。
3. 選Section / Sticky→Prototype→Scroll behavior→Position Sticky。Preview往下捲：標題先隨畫面移動，到視窗頂部後停住；往回捲則離開黏住狀態。
4. 把它放進一個只包住短區域的父Frame，再觀察父區域離開時Sticky也跟著離開的差異。還原到正確父層，說明直接父層對有效範圍的影響。

## 橫向內容：另一種Overflow

建立 `Scroll / Horizontal` Frame，W354、H160、Clip content；內放Horizontal Auto Layout，三張Card各W200、H140、Gap12、Hug寬，總內容寬624。外Frame選Prototype的Horizontal overflow，Preview左右滑動，第三張應完整看得到。外框仍354，不能把它放大為624當作完成。這個分支用於卡片瀏覽，不改主清單的Vertical。記錄第一次／最後一張；完全不能滑時先查624是否真的超出354，以及Overflow是否設在外Frame。

## 卡住時

| 現象 | 位置／原因 | 修復與重跑 |
|---|---|---|
| 完全不能捲 | 外框Overflow或內容沒超出 | 保留H874，增加內層內容，外框Vertical |
| 整個手機拖著動 | 預覽縮放／畫布拖動 | 在Present內容內捲，不在編輯畫布拖手機 |
| Header跟著走 | Position仍Scroll with parent | 選Header子Frame改Fixed，重跑中段 |
| Fixed選項不可用 | 層級、Overflow、外層Auto Layout | 移進滾動Frame；需要時Ignore auto layout |
| 最後一列看不完 | 底部Fixed遮擋 | 增加Spacer，捲到底確認Row完整 |
| Sticky完全不動或太快消失 | 起始位置／直接父層範圍 | 起始y180；檢查父框有效區域與同層順序 |

把List Long接到整個任務流程，將Button / Login目的地改為List Long，T01連Detail，Detail返回也指List Long。原短List保留作比較；第14堂測試的是包含長列表與Fixed的完整流程。

## 自己完成：改變條件再檢查

把List Long改為360×800，ListW312，Header與NavW360、Nav y736、FAB x288／y656，保持右側與底部間距合理。增加20筆任務，檢查最後一筆、Footer留白與長標題。故意把Spacer移除觀察遮擋，再恢復。交出402與360中段／底部畫面、Fixed與Sticky差異說明、橫向第一／最後一張與修復。

## 完成條件與理解檢查

- 874視窗內能Vertical捲到最後一筆，外Frame沒有為長內容增高。
- Header／Nav／FAB在中段與底部保持位置，最後一列能在遮擋區上方讀完。
- Sticky真的先捲再停，主線Login與返回已指List Long，下一堂能測此成果。

**想一想：**把外層Frame高改成2000，是否就完成874手機視窗的滾動？

<details><summary>展開參考答案與理由</summary><p>沒有。要保留874視窗，讓內部內容超出，再設Vertical overflow並實際捲動。外框直接變高，無法證明在指定手機視窗看完內容。</p></details>

## 本堂查證來源

- [Figma：Overflow與Fixed／Sticky](https://help.figma.com/hc/en-us/articles/360039818734-Prototype-scroll-and-overflow-behavior)
- [Figma：Ignore auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout-in-Figma)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
