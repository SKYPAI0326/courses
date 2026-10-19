# WebP preview repair plan

## Goal and scope

Optimize the raster payload of the existing `gen-image` learner pages while preserving original files for inspection. This is a G4 asset/HTML repair with an explicitly authorized link-behavior change and no learning-content change.

## Target learner pages

`CH1-1.html`, `CH1-2.html`, `CH2-1.html`, `CH2-2.html`, `CH3-1.html`, `CH4-1.html`, `CH4-2.html`, `CH4-3.html`, `CH5-1.html`, `CH6-A1.html` through `CH6-A6.html`, `CH6-B1.html` through `CH6-B6.html`, `CH6-C1.html` through `CH6-C6.html`, `index.html`, and `workshop-2h-poster-social.html`.

## Files and responsibility

- Backup the 29 target HTML pages under `_backup/2026-10-19-pre-webp-previews/` with SHA-256 evidence.
- Add `_tools/restore-2026-10-19-pre-webp-previews.sh` to restore HTML and remove the 61 generated WebP previews.
- Add `_tools/webp_previews.py` as the deterministic transformer and verifier.
- Add `_tools/test_webp_previews.py` for transform and audit regression tests.
- Modify `_tools/verify-image-refresh.py` so the historical PNG manifest can be satisfied by original-image links while WebP is used for display.
- Generate 61 `.webp` siblings beside the referenced PNG originals.
- Modify only the image tags and their direct image-link anchors in the 29 target pages.
- Add a repair report and machine-readable verification evidence after validation.

## Verification

1. Watch the new unit tests fail before production implementation.
2. Prove the backup and restore script in an isolated temporary copy.
3. Run the WebP audit, image-refresh validator, HTML structure checks, course lint, substance checks, and `git diff --check`.
4. Compare visible text and protected image attributes before/after.
5. Browser-smoke representative pages at 1440, 820, and 390 px; activate raster and SVG image links and confirm a new tab targets the original file.
6. Record byte totals, page counts, image counts, exceptions, and changed paths.

## Stop conditions

Stop and restore if visible text changes, an original disappears, a WebP is larger than its PNG, an image becomes broken, anchors become nested, structure/lint gains a new error, or browser rendering changes beyond the clickable-link behavior.
