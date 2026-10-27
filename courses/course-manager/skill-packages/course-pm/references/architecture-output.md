# G2 architecture output

The blueprint is a durable design document for G3 authors, not a list of labels.

## Decision narrative

Open with the learner's working situation, the result they must produce, the evidence that shaped the architecture, and why this path fits the available duration and constraints. Keep the reasoning readable enough for a course author to act on without reconstructing the research.

## Required sections

### Outcomes and assessment

For each outcome, define a stable outcome ID and one or more stable criterion IDs. Each criterion binds exactly one G0 acceptance criterion and child capability, with observable assessment evidence and the part of the final deliverable it supports. Split multi-clause outcomes; a parent outcome cannot stand in for unassessed child capabilities.

### Capability progression

Show prerequisites and the progression from explanation or demonstration through guided use to independent performance. Identify where learners must make a decision, recover from error, or transfer the method.

### Unit architecture

For each unit include:

- learning problem and workplace use
- new capability or judgment
- stable outcome, criterion and child-capability IDs
- required inputs and materials
- teaching activity, practice, feedback, and assessment
- learner output and completion check
- prerequisite units and downstream consumers
- duration with a practical reason
- G1 evidence IDs that justify material choices

### Duration fit

Account for instruction, learner action, checks, recovery, breaks when applicable, and transitions. If the promised result does not fit, reduce scope or return BLOCKED; do not hide the gap by shortening every activity.

Record positive unit minutes plus explicit break and buffer minutes. Their sum must equal G0 `available_minutes`; dependencies form an acyclic graph and may reference only known units.

### Materials and risks

List required data, accounts, permissions, examples, answer keys, environments, accessibility needs, and fallback paths. Link each material risk to its owning Gate and effect on G3.

## Handoff

Return one main blueprint. Include evidence citations, relative path, SHA-256, source revision, risks, open questions, and the validation result needed for course-run to record PASS or BLOCKED. Theme, visual system, and page layout belong to later production decisions.
