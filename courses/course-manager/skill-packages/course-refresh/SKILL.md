---
name: course-refresh
description: Use for read-only freshness and UI-drift scans of existing learner pages; reports severity, affected Gate, and next action without editing metadata or republishing.
allowed-tools: Read, Glob, Grep, Bash, WebFetch
---

# 課程新鮮度唯讀掃描

這個 skill 只讀取正式學員頁與公開版本資料，產生可追溯的維護報告。它不改 HTML、不升日期、不重建索引、不提交 Git，也不發布。

## 執行

```bash
python3 scripts/course_release.py scan --root COURSE_ROOT --as-of YYYY-MM-DD
```

掃描每個 HTML 的 `data-platform-version` 與 `data-built-at`，並依截至日期計算 age days：

- 90 天內：`OK`，不指定 affected_gate。
- 91–180 天：`REVIEW`，affected_gate 為 G1；查閱官方資料並實際核對代表操作。
- 超過 180 天：`STALE`，affected_gate 為 G1；重新驗證來源與工具行為。
- metadata 缺失或日期無效：`UNKNOWN`，affected_gate 為 G6；補充可追溯來源需另開有授權的修正流程。

時間只代表重查優先順序，不能直接證明內容錯誤。可以唯讀查閱官方 release notes；查不到時保留未知，不猜測版本差異。

## 輸出

每筆必須包含：

- `path`、`platform_version`、`built_at`、`age_days`
- `severity`
- `affected_gate`
- `recommended_action`

報告同時標示 `read_only: true`。若實際核對後確認內容、介面、素材或操作已漂移，交給 `course-repair` 建立修正提案，再重跑 affected Gate、獨立試學與必要發布流程。

## 禁止事項

- 不修改 metadata 或把日期重設為今天。
- 不改課程正文、HTML、素材、密碼、註冊、索引或 sitemap。
- 不以掃描結果自動重新發布。
- 不把年齡門檻當成內容失敗證據。
