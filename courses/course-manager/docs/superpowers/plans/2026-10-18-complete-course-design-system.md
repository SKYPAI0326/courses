# Complete Course Design System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將既有 G0–G2 基礎擴充為可自動調度、可驗證且能產出完整 learner-facing 網頁課程的 G0–G6 系統，並整併本機既有課程 Skills。

**Architecture:** `course-contract.json` 升級為 schema v2，Gate 依驗證證據自動轉為 `PASS`，外部發布授權獨立治理。所有核心與相容 Skill 以 `skill-packages/manifest.json` 作版本化來源，G3 內容、G4 試製、獨立 AI 試學、G5 全課及 G6 發布分別由小型 Python 驗證模組與 Skill 套件協作，最後以一門自包含課程完成端到端證明。

**Tech Stack:** Python 3 標準函式庫、`unittest`、JSON／JSON Schema、Markdown Skill 套件、HTML／CSS／JavaScript、既有 Skill 驗證腳本

**Spec:** `docs/superpowers/specs/2026-10-18-complete-course-design-system-design.md`

## Global Constraints

- Gate 固定為 `G0` 至 `G6`，生命週期固定為 `NOT_STARTED`、`IN_PROGRESS`、`PASS`、`FAIL`、`BLOCKED`、`STALE`。
- Gate 依證據自動通過；外部操作另用 `PUBLISH_APPROVAL_REQUIRED` 與授權紀錄治理。
- 只有缺少會改變設計的資訊、重要判斷、付費／權限／著作權問題或外部狀態變更時詢問使用者。
- G4 代表單元未通過前，不得開始 G5 批量製作。
- G4 與 G5 的試學者不得參與研究、規劃、撰寫、網頁製作或作者自驗，也不得取得內部規格與標準答案。
- 正常可讀正文不得被壓縮成名詞、欄位、片語、待辦或無前因後果的操作要求。
- 每門課可重新設計整體版型，但必須通過內容保真、導覽、響應式、無障礙、資產與操作驗證。
- 缺素材、權限、實測或完整示範時必須 `BLOCKED`；靜態檢查不能取代實際操作與獨立試學。
- 上游實質變更使受影響的下游 Gate 與證據成為 `STALE`，保留舊紀錄供追溯。
- 本計畫不修改現有 `_lessons/`、`_outlines/` 或正式課程 HTML，也不使用廣泛 staging。
- 不新增第三方 Python 相依套件。

## Review Focus

- v1 `APPROVED` 契約遷移時必須保留證據與核准歷史，不能因改名直接視為 v2 `PASS`；Task 1 測試。
- Gate 自動前進與發布授權必須完全分離，未授權外部操作永遠不可執行；Task 1、Task 7 測試。
- 內容欄位齊全但正文仍是待辦、內部編碼或斷裂片語時不得通過 G3；Task 3 測試。
- 製作者自行填寫試學紀錄、讀取作者資料或在 G4／G5 重用同一測試 context 時不得取得獨立驗證成熟度；Task 5、Task 6 測試。
- 本機 Skill 已在安裝後被使用者修改時，後續安裝與 rollback 必須停止且保留現況；Task 2、Task 9 測試。

---

### Task 1: 課程契約 v2、條件式 Gate 與外部授權

**Files:**
- Modify: `contracts/course-contract.schema.json`
- Modify: `src/course_contract.py`
- Modify: `src/course_research.py`
- Modify: `scripts/course_contract.py`
- Modify: `tests/test_course_contract.py`
- Modify: `tests/test_course_contract_cli.py`
- Modify: `tests/test_course_research.py`
- Modify: `tests/test_course_skill_packages.py`
- Modify: `skill-packages/course-researcher/SKILL.md`
- Modify: `skill-packages/course-researcher/references/research-policy.json`
- Modify: `skill-packages/course-pm/SKILL.md`
- Modify: `skill-packages/course-pm/references/architecture-policy.json`
- Create: `tests/fixtures/course-contracts/v1-approved-through-g2.json`

**Interfaces:**
- Produces: `GATE_STATUSES = frozenset({"NOT_STARTED", "IN_PROGRESS", "PASS", "FAIL", "BLOCKED", "STALE"})`
- Produces: `begin_gate(contract, gate_id, actor, at) -> None`
- Produces: `pass_gate(contract, gate_id, evidence_ids, validator_id, actor, at) -> None`
- Produces: `fail_gate(contract, gate_id, issues, actor, at) -> None`
- Preserves: `block_gate(...)`, `record_change(...)`, atomic load／save
- Produces: `propose_external_action(contract, action_id, kind, manifest_path, manifest_sha256, actor, at) -> None`
- Produces: `authorize_external_action(contract, action_id, approved_by, approved_at, note) -> None`
- Produces: `assert_external_action_authorized(contract, action_id, manifest_sha256) -> None`
- Produces: `migrate_contract_v1(contract, actor, at) -> dict[str, Any]`

- [ ] **Step 1: Write failing v2 lifecycle tests**

Add tests named:

- `test_new_contract_uses_v2_gate_states_and_external_action_sections`
- `test_pass_requires_all_previous_gates_passed_and_indexed_evidence`
- `test_pass_rejects_unresolved_blockers`
- `test_fail_preserves_issues_and_allows_restart`
- `test_semantic_change_sets_affected_gate_in_progress_and_downstream_stale`
- `test_external_authorization_is_separate_from_gate_pass`
- `test_authorization_rejects_changed_manifest_hash`
- `test_v1_approved_gate_with_complete_evidence_migrates_to_pass`
- `test_v1_approved_gate_without_complete_evidence_migrates_to_in_progress`
- `test_v1_migration_preserves_approval_history_and_revalidates_review_state`
- `test_research_routes_valid_evidence_directly_to_g1_pass`
- `test_pm_requires_g0_and_g1_pass`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_contract tests.test_course_contract_cli -v`

Expected: FAIL on v2 statuses, missing external actions and missing migration APIs.

- [ ] **Step 3: Implement schema v2 and migration**

Set `schema_version` to `2`; add `external_actions` and `maintenance`. Store gate validation events in evidence records, keep v1 `approved_by`／`approved_at` only inside migration history, and map v1 states exactly as the design specifies. Update G1 research routing and G2 package prerequisites to consume `PASS` instead of `APPROVED`.

- [ ] **Step 4: Replace submit／approve CLI flow**

Expose `begin`, `pass`, `fail`, `block`, `change`, `propose-action`, `authorize-action`, `check-action`, and `migrate`. Keep `approve` only as a v1 error message directing operators to `migrate`; do not silently reinterpret approval as passage.

- [ ] **Step 5: Run contract tests and verify GREEN**

Run: `python3 -m unittest tests.test_course_contract tests.test_course_contract_cli tests.test_course_research tests.test_course_skill_packages tests.test_course_foundation_flow -v`

Expected: all tests PASS after updating foundation-flow expectations to v2.

- [ ] **Step 6: Commit Task 1**

```bash
git add contracts/course-contract.schema.json src/course_contract.py src/course_research.py scripts/course_contract.py tests/test_course_contract.py tests/test_course_contract_cli.py tests/test_course_research.py tests/test_course_skill_packages.py tests/test_course_foundation_flow.py tests/fixtures/course-contracts/v1-approved-through-g2.json skill-packages/course-researcher skill-packages/course-pm
git commit -m "feat: automate course gate lifecycle"
```

### Task 2: 版本化完整 Skill 母群與通用安裝器

**Files:**
- Create: `skill-packages/manifest.json`
- Import: `skill-packages/{course-designer,build-course-page,course-validator,course-ops,course-refresh,course-repair,course-html-contract,course-copywriter,course-reviewer,course-register,course-handout-designer,course-typography-fixer,course-pdf}/`
- Modify: `scripts/install_course_skill_foundation.py`
- Modify: `tests/test_install_course_skill_foundation.py`
- Modify: `tests/test_course_skill_packages.py`

**Interfaces:**
- Produces: `load_package_manifest(path: Path) -> tuple[str, ...]`
- Changes: `install(..., package_names: Sequence[str] | None = None) -> InstallResult`
- Produces action types: `ADD`, `UPDATE`, `UNCHANGED`
- Preserves: verified backup, manifest hashes, transactional replace and self-contained rollback

- [ ] **Step 1: Write failing manifest and installer tests**

Add tests named:

- `test_manifest_lists_each_core_compatibility_and_optional_package_once`
- `test_every_manifest_package_is_self_contained_and_skill_valid`
- `test_installer_reads_manifest_instead_of_hardcoded_tuple`
- `test_identical_installed_package_is_unchanged_and_not_replaced`
- `test_changed_installed_package_requires_explicit_update_and_backup`
- `test_rollback_preserves_post_install_user_edits`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_install_course_skill_foundation tests.test_course_skill_packages -v`

Expected: FAIL because the manifest and imported package sources do not exist.

- [ ] **Step 3: Import exact installed baselines and record hashes**

Copy the listed `/Users/paichenwei/.agents/skills/<name>/` trees into matching `skill-packages/<name>/` directories without editing during the copy. Put role (`core`, `compatibility`, `optional`) and expected entrypoint in `manifest.json`; verify source and copied tree hashes match before later changes.

- [ ] **Step 4: Generalize the installer**

Read package names from the manifest, skip byte-identical targets, and require an explicit `--allow-update NAME` for an installed target whose current hash differs from the last known package baseline. Preserve the current transaction and rollback guarantees.

- [ ] **Step 5: Run package and installer tests**

Run: `python3 -m unittest tests.test_install_course_skill_foundation tests.test_course_skill_packages -v`

Expected: all Task 2 tests PASS.

- [ ] **Step 6: Commit Task 2**

```bash
git add skill-packages scripts/install_course_skill_foundation.py tests/test_install_course_skill_foundation.py tests/test_course_skill_packages.py
git commit -m "feat: version complete course skill family"
```

### Task 3: G3 可學習內容契約與文案能力整併

**Files:**
- Create: `contracts/course-lesson-record.schema.json`
- Create: `src/course_content.py`
- Create: `tests/test_course_content.py`
- Modify: `skill-packages/course-designer/SKILL.md`
- Create: `skill-packages/course-designer/references/learner-content-contract.json`
- Modify: `skill-packages/course-copywriter/SKILL.md`
- Modify: `skill-packages/course-handout-designer/SKILL.md`
- Modify: `skill-packages/course-validator/SKILL.md`

**Interfaces:**
- Produces: `ContentIssue(code: str, path: str, message: str, return_gate: str)`
- Produces: `validate_lesson_record(record: Mapping[str, Any]) -> list[ContentIssue]`
- Produces: `route_content_to_g3(contract, record, record_path, sha256, actor, at) -> str`
- Lesson record requires stable unit IDs, learner outcome, context, inputs, deliverable, explanation, full demonstration, guided practice, independent practice, checks, recovery, transfer and asset references.

- [ ] **Step 1: Write failing G3 tests**

Add tests named:

- `test_complete_lesson_record_can_pass_g3`
- `test_instruction_requires_purpose_start_action_and_expected_result`
- `test_demo_requires_input_reason_action_result_and_verification`
- `test_solo_task_requires_changed_context_and_real_deliverable`
- `test_missing_recovery_or_asset_reference_blocks_g3`
- `test_placeholder_internal_filename_and_checklist_prose_fail_editorial_gate`
- `test_readable_continuous_prose_is_not_rewritten_by_validator`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_content -v`

Expected: FAIL because the schema and module do not exist.

- [ ] **Step 3: Implement structural validation and G3 routing**

Validate deterministic omissions and forbidden placeholder markers without using word count, card count or sentence-shape heuristics as a quality score. Require a separate editorial evidence record for continuity and learner readability; preserve the original prose bytes.

- [ ] **Step 4: Consolidate authoring guidance**

Make `course-designer` the G3 author, move reusable content principles into its referenced contract, keep `course-copywriter` as a diagnostic editor only, and keep `course-handout-designer` as a method library. `course-validator` checks but never invents missing facts, examples or assets.

- [ ] **Step 5: Run G3 and package tests**

Run: `python3 -m unittest tests.test_course_content tests.test_course_skill_packages -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add contracts/course-lesson-record.schema.json src/course_content.py tests/test_course_content.py skill-packages/course-designer skill-packages/course-copywriter skill-packages/course-handout-designer skill-packages/course-validator
git commit -m "feat: enforce learner-readable course content"
```

### Task 4: G4 資產、課程專屬視覺與代表單元試製

**Files:**
- Create: `contracts/course-asset-manifest.schema.json`
- Create: `contracts/course-pilot-record.schema.json`
- Create: `src/course_production.py`
- Create: `tests/test_course_production.py`
- Modify: `skill-packages/build-course-page/SKILL.md`
- Create: `skill-packages/build-course-page/references/course-visual-decision.json`
- Modify: `skill-packages/course-html-contract/SKILL.md`

**Interfaces:**
- Produces: `ProductionIssue(code: str, path: str, message: str, return_gate: str)`
- Produces: `validate_asset_manifest(manifest: Mapping[str, Any]) -> list[ProductionIssue]`
- Produces: `select_pilot_unit(blueprint: Mapping[str, Any]) -> str`
- Produces: `validate_pilot_record(record, lesson_record, asset_manifest) -> list[ProductionIssue]`

- [ ] **Step 1: Write failing pilot tests**

Add tests named:

- `test_pilot_selector_chooses_highest_combined_risk_then_dependency`
- `test_asset_requires_purpose_source_rights_version_access_and_open_result`
- `test_visual_decision_uses_topic_learner_task_density_and_device`
- `test_pilot_requires_content_fidelity_and_real_render_evidence`
- `test_pilot_requires_mobile_tablet_desktop_core_path_results`
- `test_automated_accessibility_check_cannot_replace_manual_evaluation`
- `test_g5_cannot_begin_until_g4_passes`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_production -v`

Expected: FAIL because production contracts and APIs do not exist.

- [ ] **Step 3: Implement asset and pilot validation**

Use a deterministic risk tuple `(failure_cost, tool_uncertainty, asset_dependency, layout_complexity, downstream_dependency)` for pilot selection. Require content-hash comparison, browser render evidence, device results, keyboard／focus／sequence checks and learner-visible asset labels.

- [ ] **Step 4: Update page-building and HTML contracts**

Remove any assumption of a shared visual shell. Require one course-specific visual decision record while retaining common fidelity, navigation, responsive, accessibility and asset-discoverability invariants.

- [ ] **Step 5: Run G4 tests**

Run: `python3 -m unittest tests.test_course_production tests.test_course_skill_packages -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 4**

```bash
git add contracts/course-asset-manifest.schema.json contracts/course-pilot-record.schema.json src/course_production.py tests/test_course_production.py skill-packages/build-course-page skill-packages/course-html-contract
git commit -m "feat: validate representative course pilot"
```

### Task 5: 獨立 AI 試學證據與失敗回流

**Files:**
- Create: `contracts/course-trial-record.schema.json`
- Create: `src/course_validation.py`
- Create: `tests/test_course_validation.py`
- Modify: `skill-packages/course-validator/SKILL.md`
- Modify: `skill-packages/course-validator/references/evidence-format.md`
- Modify: `skill-packages/course-reviewer/SKILL.md`

**Interfaces:**
- Produces: `TrialIssue(code: str, path: str, message: str, return_gate: str)`
- Produces: `validate_trial_record(record: Mapping[str, Any], authors: Sequence[str], expected_scope: str) -> list[TrialIssue]`
- Produces: `route_trial_failure(issue_code: str) -> str`
- Produces: `evidence_maturity(record: Mapping[str, Any]) -> str`
- Produces: `route_verified_trial_to_gate(contract, gate_id, production_evidence_ids, trial_record, actor, at) -> str`
- Trial scope is exactly `representative_unit` for G4 or `full_course` for G5.

- [ ] **Step 1: Write failing trial tests**

Add tests named:

- `test_trial_actor_cannot_be_any_course_author_or_validator`
- `test_trial_rejects_author_notes_contract_or_answer_key_access`
- `test_trial_records_entry_actions_hints_blocks_recovery_artifact_and_result`
- `test_incomplete_or_unverifiable_artifact_fails_trial`
- `test_failure_code_routes_to_responsible_g1_through_g6_gate`
- `test_ai_trial_can_only_reach_independent_ai_verified`
- `test_human_verified_requires_explicit_human_participant_evidence`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_validation -v`

Expected: FAIL because trial validation does not exist.

- [ ] **Step 3: Implement trial validation and routing**

Require participant ID, isolated context ID, allowed learner-visible inputs, chronological actions, hint source, artifact hash and outcome. Route source/tool mismatch to G1, sequence/difficulty to G2, explanation/practice to G3, interface/assets to G4／G5, and access/deployment to G6. Only this composed production-plus-trial route may pass G4.

- [ ] **Step 4: Merge reviewer responsibility into validator**

Make `course-validator` the canonical content, fidelity, execution and trial verifier. Convert `course-reviewer` into a compatibility entry that dispatches to the validator without maintaining a second quality matrix.

- [ ] **Step 5: Run validation and package tests**

Run: `python3 -m unittest tests.test_course_validation tests.test_course_skill_packages -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 5**

```bash
git add contracts/course-trial-record.schema.json src/course_validation.py tests/test_course_validation.py skill-packages/course-validator skill-packages/course-reviewer
git commit -m "feat: require independent course trial evidence"
```

### Task 6: G5 全課整合與完整試學

**Files:**
- Create: `contracts/course-production-record.schema.json`
- Modify: `src/course_production.py`
- Modify: `src/course_validation.py`
- Modify: `tests/test_course_production.py`
- Modify: `tests/test_course_validation.py`
- Modify: `skill-packages/course-run/SKILL.md`
- Modify: `skill-packages/course-run/references/gate-routing.json`
- Modify: `skill-packages/course-run/references/course-contract-routing.md`

**Interfaces:**
- Produces: `validate_full_production(record, blueprint, lessons, assets, pilot, trial) -> list[ProductionIssue]`
- Produces: `route_full_production_to_g5(contract, record, evidence_refs, actor, at) -> str`
- Consumes: G4 `PASS`, G4 trial context ID and G5 full-course trial record

- [ ] **Step 1: Write failing full-course tests**

Add tests named:

- `test_full_production_requires_every_blueprint_unit_and_asset`
- `test_units_with_duplicate_outcomes_and_workflows_fail_integration`
- `test_navigation_and_cross_unit_dependencies_are_complete`
- `test_g5_trial_uses_new_isolated_context_and_full_course_scope`
- `test_g5_passes_only_after_final_artifact_matches_g0_acceptance`
- `test_course_run_auto_dispatches_passed_gate_without_user_approval`
- `test_course_run_asks_only_for_configured_decision_triggers`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_production tests.test_course_validation tests.test_course_skill_packages -v`

Expected: FAIL on missing full-production routing and old explicit-approval policy.

- [ ] **Step 3: Implement full-course validation**

Check blueprint coverage, distinct outcome／workflow fingerprints, dependency continuity, learner entry, navigation, all asset references, final artifact and a G5 trial context different from every author and the G4 trial context.

- [ ] **Step 4: Rewrite mother routing for conditional autonomy**

Set every Gate to automatic passage on validated evidence. Encode only five user-decision triggers: design-changing missing information, material judgment, paid service, credentials／rights, and external mutation. Preserve `BLOCKED` evidence and return paths.

- [ ] **Step 5: Run G5 and routing tests**

Run: `python3 -m unittest tests.test_course_production tests.test_course_validation tests.test_course_skill_packages -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 6**

```bash
git add contracts/course-production-record.schema.json src/course_production.py src/course_validation.py tests/test_course_production.py tests/test_course_validation.py skill-packages/course-run
git commit -m "feat: integrate full course production"
```

### Task 7: G6 發布授權、Ops／Register 整併與唯讀維護

**Files:**
- Create: `contracts/course-release-record.schema.json`
- Create: `src/course_release.py`
- Create: `scripts/course_release.py`
- Create: `tests/test_course_release.py`
- Modify: `skill-packages/course-ops/SKILL.md`
- Create: `skill-packages/course-ops/references/release-policy.json`
- Modify: `skill-packages/course-register/SKILL.md`
- Modify: `skill-packages/course-refresh/SKILL.md`

**Interfaces:**
- Produces: `ReleaseIssue(code: str, path: str, message: str)`
- Produces: `validate_release_record(record: Mapping[str, Any]) -> list[ReleaseIssue]`
- Produces: `build_release_proposal(course_root: Path, record: Mapping[str, Any]) -> dict[str, Any]`
- Produces: `apply_release_proposal(proposal_path: Path, contract_path: Path) -> None`
- Produces: `scan_course_freshness(course_root: Path, as_of: str) -> dict[str, Any]` and guarantees read-only behavior

- [ ] **Step 1: Write failing release tests**

Add tests named:

- `test_g6_pass_means_ready_not_published`
- `test_release_proposal_lists_exact_targets_hashes_backup_and_rollback`
- `test_apply_refuses_missing_mismatched_or_consumed_authorization`
- `test_apply_modifies_only_manifest_targets_and_records_result`
- `test_register_compatibility_entry_dispatches_to_course_ops`
- `test_refresh_scan_is_read_only_and_routes_stale_items_to_gate`
- `test_refresh_never_edits_metadata_or_republishes`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_release -v`

Expected: FAIL because G6 release contracts and APIs do not exist.

- [ ] **Step 3: Implement proposal, authorization check and scoped apply**

Build a deterministic manifest before authorization. On apply, verify manifest SHA-256, unconsumed approval, current target hashes, verified backups and exact target scope; record the result and consume the authorization atomically.

- [ ] **Step 4: Consolidate Ops, Register and Refresh**

Move registration, password, entry and index ownership into `course-ops`. Convert `course-register` to a compatibility entry. Remove all write instructions from `course-refresh`; its only output is a report with severity, affected Gate and recommended next action.

- [ ] **Step 5: Run G6 tests**

Run: `python3 -m unittest tests.test_course_release tests.test_course_skill_packages -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 7**

```bash
git add contracts/course-release-record.schema.json src/course_release.py scripts/course_release.py tests/test_course_release.py skill-packages/course-ops skill-packages/course-register skill-packages/course-refresh
git commit -m "feat: govern course release and maintenance"
```

### Task 8: 既有課程修復相容與系統文件

**Files:**
- Modify: `skill-packages/course-repair/SKILL.md`
- Create: `skill-packages/course-repair/references/new-system-routing.json`
- Create: `src/course_repair.py`
- Create: `tests/test_course_repair_compatibility.py`
- Modify: `docs/course-skill-family-foundation.md`
- Create: `docs/complete-course-design-system.md`

**Interfaces:**
- Produces: `RepairRoute(owner_gate: str, requires_new_course: bool, revalidation_scope: tuple[str, ...])`
- Produces: `classify_repair_finding(code: str, policy: Mapping[str, Any]) -> RepairRoute`
- Preserves: scan → plan → backup → fix → verify
- Requires: semantic reframing of learner／outcome／whole-course architecture routes to a new G0 contract

- [ ] **Step 1: Write failing repair compatibility tests**

Add tests named:

- `test_repair_keeps_existing_course_entry_separate_from_new_course_flow`
- `test_repair_requires_backup_before_first_mutation`
- `test_finding_routes_to_single_responsible_gate`
- `test_learner_outcome_or_whole_architecture_reframe_starts_new_contract`
- `test_repair_reuses_validator_without_claiming_new_course_gate_history`

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_course_repair_compatibility -v`

Expected: FAIL because the compatibility routing record does not exist.

- [ ] **Step 3: Update repair package and operator documentation**

Keep repair reversible and independent. Document the v2 CLI, G0–G6 evidence files, trial isolation, release authorization and maintenance commands without copying the design prose into the manual.

- [ ] **Step 4: Run repair and documentation checks**

Run: `python3 -m unittest tests.test_course_repair_compatibility tests.test_course_skill_packages -v`

Run: `git diff --check`

Expected: tests PASS and no whitespace errors.

- [ ] **Step 5: Commit Task 8**

```bash
git add skill-packages/course-repair src/course_repair.py tests/test_course_repair_compatibility.py docs/course-skill-family-foundation.md docs/complete-course-design-system.md
git commit -m "docs: integrate course repair with complete system"
```

### Task 9: 端到端證明課程與完整安裝

**Files:**
- Create: `proofs/campaign-performance-brief/course/`
- Create: `proofs/campaign-performance-brief/_design/campaign-performance-brief/course-contract.json`
- Create: `proofs/campaign-performance-brief/evidence/`
- Create: `proofs/campaign-performance-brief/trials/`
- Create: `tests/test_complete_course_flow.py`
- Modify: `scripts/install_course_skill_foundation.py`
- Modify: `tests/test_install_course_skill_foundation.py`

**Interfaces:**
- Proof course outcome: learner uses the bundled campaign CSV, calculates the defined metrics, and produces a verified `campaign-performance-brief.md` from the learner-visible web course.
- Consumes: all G0–G6 validators, package manifest, independent trial records and release proposal flow.
- Produces: reproducible `INDEPENDENT_AI_VERIFIED` evidence and G6 `PASS` with an unexecuted `PUBLISH_APPROVAL_REQUIRED` action.

- [ ] **Step 1: Write the failing end-to-end test**

Add `test_new_course_reaches_g6_ready_without_external_publish` asserting:

- the contract validates as schema v2;
- G0–G6 are `PASS` in order with indexed evidence;
- the G4 pilot and G5 full-course trials use different isolated AI context IDs;
- the final Markdown artifact passes its learner-visible rubric;
- G6 has a release proposal but no consumed authorization or external publication result.

- [ ] **Step 2: Run the test and verify RED**

Run: `python3 -m unittest tests.test_complete_course_flow -v`

Expected: FAIL because the proof package and evidence do not exist.

- [ ] **Step 3: Build the proof course through the actual G0–G6 interfaces**

Use current primary sources for metric definitions, record retrieval dates, build the complete content and assets, select the highest-risk unit, render and inspect the learner-facing HTML, and save every validator output in `evidence/`. Do not hand-edit Gate states.

- [ ] **Step 4: Run isolated G4 and G5 learner trials**

Give each fresh AI tester only the served learner entry, downloadable assets and learner-visible tools. The G4 tester completes the representative unit; a different context completes the full course and writes the final artifact. Save chronological records and artifacts under `trials/`; any failure returns to the responsible task before retrying.

- [ ] **Step 5: Run complete verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/install_course_skill_foundation.py --dry-run --skills-root /Users/paichenwei/.agents/skills
```

Run `quick_validate.py` for every package in `skill-packages/manifest.json`.

Expected: all tests PASS; every Skill prints `Skill is valid!`; dry-run reports exact `ADD`／`UPDATE`／`UNCHANGED` actions without writing outside the worktree.

- [ ] **Step 6: Apply the verified Skill installation**

Request filesystem approval, then run the installer with explicit `--allow-update` values for only changed packages. Verify installed tree hashes equal the manifest output and retain the generated backup, manifest and rollback script.

- [ ] **Step 7: Verify branch scope and main-worktree isolation**

Run `git diff --check`, `git status --short`, the complete test suite, and compare the main worktree status. Confirm no user-owned `gen-image` lesson or outline file was staged or modified by this branch.

- [ ] **Step 8: Commit Task 9**

```bash
git add proofs/campaign-performance-brief tests/test_complete_course_flow.py scripts/install_course_skill_foundation.py tests/test_install_course_skill_foundation.py operations/course-skill-foundation
git commit -m "test: prove complete course production flow"
```

## Final Verification

- [ ] Run `python3 -m unittest discover -s tests -v`; expected: zero failures and zero errors.
- [ ] Run every package through `quick_validate.py`; expected: all valid.
- [ ] Run `git diff --check main...HEAD`; expected: no output and exit 0.
- [ ] Inspect `git status --short --branch`; expected: clean `codex/course-skill-foundation` worktree.
- [ ] Inspect the installed Skill manifest and tree hashes; expected: exact match with package sources and a working rollback entrypoint.
- [ ] Confirm proof course maturity is exactly `INDEPENDENT_AI_VERIFIED`, not `HUMAN_VERIFIED`.
- [ ] Confirm no external publication occurred; release action remains `PUBLISH_APPROVAL_REQUIRED` until separate user authorization.
