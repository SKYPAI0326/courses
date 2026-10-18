# Course Design System Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將已完成的 G0–G6 課程設計系統強化成證據可重播、Gate 不可繞過、可從獨立儲存庫安裝並能可靠續跑的 Contract v3 系統。

**Architecture:** 真實檔案先經 root-bound 路徑與 SHA-256 驗證，再交給 Gate 專用 validator；只有中央 dispatcher 能提交 PASS。Contract mutation 使用 revision、鎖與 CAS，發布授權綁定 contract revision 與 G6 證據，release 使用單次消耗狀態與 durable journal。G0、G2、學習成果、試走及無障礙補強沿用原 G0–G6，不新增平行流程。

**Tech Stack:** Python 3 標準函式庫、`unittest`、JSON Schema、Markdown Skill packages、GitHub Actions

**Spec:** `docs/superpowers/specs/2026-10-18-complete-course-design-system-design.md`

## Global Constraints

- 不修改 `courses` 上架專案、既有 `_lessons/`、`_outlines/` 或正式課程 HTML。
- 不新增第三方 Python 相依套件；跨平台鎖若無法可靠提供，必須清楚宣告支援平台並 fail closed。
- Gate PASS 必須能由實體檔案、正確 Gate、專用 validator、可重算雜湊及可重播輸入證明。
- 未參與製作的 AI 身分由受治理角色名冊與隔離執行紀錄判定，不能只信任 caller 自填字串。
- AI 試走只證明 `INDEPENDENT_AI_VERIFIED`；時數、真人理解與真人遷移仍保持 `PENDING_HUMAN`。
- 版型與呈現由系統依課程主題、任務與學員情境決定；共用品質驗證，不強制共用視覺模板。
- 所有行為變更先寫失敗測試並確認 RED，再寫最小實作、確認 GREEN。
- mixed worktree 僅顯式 staging；不得 `git add -A`，不得推送或發布。

## Review Focus

- 只有 evidence ID、錯 Gate、錯 hash、缺檔、symlink escape 都必須拒絕 PASS。
- BLOCKED 必須可用有證據的 resolution 解開，但不能因 resolution 自動 PASS。
- 任一授權後 contract mutation 都必須使舊授權不可執行。
- 兩個並行 mutation／release apply 不能同時成功，也不能遺失更新。
- clean clone 不得依賴 `/Users/paichenwei`、舊 `courses/course-manager` 目錄或預先安裝的本機 validator。

---

### Task 1: Contract v3 evidence integrity

**Files:**
- Create: `contracts/course-evidence-reference.schema.json`
- Create: `src/course_evidence.py`
- Modify: `contracts/course-contract.schema.json`
- Modify: `src/course_contract.py`
- Test: `tests/test_course_evidence.py`
- Test: `tests/test_course_contract.py`

**Interfaces:**
- Produces: `register_evidence_file(workspace_root, *, evidence_id, gate_id, kind, relative_path, maturity=None, metadata=None) -> dict`
- Produces: `materialize_json_evidence(workspace_root, *, evidence_id, gate_id, kind, relative_path, value, maturity=None, metadata=None) -> dict`
- Produces: `verify_evidence_reference(workspace_root, reference, *, expected_gate=None) -> list[EvidenceIssue]`
- Contract v3 adds integer `revision` and typed evidence references.

- [ ] Write tests for missing file, wrong hash, wrong Gate, duplicate ID, absolute/traversal path and symlink escape.
- [ ] Run focused tests and confirm the new tests fail for the intended reasons.
- [ ] Implement canonical evidence materialization, file registration and root-bound verification.
- [ ] Upgrade schema/runtime validation and v2→v3 migration; unverifiable prior PASS becomes `STALE` from the earliest affected Gate.
- [ ] Run focused and contract regression tests; commit only Task 1 files.

### Task 2: Gate-specific transitions, G4/G5 evidence and independent identity

**Files:**
- Create: `src/course_gate.py`
- Modify: `src/course_validation.py`
- Modify: `src/course_production.py`
- Modify: `scripts/course_contract.py`
- Modify: `contracts/course-pilot-record.schema.json`
- Test: `tests/test_course_gate.py`
- Test: `tests/test_course_validation.py`
- Test: `tests/test_course_production.py`

**Interfaces:**
- Produces: `validate_and_transition_gate(contract, gate_id, evidence_ids, workspace_root, actor, at) -> str`
- Internal only: `_commit_gate_pass(...)`
- G4/G5 routes register actual trial/production files and consume governed production-role rosters.

- [ ] Write tests proving generic ID-only PASS, self-declared G5 PASS and author-as-trial-participant are rejected.
- [ ] Confirm RED, then remove public CLI raw `pass` and route all PASS through the Gate registry.
- [ ] Make G4/G5 evidence paths real and hash-verifiable; require complete production validation in G5 routing.
- [ ] Re-run all Gate, trial and production tests; commit only Task 2 files.

### Task 3: Blocker resolution and contract transactions

**Files:**
- Create: `src/transactions.py`
- Modify: `src/course_contract.py`
- Modify: `scripts/course_contract.py`
- Test: `tests/test_transactions.py`
- Test: `tests/test_course_contract.py`
- Test: `tests/test_course_contract_cli.py`

**Interfaces:**
- Produces: `resolve_gate_blocker(contract, gate_id, blocker_id, resolution, evidence_ids, actor, at) -> None`
- Produces: `mutate_contract_atomic(path, operation, *, expected_revision=None, lock_timeout=10.0) -> dict`

- [ ] Write tests for unresolved restart rejection, auditable resolution, wrong/reused blocker IDs and stale snapshot conflicts.
- [ ] Confirm RED, then add stable blocker IDs, explicit resolution and CLI `resolve-blocker`.
- [ ] Replace load→mutate→save with locked revision/CAS transactions; every successful mutation increments revision exactly once.
- [ ] Run concurrency and CLI regression tests; commit only Task 3 files.

### Task 4: Authorization and crash-safe release transaction

**Files:**
- Modify: `contracts/course-contract.schema.json`
- Create: `contracts/course-release-proposal.schema.json`
- Modify: `src/course_contract.py`
- Modify: `src/course_release.py`
- Modify: `scripts/course_release.py`
- Test: `tests/test_course_release.py`

**Interfaces:**
- Action lifecycle: `PUBLISH_APPROVAL_REQUIRED → AUTHORIZED → EXECUTING → CONSUMED | FAILED | INVALIDATED`
- Produces: `recover_release_proposal(proposal_path, contract_path) -> None`

- [ ] Write tests for mutation-after-authorization, concurrent apply, crash after each target and single-use recovery.
- [ ] Confirm RED; bind authorization to contract revision, G6 source revision and approval-basis hash.
- [ ] Implement release-root lock, durable per-step journal, CAS target checks and deterministic recovery/rollback.
- [ ] Run release and contract tests; commit only Task 4 files.

### Task 5: Executable G0/G2 and learning-outcome coverage

**Files:**
- Create: `contracts/course-requirements-record.schema.json`
- Create: `contracts/course-blueprint-record.schema.json`
- Create: `src/course_requirements.py`
- Create: `src/course_architecture.py`
- Modify: `contracts/course-lesson-record.schema.json`
- Modify: `contracts/course-production-record.schema.json`
- Modify: `src/course_content.py`
- Modify: `src/course_production.py`
- Test: `tests/test_course_requirements.py`
- Test: `tests/test_course_architecture.py`
- Test: `tests/test_course_content.py`
- Test: `tests/test_course_production.py`

**Interfaces:**
- Produces canonical G0/G2 validators and route handlers registered by `course_gate`.
- Stable IDs connect G0 criterion → G2 outcome/unit → G3 lesson → G5 artifact/trial evidence.

- [ ] Write tests for empty/incomplete G0/G2, material unknowns, orphan outcomes, missing assessment/practice/feedback and duration mismatch.
- [ ] Confirm RED; implement G0/G2 schemas, semantic validators and DAG/coverage checks.
- [ ] Add stable outcome/criterion references through lesson and production records; reject uncovered child capabilities.
- [ ] Run G0–G5 regression tests; commit only Task 5 files.

### Task 6: Trial transfer validity and accessibility evidence

**Files:**
- Modify: `contracts/course-trial-record.schema.json`
- Modify: `contracts/course-pilot-record.schema.json`
- Modify: `contracts/course-production-record.schema.json`
- Modify: `src/course_validation.py`
- Modify: `src/course_production.py`
- Test: `tests/test_course_validation.py`
- Test: `tests/test_course_production.py`

**Interfaces:**
- Trial binds `requirements_sha256`, `target_profile_id`, held-out task conditions and criterion-level evidence.
- Accessibility evidence records exact page coverage, claim scope, report path/hash, automated/manual checks and unresolved findings.

- [ ] Write tests for profile/hash mismatch, false entry readiness, generic actions, reused answers/data, missing changed conditions and incomplete criterion coverage.
- [ ] Write tests for missing accessibility file/hash, automated-only conformance, incomplete G5 page coverage and unresolved serious findings.
- [ ] Confirm RED; implement minimal schema and semantic validation without equating AI trial with human readiness.
- [ ] Run trial/production regressions; commit only Task 6 files.

### Task 7: Standalone runtime, installer hygiene and executable orchestration

**Files:**
- Create: `src/runtime.py`
- Create: `src/course_orchestrator.py`
- Create: `scripts/course_run.py`
- Modify: `manager.py`
- Modify: `scripts/install_course_skill_foundation.py`
- Modify: active `skill-packages/**` path references
- Modify: `skill-packages/course-run/references/gate-routing.json`
- Modify: `skill-packages/course-run/references/course-contract-routing.md`
- Modify: `.gitignore`
- Test: `tests/test_runtime.py`
- Test: `tests/test_course_orchestrator.py`
- Test: `tests/test_install_course_skill_foundation.py`
- Test: `tests/test_course_skill_packages.py`

**Interfaces:**
- Resolves `COURSE_DESIGN_SYSTEM_ROOT`, `COURSE_WEB_ROOT`, `SKILLS_ROOT`, `COURSE_DESIGN_STATE_ROOT` without personal fallbacks.
- CLI `course_run.py resume|complete` emits one idempotent dispatch envelope and stops only for governed decisions/external actions.

- [ ] Write tests from arbitrary cwd/repo name and clean HOME; prove fixed paths and local quick-validator dependency fail.
- [ ] Confirm RED; implement root resolution and replace active personal/legacy paths with variables or fail-closed options.
- [ ] Move generated operations/registry/report state outside the repo; correct installer update commands and role metadata.
- [ ] Implement resumable orchestrator behavior and replace JSON-only auto-dispatch tests with executable tests.
- [ ] Run installer, skill, runtime and orchestration tests; commit only Task 7 files.

### Task 8: Proof rebuild, CI and final independent verification

**Files:**
- Modify: `proofs/campaign-performance-brief/build_proof.py`
- Modify: proof contract/evidence/trial files generated by the builder
- Modify: `docs/complete-course-design-system.md`
- Modify: `docs/course-skill-family-foundation.md`
- Modify: `README.md`
- Create: `pyproject.toml`
- Create: `VERSION`
- Create: `.github/workflows/verify.yml`
- Test: `tests/test_complete_course_flow.py`

**Interfaces:**
- Fresh proof has every evidence path present, every hash matching, all Gate-specific validators passing and external release still unauthorized.

- [ ] Write/extend end-to-end tests so the current proof fails on missing evidence, answer reuse and incomplete coverage.
- [ ] Rebuild the proof through the v3 routes; keep truthful `INDEPENDENT_AI_VERIFIED` versus `PENDING_HUMAN` labels.
- [ ] Add clean-clone CI for supported Python versions, full tests, compile, portable path scan, package install/verify and proof replay.
- [ ] Run all tests, package validation, proof replay and a clean-clone install; run independent whole-branch review.
- [ ] Commit only the verified hardening files; do not push without a separate user request.
