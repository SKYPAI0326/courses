# 素材與成品檢查

2026-10-07，範圍僅本批PRAC2-1教案、素材與實際Gamma PDF，不含既有HTML。

實際執行：

```sh
/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 _validation/gamma-2026-10-07/check-materials.py
/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 _validation/gamma-2026-10-07/check-pdf-exports.py
```

素材結果PASS：37個本機連結、兩企劃各P01–P10、十頁參考與十段文字、六來源快照雜湊、既有兩項使用者修改雜湊、實際完整模型輸入比對；A只有試跑後的一字錯字修正另記。數據獨立重算詳material-checks.json。

PDF結果PASS：兩份十頁、逐頁正文無遺漏、A補回的兩規則及四週條件、B投入條件。正規化與PDF文字流順序詳pdf-checks.json；多欄的視覺閱讀順序另由渲染圖確認，不用原始extract_text行序判斷漏字。

PDF副本與實際匯出雜湊一致。所有新增人工文字檔已檢查尾端空白；既有兩檔git diff --check通過且未修改。平台視覺檢查及失敗修復見PLATFORM-RUN.md，與程式結果分開。
