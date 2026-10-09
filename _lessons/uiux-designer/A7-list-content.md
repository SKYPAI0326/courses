---
slug: uiux-designer
unit_id: A7-list-content
title: 把任務做成會增高、可增刪的清單
course_type: skill-operation
duration: 4h
prerequisites: [A6-button-form]
revision: 2026-10-09
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：完整Row父子層級、清單增刪與空狀態，並建立真實Detail畫面供原型串接。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 把任務做成會增高、可增刪的清單

兩個矩形加兩段文字，還不能承受真實清單內容。本堂建立有層級的任務列，測試長標題、增加與刪除資料，並做出空清單。你會留下後續原型實際使用的List與Detail畫面。

## 開始前，先找到材料與起點

前堂已完成登入與Button family。你只需能插入Primary／Default的Button。若不會區分Frame和Rectangle，回第01堂速查；本堂不借用尚未建立的List Top。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/A7-list-content/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/A7-list-content/reference/EXPECTED-CHECK.html)記錄實際結果。

## 用固定資料建立第一張清單

使用[任務資料CSV](../../courses/uiux-designer/assets/shared/TASK-DATA.csv)，也可以直接複製下表。ID是資料的固定名字，方便測試與交接；顯示的中文標題可以修改。

| ID | 標題 | 期限 | 狀態 |
|---|---|---|---|
| T01 | 整理交付包 | 今天18:00 | 待處理 |
| T02 | 確認活動報名資料並補上聯絡電話 | 明天12:00 | 待處理 |
| T03 | 更新本週任務說明 | 星期五17:00 | 待處理 |

每一列包含Title、Meta、可點選線索（例如「檢視詳情 →」）；整列由一個Auto Layout Frame包住，才知道哪些內容屬於同一筆。List父框再包住多個Row，增刪時能重新排列。

## 示範：做一列可隨長文字增高的任務

1. 新建手機Frame `Screen / List`，402×874，底色Surface。在x24、y48加入「待處理清單」，24／32。
2. 在畫布建立 `Row / Title`文字「整理交付包」，18／28；建立 `Row / Meta`文字「待處理 · 今天18:00」，14／22；建立 `Row / Link`文字「檢視詳情 →」，14／22、Primary色。
3. 選這三個文字層按Shift+A，命名 `Row / Task`，Vertical、Gap8、四邊Padding16、W354、Height Hug、白底、圓角8。三文字W Fill、Auto height。短標題一行時，列高為 `16＋28＋8＋22＋8＋22＋16＝120`。
4. 建立兩個Row副本，按資料表改標題、期限和ID名稱為 `Row / T01`、`Row / T02`、`Row / T03`。第二筆標題應自然換行，Row變高；不改18／28字級來縮短它。
5. 同選三列按Shift+A，命名 `List / Content`，Vertical、Gap12、W354、Hug高、Padding0；放入Screen / List，x24、y110。若父框新增預設padding，改0，否則列寬會意外變小。
6. 在Layers確認每個Row包住自己的Title／Meta／Link；List包住全部Row。點T02的Title時只能編輯第二筆，不要選到外面的孤立文字。

**檢查點：**第二列變高時第三列自動下移；每列內留16，列與列之間12；List寬354；畫面標題不跟著增加資料移到列表裡。

## 跟著做：資料筆數與空狀態

1. 複製第三列為T04，改標題「核對本週發票」及期限「明天17:00」。觀察List高度增加一列高度加12，不手動移動其他列。
2. 刪除T02，T03與T04應自動上移。Undo復原後，再刪除剛新增的T04，主線回到原3筆；兩個結果都要記錄。
3. 複製手機為 `Screen / List Empty`。將所有Row從這張畫面移除，在相同Content位置放「目前沒有待處理任務」與「新任務會顯示在這裡」。空狀態是可辨認的資訊，不是只有空白Frame。
4. 複製T01，將狀態改為「已完成」，名稱 `Row / T01 Done`；保留相同層級與Title，狀態文字與成功圖示一起表示完成。第12堂會使用已完成清單，不只用綠色暗示。
5. 新建 `Screen / Detail`，402×874：頂部文字「← 返回清單」，內文區x24、y120、W354，放T01標題、說明「核對檔名、尺寸與透明背景，整理成可重開的交付包。」、期限「今天18:00」，再放Primary／Default Button Instance「標記完成」，命名 `Button / Complete`。用Vertical／Gap20／Hug包住內文與按鈕。

此時Detail只是有內容的畫面，點選不會真的切頁。下一階段才把Row與Detail連線。不要把沒有設定互動當作清單視覺製作失敗。

## 卡住時，從正確層級修

- 長Title裁切：選Title設Auto height與Fill，再選Row設Hug；兩者缺一都可能失敗。
- 新Row沒有推開後面：檢查是否在List / Content內。只是放在外面會看似重疊，Auto Layout無從知道它屬於清單。
- 整個List太寬：List W354／Padding0，Row W Fill／Padding16；不要把每層都留24，造成重複內縮。
- 空狀態還留一筆舊資料：只清空List Empty副本，不刪掉主線的3筆；檢查Layers避免把原畫面一併清空。

下一堂新增Navigation與Dialog。這堂的Screen / List、List Empty、Detail與三筆資料要留在同一份課程檔。

## 自己完成：改變條件再檢查

增加7筆不同標題的任務，至少一筆超過兩行，讓總數為10筆；再做0筆空狀態及只剩1筆的版本。三種筆數都要有合理內容、不重疊、不留下多餘Gap。另將畫面與List寬改360／312，判斷是哪一層需要Fill。長列表超出874是正常現象，保留長內容作第13堂滾動輸入。

## 完成條件與理解檢查

- 三筆主線Row都有Title、Meta、Link與自己的Auto Layout，List能隨增刪重排。
- 長標題增加Row高度、下列移動；空狀態明確，不是空白。
- Screen / Detail有T01資料與Button / Complete，後續連線可以直接使用。

**想一想：**把List最後一列刪掉後，為什麼不應留著它原來的空白高度？

<details><summary>展開參考答案與理由</summary><p>垂直Auto Layout用現有子層及Gap計算高度。刪除一列後父框Hug應縮小；若留空白，檢查固定高度、空佔位Frame或子層是否仍存在。</p></details>

## 本堂查證來源

- [Figma：Auto Layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout-in-Figma)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
