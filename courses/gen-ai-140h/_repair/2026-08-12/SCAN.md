# Scan: Vercel／Render 部署角色一致化

## Scope

- Course: `gen-ai-140h`
- Date: 2026-08-12
- Source files: 19 HTML + `_outlines/gen-ai-140h.md`
- Content changes in this scan: none

## Baseline

- Full-course lint: 78 pages, 0 BLOCKER, 0 ERROR, 232 WARN.
- Existing WARN are baseline debt and are not attributed to this repair.
- Platform references are distributed across Part 4, Part 5, Part 6, Part 7, course navigation, progress UI and outline.

## Findings

### BLOCKER · STALE_UI · CH5-4 / PRAC5-4

The runnable backend path instructs learners to create a Railway project, use Railway Variables, generate a Railway domain and diagnose Railway deployment logs. Railway is no longer a sustainable free path for this course requirement.

Evidence anchors before repair:

- `railway.app`
- `.up.railway.app`
- `New Project`
- `Generate Domain`
- `Railway 常見問題`

Required repair: keep the existing Node.js／Express learner path, but replace the complete deployment operation with Render Web Service steps, Render environment variables, `onrender.com`, Logs and cold-start troubleshooting.

### MAJOR · LEARNER_PATH · platform roles conflict

The course currently treats Vercel, Railway and Render as interchangeable in several decision tables and exercises. That collapses three distinct learner decisions:

- Pure static page without secret: GitHub Pages.
- Personal non-commercial portfolio／class demo: Vercel Hobby.
- Express backend, company／client prototype or possible commercial use: Render main path.

Required repair: make the decision visible before the learner deploys, then keep the selected role consistent in instructions, expected outputs, checkpoints, rubrics and capstone references.

### MAJOR · CONTENT_THIN · Vercel usage boundary missing

Vercel deployment exercises do not consistently tell learners that Hobby is limited to personal, non-commercial use. Client, company, paid-work and sales cases can therefore be misread as valid Hobby deployments.

Required repair: full explanation in core decision pages; short `Vercel Hobby（個人非商業）` labels elsewhere. Client and company cases must not recommend Hobby.

### MINOR · OUTLINE_SYNC

The outline lists Vercel but not Render in frontmatter, labels PRAC5-4 as Railway, and describes PRAC5-17 without the personal non-commercial boundary.

Required repair: synchronize the outline after the HTML roles are stable.

## Activity Identity Audit

This repair does not change activity material, artifact, operation sequence or learner decision except the deployment-platform decision itself.

| page group | material | artifact | operation path | learner decision | overlap verdict |
|---|---|---|---|---|---|
| CH5-4 | title-tool Node／Express repo | protected AI tool URL | local → GitHub → cloud backend | whether a backend is required | retain; platform steps become Render |
| PRAC5-4 | qa-tool／learner project | protected proxy deployment | local → GitHub → cloud backend → verification | adapt endpoint and validate key protection | retain; platform steps become Render |
| PRAC5-2 | static site repo | personal portfolio URL | GitHub → static host → redeploy | choose host from purpose constraints | add commercial-use decision |
| Part 7 | capstone repo | final public project | choose architecture → deploy → verify | personal demo vs professional／commercial use | add explicit platform boundary |

CH5-4 Demo and PRAC5-4 practice use different materials and learner decisions; changing the host does not create a new Activity Identity collision.

## Shared Copy Audit

| repeated copy | pages | allowed reason | action |
|---|---|---|---|
| Full Vercel Hobby commercial boundary | core decision pages | needed before a real platform choice | keep only in CH4-3, CH5-4, PRAC5-2, PRAC5-4 |
| Short personal non-commercial label | navigation and extension pages | prevents stale platform implication | use compact wording only |
| Render Free limitations | Render operation pages | required before deployment and troubleshooting | full card in CH5-4／PRAC5-4; short cold-start note in capstone |

## Release Risk

- Near-term class: unknown.
- Backup required: yes.
- UI facts are time-sensitive: future course-refresh must revalidate Render and Vercel plan rules.
