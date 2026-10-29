# 正式網頁講義技術驗證紀錄

- 日期：2026-10-24
- 範圍：`ai-short-video-editing/index.html`、CH0-1～CH1-4，共 9 頁
- 執行者：`tool-run`
- 不包含：零基礎真人跟做、4 小時題庫講解、3 小時證照考試

## 靜態檢查

| 檢查 | 結果 |
|---|---|
| `docs/lint-page.py` | 9 頁；BLOCKER 0、ERROR 0、WARN 0 |
| `validate-course-structure.py` | `checked=9 blocked=0` |
| `audit-course-substance.py` | 正式 9 頁逐頁均 `block=0`、`missing_assets=0`；語意審查仍須另判 |
| `audit_copy_continuity.py` | 9 頁均 0 warnings；仍保留人工閱讀責任 |

## 內建瀏覽器實測

以本機 HTTP 入口逐頁開啟正式版，測試 390×844、820×1180、1440×900 三種 viewport：

- 9 頁 × 3 尺寸，共 27 組。
- `documentElement.scrollWidth - clientWidth <= 1`：27／27 通過。
- 每頁唯一 `main#main`、`data-learner-content-root="true"`、`h1`：27／27 通過。
- header 未遮住 main，h1 可見：27／27 通過。
- 390×844 下 skip link 為第一個鍵盤焦點並抵達 `#main`：9／9 通過。
- 首頁、CH0-3、CH1-3 各保存手機、平板、桌面截圖，共 9 張，位於 `_validation/production-browser/`。

Deep Review 修正後以本機 Playwright 搭配 Google Chrome 重跑同一組 viewport 與 DOM 檢查；27／27 通過，並更新 9 張代表頁截圖。

## 結論

正式網頁版的確定性結構、連結、素材與響應式版面檢查通過。此結果不能解除 Deep Review 的兩項內容阻擋，也不能替代真人完整跟做；整體狀態維持 `BLOCKED`。
