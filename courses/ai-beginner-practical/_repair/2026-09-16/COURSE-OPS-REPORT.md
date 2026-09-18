# Course Ops Report：ai-beginner-practical

**執行時間**：2026-09-16 00:43–01:42（Asia/Taipei）  
**掃描頁數**：6 頁（index、module1、CH1-1～CH4-1）

## 結果

| 項目 | 結果 | 證據／備註 |
|---|---|---|
| Audit | OK | `docs/lint-page.py`：BLOCKER 0、ERROR 0、WARN 3；警告為教學提示框數量，未阻擋本課程 |
| Internal links | OK | 89 個相對 `href`／`src` 與錨點，broken 0 |
| SEO meta | OK | 6 頁均有 description、og:title、og:description |
| Password gate | OK | 6 頁均有 `_gate`；密碼 hash 未修改；入口文字已說明「講師發放密碼後自學」，遺失或未取得時回原報名／課堂通知管道申請或重發 |
| Search index | OK | `search-index.json` 含本課程 6 筆：4 課程頁、1 導覽頁、1 總覽頁 |
| Course card | OK | 站根 `index.html` 已有 `courses/ai-beginner-practical/index.html` 卡片 |
| Sitemap | 預期排除 | 6 頁均有密碼關卡；`docs/build-sitemap.py` 依規範排除 gated page，避免搜尋引擎收錄受保護課程 |
| Mobile tables | OK | CH3、CH4 已顯示「左右滑動查看完整欄位」提示；所有 lesson table 在窄螢幕統一水平捲動與欄寬規則 |
| Artifact naming | OK | Blueprint、Coverage Ledger、capstone 工作表統一使用 `course-capstone-handoff.md` |
| NotebookLM 實機 sentinel | OK | 3 個模擬來源加入、依來源回答「286 次取用」、引用點擊回查至 `[N01-P03]`；完整紀錄見 `_validation/L4B-NOTEBOOKLM-REAL-2026-09-16.md` |
| L4a bridge | DEGRADED | case1／case2 已獲資料傳輸授權並送出；兩案均 300 秒 timeout，無模型輸出與評分；case3／case4 暫停 |

## 發布判定

技術運維項目通過。sitemap 的 0 筆不是漏登錄，而是本課程採密碼保護後的預期結果；學員入口仍由總覽卡片、站內搜尋索引與直接網址提供。

本報告不代表已完成 Git commit 或 push；NotebookLM 已完成單一實機 sentinel，但 L4a bridge 連續 timeout，完整多情境驗收仍依專案發布流程與可用帳號另行確認。

## 下一步

1. 完成本輪模擬學員與 reviewer 的獨立回報整合；模擬學員重跑結果為 0 頁 BLOCK，reviewer 條件已回補。
2. 待 bridge 恢復後完成 L4a case3／case4 與 L5 冷跟做；或改用使用者可控的外部模型環境重新執行。
3. 審核本輪 diff 後，再由使用者決定是否 commit／push。
