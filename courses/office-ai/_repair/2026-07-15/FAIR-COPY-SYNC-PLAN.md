# Fair Comparison Copy Sync Plan

## Root cause

The previous repair changed prompt pairs but did not trace dependent copy in the hero, scenario introduction, comparison explanation, takeaway, and practice instructions. The page therefore described missing facts that the repaired prompt already contained.

## Scope

- `ch1/CH1-4.html` only.
- Align the opening scenario with the meeting-notice comparison.
- Replace claims about missing time and location with the actual variable: tone, length, and structure.
- Align hero outcomes, keypoint, demo takeaway, and practice language with the fair-comparison rule.
- Preserve the existing `背景＋要求＋格式` framework while clarifying that facts control content and output specifications control presentation.

## Backup

- `courses/office-ai/_backup/2026-07-15-pre-fair-copy-sync/ch1/CH1-4.html`
- `courses/office-ai/_tools/restore-2026-07-15-pre-fair-copy-sync.sh`

## Verification

1. No copy claims the first meeting prompt lacks time, place, topic, audience, or preparation task.
2. The opening scenario and prompt pair describe the same meeting.
3. The demo explicitly compares identical facts with different output specifications.
4. Page lint and whole-course lint pass.
