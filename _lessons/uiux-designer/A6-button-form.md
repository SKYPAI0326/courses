---
slug: uiux-designer
unit_id: A6-button-form
title: 完成表單與錯誤修正
course_type: skill-operation
duration: 6h
prerequisites: [A5-variants-properties]
revision: 2026-11-02
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方文件 2026-11-02 查證（_review/2026-11-02/platform-*.md）
---

## 內部設計（不進學員頁）

本課新增能力：組成多欄表單，分辨正常／錯誤／修正狀態，以Auto Layout處理長提示。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 完成表單與錯誤修正
副標：工作室人員登入與新增任務時，要看得懂每個欄位，也要能用正確控制項完成選擇並修正錯誤。
本堂完成物：含文字屬性的四狀態文字欄元件；一張新增任務表單；符合共用規格的五種表單控制項

## 把上次整理好的按鈕放進表單

工作室人員準備登入待處理清單，登入後還要新增任務。若畫面只有白色矩形、幾個圓點和一顆按鈕，使用者看不出欄位名稱，也不知道每一種選擇能選幾個。這堂會先完成登入欄位的狀態，再把文字欄、下拉、單選、開關與勾選組成新增任務表單。

這項工作會使用上次完成的 Button 元件集。先選取登入卡片裡既有的 `Button / Login`，確認 Type 可選 Primary、State 可選 Default，而且 Label 能直接改成「登入」。接著開[本堂起始材料](../../courses/uiux-designer/assets/A6-button-form/START-HERE.html)，理解登入情境與既有圖層；完成後用[完成檢查表](../../courses/uiux-designer/assets/A6-button-form/reference/EXPECTED-CHECK.html)逐張核對。沒有上次成果時，先回到[把主次按鈕與狀態做成可選的元件](CH5-variants-properties.html)，依該頁規格表補做 Button 元件集與文字屬性，約需 20～30 分鐘。

先保留 `Screen / Login`（登入畫面）的手機外框、卡片外的 `Screen / Heading`（畫面標題），以及 `Login / Card`（登入卡片）裡的 `Message`、`Hint` 與 `Button / Login`。接下來先在元件區建好欄位，再把欄位使用處放進登入卡片；帳號與密碼欄都有固定標籤後，`Hint` 就會由欄位標籤取代。

## 一個完整欄位要回答三個問題

完整欄位至少要讓人知道「這格是什麼」「現在填了什麼」「有問題時怎麼修」。固定的 Label 負責欄位名稱，Value 負責承載輸入內容，Helper 負責平常提示或錯誤說明；三者放在同一個容器，閱讀順序才穩定。

例如，帳號欄的 Label 是「工作室帳號」，Value 可顯示 `studio@example.test`，Helper 預設為隱藏。當內容只有 `studio` 時，錯誤畫面的使用處打開 `Show helper`，再把 Helper 改成「帳號格式不正確，請輸入完整電子郵件」。這樣每個欄位都能保留自己的錯誤句，紅色只負責加強辨識。

| 部分 | 平常負責什麼 | 錯誤時負責什麼 | 判斷是否用對 |
|---|---|---|---|
| Label | 固定說明欄位名稱 | 保持原名稱 | 輸入後仍看得見這格用途 |
| Value | 顯示輸入值或示意內容 | 保留使用者需要修正的內容 | 內容和欄位名稱相符 |
| Helper | 補充格式或條件 | 說明原因與修正方向 | 句子能回答「哪裡錯、怎麼改」 |
| Button | 提交目前表單 | 依表單是否齊全選狀態 | 文字說明按下後的動作 |

Placeholder 是尚未輸入時放在輸入區內的示意，它會在輸入內容後消失，所以固定 Label 仍要保留。必填欄位在 Label 後加上「＊」，並在表單開頭放一句「標＊為必填」；選填欄位則直接標「選填」。使用者在輸入前就能知道完成條件。

文字欄這次會有四種 State。Default 是平常外觀；Focus 表示游標目前在欄位裡，使用 `Focus Ring` 的 2 px 外框；Error 只把外框與 Helper 文字色改成 `Error`；Disabled 表示這格目前無法編輯，使用 `Disabled` 作底色、`Disabled Text` 作文字色。錯誤句留在畫面上的使用處輸入，四個 Variant 的層級保持相同，切換時畫面才不會跳動。

## 示範：做出含文字屬性的四狀態帳號欄

這一節先做一個完整帳號欄，再把它整理成四種 Variant。規格表集中列出所有名稱與數值，步驟只處理一項設定並觀察結果。

| 圖層或畫面 | 規格 | 內容或用途 |
|---|---|---|
| `Screen / Login` | 402 × 874；底色沿用登入畫面 | 正常登入畫面 |
| `Screen / New Task` | 起始 402 × 874；Fill 套用 `Surface`；內容超過 874 時將 H 改為 Hug contents，或加高到內容完整顯示 | 空白新增任務畫面；做原型捲動時改回手機高度並設垂直捲動 |
| `Login / Card` | x 24、y 120、寬 354；Vertical；Gap `Space 16`；Padding `Space 16`；Hug 高 | 直接放訊息、必填說明、欄位與按鈕使用處；加入帳號與密碼欄後刪除 `Hint` |
| `Field / Account` | Vertical；Gap `Space 8`；W 322；Hug 高；內層設為 Fill container | 帳號欄使用處 |
| `Field / Label` | 套用 `Type / Label`；Fill container；Auto height | 「工作室帳號＊」 |
| `Field / Input` | Horizontal；垂直置中；W Fill container、高 48；水平內距 `Space 16`、垂直內距 `Space 12`；圓角 8 | 隨寬 322 的 `Field` 改變寬度 |
| `Field / Value` | 套用 `Type / Body`；Fill；單行 | 預設「請輸入」 |
| `Field / Icon` | 20 × 20 圓形；Fill 套用 `Muted` | 暫代眼睛圖示；由 `Show icon` 控制 |
| `Field / Helper` | 套用 `Type / Supporting`；Fill container；Auto height | 預設「說明文字」；由 `Show helper` 控制 |
| `Required Note` | 套用 `Type / Supporting`；Auto height | 「標＊為必填」 |
| State=Default | `Card` 底；`Control Border` 1 px 外框 | 一般狀態 |
| State=Focus | `Card` 底；`Focus Ring` 2 px 外框 | 游標正在欄位內 |
| State=Error | `Card` 底；`Error` 1 px 外框；Helper 文字色 `Error` | 錯誤外觀，不預寫錯誤句 |
| State=Disabled | `Disabled` 底；`Control Border` 1 px 外框；`Disabled Text` 字 | 暫時無法編輯 |

1. 建立 `Field / Label`（欄位標籤），輸入「帳號」，再套用 `Type / Label`。新文字會沿用上次用過的樣式，每次建立後都要確認並換成這一步指定的樣式；完成後欄位用途會以標籤樣式固定顯示在輸入區上方。
2. 建立 `Field / Value`（欄位內容），輸入「請輸入」，再套用 `Type / Body`；完成後會以內文樣式看到尚未填寫時的提示。
3. 選取內容文字按 **Shift+A**，把新外框命名為 `Field / Input`（輸入區），再將寬度固定為 322 並依規格表設定外觀；完成後會先看到一個寬 322 的輸入區。
4. 建立 `Field / Helper`（欄位提示），輸入「說明文字」，再套用 `Type / Supporting`；完成後輸入區下方會有採輔助文字樣式、可供使用處改寫的文字層。
5. 同時選取 Label、Input 與 Helper，按 **Shift+A**，把新外框暫時命名為 `Field / Draft`（欄位草稿），再把外層 W 設為 322。多選包框的 Padding 會是 0，保持原值即可。把 Gap 改成 8，再綁定 `Space 8`。接著將 `Field / Label`、`Field / Input` 與 `Field / Helper` 改成 Fill container；完成後三個子層會以一致間距垂直排列，標籤、輸入區與提示文字的左右邊緣也會對齊外層欄位。
6. 選取帳號欄，按右鍵選 **Create component**，再命名為 `Field`（文字欄位）；完成後 Default 來源會先保留完整結構。
7. 選取主元件，在 Properties 按加號建立 `Label`、`Value`、`Helper` 三個 Text property，預設值依序填「帳號」「請輸入」「說明文字」。也可以選取各文字層，從 Content 旁的圖示直接建立並綁定對應的 Text property；完成後元件會有三個可改文字的欄位。
8. 將三個文字層依序綁定同名屬性，再為 Helper 的可見性建立 Boolean property `Show helper`，預設設為 False；完成後一般使用處不會先顯示說明句。
9. 在 Default 完成文字與顯示屬性綁定後，按右鍵選 **Main component → Add variant**，再用元件集下方的加號建立另外兩個 Variant；完成後四個版本都會帶著相同綁定。
10. 將預設屬性改名為 State，四個值命名為 Default、Focus、Error、Disabled；完成後使用處能從右側切換完整欄位狀態。
11. 依規格表設定四個版本；Error 只改外框與 Helper 文字色，內容維持屬性預設值。完成後四種外觀會保有相同層級。
12. 從 Assets 插入 `Field` 使用處，命名為 `Field / Account`；完成後帳號欄會先在登入卡片外備妥，卡片裡原有的 `Button / Login` 保持不變。
13. 將帳號使用處的 Label 改成「工作室帳號＊」，Value 改成 `studio@example.test`；完成後同一個 `Field` 會呈現帳號內容。
14. 將登入按鈕選成 Primary／Default，Label 改成「登入」，寬度設為 Fill；完成後主要動作會沿用既有 Button 元件集。
15. 按 **T** 建立「標＊為必填」，套用 `Type / Supporting`，再命名為 `Required Note`（必填說明）；完成後畫布上會有一段獨立的必填說明。
16. 欄位是由 Label、Input 與 Helper 組成的完整群組，因此把登入卡片的 Gap 改用 `Space 16`，讓欄位群組與按鈕清楚分開。在 `Login / Card` 裡依序放入既有 `Message`、`Required Note`、帳號欄與登入按鈕；完成後訊息、必填說明、帳號欄與登入按鈕會在既有卡片內垂直排列。
17. 依序切換四種 State；完成後 Label 與整體寬度保持穩定，Focus 外框加強，Error 保留可輸入的 Helper，Disabled 仍可閱讀。

打開 `Show helper` 後，欄位高度由上方文字、間距、輸入區與下方提示共同組成。實際排版交給 Hug contents 與 Auto height；當 Helper 變成兩行時，它會增高並把後面的欄位推開。

Focus 代表目前輸入位置，Error 代表內容需要修正，兩者可能先後發生。這份靜態元件先各自呈現一個主要狀態；之後做原型時，再依操作流程決定何時切換。

## 跟著做：用同一個 Field 完成密碼欄與登入畫面

這一節要用同一個 `Field` 完成第二個欄位，並把表單整理成正常、焦點、錯誤與修正後幾種結果。每一步先想要達成的畫面，再到對應元件或使用處找設定。

1. 再插入一個 `Field` 使用處，命名為 `Field / Password`（密碼欄），Label 改成「密碼＊」，Value 改成「••••••••」；完成後密碼欄會沿用同一組 State 與文字屬性。
2. 將 Helper 改成「密碼不足 8 個字元」。`Show helper` 維持 False；完成後錯誤狀態要用的句子已備妥，正常畫面仍不顯示。
3. 到 `Field` 元件集的四個 Variant（Default、Focus、Error、Disabled），各在輸入區右側放一個 20×20 圓形暫代眼睛圖示，再把 Fill 套用 `Muted`；完成後四個版本會有相同的圖層結構與次要色圖示。
4. 選取 Default 的暫代圖示，從 Appearance 的 Apply variable/property 圖示建立 Boolean property，命名為 `Show icon`，預設設為 False；完成後帳號欄不會先出現眼睛圖示。
5. 將四個 Variant 的暫代圖示層都綁定同一個 `Show icon`；完成後切換 State 時會保留使用處的顯示選擇。
6. 將密碼欄的 `Show icon` 打開，再把密碼欄放入 `Login / Card` 的帳號欄與登入按鈕之間，接著刪除原有的 `Hint`；完成後卡片會以「工作室帳號＊」與「密碼＊」兩個固定標籤說明欄位用途，原本的帳號提示不再顯示。
7. 複製 `Screen / Login`，命名為 `Screen / Login Focus`，讓帳號欄保持 Focus、密碼欄保持 Default；完成後會看到目前輸入位置只有一處。
8. 再複製一張畫面，命名為 `Screen / Login Error`，把帳號 Value 改成 `studio` 並切成 Error。打開 `Show helper`，在 Helper 輸入「帳號格式不正確，請輸入完整電子郵件」；完成後只有出錯欄位呈現自己的錯誤句。
9. 從錯誤畫面複製修正版，命名為 `Screen / Login Fixed`，改正值並關閉 `Show helper`。再把兩欄切回 Default；完成後能直接比較修正前後。
10. 另做一張空白登入畫面，命名為 `Screen / Login Disabled`，兩欄 Value 都改成「請輸入」。把登入按鈕切到 Disabled，並在附近放「請先填寫帳號與密碼」；完成後停用外觀會配合具體原因。
11. 把帳號錯誤句加長成兩行，觀察密碼欄與按鈕；完成後兩者會被推開，內容不會重疊。

最後從標題開始順著讀一次：標＊為必填、工作室帳號、輸入值、提示、密碼、輸入值、提示、登入。不同 State 都要保有相同閱讀順序；Helper 留在所屬欄位附近，使用者能直接對照要修改的內容。

## 先選對控制項：單選、勾選、下拉與開關

文字欄處理自由輸入，選擇題則要依「能選幾個、選項有多少、是否立刻生效」挑控制項。選對控制項能讓使用者在看到畫面時就理解規則，也能降低選錯後再修正的成本。

先把共用控制項的尺寸、外觀與狀態定清楚。之後主線表單與自己的題目都沿用這張規格，畫面才不會出現同名控制項卻有不同尺寸的情況。

| 元件 | 尺寸與外觀 | 狀態 |
|---|---|---|
| `Checkbox` | 用 F 建 20×20 的 Frame 當方框；圓角 4、外框 `Control Border` 2 px；勾選時底色 `Primary`、內放置中的 16×16 `Icon / Check` 使用處（Stroke `Card`）；整列最小高度 44；文字建立 Text property `Label`，預設「記住我」 | Checked true／false |
| `Radio` | 最小高度 44 的水平 Auto layout；用 F 建 20×20 的 Frame 當圓形控制圖形，與預設「選項」文字放在同一列；外框 `Control Border` 2 px；選取時 Frame 內放 10×10 `Primary` 內點；文字建立 Text property `Label` | Selected true／false |
| `Toggle` | 最小高度 44 的水平 Auto layout；用 F 建 44×24 的 Frame 當開關控制圖形，與預設「提醒我」文字放在同一列；圓角 12；Frame 內放 20×20、Fill `Card` 的圓鈕；On 底色 `Primary`、Off 底色 `Control Border`；文字建立 Text property `Label` | On true／false |
| `Select` | 沿用 `Field` 外框並套用 `Control Border`，標籤「類別」、內容「設計」，右側放向下箭頭（可用 `Icon / Chevron Right` 旋轉 -90 度）；展開時下方列出設計、行政、客戶、財務，每列高 44 | Open true／false |
| `Field / Multiline` | 複製 `Field` 後刪除 Disabled；寬同 `Field`；三個 Variant 的 `Field / Input` 高 96，Auto layout 對齊靠上；外框用 `Control Border` | Default／Focus／Error |

| 控制項 | 適合的選項數 | 可複選嗎 | 選擇後是否立刻生效 | 工作室例子 |
|---|---|---|---|---|
| Radio（單選） | 少量且需要同時看見 | 否 | 通常提交後生效 | 優先順序：高／中／低 |
| Checkbox（勾選） | 少量獨立選項 | 是 | 可先選好再提交 | 記住我、同意條款、加購項目 |
| Select（下拉） | 選項較多，畫面空間有限 | 否 | 選完仍可再確認 | 任務類別、日期時段、取餐時間 |
| Toggle（開關） | 一個可以開或關的設定 | 不適用 | 適合立即生效 | 提醒我、訂閱電子報、需要統編 |

單選要讓所有選項同時看得見，使用者能直接比較。勾選框適合彼此獨立的多個選擇，例如同時加購驅蟲與香氛。下拉把較長清單暫時收起，選定後仍顯示目前值。開關描述一個設定現在是開或關，例如打開「提醒我」後立刻顯示提醒時間欄。

每個控制項都需要可讀的文字標籤。勾選框與單選按鈕本體雖然很小，整列文字和控制項要放在最小高度 44 的水平 Auto layout 裡；點文字也應視為選取同一項。表單欄位標籤放在控制項上方，必填與說明文字放在使用者開始操作前就看得到的位置。

## 建立五種控制項，再組成新增任務表單

這一節會先建立小型元件集，再把它們放進 `Screen / New Task`（新增任務畫面）。每個選擇控制項只有一個真假屬性，兩個 Variant 的名稱、尺寸與文字位置保持一致。

| 元件集 | Variant 屬性 | 兩個值 | 主線用途 |
|---|---|---|---|
| `Checkbox` | Checked | false／true | 登入畫面的「記住我」與新增任務的「我已確認期限」 |
| `Radio` | Selected | false／true | 優先順序：高／中／低 |
| `Toggle` | On | false／true | 「提醒我」設定 |
| `Select` | Open | false／true | 任務類別的收合與展開；選項為設計、行政、客戶、財務 |
| `Field / Multiline` | State | Default／Focus／Error | 任務備註 |

1. 在 `Components` 裡用 **F** 建立 20×20 的 Frame 當勾選控制圖形，再把它與「記住我」文字放進最小高度 44 的水平 Auto layout；完成後勾選圖形會是可容納圖示的 Frame，整列也具備足夠觸控範圍。
2. 將這列建立為 `Checkbox` 主元件；完成後元件仍會顯示方框與「記住我」。
3. 選取「記住我」文字，建立並綁定 Text property `Label`，預設值填「記住我」；完成後主元件的 Properties 會顯示可改的 Label。
4. 用 **Main component → Add variant** 增加第二個版本；完成後會得到結構與 Label 綁定相同的兩個版本。
5. 把預設屬性改名為 Checked，兩個值填 false 與 true；完成後，使用處可以從右側切換勾選狀態。
6. 選取 Checkbox 的 true 版本，依共用規格表改外觀：方框底色套用 `Primary`，把 `Icon / Check` 使用處縮成 16×16 並置中放入 Frame，再將圖示 Stroke 套用 `Card`；完成後 true 版本會顯示置中白色勾號的主色方框。
7. 在 `Components` 裡用 **F** 建立 20×20 的 Frame 當 Radio 控制圖形，再把它與一層「選項」文字放進最小高度 44 的水平 Auto layout。將整列建立為 `Radio` 主元件，再增加第二個 Variant。把屬性命名為 Selected，兩個值設成 false 與 true。最後把文字建立並綁定 Text property `Label`，預設值填「選項」；完成後會看到未選與已選兩種完整文字列，Frame 內也能容納選取內點，使用處可直接改標籤。
8. 選取 Radio 的 true 版本，依共用規格表改外觀，在圓形控制圖形內加入 10×10 的 `Primary` 內點；完成後 true 版本會顯示主色內點。
9. 在 `Components` 裡用 **F** 建立 44×24 的 Frame 當 Toggle 控制圖形，在 Frame 內放入 20×20、Fill 套用 `Card` 的圓鈕，再把控制圖形與一層「提醒我」文字放進最小高度 44 的水平 Auto layout。將整列建立為 `Toggle` 主元件，再增加第二個 Variant。把屬性命名為 On，兩個值設成 false 與 true。最後把文字建立並綁定 Text property `Label`，預設值填「提醒我」；完成後兩個版本會保有相同結構，Frame 內會有 Card 色圓鈕，使用處也能直接改標籤。
10. 選取 Toggle 的 true 版本，依共用規格表改外觀，把底色改成 `Primary`，再將 Fill 為 `Card` 的圓鈕移到右側；完成後 true 版本會顯示主色軌道與靠右的 Card 色圓鈕。
11. 從 Assets 插入一個 `Field` 使用處，再按右鍵選 **Detach instance**。把標籤改成「類別」，內容改成「設計」。在輸入區右側放入 `Icon / Chevron Right`，並旋轉 -90 度。選取整理好的欄位按右鍵選 **Create component**，再命名為 `Select`。增加第二個 Variant，把屬性命名為 Open，兩個值設成 false 與 true。收合版顯示目前類別，展開版在下方列出「設計」「行政」「客戶」「財務」；完成後會看到含向下圖示的類別欄，Open 屬性能切換目前值與四個可見選項。
12. 選取 `Field` 元件集按 **Cmd／Ctrl+D**。把複製出的新元件集命名為 `Field / Multiline`。刪除 Disabled Variant。在 Default、Focus、Error 三個 Variant 各選取 `Field / Input`，把 H 設為 96，再將 Auto layout 對齊改為靠上；完成後元件集只保留三個版本，三個輸入區的文字都會從固定高度區域上方開始排列。
13. 在 `Screen / Login` 與複製出的 Focus、Error、Fixed、Disabled 畫面中，各在密碼欄下方插入 Checkbox 使用處，把 Label 保持為「記住我」；完成後，同組五張登入畫面都會有位置一致的勾選項。
14. 建立 `Screen / New Task`（空白新增任務畫面），將 W 設為 402、H 設為 874，並把 Fill 套用 `Surface`。先加入「標＊為必填」、頁面標題、任務名稱欄位與類別 Select 使用處；完成後會看見 Surface 底色上的表單標題與欄位。
15. 全選目前的標題與欄位按 **Shift+A**，設成垂直 Auto layout；完成後各欄會依固定順序往下排列。
16. 在類別欄下方按 **T** 建立「優先順序」，套用 `Type / Label`。在 Layers 把新 Label 拖進表單 Auto layout，放在前一個欄位之後；完成後類別欄下方會先出現單選群組的名稱。
17. 在「優先順序」Label 下插入三個 Radio 使用處，透過 `Label` 分別改成「高」「中」「低」，只讓其中一個 Selected=true。在 Layers 把三個使用處依序拖進表單 Auto layout，放在前一個欄位之後；完成後畫面會清楚表達三選一。
18. 插入 Toggle 使用處，透過 `Label` 把文字改成「提醒我」。在 Layers 把使用處拖進表單 Auto layout，放在前一個欄位之後；完成後開關與文字會在同一列表示提醒設定目前是否開啟。
19. 插入 `Field / Multiline`，Label 改成「備註（選填）」。在 Layers 把使用處拖進表單 Auto layout，放在前一個欄位之後；完成後長內容會留在固定高度的備註區。
20. 插入 Primary／Default 的 Button，Label 改成「新增任務」。在 Layers 把使用處拖進表單 Auto layout，放在前一個欄位之後；完成後表單會有一個清楚的提交動作。
21. 加入必填 Checkbox 使用處，把文字改成「我已確認期限」。在 Layers 把使用處拖進表單 Auto layout，放在前一個欄位之後；完成後空白新增任務畫面會顯示期限確認勾選列，後續副本也會沿用這一列。
22. 複製新增任務畫面，命名為 `Screen / New Task Select Open`，把類別 Select 切到 Open=true。若表單內容超過 874，把這張畫面的 H 改成 Hug contents，或加高到完整容納內容；完成後會看見設計、行政、客戶、財務四個選項，後續欄位也會由 Auto Layout 往下推開。做原型捲動那一堂會把畫面改回手機高度並設垂直捲動。
23. 複製 `Screen / New Task`，命名為 `Screen / New Task Filled`（已填新增任務畫面），再填入各欄內容；完成後會得到含期限確認勾選列、提醒開關尚未打開的已填狀態。
24. 複製已填畫面，命名為 `Screen / New Task Reminder`（提醒新增任務畫面），打開提醒開關並多放一個 `Field`。將 Label 改成「提醒時間＊」，再到 Layers 把新 Field 拖進表單 Auto layout，放在前一個欄位之後。若表單內容超過 874，把這張畫面的 H 改成 Hug contents，或加高到完整容納內容；完成後只有開關打開的畫面會顯示條件欄位，期限確認勾選列仍保留在相同位置。做原型捲動那一堂會把畫面改回手機高度並設垂直捲動。
25. 在畫布旁註記後續原型會用 Change to 或 Navigate 切換兩張畫面；完成後條件欄位的出現規則會保留下來。
26. 在 `Screen / New Task Filled` 建立「請先確認期限」，套用 `Type / Supporting` 與 `Error`。在 Layers 把新文字拖進表單 Auto layout，放在前一個欄位之後，再把方框外框改成 `Error`；完成後錯誤句會顯示在勾選列下方，而且不會進入 Checkbox 元件裡。修正後移除這段錯誤文字，外框恢復 `Control Border`。

做完後檢查每個控制項的文字是否描述資料本身。Radio 文字寫優先順序，Toggle 文字寫設定名稱，Select 收合版顯示目前選項。元件的真假屬性只留在設計設定裡，使用者看到的是自然語言。

## 看兩張新增任務表單，判斷哪張較容易完成

這一節要從控制項與錯誤回饋判斷可用性。版本一把「任務名稱」固定 Label 放在文字欄上方，優先順序用三個 Radio 顯示，類別用 Select，提醒用 Toggle；每個單選列都有足夠的觸控範圍，錯誤 Helper 緊接在任務名稱下方。版本二把欄位名稱只放在 Placeholder，優先順序改成三個互相獨立的 Checkbox，類別與提醒都使用外觀相似的小開關，觸控範圍只包住圖形本體。

請判斷哪一版較適合新增任務，並說明：使用者如何知道優先順序只能選一個？輸入後還能否看見欄位名稱？手指能否容易點到控制項？錯誤訊息是否靠近需要修正的欄位？

<details><summary>查看判斷理由</summary><p>版本一較好。Radio 直接表達三選一，固定 Label 在輸入後仍可見，最小高度四十四像素的整列觸控範圍讓文字也能點選，錯誤 Helper 則把原因與修正位置放在一起。版本二的 Checkbox 暗示可以複選，Placeholder 會隨輸入消失，小圖形也較難點中。</p></details>

## 卡住時，沿著文字、狀態與父容器往外查

這一節把常見問題整理成修復順序。先查文字尺寸模式，再查 Variant 屬性，最後查整張表單的 Auto Layout，通常能找到是哪一層阻止內容變化。

| 看到的現象 | 通常的原因 | 怎麼修 |
|---|---|---|
| 長錯誤句被裁切 | Helper 仍是固定高度 | 到 Layout 將文字尺寸模式設為 Auto height |
| Helper 變高但後續欄位沒下移 | Field 或表單不是 Hug／Vertical | 讓欄位 Hug 高，並確認它在垂直 Auto layout 內 |
| 使用處無法改 Label、Value 或 Helper | 文字層尚未綁定 Text property | 回主元件從 Content 旁的圖示綁定對應屬性 |
| 切換 State 後 Label 跳位 | 四個 Variant 的名稱或階層不同 | 對齊 Label、Input、Value、Helper 的層級 |
| 單選可以同時出現多個已選 | 各使用處狀態沒有按群組檢查 | 在畫面中只保留一個 Selected=true，並逐列核對 |
| Select 展開後蓋住下一欄 | 展開清單離開表單排列 | 把 Select 使用處放在表單 Auto Layout 內並讓高度 Hug |
| 開關打開後欄位沒有出現 | 只改了 Toggle 外觀 | 對照 Off 與 On 兩張畫面，確認 On 版多了條件欄位 |

修完後用最長錯誤句與 Select 展開版各測一次。長句能推開後續欄位，展開清單也能保留閱讀順序，表示表單層級能承受兩種內容變化。

## 換你做：你的題目

從你的畫面清單挑出這次對應的畫面。接著把主線表單元件複製到題目區並換綁變數，再完成表單、具體錯誤畫面與修正後畫面。

三個題目的建議對應：

| 預約 | 點餐 | 會員 |
|---|---|---|
| 預約資料：飼主姓名、手機、寵物名字、寵物體型單選、日期時段 Select 外觀欄位、驅蟲與香氛加購勾選、備註、同意注意事項勾選且必填；日期時段欄顯示已選時段，點擊後前往整頁 `Screen / Select Slot`，這裡只完成靜態畫面。 | 取餐資料：取餐人姓名、手機、取餐時間下拉、付款方式單選、需要統編開關、備註；開關打開時顯示統編欄。 | 註冊資料：姓名、手機、Email、生日月份下拉、喜歡的書類勾選且可複選、訂閱電子報開關、同意會員條款勾選且必填。 |

要達成的條件：

- 這次做的畫面在你的畫面清單上；清單沒有的，先補進清單並寫一句理由。
- 所有固定 Label 放在欄位上方，必填項目加上「＊」，表單開頭放「標＊為必填」。
- 依題目需求選用文字欄、Radio、Checkbox、Select 或 Toggle，選項文字完全照需求頁。
- 把主線的 `Field`、`Checkbox`、`Radio`、`Toggle`、`Select` 與 `Field / Multiline` 複製到題目區，做法和複製按鈕元件集相同。再把 `Studio` 變數換綁成題目集合裡的同名變數。
- Selection colors 只會換綁顏色變數。選取各元件集，在 Padding 與 Gap 欄位逐一換成題目的間距變數；題目沒有另建間距變數時，沿用 `Studio` 的間距並在練習裡寫明「間距共用」。
- 題目畫面寬 360，左右內距各 24；`Field` 在畫面裡設為 Fill container，`Field / Input` 會跟著欄位改變寬度。
- 做出一張具體錯誤畫面，Helper 說明原因與修正方向。
- 預約題的日期時段使用看起來像 Select 的欄位並顯示已選時段；整頁的選擇時段畫面留到連接原型那一堂再做，這次只完成靜態表單。
- 預約題與會員題的必填勾選框在錯誤畫面顯示 Helper 錯誤句，方框外框套用 `Error`；修正後移除錯誤句並恢復 `Control Border`。
- 點餐題另做「需要統編」Off 與 On 兩張畫面，On 版多一個統編欄。
- 做出修正後畫面，欄位順序與主要確認動作保持一致。

合格的結果要能通過的自我檢查：

- 每個控制項都符合「可選幾個、選項數量、是否立即生效」的選用規則。
- 單選群組同一時間只有一個已選，勾選群組允許依需求複選。
- 下拉的收合與展開版都看得見欄位 Label 和目前選項。
- 錯誤訊息能回答哪裡有問題以及接下來怎麼改。
- 長說明或展開清單會推開後面內容，不會互相重疊。
- 開關控制條件欄位時，Off 與 On 兩張畫面的差異清楚。

<details><summary>真的卡住再看：提示</summary><p>先逐欄標出「只能選一個、可以選多個、選項較多、立即開關」四種需求，再選控制項；版面卡住時，從文字 Auto height、元件 Hug、表單 Vertical 三層往外檢查。題目畫面寬 360、左右各留 24 時，Field 設為 Fill container 後欄寬是 312，輸入區會跟著填滿欄位。</p></details>

## 收回工作室情境，下一步把資料排成清單

這堂讓工作室登入與新增任務都有完整表單。同一個 `Field` 能用文字屬性切換帳號、密碼與其他欄位內容，也能在 Default、Focus、Error、Disabled 間切換；新增任務畫面則用 Select、Radio、Toggle、Checkbox 與多行文字欄表達不同選擇規則。自己的題目也完成依需求頁設計的表單、錯誤與修正後畫面。

下一次會把工作室任務排成可增刪的清單，並建立空清單與詳情畫面。今天練習的 Auto height、Hug contents、狀態元件與固定 Label，會直接用在長任務標題、篩選選項和清單操作。

完成條件：

- `Field` 元件能改 Label、Value、Helper，以 `Show helper` 控制說明文字，並在四種 State 間切換。
- 空白 `Screen / New Task` 起始為 402×874 並套用 `Surface`，含任務名稱、四選一的類別、優先順序、提醒設定、備註、必填的期限確認與提交動作；Select 展開版與提醒版內容超過 874 時以 Hug contents 或足夠高度完整顯示。
- Checkbox、Radio、Toggle、Select 與多行文字欄符合共用控制項規格。
- 自選題目的表單、錯誤與修正後畫面符合需求頁欄位。

想一想：為什麼「付款方式」適合單選，而「喜歡的書類」適合勾選？

<details><summary>查看答案</summary><p>一筆訂單只採用一種付款方式，選項彼此排斥，因此用 Radio；讀者可能同時喜歡多種書類，選項可以並存，因此用 Checkbox。</p></details>

## 本堂查證來源

- [Figma：Auto layout](https://help.figma.com/hc/en-us/articles/360040451373)
- [Figma：文字尺寸與 Layout](https://help.figma.com/hc/en-us/articles/27378154668951)
- [Figma：建立與使用 Variants](https://help.figma.com/hc/en-us/articles/360056440594)
- [Figma：Component properties](https://help.figma.com/hc/en-us/articles/5579474826519)

來源查證：2026-11-02。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
