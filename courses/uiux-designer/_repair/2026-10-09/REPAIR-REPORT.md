# UI/UX講義補強完成報告

2026-10-09。本輪完成16堂教案、講義、起始材料與完成檢查表的內容修正及本機驗收。整體狀態為 `MACHINE_READY_PENDING_HUMAN`：教材與本地工具可交付，真人學習成效及指定外部平台仍待實測。

## 修正結果

| 原審查缺漏 | 本輪實際補強 | 證據位置 |
|---|---|---|
| B01 Auto Layout核心步驟缺漏 | A3分開文字Auto height與容器Hug，建立真正Message／Button／Vertical卡片，長句、增刪、Fill、固定高度故障及修復 | A3正式正文、結構圖、檢查表 |
| B02 免費方案錯誤前提 | 同檔多基本互動；同trigger多actions與一般基本連線分清，移除一檔一action及拆檔主張；歷史Probe保留且不沿用舊結論 | Environment Contract、B2／B4／B6、官方來源 |
| B03 前後堂物件不存在／規格不一致 | A4建立真元件，A5產出Button family，A6產生Button / Login，A7建立List／Detail，A8新增Confirm／Nav；材料與表格同步 | Course Blueprint、16堂正文及保真比對 |
| B04 Starter要求Dev Mode | B7改Design量測／Export，明記Dev Mode方案邊界 | B7正文、課前準備、Environment Contract |
| B05 Web／Git零基礎起點缺漏 | 完整ZIP、解壓／開檔／編輯／Reload、DOM／id／class與三檔分工、Git安裝／資料夾／init／commit／diff、錯誤修復 | B8正文、web-starter、隔離Git實跑 |
| B06 課綱交付路徑缺漏 | 真分層PSD與透明PNG、Photoshop操作、交付清單、GitHub／Pages首次部署及後續更新 | B7／B8正式正文與真實素材；外部平台操作待驗 |
| M01–M02 介面與元件方法薄弱 | 完整雙欄表單、長列／空狀態、回饋／導航結構、兩Instance同步與覆寫比較 | A4–A8 |
| M03–M04 原型核心能力與成果鏈缺漏 | 可見Smart Animate、真正已開Overlay內Swap、Fixed／Sticky／Horizontal、長List接主線、T01–T08測試與交付 | B3–B7 |
| M05 Solo重複 | 每堂加入不同尺寸、狀態、資料、來源覆寫、故障或任務；整合作品提供12筆報名CSV及80分且無阻斷判準 | 活動自審表、B6 |
| M06 文案抽象、繁瑣 | 改具體物件與動作，首次概念配中文說明；共用環境集中於課前速查，單元留下必要提醒；修正繁體轉換誤字 | 16堂正文、總覽、CONTENT-REPAIR-REVIEW |
| M07 檢查表沒有保存操作 | 16張表能保存／重開、下載／匯入JSON、列印；B6逐項8任務記提示、問題與回歸 | record-form.js、B6任務表、瀏覽器紀錄 |
| M08 視覺判斷不足 | 色彩角色、字級／字重／行高、真實對比計算、手機／桌面格線算式及視覺示意 | A1／A2、SVG、對比工具 |

## 驗收結果

- 54個公開HTML：lint為0 BLOCKER／0 ERROR／0 WARN。
- 16堂既有版型：結構檢查16 PASS，內容保留在原lesson-body；沒有以新外殼取代舊頁。
- 16堂教案與HTML：逐項核對標題、前言、段落、步驟、表格、參考答案及完整程式區。三個Web程式檔與正文完全一致。
- 389個本地連結與錨點：0錯誤。另修正16張檢查表返回總覽的錯誤路徑。
- ZIP：5檔CRC正常，解壓內容與目前web-starter逐位元組一致。
- 素材：PSD512×512、3個獨立圖層；PNG512×512且角落alpha0；12筆虛構報名CSV存在。PSD工具重開通過不等於Photoshop桌面實測。
- JavaScript：7份外部／內嵌腳本語法檢查通過。網站實際取消、確認、狀態、空清單、長列及固定導航通過；390／430最後一列可在導航上方讀完。
- 檢查表：實際保存後Reload、下載JSON及匯入還原通過。對比工具實算7.90:1，無效輸入顯示格式錯誤。
- 響應式：1440代表頁、390總覽與全16堂、430代表頁，沒有全頁水平溢位。A3再查頂部、方法、練習、底部；B6新任務表另查430。
- Git：由ZIP解壓到隔離資料夾，執行init、明確add、cached diff、首次commit、修改與diff、第二次commit，最後working tree乾淨。沒有修改本專案index、global身份或遠端。
- 搜尋：只更新UI/UX的54筆，其他911筆內容與順序保留。
- 備份：初始100份原檔，另於改索引前加備份1份，合計101份SHA-256吻合；還原腳本已做語法檢查。新增修復檔保留供審查，還原原檔不自動刪除新檔。

可重跑指令見 `_validation/repair-2026-10-09/TECHNICAL-RUN.md`；實際數值、截圖、逐項保真與素材檢查均置於同目錄。版本索引為 `_validation/evidence.json`，正式狀態輸出為 `_validation/validation-result.json`。

## 尚待實測與授課使用邊界

Figma入口目前導向登入頁，沒有可用Starter編輯帳號；因此未重跑本輪16堂設計／互動作品鏈。Photoshop桌面開啟PSD、修改及透明匯出，GitHub公開repo／Pages首次部署及更新，也尚未完成平台實測。官方文件與素材驗證不代替這些結果。

零基礎真人的進入、完成、理解、遷移及連續三堂跟做皆未填PASS。建議首輪用A4→A5→A6與B4→B5→B6檢查能力是否接得上，記卡點、提示、修復與實際成品；再跑B7→B8交付包到公開更新。99h保留行政配置，實際教學節奏未經班級試跑鎖定。

授課前先完成COURSE-START工具準備，尤其Photoshop工作站與GitHub帳號。沒有軟體／權限時，本機或閱讀可以先做，該平台完成條件仍須補測。本輪未commit、push或公開發布；原始審查與歷史Probe保留，最新結論以本報告及版本證據為準。
