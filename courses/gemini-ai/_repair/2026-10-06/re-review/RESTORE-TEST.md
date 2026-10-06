# Restore test — 2026-10-06

- Backup manifest contains 59 files. The current `assets/materials/materials.zip` was added before synchronizing the prompt asset bundle; the original archive is preserved and its SHA-256 is in the manifest.
- `bash -n _tools/restore-2026-10-06-re-review.sh`: PASS.
- Isolated retest root: `/private/tmp/gemini-course-restore-retest-rlue3ttp`.
- Mutated the copied `assets/materials/materials.zip`, ran the restore script against the isolated copy, then verified SHA-256 and byte size for all 59 manifest entries: PASS.
- Test altered only the isolated copy; the active course checkout was not used for rollback testing.
