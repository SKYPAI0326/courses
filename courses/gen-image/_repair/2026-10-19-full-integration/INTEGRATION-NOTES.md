# gen-image full repair integration notes

- Date: 2026-10-19
- Task scope: `content-change` limited to the documented 2026-10-16/17 repair candidate.
- Source: original mixed worktree, read-only during integration.
- Target baseline: `origin/main` at `6a7566fa098ccc68d00ac302f12029a470a18625`.
- Source manifest: 194 files; 56 target files existed and were backed up, 138 targets were absent.
- Included exception: ignored learner-linked `assets/downloads/skeleton-quick-card.pdf`.
- Excluded: `_backup/`, `tmp/`, `.DS_Store`, and `從AI生圖到設計完稿_2小時課程大綱.docx`.
- Baseline checks: docs tests 11/11 passed; course lint scanned 42 pages with 0 BLOCKER, 0 ERROR, 26 WARN.
- Release boundary: integration and validation may proceed; no push without a new manifest-bound authorization.

## Rulings

- Preserve the already-published v63/v64 SVG baseline and do not overwrite it from the mixed source.
- Treat the 59-row image manifest as the legacy replacement scope; later versioned assets require existence and local-reference validation but do not become fake legacy rows.
- Rebuild evidence hashes after transfer; previous `MACHINE_READY_PENDING_HUMAN` remains historical evidence only until validation completes.
- The editable workshop poster source used a forbidden CSS gradient and blocked the repository commit hook. Its overlay was changed to a solid translucent color; the learner-facing PNG remains unchanged.

## Progress

- Task 1: source inventory and before-state backup created.
- Restore script syntax: PASS.
- Restore proof: PASS in `/private/tmp/gen-image-restore-proof-mfvagxxw`; 56 existing targets matched their before SHA-256 and 138 simulated integration-only targets were removed.
- Task 2: all 194 manifest paths transferred and committed in `690dea9d`; 193 remain byte-identical to the source snapshot and one source-only poster background received the documented lint fix.
- Task 3: the image-refresh verifier now treats later versioned assets as valid when their local targets exist, without weakening the closed 59-row legacy migration checks.
