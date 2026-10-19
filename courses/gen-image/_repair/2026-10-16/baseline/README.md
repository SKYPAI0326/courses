# Gen-image Repair Baseline

- Frozen at: 2026-10-16 (Asia/Taipei)
- Scope: 41 learner-facing HTML pages, 2 canonical outline/style-guide files, 13 lesson Markdown files.
- HTML snapshot: `../../../_backup/2026-10-16-pre-repair/course-html/`
- Outline snapshot: `../../../_backup/2026-10-16-pre-repair/outlines/`
- Lesson snapshot: `../../../_backup/2026-10-16-pre-repair/lessons/`
- Restore command: `sh _tools/restore-2026-10-16-pre-repair.sh`

## Machine Baseline

- `lint-page.py`: 41 pages scanned; BLOCKER 0; ERROR 0; WARN 26.
- `audit-course-substance.py`: 34 pages; machine checks passed; semantic review remained pending.
- Course files: 41 HTML pages and 62 existing PNG reference outputs.
- Footer dates: 2026-04-24 through 2026-05-01.

## Content Red Lights

- Missing learner downloads, including `10-industries-brief-library.md` and `prompt-templates.md`.
- Generator self-evaluation presented as the primary acceptance path.
- Rights guarantees such as `版權保險`, `版權乾淨`, and `無版權負擔`.
- PRAC3 instructs learners to source third-party advertising from IG, Pinterest, or e-commerce pages.
- Platform names, quotas, prices, and fixed generation times are tied to the April 2026 snapshot.

## Mixed-worktree Boundary

The repository already contained unrelated modified, deleted, and untracked files outside `courses/gen-image`. Repair work must remain scoped to this course plus its two canonical outline files and 13 lesson files. Never use `git add -A`.
