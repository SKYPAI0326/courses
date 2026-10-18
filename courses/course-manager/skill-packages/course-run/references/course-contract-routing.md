# Course contract routing

All commands run from courses/course-manager. The contract is the only lifecycle state source.

## Commands

~~~bash
python3 scripts/course_contract.py init --root COURSE_ROOT --slug SLUG --title TITLE --created-by NAME --at ISO8601
python3 scripts/course_contract.py status --contract CONTRACT
python3 scripts/course_contract.py validate --contract CONTRACT
python3 scripts/course_contract.py begin --contract CONTRACT --gate GATE --actor NAME --at ISO8601
python3 scripts/course_contract.py pass --contract CONTRACT --gate GATE --evidence-id ID --validator-id ID --actor NAME --at ISO8601
python3 scripts/course_contract.py fail --contract CONTRACT --gate GATE --issue TEXT --actor NAME --at ISO8601
python3 scripts/course_contract.py block --contract CONTRACT --gate GATE --reason REASON --actor NAME --at ISO8601
python3 scripts/course_contract.py change --contract CONTRACT --gate GATE --reason REASON --actor NAME --at ISO8601 --semantic
python3 scripts/course_contract.py propose-action --contract CONTRACT --action-id ID --kind KIND --manifest-path PATH --manifest-sha256 SHA256 --actor NAME --at ISO8601
python3 scripts/course_contract.py authorize-action --contract CONTRACT --action-id ID --approved-by NAME --at ISO8601 --note NOTE
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
| G0 | course-run adaptive interview | learner, context, result, constraints, facts, assumptions, unknowns |
| G1 | course-researcher | research record, evidence hash, adaptation, blockers, recommendation |
| G2 | course-pm | one blueprint, outcomes, assessment, progression, units, dependencies, duration and material risks |
| G3 | course-designer | complete learner-readable lesson designs, examples, practice, checks, repair paths and asset needs |
| G4 | build-course-page plus validator | one representative complete unit and fidelity, follow-along, rendering and accessibility evidence |
| G5 | course-run coordinating producers | complete course, cross-unit consistency and production validation |
| G6 | course-ops plus validator | release, registration, access, index, deployment, rollback and maintenance evidence |

## Gate pass and external authorization

course-run records Gate PASS only after the declared validator succeeds against indexed evidence. Gate completion does not require user approval. Before publishing, deployment, registration, access changes, or another external mutation, present the exact action manifest and consequence, record explicit user authorization, and verify that its SHA-256 still matches immediately before execution.

After a validated Gate PASS, course-run begins the next Gate automatically. It asks the user only when the missing fact changes the design, a material judgment has genuinely different outcomes, a paid service is required, credentials or rights are required, or the next action mutates an external system. Ordinary production choices, evidence collection, validation failures, and reversible local repairs remain inside automatic orchestration.

## G5 full-production return

G5 uses `contracts/course-production-record.schema.json`. The return binds every blueprint unit to its reviewed lesson, learner page, assets, distinct outcome and workflow fingerprint; records exact navigation and artifact handoffs; and proves that the final artifact passes every G0 acceptance criterion. It embeds the `full_course` trial record and identifies the prior G4 trial context so the validator can reject context reuse.

The G5 PASS event cites both production evidence and the separately hashed independent trial evidence. A production validation flag without those indexed artifacts cannot pass the Gate.
