#!/usr/bin/env bash
set -euo pipefail

COURSE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_ROOT="$COURSE_ROOT/_backup/2026-10-07-stage3-route-pre-sync"
CHECKSUMS="$BACKUP_ROOT/SHA256SUMS"

if [[ ! -f "$CHECKSUMS" ]]; then
  echo "Missing backup checksum manifest: $CHECKSUMS" >&2
  exit 1
fi
printf 'This restores the listed course files to their pre-route-sync state. Type RESTORE to continue: '
read -r confirmation
if [[ "$confirmation" != "RESTORE" ]]; then
  echo "Restore cancelled."
  exit 1
fi
while read -r checksum rel; do
  [[ -n "$checksum" && -n "$rel" ]] || continue
  mkdir -p "$COURSE_ROOT/$(dirname "$rel")"
  cp "$BACKUP_ROOT/$rel" "$COURSE_ROOT/$rel"
done < "$CHECKSUMS"
echo "Restored files listed in $CHECKSUMS"
