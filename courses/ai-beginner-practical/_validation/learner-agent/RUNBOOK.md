# 學員 Agent 執行手冊

## 1. 建立實際頁面證據

在課程網站根目錄執行：

```bash
python3 courses/ai-beginner-practical/_validation/learner-agent/build_manifest.py \
  --course-root courses/ai-beginner-practical \
  --output courses/ai-beginner-practical/_validation/learner-agent/evidence-manifest.json
```

確認輸出包含 6 個頁面與 19 個學員素材，再執行：

```bash
python3 courses/ai-beginner-practical/_validation/learner-agent/test_manifest_contract.py
```

## 2. 執行 Agent

把 `L5-learner-agent-prompt.txt` 作為 Agent 指令，並附上同一課程根目錄的 `evidence-manifest.json`。若使用外部模型服務，先確認使用者已授權傳輸課程頁面與素材內容；未授權時只建立 manifest，不執行外部呼叫。

Agent 必須以三 persona 各跑一次完整核心路徑。實際瀏覽器、文字型 LLM 或 NotebookLM 不可用時，要標 `blocked`，不可用想像中的輸出補成 `done`。

## 3. 寫回驗證結果

將 Agent 的 Markdown 與 JSON 輸出保存為：

```text
_validation/learner-agent/L5-result-YYYY-MM-DD.md
_validation/learner-agent/L5-result-YYYY-MM-DD.json
```

結果至少要包含三人的第一個卡點、核心完成物、證據頁面、五項子分數、隔週回頭使用率及修補建議。

## 4. 判讀

| 結果 | 動作 |
| --- | --- |
| 平均 ≥ 7、回頭率 ≥ 60%、無核心阻斷 | 可將 L5 送人工複核，再考慮更新 G5 |
| 平均 ≥ 7 但有可修補卡點 | 修補後重跑同一 persona，保留前後結果 |
| 平均 < 7 或回頭率 < 60% | 不得發布，先處理最弱 persona 的第一個阻斷 |
| NotebookLM 無實機證據 | L4b 維持待驗，不得用 L5 推論代替 |

## 5. 修補迴圈

1. 先修學員看得到的頁面、素材或完成物路徑。
2. 重新建立 manifest，確認頁面 hash 已更新。
3. 只重跑受影響的 persona 與步驟，再跑一次三人主線。
4. 將前後分數、消失的阻斷與仍存在的證據缺口寫入結果。
5. 只有在人工確認輸出真的是學員頁面證據後，才更新 `_gates.md`。
