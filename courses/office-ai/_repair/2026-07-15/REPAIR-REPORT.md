# Repair Report: office-ai

**執行日期**：2026-07-15
**範圍**：19 個單元頁，Batch 1–10
**依據**：`SCAN.md`、`REPAIR-PLAN.md`、Learner Action Contract

## 修復摘要

- 15 個操作型單元補上可辨識完成物、起始狀態、5–12 步最短成功路徑、checkpoint、卡關修復與變化練習。
- 4 個概念型單元補上可保存產物與可核對練習：
  - CH1-1：任務適配判斷表（4 個情境）
  - CH1-2：工具選擇卡（4 個情境）
  - CH6-2：去識別化檢查表（4 個情境）
  - CH6-3：30 天應用計畫與 3 題自我檢查
- 19 頁字階改為 V4 白名單值，補 `data-built-at="2026-07-15"`。
- 學員敘述統一使用「你」；正式信件範例中的稱謂也已依本批 lint 要求統一。

## Reviewer 結果

### BLOCKER

無。

### MAJOR / Remaining

1. **案例真跑證據仍不完整**：本課沒有 `_lessons/office-ai/`，也沒有可供 L0 truth table 使用的本地 dataset；既有 AI 輸出案例本批未重新呼叫各平台重跑。頁面保留原案例與警示，不把本次修復描述成平台真跑。
2. **平台 UI 僅部分核對**：CH5-1 的 Google 文件語音輸入路徑已對照 Google 官方說明；其餘精確介面文字未逐一做 2026-07-15 live UI 驗證，`data-platform-version` 因此保留 `2026-04-v3`，未冒進更新。
3. **視覺人工抽查待執行**：lint 已清零，但本批未完成桌面與 mobile 的瀏覽器逐頁視覺走查。

**Reviewer 放行建議**：CONDITIONAL-PASS。Learner Action Contract 的 BLOCKER 已排除；上述三項保留為後續真跑與視覺驗收工作。

## Ops 驗證

| 項目 | 結果 |
|---|---|
| `lint-page.py courses/office-ai/` | 20 頁；0 BLOCKER、0 ERROR、0 WARN |
| 內部相對連結 | 117 筆；0 broken |
| 密碼 gate | 20 / 20 頁存在 |
| SEO description / OG title | 20 / 20 頁存在 |
| 搜尋索引 | 重建成功；全站 649 筆，其中 office-ai 20 筆 |
| Sitemap | 重建成功；全站 42 筆；office-ai 因全課有 gate，依產生器規則不收錄 |

## Validator 結果

- Preflight：24 PASS、0 WARN、0 FAIL。
- L1：20 頁 lint 全綠。
- L2：未指定跨檔錯誤數字 pattern，跳過。
- L3：找不到 `prompts-*.md`，跳過。
- L0 / L4a / L4b / L5：不在本修復計畫 Batch 10 的 preflight 驗收範圍；未標記為已通過。
- 執行紀錄：`courses/office-ai/_validation/status.jsonl`、`L1-L2-L3-static.txt`。

## 還原方式

```bash
bash courses/office-ai/_tools/restore-2026-07-15-pre-repair.sh
```

還原來源：`courses/office-ai/_backup/2026-07-15-pre-repair/`（19 頁）。還原後須重新執行 lint、搜尋索引與 sitemap 產生器。

## 結論

Batch 1–10 的內容修復與靜態／運維驗收已完成。課程目前達到 0 lint issue、0 內部斷鏈、gate 完整；完整 G5 真跑與瀏覽器視覺驗收仍明確列為後續工作，未冒充完成。
