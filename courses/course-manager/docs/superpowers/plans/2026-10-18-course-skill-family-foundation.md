# Course Skill Family Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立課程契約、Gate 狀態機、G0–G2 母控流程與新的外部研究 Skill，完成新課系統第一個可運行垂直切片。

**Architecture:** 課程狀態使用 `_design/{slug}/course-contract.json` 作唯一來源，由 Python 標準函式庫提供驗證、原子寫入、Gate 轉換及變更影響傳播。`course-run` 是唯一母入口，`course-researcher` 產出 G1 研究證據，既有 `course-pm` 改為只處理 G2；Skill 先在 `skill-packages/` 建置與驗證，再透過可回復安裝器同步至本機 Skill 目錄。

**Tech Stack:** Python 3 標準函式庫、`unittest`、JSON／JSON Schema 文件、Markdown Skill 套件

**Spec:** `docs/superpowers/specs/2026-10-18-course-design-skill-family-design.md`

## Global Constraints

- Gate 固定為 `G0` 至 `G6`，狀態固定為 `DRAFT`、`REVIEW`、`APPROVED`、`BLOCKED`、`STALE`。
- 子 Skill 可提交成果與證據，只有母 Skill 在取得使用者明確核准後可寫入 `APPROVED`。
- Gate 核准後凍結；語義變更使最早受影響 Gate 回到 `DRAFT`，所有下游 Gate 成為 `STALE`。
- Gate lifecycle 與 `MACHINE_CHECKED`、`LEARNER_READ`、`PLATFORM_VERIFIED`、`HUMAN_READY` 等證據成熟度分開。
- G1 不使用固定來源數量；重要主張必須有來源、日期、版本或適用情境及設計含義。
- 高工具依賴課程缺少代表性實測時必須 `BLOCKED`。
- 課程契約只保存結構化狀態及證據索引；長篇研究、正文與測試紀錄留在外部檔案並以相對路徑和 SHA-256 連結。
- 正常可讀文案不得因 schema、摘要或 Skill 重構被壓縮成片語、欄位清單或待辦事項。
- 本計畫不修改任何既有課程內容、HTML、大綱或目前工作區中的其他使用者變更。
- 不新增第三方 Python 相依套件。

## Review Focus

- 非法或含路徑穿越的 `slug` 必須拒絕，不能在 `_design/` 外建立契約；Task 1 測試。
- 未核准前置 Gate、仍有 blocker 或缺少使用者核准資訊時，不得進入 `APPROVED`；Task 2 測試。
- 上游語義變更與純排版／錯字修正必須產生不同的失效範圍；Task 2 測試。
- 高工具依賴、快速變動的研究缺少實測或複查日期時必須失敗；Task 4 測試。
- 讀取、驗證與產生摘要不得改寫或截短使用者原始需求與完整敘述；Task 3 整體測試。

---

### Task 1: 課程契約資料模型與基本驗證

**Files:**
- Create: `contracts/course-contract.schema.json`
- Create: `src/course_contract.py`
- Create: `tests/test_course_contract.py`

**Interfaces:**
- Produces: `GATE_ORDER: tuple[str, ...]`
- Produces: `GATE_STATUSES: frozenset[str]`
- Produces: `ValidationIssue(code: str, path: str, message: str)`
- Produces: `new_contract(slug: str, title: str, created_by: str, created_at: str) -> dict[str, Any]`
- Produces: `validate_contract(contract: Mapping[str, Any]) -> list[ValidationIssue]`
- Produces: `load_contract(path: Path) -> dict[str, Any]`
- Produces: `save_contract_atomic(path: Path, contract: Mapping[str, Any]) -> None`

- [ ] **Step 1: Write failing model tests**

Add tests named:

- `test_new_contract_has_all_gates_and_single_state_source`
- `test_validate_rejects_unknown_gate_status`
- `test_validate_rejects_missing_required_gate_fields`
- `test_new_contract_rejects_path_traversal_slug`
- `test_atomic_save_round_trips_utf8_prose_without_rewriting`

Assert the exact seven Gate IDs, five statuses, required top-level sections, and byte-for-byte preservation of Traditional Chinese prose after JSON round-trip.

- [ ] **Step 2: Run model tests and confirm they fail**

Run: `python3 -m unittest tests.test_course_contract -v`

Expected: FAIL because `src.course_contract` does not exist.

- [ ] **Step 3: Add the JSON schema document**

Define `schema_version: 1`, the fixed Gate IDs and statuses, required Gate fields, `changes`, `evidence_index`, and G0–G6 sections. Use `additionalProperties` deliberately: closed for status-bearing records, open for evolving Gate payloads.

- [ ] **Step 4: Implement the contract model**

Implement the listed interfaces with Python standard library only. Validate `slug` with `^[a-z0-9]+(?:-[a-z0-9]+)*$`; write JSON through a temporary sibling file followed by `os.replace`.

- [ ] **Step 5: Run model tests**

Run: `python3 -m unittest tests.test_course_contract -v`

Expected: all Task 1 tests PASS.

- [ ] **Step 6: Commit Task 1 with explicit paths**

```bash
git add contracts/course-contract.schema.json src/course_contract.py tests/test_course_contract.py
git commit -m "feat: add course contract model"
```

### Task 2: Gate 狀態機與變更影響傳播

**Files:**
- Modify: `src/course_contract.py`
- Modify: `tests/test_course_contract.py`

**Interfaces:**
- Consumes: Task 1 contract dictionaries and `ValidationIssue`
- Produces: `submit_gate(contract: MutableMapping[str, Any], gate_id: str, actor: str, at: str) -> None`
- Produces: `approve_gate(contract: MutableMapping[str, Any], gate_id: str, approved_by: str, approved_at: str, approval_note: str) -> None`
- Produces: `block_gate(contract: MutableMapping[str, Any], gate_id: str, reason: str, actor: str, at: str) -> None`
- Produces: `record_change(contract: MutableMapping[str, Any], affected_gate: str, reason: str, actor: str, at: str, semantic: bool) -> list[str]`
- Produces: `ContractStateError`

- [ ] **Step 1: Write failing state-transition tests**

Add tests named:

- `test_submit_requires_previous_gate_approval`
- `test_approve_requires_review_state_and_user_approval_fields`
- `test_approve_rejects_unresolved_blockers`
- `test_child_submission_cannot_mark_gate_approved`
- `test_semantic_change_resets_affected_gate_and_stales_downstream`
- `test_nonsemantic_change_preserves_gate_states`
- `test_blocked_gate_can_return_to_draft_but_cannot_skip_review`

- [ ] **Step 2: Run the new tests and confirm failure**

Run: `python3 -m unittest tests.test_course_contract -v`

Expected: new tests FAIL because transition functions do not exist.

- [ ] **Step 3: Implement the state machine**

Use one transition table. `approve_gate` must reject empty approver, timestamp or approval note, any unresolved `risks` item with `blocking: true`, and any non-approved previous Gate. `record_change(..., semantic=True)` appends one immutable change record, sets the affected Gate to `DRAFT`, clears its approval fields, and marks only later Gates `STALE`.

- [ ] **Step 4: Run state-transition tests**

Run: `python3 -m unittest tests.test_course_contract -v`

Expected: all Task 1–2 tests PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add src/course_contract.py tests/test_course_contract.py
git commit -m "feat: govern course gate transitions"
```

### Task 3: 課程契約 CLI 與人類可讀摘要

**Files:**
- Create: `scripts/course_contract.py`
- Create: `tests/test_course_contract_cli.py`
- Modify: `src/course_contract.py`

**Interfaces:**
- Consumes: Task 1–2 model and transition functions
- Produces: `render_gate_summary(contract: Mapping[str, Any]) -> str`
- Produces CLI commands: `init`, `validate`, `status`, `submit`, `approve`, `block`, `change`

- [ ] **Step 1: Write failing CLI tests**

Use `tempfile.TemporaryDirectory` and subprocess invocation. Add tests named:

- `test_init_writes_design_contract_at_expected_path`
- `test_status_reports_gate_state_evidence_risks_and_next_action`
- `test_approve_requires_explicit_approval_note`
- `test_change_semantic_flag_controls_invalidation`
- `test_validate_returns_nonzero_for_invalid_contract`
- `test_status_does_not_mutate_or_summarize_away_original_prose`

- [ ] **Step 2: Run CLI tests and confirm failure**

Run: `python3 -m unittest tests.test_course_contract_cli -v`

Expected: FAIL because the CLI does not exist.

- [ ] **Step 3: Implement summary rendering**

Render current Gate, state, deliverables, evidence references, blockers, risks, open questions and allowed next action. Do not copy long prose into abbreviated replacements; link to its contract field or evidence file.

- [ ] **Step 4: Implement CLI commands**

`init --root ROOT --slug SLUG --title TITLE --created-by NAME --at ISO8601` writes `ROOT/_design/SLUG/course-contract.json`. Mutation commands must load, apply one domain operation, validate, and atomically save. `status` and `validate` are read-only.

- [ ] **Step 5: Run CLI and model tests**

Run: `python3 -m unittest tests.test_course_contract tests.test_course_contract_cli -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add scripts/course_contract.py src/course_contract.py tests/test_course_contract_cli.py
git commit -m "feat: add course contract command interface"
```

### Task 4: G1 研究證據格式與驗證器

**Files:**
- Create: `contracts/course-research-record.schema.json`
- Create: `src/course_research.py`
- Create: `tests/test_course_research.py`

**Interfaces:**
- Consumes: G0 facts and adaptation dimensions from the course contract
- Produces: `validate_research_record(record: Mapping[str, Any], adaptation: Mapping[str, Any]) -> list[ResearchIssue]`
- Produces: `ResearchIssue(code: str, path: str, message: str)`
- Produces: `research_ready(record: Mapping[str, Any], adaptation: Mapping[str, Any]) -> bool`

- [ ] **Step 1: Write failing research validation tests**

Add tests named:

- `test_claim_requires_source_date_context_and_design_implication`
- `test_no_fixed_source_count_when_decisions_are_supported`
- `test_conflicting_sources_and_unknowns_are_preserved`
- `test_high_tool_dependency_requires_hands_on_execution`
- `test_high_volatility_requires_review_due_and_owner`
- `test_hands_on_failure_can_be_valid_evidence_but_blocks_readiness`
- `test_research_implication_must_reference_claim_or_hands_on_record`

- [ ] **Step 2: Run tests and confirm failure**

Run: `python3 -m unittest tests.test_course_research -v`

Expected: FAIL because `src.course_research` does not exist.

- [ ] **Step 3: Add the research schema**

Define research questions, claims, sources, conflicts, unknowns, representative task, hands-on record, design implications and maintenance fields. Require stable IDs for claims and implications so G2 can cite them.

- [ ] **Step 4: Implement semantic validation**

Treat source count as irrelevant. Require evidence links for decisions; require `executed`, environment, input, result, failure notes and limitations when tool dependency is `high`; require review owner and ISO date when volatility is `high`.

- [ ] **Step 5: Run research tests**

Run: `python3 -m unittest tests.test_course_research -v`

Expected: all Task 4 tests PASS.

- [ ] **Step 6: Commit Task 4**

```bash
git add contracts/course-research-record.schema.json src/course_research.py tests/test_course_research.py
git commit -m "feat: validate course research evidence"
```

### Task 5: 重構後的 `course-run` Skill 套件

**Files:**
- Create: `skill-packages/course-run/SKILL.md`
- Create: `skill-packages/course-run/agents/openai.yaml`
- Create: `skill-packages/course-run/references/course-contract-routing.md`
- Create: `skill-packages/course-run/references/gate-routing.json`
- Create: `tests/test_course_skill_packages.py`

**Interfaces:**
- Consumes: `scripts/course_contract.py`, approved design spec, packaged child Skill names
- Produces: one public orchestration entry for G0–G6

- [ ] **Step 1: Write failing package tests**

Add tests named:

- `test_all_skill_package_references_exist`
- `test_gate_routing_has_exact_g0_through_g6_order`
- `test_gate_routing_requires_user_approval_for_every_gate`
- `test_gate_routing_gives_children_submit_but_not_approve_authority`
- `test_gate_routing_routes_missing_required_evidence_to_blocked`
- `test_gate_routing_separates_lifecycle_from_evidence_maturity`

These tests load the routing data and referenced files; they do not match prose style or force specific wording.

- [ ] **Step 2: Run package tests and confirm failure**

Run: `python3 -m unittest tests.test_course_skill_packages -v`

Expected: FAIL because the package does not exist.

- [ ] **Step 3: Write `course-run/SKILL.md`**

Keep the body focused on entry routing, adaptive G0 questioning, Gate stop behavior, approval handling, child dispatch, `BLOCKED` rules and change control. Reference shared files for schema details. Do not copy the 410-line design spec into the Skill. Put the deterministic Gate order, prerequisites, producer capability, approval authority and blocked behavior in `gate-routing.json`.

- [ ] **Step 4: Write routing reference and UI metadata**

Define exact child capability called at each Gate, expected return fields, and the command used to read or mutate contract status. Generate UI metadata with:

```bash
python3 /Users/paichenwei/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py \
  skill-packages/course-run \
  --interface 'display_name=課程流程總籌' \
  --interface 'short_description=以課程契約與核准 Gate 推進新課設計' \
  --interface 'default_prompt=使用 $course-run 從需求問答開始建立一門新課。'
```

- [ ] **Step 5: Run package tests**

Run: `python3 -m unittest tests.test_course_skill_packages -v`

Expected: all Task 5 tests PASS.

- [ ] **Step 6: Commit Task 5**

```bash
git add skill-packages/course-run tests/test_course_skill_packages.py
git commit -m "feat: package gated course orchestrator"
```

### Task 6: 新增 `course-researcher` 並收斂 `course-pm`

**Files:**
- Create: `skill-packages/course-researcher/SKILL.md`
- Create: `skill-packages/course-researcher/agents/openai.yaml`
- Create: `skill-packages/course-researcher/references/research-evidence.md`
- Create: `skill-packages/course-pm/SKILL.md`
- Create: `skill-packages/course-pm/agents/openai.yaml`
- Create: `skill-packages/course-pm/references/architecture-output.md`
- Modify: `tests/test_course_skill_packages.py`

**Interfaces:**
- Consumes: approved G0 contract section
- Produces from researcher: research record path, evidence hash, adaptation, blockers and G1 recommendation
- Consumes in PM: approved G0, approved G1 and adaptation
- Produces from PM: one G2 course blueprint with outcomes, assessment, capability progression, units, dependencies, duration fit and material risks

- [ ] **Step 1: Write failing researcher and PM package tests**

Add tests named:

- `test_researcher_requires_external_current_sources`
- `test_researcher_requires_hands_on_for_high_tool_dependency`
- `test_researcher_records_conflicts_unknowns_and_non_conclusions`
- `test_researcher_does_not_use_source_count_as_pass_condition`
- `test_pm_does_not_repeat_g0_interview`
- `test_pm_requires_approved_g0_and_g1`
- `test_pm_outputs_one_reasoned_main_blueprint`
- `test_pm_uses_adaptation_not_fixed_course_type_template`

- [ ] **Step 2: Run tests and confirm failure**

Run: `python3 -m unittest tests.test_course_skill_packages -v`

Expected: new tests FAIL because packages do not exist.

- [ ] **Step 3: Write `course-researcher` package**

The Skill must browse current authoritative sources, use primary sources for technical claims, perform representative tool use where required, write a structured record, and return `BLOCKED` when access or evidence is missing. It must translate findings into explicit design implications.

- [ ] **Step 4: Write the refactored `course-pm` package**

Remove ownership of intake, theme color selection and fixed course-type branching. Preserve useful outcome, capability progression, dependency, assessment and duration logic. Require one recommended architecture and cite G1 evidence IDs.

- [ ] **Step 5: Run package tests and Skill validation**

Run: `python3 -m unittest tests.test_course_skill_packages -v`

Expected: all Task 5–6 tests PASS.

Run:

```bash
python3 /Users/paichenwei/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-packages/course-run
python3 /Users/paichenwei/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-packages/course-researcher
python3 /Users/paichenwei/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-packages/course-pm
```

Expected: each command prints `Skill is valid!` and exits 0. Generate each `agents/openai.yaml` with `generate_openai_yaml.py`, using a one-sentence default prompt that explicitly names the corresponding `$skill-name`.

- [ ] **Step 6: Commit Task 6**

```bash
git add skill-packages/course-researcher skill-packages/course-pm tests/test_course_skill_packages.py
git commit -m "feat: add research and architecture skills"
```

### Task 7: 可回復安裝器與相容性保護

**Files:**
- Create: `scripts/install_course_skill_foundation.py`
- Create: `tests/test_install_course_skill_foundation.py`
- Create at runtime: `operations/course-skill-foundation/<timestamp>/manifest.json`
- Create at runtime: `operations/course-skill-foundation/<timestamp>/backups/`
- Create at runtime: `operations/course-skill-foundation/<timestamp>/rollback.py`

**Interfaces:**
- Consumes: validated packages for `course-run`, `course-researcher`, `course-pm`
- Produces: `install(packages_root: Path, skills_root: Path, operations_root: Path, apply: bool) -> InstallResult`
- Produces CLI flags: `--dry-run` default, `--apply`, `--skills-root`, `--operations-root`

- [ ] **Step 1: Write failing installer tests**

Add tests named:

- `test_dry_run_does_not_write_skill_root`
- `test_apply_backs_up_existing_skills_before_replace`
- `test_apply_installs_new_researcher_and_updates_existing_packages`
- `test_manifest_records_before_and_after_hashes`
- `test_rollback_refuses_when_installed_files_changed_after_install`
- `test_rollback_restores_exact_previous_bytes`

- [ ] **Step 2: Run installer tests and confirm failure**

Run: `python3 -m unittest tests.test_install_course_skill_foundation -v`

Expected: FAIL because installer does not exist.

- [ ] **Step 3: Implement dry-run, apply and rollback**

Use temporary sibling directories and `os.replace`; never delete a target before a verified backup exists. Rollback compares installed hashes before restoring. A new `course-researcher` target records that no prior version existed and rollback removes only that exact installed version.

- [ ] **Step 4: Run installer tests**

Run: `python3 -m unittest tests.test_install_course_skill_foundation -v`

Expected: all tests PASS.

- [ ] **Step 5: Run a real dry-run against `/Users/paichenwei/.agents/skills`**

Run: `python3 scripts/install_course_skill_foundation.py --dry-run --skills-root /Users/paichenwei/.agents/skills`

Expected: reports two updates and one addition, creates no files outside the workspace, and exits 0.

- [ ] **Step 6: Request the required filesystem approval and apply**

Run the same command with `--apply` only after sandbox approval. Expected: backup, manifest and rollback files are created in the workspace operations directory before the three global Skill targets change.

- [ ] **Step 7: Commit Task 7 source files and generated non-secret manifest**

```bash
git add scripts/install_course_skill_foundation.py tests/test_install_course_skill_foundation.py operations/course-skill-foundation
git commit -m "feat: install course skill foundation safely"
```

### Task 8: 垂直切片整合驗證

**Files:**
- Create: `tests/fixtures/course-contracts/g0-approved.json`
- Create: `tests/fixtures/course-research/valid-high-tool.json`
- Create: `tests/fixtures/course-research/blocked-no-hands-on.json`
- Create: `tests/test_course_foundation_flow.py`
- Create: `docs/course-skill-family-foundation.md`

**Interfaces:**
- Consumes: all prior tasks
- Produces: reproducible proof that G0 → G1 → G2 routing and invalidation work

- [ ] **Step 1: Write the failing vertical-flow tests**

Add tests named:

- `test_g0_must_be_approved_before_research_submission`
- `test_valid_high_tool_research_can_reach_g1_review`
- `test_missing_hands_on_keeps_g1_blocked`
- `test_g1_approval_allows_g2_submission`
- `test_g0_semantic_change_stales_g1_and_g2`
- `test_human_summary_preserves_full_requirement_text`

- [ ] **Step 2: Run the flow tests and confirm any integration gaps**

Run: `python3 -m unittest tests.test_course_foundation_flow -v`

Expected before fixture and integration completion: FAIL with missing fixture or routing assumptions.

- [ ] **Step 3: Add fixtures and close only integration gaps**

Use a fictional, non-production course. Do not create learner-facing lessons or modify existing courses. Keep each fixture small while covering high tool dependency, volatility, blocking and downstream invalidation.

- [ ] **Step 4: Document operator workflow**

Document exact commands for `init`, G0 submission and approval, research validation, G1 submission and approval, G2 handoff, status reading and semantic change. Link to the design spec rather than repeating its principles.

- [ ] **Step 5: Run the complete foundation suite**

Run:

```bash
python3 -m unittest \
  tests.test_course_contract \
  tests.test_course_contract_cli \
  tests.test_course_research \
  tests.test_course_skill_packages \
  tests.test_install_course_skill_foundation \
  tests.test_course_foundation_flow -v
```

Expected: all new tests PASS.

- [ ] **Step 6: Run existing course-manager regression tests**

Run: `python3 -m unittest discover -s tests -v`

Expected: all existing and new tests PASS; no PDF manager regression.

- [ ] **Step 7: Inspect scoped diff and verify unrelated files remain untouched**

Run: `git diff --check`

Run a path-scoped diff covering only files from this plan. Confirm no `_lessons/`, `_outlines/` or existing course HTML appears.

- [ ] **Step 8: Commit the vertical slice**

```bash
git add tests/fixtures tests/test_course_foundation_flow.py docs/course-skill-family-foundation.md
git commit -m "test: verify gated course foundation flow"
```

## Deferred Subsystems

After this foundation passes, write separate implementation plans for:

1. G3–G5 teaching content, learner-facing production, copy quality and unified validation.
2. G6 register／ops／refresh consolidation and existing-course repair integration.

Those plans must consume the interfaces established here rather than reopening the course contract or Gate model.
