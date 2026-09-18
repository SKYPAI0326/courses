# 網頁版講義產出報告：ai-beginner-practical

## 產出結果

已依既有教案完成四個 learner-facing 單元頁，並整合課程導覽：

- `CH1-1.html`：既有第 1 單元代表頁，更新下一頁導覽至 `CH2-1.html`。
- `CH2-1.html`：日常溝通；304 行。
- `CH3-1.html`：NotebookLM 閱讀實務；217 行。
- `CH4-1.html`：生活化應用；320 行。
- `module1.html`：更新 CH2–CH4 的網頁講義連結。

三個新頁面均從既有 lesson template 產出，包含情境、起始材料、完成物、完整示範、操作步驟、checkpoint、錯誤修復、資產入口、驗收與互動檢核。

## 教案補強

為符合網頁建置契約，補齊了三份教案的建置欄位：

- CH2：補 `learning_objective`。
- CH3：校正課程 `slug`，補 `unit_id`、`course_type`、`learning_objective`、`style_guide`、`platform_version`，並補齊試跑包、案例、動手題、常見錯誤與檢核題。
- CH4：校正課程 `slug`，補 `unit_id`、`course_type`、`learning_objective`、`style_guide`、`platform_version`，並補齊試跑包、案例、動手題、常見錯誤與檢核題。

這些是將既有內容結構化，未改變課程定位：CH3 固定使用 NotebookLM；CH2 與 CH4 維持 LLM 平台中立。

## 驗證結果

- 整體頁面 lint：5 頁，BLOCKER 0、ERROR 0、WARN 0。
- 內容覆蓋檢查：CH2 10 步／2 題檢核；CH3 5 步／9 份來源／2 題檢核；CH4 30 張提示詞／7 步以上／2 題檢核：PASS。
- HTML 本地連結：60 個連結全部通過，包含導覽、資產與片段連結。
- 平台邊界：CH2／CH4 未出現指定平台名稱；CH3 僅使用 NotebookLM；未出現註冊、登入或資安課程內容。
- 備份與還原：`restore-2026-09-14-pre-html-integration.sh` 語法與可執行狀態通過。
- 格式檢查：無尾端空白。
- 搜尋索引：已重建，共 665 筆。

`docs/audit-course-substance.py` 不存在於目前網站環境，因此無法執行該專項腳本；已以教案逐段對照、完整示範／步驟／資產數量與連結驗證替代，並保留此限制供後續環境補驗。

## 尚未宣告

- `_gates.md` 的使用者本人 cold follow 仍待完成；agent 產出檢查不能取代使用者實測。
- 目前可宣告「網頁版講義已產出並通過靜態與內容覆蓋驗證」，尚不宣告整門課已完成 release gate。
- 依流程，仍需由 `course-ops` 重建 sitemap，並可再安排正式的 course-reviewer／validator 驗收。

## 還原資訊

- 產出前備份：[2026-09-14-pre-html-integration](../../_backup/2026-09-14-pre-html-integration/)
- 還原腳本：[restore-2026-09-14-pre-html-integration.sh](../../_tools/restore-2026-09-14-pre-html-integration.sh)
