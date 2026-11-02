# uiux-designer 第四輪：一致性與無障礙修正

發包人：產品經理（Claude Opus 5.5）。承作：GPT-5.6 Sol（high）。日期：2026-11-02。
課程負責人指示「先修一致性與無障礙」：只修 `independent-review.md` 審查員 E 前五項的第 1、2 項，以及 PM 核對屬實的矛盾。**不新增功能、不調時數、不改評分表、不改練習範圍。** 前三份規格書的必守規則全部有效。

輸入 `round3/<單元>.md`，輸出 `round4/<單元>.md`。只改本檔列出的地方，其餘原文照抄（含截圖行與前後空行）。頁尾 `## 自我檢查` 加「第四輪修改」逐條列改了什麼。

## 1. 主線物件總表（全課以此為準）

下表是主線（工作室待處理清單）的正式名稱。各頁規格表、步驟、排錯表、事實核對一律用這些名稱；遇到不同叫法就改成表中名稱。

| 物件 | 名稱 | 第一次出現 | 說明 |
|---|---|---|---|
| 登入畫面 | `Screen / Login` | A1 | 402×874 |
| 登入卡片 | `Login / Card` | A1 | A1 用 **Frame（F）** 建立（不是 Rectangle），固定高度；A3 加 Auto layout 改成隨內容長高。卡片內的標題、說明、欄位、按鈕都是它的子層 |
| 登入內容欄 | 不另建 | — | 刪除 `Login / Content`。A2 若需要一個容器包標題與說明，就用 `Login / Card`；A6 不再新建容器，直接在 `Login / Card` 裡排欄位 |
| 草稿按鈕 | `Button / Draft` | A1 | A4 轉成主元件後改名 `Button / Primary` |
| 按鈕主元件集 | `Button` | A5 | 屬性 Type（Primary／Secondary）× State（Default／Hover／Pressed／Focus／Disabled） |
| 按鈕使用處 | `Button / Login`、`Button / Complete`、`Button / Cancel`、`Button / Confirm` | A4、A8 | 使用處名稱 |
| 返回鈕 | `Button / Back` | A8 | **只有一個**：A8 `Top Bar` 左側 44×44 的返回圖示鈕。B2、B3 一律用它，刪除 120×48 的返回按鈕 |
| 頂部標題列 | `Top Bar`、`Top Bar / Title` | A8 | |
| 標籤列元件 | `Tags` | A3 | A3 做好後 **Create component**；A7 的 `Row / Tags` 是它的使用處 |
| 圖示元件 | `Icon / Check`、`Icon / Plus`、`Icon / Arrow Left`、`Icon / Clock`、`Icon / Alert`、`Icon / Chevron Right` | A4 | A4 一次建好這六個（`icon-clock.svg`、`icon-alert.svg`、`icon-chevron-right.svg` 都在圖示包），後面各頁直接用 |
| 文字欄元件集 | `Field` | A6 | State：Default／Focus／Error／Disabled；屬性見第 3 節 |
| 任務列元件 | `Row / Task` | A7 | Text property `Title`、`Due`，Variant `Status`（Todo／Done） |
| 任務列使用處 | `Row / T01`～`Row / T12` | A7 | A7 放好 12 個使用處後，依 `TASK-DATA.csv` 的編號把圖層改名（只當圖層名，正文用任務名稱稱呼） |
| 清單畫面 | `Screen / List` | A7 | |
| 詳情畫面 | `Screen / Detail`（整理交付包）、`Screen / Detail T02`（確認活動報名資料並補上聯絡電話） | A7、B2 | A7 只做 `Screen / Detail`；B2 跟著做時複製出 `Screen / Detail T02`。兩筆詳情的說明文字在 A7 規格表一次給齊（自擬一兩句，例如整理交付包：「核對檔名與尺寸，把畫面圖、規格與測試紀錄放進同一個資料夾。」），B2 照用 |
| 空清單 | `Screen / List Empty` | A7 | |
| 完成清單 | `Screen / List Done` | A8 | 全課唯一名稱，刪除 `Screen / Completed`；B2 的 `Button / View Completed` 改名 `Button / View Done` |
| 主線完成流程 | 登入 → 清單 → 詳情 → 按 `Button / Complete` → `Screen / List Done`（上方出現成功 `Toast`） | A8、B2、B4 | **沒有獨立的成功畫面**。B2 先用 Navigate 從詳情直接到 `Screen / List Done`；B4 再在中間插入確認彈窗 |
| 提示元件集 | `Toast` | A8 | Variant `Type`：Success／Warning／Error；Text property `Message` |
| 底部導覽 | `Nav / Bottom` | A8 | |

B2 正文提到「找到第二筆詳情畫面」的地方改成「複製 `Screen / Detail`，做出 `Screen / Detail T02`」。

## 2. 題目一致性

- **預約題的選擇時段統一成「整頁」**：`Screen / Select Slot`（B2 已有）。A6 表單的「日期時段」改成一個看起來像 Select 的欄位，顯示已選時段，點它進入選擇時段畫面（A6 只做靜態畫面）；B4 預約題的底部面板改成「篩選服務（依體型：小型犬／中型犬／大型犬／貓）」。`round2-topics.md` 已同步。
- **預約題額滿資料**：B2 時段規格表補一行「示範資料：11/8 的 11:00、15:00 已額滿（對應 `BOOKING-MINE.csv` 那天的 11:00 已有預約，另一格自訂）」，讓學員不必自己編。日期鈕列的「可水平捲動」改成「一排 7 天、超出畫面的部分先不做捲動，捲動到做長清單那一堂再加」。
- **題目的文字樣式**：A1 練習寫明「題目沿用同一組五種文字樣式，不另建；顏色另建集合」。
- **題目畫面尺寸**：A1 練習寫明題目畫面是 360×800（需求頁指定），和主線 402×874 不同。
- **A1 練習第一句**：A1 的「換你做」第一句不能是「從你的畫面清單挑出…」（此時清單還不存在），改成「先選題，再寫需求初稿」；刪除重複的句子。
- **Section**：A1 提到主線與題目分區時，用一句教 Section：按 ⇧S 拖出一個區，雙擊名稱改名。A4 的元件區沿用這個操作，改說「上次用過的 Section」。

## 3. A6 文字欄元件的正確做法（已實機確認）

實機結果：同一個 Text property 綁到不同 Variant 的文字層時，各 Variant 的文字都會變成屬性的預設值，原本寫在 Error 版本的錯誤句會被蓋掉。因此：

- `Field` 的 Text property：`Label`（預設「帳號」）、`Value`（預設「請輸入」）、`Helper`（預設「說明文字」）。另加 Boolean `Show helper`（預設 False）。
- **錯誤句不寫在元件裡**：Error Variant 只改外觀（外框 `Error`、Helper 文字色 `Error`）。到錯誤畫面的使用處，打開 `Show helper`，在右側 `Helper` 欄位輸入該欄的錯誤句（例如「請輸入工作室帳號」）。說明這樣每個欄位能有自己的錯誤句。
- 步驟順序：先在 Default Variant 建好 Label、Value、Helper 三個文字層並綁定屬性，**再** Add variant 做出 Focus、Error、Disabled（新 Variant 會帶著綁定）。刪掉「先在 Error 寫錯誤句再綁定」的順序。
- 密碼欄：Boolean `Show icon` 預設 **False**（帳號欄不會出現眼睛）；密碼欄的使用處才打開。圖示包沒有眼睛圖示，寫「用一個 20×20 的圓形暫代，之後可換成正式圖示」，並提醒四個 Variant 的圖示層都要綁 `Show icon`。
- 第 1 步順序修正：先建好欄位與按鈕的使用處，再放進 `Login / Card` 排列；不要在欄位還沒建時就叫學員「放入欄位」。
- 間距一律用 A3 的間距變數（4、8、12、16、24、32）；`Gap 20` 改成 16 或 24 並套變數。
- `Radio` 外框色寫明用 `Control Border`（見第 4 節）。
- 題目必填勾選框（例如「同意注意事項」）的錯誤狀態：勾選框列下方顯示 Helper 錯誤句，勾選框外框改 `Error`；寫一步示範。

## 4. 無障礙矛盾修正

計算依據：WCAG 對比公式（PM 已算）。

| 問題 | 現況 | 修正 |
|---|---|---|
| 輸入框與控制項外框太淡 | `Border` #CBD5E1 對白底 1.48:1，違反 A1 自訂的「輸入框邊界至少 3:1」 | A1 新增變數 `Control Border` #76859A（白底 3.76:1、Surface 3.50:1）。Field、Checkbox、Radio 外框、Toggle Off 底色、Select 外框一律改用 `Control Border`。`Border` 保留給卡片、分隔線這類裝飾外框，並在 A1 寫一句區分：「看得見才能操作的邊界用 `Control Border`，只是分區的線用 `Border`」 |
| Primary 按鈕內圖示看不清 | A4 圖示 Stroke 套 `Text`，在 `Primary` 底上 1.85:1 | A4：放進 Primary 按鈕的圖示 Stroke 改套 `Card`（白色，對 Primary 7.9:1）；Secondary 按鈕與一般畫面上的圖示仍用 `Text`。A5 的 Primary Variant 統一用白色圖示 |
| Hover 看不出來 | A5 Primary Hover 用 `Primary Soft` 外框，對白底 1.16:1 | A1 新增 `Primary Hover` #2F6E55（白字 6.03:1）；A5 Primary Hover 底色改 `Primary Hover`。Secondary Hover 用 `Primary Soft` 底色即可（它是填色，不是唯一線索） |
| 沒有焦點狀態 | 按鈕沒有 Focus | A1 新增 `Focus Ring` #1E293B；A5 State 加 **Focus**：外加 2 px `Focus Ring` 外框、與按鈕保留 2 px 間隔（可用 Stroke 的 Outside）。說明：用鍵盤 Tab 操作的人靠這圈知道目前在哪；A6 的 Field Focus 也改用 `Focus Ring`。按鈕元件因此變成 Type 2 種 × State 5 種＝10 個 Variant，A5 正文的「8 種」全部改成 10 種 |
| 交付沒有無障礙標註 | B7 `Note` 只標四類 | B7 `Note` 標註類型加第五類「無障礙」：焦點順序（用數字標出 Tab 的順序）、圖示與圖片的替代文字、觸控範圍。主線示範各標一處 |

A1 規格表與變數清單同步加入 `Control Border`、`Primary Hover`、`Focus Ring`、`Disabled Text`。A1 對比練習加一題：用對比檢查器比較 `Control Border` 與 `Border` 對白底的數值，說明為什麼要分兩個。

## 5. 其他屬實矛盾

- **B2 排錯表**：刪掉「目標 Variant 缺少返回互動 → 為 Hover 或 Pressed 補上回到適當狀態的 Trigger」這一列，改成「Hover 沒反應｜互動加在使用處而不是主元件的 Variant 上｜回到 Components 區的 Default Variant 加 While hovering」。
- **A2**：說清楚 `Title` 的父層。依第 1 節，標題是 `Login / Card` 的子層；Constraints 那段若示範「畫面內直接子層的標題」，改用畫面上方另一個直接子層（例如畫面標題「登入工作室」放在卡片外），並在規格表寫明它的父層是 `Screen / Login`。
- **B6 觀察紀錄**：素材頁 `assets/B6-prototype-task-test/reference/OBSERVATIONS.html` 由 PM 修；B6 正文若提到「長標題」，指的是「確認活動報名資料並補上聯絡電話」。

## 6. 分組與交付

- 每組只改負責的單元。跑 `python3 _review/2026-11-02/check-pages.py _review/2026-11-02/round4` 修到 OK。
- 完成後用這個指令檢查名稱是否統一：`grep -n "Screen / Completed\|Login / Content\|Button / View Completed" _review/2026-11-02/round4/*.md`（自我檢查與事實核對以外不得出現）。
- 不 git、不詢問、不用 course-* 技能、不上網。
