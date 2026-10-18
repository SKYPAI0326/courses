# Research evidence workflow

## Required input

Use the approved G0 section as the research brief. If G0 is not APPROVED, return BLOCKED without beginning architecture work.

## Evidence record

Write a JSON record conforming to contracts/course-research-record.schema.json. Stable IDs let G2 cite findings without copying the research report.

Each research question states the course decision it informs. Each claim cites source IDs. Each source records title, URL, type, retrieval date, version, and applicable context. A claim is useful only when at least one design implication uses it.

## Current external research

Browse for the current state of the subject. Prefer the authority that owns the rule, product, interface, standard, or dataset. Use secondary material when it adds practice context, user problems, or independent comparison. Record conflicts rather than selecting the convenient source.

No minimum source count exists. Stop when every material decision is supported, contradicted, or explicitly unknown.

## Representative tool execution

When adaptation.tool_dependency is high, use the intended account tier, locale, device, data constraints, and workflow where access permits. Record:

- stable hands-on ID and executed state
- tool, plan, version, locale, device, and relevant permissions
- representative input and expected deliverable
- actual result and evidence path
- failure notes and recovery attempts
- limitations and what was not tested

Missing access or execution makes the recommendation BLOCKED. A failed execution is retained as evidence; it cannot be rewritten into a successful conclusion.

## Adaptation and implications

Derive adaptation from learner gap, task nature, tool dependency, volatility, failure risk, and evidence type. Subject labels do not select a template.

Every design implication states a decision, its reason, and evidence_refs pointing to claim IDs or a hands-on ID. Preserve conflicts, unknowns, and non-conclusions even when they complicate the recommendation.

For high volatility, set an ISO review date and a named owner.

## Handoff

Return the record path, SHA-256, adaptation, blockers, and REVIEW or BLOCKED recommendation. course-run presents the package to the user and owns approval.
