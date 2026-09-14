#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/_backup/2026-09-14-pre-repair"

FILES=(
  "lessons/post-llm-1-overview.html"
  "lessons/post-llm-2-flow.html"
  "lessons/post-llm-3-steps-decompose.html"
  "lessons/post-llm-5-redlines.html"
  "lessons/post-llm-6-walkthrough.html"
  "lessons/post-llm-7-triage.html"
  "lessons/post-llm-8-environment.html"
  "lessons/post-llm-9-format-adapt.html"
  "lessons/post-llm-appendix-nodes.html"
  "lessons/post-cloud-n8n.html"
  "lessons/m0-cloud-vs-selfhost.html"
  "lessons/m0-local-llm-guide.html"
  "lessons/m0-workflow-04-daily.html"
  "lessons/m0-workflow-07-tunnel.html"
  "lessons/m0-workflow-09-gmail.html"
  "lessons/m0-workflow-12-knowledge-rag.html"
  "lessons/m0-workflow-tour.html"
  "lessons/m1-2-tunnel.html"
  "lessons/m3-3-generate.html"
  "lessons/m4-1-remote.html"
  "lessons/m4-2-api.html"
  "_lessons/post-llm/post-llm-2-flow.md"
  "_lessons/post-llm/post-llm-3-steps-decompose.md"
  "_lessons/post-llm/post-llm-4-steps-import.md"
  "_lessons/post-llm/post-llm-5-redlines.md"
  "_lessons/post-llm/post-llm-6-walkthrough.md"
  "_lessons/post-llm/post-llm-7-triage.md"
  "_lessons/post-llm/post-llm-8-environment.md"
  "_lessons/post-llm/post-llm-9-format-adapt.md"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/web-ui/06-ai-ui.html"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/web-ui/12-kb-ui.html"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/README.md"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/_change-log.md"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/workflows/01-webhook-hello-world.json"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/workflows/04-daily-ai-report.json"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/workflows/09-gmail-categorize.json"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/workflows/06-webhook-gemini-file.json"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/workflows/07-quick-tunnel-receiver.json"
  "_work/2026-09-13-aq-key-format/n8n-lite-pack/workflows/12-knowledge-rag.json"
  "assets/n8n-lite-pack.zip"
)

for file in "${FILES[@]}"; do
  cp "$BACKUP/$file" "$ROOT/$file"
done

echo "Restored n8n stale-content repair backup (2026-09-14)."
