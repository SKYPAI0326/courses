# Fair Comparison Repair Report

## Changed

- `ch1/CH1-4.html`: meeting comparison now holds meeting facts constant and adds only output specifications.
- `ch1/CH1-4.html`: system-maintenance exercise now gives both prompts the same date, time, audience, and impact.
- `ch1/CH1-4.html`: expected output no longer invents work-completion or urgent-task policies.
- `ch1/CH1-4.html`: negative-constraint example now requests the same project report in both versions.
- `ch3/CH3-1.html`: weekly-report comparison now gives both versions the same work log.
- `ch3/CH3-1.html`: announcement comparison now gives both versions the same subject and audience.

## Reviewer recheck

- Controlled variable: PASS. Each repaired pair holds source facts and artifact constant.
- Named variable: PASS. The second prompt adds only format, audience treatment, decision criteria, or missing-value rules.
- Expected output grounding: PASS. The repaired maintenance notice contains no unsupported action or policy.

## Verification

- Target-page lint: BLOCKER 0, ERROR 0, WARN 0.
- Whole-course lint: 20 pages; BLOCKER 0, ERROR 0, WARN 0.
- Search index: rebuilt, 649 entries.
- Sitemap: rebuilt, 42 URLs.
- Restore script: syntax PASS.

## Restore

- Backup: `courses/office-ai/_backup/2026-07-15-pre-fair-comparison/`.
- Script: `courses/office-ai/_tools/restore-2026-07-15-pre-fair-comparison.sh`.
