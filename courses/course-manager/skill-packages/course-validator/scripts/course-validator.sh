#!/bin/bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$#" -lt 1 ]; then echo "usage: course-validator.sh <slug> [all|preflight|status|report|content|L0|L1-L3|L4a|L4b|L5]"; exit 2; fi
case "${2:-all}" in
  L0|L1-L3|L4a|L4b|L5) exec bash "$script_dir/legacy-layers.sh" "$@" ;;
  *) exec python3 "$script_dir/validate_course.py" "$@" ;;
esac
