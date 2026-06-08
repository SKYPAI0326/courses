# course-run 檢核紀錄 · gen-ai-140h

> 此課為成熟課（66+ HTML 已上線），course-run 於 Phase 2 增量加單元時才建檔。
> 既有 Part 1~7 主體不重跑 Gate。本檔只追蹤 **Phase 2 增量單元**。

## Phase 2 啟動閘門（使用者自設前置條件）

- **狀態：PASS**（2026-06-08，使用者確認）
- 條件 1 實體課跑通 + 學員真做出 GH Pages 連結 → ✅ 使用者確認
- 條件 2 0 基礎 persona 試做 CH5-5 + PRAC5-13~15 全過關 → ✅ 使用者確認
- 條件 3 無「太複雜想放棄」訊號 → ✅ 使用者確認

## Phase 2 範圍

本輪：**CH5-6** + **PRAC5-16**。PRAC5-17 **BLOCKED**（前置：講師需先建 `gen-ai-140h-api-proxy-template` repo）。
規格來源：`~/.claude/plans/image-1-140h-ai-github-github-gen-ai-ap-wiggly-robin.md`（CH5-6 @165、PRAC5-16 @195）。

## Gate 進度

| Gate | 狀態 | 備註 |
|------|------|------|
| G1 大綱 | PASS（繼承） | 成熟課；Phase 2 spec 在 plan + outline 補 CH5-6/PRAC5-16 |
| G2 教案 | PASS | `_lessons/gen-ai-140h/CH5-6.md`、`PRAC5-16.md` 完成 |
| G3 講義 HTML | PASS | `part5/CH5-6.html`(420行)、`part5/PRAC5-16.html` 建好；course-lesson-writer 並行產出、複製 sibling 殼；lint 0 BLOCKER、0 孤兒 class、Playwright smoke-test 0 JS 錯誤 |
| G4 收尾 | PASS | index 加 2 卡 + 學習單元→60 + CLAUDE.md Part5「6 CH」+ _outlines 標已上線 + search-index/sitemap 重建；gate 隨 sibling 複製已present |
| PRAC5-17 | BLOCKED | 待講師建 gen-ai-140h-api-proxy-template repo（fork→import→填 KEY 三步教學） |

## 設計鐵律（沿用 Phase 1）

複製→貼上→不要理解 / AI 是工具不是老師 / 錯了就重做 / 視覺地標 + 截圖驅動 / 「先回我」式提示詞。
套 Part 6 教訓：偏工程內容保留 mock/傻瓜路徑、真實部署設加分非必過。
