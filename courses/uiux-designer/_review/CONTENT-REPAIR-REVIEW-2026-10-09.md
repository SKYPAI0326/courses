# 本輪教學內容與活動自審

日期：2026-10-09。身分：author-self-check，非獨立審查或真人學員。範圍：正式教案 A1–A8、B1–B8 的 learner-content、目前起始材料／檢查表、共用素材、下載專案。

先核對正式教案的定義、完整輸入、方法、可見結果、故障修復、下一堂所需物件與新條件練習，再核對 HTML 的逐項保真。下列 PASS 僅表示作者已完成內容修訂與自審；Figma、Photoshop、公開部署及真人完成能力另驗。

| 單元 | Demo首次方法 | Together需要自己判斷 | Solo新增條件與完成物 | 核對結果 |
|---|---|---|---|---|
| A1 | Frame／文字、角色色彩與字級／行高、真實對比計算 | 用同一規則判斷資訊層級，不只抄色碼 | 更換主要色與錯誤文字，重測對比、記理由 | 色彩表、文字表、對比工具與視覺參考齊全；PASS |
| A2 | 402四欄，1440十二欄，欄寬與跨欄算式 | 桌面主／側區的用途與手機閱讀順序 | 360欄寬69、卡片312、兩欄150，重排提醒 | 354／171、792／384與邊界／溝槽算式核對；PASS |
| A3 | Message與Button包入Vertical卡片，分開文字Auto height與父框Hug | 自己找設定層、加長文字、增刪子層、故意固定高度後修復 | 360卡片312、內容280，長句不重疊 | Padding16、Gap12、Hug／Fill層级與按鈕建立順序明確；PASS |
| A4 | 主元件改動→兩Instance同步，個別Label覆寫 | 選正確來源與覆寫位置，保留普通副本作對照 | 第三Instance覆寫填色，預測／觀察／恢復連結規則 | 主元件寬Hug、Label Auto width，避免長Label裁切；PASS |
| A5 | Hierarchy×State四組Variant、Label文字屬性 | 找重複組合、分清次要與停用、切換後檢查文字 | 取消／確認／缺資訊配置、長Label與修復紀錄 | 不依賴尚未建立的List；文字覆寫備援不冒充Text property完成；PASS |
| A6 | 真正Label／Input／Helper／Button的Auto Layout表單 | 正常、錯誤、修正後與空值版本；定位高度原因 | 360長提示、重寫有修正方向的錯誤句 | 帳號／密碼資料與層名完整；本堂產生Button / Login；PASS |
| A7 | 三筆CSV→Title／Meta／Link的Row與List／Detail | 0／1／10筆、長標題與增刪後位置判斷 | 狀態、資料與列數改變，核對內容對應 | T01／T02內容與期限對應、空狀態有資訊；PASS |
| A8 | Toast與Dialog用途、父子結構、兩按鈕與底部導覽 | 用位置與內容判斷阻斷／非阻斷回饋 | 新確認情境與長說明，選擇回饋形式並說理由 | Dialog320、內容272、兩Fill按鈕130＋Gap12；PASS |
| B1 | 任務→線框→五個實際畫面的對照與起點 | 檢查入口／出口、熱區、前堂實物是否存在 | T02詳情與不同資料的任務對照 | 線框與成品目的有區分，缺檔有重建位置；PASS |
| B2 | 同檔不同物件的基本On click／Navigate／Back | Destination None故障、正確目的地、Disabled不接線 | 第二筆資料與返回路徑獨立接線 | 修正「一檔一action」；基本多互動與同trigger多action分開；PASS |
| B3 | 進入／返回方向、200ms／Ease out、Smart Animate完整配對 | 單改層名→觀察→修復；單改Duration作比較 | 位置＋透明度新條件及Instant比較 | Before／After尺寸、同名階層、Flow與回連完整；PASS |
| B4 | Complete開Confirm、取消關閉、確認到List Done | 已開Menu內Swap Help→關閉，核對背景與位置 | 取消編輯情境、外側關閉選擇、長Help | 一個trigger一動作、結果Frame含Toast，不需付費多動作；PASS |
| B5 | 固定視窗的Vertical overflow | Fixed／Sticky與Spacer遮擋修復、Horizontal分支 | 360×800、20筆與最後一列 | 連接Login／Back到List Long；橫向354視窗、624內容；PASS |
| B6 | 完整T01–T08、Destination故障與回歸範例 | 真實／本人自測、提示紀錄、嚴重程度與回修位置 | 12筆報名CSV、360×800整合作品，80分且無阻斷 | 8項專用表格、12筆可取得資料、評分與參考結果齊全；PASS |
| B7 | Design量測、Export、3層PSD→透明PNG、交付清單 | 缺圖、白底PNG與重開交付包定位 | 白底／透明比較、長Dialog重匯出、更新實際規格 | Starter不要求Dev Mode；PSD是真檔案，桌面操作待驗；PASS |
| B8 | ZIP解壓、三檔與DOM、完整Web、Git首次／第二次提交、GitHub／Pages | 取消／確認／空狀態、相對路徑、diff及線上更新判斷 | 報名情境、自己的PNG、資料／色彩／標題及公開交付 | 程式與ZIP逐檔一致，本地流程及隔離Git已跑；公開部署待驗；PASS |

## 連續單元與共用文字核對

A4→A5→A6：前課建立來源與Instance；本課新增四組狀態及文字屬性判斷；後課使用Button family完成雙欄表單。元件、狀態、表單各有不同產物與決策。沒有真實Figma檔案鏈驗證，本筆只記作者的來源與依賴審查。

B4→B5→B6：前課補可取消確認與Swap；本課把長List和Fixed接到Login／Back；後課T03／04檢驗取消確認、T05檢驗最後一筆及固定物件、T06檢驗Swap、T07檢驗不同資料、T08檢驗Horizontal。測試要求已對應到實際教學位置；真人連續三課跟做待驗。

共用環境、素材真實性與保存入口集中在COURSE-START。各課保留同一材料／檢查表連結格式，但核心正文、故障與Solo的決策不同。沒有以同一段「交接規範」反覆替代教學。保留英文欄位名稱讓學員能在工具中查找，先用中文解釋用途；改掉抽象標籤、錯誤合併設定、轉換誤字與不自然的「透過條件」。

## 可信度與尚待驗證

方案修正依據Figma官方的Multiple actions、Starter與Design inspection文件；不是從一次升級提示推論整檔上限。來源連結保留於各堂。SVG明記為示意，不冒充Figma截圖、含互動Starter或實測完成物；分層PSD與Web ZIP以實檔檢查。

本次Figma入口導向登入頁，沒有可用Starter編輯帳號；未執行Photoshop桌面開檔／匯出、GitHub公開部署。不得沿用歷史Probe為本次16堂全部平台PASS。真人進入、完成、理解、遷移與連續三堂測試仍為PENDING；99h保留行政配置，未宣稱班級時間已試跑。
