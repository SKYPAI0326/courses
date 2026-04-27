# gen-ai-140h 學習資產 Schema

> 對應 §1 I-6 (Learning Continuity / Reuse)。這是學員作品集 / 反思 / 證據提交的統一資料結構。
> Phase 1 Task 2 建立。後續 Task 3-9 的元件全部寫入 / 讀取依此 schema。

## localStorage Key 命名

統一前綴 `gen140_`，依類型分子前綴：

| Key 模式 | 內容類型 | 範例 |
|----------|---------|------|
| `gen140_artifact_{ak}` | 單一作品 JSON | `gen140_artifact_prac1-1-prompt-builder` |
| `gen140_artifact_index` | 所有 ak 列表 + 元資料 | `[{"ak":"prac1-1-...", "title":"...", "savedAt":"..."}]` |
| `gen140_reflect_{rk}` | 反思文字 | `gen140_reflect_ch1-2-r1` |
| `gen140_peer_{pk}` | bool（同儕完成） | `gen140_peer_ch1-2-peer-1` |
| `gen140_check_{ck}` | bool（自評/講師勾） | `gen140_check_ch1-2-ic` |
| `gen140_check_{ck}_feedback` | 講師回饋摘要（搭配 check） | `gen140_check_ch1-2-ic_feedback` |
| `gen140_evidence_{ek}` | 證據 JSON | `gen140_evidence_prac4-3-deploy` |
| `gen140_recycle_{rk}` | AI 回收 JSON | `gen140_recycle_prac1-1-recycle` |
| `gen140_realtask_{tk}` | 真實任務改寫 JSON | `gen140_realtask_prac1-1-rt` |

## Artifact JSON 結構

```json
{
  "ak": "prac1-1-prompt-builder",
  "title": "我的 Prompt 黃金公式（PRAC1-1）",
  "sourcePage": "part1/PRAC1-1.html",
  "kind": "prompt | workflow | tool-page | reflection | evidence",
  "content": {
    "role": "...",
    "task": "...",
    "constraint": "...",
    "output": "..."
  },
  "savedAt": "2026-05-01T10:30:00+08:00",
  "tags": ["prompt", "p1"]
}
```

## kind 列舉

- `prompt`：PRAC1-1 ~ PRAC1-4 等 prompt 設計類
- `workflow`：PRAC3-* 自動化流程類
- `tool-page`：PRAC4-* / PRAC5-* 工具或網頁類
- `reflection`：CH 頁的反思留答
- `evidence`：截圖 / 部署 URL 等證據型

## 跨單元引用（Future-proof）

`content.refs: ["prac1-1-prompt-builder"]` — 表示此作品引用了 PRAC1-1 的產出，用於 Phase 2+ 的「學習軌跡」視覺化。Phase 1 不實作此欄位，schema 留位即可。

## 變更紀錄

- 2026-04-27 Phase 1 Task 2 建立。
