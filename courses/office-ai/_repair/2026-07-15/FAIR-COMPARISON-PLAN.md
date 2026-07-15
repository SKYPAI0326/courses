# Fair Comparison Repair Plan

## Scope

- `ch1/CH1-4.html`: two unfair vague/clear comparisons, one reversed task pair, and one expected output that invents actions.
- `ch3/CH3-1.html`: two summary comparison cards that change both source facts and control rules.

## Repair rule

- Every A/B pair uses identical source facts and the same requested artifact.
- The second prompt may add only the variable named by the lesson: audience, format, length, decision criteria, or missing-value policy.
- Expected output may not introduce actions, policies, dates, or contacts absent from the shared facts.

## Backup

- `courses/office-ai/_backup/2026-07-15-pre-fair-comparison/`
- `courses/office-ai/_tools/restore-2026-07-15-pre-fair-comparison.sh`

## Validation

1. Confirm both prompts in each pair contain the same facts.
2. Confirm both prompts request the same artifact.
3. Confirm expected outputs contain no unsupported operational instruction.
4. Run page lint and whole-course lint.
