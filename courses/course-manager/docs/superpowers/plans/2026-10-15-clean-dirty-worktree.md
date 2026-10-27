# Course Repository Dirty Worktree Cleanup Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Do not use subagents unless the user separately authorizes delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve every legitimate local change, isolate unrelated work, remove only verified residue, and return the `課程專用網頁` repository to a clean, auditable state without accidentally publishing other courses.

**Architecture:** Treat cleanup as a gated incident-recovery workflow: inventory first, classify every path, create recoverable evidence, then handle one ownership group at a time. No mutating Git command is allowed before the user approves the classification ledger and the proposed action for each path.

**Tech Stack:** Git CLI, repository-local validation scripts, GitHub remote metadata, Markdown evidence ledger.

**Spec:** Current chat request dated 2026-10-15: formulate a cleanup plan only; do not execute cleanup without separate authorization.

## Global Constraints

- Repository root is `/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁`; current branch observed during planning is `main`.
- This planning pass must not run `git add`, `git restore`, `git stash`, `git commit`, `git push`, `git clean`, `git reset`, or edit course files.
- During execution, never use `git add -A`, `git add .`, blanket `git restore .`, `git reset --hard`, or `git clean -fd`.
- Existing user changes are preserved unless their owner, purpose, and removal decision are explicitly confirmed.
- Deleted files are treated as high-risk until their references, build source, and intended deletion are verified.
- Staged, unstaged, untracked, ignored, and remote-divergence states must be reported separately.
- Each commit, if later authorized, contains one logical ownership group and uses explicit path staging.
- No push or deployment is included in cleanup authorization; either action requires a separate approval after verification.

## Review Focus

- A path under another course may belong to active work; expected behavior is preservation and isolation, never automatic rollback.
- A deleted PDF or report may be generated or authoritative; expected behavior is trace its source and references before deciding restore, regenerate, or accept deletion.
- A generated index or catalog can be legitimately stale; expected behavior is rebuild it only after source changes are settled, then verify the exact diff.
- A pre-existing staged change can silently enter the next commit; expected behavior is inspect `git diff --cached --name-status` before and after every staging action.
- Local `main` may differ from `origin/main`; expected behavior is inspect divergence before cleanup decisions and never pull, rebase, or push during inventory.

---

### Task 1: Freeze the mutation boundary and capture a read-only baseline

**Files:**
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/BASELINE.md`
- Do not modify: any existing tracked or untracked course file

**Interfaces:**
- Consumes: repository state at the start of the cleanup session
- Produces: immutable baseline containing repository root, branch, HEAD, upstream, divergence, and all worktree categories

- [ ] **Step 1: Confirm repository identity without changing state**

  Run from `courses/course-manager`:

  ```bash
  git rev-parse --show-toplevel
  git branch --show-current
  git rev-parse HEAD
  git remote -v
  git status --porcelain=v2 --branch
  ```

  Expected: repository root resolves to `課程專用網頁`; output is captured before any mutating command.

- [ ] **Step 2: Separate index, worktree, untracked, and ignored state**

  ```bash
  git diff --cached --name-status
  git diff --name-status
  git ls-files --others --exclude-standard
  git status --short --ignored
  ```

  Expected: no category is inferred from the ordinary short-status view alone.

- [ ] **Step 3: Record remote divergence without integrating it**

  ```bash
  git rev-list --left-right --count HEAD...@{upstream}
  git log --oneline --decorate -5
  ```

  Expected: the baseline states whether local HEAD is ahead, behind, or diverged. Do not run `fetch`, `pull`, `merge`, or `rebase` unless separately authorized.

- [ ] **Step 4: Stop Gate 1**

  Present the baseline to the user. Continue only after the user confirms that the inventory is complete enough to classify paths.

### Task 2: Build a path-by-path ownership and decision ledger

**Files:**
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/CLASSIFICATION.md`
- Read only: every changed path and its directly relevant references

**Interfaces:**
- Consumes: `BASELINE.md`
- Produces: one decision row for every changed, deleted, untracked, or unexpectedly ignored path

- [ ] **Step 1: Inspect actual diffs without editing files**

  ```bash
  git diff --stat
  git diff --cached --stat
  git diff --check
  git diff --summary
  ```

  For each path, inspect its focused diff with:

  Use the two-command form below only after copying one exact path from `BASELINE.md`; do not use globs or directory-wide guesses. For the previously observed management README, the concrete form is:

  ```bash
  git diff -- courses/course-manager/README.md
  git diff --cached -- courses/course-manager/README.md
  ```

  Expected: binary files, mode changes, renames, and deletions are explicitly identified.

- [ ] **Step 2: Assign every path exactly one ownership class**

  Use these exact classes in `CLASSIFICATION.md`:

  | Class | Meaning | Candidate action |
  |---|---|---|
  | `TARGET-COMPLETE` | Finished work intended for a scoped commit | Validate, explicitly stage, commit only after approval |
  | `ACTIVE-UNRELATED` | Legitimate unfinished work from another task/course | Preserve in place or path-scoped stash after approval |
  | `GENERATED-REBUILD` | Derived artifact whose source is known | Rebuild only after source state is settled |
  | `ACCIDENTAL-CHANGE` | Verified unintended modification | Restore only after backup and approval |
  | `INTENTIONAL-DELETE` | Deletion is confirmed and references are safe | Include only in its owning logical change |
  | `UNKNOWN-BLOCK` | Purpose or owner is not proven | Stop; no mutation allowed |

  Expected: ledger row count equals the complete changed-path count from Task 1.

- [ ] **Step 3: Trace deleted and generated files**

  For every deletion or generated artifact, search repository references and build scripts:

  For a previously observed deleted PDF, begin with the concrete filename and owning course, then repeat with each literal filename from the current baseline:

  ```bash
  rg -n --fixed-strings '全課程Prompt工具箱.pdf' .
  rg -n 'build|generate|pdf|catalog|sitemap|search-index' courses/digital-marketing-70h
  ```

  Expected: each deletion records its source, consumers, regeneration path, and recovery choice. A missing answer sets the class to `UNKNOWN-BLOCK`.

- [ ] **Step 4: Stop Gate 2**

  Present the complete ledger and proposed action per row. The user must approve or revise every action group before cleanup begins.

### Task 3: Create recovery evidence before any cleanup mutation

**Files:**
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/unstaged.patch`
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/staged.patch`
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/RECOVERY.md`
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/TARGET-COMPLETE.paths`
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/ACTIVE-UNRELATED.paths`
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/ACCIDENTAL-CHANGE.paths`
- Preserve separately: every approved untracked file group

**Interfaces:**
- Consumes: approved `CLASSIFICATION.md`
- Produces: tested recovery assets and an exact recovery procedure

- [ ] **Step 1: Create a dated recovery directory**

  ```bash
  mkdir -p /private/tmp/course-repo-cleanup-2026-10-15
  ```

- [ ] **Step 2: Export tracked changes including binary data**

  ```bash
  git diff --binary --output=/private/tmp/course-repo-cleanup-2026-10-15/unstaged.patch
  git diff --cached --binary --output=/private/tmp/course-repo-cleanup-2026-10-15/staged.patch
  git apply --check --reverse /private/tmp/course-repo-cleanup-2026-10-15/unstaged.patch
  ```

  Expected: patch files are non-ambiguous and the reverse check succeeds when the unstaged patch is non-empty. Record empty-patch cases explicitly.

- [ ] **Step 3: Preserve untracked files by approved ownership group**

  Copy only the exact untracked paths approved in Gate 2 into group-specific directories beneath `/private/tmp/course-repo-cleanup-2026-10-15/untracked/`. Record SHA-256 checksums and source paths in `RECOVERY.md`.

  Expected: source count, backup count, and checksum count match for every group. Do not copy ignored caches unless the ledger identifies them as required evidence.

- [ ] **Step 4: Stop Gate 3**

  Show recovery asset paths, counts, and validation results. No restore, stash, staging, or commit occurs until the user approves the recovery evidence.

### Task 4: Resolve one approved ownership group at a time

**Files:**
- Modify: only paths explicitly approved for the current ownership group
- Update during execution: `/private/tmp/course-repo-cleanup-2026-10-15/CLASSIFICATION.md`

**Interfaces:**
- Consumes: validated recovery assets and one approved action group
- Produces: one resolved group with all unrelated paths unchanged

- [ ] **Step 1: Handle `TARGET-COMPLETE` paths**

  Run the owning course's relevant lint, link, build, or artifact checks first. Copy the exact approved repository-relative paths, one per line, into `TARGET-COMPLETE.paths`; show that file to the user, then stage only that reviewed pathspec:

  ```bash
  git add --pathspec-from-file=/private/tmp/course-repo-cleanup-2026-10-15/TARGET-COMPLETE.paths
  git diff --cached --name-status
  git diff --cached --check
  ```

  Expected: cached path list exactly equals the approved group. Commit only after the user sees and accepts this list.

- [ ] **Step 2: Handle `ACTIVE-UNRELATED` paths**

  Preferred order:

  1. Leave them untouched if the immediate goal does not require a fully clean tree.
  2. If a clean `main` is required, use one named, path-scoped stash per ownership group after approval:

     Copy exactly one approved ownership group's repository-relative paths into `ACTIVE-UNRELATED.paths`, show it to the user, then run:

     ```bash
     git stash push -u -m 'wip: approved active-unrelated group before repository cleanup 2026-10-15' --pathspec-from-file=/private/tmp/course-repo-cleanup-2026-10-15/ACTIVE-UNRELATED.paths
     git stash show --stat stash@{0}
     ```

  3. Restore the stash only in the intended future task, preferably after creating its own branch or worktree.

  Expected: stash statistics match the approved group, and unrelated paths remain unchanged.

- [ ] **Step 3: Handle `ACCIDENTAL-CHANGE` paths**

  Verify every path exists in the recovery evidence. Copy only the approved repository-relative paths into `ACCIDENTAL-CHANGE.paths`, show it to the user, then run:

  ```bash
  git restore --pathspec-from-file=/private/tmp/course-repo-cleanup-2026-10-15/ACCIDENTAL-CHANGE.paths
  ```

  For a staged path, resolve index and worktree states separately; do not use a blanket reset.

  Expected: only the approved path changes status, and the path's intended HEAD content is confirmed.

- [ ] **Step 4: Handle `GENERATED-REBUILD` and `INTENTIONAL-DELETE` paths**

  Rebuild derived files from the authoritative source only after source changes are settled. For intentional deletions, confirm all references and package/index entries have been updated.

  Expected: regenerated or deleted outputs match their documented source and consumers; no orphan links remain.

- [ ] **Step 5: Verify after every group**

  ```bash
  git status --short
  git diff --name-status
  git diff --cached --name-status
  git diff --check
  ```

  Expected: the next group's baseline still matches the classification ledger. Stop immediately on drift.

### Task 5: Prove the final state and establish the prevention workflow

**Files:**
- Create during execution: `/private/tmp/course-repo-cleanup-2026-10-15/FINAL-REPORT.md`
- Modify only if separately approved: repository documentation or helper scripts for future preflight checks

**Interfaces:**
- Consumes: all resolved ownership groups
- Produces: reproducible evidence of a clean or intentionally bounded state and a future operating rule

- [ ] **Step 1: Run repository-level final checks**

  ```bash
  git status --porcelain=v2 --branch
  git diff --check
  git diff --cached --check
  git log --oneline --decorate -5
  ```

  Expected for a fully clean result: no ordinary path records in porcelain output and no staged diff. If the user chooses to keep active changes visible, `FINAL-REPORT.md` must list every remaining path and owner instead of claiming the tree is clean.

- [ ] **Step 2: Verify recovery handles remain usable**

  List patch, stash, branch, commit, and untracked-backup identifiers in `FINAL-REPORT.md`. Do not delete recovery assets during the same cleanup session.

- [ ] **Step 3: Adopt the future publishing preflight**

  Before every course publication:

  ```bash
  git rev-parse --show-toplevel
  git status --short --branch
  git diff --cached --name-status
  git diff --check
  ```

  Stage only named files, verify the staged list, run course-specific validation, commit one logical scope, then separately authorize push/deployment.

- [ ] **Step 4: Final user acceptance Gate**

  Present `FINAL-REPORT.md` with four explicit outcomes: preserved work, committed work, stashed/isolated work, and removed/regenerated residue. Cleanup is complete only when the user accepts those outcomes and the reported Git state.

## Execution Boundary

This document authorizes planning only. Starting Task 1 or creating `/private/tmp/course-repo-cleanup-2026-10-15/` evidence files requires a new, explicit instruction from the user. Any transition from read-only inspection to restore, stash, staging, commit, push, or deployment requires the corresponding Gate approval above.
