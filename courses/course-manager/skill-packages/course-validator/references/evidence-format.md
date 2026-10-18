# 課程版本證據格式（schema_version 1）

`courses/{slug}/_validation/evidence.json` 是交接索引，審查與實測正文放 `_review/` 或 `_validation/` 的紀錄檔。路徑一律相對專案根目錄，sha256 由實檔計算。先建立大綱與單元清單；每單元只有一份 source。assets 列出所有核心外部檔案，內嵌正文的材料由 source hash 涵蓋。

```json
{
  "schema_version": 1,
  "outline": {"path": "_outlines/demo.md", "sha256": "實檔SHA256"},
  "scope_note": "本輪覆蓋大綱全部三單元；不含選修分支",
  "units": [{
    "id": "CH1-1", "course_type": "concept",
    "source": "_lessons/demo/CH1-1.md",
    "page": "courses/demo/CH1-1.html", "assets": [],
    "platform_required": false, "platform_reason": "紙筆推導，無外部平台"
  }],
  "records": [{
    "layer": "content", "unit_ids": ["CH1-1"],
    "actor": "author-self-check", "verdict": "PASS",
    "notes": "已逐項核對正式正文中的定義、推理、練習及答案；此為作者自審。",
    "log": {"path": "courses/demo/_review/CH1-1-content.md", "sha256": "紀錄SHA256"},
    "artifacts": [{"path": "_lessons/demo/CH1-1.md", "sha256": "來源SHA256"}]
  }]
}
```

允許 layer：technical、content、fidelity、entry、completion、understanding、transfer、platform、sequence；actor：author-self-check、independent-ai、human、tool-run；verdict：PASS、FAIL、PENDING。真人紀錄由實際受測結果填入，作者／模型不能代填。

- technical：實際跑逐頁 lint、連結與必要程式檢查，log 保留命令範圍與結果；actor 為 tool-run 或 human，與語意審查分列。
- content：綁 source 與指定 assets；先於 HTML。執行 `course-validator.sh <slug> content --unit CH1-1` 檢查交接；PASS 僅由 reviewer 讀正文後記錄。
- 其他層：綁 source、page 及全部指定／頁面實際引用的學員 assets；fidelity 需逐項比對內容，不以字串比例自動通過。
- 每份 log 記測試時間、實際教材範圍、方法、引用或動作、結果；跟做另記卡點、提示、自我修正、完成物與答案。讀者身分與測試模式明示，程式不能辨識真人身分。
- sequence：unit_ids 至少涵蓋三個代表性連續單元，不足三課時全數；log 記前課能力、本課新增判斷、後課整合，有真實產物鏈再核對檔案。
- 相同 layer／unit_ids／actor 的後一筆替代前一筆為現行證據，舊紀錄保留。變更教材後重測或附影響分析重審，重新計算 hash；禁止只改 hash 而沿用未查過的結論。
- outline hash 與 scope_note 防止悄悄換範圍；reviewer 仍需核對單元清單與大綱一致，機器不解析自然語言大綱來推定完整性。

工具只驗版本、確定性條件及必要紀錄。缺 technical／content／fidelity、未解 FAIL 或版本過期為 BLOCKED；這些齊全而真人或適用平台缺驗，為 MACHINE_READY_PENDING_HUMAN。完整正式狀態語義仍以 learner-action-contract.md 為準。

## 獨立試學紀錄

代表單元與全課試走另存一份符合 `contracts/course-trial-record.schema.json` 的 JSON。G4 的 `scope` 固定為 `representative_unit`；G5 固定為 `full_course`。這份紀錄描述執行事實，不是心得或審查摘要。

```json
{
  "schema_version": 1,
  "scope": "representative_unit",
  "participant": {
    "id": "cold-learner-ai-01",
    "type": "independent-ai",
    "roles": ["learner-trial"]
  },
  "isolated_context_id": "cold-run-20261018-01",
  "allowed_inputs": [{
    "kind": "learner-page",
    "path": "courses/demo/unit-1.html",
    "sha256": "64位小寫SHA256"
  }],
  "forbidden_inputs_accessed": [],
  "entry": {
    "started_at": "2026-10-18T15:00:00+08:00",
    "page": "courses/demo/unit-1.html",
    "goal_understood": true,
    "materials_found": true
  },
  "actions": [{
    "sequence": 1,
    "action": "開啟學員素材並找出預算與截止日。",
    "observable_result": "在資料表找到兩個欄位。",
    "at": "2026-10-18T15:01:00+08:00"
  }],
  "hints": [{
    "source": "learner-page",
    "detail": "使用頁面中資料不完整時的修復提示。"
  }],
  "blocks": [{
    "code": "practice_instruction_gap",
    "detail": "第一次沒有注意到預算必須拆分。",
    "recovered": true
  }],
  "recovery": [{
    "block_code": "practice_instruction_gap",
    "action": "回到商品資料核對預算欄。",
    "result": "修正後通過頁面檢查。"
  }],
  "artifact": {
    "path": "trial-output/cold-run-20261018-01/plan.pdf",
    "sha256": "64位小寫SHA256",
    "complete": true,
    "verifiable": true,
    "acceptance_result": "PASS"
  },
  "result": {
    "status": "PASS",
    "completed_at": "2026-10-18T15:10:00+08:00",
    "notes": "只依學員可見頁面與素材完成。"
  }
}
```

真人試學把 `participant.type` 設為 `human`，並加上 `human_participant_evidence`，其中必須有 consent record、observer ID 與 session recording SHA-256。沒有這些證據時最多只能保留較低成熟度，不能標記 `HUMAN_VERIFIED`。

試走紀錄的 SHA-256 連同製作證據 ID 寫入 contract `evidence_index`。Gate PASS event 必須同時引用製作證據與試走證據，並記錄 `INDEPENDENT_AI_VERIFIED`；缺任一類都不能完成 G4 或 G5。
