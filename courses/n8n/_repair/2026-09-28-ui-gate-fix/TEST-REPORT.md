# Verification Report — Lite Pack #06/#12 UI Repair

Date: 2026-09-28

## Result

- Repair archive built at `n8n/assets/n8n-lite-pack-ui-fix.zip` (25,253 bytes).
- SHA-256: `2c4342db177af7ed84918f527f4820bd9d273232f1acaa4b3e8c70e5cb7ff51c`.
- Rebuilding twice produced the same archive hash.
- 16 Node tests passed, including targeted merge preservation, fail-closed ID/node validation, cancellation, rollback after simulated import failure, and refusal to apply when an active workflow has unpublished differences.
- `check-lite-pack-contract.py` passed: the source Lite Pack remains 14 workflows, local UI routes are clean of course password gates, and starter archive matches.
- ZIP member list and compressed data integrity passed; the archive includes both Mac and Windows launchers, instructions, merger and only #06/#12 workflow payloads.
- Mac shell scripts passed `bash -n`; `git diff --check` passed.
- Both Mac and Windows install pages link to the patch inside B1. Their matching link resolves to the generated archive.
- Course page lint scanned both modified pages: 0 blockers, 0 errors, 6 existing warnings; every relative `href`/`src` target on both pages resolves.
- The shared structure validator reports both pages as blocked because they predate and lack the validator's required `.lesson-body` wrapper. The same wrapper findings occur in the untouched snapshots; the only new visible-text/href differences are the intended repair callouts and download links.

## Not verified on a real learner machine

- No live n8n/Docker database was imported or restarted. Runtime behavior was exercised against an isolated Docker CLI mock only.
- This Mac environment has no PowerShell executable, so the Windows `.ps1` was statically reviewed but not parsed or executed here.
- Browser download smoke test is pending publication; this repair was not committed or pushed.
- Visual browser smoke was not performed because the local-page browser preview was denied by the app's URL security policy; no alternate route was used.
