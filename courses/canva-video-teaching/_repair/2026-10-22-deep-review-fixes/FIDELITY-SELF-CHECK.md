# 2026-10-22 來源與 HTML 保真自查

`run_static_checks.py` 重新核對 28 個 active HTML，其中 25 個單元／資源頁具有正式來源對照。

- 來源段落、標題、清單項目與表格：0 缺漏。
- 本地連結：676 個，0 缺檔，0 缺 anchor。
- learner content wrapper、access gate 與 course HTML contract：25 頁通過。
- CH2-1 新增的 `footage-v1.mp4` 連結可解析；CH2-1、CH2-3 仍保留 `action-layout-pilot` 與 `action-steps`。
- `search-index.json`、`Canva完整操作步驟.txt` 與兩個重建 ZIP 已包含本次正文。

結論：作者保真自查 PASS；自動比對結果見 `static-results.json`。這項檢查不代表 Canva 平台或真人跟做通過。
