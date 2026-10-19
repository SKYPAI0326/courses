# SDD ledger — plan: _repair/2026-10-17-image-refresh/IMAGE-REFRESH-PLAN.md

Pre-flight: Tasks 2–5 produce versioned assets and contextual `src` replacements consumed by Task 6 whole-course verification; the shared interface is `IMAGE-MANIFEST.tsv` plus `assets/course-visuals/2026-10/`.

Ruling: Execute in the current worktree instead of a new worktree — the image refresh must build on the uncommitted 2026-10-16 repaired HTML currently served to the user, and the writable scope does not include the repository root needed for a sibling worktree — cost if wrong: the resulting diff is mixed with the prior repair, mitigated by scoped backup, manifest, and no commit/push.

Ruling: Use one course-wide RED→GREEN migration verifier instead of a unit test per generated image — the deliverables are generated visual assets and contextual HTML references; the verifier can prove legacy references, versioned targets, existence, decodability, and manifest coverage — cost if wrong: semantic quality still needs browser inspection and a fresh reviewer.

Task 1: Ruling: Correct the planned asset count from 60 to 59 — the fresh `rg` inventory contains 59 unique files referenced 66 times across 26 pages; the earlier total double-counted one shared asset — cost if wrong: a missing asset could escape the manifest, mitigated by exact set comparison in the migration verifier.

Task 1: complete (tests: manifest rows 59 / unique old 59 / unique new 59; backup HTML 26 / legacy assets 59).

Task 2: Ruling: Interpret the responsive gate as no image-caused overflow — CH2-1 already has a 473 px document width at 390/430 px from pre-existing wide teaching content, while every refreshed image reports 0 px overflow and no layout/CSS was authorized — cost if wrong: the course retains a pre-existing mobile horizontal-scroll issue outside this image-only scope.

Task 2: complete (15/15 assets present; CH1-1/CH2-1/CH2-2 visible text unchanged; structure OK 3/3; lint blocked 0; browser legacy 0, broken 0, image overflow 0 at 390/430/1440).

Task 3: complete (12/12 assets present; CH3-1/CH4-1/CH4-2/CH4-3 visible text unchanged; structure OK 4/4; lint blocked 0; browser legacy 0, broken 0, image overflow 0 at 390/430/1440).

Task 4: complete (14 new assets plus 4 shared refreshed assets; CH5-1 visible text unchanged; structure OK; lint blocked 0; 13 image-bearing details expanded in browser; legacy 0, loaded 20/20, broken 0, image overflow 0 at 390/430/1440).

Task 5: complete (18/18 assets present; CH6 visible text unchanged 18/18; structure OK 18/18; lint blocked 0; browser loaded 18/18 after lazy-load traversal, legacy 0, broken 0, image overflow 0 at 430 and representative 390/1440; Mid-Autumn gift visual corrected from Christmas cues to osmanthus, lantern, and mooncake).

Task 6: complete after four fresh-review rounds. Round 1 corrected CH6 text/pixel mismatches, C6 model repetition, C4 synthetic-person disclosure, C5 naming risk, provenance, manifest, and browser evidence. Round 2 corrected v15 wireframe compatibility and v42 geographic implication. Round 3 restored the causal NG/OK comparison by regenerating v30 from v15 with only legacy matcha styling changed. Round 4 verdict: PASS — blocker 0, major 0, minor 0; release state `MACHINE_READY_PENDING_HUMAN`.
