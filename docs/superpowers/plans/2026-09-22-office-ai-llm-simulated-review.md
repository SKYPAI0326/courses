# office-ai LLM Simulated Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 為 `office-ai` 建立一套兩階段 LLM 模擬學員檢視、可追溯 evidence 合併與人工優先分流流程，讓真人只需處理高風險項目，且不會把 LLM 結果誤報為真人通過。

**Architecture:** 先從 learner-facing HTML 與實際素材產生隔離的 context bundle；第一階段 LLM 對全部 19 單元模擬入口、跟做、理解與遷移；第二階段只挑戰疑點、平台頁、flagship 頁與 sequence。Python 工具只負責建立隔離輸入、驗證輸出、合併 `independent-ai` records 與產生 triage；LLM 本身不直接修改課程檔案。

**Tech Stack:** Python 3 standard library、既有 BeautifulSoup、JSON、SHA-256、Markdown；既有 `course-validator.sh` 與 `evidence.json` schema version 1。

**Spec:** `docs/superpowers/specs/2026-09-22-office-ai-llm-simulated-review-design.md`

## Global Constraints

- 只能使用 learner-facing HTML 的可見正文、頁面實際素材與必要的大綱標題；不得把作者備註、既有 review、validator report 或 source 內部區塊送入 simulated learner context。
- 所有 AI 結果使用 `actor: independent-ai` 與 `simulated_not_human: true`；不能建立或修改 `human` evidence。
- source、HTML、素材或 prompt revision 改變後，受影響的 AI log 必須重跑並更新 hash。
- LLM 無法判斷平台、登入、權限或素材可用性時寫 `PENDING`，不可推測 `PASS`。
- 不修改 `course-validator` 狀態語義；真人、平台與 sequence 未完成時仍維持 `MACHINE_READY_PENDING_HUMAN`。
- 本輪只覆蓋 `office-ai` 19 個單元，並保留既有 backup、author-self-check records 與 restore script。

---

### Task 1: 建立隔離的 learner context bundle

**Files:**
- Create: `courses/office-ai/_tools/build-ai-review-context.py`
- Create: `courses/office-ai/_validation/ai-simulated/context/manifest.json`
- Create: `courses/office-ai/_validation/ai-simulated/context/CH1-1.json` through `CH6-3.json`
- Test: `courses/office-ai/_tools/test-ai-review-context.py`

**Interfaces:**
- `build_context(page_path: Path, course_root: Path, project_root: Path) -> dict`
- `build_manifest(course_root: Path, project_root: Path) -> dict`
- Context fields: `schema_version`, `course`, `unit_id`, `title`, `course_type`, `page`, `page_sha256`, `visible_sections`, `assets`, `input_boundary`.
- Each asset entry contains `path`, `sha256`, `size`, `media_type`, and `text_content` only for UTF-8 text assets.

- [x] **Step 1: Write the failing checks**

  In `test-ai-review-context.py`, assert that the manifest contains exactly 19 units, every context has one page hash, and no serialized context contains `_review`, `_validation`, `_lessons`, `author-self-check`, `validator`, `learner-content:start`, or `learner-content:end`.

- [x] **Step 2: Run the checks and verify they fail before the builder exists**

  Run from `courses/`:

  ```bash
  python3 office-ai/_tools/test-ai-review-context.py
  ```

  Expected: failure because the context builder and manifest do not yet exist.

- [x] **Step 3: Implement the minimal context builder**

  Parse each `ch*/CH*.html` with BeautifulSoup. Keep the lesson hero and lesson body text, headings, ordered steps, tables, code blocks and learner-visible links. Remove `script`, `style`, `nav`, `footer`, `_gate` and all author/internal comments. Resolve only local asset links and include their current SHA-256; never read `_lessons`, `_review` or `_validation`.

- [x] **Step 4: Run the checks and inspect the manifest**

  ```bash
  python3 office-ai/_tools/build-ai-review-context.py office-ai
  python3 office-ai/_tools/test-ai-review-context.py
  ```

  Expected: 19 contexts, 19 page hashes, 0 internal-marker hits, and asset hashes matching the current page references.

- [x] **Step 5: Run existing deterministic checks**

  ```bash
  python3 docs/audit-course-substance.py office-ai --build-evidence-manifest
  python3 docs/lint-page.py courses/office-ai/ --summary --by-bucket
  ```

  Expected: 19 machine-checked lesson pages, 0 missing assets, 0 BLOCKER, 0 ERROR; existing warnings remain recorded as migration debt.

### Task 2: Add versioned prompt contracts and output schema

**Files:**
- Create: `courses/office-ai/_validation/ai-simulated/prompts/simulated-learner-v1.md`
- Create: `courses/office-ai/_validation/ai-simulated/prompts/adversarial-review-v1.md`
- Create: `courses/office-ai/_validation/ai-simulated/prompts/output-schema-v1.json`
- Create: `courses/office-ai/_validation/ai-simulated/README.md`
- Test: `courses/office-ai/_tools/test-ai-review-prompts.py`

**Interfaces:**
- `prompt_revision`: exact string `simulated-learner-v1` or `adversarial-review-v1`.
- Stage 1 log JSON fields: `unit_id`, `stage`, `actor`, `simulated_not_human`, `prompt_revision`, `model`, `input_context`, `artifacts`, `entry`, `completion`, `understanding`, `transfer`, `issues`, `limitations`.
- Stage 2 log JSON fields: `unit_ids`, `stage`, `actor`, `simulated_not_human`, `prompt_revision`, `model`, `input_context`, `artifacts`, `challenge_findings`, `verdict`, `limitations`.
- Each layer finding has `verdict`, `confidence` (`high|medium|low`), `citations` (page section or context line), `observations`, `risk`, and `repair_direction`.

- [x] **Step 1: Write prompt contract checks**

  Assert that both prompt files require the six entry questions, first action before judgment, observable result, completion artifact, recovery path, explicit `simulated_not_human: true`, and `PASS` evidence citations. Assert the adversarial prompt forbids reading author notes and requires disagreement escalation.

- [x] **Step 2: Run checks before prompt files exist**

  ```bash
  python3 office-ai/_tools/test-ai-review-prompts.py
  ```

  Expected: failure for missing prompt revisions.

- [x] **Step 3: Write the first-stage prompt**

  Require a novice office worker persona, no teacher assumptions, visible-page-only reasoning, one simulated first action, six entry answers, complete follow-along path, observable artifact, recovery, transfer judgment, confidence, citations, and explicit limitations. The prompt must return JSON matching `output-schema-v1.json`.

- [x] **Step 4: Write the second-stage prompt**

  Provide only the stage-1 conclusions plus the same learner context. Require an adversarial check for list-like prose, missing subjects/objects/conditions/results, hidden materials, repeated workflows, false platform claims and unsupported PASS verdicts. Conflicting findings must become `PENDING` for human triage.

- [x] **Step 5: Run prompt checks**

  ```bash
  python3 office-ai/_tools/test-ai-review-prompts.py
  python3 -m json.tool office-ai/_validation/ai-simulated/prompts/output-schema-v1.json >/dev/null
  ```

  Expected: PASS and valid JSON.

### Task 3: Execute stage-1 simulated learner review for all units

**Files:**
- Create: `courses/office-ai/_validation/ai-simulated/stage1/CH1-1.json` through `CH6-3.json`
- Create: `courses/office-ai/_validation/ai-simulated/stage1/RUN-REPORT.md`
- Create: `courses/office-ai/_tools/validate-ai-review-output.py`
- Test: `courses/office-ai/_tools/test-ai-review-output.py`

**Interfaces:**
- `validate_log(log_path: Path, context_path: Path, stage: str) -> list[str]`
- `load_artifacts(log: dict) -> list[dict]`
- Stage-1 output is one JSON log per unit with four layer findings: `entry`, `completion`, `understanding`, `transfer`.
- Every AI log artifact must equal the current context manifest page/asset path and hash; the merger later adds the existing formal source hash without exposing that source to the simulated learner.

- [x] **Step 1: Add output validation checks**

  Validate actor, stage, prompt revision, simulated flag, unit id, four layer findings, allowed verdicts, confidence values, non-empty citations for PASS, non-empty observations for FAIL/PENDING, and exact current artifact hashes.

- [x] **Step 2: Run validator against a deliberately incomplete fixture**

  Create a temporary JSON fixture missing `simulated_not_human` and one citation, then run:

  ```bash
  python3 office-ai/_tools/validate-ai-review-output.py --stage stage1 --file /private/tmp/office-ai-invalid-ai-review.json
  ```

  Expected: non-zero exit with both missing-field errors.

- [x] **Step 3: Execute stage 1 using the prompt contract**

  For each context JSON, run the LLM with `simulated-learner-v1`; save the returned JSON without editorial rewriting. Set `model` to the actual model identifier, set `input_context` to the context path and prompt revision, and keep all limitations. Do not read or include `_lessons` or author review logs in the model input.

- [x] **Step 4: Validate all 19 logs**

  ```bash
  python3 office-ai/_tools/validate-ai-review-output.py --stage stage1 --dir office-ai/_validation/ai-simulated/stage1
  python3 office-ai/_tools/test-ai-review-output.py --stage stage1
  ```

  Expected: 19 valid logs, no stale hashes, and a report listing every unit's four verdicts and confidence values.

- [x] **Step 5: Record the stage-1 run manifest**

  `RUN-REPORT.md` must include run date, model, prompt revision, context manifest hash, unit count, verdict counts, limitations, and the exact command used for deterministic validation.

### Task 4: Run stage-2 adversarial review on the selected scope

**Files:**
- Create: `courses/office-ai/_tools/select-ai-review-scope.py`
- Test: `courses/office-ai/_tools/test-ai-review-scope.py`
- Create: `courses/office-ai/_validation/ai-simulated/stage2/scope.json`
- Create: `courses/office-ai/_validation/ai-simulated/stage2/*.json`
- Create: `courses/office-ai/_validation/ai-simulated/stage2/RUN-REPORT.md`
- Modify: `courses/office-ai/_tools/validate-ai-review-output.py`
- Test: `courses/office-ai/_tools/test-ai-review-output.py`

**Interfaces:**
- `select_adversarial_scope(stage1_dir: Path, outline_path: Path, required_platform_units: set[str]) -> dict`
- Stage-2 scope contains `unit_ids`, `reasons`, `source_stage1_hashes`, and `prompt_revision`.
- Stage-2 log contains `challenge_findings`, `verdict`, `conflicts_with_stage1`, and artifact hashes.

- [x] **Step 1: Implement deterministic scope selection**

  Select any unit with a BLOCKER or MAJOR finding, `CH1-2`, `CH5-1`, outline-marked flagship units (`CH2-3`, `CH3-1`, `CH3-2`), low confidence, missing completion artifact, or membership in the configured three-unit sequence `CH1-1 -> CH1-2 -> CH1-3`.

- [x] **Step 2: Verify scope selection with a fixture**

  Feed two stage-1 fixture logs: one low-confidence unit and one clean unit. Assert the low-confidence unit is selected and the clean unit is selected only when it is a platform/flagship/sequence unit.

- [x] **Step 3: Execute stage 2 for the selected units**

  Run the LLM with `adversarial-review-v1`, giving it the same learner context and stage-1 conclusions but not author source/review data. Save one JSON log per selected unit or sequence; conflicting PASS/FAIL results become `PENDING` with `conflicts_with_stage1: true`.

- [x] **Step 4: Validate stage-2 logs and scope coverage**

  ```bash
  python3 office-ai/_tools/validate-ai-review-output.py --stage stage2 --dir office-ai/_validation/ai-simulated/stage2
  python3 office-ai/_tools/test-ai-review-output.py --stage stage2
  ```

  Expected: every selected scope item has one valid adversarial log and every log references current artifacts.

### Task 5: Merge AI evidence and build the human triage report

**Files:**
- Create: `courses/office-ai/_tools/merge-ai-review-evidence.py`
- Create: `courses/office-ai/_validation/ai-simulated/AI-TRIAGE-REPORT.md`
- Modify: `courses/office-ai/_validation/evidence.json`
- Test: `courses/office-ai/_tools/test-ai-evidence-merge.py`

**Interfaces:**
- `build_records(stage1_dir: Path, stage2_dir: Path, context_manifest: Path) -> list[dict]`
- `merge_records(evidence: dict, new_records: list[dict]) -> dict`
- `build_triage(records: list[dict], stage1_dir: Path, stage2_dir: Path) -> str`
- Existing author/tool records remain unchanged. A later `independent-ai` record with the same layer and unit ids supersedes an earlier AI record, while both logs remain on disk.

- [x] **Step 1: Write merge tests using a copy of current evidence**

  Assert that merging adds only `independent-ai` records, preserves all 39 existing records byte-for-byte in their fields, rejects `actor: human`, rejects stale hashes, and keeps the latest same-layer AI record as the active one.

- [x] **Step 2: Run merge tests before the merger exists**

  ```bash
  python3 office-ai/_tools/test-ai-evidence-merge.py
  ```

  Expected: failure because the merge functions are not defined.

- [x] **Step 3: Implement record construction**

  Convert each validated stage-1 finding into one record per layer (`entry`, `completion`, `understanding`, `transfer`) with `actor: independent-ai`, `simulated_not_human: true`, log hash, source/page/asset artifacts, model, prompt revision, method and limitations. Convert stage-2 findings into `content`, `fidelity`, `platform` or `sequence` records as applicable.

- [x] **Step 4: Implement triage ordering**

  Sort findings by BLOCKER, MAJOR, platform/permission, sequence, low confidence, then PASS. Include unit, layer, verdict, confidence, citations, observed risk, repair direction, stage-1/stage-2 disagreement and the exact human action required.

- [x] **Step 5: Run the merger in dry-run mode**

  ```bash
  python3 office-ai/_tools/merge-ai-review-evidence.py office-ai --dry-run
  ```

  Expected: print record counts and triage counts without modifying `evidence.json`.

- [x] **Step 6: Merge and validate**

  ```bash
  python3 office-ai/_tools/merge-ai-review-evidence.py office-ai
  python3 -m json.tool office-ai/_validation/evidence.json >/dev/null
  bash /Users/paichenwei/.agents/skills/course-validator/scripts/course-validator.sh office-ai all
  ```

  Expected: validator errors remain 0; status remains `MACHINE_READY_PENDING_HUMAN`; AI records are visible but no human status is upgraded.

### Task 6: Verify the complete workflow and publish the handoff

**Files:**
- Modify: `courses/office-ai/_validation/FINAL-REPORT.md`
- Modify: `courses/office-ai/_repair/2026-09-22/REPAIR-REPORT.md`
- Modify: `courses/office-ai/_validation/HUMAN-VALIDATION-CHECKLIST.md`
- Create: `courses/office-ai/_validation/ai-simulated/FINAL-RUN-REPORT.md`

**Interfaces:**
- Final report references context manifest, prompt revisions, stage-1 report, stage-2 scope/report, triage report and merged evidence.
- Human checklist receives the ordered list of pages to inspect and the reason each page was selected.

- [x] **Step 1: Run the full deterministic check suite**

  ```bash
  python3 office-ai/_tools/test-ai-review-context.py
  python3 office-ai/_tools/test-ai-review-prompts.py
  python3 office-ai/_tools/test-ai-review-output.py --stage stage1
  python3 office-ai/_tools/test-ai-review-output.py --stage stage2
  python3 office-ai/_tools/test-ai-evidence-merge.py
  python3 docs/lint-page.py courses/office-ai/ --summary --by-bucket
  python3 docs/audit-course-substance.py office-ai --build-evidence-manifest
  bash /Users/paichenwei/.agents/skills/course-validator/scripts/course-validator.sh office-ai status
  ```

  Expected: all workflow tests pass, lint remains 0 BLOCKER/ERROR, assets remain complete, and validator remains `MACHINE_READY_PENDING_HUMAN` with no errors.

- [x] **Step 2: Check stale-artifact protection**

  Modify one temporary context hash, run the output validator, and assert it rejects the log. Restore the temporary fixture and confirm the real manifest is unchanged.

- [x] **Step 3: Check no human overclaim**

  Search the merged evidence and reports for `actor: human`, `HUMAN_READY`, `LEARNER_READ`, or `PLATFORM_VERIFIED` introduced by the AI workflow. The only allowed occurrences are limitations or pending-state explanations.

- [x] **Step 4: Write the final handoff**

  `FINAL-RUN-REPORT.md` records the model and prompt revisions, 19-unit coverage, selected adversarial scope, verdict counts, stale-hash test, validator result, top human priorities and explicit limitations.

- [x] **Step 5: Offer execution mode**

  After the plan is reviewed, execute either with `superpowers:subagent-driven-development` (fresh worker per task and review gates) or `superpowers:executing-plans` (inline checkpoints). Do not mix the two modes during one run.
