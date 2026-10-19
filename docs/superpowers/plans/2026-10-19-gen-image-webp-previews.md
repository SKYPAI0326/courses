# Gen-image WebP Previews Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Serve compact WebP previews throughout the gen-image learner pages while opening retained original images in a new tab on activation.

**Architecture:** A focused Python tool parses top-level learner HTML with DOM ancestry, converts only referenced PNG originals, and performs surgical tag edits without reformatting pages. The same tool audits the mapping; existing course validators remain authoritative for structure and content.

**Tech Stack:** Python 3 standard library, `cwebp`, static HTML, existing course validators.

**Spec:** `courses/gen-image/_repair/2026-10-19-webp-previews/SPEC.md`

## Global Constraints

- Single-agent execution only; no subagents are authorized.
- WebP quality is 90 and pixel dimensions must match the PNG original.
- Preserve every original and all visible course content.
- SVG remains SVG.
- No commit or push without separate authorization.

## Review Focus

- Existing workshop image anchors must be updated, never nested.
- Reused PNGs must produce one WebP but may appear in multiple pages.
- SVG images must gain new-tab behavior without raster conversion.
- Image tags split across formatting styles must retain all protected attributes.
- Historical image-refresh validation must recognize original PNG anchor targets.

---

### Task 1: Reversible baseline and failing contract tests

**Files:**
- Create: `courses/gen-image/_backup/2026-10-19-pre-webp-previews/`
- Create: `courses/gen-image/_tools/restore-2026-10-19-pre-webp-previews.sh`
- Create: `courses/gen-image/_tools/test_webp_previews.py`

**Interfaces:**
- Produces: fixture expectations for `transform_html(text: str) -> str` and `audit_course(root: Path) -> AuditResult`.

- [ ] Back up the 29 target pages, record SHA-256 values, and prove restoration in a temporary copy.
- [ ] Write tests for an unwrapped PNG, an existing download anchor, reused assets, SVG handling, protected attributes, and nested-anchor rejection.
- [ ] Run `python3 -m unittest courses/gen-image/_tools/test_webp_previews.py -v` and confirm failure because the production module is absent.

### Task 2: Deterministic converter and HTML transformer

**Files:**
- Create: `courses/gen-image/_tools/webp_previews.py`
- Create: 61 sibling `.webp` files under `assets/course-visuals/2026-10/`, `assets/reference-pack/`, and `img/workshop2h/`.
- Modify: the 29 target learner pages named in the repair plan.

**Interfaces:**
- Produces: `transform_html(text: str) -> str`, `audit_course(root: Path) -> AuditResult`, and CLI modes `--write` / `--check`.

- [ ] Implement only enough parser-backed transformation logic to pass the fixture tests.
- [ ] Run unit tests and confirm they pass.
- [ ] Run `webp_previews.py --write` to generate Q90 previews and update image tags/anchors.
- [ ] Run `webp_previews.py --check` and confirm all count, path, size, dimension, and link contracts pass.

### Task 3: Preserve the historical image-refresh gate

**Files:**
- Modify: `courses/gen-image/_tools/verify-image-refresh.py`
- Modify: `courses/gen-image/_tools/test_webp_previews.py`

**Interfaces:**
- Consumes: original PNG paths carried by image-anchor `href` attributes.
- Produces: manifest usage validation over display sources plus original targets.

- [ ] Add a failing test showing a manifest PNG used as an original link with a WebP display.
- [ ] Update the verifier's contextual reference collection minimally.
- [ ] Run the focused tests and `verify-image-refresh.py`; confirm both pass.

### Task 4: Full validation and report

**Files:**
- Create: `courses/gen-image/_repair/2026-10-19-webp-previews/REPAIR-REPORT.md`
- Create: `courses/gen-image/_validation/webp-previews-2026-10-19.json`

**Interfaces:**
- Consumes: completed assets, HTML, unit tests, and existing validators.
- Produces: reproducible byte, structure, content, and browser evidence.

- [ ] Compare before/after visible text and protected image attributes.
- [ ] Run structure, lint, substance, unit, WebP, image-refresh, and diff checks.
- [ ] Browser-smoke CH2-1, CH5-1, CH4-2, index, and workshop pages at 1440, 820, and 390 px; confirm original targets open in new tabs.
- [ ] Record results, exceptions, and restore path; leave changes uncommitted for review.
