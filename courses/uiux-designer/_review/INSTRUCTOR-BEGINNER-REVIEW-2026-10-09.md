# 講師視角與零基礎閱讀審查

日期：2026-10-09。對象：`uiux-designer` 現有講義。範圍：唯讀審查；未改教案、HTML、素材或 Gate。

結論：目前適合作為講師備課草稿，尚不足以直接作為零基礎學員的正式操作講義。講師可以補充後使用部分活動，但需要補核心步驟、修正平台前提與成果交接，不能只做句子精簡後就放行整門課。

文案確實有閱讀負擔：抽象名詞密集、英文欄位提早出現、檢核與未測提醒反覆占據正文；必要的概念、操作與判斷理由反而不足。這會讓學員記住「要留下什麼證據」，卻不知道如何做出作品。

## 審查範圍與證據界線

- 逐頁閱讀總覽與 16 個正式單元的可見文字，核對 16 個起始材料頁。
- 對照目前大綱、Style Guide、內容實質與學員任務規範；抽查 A3、A6、B8 教案完整內容，並查閱其餘教案的目標／章節資料，未宣稱完成 16 份教案逐句保真審查。
- 查閱代表檢查表、B6 測試表、B7 交付表、web-starter 原始檔，以及舊 Probe／Gate 記錄。
- 本次解析 50 個相關 HTML 的本地相對檔案連結：250 個連結，0 個檔案缺失。此結果只證明檔案存在；未驗證遠端 Figma 權限或 HTML 錨點，也不能證明步驟可完成。
- 16 個正式單元沒有內嵌 `img`、`video` 或 `iframe`。第 12 堂有外連 PNG 參考，第 1 堂有官方說明連結，不能因此稱為完全沒有視覺資源。
- Figma 平台前提以本次取得的官方文件核對；沒有登入學員帳號重跑平台，沒有真人計時入口測試或完整跟做，也沒有重新跑既有 lint。因此本報告是內容／教學語意審查，不是平台或真人放行。
- [_gates.md](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/_gates.md:206>) 最後一筆既有紀錄仍是待人工驗證。本次另找到實際內容與前提缺口，不能將它們全部歸為「只是少了真人證據」。

## 逐堂判斷

「可保留」表示活動方向有用，不代表已通過真人或平台驗收。

| 堂次 | 講師判斷 | 零基礎主要卡點／修訂重點 |
|---|---|---|
| 01 色彩與字型 | 可保留，需調整閱讀節奏與概念 | 起始操作比其他堂完整；大量選取提醒重複。字型、行高、可讀性判斷不足，需成品及前後對照。 |
| 02 格線 | 需補引導 | Layout guide 的入口、Columns／Stretch 定義與列表起始內容不足；需展示物件跨欄及對齊例子。 |
| 03 Auto Layout | 核心阻塞 | 沒有建立 Auto Layout 的完整操作；把文字 Auto height 與容器 Hug 混寫，卻要求下方按鈕自動移動。 |
| 04 Component／Instance | 可保留，需補核心示範 | 能建立來源與實例，但未實際修改來源並觀察同步；Create component 的入口也太簡略。 |
| 05 Variants／Properties | 可保留，需補對照 | 狀態／欄位／選項的區分有用；需具體面板例子。以錯誤訊息替換登入標題的案例理由不足。 |
| 06 Button／Form | 核心交接阻塞，內容偏薄 | 第 5 堂沒產生所要求的 Frame；按鈕未加文字，也未做兩種視覺差異。表單主要停在命名。 |
| 07 List | 需補結構教學 | 兩個矩形與一段文字不足以教會列結構；長標題沒有示範如何推開下一列，空狀態也沒有完整畫面對照。 |
| 08 Toast／Dialog／Navigation | 需補結構教學 | 以 Rectangle 當容器，卻要求把文字放在其「內」；未交代 Frame／群組及父子層。主要只畫外觀和命名。 |
| 09 線框與原型入口 | 可保留，需補引導 | 任務卡與畫面清單有教學價值；需完成線框參考、按鈕物件命名及起始點入口。Solo 又只換長文字。 |
| 10 觸發事件 | 平台前提與交接阻塞 | 把同觸發多動作誤寫成全檔限一動作；`Button / Login` 沒有前課建立／改名路徑。 |
| 11 轉場 | 需補可重現例子 | 沒有具體速度設定與匹配層差異；Smart animate 可填未觀察，尚不足以驗收動效能力。 |
| 12 Overlay／Swap | Overlay 活動可保留，需修前提與 Swap | 點擊整個 Host 可教最小原型；與原承諾的完成按鈕情境有落差。Swap 沒有完整 action／hotspot／預覽示範。 |
| 13 滾動／固定／漂浮 | 核心操作不足 | 有 Vertical 設定，但 Header 固定只寫「測試固定設定」；未教面板位置、選項及 Fixed／Sticky 差異。 |
| 14 任務測試 | 相對完整，需整理前後依賴 | Expected／Actual 與故意清空 Destination 的修復活動可保留；第 13 堂滾動案例沒有接入實際測試腳本。 |
| 15 Handoff／輸出 | 免費路徑阻塞，課綱內容缺口 | Dev Mode 不適用 Starter 主線；Export 步驟太薄。Photoshop 與總覽所列 Smart Animation 未形成完整教學。 |
| 16 Web／Git／部署 | 零基礎起點與課綱交付阻塞 | 沒有本機專案取得／Git 初始化路徑；DOM、selector、breakpoint 未教就使用。GitHub／部署沒有可執行章節。 |

## BLOCKER：會卡住操作或使整門課無法達成承諾

### B01｜第 3 堂沒有教出 Auto Layout，卻要求自動重排

- 類別：教學實質／可跟做性。
- 位置：[第 3 堂概念、示範與跟做](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH3-auto-layout-pressure.html:22>)，起始材料第 4–5 行；教案 A3 第 19–44 行也存在相同缺口。
- 原文：「將文字容器高度改為 Auto height／Hug；容器向下增高，錯誤輔助文字與按鈕一起往下移。」
- 問題：正文沒有交代建立哪個容器、選哪些子層加入 Auto Layout、方向／間距／內距如何設定，也沒有建立用來觀察移動的按鈕。文字自動增高不會單獨教出相鄰物件的重排。
- 官方核對：文字 Auto height 與 Auto Layout Frame 的 Hug contents 是不同層級的設定；Hug 適用於 Auto Layout Frame。[Auto Layout 官方說明](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout-in-Figma)、[文字尺寸官方說明](https://help.figma.com/hc/en-us/articles/30938465113751-FD4B-Build-your-bio-using-text-layers)。
- 修訂：提供短句、按鈕及父層的完整結構；逐步建立垂直 Auto Layout，再分開設定文字 Auto height 與父層 Hug。完成例子要實際展示按鈕隨長句往下移。

### B02｜把付費的「同觸發多動作」誤判為「一檔一動作」

- 類別：專業正確性／課程前提。
- 位置：[第 10 堂](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH2-trigger-navigation-action.html:9>)、[第 12 堂](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH4-overlay-single-action.html:150>)，並延伸到第 14 堂與起始材料。
- 原文：「同一檔第二個 action 會要求升級。」
- 問題：把平台限制擴大到整份檔案，使正常的登入、清單、彈窗流程被拆成互不相連的測試檔，還要求學員將這個錯誤前提當作測驗答案。
- 官方核對：一般原型連線適用所有方案；付費的 multiple actions 是同一 trigger 下堆疊多個 actions。[連接原型](https://help.figma.com/hc/en-us/articles/360040315773-Connect-your-prototype)、[Multiple actions and conditionals](https://help.figma.com/hc/en-us/articles/15253220891799-Multiple-actions-and-conditionals)。
- 既有 Probe B 第 19 行確實記錄升級提示，但沒有證明是在不同物件建立獨立 interaction。由官方文件與紀錄推論，可能混用了新增 interaction 與同一 interaction 的 Add action；本次沒有重跑，不能斷言當時點了哪個控件。
- 修訂：修正大綱、教案、HTML、材料、檢查題及 Probe 結論；用免費帳號另驗證兩個按鈕各一條 interaction，再示範同一觸發的第二個 action，分清兩種操作。單動作可以作為初學練習安排，不能宣稱為整檔上限。

### B03｜前後堂要求的物件沒有建立，檢查表又使用另一份規格

- 類別：完成物交接／一致性。
- 位置：[第 6 堂跟做第 1 步](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH6-button-form.html:25>)、[第 10 堂跟做第 3 步](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH2-trigger-navigation-action.html:13>)、[第 3 堂檢查表](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/assets/A3-auto-layout-pressure/reference/EXPECTED-CHECK.html:12>)。
- 問題：第 6 堂要求從第 5 堂檔案選 `Screen / List Top`，但第 5 堂沒有建立這個 Frame 的路徑，材料頁也只是列名。第 10 堂要選 `Button / Login`，第 6 堂只有 `Button / Primary`，第 9 堂加入按鈕文字卻未交代此命名。
- 第 3 堂正文使用 `Mobile / Login & List`，檢查表改為 `Screen / Login`，並要求增刪文字與 360px 窄畫面，而正文並未完整教做這些測試。學員可能照正文完成，仍無法照表驗收。
- 修訂：建立唯一物件名稱與產物規格；明確教建立／複製／改名，讓下一堂指向實際完成物。檢查表只驗收當堂已教的能力，新增測試須同步補正文。

### B04｜第 15 堂要求 Starter 學員使用 Dev Mode

- 類別：環境／權限契約。
- 位置：[第 15 堂輸出與 Inspect](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH7-figma-handoff-export.html:10>)、[材料頁](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/assets/B7-figma-handoff-export/START-HERE.html:5>)、[交付檢查表](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/assets/B7-figma-handoff-export/reference/HANDOFF-CHECK.md:8>)。
- 問題：免費主線要求「切換 Dev Mode」，沒有可完成的免費替代操作；「只記錄可見控件」無法解決學員沒有此功能的問題。
- 官方核對：Starter 沒有 Dev Mode；仍可在 Design Mode 做基本檢查。[Starter plan overview](https://help.figma.com/hc/en-us/articles/13838684089751-Starter-plan-overview)、[Guide to inspecting](https://help.figma.com/hc/en-us/articles/22012921621015-Guide-to-inspecting)。
- 修訂：免費主線改教 Design Mode 的尺寸、顏色、間距、匯出與可用程式碼複製；Dev Mode 另列有相應方案／seat 才適用的補充。舊 Probe C 的帳號／seat／檔案所屬 team 條件須查清，不能直接推廣到全體 Starter 學員。

### B05｜第 16 堂從 Git status 起跑，省略零基礎必需的起點

- 類別：素材取得／環境／可跟做性。
- 位置：[第 16 堂](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part3/CH8-web-git-deploy.html:7>)、[Git 段落](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part3/CH8-web-git-deploy.html:11>)、[README](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/web-starter/README.md:7>)。
- 問題：已有三個原始檔，但沒有讓線上學員下載成可編輯資料夾的完整入口，沒有教 VS Code 開資料夾、開終端、Git 安裝確認、repository 初始化／取得及第一次 commit。`git add uiux-designer/web-starter/...` 也沒有指定執行目錄。
- README.md 要求啟動本地伺服器卻沒有命令；README.html 又直接開 index.html。教材把作者已有 repository 的起點套到學員。正文還要求讀 DOM、selector、breakpoint，未先用程式例子教會。
- 修訂：交付可下載專案，指定資料夾與終端目錄；建立可從空白環境開始的 Git 路徑及基準版本。展示一行標題修改的前後差異，再教 status、diff、add、commit 與實際恢復。只改 HTML 時，預期 diff 也應只出現 HTML。

### B06｜總覽承諾的 Photoshop、GitHub 與部署沒有正式教學路徑

- 類別：課綱／成果對齊。
- 位置：[總覽第 15、16 堂](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/index.html:101>)、[第 15 堂](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH7-figma-handoff-export.html:12>)、[第 16 堂](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part3/CH8-web-git-deploy.html:15>)、[第 16 堂材料](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/assets/B8-web-git-deploy/START-HERE.html:6>)。
- 問題：總覽列出 Photoshop 輸出、GitHub 與公開部署；正式頁把它們列為未驗收或 release gate。材料頁叫學員依講義 Gate 建 repository／push／部署，講義卻沒有那段操作。這是缺教材，並非已有完整教材只待實測。
- 修訂：若維持現有課綱，補 Photoshop 實際素材與開檔／修改／輸出、GitHub repository／push、明確平台部署與公開網址驗收；若縮減課程，必須同步調整總覽、大綱與成果承諾。
- 學員操作課不應引用 AI 作者的外部發布確認流程作為課程知識。「何時可以討論 GitHub？使用者明確確認 release gate」屬製作流程滲入教材。

## MAJOR：可以靠講師補充，但現有講義教學力不足

### M01｜第 6～8 堂偏重畫形狀與命名，缺少介面設計方法

- 類別：教學實質。位置：[第 6 堂示範](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH6-button-form.html:23>)、[第 7 堂示範](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH7-list-content.html:22>)、[第 8 堂示範](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH8-toast-dialog-navigation.html:22>)。
- 按鈕沒有標籤、內距、對齊及可辨識的 Disabled 外觀；兩個狀態主要只是不同 Value 名稱。Primary 是行動層級，Disabled 是可用性，講義沒有說清楚它們屬於不同判斷軸。
- List 使用兩個矩形，沒有完整列內文字／容器／下一列的結構。空狀態放了文字，卻沒有「有資料」與「無資料」兩份完整畫面的比較。
- Toast／Dialog 用矩形做底，但後文的「內」「子層」「容器」沒有對應結構操作。零基礎學員需要知道把底色與文字包在哪個 Frame 或群組，不能由命名推得父子關係。
- 建議：保留命名，補一個完整、可比較的 UI 元件及使用畫面；教理由與選擇，不要求此階段就完成真實資料輸入或後端功能。

### M02｜第 4 堂沒有展示主元件修改如何同步 Instance

- 類別：概念／示範。位置：[第 4 堂示範及驗收](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH4-component-instance.html:26>)。
- 來源與實例的同步是建立元件的主要理由，正文卻主要驗收名稱、Assets 與 disabled 面板。這不足以讓學員辨認元件與普通複製的差異。
- 建議：插入兩個 Instance，修改一次來源的字色或間距，觀察兩個使用處同步；再展示一個文字 override 的影響。不要把「控制呈 disabled」當作主要學習成果。

### M03｜第 11～13 堂把未完成的核心能力變成「可填未觀察」

- 類別：示範／評量。位置：[第 11 堂 Solo](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH3-transition-motion-purpose.html:8>)、[第 12 堂 Swap](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH4-overlay-single-action.html:202>)、[第 13 堂跟做](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH5-scroll-fixed-floating.html:7>)。
- Smart animate 沒有指定相同層名／父鏈及前後位置差異的完整例子；只換選單值不足以保證看到要學的效果。轉場速度與方向也缺可操作的設定示例。
- Swap 只寫「待測 Swap action」，沒有完整選項名稱、觸發物件與開啟／替換的過程。應分清 Swap overlay、Navigate to 及元件狀態 Change to 的用途。[Prototype actions](https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions)。
- 固定 Header 寫「測試固定設定」，修復又寫「回第 6 步」，該步本身沒有面板操作。學員繞回同一個缺口。
- 建議：各提供一個能重建的完整例子與成功結果；未執行可作誠實的進度記錄，但不能等同已學會核心能力。

### M04｜第 13 → 14 → 15 → 16 堂的成果鏈沒有真正串起來

- 類別：整合／前後承接。位置：[第 13 堂結尾](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH5-scroll-fixed-floating.html:10>)、[第 14 堂測試](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part2/CH6-prototype-task-test.html:9>)、[第 16 堂檔案介紹](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part3/CH8-web-git-deploy.html:8>)。
- 第 13 堂說要把第 10 筆是否可見、Header 是否固定、按鈕是否遮擋交給第 14 堂。第 14 堂實際腳本卻回到第 12 堂點 Host 開 Overlay；補一段 SCROLL-01 保存提醒沒有形成真正的滾動測試。
- 第 16 堂也沒有把第 15 堂尺寸、色值、圖檔逐項映射進網站，只使用已完成的另一份 task-card。沿用同一故事不等於沿用作品。
- 建議：明確選一份逐堂累積的作品；第 14 堂加入第 13 堂真實腳本，第 16 堂至少實作一次交付規格到 CSS／HTML 的對照。

### M05｜多堂 Solo 只是再換一段長文字，能力增量有限

- 類別：練習／重複控制。位置：第 1、3、5、6、7、8、9 堂的「自己改一個條件」；第 10 堂只換目的地標題，第 16 堂也只換任務標題。
- 長文字壓力測試本身有價值；但元件、狀態、表單、彈窗與流程多堂都以換字驗收，學員沒有被要求運用新方法做不同判斷。部分「記錄一個修正點」也強迫沒有錯誤的作品填出問題。
- 建議：第 4 堂驗收來源同步，第 5 堂自行設計新狀態，第 6 堂判斷欄位錯誤與按鈕可用性，第 7 堂增刪一列並維持間距，第 8 堂選擇何時用 Toast／Dialog。保留有目的與回饋的同素材重練。
- 第 14 堂故意清空 Destination、第 15 堂故意漏掉 Overlay PNG 的活動相對有實質，值得保留。

### M06｜抽象詞與英文字比新手所需更多，提示又反覆出現

- 類別：Style／敘事。位置：第 1 堂第 46–74 行、第 6～8 堂各第 18–30 行、第 10～16 堂的成果／驗收段，及各材料頁「工作位置」。
- 「工作位置」「欄位責任」「狀態來源」「視覺 Value」「文字責任」「可重讀」「聯合行為」「可回歸」「證據邊界」不如具體物件與動作直觀。
- `CASE-B2-01`、`Input`、`Expected`、`Actual`、`case_id`、`repair`、`rerun_result`、`release gate` 常先列出，才解釋用途；表單代碼容易被誤認成另一個工具或功能。
- 第 1 堂選取 Page／Frame／文字的提醒有用，但分散於示範、跟做、Checkpoint、判斷方法、修復表；第 6～8 堂又在開頭、概念、跟做、Solo、修復、驗收、測驗與頁尾反覆談未測邊界。
- 建議：關鍵操作旁保留必要提醒，重複說明集中到一張排錯表；每堂只要求當堂必要紀錄。名詞先中文白話，再括號保留工具面板英文。不能只刪字而把必要數值或錯誤恢復刪掉。

### M07｜檢查表要求填寫與保存，卻沒有教用哪個工具完成

- 類別：成果取得／記錄方式。位置：[第 1 堂檢查表](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/assets/A1-visual-foundations/reference/EXPECTED-CHECK.html:23>)、[第 14 堂測試表](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/assets/B6-prototype-task-test/reference/TASK-TEST-FORM.html:1>)。
- HTML 內的備註多為 `<span class="line">` 或底線，B6 是靜態表格，沒有可輸入欄位或保存機制。勾選框也沒有在本頁提供保存流程。課程沒有指定列印、複製到文件或下載可填寫表格。
- 第 14 堂講義要求先寫 Expected；材料頁卻叫先點擊、再填 Expected／Actual，順序需要同步。
- 建議：提供單一明確方式，例如複製可填寫文件到自己的資料夾，示範檔名、填寫、保存與交付；Expected 在操作前寫，Actual 在觀察後填。

### M08｜視覺基礎缺少足夠的視覺判斷示範

- 類別：概念／評量。位置：[第 1 堂概念](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH1-visual-foundations.html:30>)、[第 1 堂文字設定](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH1-visual-foundations.html:54>)、[第 2 堂示範](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/part1/CH2-grid-layout.html:21>)。
- 第 1 堂主要教固定字級與色碼，字族與行高沿用初值，卻要求學員判斷閱讀順序、可讀性及第一視覺焦點。第 2 堂要求共享欄線，沒有展示跨欄與版面安排。學員缺少可比較的好／壞例子。
- 16 頁沒有內嵌操作圖或成品圖不是單獨退件理由；這門課大量依賴視覺位置與層級，必要參考又主要留給外部官方頁，會增加零基礎學員的比對成本。
- 建議：在真正需要視覺判斷的地方加入標註截圖及前後對照，指出「哪裡變了、為什麼較容易讀」。優先補示範，不擴張成完整品牌或 UX 研究課。

## 遣詞用字：具體改寫示例

以下是修訂方向，尚未寫回講義。牽涉缺步驟的例子仍需先補教學事實。

| 原文／原詞與位置 | 閱讀問題 | 建議表述 |
|---|---|---|
| 「你以阿凱的工作位置接手一張登入畫面。」第 1 堂第 14 行 | 角色介紹繞遠 | 「你要替工作室整理一張登入畫面。」 |
| 「主要行動與欄位責任清楚可找。」第 6 堂第 16 行 | 責任與可找都抽象 | 「讓使用者看得出要填哪個欄位、按哪個按鈕。」 |
| 「每個中間結果都要在 Layers 或 Properties 讀得到。」第 6 堂第 23 行 | 先談驗收，沒有具體結果 | 「選取按鈕後，右側應看到 Primary 和 Disabled 兩個選項。」 |
| 「用可重讀的名稱完成清單材料。」第 7 堂第 24 行 | 標題無法告訴新手要做什麼 | 「建立兩筆清單，為每筆加上標題。」 |
| 「先確認三個 Layer 的責任。」第 8 堂第 24 行 | 用責任代替功能 | 「分別確認：提示說明結果、彈窗讓人確認或取消、導覽顯示目前位置。」 |
| 「一條可回歸 action。」第 10 堂第 7 行 | 英文與測試術語堆疊 | 「一條能重複測試的點擊連結。」 |
| 「固定與滾動的聯合行為。」第 13 堂第 6 行 | 看不出要觀察什麼 | 「捲動清單時，頂端導覽仍留在原位。」 |
| 「只改一個主要變因，再用同一任務回歸。」第 14 堂第 5 行 | 變因與回歸沒有具體對象 | 「一次只改一個設定，再照原本步驟測一次。」 |
| 「凍結來源版本。」第 15 堂第 9 行 | 新手可能以為有 Freeze 功能 | 「複製測試通過的 Figma 檔，作為交付版本。」需另教複製與命名。 |
| 「可審計版本／release gate。」第 16 堂第 5、11 行 | 製作治理名詞進入學員正文 | 「能看出改了哪裡的版本／發布前檢查。」但仍須補完整 Git 與部署路徑。 |

英文保留於對應工具時有用，例如首次寫「預期結果（Expected）」；不需要把整份學習活動都換成英文字段。長操作應按真正的動作拆開，避免一段塞入正常流程、平台說明、所有異常與證據要求。

## MINOR：順序與呈現需要整理

- 第 14～16 堂的 `(09)` 出現在 `(08)` 前，閱讀順序不直觀。另有 A／B 代號、NOT_RUN、反引號直接出現在學員頁，與正式堂次命名混用。應統一學員用語，但不為形式重排有用內容。
- 第 12 堂稱「四個概念」，實際段落又塞入第五項「一檔一核心 action」；該項本身還是錯誤平台前提。先修內容，再整理標題。

## 修訂先後與授課驗收

1. 先修平台事實、Auto Layout 核心步驟、前後物件名稱與 Git 起點。這些問題會使學員直接停住。
2. 補第 6～8 堂的完整介面示範、第 11～13 堂動效／Swap／固定操作，以及課綱承諾的 Photoshop、GitHub／部署內容。
3. 決定一份逐堂累積的作品；同步正文、材料與檢查表，讓測試、交付及網站實際接手前課成果。
4. 再精簡文案：先說可見問題，再說要做的動作，最後說應看到的結果。合併重複邊界提醒，保留必要操作與修復。
5. 讓零基礎試讀者只拿講義與提供的材料，連做第 1→2→3、第 4→5→6、第 12→13→14、第 15→16。記錄需要提示的原句、缺步驟與完成物；平台免費路徑另以乾淨帳號驗證。

這輪審查不以時數、字數、區塊數或 lint 成績推斷內容充實度。講師可自行調節上課節奏；講義仍須讓每堂有不同且能完成、能解釋的學習成果。

## 補充：課程完整度

本節補充「課程還缺哪些教學內容與整合成果」。這些是審查與補課規格，尚未寫入教案或 HTML，也未製作或驗證所列的新素材。

整體判斷：現有章節名稱涵蓋多數課綱主題，但教學深度與能力證據不足；部分必教內容只被列成待測，最後也缺少一份真正串起各堂的作品。不能以 16 個頁面齊備代表完整課程。

### 原始課綱核對

本次直接檢視原始圖片：[42 小時課綱](</Users/paichenwei/Downloads/1788509783989.jpg>)、[57 小時課綱](</Users/paichenwei/Downloads/1788509797593.jpg>)，再對照現有頁面與 [Coverage Matrix](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/uiux-designer/_design/99h-coverage-matrix.md:30>)。

42 小時來源列出 12 個主題。57 小時來源先列線框、工具、手機介面與原型應用，後面再列 9 個項目；其中「網頁設計入門」與「雲端佈署」分開列出。現有矩陣將兩者合為 `57-09`，本次拆開審查，避免本機網站掩蓋部署缺口。

下表「現況」依實際講義內容判斷，並未將缺少真人驗證一律視為缺教材。涉及操作缺口的引用位置見前述 B01–B06、M01–M08。

### 42 小時內容：從規則到完整介面

| 原始課綱項目／現有堂次 | 現況 | 需要補的教學 | 最低可觀察成果 |
|---|---|---|---|
| 色彩系統／01 | 有固定色碼與用途命名；缺選色與可讀性判斷 | 背景、文字、主要行動、錯誤／成功的用途；同一畫面的好壞對照與修正理由 | 一份色彩規則及實際套用畫面，能解釋每色用途 |
| 字型系統／01 | 有字級；字族與行高沿用初值 | 字族、字重、行高與資訊層級；中文長段落、按鈕文字與錯誤訊息的比較 | 文字樣式表、短／長文字畫面與閱讀判斷 |
| 格線系統／02 | 有手機／桌機數值；跨欄示範不足 | Columns／Stretch 的操作、內容跨欄、欄間距與物件間距差別、縮窄時如何調整 | 同一組內容的手機／桌機版，標明對齊線與跨欄 |
| Auto Layout／03 | 固定文字寬度與增高；核心配置不完整 | 水平／垂直排列、內距、間距、對齊、Hug／Fill／Fixed 的不同用途 | 長文字、增刪一列及縮窄後仍不重疊的區塊 |
| Component／04 | 會建立來源與 Instance；同步示範不足 | 何時抽成元件、一般複製與 Instance 差別、來源修改與使用處覆寫 | 兩個 Instance 隨一次來源修改同步，並能指出覆寫內容 |
| Button／06 | 有矩形與 Value 命名；可見設計不足 | 主要／次要行動、標籤、內距與對齊；一般／不可用狀態與使用情境 | 有文字、可辨識層級與狀態的按鈕組 |
| Form／06 | 只有 Label／Input／Helper 三層 | 必填、一般、錯誤、修正後狀態；錯誤文字應出現在哪裡及如何提示修正 | 至少兩個欄位的靜態表單，能展示錯誤及修正後畫面 |
| List／07 | 有兩個矩形、長標題與空狀態文字 | 列內資訊結構、列間距、長標題增高、增刪資料列、空／有資料畫面切換 | 一份可增刪列且保持間距的清單與獨立空狀態畫面 |
| Toast／08 | 只有成功文字 | 成功、警告／失敗的訊息差異；短提示何時足夠，何時要要求確認 | 同一個操作的回饋選擇及理由，附完整提示畫面 |
| Dialog／08 | 有底框與確認／取消文字 | 標題、說明、行動層級、關閉規則與背景阻擋的設計 | 確認彈窗元件與開啟／取消／確認規格 |
| Navigation／08 | 三個選項文字；缺目前頁與手機規則 | 目前頁、可去的頁面、選取樣式、桌機與手機配置 | 能辨認目前位置的導航元件與兩種版面 |
| Variants／05、06 | 有兩個狀態與切換；跨元件運用不足 | 屬性名／值、來源／Instance 關係；把狀態規則用到 Button／Input／Navigation | 至少一組完整狀態表及可切換的 Instance，與畫面用途對應 |

Form 在這一階段可用設計畫面展示狀態，不必加入後端驗證；List 增刪先驗收 Figma 的版面重排，不必做動態資料服務。這能補足原有課綱，也維持介面設計與互動課的分工。

### 57 小時內容：從畫面到可交付作品

| 原始課綱項目／現有堂次 | 現況 | 需要補的教學 | 最低可觀察成果 |
|---|---|---|---|
| 線框、工具、手機介面與原型應用／09 | 有任務卡、畫面清單與 Frame；線框設計方法不足 | 線框與視覺稿的用途、資訊優先順序；一份完整線框到既有元件組成畫面的示範 | 同一需求的線框、手機畫面及任務路徑，能解釋內容安排 |
| 觸發事件與互動連結／10 | 一條 Navigate；免費方案前提有誤 | 選對觸發物件、Navigate／Back、返回與錯誤路徑；修正一檔一 action 說法 | 能走完並返回的基本任務流程，沒有只能前進的死路 |
| 互動與轉場效果／11 | 有選項與理由表；具體設定不足 | 至少兩種轉場的速度、方向與任務用途；完整設定與 Preview 對照 | 可比較的兩種效果，並說明保留哪種及原因 |
| Overlay 基礎與進階／12 | 只教置中的確認文字 | 置中 Dialog 與另一種選單／底部面板；位置、背景、遮擋、點外部／關閉按鈕規則 | 兩種可開啟與關閉的 Overlay，各符合使用情境 |
| Swap 搭配 Overlay／12 | 只有另檔待測要求 | 完整開啟第一個 Overlay、觸發 Swap overlay、替換內容與關閉／回到主畫面的示範 | 一條真正替換 Overlay 的流程，能分辨替換與新增疊層 |
| 滾動、置頂與漂浮按鈕／13 | 有 Vertical；固定與漂浮操作不完整 | 滾動內容與視窗的層級、Scroll with parent／Fixed／Sticky 的差異；固定入口與遮擋修正 | 滾動到末筆時仍能看見必要入口，按鈕不遮住內容；有設定與 Preview |
| Smart Animation／11、15 | 主要是選下拉值；成功與失敗例不足 | Matching layers、名稱／父鏈、可變屬性與動效設定；一個故意匹配失敗的修復例 | 一段可觀察的連續變化，以及修正前後的失敗紀錄 |
| Figma／PS 發布規劃與輸出／15 | Figma 部分輸出；PS 未形成正式教學 | 交付對象、格式、倍率、透明背景、命名／版本；PS 的開檔、圖層、尺寸調整、保存與輸出 | Figma 來源、可重開 PSD、實際輸出檔及讓同伴能取用的清單 |
| 網頁設計入門／16 | 能看與點已完成範例；自行製作支援不足 | HTML 結構、CSS 選取與版面、相對路徑、手機寬度；最小按鈕事件；設計規格如何寫進程式 | 由學員修改或完成的頁面，至少展示一次設計稿到 HTML／CSS 的對照 |
| 雲端佈署／16 | 無正式操作段落 | 指定單一部署平台、repository／push／發布設定、公開網址、更新版本及常見失敗修復 | 另一個人能開啟的公開網址，對應 repository 版本與部署紀錄 |

Git／GitHub 與最小 JavaScript 已納入目前核准的大綱，補課時讓它們服務這份網站；不擴張成獨立工程課。任務測試與交付整理則沿用第 14、15 堂的有用活動，補足作品依賴。

### 最需要補齊的整合成果

目前登入、清單、Overlay、滾動與網站多為各自的測試片段。建議沿用「工作室待處理清單」，安排一份逐堂累積的作品：

1. 登入畫面：一般與錯誤兩種介面狀態，清楚說明這是原型模擬。
2. 任務清單：有資料、長標題與空狀態，套用已建立的色彩、字型、格線與元件。
3. 任務詳情：從一筆清單進入，完成或取消後能返回。
4. 完成確認：打開 Dialog；取消可回原畫面，確認後有回饋。
5. 長清單：能捲動到末筆，導航與必要操作維持可見，沒有遮擋。
6. 選單／面板：用同一作品的支線示範第二種 Overlay 與 Swap；Smart animate 則選一個能看見前後差異的狀態。
7. 交付與網站：由這份作品取得尺寸、色值與資產，完成交付包，再做成對應的最小網站並發布。

上述為待補的示例規格，不宣稱現有檔案已具備這條路徑。原型可以模擬登入、錯誤與完成狀態；網站保留課綱所需的最小互動，資料庫與真實帳密驗證無須加入。

主線與額外功能示範要分清：多種轉場或 Overlay 可用同一作品的比較支線教，不必把所有功能硬塞進使用者的單一路徑。

### 建議補課包與放入位置

| 補課包 | 放入現有單元 | 必須先提供的材料 | 補課後怎麼驗收 |
|---|---|---|---|
| 視覺與排版判斷 | 01–03 | 同一內容的前後對照、樣式規則、可編輯排版起始檔 | 學員修正一個新排版問題，說出理由；長文、增刪與窄版都能檢查 |
| 元件與狀態設計 | 04–08 | 完整按鈕／雙欄位表單／清單的起始與完成範例、狀態表 | 來源修改能同步；學員能選對狀態與回饋方式，完成完整介面 |
| 線框到完整手機畫面 | 09–10 | 任務需求、低細節線框、完整畫面參考及物件對照 | 每個畫面對應任務，點擊與返回路徑沒有死路 |
| Overlay／Swap／動效／滾動 | 11–13 | 成功與故意失敗的可編輯例子，必要層級與設定圖 | 各核心效果在 Preview 出現，學員能自行診斷一個新錯誤 |
| 任務測試與修正 | 14 | 可保存的測試表、主線與滾動任務、完成與失敗範例 | 同伴依任務自行操作；問題、修正及同一任務重測可追蹤 |
| PS 與設計交付 | 15 | 實際可開啟的分層 PSD／原始圖片、Figma 來源、輸出規格及完成包 | PSD 能重開；格式、尺寸、透明背景與命名符合用途，同伴能找到所需檔案 |
| 網站、版本與部署 | 16 | 可下載專案、學員專用空白工作目錄、範例差異、明確部署平台路徑 | 本機與公開頁面一致；手機可用；一次更新能對應到 Git 版本 |

起始檔、完成檔與錯誤檔須真的製作並檢查能開啟。材料名稱與規格只能當製作清單，不能再拿來代替實檔。

### 練習與評量還要補哪一層

目前多堂要求照值設定、命名、截圖，獨立練習又只換文字。完整課程至少還要讓學員：

- **做選擇**：這個結果用 Toast 還是 Dialog？這個尺寸用 Hug 還是 Fill？提出與案例相關的理由。
- **處理新條件**：新增一個表單欄位、一種狀態、一筆較長資料或一個返回路徑，沿用已學方法完成。
- **找出錯誤**：從作品現象查回設定或層級，修正後重做同一任務。保留第 14 堂故意清空 Destination、第 15 堂漏件檢查等有實質的活動。
- **讓別人取用**：同伴只看任務與交付包，就能操作原型、找到資產、開啟網站；不能靠作者口頭指路。

功能測試與使用者任務要分開：前者可明確要求「點此按鈕應開啟彈窗」；後者給「找出一筆待處理任務並標記完成」，觀察學員能否自己找到入口與理解回饋。

不必每堂都交大型報告。只保留能判斷該堂新能力的作品與少量紀錄，把整體交付集中於最後階段。

### 整門課最低完成條件

- **規則能使用**：色彩、文字與格線實際套在作品上，長文字、增刪及窄畫面沒有破版。
- **元件能維護**：至少一組來源、狀態與多個 Instance 可以追蹤，修改來源會反映到使用處。
- **任務能走完**：主要點擊、返回、取消、確認、關閉與滾動都有完成結果；必教的 Swap／Smart animate 有成功例子及修復證據。
- **交付能取用**：Figma／PS 來源與輸出真正存在，另一人能依清單找到、重開與使用。
- **網站能發布**：學員自己的原始檔、Git／GitHub 版本與公開網址互相對應，另一人可開啟並完成最小操作。
- **能力能遷移**：撤除逐步提示後，學員至少能調整一個新的介面條件並解釋選擇；真人連續跟做與適用的平台測試另行記錄。

這些條件是本次提出的補課與驗收建議，不是已完成的驗證結果。補齊前，課程完整度仍應判為「主題架構已具備，核心能力與整合作品待補」。
