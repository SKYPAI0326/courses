# 修復與驗證工具

- `restore-2026-10-06-pre-repair.sh`：還原41個原頁；加`--site`只還原共享搜尋／sitemap的本課紀錄，保留其他課程。新素材不刪除。
- `verify-static.py`：連結、錨點、10站路線、來源保真、素材ZIP與搜尋範圍。
- `verify-browser.cjs`：在本課以`python3 -m http.server 31876 --bind 127.0.0.1`提供頁面後，執行Chrome操作與RWD自驗；不登入外部平台，不能替代真人。
- `build-evidence.py`：實際審閱與測試完成後整理當前hash；不能只執行此命令就沿用未檢查的PASS。

其他build／apply／correct／finalize腳本是本次一次性製作紀錄，不能作日常重建入口。現行正式正文以`_source/`為準；日後修改源頭並同步HTML，重新驗證受影響版本。
