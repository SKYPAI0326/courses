# Dedup Repair Plan: office-ai

## Scope

- 11 pages: remove the section (06) `Together` replay of the fully completed section (03) case.
- Preserve every page's templates, changed-scenario `Solo`, independent pass criteria, and troubleshooting.
- 7 pages: remove the repeated course-level slogan; retain it only at CH1-1 and CH6-3.
- Do not change visual design, navigation, platform guidance, or unrelated lesson content.

## Planned merges and deletions

- Merge each main-case learning path into its first complete appearance in section (03); section (06) no longer recreates the same artifact.
- Delete only the repeated `Together` steps and their duplicate intermediate checkpoint.
- Rewrite the remaining section (06) as a concise transfer challenge with one observable independent completion standard.
- Delete seven verbatim copies of `帶著走的一句話`.

## Risk and rollback

- Near-term class: unknown.
- Backup required: yes.
- Backup: `courses/office-ai/_backup/2026-07-15-pre-dedup-repair/`.
- Restore: `courses/office-ai/_tools/restore-2026-07-15-pre-dedup-repair.sh`.

## Validation

1. Lint each 1-3 page batch.
2. Confirm section (06) has no same-case `Together` replay on the 11 target pages.
3. Confirm every target page retains a changed-material or changed-decision Solo and pass criterion.
4. Confirm full slogan remains only at CH1-1 and CH6-3.
5. Rebuild search index and sitemap; run whole-course lint.
