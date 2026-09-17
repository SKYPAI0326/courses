# Repair Plan: digital-content-growth-126h

## Scope

- Slug: `digital-content-growth-126h`
- Pages: `index.html`, `module1.html`–`module6.html`, 40 CH/PRAC pages.
- Source of truth for sequence and hours: `_outlines/digital-content-growth-126h.md`.
- Repair boundary: learner-facing page structure, navigation, styles, and production-note separation. Existing teaching prose, examples, prompts, tables, links, and artifacts are preserved unless they are explicitly internal production notes.

## Risk

- Near-term class: unknown.
- Backup required: yes; completed at `_backup/2026-09-16-pre-repair/`.
- Restore script: `_tools/restore-2026-09-16-pre-repair.sh`.

## BLOCKER

### [LEARNER_PATH] Internal notes exposed in learner pages

- Files: `CH1-1.html`, `CH1-2.html`, `CH1-3.html`, `PRAC1.html`.
- Repair: archive the existing internal section in the repair record and exclude it from the learner-facing body.
- Verification: no learner HTML contains `講師授課筆記` or `不進講義`.

### [NAV_OPS] Course entry and module routes disagree

- Files: `index.html`, `module1.html`–`module6.html`, all unit pages.
- Repair: index lists six Parts; every module lists its own units; every unit uses the same course index, Part, previous, and next route contract.
- Verification: all local links resolve and a three-page sequence can be followed from the course index.

## MAJOR

### [TECH_LINT] Seven page-shell families

- Repair: introduce one course-local CSS shell and rebuild index/module/lesson wrappers from it.
- Verification: all learner pages reference the same shell stylesheet and have one shared topbar/footer/navigation vocabulary.

### [LEARNER_PATH] Mixed first section and section sequence

- Repair: add a common unit orientation block containing situation, starting material, finished artifact, first action, and next-use connection. Preserve existing lesson sections below it; do not invent new teaching operations.
- Verification: every unit begins with the same orientation contract and retains the existing body evidence.

### [TECH_LINT] Invalid and undefined color variables

- Repair: remove page-local color variables and use the course theme `#5a7a5a` plus neutral tokens.
- Verification: no `var(--)`, `rgba(,)`, or undefined `var(--a3)` remains; module card links use `color: inherit`.

### [CONTENT_THIN] Production status appears as learner content

- Repair: remove `單元頁已建立`, `資產「待課前確認」`, and `課程專屬導覽` from entry/module learner navigation. Replace with learner-facing purpose, hours, output, and prerequisites.
- Verification: production-status scan is empty in learner HTML.

## MINOR

### [TECH_LINT] Metadata debt

- Repair: add complete shared SEO/Twitter metadata during shell rebuild; retain canonical paths.
- Verification: rerun course lint and record remaining warnings separately from learner-path status.

## Target page contract

### Course index

Hero → course purpose/audience → capability chain → six Part cards → start route.

### Module landing

Part identity/hours → Part purpose → prerequisites and Part output → complete CH/PRAC list → previous/next Part.

### Learner unit

Hero → orientation contract → existing teaching body → learner-facing materials/fallback → previous/Part/next navigation.

### Practice unit

Use the same learner unit shell, with a visible `整合實作` label and the existing capstone evidence.

## Execution order

1. Read-only scan and backup.
2. Archive internal notes and create the shared course shell stylesheet.
3. Rebuild the course index and six module landings from the outline sequence.
4. Rebuild all learner-page wrappers while preserving teaching body content and asset links.
5. Run link, CSS, structure, and lint checks.
6. Run the learner-path reviewer and a cold structural read of index → module → unit.
7. Write `REPAIR-REPORT.md` with remaining content-level issues that need separate lesson editing.
