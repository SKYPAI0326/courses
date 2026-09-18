#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-18-pre-all-workbenches"

cp "$BACKUP/CH2-1.html" "$ROOT/CH2-1.html"
cp "$BACKUP/CH3-1.html" "$ROOT/CH3-1.html"
cp "$BACKUP/CH4-1.html" "$ROOT/CH4-1.html"
cp "$BACKUP/CH2-1-LESSON-PLAN.md" "$ROOT/CH2-1-LESSON-PLAN.md"
cp "$BACKUP/CH3-1-LESSON-PLAN.md" "$ROOT/CH3-1-LESSON-PLAN.md"
cp "$BACKUP/CH4-1-LESSON-PLAN.md" "$ROOT/CH4-1-LESSON-PLAN.md"
cp "$BACKUP/COURSE-BLUEPRINT.md" "$ROOT/COURSE-BLUEPRINT.md"
cp "$BACKUP/COVERAGE-LEDGER.md" "$ROOT/COVERAGE-LEDGER.md"
cp "$BACKUP/unit2-communication-scenarios.html" "$ROOT/assets/templates/unit2-communication-scenarios.html"
cp "$BACKUP/unit3-notebooklm-reading-pack.md" "$ROOT/assets/worksheets/unit3-notebooklm-reading-pack.md"
cp "$BACKUP/unit4-lifestyle-application-card.md" "$ROOT/assets/worksheets/unit4-lifestyle-application-card.md"

echo "Restored CH2-CH4 pre-workbench state from $BACKUP"
