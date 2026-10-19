# Gen-image WebP preview repair report

## Result

Implementation and local verification pass. The work remains uncommitted and unpublished on branch `codex/gen-image-webp-previews`.

## Changes

- Generated 61 same-dimension WebP previews with `cwebp -q 90 -mt`.
- Reduced the learner-facing raster payload from 128.40 MiB to 13.30 MiB (89.6%).
- Updated 69 raster occurrences to display WebP while linking to retained PNG originals.
- Kept 10 SVG occurrences as SVG displays and linked them to their SVG originals.
- Updated all 79 image occurrences across 29 pages to use direct image links with `target="_blank"`, `rel="noopener"`, and an accessible new-tab label.
- Replaced the workshop page's image `download` behavior with new-tab original viewing.
- Added a deterministic build/audit tool and seven focused regression tests.
- Updated the historical image-refresh verifier to recognize WebP display sources plus original PNG targets.

No visible lesson text, image order, `alt`, `loading`, inline style, dimensions, navigation, or lesson wrapper changed.

## Verification

- Backup/restore: PASS — 30 existing files restored by SHA-256 in an isolated proof; 61 simulated WebP previews removed.
- Unit tests: PASS — 7/7.
- WebP contract: PASS — 29 pages, 79 occurrences, 61 PNG originals, 61 WebP previews.
- Image-refresh gate: PASS — 59 manifest assets, 112 versioned display/original references, 0 legacy references.
- Content snapshot: PASS — visible text and protected image attributes unchanged on 29 pages / 79 images.
- Structure: PASS — 44/44 pages.
- Lint: PASS — 44 pages, 0 BLOCKER, 0 ERROR, 8 WARN, 23 baseline-suppressed findings.
- Target-page substance: PASS — 29/29, 0 BLOCK.
- Browser: PASS — CH2-1, CH5-1, CH4-2, index, and workshop at 1440, 820, and 390 px; 15/15 combinations loaded every image and opened the original target in a new tab. Keyboard Enter also opened a representative WebP→PNG target and SVG→SVG target.
- Visual inspection: PASS — representative desktop, tablet, and mobile screenshots retained the existing layout.
- `git diff --check`: PASS.

Machine-readable evidence: `_validation/webp-previews-2026-10-19.json`.

## Existing exceptions and tradeoffs

- CH2-1 retains its previously documented 83 px mobile overflow at 390 px from the funnel table; this change introduced no new overflow.
- The recursive substance scanner still finds two historical, non-learner files: a workshop backup with stale links and an editable poster source without an H1. The 29 target learner pages pass the scoped gate.
- Original PNG files remain in the repository by requirement, so repository size grows by the 13.30 MiB preview set even though learner transfer size falls sharply.

## Recovery

Run `courses/gen-image/_tools/restore-2026-10-19-pre-webp-previews.sh`. It restores the 29 learner pages plus the historical image verifier, verifies their original hashes, and removes the 61 generated previews and new preview tools.
