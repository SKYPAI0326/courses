# Gen Image 2026-10 Course Visual Refresh Design

## Intent

Replace every legacy `img/v*.png` asset still embedded in the current learner-facing handouts so the visual layer clearly matches the 2026-10 repaired content. The user has authorized a course-only reference pack, batch execution, and a fresh reviewer after the main flow.

## Scope

- `task_scope = content-change`
- Replace 59 unique legacy assets referenced 66 times by 26 HTML pages.
- Preserve each image's teaching role, surrounding visible text, `alt`, wrapper, navigation, gate, and page order.
- Store all refreshed assets under `assets/course-visuals/2026-10/` and update only the matching `img src` values.
- Keep `img/` untouched as a recovery source; do not overwrite legacy files.
- Keep the six-file READY reference pack unchanged unless an image is explicitly reused as a refreshed course visual.

## Visual Direction

- Course system: warm off-white, tea brown, sage green, restrained editorial spacing, believable material texture, and controlled lighting.
- Teaching examples retain their intended differences: layout type, industry, style preset, season, intentional NG defect, or CH6 use case must remain immediately distinguishable.
- Critical copy remains in HTML. New raster assets avoid relying on generated text for correctness; deterministic diagrams may use SVG.
- No real brand, trademark, public figure, recognizable copyrighted character, watermark, or unlicensed reference.
- People appear only where the lesson requires them, with fictional identity and non-sensitive context.

## Batch Map

1. Foundation: CH1-1, CH2-1, CH2-2 — 15 unique assets.
2. Structure and transfer: CH3-1, CH4-1, CH4-2, CH4-3 — 12 unique assets.
3. Capstone evidence: CH5-1 — 14 additional unique assets plus shared assets from earlier batches.
4. Use-case library: CH6-A1 through CH6-C6 — 18 unique assets.

## Acceptance Contract

- No learner-facing HTML contains `src="img/` after migration.
- All new `src` targets exist, are readable, and use versioned paths.
- Every old semantic role has a one-to-one manifest entry and a matching replacement.
- Visible text snapshots and DOM structure remain unchanged except the authorized image `src` paths.
- No missing local references, duplicate IDs, wrapper drift, or image-caused horizontal overflow at 1440 px, 430 px, and 390 px.
- A fresh reviewer checks semantic fidelity, obvious AI artifacts, instructional usefulness, rights risk, responsive rendering, and absence of legacy image references.

## Recovery

The pre-refresh HTML pages and image mapping are preserved under `_backup/2026-10-17-pre-image-refresh/`. Legacy image files remain in `img/`, so rollback does not require regenerating assets.
