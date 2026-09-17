# Scan: digital-content-growth-126h

## Scope

- 47 HTML pages: 1 course index, 6 module pages, 40 learner-facing unit pages.
- Source outline: `_outlines/digital-content-growth-126h.md`.
- This scan treats the attached screenshot as evidence of the current rendered state, not as a new design specification.

## Structural findings

1. The course index expands Part 1 but only links to module pages for Parts 2–6. `module1.html` repeats the Part 1 list.
2. The learner pages use four lesson-page CSS families; the module pages use two additional families; the index is a seventh family.
3. Learner section counts are inconsistent: 8 pages have 3 sections, 12 have 4, 4 have 7, 8 have 8, and 8 have 10.
4. The first visible section varies between task, learning flow, case, and teaching content.
5. `module*.html` exposes production status text such as `單元頁已建立` and `資產「待課前確認」`.
6. `CH1-1.html`, `CH1-2.html`, `CH1-3.html`, and `PRAC1.html` expose `講師授課筆記（不進講義）`.
7. Module card links do not set `color: inherit`; visited and unvisited cards therefore render purple and blue in the browser.
8. Part 3 contains invalid CSS variables such as `var(--)` and `rgba(,)`; Part 5–6 contains undefined `var(--a3)` references.
9. Unit-page logo links and back links do not use one navigation contract.

## Automated baseline

- Current course lint before repair: 0 BLOCKER, 16 ERROR, 105 WARN.
- The automated lint result does not cover learner-facing production notes, route asymmetry, or visual template drift.

## Activity Identity quick audit

The repair is limited to the page shell and learner-facing separation. Existing lesson activities and artifacts remain in place for content review. The page rebuild must not invent new Demo/Together/Solo activities or duplicate existing workflows.

| page family | material | artifact | path | learner decision | verdict |
|---|---|---|---|---|---|
| CH1–CH2 | existing lesson examples and templates | existing unit artifact | existing lesson body | existing lesson decisions | preserve; normalize shell |
| CH3 | existing PRAC2/social examples | existing social plan artifacts | existing lesson body | existing channel decisions | preserve; normalize shell |
| CH4 | LocalWP/GA4/GTM/GSC materials named by lesson | existing SEO/tracking artifacts | existing lesson body | existing evidence decisions | preserve; normalize shell |
| CH5–CH6 | existing planning/capstone material | existing campaign/capstone artifacts | existing lesson body | existing market and delivery decisions | preserve; normalize shell |

## Shared Copy Audit

| repeated copy | pages | action |
|---|---|---|
| `單元頁已建立` | index + module pages | remove from learner-facing navigation; replace with purpose/output metadata |
| `資產「待課前確認」` | index + module pages | remove production status from learner view; keep learner-specific material and fallback inside the relevant unit |
| `講師授課筆記（不進講義）` | CH1-1, CH1-2, CH1-3, PRAC1 | move to repair archive; exclude from generated learner pages |
