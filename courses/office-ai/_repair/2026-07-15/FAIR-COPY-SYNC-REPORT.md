# Fair Comparison Copy Sync Report

## Root cause

The prior repair replaced the prompt cards but did not update all downstream copy that interpreted those cards. Old claims about missing time and location therefore remained after both prompts had been given those facts.

## Changed

- Updated metadata, hero copy, learning outcome, scenario heading, scenario introduction, comparison explanation, keypoint, and demo takeaway.
- Clarified the teaching distinction: facts determine content; output specifications determine tone, length, and structure.
- Aligned the opening scenario with the quarterly-meeting prompt pair.
- Explicitly introduced system maintenance as a separate practice case instead of referring to it as the section (01) case.
- Retained the original `背景＋要求＋格式` framework and learner steps.

## Verification

- Removed stale claims that the first prompt lacks time or location.
- Removed stale `模糊指令／清楚指令` comparison wording from the page.
- Confirmed both meeting prompts share the same facts.
- Confirmed both maintenance prompts share the same facts.
- Target-page lint: BLOCKER 0, ERROR 0, WARN 0.
- Whole-course lint: 20 pages; BLOCKER 0, ERROR 0, WARN 0.
- Search index: rebuilt, 649 entries.
- Sitemap: rebuilt, 42 URLs.
- Restore script syntax: PASS.

## Restore

- Backup: `courses/office-ai/_backup/2026-07-15-pre-fair-copy-sync/`.
- Script: `courses/office-ai/_tools/restore-2026-07-15-pre-fair-copy-sync.sh`.
