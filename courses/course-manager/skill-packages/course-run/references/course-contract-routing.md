# Course contract routing

All commands run from courses/course-manager. The contract is the only lifecycle state source.

## Commands

~~~bash
python3 scripts/course_contract.py init --root COURSE_ROOT --slug SLUG --title TITLE --created-by NAME --at ISO8601
python3 scripts/course_contract.py status --contract CONTRACT
python3 scripts/course_contract.py validate --contract CONTRACT
python3 scripts/course_contract.py submit --contract CONTRACT --gate GATE --actor NAME --at ISO8601
python3 scripts/course_contract.py approve --contract CONTRACT --gate GATE --approved-by NAME --at ISO8601 --note NOTE
python3 scripts/course_contract.py block --contract CONTRACT --gate GATE --reason REASON --actor NAME --at ISO8601
python3 scripts/course_contract.py change --contract CONTRACT --gate GATE --reason REASON --actor NAME --at ISO8601 --semantic
~~~

Omit --semantic only when meaning, scope, outcomes, environment, assessment, and learner action remain unchanged.

## Producer returns

Every producer returns:

- gate_id and recommended status: REVIEW or BLOCKED
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

## Approval handoff

Before requesting approval, present links to actual deliverables and evidence. State blockers, risks, unknowns, and the exact downstream consequence. Approval is valid only when the user responds to that Gate's presented result; record the approval note verbatim enough to preserve its meaning.
