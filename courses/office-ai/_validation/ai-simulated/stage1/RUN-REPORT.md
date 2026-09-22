# Stage 1 Simulated Learner Run: office-ai

- run_date: `2026-09-22`
- actor: `independent-ai`
- model: `gpt-6 (Codex current session)`
- prompt_revision: `simulated-learner-v1`
- context_manifest: `courses/office-ai/_validation/ai-simulated/context/manifest.json`
- context_manifest_sha256: `ad58f510dd1d0c27f1900ea722e9713228c74f2ee79184f575bd116dd1ec6ae0`
- unit_count: `19`
- simulated_not_human: `true`

## Coverage

每個單元各一份 JSON log，依序回答 `entry`、`completion`、`understanding`、`transfer`。輸入只包含 learner-facing visible context 與該頁直接引用的素材；沒有把正式 source、作者 review 或 validator report 送入模擬。

## Verdict counts

- `completion:PASS`: 17
- `completion:PENDING`: 2
- `entry:PASS`: 19
- `transfer:PASS`: 18
- `transfer:PENDING`: 1
- `understanding:PASS`: 19

## Confidence counts

- `completion:high`: 17
- `completion:low`: 1
- `completion:medium`: 1
- `entry:high`: 19
- `transfer:high`: 18
- `transfer:medium`: 1
- `understanding:high`: 19

## Deterministic verification

```bash
python3 office-ai/_tools/validate-ai-review-output.py --stage stage1 --dir office-ai/_validation/ai-simulated/stage1
python3 office-ai/_tools/test-ai-review-output.py --stage stage1
```

結果：19 logs 通過；artifact page／asset hash 與當前 context 一致。

## Limitations

這是獨立 AI 模擬，不是真人冷讀。它不能證明真人理解、操作速度、動機、外部平台權限、麥克風狀態或 30 天後的真實遷移。`CH1-2`、`CH5-1` 的平台執行，以及 `CH6-3` 的長期計畫，保留為 `PENDING`。
