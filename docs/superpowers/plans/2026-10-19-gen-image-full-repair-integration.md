# Gen Image Full Repair Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the verified 2026-10-16/17 `gen-image` repair candidate from the mixed source worktree into a clean branch based on current `origin/main`, refresh invalidated evidence, and stop at an exact G6 publication proposal.

**Architecture:** Treat the original mixed worktree as an immutable source snapshot and the managed worktree as the only integration target. Build a SHA-256 manifest before copying, preserve the current published state in an ignored backup with a tested restore script, transfer only allowlisted repair files, then validate the integrated learner-facing course before preparing a single-use release proposal.

**Tech Stack:** Git worktrees, HTML/CSS/SVG/PNG/PDF, Python standard-library validators, Playwright browser smoke tests, SHA-256 manifests.

**Spec:** `courses/gen-image/_repair/2026-10-16/REPAIR-PLAN.md`, `courses/gen-image/_repair/2026-10-17-image-refresh/IMAGE-REFRESH-PLAN.md`, `courses/gen-image/_repair/2026-10-17/STANDALONE-NAMING-REPAIR.md`

## Global Constraints

- Keep the original mixed worktree unchanged; it is a read-only source.
- Base all integration work on `origin/main` commit `6a7566fa098ccc68d00ac302f12029a470a18625`.
- Task scope is `content-change`, limited to already documented repair outputs and their evidence; do not invent new teaching content.
- Include the ignored but learner-linked `courses/gen-image/assets/downloads/skeleton-quick-card.pdf` explicitly.
- Exclude `_backup/`, `tmp/`, `.DS_Store`, and `從AI生圖到設計完稿_2小時課程大綱.docx` from the release candidate.
- Never use `git add -A`; stage only named files from the final integration manifest.
- Old validation hashes cannot be carried forward after integration; rebuild evidence from integrated files.
- Do not push without a new exact manifest SHA-256 authorization.

## Review Focus

- Mixed-worktree leakage: the target must contain only allowlisted repair outputs and required evidence.
- Learner asset completeness: every local `href` and `src` must resolve, including the ignored PDF.
- HTML contract preservation: every lesson section must remain inside the expected learner-content root with valid navigation order.
- Image migration integrity: all 59 legacy migration targets remain present while later v63/v64 assets do not invalidate the scoped verifier.
- Evidence freshness: content, fidelity, browser, and release evidence must reference the integrated file hashes rather than pre-integration hashes.

---

### Task 1: Freeze the integration source and rollback boundary

**Files:**
- Create: `courses/gen-image/_repair/2026-10-19-full-integration/INTEGRATION-MANIFEST.tsv`
- Create: `courses/gen-image/_repair/2026-10-19-full-integration/INTEGRATION-NOTES.md`
- Create: `courses/gen-image/_tools/restore-2026-10-19-pre-full-integration.sh`
- Create ignored backup: `courses/gen-image/_backup/2026-10-19-pre-full-integration/`

**Interfaces:**
- Consumes: current `origin/main`, the original mixed worktree, and the three repair specs.
- Produces: an allowlisted source/target/hash ledger and a proven restore path used by every later task.

- [ ] Record every included path, source SHA-256, target-before SHA-256 or `ABSENT`, and owning repair batch.
- [ ] Reject ignored/untracked files not explicitly allowed by the global constraints.
- [ ] Back up every existing target path before copying any repair file.
- [ ] Run `bash -n` on the restore script and prove restoration in a temporary directory by matching the recorded before hashes.

### Task 2: Transfer the documented course repair

**Files:**
- Modify: the 41 learner-facing HTML files currently reported by `git diff --name-only origin/main -- courses/gen-image/*.html`.
- Modify: `_lessons/gen-image/CH1-1.md` through the 13 modified lesson sources.
- Modify: `_outlines/gen-image.md` and `_outlines/gen-image.style-guide.md`.
- Create: the allowlisted files under `courses/gen-image/assets/downloads/`, `assets/reference-pack/`, `_repair/`, `_validation/`, `_workshop/`, `_tools/`, and `img/workshop2h/` recorded in the integration manifest.

**Interfaces:**
- Consumes: Task 1 manifest and backup.
- Produces: a clean-worktree reconstruction of the previously reviewed repair candidate.

- [ ] Copy only manifest-listed files from the original worktree.
- [ ] Recompute every copied SHA-256 and require equality with the source hash.
- [ ] Compare the resulting target path set with the integration manifest and report any missing or extra files.

### Task 3: Reconcile post-refresh SVG verification

**Files:**
- Modify: `courses/gen-image/_tools/verify-image-refresh.py`
- Modify: `courses/gen-image/_repair/2026-10-17-image-refresh/IMAGE-REFRESH-REPORT.md`
- Modify: `courses/gen-image/_repair/2026-10-19-full-integration/INTEGRATION-NOTES.md`

**Interfaces:**
- Consumes: the 59-row legacy replacement manifest and the already-published v63/v64 SVGs.
- Produces: a verifier that proves the legacy migration without treating legitimate post-migration versioned assets as manifest corruption.

- [ ] Preserve the checks for 59 unique legacy assets, zero legacy references, all manifest targets used, target existence, PNG dimensions, and local-reference validity.
- [ ] Change only the assertion that rejects additional later versioned assets; verify those assets through the general local-reference check.
- [ ] Run `python3 courses/gen-image/_tools/verify-image-refresh.py`; expected result is PASS for 59 legacy migration targets and zero legacy references.

### Task 4: Rebuild deterministic validation evidence

**Files:**
- Modify: `courses/gen-image/_validation/evidence.json`
- Modify: `courses/gen-image/_validation/validation-result.json`
- Modify: `courses/gen-image/_validation/L5-evidence-manifest.json`
- Modify: `courses/gen-image/_validation/FINAL-REPORT.md`
- Modify as produced: `search-index.json`, `sitemap.xml`

**Interfaces:**
- Consumes: integrated source, pages, assets, and repaired verifier.
- Produces: evidence bound to current hashes and current publication indexes.

- [ ] Run the course evidence builder and validator against the isolated worktree.
- [ ] Run structure validation on all 41 top-level course HTML pages plus the quick-card page.
- [ ] Run scoped lint and substance checks; separate backup/source-only HTML from learner-page results.
- [ ] Rebuild search index and sitemap, retaining only deterministic generated changes.
- [ ] Keep human/platform/independent-trial items PENDING where no new execution evidence exists.

### Task 5: Verify learner-facing behavior

**Files:**
- Create or update: `courses/gen-image/_validation/full-integration-browser-evidence.json`
- Modify: `courses/gen-image/_repair/2026-10-19-full-integration/INTEGRATION-NOTES.md`

**Interfaces:**
- Consumes: the integrated course candidate.
- Produces: current browser evidence for representative image-heavy, workflow, CH6, navigation, and downloadable-asset paths.

- [ ] Serve the isolated repository locally.
- [ ] Test representative pages at 390, 430, 820, and 1440 px with cleared localStorage.
- [ ] Assert no broken images, no unexpected page overflow, usable navigation, valid anchor behavior, and successful PDF/download responses.
- [ ] Record exact pages, dimensions, results, and any pre-existing exception without converting it into PASS.

### Task 6: Commit the isolated candidate and prepare G6 proposal

**Files:**
- Modify as required by pre-push generation: `search-index.json`, `sitemap.xml`.
- Create outside the repository: `/private/tmp/gen-image-full-repair-release-proposal.json`.

**Interfaces:**
- Consumes: Tasks 1–5 and their current hashes.
- Produces: reviewable commits plus an exact single-use publication proposal; no external publication.

- [ ] Review `git diff --check`, `git status --short`, and the manifest-to-diff path equality.
- [ ] Stage only manifest-listed paths and deterministic index files using explicit `git add -- <paths>` commands.
- [ ] Commit cohesive repair batches with their verification evidence.
- [ ] Run the repository pre-push checks without changing the remote.
- [ ] Generate a proposal containing exact targets, before/after SHA-256, remote before commit, rollback commands, and required technical/links/registration/access/rollback/maintenance evidence.
- [ ] Stop and request authorization bound to the new proposal SHA-256.
