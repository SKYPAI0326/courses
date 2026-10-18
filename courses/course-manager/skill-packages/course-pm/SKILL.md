---
name: course-pm
description: Use when approved G0 requirements and G1 research need to become one evidence-backed course blueprint with outcomes, assessment, progression, units, dependencies, and duration fit.
---

# Course PM

## Overview

Turn approved requirements and research into one reasoned G2 course blueprint. Use evidence and adaptation to decide the learning path; do not restart intake or choose presentation styling.

Read [architecture-policy.json](references/architecture-policy.json) for the deterministic contract and [architecture-output.md](references/architecture-output.md) for the blueprint structure.

## Input Gate

Begin only when G0 and G1 are APPROVED. Read G0_requirements, G1_research, and adaptation from the course contract. Treat stated learner, context, result, constraints, and research findings as inputs. Return BLOCKED when a missing decision or evidence makes architecture unsafe; send the gap to its owning Gate instead of interviewing from zero.

## Build the Blueprint

1. Define the final learner deliverable and observable acceptance criteria.
2. Identify the capabilities needed to produce it, including prerequisites and the progression from supported work to independent performance.
3. Align each outcome with teaching activity, practice, feedback, and assessment evidence.
4. Sequence units by dependency and authentic workflow. Each unit must add a capability, judgment, or transfer demand.
5. Allocate duration to actual learner activity, checks, recovery, and transitions; show that the total fits.
6. Apply learner gap, task nature, tool dependency, volatility, failure risk, and evidence type to teaching choices.
7. Cite G1 claim, hands-on, conflict, or unknown IDs for material architecture decisions.
8. State required materials, environments, unresolved risks, and what would block G3.

Produce one recommended architecture with its reasons. Do not generate alternatives merely to appear comprehensive. Course subject labels and legacy course_type values are metadata, not template switches.

## Return

Write the blueprint outside the course contract and return its relative path, SHA-256, source revision, evidence citations, risks, open questions, and a G2 recommendation of REVIEW or BLOCKED. Submit to course-run; this Skill cannot approve G2.
