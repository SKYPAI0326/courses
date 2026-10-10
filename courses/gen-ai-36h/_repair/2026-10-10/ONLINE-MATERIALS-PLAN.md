# 線上學員素材入口與實作包修復計畫

日期：2026-10-10（Asia/Taipei）
對象：gen-ai-36h 線上公開教材；工作副本以目前遠端 `main` 為基底。

## Scan findings

- Chrome 實際畫面顯示學員開啟 `assets/workplace-cases/part2/START-HERE.md`；GitHub Pages 把 `.md` 當純文字呈現，表格與 Markdown 連結均未渲染。
- Part 2 素材只有 9 則聊天、6 列追蹤表與 7 句逐字紀錄；Part 3 示範／獨立案例的核心來源多為 300–400 bytes；capstone 政策、狀態表與會議紀錄也不足以支撐真實的跨文件交接。
- 多個課程頁直接連到 `.md` 答案鍵／來源檔，學員會看到原始標記；核心入口目前無下載、工作順序、成品模板或清楚的教師答案隔離。

## Classification and scope

- `task_scope: content-change`，依使用者先前核准的課程修正延續執行。
- `ASSET_DISCOVERABILITY: BLOCKER`：把學員入口連到未渲染的 Markdown。
- `CONTENT_THIN: MAJOR`：補足三組職場案例來源、CSV 欄位、版本／決策證據、答案理由與可複製成品；增加一份 PRAC2 可用的交接模板。
- 修正責任層：案例素材本身、靜態 HTML 素材入口，以及教案／講義中的資產連結。既有講義外層、導覽、表單互動與課程順序不變。

## 允許的內容變更

1. Part 2「門市退貨試辦」：重寫 `chat-log.md`、`progress-register.csv`、`change-note.md`、`attachment-case.md`、`answer-key.md`；在 `START-HERE.md` 加入排版頁連結；新增 `START-HERE.html` 與可複製的 `handoff-template.csv`。補足跨角色訊息、時間順序、狀態快照、有限核准、依賴與未決責任，提供逐來源答案和工作交接樣本。
2. Part 3 示範「星河成果展」與 Solo「海岸志工日」：擴寫每份委託／核准／變更／報價／會議來源與教師核對答案；各新增一個 `START-HERE.html`，提供情境、檔案下載、建議閱讀順序和任務入口。
3. Capstone「門市新人訓練」：擴寫委託、政策 v1/v2、六店狀態 CSV、會議紀錄、逐來源完整示範、測試證據與答案鍵；在原 Markdown 入口加入排版頁連結，新增 `START-HERE.html`。
4. 只更新 11 個相關 lesson plan 的素材連結，將入口、教師答案、完整示範與測試證據改連到排版入口；依既有流程更新鏡像教案並重轉製 11 個 learner HTML。新增入口為獨立 asset HTML，既有 lesson HTML 只改明列的 `href`／對應說明文字。

## 目標檔案

- 資料包：`courses/gen-ai-36h/assets/workplace-cases/part2/`、`part3-demo/`、`part3-solo/`、`capstone/`。
- 教案來源與鏡像：`_repair/2026-10-09/lesson-plans/`、`_lessons/gen-ai-36h/` 中的 CH2-1、CH2-2、CH2-3、PRAC2、CH3-1、CH3-2、PRAC3、CH7-1、CH7-2、CH7-3、PRAC7。
- 轉製頁：對應的 Part 2、Part 3、Part 7 共 11 個 learner HTML。
- 驗證紀錄：本資料夾新增 `ONLINE-MATERIALS-PLAN.md`、備份 manifest、深度審查與修復報告；另新增本輪 renderer／連結驗證紀錄。

## 完成與驗收

- 每組資產入口使用 HTML，清楚區分「供 AI／試算表讀取的原始來源」、「學員交付物」和「完成後才開啟的教師答案」；下載連結都指向存在的檔案。
- 案例來源具備可追溯文件 ID、日期／時間、版本和具體決策；答案鍵逐題給出證據、不能推論、修正後範例與下一步。
- 自動核對三組資料的數字、時間順序、引用 ID、版本範圍與答案鍵；確認教案、鏡像、HTML 的本輪連結一致。
- 執行 course lint、HTML 結構檢查、Substance audit、link scan、Git diff checks 和可冷讀跟做的人工檢查；部署後重新開線上 Part 2 入口確認 `.md` 不再是學員主入口。
- 真人冷讀／指定帳號平台驗證如未執行，報告保留 `PENDING`，不宣稱 `LEARNER_READ` 或 `HUMAN_READY`。

## 變更邊界

不刪除既有檔案；不修改其他課程、全站版型或自動化功能；不新增真人／真實公司資料；不把留言或會議中的提案升格成核准。修改前先建立本輪 dated backup 與可執行 restore script。
