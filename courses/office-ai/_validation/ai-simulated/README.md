# office-ai LLM 模擬學員檢視

這個目錄保存 learner-only context、版本化 prompt、LLM 輸出與分流報告。LLM 結果使用 `actor: independent-ai`，並且永遠帶有 `simulated_not_human: true`。它只能協助排序人工檢測，不能取代 `human`、平台實跑或三課 sequence 證據。

## 執行順序

1. `build-ai-review-context.py` 從 learner-facing HTML 建立 19 個隔離 context。
2. 使用 `simulated-learner-v1.md` 逐單元產生 stage-1 JSON。
3. 使用 output validator 驗證欄位、citation 與當前 hash。
4. 依 stage-1 的 BLOCKER／MAJOR、低信心、平台頁、flagship 與 sequence 選出 stage-2 scope。
5. 使用 `adversarial-review-v1.md` 產生 stage-2 JSON。
6. 合併 AI records 並產生 `AI-TRIAGE-REPORT.md`。
7. 重新執行 `course-validator.sh office-ai all`；若真人或平台未驗證，狀態仍為 `MACHINE_READY_PENDING_HUMAN`。

任何 source、HTML、素材或 prompt revision 變更都會使相關 AI log 的 hash 失效，必須重跑。
