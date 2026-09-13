# Repair Plan: n8n AQ authorization key compatibility

## Scope
- `n8n/assets/n8n-lite-pack.zip`
- `n8n/lessons/m0-install-mac.html`
- `n8n/lessons/m0-install-win.html`

## Problem
Google AI Studio now creates authorization keys beginning with `AQ.` for new accounts. The Lite Pack wizard still accepted only the legacy `AIza` prefix, so a current learner could not pass Step 2.

## Repair
1. Back up the distribution zip and both platform guides.
2. Remove brittle prefix rejection; accept any non-empty complete key in macOS and Windows wizards, with `AIza` and `AQ.` shown as current examples.
3. Extend secret-leak scans and old-install detection to cover `AQ.` values.
4. Update learner-facing instructions, README version, and download cache-buster to v1.3.3.
5. Validate shell syntax, archive integrity, workflow count, and guide links before republishing.

## Manual validation
The Gemini smoke test remains the authority for whether the supplied key can call the configured endpoint. Prefix validation alone never marks a key usable.
