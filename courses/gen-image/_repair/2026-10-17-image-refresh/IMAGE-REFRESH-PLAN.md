# Course Visual Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all legacy course images with versioned 2026-10 course-owned visuals while preserving lesson meaning and HTML structure.

**Architecture:** Build a one-to-one asset manifest, generate deterministic SVGs for diagrams and fresh raster assets for photographic or illustrative examples, then update only contextual `img src` attributes. Validate each batch before continuing and finish with a fresh independent review.

**Tech Stack:** HTML, SVG, PNG, built-in image generation, shell reference checks, Python HTML structure validators, browser smoke tests.

**Spec:** `_repair/2026-10-17-image-refresh/IMAGE-REFRESH-DESIGN.md`

## Global Constraints

- `task_scope = content-change`; image assets and matching `src` paths are primary. A fresh-review finding may also change only the adjacent prose, alt text, caption, or prompt label required to make the lesson truthful and safe.
- Do not overwrite files under `img/`.
- New assets live under `assets/course-visuals/2026-10/`.
- Preserve DOM wrappers, navigation, scripts, and lesson order. Keep visible text and `alt` unchanged by default; record any reviewer-required semantic alignment in the final review log.
- Do not commit or push without explicit user authorization.

## Review Focus

1. Semantic mismatch between replacement and surrounding lesson claim.
2. Generated text, logo, watermark, trademark, or recognizable brand leakage.
3. NG examples accidentally becoming acceptable examples or vice versa.
4. Image dimensions or aspect ratio causing mobile overflow or unusable comparison grids.
5. A legacy `img/` reference surviving in a less-visible page.

---

### Task 1: Freeze baseline and create manifest

**Files:**
- Create: `_backup/2026-10-17-pre-image-refresh/`
- Create: `_repair/2026-10-17-image-refresh/IMAGE-MANIFEST.tsv`

- [x] Save the 26 affected HTML pages and the legacy-reference inventory.
- [x] Record every unique old asset, consuming pages, teaching role, output type, and new path.
- [x] Confirm the baseline contains 59 unique legacy assets, 66 references, and 26 affected pages.

### Task 2: Refresh foundation visuals

**Files:**
- Modify: `CH1-1.html`, `CH2-1.html`, `CH2-2.html`
- Create: foundation assets under `assets/course-visuals/2026-10/`

- [x] Produce the PM-role and brief diagrams deterministically where readable structure matters.
- [x] Produce eight layout variants, vague/structured brief comparison, and three style presets.
- [x] Update only manifest-matched `src` values.
- [x] Validate assets, HTML structure, local references, and 1440/390 rendering before Task 3.

### Task 3: Refresh structure and transfer visuals

**Files:**
- Modify: `CH3-1.html`, `CH4-1.html`, `CH4-2.html`, `CH4-3.html`
- Create: structure/transfer assets under `assets/course-visuals/2026-10/`

- [x] Produce L4/L2, cross-industry, layout-variant, and seasonal-series visuals.
- [x] Preserve same-skeleton evidence across transfer examples.
- [x] Update manifest-matched `src` values and run the batch gate.

### Task 4: Refresh capstone evidence

**Files:**
- Modify: `CH5-1.html`
- Create: capstone and intentional-NG assets under `assets/course-visuals/2026-10/`

- [x] Produce five industry cases, three lookbook styles, and six intentional NG examples.
- [x] Check that each intentional defect is visible and matches its caption.
- [x] Update manifest-matched `src` values and run the batch gate.

### Task 5: Refresh CH6 use-case library

**Files:**
- Modify: `CH6-A1.html` through `CH6-C6.html`
- Create: 18 use-case assets under `assets/course-visuals/2026-10/`

- [x] Produce each use-case visual without depending on generated copy for correctness.
- [x] Preserve the specific commercial channel and aspect-ratio teaching purpose.
- [x] Update manifest-matched `src` values and run the batch gate.

### Task 6: Whole-course verification and fresh review

**Files:**
- Create: `_repair/2026-10-17-image-refresh/IMAGE-REFRESH-REPORT.md`
- Create: `_validation/image-refresh-fresh-review.md`

- [x] Verify zero `src="img/` occurrences and zero missing local image references.
- [x] Run structure, lint, substance, `git diff --check`, and scoped diff review.
- [x] Run browser smoke tests at 1440 px, 430 px, and 390 px on representative pages from every batch.
- [x] Ask a fresh reviewer to inspect manifest completeness, semantic fidelity, artifacts, rights risk, and responsive rendering.
- [x] Record exact evidence, remaining human checks, and rollback path.
