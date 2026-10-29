# 既有資料／提示詞 L0–L5 專項流程

只在資料集或提示詞課程使用；外部 Codex consult 需當次授權。通用課程使用本機 evidence.json，不需要 CSV、四個案例或模型分數。

- L0：有數值真值需求時執行課程自己的 `_validation/L0-generate.py`，參考 scripts/L0-template.py。
- L1-L3：資料／提示詞專項檢查；先閱讀 scripts/run-L1-L2-L3.sh 與 L3-prompt-parser.py 的適用條件，不套用到非提示詞課。
- L4a：已授權才用 codex-consult-wrapper.sh 模擬案例，記錄 Call ID、實際輸入輸出及採納理由。
- L4b：模型的 sentinel 建議只列待查；平台驗證須真的在指定帳號路徑跑過。
- L5：若啟用獨立 AI，提供實際學員頁及素材、版本與任務，不提供作者推理及預期判決，明示 independent-ai。

命令：`bash scripts/course-validator.sh <slug> L0`（其餘層同理）。舊方法論目錄由 COURSE_VALIDATOR_SSOT 指定。preflight/報告/all 的通用入口不依賴此目錄，也不自動呼叫外部模型。

舊 status.jsonl 僅為歷史執行記錄，不供正式放行；把經核對的實際證據依 evidence-format.md 匯入，不能把 OK／高分直接翻成 PASS。
