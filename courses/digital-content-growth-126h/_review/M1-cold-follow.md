# M1 Part 1 冷跟做記錄

狀態：`MACHINE_READY`；人工冷跟做：`PENDING`

## 範圍

- 學員頁：`CH1-1.html`、`CH1-2.html`、`CH1-3.html`、`PRAC1.html`
- 閱讀版與下載版資產：14 份
- 來源教案：`../_lessons/digital-content-growth-126h/CH1-1.md` 至 `PRAC1.md`

## 已完成的機器驗收

- [x] 四個學員頁都由 `_lessons` Markdown 重新生成。
- [x] CH1-1：兩種情境選擇、四種情境案例、判斷練習與阿凱參考完成品可取得。
- [x] CH1-2：問題拆解、十張線索卡、分類練習與阿凱修正痕跡可取得。
- [x] CH1-3：價值主張工作表、六組前後版本、分類練習與阿凱參考完成品可取得。
- [x] PRAC1：八個 Brief 欄位、四種情境參考、五科交接檢核與整合練習可取得。
- [x] 學員頁沒有講師筆記、Verification Asset Spec、`course_type`、來源路徑或 `BLOCK：待建立`。
- [x] 所有首次使用材料都有 HTML 閱讀版與 UTF-8 原始檔下載入口。
- [x] 來源教案列出的 M1 主要檢核材料已從 BLOCK 更新為 READY。

## 實際驗證證據

- `python3 digital-content-growth-126h/_tools/test_learner_render_contract.py`：4 tests passed。
- `python3 docs/lint-page.py ... --summary`：18 頁，BLOCKER 0、ERROR 0。
- 連結與 UTF-8 檢查：4 個學員頁、14 份資產，無缺檔、無缺 BOM。
- `git diff --check`：待提交前重跑。

## 人工冷跟做待辦

1. 只從課程總覽進入 Part 1，依序開啟 CH1-1 至 PRAC1。
2. 只使用頁面上的閱讀版／下載版材料，完成一份自己的四情境選擇與共同 Brief。
3. 檢查不看 Markdown 原稿時，仍能知道每個欄位怎麼填、答案如何判斷、卡住時回哪一節。
4. 確認四種應用情境都能銜接後續 Part，且求職、企業專案、自由工作與個人品牌都不是裝飾性出口。

人工冷跟做完成前，M1 不標記 `CONDITIONAL_READY` 或 `READY`，也不作為整包課程可販售的證明。
