# Course contract routing

All commands run from courses/course-manager. The contract is the only lifecycle state source.

## Commands

~~~bash
python3 scripts/course_contract.py init --root COURSE_ROOT --slug SLUG --title TITLE --created-by NAME --at ISO8601
python3 scripts/course_contract.py enroll-approval-authority --contract CONTRACT --authority-id AUTHORITY --public-key PUBLIC_KEY_JSON --expected-revision 0
python3 scripts/course_contract.py status --contract CONTRACT
python3 scripts/course_contract.py validate --contract CONTRACT
python3 scripts/course_contract.py begin --contract CONTRACT --gate GATE --actor NAME --at ISO8601
python3 scripts/course_contract.py pass --contract CONTRACT --gate GATE --evidence-id ID --validator-id ID --actor NAME --at ISO8601
python3 scripts/course_contract.py fail --contract CONTRACT --gate GATE --issue TEXT --actor NAME --at ISO8601
python3 scripts/course_contract.py block --contract CONTRACT --gate GATE --reason REASON --actor NAME --at ISO8601
python3 scripts/course_contract.py change --contract CONTRACT --gate GATE --reason REASON --actor NAME --at ISO8601 --semantic
python3 scripts/course_contract.py propose-action --contract CONTRACT --action-id ID --kind KIND --manifest-path PATH --manifest-sha256 SHA256 --actor NAME --at ISO8601
python3 scripts/course_contract.py authorize-action --contract CONTRACT --action-id ID --receipt SIGNED_APPROVAL_RECEIPT_JSON --at ISO8601
python3 scripts/course_contract.py check-action --contract CONTRACT --action-id ID --manifest-sha256 SHA256
python3 scripts/course_contract.py migrate --contract CONTRACT --actor NAME --at ISO8601
~~~

Omit --semantic only when meaning, scope, outcomes, environment, assessment, and learner action remain unchanged.

## Producer returns

Every producer returns:

- gate_id and evidence result: ready for validation or BLOCKED
- deliverable references: relative path, SHA-256, source revision
- evidence references with maturity kept separate from Gate status
- blocking risks, other risks, and open questions
- one reasoned next action

Gate-specific returns:

| Gate | Producer capability | Required result |
|---|---|---|
| G0 | course-run adaptive interview | canonical requirements record with learner/baseline, work context, observable artifact, delivery/time, environment, constraints, criterion-level capabilities, assumptions, unknowns and decisions; every unresolved unknown requires a `VERIFIED_FALLBACK` support record conforming to `contracts/course-requirements-support.schema.json` plus at least one same-transition, hash-verified `requirements_support_artifact` |
| G1 | course-researcher | research record, evidence hash, adaptation, blockers, recommendation |
| G2 | course-pm | one reasoned blueprint with stable outcome/criterion/capability refs, executable units, dependency DAG, exact duration reconciliation and material risks |
| G3 | course-designer | one aggregate set of learner-readable lesson records that covers every canonical G2 unit exactly once, with examples, practice, checks, repair paths and asset needs |
| G4 | build-course-page plus validator | one representative complete unit and fidelity, follow-along, rendering and accessibility evidence |
| G5 | course-run coordinating producers | complete course, cross-unit consistency and production validation |
| G6 | course-ops plus validator | release, registration, access, index, deployment, rollback and maintenance evidence |

## Gate pass and external authorization

course-run records Gate PASS only after the declared validator succeeds against indexed evidence. Gate completion does not require user approval. Before publishing, deployment, registration, access changes, or another external mutation, present the exact action manifest and consequence, record explicit user authorization, and verify that its SHA-256 still matches immediately before execution.

Every PASS event freezes the full consumed evidence set with each reference's id, Gate, kind, path, and SHA-256. Later Gates replay those exact bindings and securely reread every bound file; missing, duplicate, extra, replaced-index, or changed-file evidence fails closed.

Immediately after `init`, an operator must explicitly run `enroll-approval-authority` to bind the externally governed verification public key. This is a trust-root governance step: course producers never generate, select, sign with, or automatically enroll this authority. Enrollment is single-use, revision-CAS guarded, and must happen before Gate work, actions, or receipts exist. `authorize-action` accepts only a signed external approval receipt bound to the exact contract/action basis.

After a validated Gate PASS, course-run begins the next Gate automatically. It asks the user only when the missing fact changes the design, a material judgment has genuinely different outcomes, a paid service is required, credentials or rights are required, or the next action mutates an external system. Ordinary production choices, evidence collection, validation failures, and reversible local repairs remain inside automatic orchestration.

## G5 full-production return

G5 uses `contracts/course-production-record.schema.json`. The return binds every blueprint unit to its reviewed lesson, learner page, assets, distinct outcome and workflow fingerprint; records exact navigation and artifact handoffs; and proves that the final artifact passes every G0 acceptance criterion. It embeds the `full_course` trial record and identifies the prior G4 trial context so the validator can reject context reuse.

Its `learning_coverage` matrix must cover every G0 child capability exactly once through G2 outcome/criterion/unit, G3 teaching/practice/assessment evidence, and G5 artifact/trial evidence. Duplicate, unknown, orphan, or parent-only coverage fails closed.

G3 and G5 replay the canonical bytes and hashes recorded by prior PASS events. Caller copies are convenience inputs only and must be byte-equivalent; a subset blueprint, missing lesson, extra lesson, duplicate owner, or relabelled workflow is rejected without changing the contract. Coverage evidence fields are stable IDs: G3 IDs must name atoms present in the lesson record, while G5 artifact and trial IDs must name an actual acceptance result and trial action.

The G5 PASS event cites both production evidence and the separately hashed independent trial evidence. A production validation flag without those indexed artifacts cannot pass the Gate.

## G4/G5 trial and accessibility evidence

Both Gates consume a separate `contracts/course-trial-record.schema.json` record. It binds the canonical G0 requirements SHA-256, target profile, baseline and prerequisites, allowed tools and learner-visible inputs, plus the governed runner authority. The held-out task records structured `changed_conditions` that alter data, threshold, or context enough to require a new judgment. Demonstration, guided-practice, answer-key, and held-out input/output hashes must all differ. Every in-scope G0 child capability and G2 criterion binds exactly one passing held-out action ID and the verified artifact; filenames, sequence-derived IDs, generic actions, or copied answers do not count.

An AI run can establish only `INDEPENDENT_AI_VERIFIED`. Its elapsed time cannot validate G0 duration, readability, or target-learner independence; `human_duration`, `human_readability`, and `target_learner_independence` remain `PENDING_HUMAN` until separate qualifying human evidence exists.

Accessibility is a separate, safely consumed file conforming to `contracts/course-accessibility-report.schema.json`. Pilot and production records declare its exact evidence ID, path, SHA-256, and claim scope. G4 coverage is the exact representative learner page and cannot be promoted to full-course coverage. G5 coverage is the exact course entry, every learner unit page, and completion page.

`basic_accessibility_smoke` covers only the declared keyboard, focus, reading-order, and overflow checks. `wcag_2_2_aa` requires every applicable WCAG 2.2 A/AA criterion, complete page coverage, recorded automated and manual results, and no unresolved HIGH, SERIOUS, or CRITICAL finding. A PASS label inside the report never substitutes for these records.
