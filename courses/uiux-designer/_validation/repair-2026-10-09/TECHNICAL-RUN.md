# 技術驗收指令與結果

日期2026-10-09，actor: tool-run。範圍為本輪當前16堂正式來源／講義、54公開頁、學員材料、ZIP／PSD／PNG與Web。所有命令由本課目錄執行；lint相對路徑以站根為準，使用courses/uiux-designer避免誤掃全站。

```sh
python3 ../../docs/lint-page.py courses/uiux-designer --summary
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py part1/*.html part2/*.html part3/*.html
python3 _tools/learner-entry-smoke.py
python3 _tools/verify-repair-2026-10-09.py
PYTHONPATH=/tmp/uiux-repair-deps python3 _tools/verify-web-package.py
git diff --check -- . ../../_lessons/uiux-designer ../../_outlines/uiux-designer.md ../../search-index.json
```

對應結果：lint.txt、structure.txt、learner-entry.txt、fidelity-links.json、runtime-assets-git.json。結果全通過。verify-repair需要BeautifulSoup；verify-web-package需要Pillow與psd-tools，本次使用已安裝於上述臨時依賴目錄的版本。依賴路徑不屬於學員Web的執行前提；Web本身無套件、server或build要求。

scripts-backup.json記錄Node --check的7個實際腳本、101個備份SHA-256及實際下載JSON驗證；form-download-test.json為「講義功能測試」假資料，不能當成學員作品。git diff --check無輸出；本次Git範例僅在TemporaryDirectory建立測試repo。

瀏覽器動作與尺寸在BROWSER-RUN.md、responsive-observations.json、a3-positions.json，最新確認結果web-confirm-430.jpg。檢查順序發現問題後已修正並重跑：檢查表16個返回總覽路徑、Web程式文字與來源不一致、ZIP檔案路徑、B6測試表及練習資料缺口、瀏覽器JS快取。

本筆為確定性與本地執行驗證，不把缺少的平台實測或真人能力推論為PASS。

最終CJK標題完整片語換行修補後重跑54頁lint與16堂逐項保真／389連結／ZIP比對，仍全數通過；瀏覽器代表桌面及手機再驗無水平溢位。
