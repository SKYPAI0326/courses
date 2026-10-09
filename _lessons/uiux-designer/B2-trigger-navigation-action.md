---
slug: uiux-designer
unit_id: B2-trigger-navigation-action
title: 連好登入、清單、詳情與返回
course_type: skill-operation
duration: 6h
prerequisites: [B1-wireframe-prototype-entry]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：建立同檔多步基本Flow，檢查熱區、目的地與返回，分辨方案限制及故障。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 連好登入、清單、詳情與返回

現在讓畫面能點。你會在同一份Starter檔案，分別為登入Button、任務Row與返回Button建立基本互動，從Login一路到Detail再返回。每個互動先確認選對物件、觸發與目的地，再開啟Preview真點一次。

## 開始前，先找到材料與起點

前堂Preview應從Login開始；Layers找得到Button / Login、Row / T01、Detail與Detail T02。缺T02先依第09堂Solo建好，不能把第2筆連到空白目的地。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/B2-trigger-navigation-action/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/B2-trigger-navigation-action/reference/EXPECTED-CHECK.html)記錄實際結果。

## 一條互動由三件事組成

Trigger是「什麼時候發生」，Action是「發生什麼」，Destination是「去哪裡」。本課先用On click／點選和Navigate to／切換整張畫面。手機預覽點選相當於Tap，不需要另建一份限制一個動作的檔案。

| 點選物件 | Trigger | Action | Destination | 預期 |
|---|---|---|---|---|
| Login的 `Button / Login` | On click | Navigate to | Screen / List | 看見三筆待處理任務 |
| List的 `Row / T01` | On click | Navigate to | Screen / Detail | 看見T01內容 |
| Detail的「返回清單」物件 | On click | Navigate to | Screen / List | 回到任務清單 |
| List的 `Row / T02` | On click | Navigate to | Screen / Detail T02 | 看見T02的期限與標題 |

Starter可以有上述多個基本互動；付費的Multiple actions指同一個trigger執行多個動作。這裡每個熱區各有一個action，完全不同。確認Dialog開關在第12堂加進這個檔案。

## 示範：連第一個登入Button

1. 開啟原課程檔，Layers展開Screen / Login，選擇Button / Login外框，不只選Label，避免只有文字能點。
2. 切Prototype，拖該物件旁的連線節點到Screen / List最外層Frame。目標應是整張手機畫面，不是其中的Row。
3. 在Interaction details設定Trigger On click、Action Navigate to、Destination Screen / List，Animation先用Instant。若用Interactions的＋建立，填相同三個欄位即可。
4. 回頭點這條連線檢查欄位；Destination如果是None或同名錯誤Frame，現在修正，不等到測試才猜。
5. 從TASK-01起點開啟Preview，點登入Button。畫面應從帳號／密碼切到三筆清單；不能只憑編輯畫布上的箭頭判斷成功。

此處登入不驗證輸入，點Button只模擬已登入狀態。第06堂的Error與Empty是展示用的分支；真實驗證需要程式，不要告訴測試者在Figma輸入真實帳密。

## 跟著做：連第二步與返回，減少提示

1. 自己找到Row / T01外框並連到Screen / Detail；用表格判斷Trigger、Action與Destination，不照著先前畫布位置猜。
2. 在Detail將「← 返回清單」文字包入Frame，設為 `Button / Back`，寬120、高48；對齊內容後連到Screen / List。使用明確目的地，可以直接從Detail開始測試也能返回；單純Back依歷史返回，沒有前一步時可能無效。
3. 將Row / T02連到Detail T02，並建立同樣的Button / Back。現在你應能從清單進入兩筆不同資料，而不是兩列都顯示T01。
4. Preview重啟TASK-01，執行Login→List→T01→返回→T02→返回。每一步在檢查表寫預期畫面與實際畫面名稱。
5. 在Screen / Login Empty選擇Disabled Button檢查Interactions，刪除或移除意外保留的點選連線。Disabled樣式本身不會阻止Navigate，必須在原型配置核對。

**檢查點：**點選按鈕邊緣仍能觸發；點選第二筆內容真的改成T02；返回不需要上一頁歷史；Disabled點了不應切頁。動畫目前Instant，避免先混入轉場問題。

## 故意做一個故障，再定位

複製測試用Button，在它的Interaction把Destination設為None。Preview點它不會有目標畫面。你的排錯順序是：選中的熱區對嗎→有On click嗎→Action對嗎→Destination存在嗎→Preview起點對嗎。修好後重新從Login執行整段，不只測試修過的Button。

| 現象 | 回修位置 | 正確結果 |
|---|---|---|
| 只有文字中央可點 | 連線綁在Label | 移到Button外框，邊緣也可點 |
| 點選卻回Login | Destination選錯Frame | 目的地List，預覽見三筆 |
| 列表兩列同一內容 | 兩熱區都指到T01 Detail | T02指到Detail T02 |
| 直接從Detail開啟，Back無效 | Back沒有歷史 | 本課返回清單用Navigate to明確目的地 |
| Disabled仍能跳頁 | 普通Instance複製連線 | 在停用使用處移除互動 |

儲存完整基本Flow；下一堂在這些連線上調動畫，不重新建立另一套Login與List。

## 自己完成：改變條件再檢查

從List Empty增加「檢視示範任務」Button，連回Screen / List；再建立Detail T03並獨立接上T03及返回。請同學從List Empty開始，不給口頭引導，確認能找到T03期限再回清單。交出新增的兩條連線、一次故障修復及實際Preview結果。

## 完成條件與理解檢查

- 同一檔案至少完成Login→List→T01 Detail→返回，T02顯示不同內容。
- 熱區綁在Button／Row外框，Destination不是None或錯誤Frame。
- Disabled沒有切頁行為，故意Destination故障已修復並跑完整回歸。

**想一想：**Starter可以在不同Button上建立多條Navigate，為什麼這不等於付費的Multiple actions？

<details><summary>展開參考答案與理由</summary><p>每個Button的點選各執行一個動作；Multiple actions是在同一個trigger堆疊多個action。本課沒有依賴這種付費堆疊功能。</p></details>

## 本堂查證來源

- [Figma：連線原型](https://help.figma.com/hc/en-us/articles/360040315773-Connect-your-prototype)
- [Figma：同一觸發的多動作與條件](https://help.figma.com/hc/en-us/articles/15253220891799-Multiple-actions-and-conditionals)
- [Figma：Prototype actions](https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
