# Accounting Function Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an offline accounting batch-calculation app and a separate HTML presentation that truthfully shows how prompting, constraints, and tests corrected LLM-generated mistakes.

**Architecture:** Each deliverable is a self-contained HTML file with inline CSS and JavaScript. The calculator keeps pure parsing and accounting functions in a named `accounting-core` script exposed through `globalThis.AccountingLab`, while a separate UI script owns DOM state; Node tests extract and execute the pure core without browser dependencies. The presentation uses a small inline slide engine and derives its case studies from a checked-in build-evidence log created while implementing the calculator.

**Tech Stack:** HTML5, native CSS, native JavaScript, Node.js built-in `node:test`, no runtime dependencies

**Spec:** `accounting-function-lab/docs/superpowers/specs/2026-08-20-accounting-function-lab-design.md`

## Global Constraints

- Deliver `accounting-function-lab/accounting-calculator.html` and `accounting-function-lab/ai-development-story.html` as independently openable, offline files.
- Use native HTML, CSS, and JavaScript only; no framework, CDN, backend, external font, network API, or LLM call.
- Treat pasted data as text; never inject it through `innerHTML`.
- Never silently fill missing accounting values, discard invalid rows, infer ambiguous dates, or claim jurisdiction-specific tax correctness.
- Every successful result must retain source row, formula, parameters, rounding rule, and status.
- The deck may condense actual interactions but must label condensed material and must not invent failures or successes.
- Existing unrelated worktree changes are out of scope; stage only files under `accounting-function-lab/`.

## File Map

- `accounting-function-lab/accounting-calculator.html` — complete calculator UI, styles, pure core functions, UI controller, built-in regression-test panel.
- `accounting-function-lab/ai-development-story.html` — complete slide deck, styles, slide navigation, overview, fullscreen behavior, and embedded evidence-backed narrative.
- `accounting-function-lab/tests/accounting-core.test.mjs` — Node tests for delimiter detection, CSV parsing, number/date safety, four calculator modules, and export hardening.
- `accounting-function-lab/tests/html-contract.test.mjs` — structural tests for offline constraints, accessibility landmarks, safe rendering, and both HTML files' required controls.
- `accounting-function-lab/docs/ai-build-evidence.md` — concise source log of actual implementation failures, reproductions, prompt constraint added, and verification result used by the deck.

---

### Task 1: Calculator Shell and Test Harness

**Files:**
- Create: `accounting-function-lab/accounting-calculator.html`
- Create: `accounting-function-lab/tests/accounting-core.test.mjs`
- Create: `accounting-function-lab/tests/html-contract.test.mjs`
- Create: `accounting-function-lab/docs/ai-build-evidence.md`

**Interfaces:**
- Produces: `<script id="accounting-core">` containing `globalThis.AccountingLab`.
- Produces: `AccountingLab.parseDelimited(text, delimiter): {headers:string[], rows:Array<{sourceRow:number, values:string[]}>}`.
- Produces: calculator DOM IDs `module-tabs`, `data-input`, `delimiter-select`, `parse-button`, `mapping-panel`, `parameter-panel`, `calculate-button`, `result-summary`, `error-list`, `result-table`, `copy-button`, `download-button`, `run-tests-button`, `test-results`.

- [ ] **Step 1: Write the failing HTML contract test**

Create `tests/html-contract.test.mjs` with Node built-ins. Assert the calculator is offline and exposes its required structure:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const calculatorPath = new URL('../accounting-calculator.html', import.meta.url);

test('calculator is offline and contains required controls', async () => {
  const html = await readFile(calculatorPath, 'utf8');
  assert.match(html, /<!DOCTYPE html>/i);
  assert.doesNotMatch(html, /<script[^>]+src=/i);
  assert.doesNotMatch(html, /<link[^>]+href=["']https?:/i);
  for (const id of ['module-tabs', 'data-input', 'parse-button', 'mapping-panel',
    'parameter-panel', 'calculate-button', 'result-summary', 'error-list',
    'result-table', 'copy-button', 'download-button', 'run-tests-button', 'test-results']) {
    assert.match(html, new RegExp(`id=["']${id}["']`));
  }
  assert.match(html, /id=["']accounting-core["']/);
  assert.doesNotMatch(html, /\.innerHTML\s*=/);
});
```

- [ ] **Step 2: Run the contract test and verify it fails**

Run: `node --test accounting-function-lab/tests/html-contract.test.mjs`

Expected: FAIL with `ENOENT` for `accounting-calculator.html`.

- [ ] **Step 3: Create the minimal calculator shell**

Create a valid `zh-Hant` HTML document with inline `<style>`, semantic `<header>`, `<main>`, `<section>`, `<table>`, labelled controls, all IDs listed above, a status region using `aria-live="polite"`, and:

```html
<script id="accounting-core">
(() => {
  function parseDelimited() {
    return { headers: [], rows: [] };
  }
  globalThis.AccountingLab = { parseDelimited };
})();
</script>
<script id="accounting-ui">
(() => {
  const byId = id => document.getElementById(id);
  byId('parse-button').addEventListener('click', () => {
    const parsed = globalThis.AccountingLab.parseDelimited(byId('data-input').value, '\t');
    byId('result-summary').textContent = `讀取 ${parsed.rows.length} 筆資料`;
  });
})();
</script>
```

Use CSS custom properties, a restrained ink-blue/muted-green palette, visible focus styles, responsive grid layout, horizontal scrolling only inside table containers, and a reduced-motion media query.

- [ ] **Step 4: Add the core extraction helper and smoke test**

In `tests/accounting-core.test.mjs`, extract only the pure core script and execute it in a VM context:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { readFile } from 'node:fs/promises';

async function loadCore() {
  const html = await readFile(new URL('../accounting-calculator.html', import.meta.url), 'utf8');
  const match = html.match(/<script id="accounting-core">([\s\S]*?)<\/script>/);
  assert.ok(match, 'accounting-core script exists');
  const context = vm.createContext({ globalThis: {} });
  vm.runInContext(match[1], context);
  return context.globalThis.AccountingLab;
}

test('core exposes parser', async () => {
  const core = await loadCore();
  assert.equal(typeof core.parseDelimited, 'function');
});
```

- [ ] **Step 5: Run both tests and verify they pass**

Run: `node --test accounting-function-lab/tests/*.test.mjs`

Expected: 2 tests PASS, 0 FAIL.

- [ ] **Step 6: Start the evidence log and commit**

Create `docs/ai-build-evidence.md` with headings `Issue`, `Reproduction`, `LLM tendency`, `Constraint added`, and `Verification`. Record only problems actually observed while executing later tasks; initially state that the log contains no case until a failure is reproduced.

```bash
git add accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/tests/accounting-core.test.mjs \
  accounting-function-lab/tests/html-contract.test.mjs \
  accounting-function-lab/docs/ai-build-evidence.md
git commit -m "feat: scaffold offline accounting lab"
```

### Task 2: Robust Pasted-Table Parsing

**Files:**
- Modify: `accounting-function-lab/accounting-calculator.html`
- Modify: `accounting-function-lab/tests/accounting-core.test.mjs`
- Modify: `accounting-function-lab/docs/ai-build-evidence.md`

**Interfaces:**
- Produces: `detectDelimiter(text): '\t' | ',' | ';'`.
- Produces: `parseDelimited(text, delimiter): {headers, rows, errors}` with quoted-field and escaped-quote support.
- Produces: `parseAccountingNumber(raw, options): {ok:boolean, value?:number, error?:string}`.
- Produces: `parseStrictDate(raw, order): {ok:boolean, value?:string, error?:string}` where `value` is ISO `YYYY-MM-DD`.

- [ ] **Step 1: Add failing parser tests**

Add tests for quoted commas, escaped quotes, TSV, consistent delimiter detection, blank cells, parentheses negatives, thousands separators, currency-symbol rejection, and ambiguous dates:

```js
test('parses quoted CSV and preserves source rows', async () => {
  const core = await loadCore();
  const result = core.parseDelimited('名稱,金額\n"甲,公司","1,200"\n乙公司,', ',');
  assert.deepEqual([...result.headers], ['名稱', '金額']);
  assert.equal(result.rows[0].values[0], '甲,公司');
  assert.equal(result.rows[0].values[1], '1,200');
  assert.equal(result.rows[0].sourceRow, 2);
  assert.equal(result.rows[1].values[1], '');
});

test('rejects currency symbols and ambiguous dates', async () => {
  const core = await loadCore();
  assert.equal(core.parseAccountingNumber('NT$1,000', { allowCurrency: false }).ok, false);
  assert.equal(core.parseAccountingNumber('(1,250)', { allowCurrency: false }).value, -1250);
  assert.equal(core.parseStrictDate('03/04/2026', 'reject-ambiguous').ok, false);
});
```

- [ ] **Step 2: Run the targeted tests and verify failure**

Run: `node --test --test-name-pattern="parses quoted|rejects currency" accounting-function-lab/tests/accounting-core.test.mjs`

Expected: FAIL because the parser helpers are missing or incomplete.

- [ ] **Step 3: Implement a character-by-character parser**

Implement parsing without `split(',')`: maintain `field`, `row`, `inQuotes`, and `sourceRow`; treat `""` inside a quoted field as one quote; preserve empty fields; reject inconsistent row widths into `errors`. Make delimiter detection score `\t`, `,`, and `;` by consistent non-singleton column counts across non-empty lines.

Implement number parsing with explicit regular expressions for `-1234.50`, `1,234.50`, and `(1,234.50)`. Reject currency symbols unless `allowCurrency` is true. Implement strict ISO parsing and explicit `dmy`/`mdy` modes; `reject-ambiguous` must reject slash dates where both first components are 1–12.

- [ ] **Step 4: Run all core tests**

Run: `node --test accounting-function-lab/tests/accounting-core.test.mjs`

Expected: all parser tests PASS.

- [ ] **Step 5: Record one actual parser failure and its prompt constraint**

If the first implementation failed a test, add the exact input, wrong result, and the new constraint to `docs/ai-build-evidence.md`. If it passed immediately, record no invented failure; defer the first case to a later task.

- [ ] **Step 6: Commit the parser**

```bash
git add accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/tests/accounting-core.test.mjs \
  accounting-function-lab/docs/ai-build-evidence.md
git commit -m "feat: parse pasted accounting tables safely"
```

### Task 3: Accounting Calculators and Row-Level Validation

**Files:**
- Modify: `accounting-function-lab/accounting-calculator.html`
- Modify: `accounting-function-lab/tests/accounting-core.test.mjs`
- Modify: `accounting-function-lab/docs/ai-build-evidence.md`

**Interfaces:**
- Produces: `calculateTax(row, params): CalculationResult`.
- Produces: `calculateProfit(row, params): CalculationResult`.
- Produces: `calculateDepreciation(row, params): CalculationResult`.
- Produces: `calculateAging(row, params): CalculationResult`.
- `CalculationResult` shape: `{ok:boolean, sourceRow:number, outputs:Record<string,number|string>, formula:string, parameters:Record<string,number|string|boolean>, rounding:string, errors:Array<{field:string, message:string}>}`.
- Produces: `runBatch(moduleId, rows, mapping, params): {successes:CalculationResult[], failures:CalculationResult[], warnings:CalculationResult[]}`.

- [ ] **Step 1: Add failing formula tests with fixed expected answers**

Add at least these cases:

```js
test('tax conversion has traceable rounding', async () => {
  const core = await loadCore();
  const result = core.calculateTax({ sourceRow: 2, amount: 1000 },
    { mode: 'net-to-gross', taxRate: 0.05, decimals: 0 });
  assert.equal(result.ok, true);
  assert.equal(result.outputs.tax, 50);
  assert.equal(result.outputs.gross, 1050);
  assert.match(result.formula, /1000/);
  assert.equal(result.sourceRow, 2);
});

test('profit rejects zero revenue for margin', async () => {
  const core = await loadCore();
  const result = core.calculateProfit({ sourceRow: 3, revenue: 0, cogs: 0 }, { metric: 'gross-margin' });
  assert.equal(result.ok, false);
  assert.match(result.errors[0].message, /不可為 0/);
});

test('depreciation is capped at depreciable basis', async () => {
  const core = await loadCore();
  const result = core.calculateDepreciation({ sourceRow: 2, cost: 120000, residual: 12000,
    years: 3, startDate: '2023-01-15' }, { cutoffDate: '2028-12-31', decimals: 0 });
  assert.equal(result.outputs.accumulatedDepreciation, 108000);
});

test('aging uses due date rather than transaction date', async () => {
  const core = await loadCore();
  const result = core.calculateAging({ sourceRow: 2, id: 'INV-1', dueDate: '2026-07-01', amount: 8000 },
    { asOfDate: '2026-08-20', buckets: [30, 60, 90] });
  assert.equal(result.outputs.daysOverdue, 50);
  assert.equal(result.outputs.bucket, '31–60');
});
```

Also test gross-to-net tax, net profit, break-even with non-positive contribution margin, residual greater than cost, cutoff before start, invalid date, missing values, custom aging buckets, and the explicit `blankAsZero` choice.

- [ ] **Step 2: Run formula tests and verify failure**

Run: `node --test accounting-function-lab/tests/accounting-core.test.mjs`

Expected: FAIL because calculator functions are not defined.

- [ ] **Step 3: Implement minimal pure calculators**

Create a shared `makeResult`, decimal rounding helper, required-field validator, and the four named calculators. Tax rate must come from params. Depreciation counts start and cutoff calendar months inclusively, divides `(cost - residual)` across `years * 12`, and caps accumulated depreciation at the depreciable basis. Aging computes whole calendar-day difference using UTC dates and labels negative values `未到期`.

- [ ] **Step 4: Implement batch routing and failure isolation**

`runBatch` must map source headers explicitly, call one calculator per valid row, keep invalid rows in `failures`, and never coerce missing values to zero unless `params.blankAsZero === true`. Add a test proving one bad row does not remove two valid neighboring rows.

- [ ] **Step 5: Run all calculator tests**

Run: `node --test accounting-function-lab/tests/accounting-core.test.mjs`

Expected: all parser and accounting tests PASS.

- [ ] **Step 6: Update evidence and commit**

Record any actual semantic mistake such as aging from the wrong date, automatic blank-to-zero conversion, uncapped depreciation, or a missing boundary. Include the failing fixture and passing command; do not create a case that did not occur.

```bash
git add accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/tests/accounting-core.test.mjs \
  accounting-function-lab/docs/ai-build-evidence.md
git commit -m "feat: add traceable accounting calculations"
```

### Task 4: Calculator Workflow, Mapping, Results, and Export

**Files:**
- Modify: `accounting-function-lab/accounting-calculator.html`
- Modify: `accounting-function-lab/tests/accounting-core.test.mjs`
- Modify: `accounting-function-lab/tests/html-contract.test.mjs`
- Modify: `accounting-function-lab/docs/ai-build-evidence.md`

**Interfaces:**
- Produces: `sanitizeSpreadsheetCell(value): string`.
- Produces: `toDelimited(headers, rows, delimiter): string`.
- Consumes: all Task 2 and Task 3 core functions.

- [ ] **Step 1: Add failing export-safety tests**

```js
test('neutralizes spreadsheet formula injection', async () => {
  const core = await loadCore();
  assert.equal(core.sanitizeSpreadsheetCell('=2+2'), "'=2+2");
  assert.equal(core.sanitizeSpreadsheetCell('+SUM(A1:A2)'), "'+SUM(A1:A2)");
  assert.equal(core.sanitizeSpreadsheetCell('一般文字'), '一般文字');
});

test('quotes exported delimiters and newlines', async () => {
  const core = await loadCore();
  const csv = core.toDelimited(['名稱', '備註'], [['甲,公司', '第一行\n第二行']], ',');
  assert.equal(csv, '名稱,備註\r\n"甲,公司","第一行\n第二行"');
});
```

- [ ] **Step 2: Run export tests and verify failure**

Run: `node --test --test-name-pattern="neutralizes|quotes exported" accounting-function-lab/tests/accounting-core.test.mjs`

Expected: FAIL because export helpers are missing.

- [ ] **Step 3: Implement safe export helpers**

Prefix text cells beginning with `=`, `+`, `-`, or `@` with an apostrophe; do not alter numeric results. Quote fields containing delimiter, quote, CR, or LF, and double internal quotes.

- [ ] **Step 4: Implement the end-to-end UI controller**

Build a state object with `moduleId`, `parsed`, `mapping`, `params`, and `batchResult`. Render with `document.createElement`, `replaceChildren`, and `textContent`. Implement:

- module-specific sample headers and a sample-data button;
- delimiter auto-detection with a manual override;
- preview and explicit source-to-required-field mapping;
- module-specific parameter controls;
- disabled Calculate button until required mappings and parameters are valid;
- success/warning/failure counts;
- row-level error list linking to source row;
- result table with source row, outputs, formula, parameters, rounding, and status;
- copy TSV and download CSV actions;
- confirmation before clearing or switching module when pasted data exists;
- a privacy notice stating that data stays in the browser.

- [ ] **Step 5: Add and run HTML safety/structure assertions**

Extend `html-contract.test.mjs` to assert four module buttons, a privacy notice, accessible labels, reduced-motion CSS, no assignment to `innerHTML`, and no network URLs.

Run: `node --test accounting-function-lab/tests/*.test.mjs`

Expected: all tests PASS.

- [ ] **Step 6: Implement the built-in regression panel**

Create a small array of fixed fixtures calling the same pure functions used by production. The `run-tests-button` must display each named test, expected value, actual value, and pass/fail status in `test-results`. Include at least one normal, one boundary, and one invalid-input case per module.

- [ ] **Step 7: Perform a browser smoke test**

Open `accounting-calculator.html` locally. For each module: load sample data, parse, map fields, calculate, inspect one formula, and export. Verify keyboard focus, narrow-width scrolling, and that invalid pasted markup such as `<img src=x onerror=alert(1)>` appears only as text.

Expected: all four flows complete offline; no console error; invalid row is visible and not calculated.

- [ ] **Step 8: Update evidence and commit**

Record any actual partial-generation or local-edit regression found while wiring the UI, including which existing behavior broke and the prompt constraint that would have prevented it (for example: “only edit the export function; preserve parser tests; return a change summary”).

```bash
git add accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/tests/accounting-core.test.mjs \
  accounting-function-lab/tests/html-contract.test.mjs \
  accounting-function-lab/docs/ai-build-evidence.md
git commit -m "feat: complete accounting batch workflow"
```

### Task 5: Evidence-Backed HTML Presentation

**Files:**
- Create: `accounting-function-lab/ai-development-story.html`
- Modify: `accounting-function-lab/tests/html-contract.test.mjs`
- Modify: `accounting-function-lab/docs/ai-build-evidence.md`

**Interfaces:**
- Produces: deck DOM IDs `deck`, `prev-slide`, `next-slide`, `slide-counter`, `overview-button`, `fullscreen-button`.
- Produces: `goTo(index)`, `next()`, `previous()`, `toggleOverview()`, and `toggleFullscreen()` inside an isolated deck script.
- Consumes: verified cases from `docs/ai-build-evidence.md`.

- [ ] **Step 1: Ensure the evidence source is sufficient**

Review `docs/ai-build-evidence.md`. It must contain at least three reproducible cases covering three distinct categories among semantic misunderstanding, incomplete boundary handling, context/local-edit regression, and web-LLM output truncation. If fewer than three naturally occurred, use a passing implementation to reproduce a known risk by temporarily applying the weaker prompt/logic in a throwaway copy under `/tmp`; record the reproducible comparison, then discard the copy. Do not describe an unobserved event as something that happened.

- [ ] **Step 2: Add a failing deck contract test**

```js
test('deck is offline, navigable, and contains evidence structure', async () => {
  const html = await readFile(new URL('../ai-development-story.html', import.meta.url), 'utf8');
  assert.doesNotMatch(html, /<script[^>]+src=/i);
  for (const id of ['deck', 'prev-slide', 'next-slide', 'slide-counter', 'overview-button', 'fullscreen-button']) {
    assert.match(html, new RegExp(`id=["']${id}["']`));
  }
  assert.ok((html.match(/class=["'][^"']*slide\b/g) || []).length >= 12);
  assert.match(html, /依實際互動濃縮/);
  assert.match(html, /語意|片面|上下文/);
  assert.match(html, /角色與任務/);
});
```

- [ ] **Step 3: Run the deck test and verify failure**

Run: `node --test --test-name-pattern="deck is offline" accounting-function-lab/tests/html-contract.test.mjs`

Expected: FAIL with `ENOENT` for `ai-development-story.html`.

- [ ] **Step 4: Build the 12-slide narrative**

Create the exact sequence from the spec: Excel problem, task framing, weak first prompt, semantic error, incomplete generation, web-LLM limitations, first prompt tightening, second prompt tightening, tests as dialogue, before/after comparison, human/AI responsibility split, and reusable seven-part prompt framework.

For each case-study slide, use the fixed fields `原始提示詞`, `LLM 行為摘要`, `問題症狀`, `根因`, `修正版提示詞`, `驗證結果`, `人工責任`. Copy facts from the evidence log and mark the dialogue `依實際互動濃縮`.

- [ ] **Step 5: Implement the native slide engine**

Use one active slide at a time, ArrowLeft/ArrowRight, PageUp/PageDown, Home/End, button navigation, an `aria-live` counter, overview grid, and Fullscreen API with rejection handled as status text. Do not call `scrollIntoView`; use class changes and `window.scrollTo({top: 0})` only when leaving overview.

- [ ] **Step 6: Apply the documentary visual system**

Use a dark ink background, paper-toned content surfaces, muted cyan for human constraints, amber for uncertainty, and red only for reproduced failures. Use system CJK fonts, code-like labels, visible focus, `clamp()` typography, 16:9 slide proportions with responsive fallback, and reduced-motion support. Do not use gradients, fake metrics, decorative emoji, or unrelated icons.

- [ ] **Step 7: Run tests and browser smoke test**

Run: `node --test accounting-function-lab/tests/*.test.mjs`

Expected: all tests PASS.

Open the deck locally and verify buttons, all keyboard commands, overview, fullscreen fallback, slide count, narrow viewport, and that every case maps back to a build-evidence entry.

- [ ] **Step 8: Commit the presentation**

```bash
git add accounting-function-lab/ai-development-story.html \
  accounting-function-lab/tests/html-contract.test.mjs \
  accounting-function-lab/docs/ai-build-evidence.md
git commit -m "feat: present the AI correction journey"
```

### Task 6: Final Integrated Verification

**Files:**
- Modify only if a verification failure requires a scoped fix: `accounting-function-lab/accounting-calculator.html`
- Modify only if a verification failure requires a scoped fix: `accounting-function-lab/ai-development-story.html`
- Modify only if tests need correction: `accounting-function-lab/tests/*.test.mjs`

**Interfaces:**
- Consumes: both final HTML files and both test files.
- Produces: verified, offline deliverables matching the design spec.

- [ ] **Step 1: Run automated tests**

Run: `node --test accounting-function-lab/tests/*.test.mjs`

Expected: 0 FAIL.

- [ ] **Step 2: Run source and offline checks**

Run:

```bash
rg -n "https?://|<script[^>]+src=|<link[^>]+href=" \
  accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/ai-development-story.html
rg -n "innerHTML\s*=|eval\(|new Function" \
  accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/ai-development-story.html
```

Expected: no matches.

- [ ] **Step 3: Verify scope and spec anchors**

Run:

```bash
git status --short -- accounting-function-lab
rg -n "營業稅|毛利|損益兩平|折舊|帳齡|資料不會上傳" \
  accounting-function-lab/accounting-calculator.html
rg -n "依實際互動濃縮|語意|片面|上下文|人工責任|角色與任務" \
  accounting-function-lab/ai-development-story.html
```

Expected: only intended files appear; every listed content anchor has a match.

- [ ] **Step 4: Run the final manual journey**

Use one pasted TSV sample containing two valid rows and one invalid row in every calculator module. Confirm valid rows calculate, the invalid row remains visible, formulas and parameters are traceable, TSV copy works, CSV download opens safely in a spreadsheet, and built-in regressions pass. Then navigate every slide and compare the three correction cases to `docs/ai-build-evidence.md`.

- [ ] **Step 5: Fix only observed failures and rerun Steps 1–4**

For each observed failure, add a failing automated test when the behavior is testable, implement the smallest scoped fix, and repeat the complete verification sequence. Do not modify unrelated course files.

- [ ] **Step 6: Commit final verification fixes if any**

If files changed during verification:

```bash
git add accounting-function-lab/accounting-calculator.html \
  accounting-function-lab/ai-development-story.html \
  accounting-function-lab/tests/accounting-core.test.mjs \
  accounting-function-lab/tests/html-contract.test.mjs \
  accounting-function-lab/docs/ai-build-evidence.md
git commit -m "fix: close accounting lab verification gaps"
```

If no file changed, do not create an empty commit.
