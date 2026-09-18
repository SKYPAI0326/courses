# 全課頁面工作台修復報告

日期：2026-09-18

## 修復結論

CH2-1、CH3-1、CH4-1 已完成與 CH1-1 一致的頁面內學習路徑。學員先在講義頁面看到並填寫可保存的工作區，再把提示詞送到自己可使用的文字型 LLM，最後把回答貼回、檢查、匯出或列印。Markdown 不再是主要起始動作，只保留為離線／印刷備援。

CH3-1 保留 NotebookLM 為唯一固定平台；頁面提供伴隨紀錄台，不自動讀取或假裝嵌入 NotebookLM。

## 已完成項目

- CH2-1：新增日常溝通工作台，涵蓋 Email、LINE／短訊息、三版自我介紹、單一變因修訂、保存、匯出與列印。
- CH3-1：將 NotebookLM 閱讀包改為伴隨紀錄台，涵蓋來源狀態、新聞三段摘要、公告白話卡、書籍重點與行動、引用回查、待重跑狀態、匯出與列印。
- CH4-1：新增個人生活應用工作台，涵蓋五個個人條件、四段式提示詞、第一版、單一變因修訂、前後比較、人工／專業確認與匯出列印。
- 新增共用 `assets/learner-workbench.css` 與 `assets/learner-workbench.js`，提供本機暫存、重新整理恢復、進度、匯出 Markdown、列印與清除資料。
- 同步修正 CH2–CH4 lesson plan、`COURSE-BLUEPRINT.md`、`COVERAGE-LEDGER.md` 與離線素材的主線描述。
- 保留 `_backup/2026-09-18-pre-all-workbenches/` 與 `restore-2026-09-18-pre-all-workbenches.sh` 作為可回復點。

## 驗證證據

- 4 個 learner-facing HTML lint：4 頁皆 `BLOCKER 0 / ERROR 0 / WARN 0`。
- 課程 substance audit：`pages=4, block=0, review=0, ready_for_human=4, missing_assets=0`。
- `test_workbench_contract.py`：PASS。
- `test_all_workbenches_contract.py`：PASS。
- `test_cold_follow_contract.py`：PASS。
- `test_ui_practicality_contract.py`：PASS。
- L0 truth contract：PASS。
- learner-agent evidence manifest：PASS。
- shared／inline JavaScript syntax：PASS。
- 本課程 local links：91 checked，0 missing。
- course-validator preflight：24 PASS、0 WARN、0 FAIL。
- course-validator L1–L3：全綠；7 頁、0 BLOCKER／ERROR／WARN。
- 站內搜尋索引已更新：949 筆。

## 人工驗收邊界

目前已完成靜態、契約與可恢復路徑驗收；NotebookLM 的實際登入、加入來源、引用點擊仍需真人在可用帳號與當期介面中完成最後一次確認。
