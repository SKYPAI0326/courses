# Part 3、Part 4 改寫規格書

發包人：產品經理（Claude Opus 5.5）。承作：GPT-5.6 Sol（high）。日期：2026-11-01。
寫作標準沿用 `../pm-test/改寫規格書-Part2.md` 第 2 節；與課程資料夾其他規範衝突時以本檔為準。

## 1. 範圍與頁面設計

頁面設計以 `../rewrite-plan.md` 第 2 節「Part 3」「Part 4」兩張表為準（新標題、副標、要教會的 AI 能力、完成物、拿掉／改法），標題與完成物也已寫在 `_outlines/gen-ai-36h.md`。本檔不重抄，只補下列要求。

| Part | 頁 | 素材（`courses/gen-ai-36h/assets/` 下） |
|---|---|---|
| 3 | CH3-1、CH3-2 | `workplace-cases/part3-demo/`（approval-scope、change-notice、meeting-extract、vendor-quote、answer-key、START-HERE）、`notebook-start.html`、`mock-project-v1.pdf` |
| 3 | PRAC3 | `workplace-cases/part3-solo/`（project-brief、supplier-quote、change-record、meeting-notes、answer-key、START-HERE） |
| 4 | CH4-1 | `reference-timer.html`、`html-file-workflow.html` |
| 4 | CH4-2 | `quote-rules.md`、`quote-test-cases.csv`、`reference-quote.html` |
| 4 | CH4-3 | `sales-raw-transactions.csv`、`sales-24-months.csv`、`sales-data-dictionary.md`、`sales-expected-results.md`、`sales-case-answer-key.md`、`reference-chart.html` |
| 4 | CH4-4 | `html-file-workflow.html` |
| 4 | PRAC4 | `part4-transfer.html`、`part4-transfer-answer.html`、`quote-test-cases.csv`、`reference-timer.html`、`sales-data-dictionary.md` |

各頁的事實（金額、日期、版本差異、清理規則、預期結果）以素材與各 answer-key、expected-results 檔為準；現有正文（`_lessons/gen-ai-36h/` 同名檔的 learner-content 段）只用來了解案例，不沿用結構與用語。

## 2. 必守的累積教訓（前兩個 Part 驗收時發現的問題）

1. **核對交給 AI**：Part 3 的核對主要靠 NotebookLM 的引用——請它每個答案附引用，學員只點開 AI 回答中最關鍵的 3 處以內看原文。Part 4 的測試交給 AI：請 AI 依規則產生測試案例與預期值、列出試用清單，學員只試其中 3 項並把結果貼回給 AI 判斷。不要出現手算、逐筆填表、逐欄比對。
2. **看工具結果也交給 AI**：試完工具後，把畫面結果或數字貼給 AI，請它對照預期值列出不一致處。
3. **每次開新對話或換工具，寫清楚要貼什麼**。Part 3 寫清楚是在 NotebookLM 的哪個筆記本、要勾選哪幾份來源；Part 4 寫清楚要把哪個檔案或文字交給 AI。
4. **案例附人物或資料表**：每個案例第一次出現時附一張小表（人物與角色，或資料與用途）。用內容稱呼文件，不用檔名。
5. **PRAC 頁**（PRAC3、PRAC4）：每一步只給「要達成什麼」清單，學員自己寫提示詞；參考寫法放頁尾「卡住時的參考寫法」，前面加「先完成自己的版本，真的卡住再看」。不附完整範例輸出，改給「合格的結果要能回答」自我檢查清單；不在正文或提示詞裡寫出答案。完成後才開答案檔比對，比對也交給 AI。
6. **單人可完成**：拿掉所有「請同伴」「交給同學」，改成「開新對話請 AI 扮演第一次使用的人」。
7. **提示詞以動詞開頭**，不用「你是…」「請扮演…專家」這類開頭；需要角色時寫成「扮演第一次使用這個工具的同事，照說明操作並指出卡住的地方」。
8. **編號**：不出現 Q01、SRC-、MSG-、T01、NOT_RUN 等代碼；跨頁引用寫內容（「整理工作訊息那一節學過的三個問題」），不寫 Part 編號或章節碼。
9. **限制語**：每個 `##` 小節正文最多一句「不要／不能／仍須」類警語，其餘改成正面寫法。
10. **檔案怎麼交給 AI**：CSV、md 寫成「打開檔案，複製全部文字貼進對話」；HTML 工具寫成「存成 .html 檔，用瀏覽器打開」。工具不能產生或預覽網頁時，換一個免費 AI 工具，不寫「手動完成」。
11. **開場與收尾**：每頁第一段寫工作情境；每段第一句接住上一段；最後一段收回成果並說下一頁做什麼（PRAC 收回本 Part 能力並接下一個 Part）。不要在第一個 `##` 之前寫正文段落。

## 3. 承作與交付

1. 讀本檔、`../pm-test/改寫規格書-Part2.md` 第 2 節、`../rewrite-plan.md` 第 2 節 Part 3／Part 4 表、評分尺 `../rubric.md`、第 1 節列出的素材與現有正文。
2. 每頁格式：`# 標題`、副標一行、`本節完成物：…`、各 `##` 小節（第一個 `##` 之前只放這三行）、提示詞放 ``` 框；頁尾附「## 自我檢查」（學員動作分類與比例、第 2 節 11 條逐條是否做到）與「## 事實核對」（每個數字、日期、版本結論、清理規則對應到哪個素材的哪一句）。
3. 連結格式 `../assets/…`，連結前確認檔案存在。
4. 只寫本次指定的輸出檔；不要 git add 或 commit；不能詢問使用者；不要使用任何 course-* 技能。
