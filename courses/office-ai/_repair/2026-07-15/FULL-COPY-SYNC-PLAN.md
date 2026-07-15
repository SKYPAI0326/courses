# Full Copy Sync Plan

## Scope

- Pages: `ch1/CH1-4.html`, `ch2/CH2-1.html`, `ch3/CH3-1.html`, `ch5/CH5-3.html`, `ch6/CH6-2.html`
- Goal: ensure every repaired comparison uses the same task facts and changes only the named teaching variable.
- Risk: existing course; backup and restore required.

## Issues and fixes

1. Give both CH2-1 holiday-letter prompts the same length limit.
2. Give both CH2-1 product-review prompts the same deliverable; change only the role.
3. Give both CH2-1 social-post prompts the same product; change only the example.
4. Give both CH3-1 announcement prompts the same audience and output specifications; change only the missing-value rule.
5. Give both CH5-3 meeting prompts the same meeting facts; change only the missing-value rule.
6. Give both CH6-2 discount prompts the same policy; change only identifying details.
7. Describe CH1-4's third turn as adding a new requirement, not filling an omission.

## Verification

- Target-page lint and whole-course lint.
- Semantic comparison audit: same facts and deliverable on both sides, with one named variable changed.
- Rebuild search index and sitemap.
- Validate restore script syntax.
