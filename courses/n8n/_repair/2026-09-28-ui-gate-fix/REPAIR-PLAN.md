# Repair Plan — Existing Lite Pack UI Gate Patch

- **task_scope:** content-change + targeted workflow update artifact
- **course_slug:** n8n
- **status:** implemented and locally verified; not pushed
- **approved change:** provide an independently downloadable incremental patch for existing installs and add an entry to both Mac and Windows install pages; no full reinstall.

## Allowed changes

1. Add a self-contained patch package under `n8n/assets/n8n-lite-pack-ui-fix/` plus distributable `n8n/assets/n8n-lite-pack-ui-fix.zip`.
2. Patch package updates only the UI Code node JavaScript of workflow IDs `lite-pack-06-webhook-gemini-file` and `lite-pack-12-knowledge-rag`, by merging corrected code into each learner's own exported workflow.
3. Add one download link and concise safe-use explanation inside Phase B B1 of `n8n/lessons/m0-install-mac.html` and `m0-install-win.html`.
4. Add focused automated tests/build tooling and repair evidence under this dated repair directory.

## Explicitly out of scope

- No full Lite Pack import/reinstall, setup wizard, DB/volume cleanup, or `docker compose down -v`.
- No change to any workflow other than #06/#12, any other node in those workflows, credentials, shared files, course gates, or unrelated course pages.
- No commit or push.

## Implementation sequence

1. Record current page snapshots; create restore script.
2. Add failing tests for merge allowlist, preservation, and fail-closed behavior; confirm RED.
3. Implement merger, cross-platform updater scripts, package README and reproducible zip builder.
4. Verify Mac/Windows instructions and updater preflight/backup/rollback flow.
5. Add the download card to the exact B1 block on each platform page.
6. Run tests, archive checks, HTML/link checks, diff-scope audit; record limitations and results.

## HTML anchor

Within each install page's `<section id="phaseB" class="lesson-section">`, target the exact `<div class="step-block">` whose `.step-num` is `B1` and whose `.step-title` is `下載 Lite Pack zip`. Add the patch link and safety explanation immediately after the existing Lite Pack ZIP link; leave first-install steps unchanged.

## Acceptance criteria

- Merger copies only the approved code field from corrected package into an exported current workflow and retains all other JSON data.
- It refuses unsupported workflow/node identities and malformed or incomplete inputs before emitting an output.
- Updater makes timestamped backups before import, stops/starts only n8n, never removes a Docker volume, has a rollback path, and does not touch other workflow IDs.
- For a currently published workflow, updater compares the exported draft with its published version and aborts before stopping n8n if any content differs, preventing publication of unrelated draft work.
- Patch archive is reproducible from tracked package sources and contains only required files.
- Both pages contain accessible, matching wording and links to an existing archive.
- Focused updater/package tests, Lite Pack contract, archive checks, targeted relative-link check, and page lint pass. The structure validator has the same pre-existing `.lesson-body` wrapper block on both pages and their untouched snapshots. Runtime Docker application is reported as not performed unless independently tested in a safe disposable environment.
