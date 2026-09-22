# Technical Verification: office-ai

- actor: `tool-run`
- run date: `2026-09-22`

## Commands and results

- `python3 docs/lint-page.py courses/office-ai/ --summary --by-bucket`: 20 pages; 0 BLOCKER; 0 ERROR; 21 WARN.
- `python3 docs/audit-course-substance.py office-ai --build-evidence-manifest`: 19 lesson pages; 19 MACHINE_CHECKED; 0 missing assets.
- Local relative-link audit: 117 links; 0 broken.
- Gate audit: 20 / 20 HTML pages contain `_gate`.
- Source audit: 19 sources; one learner-content boundary pair per source.

Warnings are retained as migration debt and do not become a teaching PASS.
