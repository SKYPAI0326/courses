#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-17-pre-contract-rebuild"

for file in \
  CH1-1-LESSON-PLAN.md \
  CH2-1-LESSON-PLAN.md \
  CH3-1-LESSON-PLAN.md \
  CH4-1-LESSON-PLAN.md \
  CH1-1.html \
  CH2-1.html \
  CH3-1.html \
  CH4-1.html \
  COURSE-BLUEPRINT.md \
  COVERAGE-LEDGER.md
do
  cp "$BACKUP/$file" "$ROOT/$file"
done

rm -f "$ROOT/assets/templates/unit2-communication-scenarios.html"
mkdir -p "$ROOT/tmp/pdfs"
for file in \
  ai-beginner-practical-classroom-print-handout.html \
  ai-beginner-practical-full-offline-handout.html
do
  cp "$BACKUP/tmp-pdfs/$file" "$ROOT/tmp/pdfs/$file"
done
echo "Restored ai-beginner-practical contract-rebuild scope from $BACKUP"
