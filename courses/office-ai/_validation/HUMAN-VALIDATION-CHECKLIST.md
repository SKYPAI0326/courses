# office-ai 真人與平台驗證清單

目前機器狀態：`MACHINE_READY_PENDING_HUMAN`。本清單用來把 pending evidence 補成可追溯紀錄；完成前不可宣告 `LEARNER_READ`、`PLATFORM_VERIFIED` 或 `HUMAN_READY`。

## 每個單元的測試順序

對 `CH1-1` 到 `CH6-3` 每一頁各找一位沒有看過教師筆記的冷讀者，使用正式 HTML、頁面列出的素材與必要的備援材料。測試者只在卡住後獲得最小提示，並記錄提示內容。

1. **Entry**：只給頁面，記錄 30 秒入口六題的回答、開始時間、第一個動作與提示。
2. **Completion**：讓測試者從起始材料完整跟做，保存完成物、檔名／位置／格式、耗時、卡點與修復。
3. **Understanding**：請測試者用自己的話說明關鍵判斷、為什麼這樣做、何時不能交給 AI；記錄原話與漏答。
4. **Transfer**：換一個同類但不同表面情境，要求測試者獨立完成並保存產物鏈；記錄哪些提示仍必要。

每筆紀錄必須包含測試日期、測試者身分（真人）、教材版本與 source/page/assets hash、實際材料、步驟、卡點、提示、自我修正、完成物路徑與結論。結果只可填 `PASS`、`FAIL` 或 `PENDING`，不可用作者模擬代填真人層。

## 必須實跑的平台

| 單元 | 實跑內容 | 必記環境 | 通過證據 |
|---|---|---|---|
| CH1-2 | 開啟 `courses/office-ai/assets/datasets/meeting-transcript-sample.txt`；分別以通用 LLM 與 Gemini Notebook 的指定來源工作模式完成同一個回查問題 | 帳號／方案、瀏覽器、平台版本、來源上傳結果、引用與失敗恢復 | 能說明自由生成與指定來源的差異，並從引用回到原文 |
| CH5-1 | 依頁面三種免費方案之一完成短句語音轉文字；核對原音與文字、權限與備援路徑 | 作業系統、瀏覽器、麥克風權限、工具版本、音檔／原音、轉錄結果 | 能完成轉錄、指出錯字並在權限失敗時改走備援 |
| CH6-1 | 下載並啟用 `ta-core` 與通用 `ta-work`；完成唯讀列本、來源鎖定、行政優先事項、缺資料宣告、預覽／確認／寫入與五項職務客製化 | 帳號／方案、Skills 與 Gemini Notebook 連接器狀態、目標筆記本、來源數、每步畫面與人工查核 | 八項辦公助理驗收證據齊全；自動寫入不可用時，須保存手動追加與備援標記 |
| CH6-3 | 下載並啟用 `ta-core` 與 `ta-learning`；以講師講義為核心完成唯讀列本、講義回查、引導式解惑、缺私人資訊測試、QA 受控沉澱與工作／學習移植 | 帳號／方案、Skills 與連接器狀態、課程 Notebook、來源數、引用、沉澱前後及 30 天表 | 八項結訓證據齊全；補充內容與講師原意可辨，原始講義保持唯讀 |

2026-10-16 已在指定付費帳號確認：`ta-core`、`ta-learning`、`ta-work` 已安裝，Gemini Notebook 連接器已啟用，且 `ta-core + ta-learning` 的唯讀列本指令能列出 15 本筆記本；未建立、修改或刪除 Notebook。這只證明安裝、連接器與唯讀入口，不能代替上表完整流程，也不能證明免費帳號路徑。

其他單元目前沒有宣稱特定平台通過；若測試中發現頁面實際依賴平台，新增 `platform` record 並更新 `platform_required`。

## 三課 sequence

至少選一組連續單元，例如 `CH1-1 -> CH1-2 -> CH1-3` 或 `CH3-1 -> CH3-2 -> CH3-3`。保存前課完成物、本課新增判斷、後課整合後的真實產物鏈；說明前課能力如何被下課使用、哪一個檢查避免錯誤累積。

## 回填方式

真人與平台紀錄放在 `courses/office-ai/_review/` 或 `_validation/`，每筆 record 綁定現行 source、page、assets hash，再重新執行：

```bash
bash /Users/paichenwei/.agents/skills/course-validator/scripts/course-validator.sh office-ai all
```

教材或素材一旦修改，先重新計算受影響 hash，再重做相關層級；不可只換 hash 沿用未重查的結論。

## 本輪 AI 分流優先順序

先看 [AI-TRIAGE-REPORT.md](../ai-simulated/AI-TRIAGE-REPORT.md)，依這個順序節省人工時間：

1. `CH1-1 → CH1-2 → CH1-3`：連續完成三課並保存產物鏈，補 sequence evidence。
2. `CH6-1`：在免費帳號完成八項辦公助理驗收，特別記錄 Skills 不可用及寫入不可用時的手動備援。
3. `CH6-3`：完成八項結訓驗收；第 1 天先保存可信來源、講義回查、缺資料測試與沉澱紀錄，第 30 天再回填耗時／錯誤率／品質比較。
4. `CH1-2`：用免費帳號實跑通用 LLM／Gemini Notebook、來源上傳、引用回查與失敗恢復。
5. `CH5-1`：用指定瀏覽器與麥克風完成 Google 文件語音輸入，核對原音、轉錄、權限與備援。
6. 其他單元：先抽查 LLM 判定 PASS 的入口、完成物與遷移；遇到提示或無法保存產物，再建立對應 human record。

AI 的 PASS 只表示目前模擬找不到確定性缺口；它不能替代真人 record，也不會解除 validator 的 human pending。
