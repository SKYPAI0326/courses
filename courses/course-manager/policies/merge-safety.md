# Merge Safety Policy

Compare files by workspace-relative path and SHA-256:

- missing destination file: `new`
- same path and same hash: `identical`
- same path and different hash: `conflict`

Conflicts are BLOCKED. The first version never performs semantic merges or overwrites different content automatically.
