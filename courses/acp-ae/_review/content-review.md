# ACP-AE 學員內容審查

審查日期：2026-10-16

## 結論

學員版正文已完成結構與內容自審，可進入試教；After Effects 實機路徑與真人 cold follow-along 尚未完成，不能標示為正式可授課版。

2026-10-16 已完成零基礎文案修復：所有 10 課先用直白情境說明目標；操作段落改為 Step by Step，並補上操作、應看到的結果、checkpoint 或卡住時的回復方式。

## 審查結果

| 項目 | 結果 | 證據 |
|---|---|---|
| 9 小時配置 | PASS | Part 1 300 分鐘、Part 2 60 分鐘、Part 3 180 分鐘 |
| 正式單元 | PASS | `_lessons/acp-ae/` 共 10 份，皆含第一個動作、成功訊號、完成檢查與修復 |
| 學員視角 | PASS | HTML 未出現「講師示範」或敬稱式第二人稱；活動直接對學員說明行動與證據 |
| Part 1 基礎鏈 | PASS | 從空白 Project 到 Composition、Layer、Keyframe、合成、輸出與 PRAC1 |
| Part 2 概念題 | PASS | 13 題自製同能力題，要求答案、線索、依據與排除理由 |
| Part 3 操作題 | PASS | 40 張路徑卡全部覆蓋；9 題具完整代表實作 |
| 完成證據 | PASS | 每課皆列出可觀察結果、命名、存檔或畫面狀態 |
| 復原路徑 | PASS | 每課在操作當下提供常見錯誤、修復方式與完成檢查，不要求跳離講義查看另一份檔案 |
| 零基礎可讀性 | PASS（機器與人工內容審查） | 10 課均含 Step by Step；Part 1 每一核心操作附「操作／應看到／如果沒有」，Part 2 使用四步判斷，Part 3 使用六步讀題與代表題逐步操作 |
| 內容授權邊界 | PASS | 使用自製能力題與摘要映射，未嵌入原書完整題文或頁面截圖 |
| AE 實機驗證 | BLOCKED | 本機未安裝 After Effects，介面名稱與步驟須在授課機 v25.x 重跑 |
| 真人跟做 | PENDING | 尚未由目標學員依講義獨立完成 9 小時路徑 |

## 試教前必做

1. 在實際授課電腦建立空白 `ACP-AE-Lab.aep`，依 10 課從頭重做。
2. 記錄任何介面名稱、位置或預設值差異，逐頁更新 `data-platform-version`。
3. 安排至少一位目標學員 cold follow-along，只提供講義中已寫出的復原資訊。
4. 確認 9 題代表實作能產生講義要求的證據，再解除 `HUMAN_READY` 的 PENDING。

## 本輪修復證據

- 修復範圍與做法：`_repair/2026-10-16-beginner-step-by-step/REPAIR-PLAN.md`
- 回復工具：`_tools/restore-2026-10-16-pre-beginner-rewrite.sh`
- 驗收結果：`_repair/2026-10-16-beginner-step-by-step/REPAIR-REPORT.md`
