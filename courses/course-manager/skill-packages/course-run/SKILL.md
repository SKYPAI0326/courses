---
name: course-run
description: Use when creating a new course from initial requirements through staged production, especially when several course capabilities need one contract, explicit approvals, evidence gates, or change control.
---

# Course Run

## Overview

Use one course contract to move a new course through G0–G6. Ask only questions that can change the design, preserve full teaching prose, and stop at every Gate until the user explicitly approves it.

Read [gate-routing.json](references/gate-routing.json) for deterministic authority and prerequisites. Read [course-contract-routing.md](references/course-contract-routing.md) for commands and child return fields.

## Start or Resume

1. Locate _design/{slug}/course-contract.json.
2. If absent, begin G0 with an adaptive interview covering learner, work context, observable result, duration, delivery, tools, permissions, known facts, assumptions, unknowns, and blockers. Do not repeat facts already supplied.
3. Create the contract with the CLI init command in the routing reference.
4. Run status; resume the first Gate that is not APPROVED.

A G0 draft may be saved with unknowns. Important unknowns prevent submission or approval.

## Gate Cycle

For the current Gate:

1. Confirm every prerequisite is APPROVED.
2. Dispatch the producer and require the structured return defined in the routing reference.
3. Keep detailed research, prose, media, and test records in external files. Put paths and SHA-256 evidence references in the contract.
4. If required information, material, permission, environment, hands-on execution, or evidence is missing, record the reason and set the Gate to BLOCKED. Preserve failed attempts as evidence.
5. When deliverables are ready, submit the Gate to REVIEW.
6. Show the user the actual deliverables, evidence, blockers, risks, open questions, and next action. Do not replace their prose with an abbreviated summary.
7. Only after an explicit user approval, call approve with the approver, timestamp, and approval note.

A producer may submit. No child capability may approve. Never infer approval from silence, previous approvals, or permission to continue a different action.

## G0 and Adaptation

G0 is a conversation, not a fixed questionnaire. Ask the smallest next question that changes the course architecture. G1 derives adaptation from learner gap, task nature, tool dependency, volatility, failure risk, and evidence type. Subject labels such as AI, marketing, or software do not select a fixed template.

## Change Control

For a semantic change, record the earliest affected Gate with change --semantic. Rework that Gate from DRAFT; treat every downstream STALE Gate as unusable until revalidated. Record typo or layout-only changes without --semantic and run the relevant technical regression.

## Boundaries

Use this Skill only for new courses. Route diagnosis or repair of an existing course to course-repair. Do not enter G4 batch production before the representative unit passes. Do not treat evidence maturity labels as Gate lifecycle states.
