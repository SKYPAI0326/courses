# uiux-designer 零基礎可讀性全課審查（2026-11-03）

- 版本：`claude/uiux-deep-review-3b8c69`，已含 PR #81 的 5 項修正
- 審查方式：4 個未繼承對話的 agent 分組逐段讀完 16 堂、START-HERE、reference、practice；講義中 49 張 `<img>` 全數打開比對；連結以腳本逐一確認
- 焦點：完全沒有設計與 Figma 經驗的學員，能否只靠講義讀懂並學會
- 共 76 項待修：高 5、中 33、低 38（L39 併入 M28，L40 為檢查結果說明）
- 「需要」欄：文字＝只改講義文字；素材＝改起始材料或下載包；截圖＝需 Figma／GitHub 實機重拍（未重拍前以圖說暫解）

## 每堂能否自學

| 堂 | 判定 | 主要原因 |
|---|---|---|
| A1 色彩字型 | 勉強 | 沒教套用文字樣式；直接輸入 Hex 的截圖與變數做法衝突；換你做缺建第二個變數集合 |
| A2 格線 | 勉強 | 桌面畫面與 Desktop / Main 父層步驟太跳 |
| A3 Auto layout | 勉強 | 示意圖按鈕寬度與規格矛盾；元件提前出現 |
| A4 元件 | 勉強 | 圖示 SVG 無法下載，圖示一節做不下去 |
| A5 Variant | 勉強 | 三張截圖紅框與文字不符；Stroke／屬性綁定入口沒交代 |
| A6 按鈕表單 | 勉強 | 全堂無截圖；Select 展開版、表單容器步驟太跳 |
| A7 清單內容 | 勉強 | Done 外觀無規格；詳情內容組裝不清 |
| A8 Toast／彈窗 | 勉強 | Detail / Content 名稱接不上；Toast 照數值會蓋住標題 |
| B1 線框原型 | 勉強 | 第一次原型連線沒教怎麼拖 |
| B2 觸發導覽 | 可 | 熱區未定義、一張截圖屬性名不符 |
| B3 轉場 | 可／勉強 | 點餐、會員題要用 B4 才教的 After delay |
| B4 Overlay | 可 | 彈層 Frame 沒說放在手機畫面外 |
| B5 捲動 | 勉強 | Sticky 與橫向卡片插入位置、卡片內容沒交代 |
| B6 任務測試 | 勉強 | 紀錄表缺測試計畫與走查欄位；沒保留修正前畫面 |
| B7 交付 | 勉強偏不可 | Note 元件照步驟做不起來；交付資料夾與 .md 檔沒有建立步驟 |
| B8 網站部署 | 勉強 | token 順序、USERNAME 佔位、截圖紅框錯位；換你做的不可選狀態做不到 |

## 高（做不下去）

| # | 堂 | 位置 | 問題 | 修法 | 需要 |
|---|---|---|---|---|---|
| H1 | A4 | part1/CH4:59、assets/shared/icons/README.html | 「從電腦上的 assets/shared/icons/」：網頁學員沒有這個資料夾，全課無圖示下載入口 | README 每個圖示加 `download` 連結並附 icons.zip；講義改寫成下載、解壓、拖入；README 返回連結改回 CH4 | 素材＋文字 |
| H2 | B1 | part2/CH1:78 | 「從登入按鈕拖出原型連線」：全課第一次建連線，沒教 Prototype 分頁與拖藍色圓點 | 補「切 Prototype → 選按鈕 → 拖右緣圓點到清單外框」並說明做完看到什麼 | 文字 |
| H3 | B7 | part2/CH7:40 | Note 用 Ellipse 做圓點，Ellipse 不能包子層，數字落在 Auto layout 外，Number 屬性建不起來 | 圓點改成 24×24、圓角 12、Fill Primary、內容置中的 Auto layout Frame，數字放裡面 | 文字 |
| H4 | B8 | part3/CH8:130 | 「一筆使用不能選的狀態」：app.js 只有 id／title／due／done，無程式經驗做不到 | 從 app.js 要求移除，只在 my-screen.html 做 | 文字 |
| H5 | B7 | part2/CH7:21（另見 16、30、34、49） | 「記入 spec/visual-rules.md」：交付資料夾、四個子資料夾、.md、README 從沒教過建立 | 示範開頭補建立資料夾與用 VS Code 新增 .md 的步驟，附最小範本 | 文字 |

## 中（容易做錯或誤解）

| # | 堂 | 位置 | 問題 | 修法 | 需要 |
|---|---|---|---|---|---|
| M1 | A3／A4 | part1/CH3:41 autolayout-reference.svg、CH4:36 | 示意圖寫 W Fill，規格是 W 322 Fixed；CH4 說原本是 Fill container | SVG 改 W 322 Fixed 並補 Hint；CH4 改成「原本就固定 322」 | 素材＋文字 |
| M2 | A3 | part1/CH3:63 | Create component 在 A4 教之前出現 | 補一句元件定義與「下一堂詳細說明」 | 文字 |
| M3 | A1 | part1/CH1:46 figma-fill-hex | 直接輸入 Hex 的截圖，與全程用變數的做法衝突 | 刪除此圖 | 文字 |
| M4 | A1 | part1/CH1:51 步驟 13 | 「再套用對應文字樣式」：只教建立沒教套用 | 補套用操作位置 | 文字 |
| M5 | A1 | part1/CH1:58 | 要學員寫出沒觀察過的結論 | 改成先貼入正式卡片觀察再 Undo | 文字 |
| M6 | A2 | part1/CH2:37 步驟 9、10 | 建桌面畫面沒給按 F／尺寸／改名；Desktop / Main 父層與座標基準未寫 | 補步驟與「座標以桌面畫面左上角為 0」 | 文字 |
| M7 | A4 | part1/CH4:59 步驟 2、3 | 沒說在外層 24×24 Frame 上建元件 | 寫明選外層 icon Frame，完成後 W 24、H 24 | 文字 |
| M8 | A1 | part1/CH1:76、80 | 沒教新增第二個變數集合、題目 Section | 補 Collections ＋ 與 Shift+S 建 Section 兩步 | 文字 |
| M9 | A5 | part1/CH5:37 figma-create-property-menu | 紅框框 Text，步驟要選 Variant | 圖說註明本步選 Variant | 截圖 |
| M10 | A5 | part1/CH5:59 figma-selection-colors-swap | 截圖選 Primary Pressed，不是同名變數 | 圖說註明本步選同名變數 | 截圖 |
| M11 | A5 | part1/CH5:72 | 斜線名稱加 Variant 會被拆開，沒要求改回 `題目名 / Status` | 比照 CH7 補改回原名一步 | 文字 |
| M12 | A5 | part1/CH5:30、38 | Stroke Outside、Inside stroke Excluded 沒說入口與原因 | 補入口位置與一句原因 | 文字 |
| M13 | A5 | part1/CH5:54 | 其他九個 Variant 連同一布林屬性沒說用既有屬性 | 寫明從清單選既有 Show icon，不按 ＋ | 文字 |
| M14 | A6 | part1/CH6:48 | 下拉選項沒說放進 Open=true 版本的 Auto layout | 補建立選項清單步驟 | 文字 |
| M15 | A7 | part1/CH7:36 | 詳情內容組裝「包起來」「以新按鈕取代」不清；未命名 | 改成依序步驟並命名 Detail / Content | 文字 |
| M16 | A8 | part1/CH8:29、35、42 | 引用 Detail / Content，前堂沒命名 | 由 M15 一併解決 | 文字 |
| M17 | A8 | part1/CH8:35 | Toast x24、y72 會蓋住標題與清單 | 重算位置或寫明是浮層 | 文字 |
| M18 | A8 | part1/CH8:35 | 桌面導覽只有一句 | 補規格表列與步驟 | 文字 |
| M19 | A7 | part1/CH7:31、51 | Done 版本無外觀規格，且只在 Done 加圖層會跳位 | 兩版本都放同一層，用顯示屬性或顏色區分 | 文字 |
| M20 | B1 | part2/CH1:34、40、48 | 要放在尚未建立的 IA 區旁，且與 IA 區用途矛盾 | 建 IA Section 移到第 3 節開頭，統一「放進 IA 區」 | 文字 |
| M21 | B1 | part2/CH1:80 | 連開 Present 與 Preview，沒說差別 | 第 6 步只找 Flow，不點播放 | 文字 |
| M22 | B1 | part2/CH1:69 flow-reference.svg | 示意圖無箭頭、無錯誤分支、多一個節點 | 依規格重畫 SVG | 素材 |
| M23 | B3 | part2/CH3:49 | 點餐、會員題要 B4 才教的 After delay | 降為 Before→After 兩狀態 | 文字 |
| M24 | B4 | part2/CH4:144 | 建 Overlay / Menu、Sort 沒說在手機畫面外 | 補「在手機畫面外按 F」與原因 | 文字 |
| M25 | B6／B7 | part2/CH6:53、CH7:53 | 沒要求保留修正前畫面，B7 卻要並排前後 | B6 修改前補複製 Before 畫面一步 | 文字 |
| M26 | B6 | part2/CH6:25、36、47 | 紀錄表沒有測試計畫與走查欄位，講義說可代替 | 刪「可用紀錄表代替」，統一用 Figma 文字框 | 文字 |
| M27 | B8 | part3/CH8:62–65 | push 之後才建 token | token 步驟移到 push 前，補 VS Code 登入視窗說明 | 文字 |
| M28 | B8 | part3/CH8:62、33–34 | USERNAME 與引號內文字沒說要換 | 補說明 | 文字 |
| M29 | B8 | part3/CH8:67 github-token-access | 紅框框 Account permissions，文字要 Repository permissions | 圖說註明 | 截圖 |
| M30 | B8 | part3/CH8:108 | Selection colors 只顯示變數名，讀不到色碼 | 改從 Local variables 讀 | 文字 |
| M31 | B8 | part3/CH8:128、130 | 預約 S06 名稱不長，測不到換行 | 改成用長說明測換行 | 文字 |
| M32 | B5 | part2/CH5:30、31、18、59 | Sticky／橫向卡片插入位置、卡片內容、短父 Frame 沒交代；主線要不要保留 Sticky 不一致 | 補 Layers 拖放步驟、卡片 W 200／H 140 與內容、短 Frame 做法，並寫明主線是否保留 | 文字 |
| M33 | B8 | part3/CH8:40 | Mac .DS_Store 讓「工作區會乾淨」對不上 | 疑難排解表加一列 | 文字 |

## 低（小困惑）

| # | 堂 | 位置 | 問題 | 修法 | 需要 |
|---|---|---|---|---|---|
| L1 | A1／A3 | CH1:51、CH3:37 | 置中沒指出按鈕位置 | 寫出 Alignment／九宮格位置 | 文字 |
| L2 | A1–A4 | CH1:65、CH2:58、CH3:67、CH4:61 | 「看兩版」沒附圖；CH2 標題與內容不符 | 標題改「想像兩版」，修 CH2 標題 | 文字 |
| L3 | A1 | CH1:51 步驟 11 | Fill 按 ＋ 會多疊一層 | 改成四點圖示套用 | 文字 |
| L4 | A4 | CH4:39 等三張 | 截圖元件名 Base，文字是 Primary | 圖說註明 | 截圖 |
| L5 | A2／A3 | CH2:18、CH3:21 | 「依本堂規格表補做」應為該頁 | 改字 | 文字 |
| L6 | A3 | CH3:57 | 桌面測試 Frame 沒尺寸、沒說怎麼放入 | 補 1200×400 與放入方法 | 文字 |
| L7 | A3 | CH3:63 | Tags Gap、文字樣式未指定；Card 360 寬 312 | 補規格與一句說明 | 文字 |
| L8 | A4 | CH4:84、EXPECTED-CHECK | 證據在要刪除的 Test 裡 | 刪除前截圖 | 文字 |
| L9 | A1 | CH1:19 | 已建檔又叫再建一次 | 補「已建檔者直接開原檔」 | 文字 |
| L10 | A5 | CH5:35 | 截圖顯示 Base／Variant2 | 圖說註明 | 截圖 |
| L11 | A5 | CH5:57 | 「最初的換你做」沒寫哪一堂 | 補 A1 與連結 | 文字 |
| L12 | A6 | CH6:48 | Detach instance 沒解釋 | 補一句 | 文字 |
| L13 | A6 | CH6:31、36 | 「保持 Focus」前沒切回 | 改字 | 文字 |
| L14 | A6 | CH6:48 | 表單容器沒命名與規格 | 補命名與規格 | 文字 |
| L15 | A6／A7 | CH6:36、CH7:41、43 | 橢圓矩形工具沒教；「包成」沒說 Shift+A；矩形位置 | 補快捷鍵與位置 | 文字 |
| L16 | A8 | CH8:35、42 | Warning／Error 副本留舊返回列；Nav 父層未確認 | 補步驟 | 文字 |
| L17 | A8 | CH8:29 | Overlay 一詞沒解釋 | 補一句 | 文字 |
| L18 | A5／A6／A8 | CH5:72、CH6:59、CH8:58、START-HERE | 換你做沒連需求頁；START-HERE 附無關 CSV | 補需求頁連結 | 文字 |
| L19 | B1 | CH1:61 | 第 7、9 節重複建同一線框 | 第 61 行改預告語氣 | 文字 |
| L20 | B1 | CH1:79 figma-overflow-flow-start | 多一個 Overflow 紅框 | 圖說註明 | 截圖 |
| L21 | B2 | CH2:54 figma-hover-change-to | 截圖屬性名不符 | 圖說註明 | 截圖 |
| L22 | B2 | CH2:55 | 「所有按鈕都會顯示 Hover」 | 改字 | 文字 |
| L23 | B2 | CH2:13 | 熱區未定義 | 補定義 | 文字 |
| L24 | B4 | CH4:144 | Help 副本的按鈕處理不清 | 寫明刪除或改成關閉 | 文字 |
| L25 | B4 | CH4:151 | 新 Toast 沒說改文字 | 補 Message 與 Type | 文字 |
| L26 | B4 | CH4 第 14 步 | 「最短時間」沒數字 | 寫「填 1」 | 文字 |
| L27 | B4 | B4 START-HERE | 規格表沒同步第 13～17 步 | 補一列 | 素材 |
| L28 | B4 | CH4 canonical、og:url | 指向不存在的 B4-overlay-single-action.html | 改成 CH4 檔名 | 文字 |
| L29 | B1／B2 | CH1:93、CH2:47、CH2:30 | 需求頁、CSV 沒連結；Row / T02 沒命名 | 補連結與命名 | 文字 |
| L30 | B5 | CH5:22 | 只給 Mac 快捷鍵 | 補 Ctrl+Alt+G | 文字 |
| L31 | B5 | CH5:50 | Preserve scroll position 沒教 | 補設定位置 | 文字 |
| L32 | B6／B8 | CH6:6、27、36、CH8:6 | 頁首時數與總覽不一致 | 對齊總覽 | 文字 |
| L33 | B6 | TASK-TEST-FORM | 範例「隔天再測」與講義矛盾 | 改範例 | 素材 |
| L34 | B6 | CAPSTONE-SCORE | 返回連結指到 section-6 | 改 section-12 | 素材 |
| L35 | B7／B5 | CH7:31 figma-file-menu、CH5:20 | 多餘紅框 | 圖說註明 | 截圖 |
| L36 | B7 | CH7:47 | 看像素寬高沒說 Mac／Windows 做法 | 補一句 | 文字 |
| L37 | B7／B8 | CH7:14、CH8:16、27、70 | Dev Mode、repo、main、Actions、靜態網站未解釋 | 第一次出現補定義 | 文字 |
| L38 | B7 | HANDOFF-CHECK | 「若由同學驗收」違反不設計學員互動 | 刪除 | 素材 |
| L39 | B8 | CH8:33–34 | 引號保留說明 | 併入 M28 | 文字 |
| L40 | 全課 | — | 圖片與連結 | 連結全部存在、無轉義 HTML；A1 對比值重算正確 | — |
