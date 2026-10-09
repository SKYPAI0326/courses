# 本課修訂工具

目前的權威內容是 `_repair/2026-10-09/lesson-plans/*.md`、`assets/` 的實檔及正式 `_lessons/gen-ai-36h/`。改教案後執行 `python3 _tools/render-lessons.py`，再跑 `python3 _tools/verify-course.py`；若正式來源要同步到網站根目錄，執行 `python3 _tools/sync-global-sources.py`。

教材有變動時，先重讀受影響正文、檢查轉製與功能，更新 `_validation/2026-10-09/` 對應紀錄，再執行 `python3 _tools/build-validation-evidence.py` 重綁雜湊與 `course-validator.sh gen-ai-36h all`。只重產雜湊不能延用舊審查結論。

`author-lessons.py`、`author-more.py`、`create-assets.py`、`create-audio.py`、`create-media.py`、`create-reference-tools.py`、`convert-traditional.py` 與 `sync-course.py` 是這次製作時的一次性產製紀錄，內嵌的是初稿，**不要在現有課程上重跑**，否則會覆寫後來的教學修訂。Part 5 的現行重建指南與 T07 規格，以 `assets/part5-rebuild-guide.md`、`assets/part5-test-cases.csv` 為準。

還原修訂前原檔請先跑 `_tools/restore-2026-10-09-pre-repair.sh --dry-run`；確認後才在課程維護時使用 `--live`。還原只處理 manifest 中 37 個原檔，新產檔保留。
