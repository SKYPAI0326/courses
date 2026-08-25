#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ "${CODEX_SANDBOX:-}" = "seatbelt" ]; then
  printf '%s\n' "PDF rendering requires an authorized host process; Chrome was not started." >&2
  printf '%s\n' "Re-run this exact command with external authorization: $0 ${*:-all}" >&2
  exit 2
fi

MODE=${1:-all}
shift || true
exec node "$SCRIPT_DIR/build-deliverables.js" "$MODE" "$@"
