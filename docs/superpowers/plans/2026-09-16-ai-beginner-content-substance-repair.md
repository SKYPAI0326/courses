# AI Beginner Course Content Substance Repair

日期：2026-09-16

## Goal

Repair the learner-facing substance of `courses/ai-beginner-practical`, with CH1-1 as the first priority, so a zero-background learner can see complete worked outputs before producing their own artifact.

## Design

- Preserve the existing platform-neutral scope, NotebookLM-only fixed platform rule for the course, page layout, navigation, links, and existing assets.
- Keep the dinner case as the main demonstration.
- Add a normal-path example bank for self-introduction, current-weather boundary, ETF explanation, and notice extraction. Each case includes input, complete output, judgement criteria, plausible wrong output, and repair instruction.
- Change the personal transfer from a blank-slate start to a guided starter with three prefilled conditions, then allow transfer to a personal task.
- Audit CH2-CH4 against the same evidence standard and make only targeted alignment edits.

## Evidence and verification

- Preserve CH1 atom IDs `CH1-A01` through `CH1-A10`.
- Back up exact target files before editing and provide an explicit restore script.
- Run diff whitespace checks, page lint, local-link checks, course contract tests, and a cold learner read.
- Report remaining external-bridge or real-platform limitations separately from local content results.

## Files

- `courses/ai-beginner-practical/CH1-1.html`
- `courses/ai-beginner-practical/CH1-1-LESSON-PLAN.md`
- `courses/ai-beginner-practical/COVERAGE-LEDGER.md`
- `courses/ai-beginner-practical/CH2-1.html` (分享預覽標題一致性)
- `courses/ai-beginner-practical/_repair/2026-09-16-content-substance/REPAIR-REPORT.md`

## Execution

This plan is executed inline under the user's approval of the repair design. No separate planning handoff is required.
