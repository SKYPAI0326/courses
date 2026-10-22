# Gen Image Course Visual Refresh Report

Date: 2026-10-17  
Scope: 26 manifest-named learner pages; 59 unique legacy assets referenced 66 times.

## Result

- Added a course-only versioned pack at `assets/course-visuals/2026-10/`: 52 PNG + 7 SVG.
- Replaced all 66 scoped `img/v*.png` references with 59 versioned targets.
- Kept the legacy `img/` files intact for rollback.
- The initial `src` migration preserved learner-visible text on all 26 pages. Fresh review then authorized narrowly scoped semantic corrections beside mismatched images on 16 CH6 pages plus CH4-1 and CH5-1.
- Recorded asset roles and ownership in `IMAGE-MANIFEST.tsv`, normalized generation directives in `IMAGE-PROMPT-SET.md`, and per-asset source/checksum/edit history in `ASSET-PROVENANCE.tsv`.

## Batch evidence

| Batch | Assets | Pages | Static gate | Browser gate |
|---|---:|---:|---|---|
| CH1–CH2 foundation | 15 | 3 | text unchanged; structure OK; lint 0 blocker | legacy 0; broken 0; image overflow 0 at 390/430/1440 |
| CH3–CH4 transfer | 12 | 4 | text unchanged; structure OK; lint 0 blocker | legacy 0; broken 0; image overflow 0 at 390/430/1440 |
| CH5 capstone | 14 new + 4 shared | 1 | text unchanged; structure OK; lint 0 blocker | 13 image-bearing details opened; 20/20 loaded; legacy 0; broken 0; image overflow 0 at 390/430/1440 |
| CH6 use cases | 18 | 18 | structure OK; lint 0 blocker; 16 adjacent descriptions aligned to final pixels after fresh review | 18/18 loaded after lazy-load traversal; legacy 0; broken 0; overflow 0 at 430 and representative 390/1440 |

The CH6 Mid-Autumn gift-set visual was regenerated after review found Christmas cues; the final image uses osmanthus, a round lantern, and mooncake.

## Whole-scope verification

```text
python3 _tools/verify-image-refresh.py
IMAGE REFRESH VERIFY: PASS — 59 assets, 59 versioned targets, 0 legacy references

scoped learner-page lint: 26/26 passed
scoped learner-page substance audit: 26/26 machine-checked, 0 block
HTML structure summary: checked=44 blocked=0
git diff --check: pass
asset provenance: 59/59 checksums and generator references verified
```

Before fresh review, the src-only migration passed a 26/26 visible-text-unchanged comparison. The final release intentionally differs in adjacent learner text where the reviewer found inaccurate image descriptions, missing synthetic-content disclosure, a trademark-risk mascot name, an incompatible wireframe example, or a non-causal NG/OK comparison. Those corrections are recorded in `_validation/image-refresh-fresh-review.md`.

The recursive course-root lint and substance-audit commands also discover existing workshop backups and an HTML image-source file. Those unrelated files can produce blockers, so the release evidence above is intentionally scoped to the 26 manifest pages for this migration. The standalone two-hour workshop has its own current `img/workshop2h/` pack and is outside this replacement manifest.

## Rollback

- HTML backup: `_backup/2026-10-17-pre-image-refresh/course-html/` (26 pages)
- Legacy asset backup: `_backup/2026-10-17-pre-image-refresh/legacy-img/` (59 files)
- Mapping: `_repair/2026-10-17-image-refresh/IMAGE-MANIFEST.tsv`

## Remaining publication checks

This pack is suitable as course reference material. External publication still requires a human to verify generated copy, factual claims, product fidelity, rights, accessibility text, platform dimensions, and final brand approval.

## Fresh review

Four review rounds were completed after the main batches. The final round returned PASS with 0 blocker, 0 major, and 0 minor. Release state: `MACHINE_READY_PENDING_HUMAN`. Full issue and repair history is in `_validation/image-refresh-fresh-review.md`.
