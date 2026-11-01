# Part 1、Part 6、Part 7 改寫規格書

發包人：產品經理（Claude Opus 5.5）。承作：GPT-5.6 Sol（high）。日期：2026-11-01。
寫作標準與 11 條累積教訓沿用 `../part34/改寫規格書-Part3-4.md` 第 2 節（核對交給 AI、看工具結果也交給 AI、每次開新對話寫明要貼什麼、案例附人物或資料表、PRAC 只給達成清單與自我檢查且參考寫法放頁尾、單人可完成、提示詞動詞開頭、不用代碼與 Part 編號引用、每節最多一句限制語、檔案交給 AI 的方式、開場與收尾且第一個 `##` 前只放三行），以及 `../pm-test/改寫規格書-Part2.md` 第 2 節。與課程資料夾其他規範衝突時以本檔為準。

## 1. 範圍與頁面設計

頁面設計以 `../rewrite-plan.md` 第 2 節「Part 1」「Part 6」「Part 7」三張表為準（新標題、副標、要教會的 AI 能力、完成物、拿掉／改法），標題與完成物也已寫在 `_outlines/gen-ai-36h.md`。

| Part | 頁 | 素材（`courses/gen-ai-36h/assets/` 下） |
|---|---|---|
| 1 | CH1-1 | `beginner-start.md`（及現有正文中的五行工作紀錄） |
| 1 | CH1-2 | `part1-4-safe-practice-pack.md` |
| 1 | CH1-3 | `email-delay-facts.md` |
| 1 | PRAC1 | `prompt-library.md` |
| 6 | CH6-1 | `tool-card-template.md` |
| 6 | CH6-2 | `part6-workflow-case.md`、`part6-filled-workflow.html`、`tool-card-template.md` |
| 6 | PRAC6 | `part6-workflow-case.md`、`part6-transfer.html`、`part6-transfer-answer.html` |
| 7 | CH7-1～CH7-3 | `capstone/`（START-HERE、branch-guide、transfer-update 等） |
| 7 | PRAC7 | `capstone/`、`showcase-example.html` |

事實以素材、答案檔、現有正文中的案例資料為準；現有正文（`_lessons/gen-ai-36h/` 同名檔的 learner-content 段）只用來了解案例，不沿用結構與用語。

## 2. 各 Part 補充

- **Part 1 是學員第一次接觸 AI**：不可引用後面 Part 才教的做法。這裡是「AI 可能寫錯，所以要它附依據」第一次出現的地方，用白話說明一次。CH1-1 要包含保存與找回成果（存到自己的文件或資料夾）。CH1-3 的「自訂指示」只寫概念與一個例子，不寫特定平台的選單路徑。
- **Part 6 的表單**：PRAC6 頁面下方會自動出現「填寫與保存」表單（工具卡欄位固定，寫在 `assets/course-tools.js` 與 `tool-card-template.md`，可存在瀏覽器並匯出、匯入 JSON 備份）。講義只說「把 AI 起草的內容填進本頁下方的表單」，欄位名稱照 `tool-card-template.md`；不要自己設計新欄位，也不要在正文重做一個表單。CH6-2 保留一小段「哪一步該由人決定、不交給 AI」的說明（例如核准改期、通知是否發出），寫成判斷原則，不寫成人工作業。
- **Part 7 的表單**：PRAC7 頁面下方同樣會自動出現發表頁表單（欄位固定在 `course-tools.js`，可匯出個人 HTML 與 JSON）。講義只說「請 AI 協助撰寫各欄，再填進本頁下方的表單」。結業專題允許學員選路線（依 `capstone/branch-guide`），講義用示範案例帶過一次，不要求學員逐字照做示範內容。
- **單人化**：Part 6、7 原本的「請同伴看卡／讀提案／試用／交接」一律改成「開新對話，請 AI 扮演（同事／委託人／第一次使用的人／接手者），只看你給的內容，指出卡住或缺漏的地方」，提示詞以動詞開頭。

## 3. 承作與交付

1. 讀本檔、`../part34/改寫規格書-Part3-4.md` 第 2 節、`../pm-test/改寫規格書-Part2.md` 第 2 節、`../rewrite-plan.md` 第 2 節三張表、評分尺 `../rubric.md`、第 1 節素材與現有正文。
2. 每頁格式：`# 標題`、副標一行、`本節完成物：…`（第一個 `##` 之前只放這三行）、各 `##` 小節、提示詞放 ``` 框；頁尾「## 自我檢查」（學員動作分類與比例、累積教訓逐條是否做到）與「## 事實核對」。
3. 連結格式 `../assets/…`，連結前確認檔案存在。
4. 只寫本次指定的輸出檔；不要 git add 或 commit；不能詢問使用者；不要使用任何 course-* 技能。
