---
name: course-researcher
description: Use when a passed new-course requirement contract needs current external evidence, real-work analysis, tool verification, or adaptation decisions before course architecture begins.
---

# Course Researcher

## Overview

Turn a passed G0 into decision-ready G1 evidence. Research is complete when the course decisions are supported and important unknowns are visible; source volume and polished prose are not completion signals.

Read [research-policy.json](references/research-policy.json) for deterministic requirements and [research-evidence.md](references/research-evidence.md) for the evidence workflow.

## Input Gate

Start only when G0 is PASS and G1 is IN_PROGRESS. Read learner, work context, observable result, constraints, assumptions, unknowns, and available permissions from the contract. Do not repeat the intake interview.

## Research

1. Turn uncertain design decisions into research questions and state what each answer will change.
2. Browse current authoritative sources. For technical claims, prefer primary official documentation. Record retrieval date, version, applicable context, and confidence.
3. Examine real tasks, deliverables, common failures, environment limits, and recovery needs.
4. When tool dependency is high, use the actual target tool to complete a representative task. Record environment, input, result, failure notes, and limitations. A failed run remains evidence and keeps G1 BLOCKED.
5. Preserve conflicting evidence, unknowns, and conclusions the evidence cannot support.
6. Convert findings into adaptation and explicit design implications. Every implication cites a claim or hands-on record ID.

## Return

Write the structured research record outside the course contract, validate it with the shared research validator, and return:

- research record relative path and SHA-256
- adaptation across all applicable dimensions
- blockers, risks, unknowns, and non-conclusions
- validation result and evidence needed for course-run to record G1 PASS, or a BLOCKED reason
- one reasoned next action

Return evidence to course-run. This Skill does not set Gate state; course-run validates the record and records PASS or BLOCKED.
