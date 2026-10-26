# Repair Plan: acp-ae 零基礎 Step by Step

## Scope

- slug：`acp-ae`
- task_scope：`content-change`
- lessons：`_lessons/acp-ae/` 的 10 份正式正文
- pages：`part1/`、`part2/`、`part3/` 的 10 個 lesson HTML
- 保留：課程時數、13 題、40 張卡、9 題代表實作、技術數值、檔名、連結、導覽順序與外層版型
- 不處理：Adobe 實機驗證、原題全文、第三方截圖、上線註冊與部署

## Risk

- near-term class：unknown
- backup required：yes
- platform state：AE v25.x 尚未在本機實測，既有路徑只重寫表達方式，不宣稱現行介面已驗證

## BLOCKER

### [LEARNER_PATH] CH1-1～CH1-5

- 問題：操作步驟未逐項提供位置、輸入、畫面結果與就地修復。
- 修法：將每一段完整示範改為 `Step 1…N`，每步依需要寫出「操作／應看到／如果沒有」。
- 驗證：每個操作頁至少有一條可從起始檔走到完成物的完整 step chain。

### [LEARNER_PATH] CH3-1～CH3-3

- 問題：代表題在 HTML 中沒有 step block，零基礎學員難以辨認動作邊界。
- 修法：三題代表實作各自拆成明確 Step by Step，保留原數值與證據要求；路徑卡補閱讀順序。
- 驗證：9 題代表實作都有編號、預期結果與復原位置。

## MAJOR

### [BEGINNER_CONTINUITY] 全課

- 問題：第一個專有名詞與第一個操作的關係不夠直接。
- 修法：用「白話意思＋畫面位置＋現在用途」介紹首次出現的術語，操作句以選取對象與面板開始。
- 驗證：30 秒入口六題可從頁面頂部與第一段操作回答。

### [CONTENT] CH2-1

- 問題：缺少可重複使用的逐題作答方法。
- 修法：加入四步判斷流程與第 1 題完整示範，再進入其餘 12 題。
- 驗證：學員不先看答案，也能依 Step 1–4 產出四欄解析。

### [INTEGRATION] PRAC1

- 問題：只有決策順序，零基礎學員不易知道每階段何時可以繼續。
- 修法：保留開放選擇，但改成 S1–S5 階段式 Step by Step，每階段加入 checkpoint 與安全停止狀態。
- 驗證：能從空白 Composition 走到輸出與證據清單，不依賴口頭補步驟。

## 允許變更文字與 DOM 清單

1. 目標：10 份 lesson Markdown。新增／改寫入口說明、術語白話定義、Step、預期結果、checkpoint 與修復文字。
2. 目標：10 個 lesson HTML。把教案已完成的內容同步為既有 `.lesson-section`、`.step-block`、`.callout` 與表格元件。
3. 原因：學員為零基礎，現有摘要式步驟不足以獨立跟做。
4. 版面影響：內容會增長；不改 topbar、hero、main、nav、footer、href、JS 與導覽順序。
5. 刪除／合併：無。只把原有簡略步驟展開或等價改寫。

## Execution Order

1. 建立 backup 與 restore script。
2. 先修 10 份正式正文，凍結技術事實與零基礎用語。
3. 先同步 CH1-2 代表頁，執行結構、lint 與 390／430／1440px 瀏覽器檢查。
4. 同步其餘 9 頁，小批次跑 validator 與 lint。
5. 重做 content／fidelity／beginner continuity 審查，重建搜尋索引。
6. 產出 `REPAIR-REPORT.md`；平台與真人證據維持 BLOCKED／PENDING。
