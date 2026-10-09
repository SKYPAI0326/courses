---
slug: uiux-designer
unit_id: A5-variants-properties
title: 把主次按鈕與停用狀態做成可選的元件
course_type: skill-operation
duration: 6h
prerequisites: [A4-component-instance]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：設計互相獨立的Variant軸、四種狀態組合與可維持的Label屬性。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 把主次按鈕與停用狀態做成可選的元件

「主要」是按鈕的角色，「停用」是按鈕目前能不能操作。兩者是不同條件。本堂用四種組合建立Variants，並把按鈕文字做成Label欄位，讓後面表單與彈窗可以直接選用。

## 開始前，先找到材料與起點

在前堂元件區選Button / Base，再確認兩個Instance會同步。若尚未完成來源同步測試，回第04堂修好；本堂不要用Detach之後的獨立Frame當元件來源。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/A5-variants-properties/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/A5-variants-properties/reference/EXPECTED-CHECK.html)記錄實際結果。

## 先列組合，避免混淆角色與狀態

Variant是同一元件家族中的一種版本；Property是用來選版本或調整內容的欄位。這堂的Hierarchy表示Primary／Secondary，State表示Default／Disabled；Label是可改的文字。

| Hierarchy角色 | State狀態 | 外觀規則 | 使用例 |
|---|---|---|---|
| Primary | Default | 綠底白字；H48、置中 | 登入、確認完成 |
| Secondary | Default | 白底深字，深灰1px外框 | 取消、返回 |
| Primary | Disabled | 淺灰底、灰字；仍維持H48 | 帳號尚未填齊的登入 |
| Secondary | Disabled | 淺灰底、灰字與灰框 | 目前不能返回的操作 |

不能把Primary與Disabled當成同一欄的二選一：你會需要「主要但停用」和「次要但可用」。樣式的停用也不會自動禁止原型點選；第10堂會檢查停用物件沒有互動連線。

## 示範：從來源建立四個Variant

1. 在元件區找到 `Button / Base` 主元件。保留兩個Instance在測試區，不選它們一起合併。
2. 複製主元件三次，讓四個來源都保有同樣的Label層級與Auto Layout。它們都是主元件版本，不是Instance。
3. 逐個修改外觀，按表格建立四種組合。Disabled仍有「登入」文字與完整尺寸；不得做成一個沒有文字的灰矩形。
4. 同時選四個主元件，在右側或右鍵找Combine as variants，將外層Component set命名為 `Button`。
5. 選Component set檢查屬性。Figma可能先給 `Property 1`／`Variant`等名稱；將第一個屬性改成 `Hierarchy`，建立另一個Variant property叫 `State`。選各子元件，在右側指定其Hierarchy與State值，四組要與表格完全相同。
6. 若你的介面沒有直接新增欄位入口，可用各子元件名稱 `Hierarchy=Primary, State=Default`、`Hierarchy=Secondary, State=Default`、`Hierarchy=Primary, State=Disabled`、`Hierarchy=Secondary, State=Disabled`建立屬性和值；再確認右側呈現兩個屬性，而不是四個不明意義的Variant數字。
7. 如果跳出Duplicate variant／相同屬性組合警告，逐個比對兩欄值；同一組只能有一個版本。改名稱或顏色本身不會修好重複組合。

## 把Label做成文字欄位

1. 進入Primary／Default主元件，選Label文字層。在右側文字內容設定旁找Create text property／建立文字屬性入口，命名 `Label`，預設文字「登入」。
2. 其他Variant的Label也要繫結同一個Label屬性；若選到外層看不到文字入口，回Layers選文字層。繫結後，選Instance應能在屬性區輸入Label，不需要每次鑽進內層。
3. 從Assets插入新Button Instance，分別切換Hierarchy及State。將Label改「標記完成」，切換四種組合，文字仍要保留、置中，H仍48。
4. 找不到Text property入口時，先用Instance的Label子層覆寫文字完成視覺測試；這是文字覆寫備援，Text property仍需在可用介面補做並記錄，不能寫成已完成。

## 跟著做：用組合表找出一個錯誤

先不看示範的點選順序，自己插入兩個Button Instance：第一個選Primary／Default、Label「登入」；第二個選Secondary／Default、Label「取消」。把第二個切為Disabled，觀察外觀變化。每一步先說出要改的是角色、狀態或內容，才點屬性。

講師故意把兩個Variant都設成Primary／Default。你要用組合表找出哪一列缺失，再修正Hierarchy或State。若只有顏色不同但屬性值重複，仍然不算通過。

**檢查點：**4種組合都能選；長Label仍能閱讀；取消是Secondary不是Disabled；Disabled樣式不改變按鈕尺寸；Instance的內容欄位與狀態欄位用途不同。

## 卡住時

| 現象 | 可能原因 | 回修 |
|---|---|---|
| 只看到Variant 1／2／3 | 沒有把屬性命名成用途 | 在Component set命名Hierarchy與State，再填每個版本值 |
| 切狀態後文字丟失 | 各版本Label名稱／層級或文字屬性繫結不同 | 對齊Label命名與階層，綁同一Label屬性 |
| 找不到本檔Button | 選到Instance或一般Frame去合併 | 回來源元件區確認4個主元件在Component set裡 |
| Disabled點了仍切頁 | Prototype連線仍存在 | 視覺狀態不會自動移除互動，第10堂取消該物件連線 |

本堂產出Button family，不建立「Screen / List Top」等尚未教過的畫面。下一堂直接使用本堂Button做完整表單。

## 自己完成：改變條件再檢查

獨立建立「取消」與「確認完成」兩個按鈕配置：取消為Secondary／Default，確認為Primary／Default。再做「必填資訊尚未齊全」版本，只把確認改Disabled，新增提示原因。把Label改成「確認這筆任務已完成」，檢查左右內距及閱讀。交出四組狀態表、三個Instance與一個重複組合修復。

## 完成條件與理解檢查

- 四個Variant有唯一的Hierarchy／State組合，Default與Disabled能辨認。
- Label是可調文字欄位，切狀態後不丟文字；備援尚未補的項目據實記錄。
- 主次與停用分開，取消不會因為是次要動作就變成不可用。

**想一想：**把「Primary、Secondary、Disabled」塞在同一個屬性有什麼問題？

<details><summary>展開參考答案與理由</summary><p>它混合動作角色與可用狀態，無法完整表示Primary＋Disabled。用Hierarchy和State兩個屬性，才能建立四個明確組合。</p></details>

## 本堂查證來源

- [Figma：Variants](https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants)
- [Figma：Component properties](https://help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
