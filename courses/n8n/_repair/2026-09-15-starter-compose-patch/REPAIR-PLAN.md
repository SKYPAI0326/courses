# Lite Pack Starter Compose patch repair

## Root cause

The published macOS and Windows wizards search for an `environment:` block whose
items are consecutive YAML list lines. The Starter Kit intentionally contains
comments and blank lines in that block, so a missing variable makes the wizard
report `compose.yml patch 失敗` even when the compose file is valid YAML.

The wizard also asked for `N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false` while the
Starter Kit contract uses `true`.

## Scope

- Make both platform wizards locate the `n8n` service and insert missing env
  items around comments/blank lines.
- Align the required value and learner-facing error text with the Starter Kit.
- Bump the Lite Pack wizard/cache-buster to v1.3.6 and align the Starter Kit cache-buster with v1.1.0.
- Preserve the existing uncommitted Gmail-optional edits in the Mac/Windows
  install pages.

## Validation gate

1. Run the regression fixture before and after the patch (RED → GREEN).
2. Run `bash -n` on the macOS wizard.
3. Validate PowerShell source invariants; Windows runtime execution remains a
   manual gate because PowerShell is not installed on this host.
4. Rebuild the zip, run `unzip -t`, parse all 14 workflow JSON files, and
   verify the archive contains the patched v1.3.6 wizard and current Starter Kit
   contract.
