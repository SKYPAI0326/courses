# SDD ledger — plan: courses/office-ai/_repair/2026-10-16-growth-assistant/REPAIR-PLAN.md

Setup ruling: user explicitly approved implementation in the current `main` working tree; unrelated parent-repository changes are preserved and no commit or staging is performed.

Setup ruling: `sdd-workspace` cannot create `<repo>/.superpowers` because the managed workspace permits writes only under `courses/office-ai`; its `owns()` function is called under `if !`, so `set -e` does not stop the failed `mkdir` and the collision loop repeats. Use this plan-local ledger and repair directory instead. Cost if wrong: the standard task-start/task-done automation is unavailable, so commands and results must be recorded manually.

TDD ruling: the deliverables are learner-facing prose, copied assets and HTML content. The TDD reference says human prose earns no test; content receives reviewer issue checks, while HTML behavior receives lint, structure, link and browser tests. Cost if wrong: wording regressions rely on semantic review rather than an automated exact-text test.

Pre-flight Task 1 -> Task 2: Task 1 produces `assets/skills/{ta-core,ta-learning,ta-work}.md`; Task 2 consumes those exact paths in the lesson Asset Gate. Hashes match the supplied source files.

Pre-flight Task 2 -> Task 3: Task 2 produces the sole learner-content source for CH1-2, CH6-1 and CH6-3; Task 3 may render but not invent teaching facts.

Pre-flight Task 3 -> Task 4: Task 3 produces the final source/page/assets versions whose hashes and fidelity evidence Task 4 records.

Task 1: complete (no commit by user scope; tests: `sh -n` restore script, `cmp -s` three HTML backups, SHA-256 equality for three Skill assets -> pass)

Task 2: complete (official outline, new style guide and three lesson sources match reviewed staging byte-for-byte; author self-review BLOCKER 0 / MAJOR 0 / MINOR 0)

Task 3 ruling: CH1-1, CH1-3, CH5-3 and CH6-2 consume the changed unit titles through previous/next navigation. Keeping their stale labels would break learner continuity, so they are backed up and included only for exact navigation-label synchronization. Cost if wrong: four extra HTML files change; the restore script now covers each one.

Task 3: complete (three learner-facing pages rendered from the reviewed sources; index, adjacent navigation labels and after-class guide synchronized; all 20 public pages pass structure checks; 128 local references have 0 missing target; 9 responsive browser cases pass)

Task 4: complete within machine-verifiable scope (three changed units are `MACHINE_CHECKED`; full-course validator is `MACHINE_READY_PENDING_HUMAN` with 0 errors; the paid-account installation, connector and read-only notebook listing are verified; complete platform journeys, free-account 50-source path and human learning records remain pending)

Final review: no blocker or major issue found in the authorized change scope. Restore script syntax and 19 direct backup sources checked; shared search index preserves the 971 baseline non-office-ai records and changes only four office-ai records. PDF sync remains `PLAN_ONLY`: current PDFs are stale or unverified and were not modified. No commit or staging was performed.
