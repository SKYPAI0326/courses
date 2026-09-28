const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { spawnSync } = require('node:child_process');
const test = require('node:test');
const { activeState, assertPublishedMatchesDraft, mergeWorkflow, TARGETS } = require('../../../_tools/lite-pack-ui-fix/merge-workflow.cjs');
const n8nDir = path.resolve(__dirname, '../../..');

function workflow(id, nodeId, nodeName, jsCode, extra = {}) {
  return {
    id,
    name: `workflow-${id}`,
    active: false,
    nodes: [
      { id: nodeId, name: nodeName, type: 'n8n-nodes-base.code', parameters: { jsCode, mode: 'runOnceForAllItems' }, position: [1, 2] },
      { id: 'other-node', name: 'Other', type: 'n8n-nodes-base.set', parameters: { keep: true }, position: [3, 4] },
    ],
    connections: { Other: { main: [] } },
    settings: { executionOrder: 'v1' },
    pinData: { Other: [{ json: { retained: true } }] },
    ...extra,
  };
}

test('updates only the approved UI Code node and preserves the learner workflow', () => {
  const target = TARGETS['lite-pack-06-webhook-gemini-file'];
  const current = workflow(target.workflowId, target.nodeId, target.nodeName, 'old local UI');
  const corrected = workflow(target.workflowId, target.nodeId, target.nodeName, 'fixed local UI');
  const before = structuredClone(current);

  const merged = mergeWorkflow(current, corrected);

  assert.equal(merged.nodes[0].parameters.jsCode, 'fixed local UI');
  const expected = structuredClone(before);
  expected.nodes[0].parameters.jsCode = 'fixed local UI';
  assert.deepEqual(merged, expected);
  assert.equal(current.nodes[0].parameters.jsCode, 'old local UI', 'must not mutate the input object');
});

test('supports the second approved workflow only at its designated UI node', () => {
  const target = TARGETS['lite-pack-12-knowledge-rag'];
  const current = workflow(target.workflowId, target.nodeId, target.nodeName, 'old kb UI');
  const corrected = workflow(target.workflowId, target.nodeId, target.nodeName, 'fixed kb UI');

  assert.equal(mergeWorkflow(current, corrected).nodes[0].parameters.jsCode, 'fixed kb UI');
});

test('rejects any workflow outside the two-workflow allowlist', () => {
  const current = workflow('learner-custom-workflow', 'ui-node', 'Code: UI', 'old');
  const corrected = workflow('learner-custom-workflow', 'ui-node', 'Code: UI', 'new');

  assert.throws(() => mergeWorkflow(current, corrected), /not allowlisted/i);
});

test('rejects an ID mismatch before returning a merged workflow', () => {
  const target = TARGETS['lite-pack-06-webhook-gemini-file'];
  const current = workflow(target.workflowId, target.nodeId, target.nodeName, 'old');
  const otherTarget = TARGETS['lite-pack-12-knowledge-rag'];
  const corrected = workflow(otherTarget.workflowId, otherTarget.nodeId, otherTarget.nodeName, 'new');

  assert.throws(() => mergeWorkflow(current, corrected), /workflow ID mismatch/i);
});

test('rejects missing or duplicate target nodes instead of guessing', () => {
  const target = TARGETS['lite-pack-06-webhook-gemini-file'];
  const missing = workflow(target.workflowId, 'other', 'Other', 'old');
  const correct = workflow(target.workflowId, target.nodeId, target.nodeName, 'new');
  assert.throws(() => mergeWorkflow(missing, correct), /target node/i);

  const duplicate = workflow(target.workflowId, target.nodeId, target.nodeName, 'old');
  duplicate.nodes.push(structuredClone(duplicate.nodes[0]));
  assert.throws(() => mergeWorkflow(duplicate, correct), /exactly one target node/i);
});

test('requires stable node identity/type and non-empty replacement code', () => {
  const target = TARGETS['lite-pack-06-webhook-gemini-file'];
  const current = workflow(target.workflowId, target.nodeId, target.nodeName, 'old');
  const wrongName = workflow(target.workflowId, target.nodeId, 'Different node', 'new');
  assert.throws(() => mergeWorkflow(current, wrongName), /exactly one target node/i);

  const emptyCode = workflow(target.workflowId, target.nodeId, target.nodeName, '');
  assert.throws(() => mergeWorkflow(current, emptyCode), /non-empty/i);
});

test('publish status is read explicitly and preserved by the merge', () => {
  const target = TARGETS['lite-pack-06-webhook-gemini-file'];
  const current = workflow(target.workflowId, target.nodeId, target.nodeName, 'old', { active: true });
  const corrected = workflow(target.workflowId, target.nodeId, target.nodeName, 'new', { active: false });
  const merged = mergeWorkflow(current, corrected);

  assert.equal(activeState(current), true);
  assert.equal(merged.active, true);
  assert.throws(() => activeState({ ...current, active: undefined }), /active field is missing/i);
});

test('published comparison ignores version metadata but blocks any unpublished workflow edit', () => {
  const target = TARGETS['lite-pack-06-webhook-gemini-file'];
  const draft = workflow(target.workflowId, target.nodeId, target.nodeName, 'current draft UI', {
    versionId: 'draft-version', versionCounter: 4, updatedAt: '2026-09-28T12:00:00Z',
  });
  const published = workflow(target.workflowId, target.nodeId, target.nodeName, 'current draft UI', {
    versionId: 'published-version', versionCounter: 3, updatedAt: '2026-09-27T12:00:00Z',
    versionMetadata: { name: 'historical name', description: 'historical description' },
  });
  assert.equal(assertPublishedMatchesDraft(draft, published), true);

  const pendingDraft = structuredClone(draft);
  pendingDraft.nodes[1].parameters.keep = false;
  assert.throws(() => assertPublishedMatchesDraft(pendingDraft, published), /differs from the published workflow/i);
  const changedUiDraft = structuredClone(draft);
  changedUiDraft.nodes[0].parameters.jsCode = 'unpublished UI change';
  assert.throws(() => assertPublishedMatchesDraft(changedUiDraft, published), /differs from the published workflow/i);
});

test('both platform updaters back up before import and never remove volumes', () => {
  const packageDir = path.join(n8nDir, 'assets/n8n-lite-pack-ui-fix');
  const mac = fs.readFileSync(path.join(packageDir, 'apply-fix.command'), 'utf8');
  const windows = fs.readFileSync(path.join(packageDir, 'apply-fix.ps1'), 'utf8');
  const scripts = [mac, windows];

  for (const script of scripts) {
    assert.match(script, /export:workflow/);
    assert.match(script, /--published/);
    assert.match(script, /--assert-published/);
    assert.match(script, /import:workflow/);
    assert.match(script, /publish:workflow/);
    assert.doesNotMatch(script, /down\s+-v/i);
    assert.doesNotMatch(script, /setup-wizard/i);
    assert.match(script, /輸入 YES/);
  }

  const macApply = mac.indexOf('echo "備份與差異檢查完成');
  assert.ok(mac.indexOf('n8n export:workflow') < macApply);
  assert.ok(mac.indexOf('--assert-published') < macApply);
  assert.ok(macApply < mac.indexOf('compose stop n8n', macApply));
  assert.ok(mac.indexOf('compose stop n8n', macApply) < mac.indexOf('import:workflow', macApply));

  const windowsApply = windows.indexOf("Write-Host '備份與差異檢查完成");
  assert.ok(windows.indexOf('export:workflow') < windowsApply);
  assert.ok(windows.indexOf('--assert-published') < windowsApply);
  assert.ok(windowsApply < windows.indexOf("@('stop', 'n8n')", windowsApply));
  assert.ok(windows.indexOf("@('stop', 'n8n')", windowsApply) < windows.indexOf('import:workflow', windowsApply));
});

test('both install pages link to the patch inside the B1 install section', () => {
  for (const pageName of ['m0-install-mac.html', 'm0-install-win.html']) {
    const pagePath = path.join(n8nDir, 'lessons', pageName);
    const html = fs.readFileSync(pagePath, 'utf8');
    const b1 = html.indexOf('<div class="step-num">B1</div>');
    const b2 = html.indexOf('<div class="step-num">B2</div>', b1);
    const block = html.slice(b1, b2);
    assert.ok(b1 >= 0 && b2 > b1, `${pageName} has B1 and B2 anchors`);
    assert.match(block, /n8n-lite-pack-ui-fix\.zip\?v=1\.0\.0/);
    assert.match(block, /只更新這兩個頁面/);
    assert.ok(fs.existsSync(path.resolve(path.dirname(pagePath), '../assets/n8n-lite-pack-ui-fix.zip')));
  }
});

test('repair ZIP contains only the required learner-facing patch files', () => {
  const zipPath = path.join(n8nDir, 'assets/n8n-lite-pack-ui-fix.zip');
  const members = execFileSync('unzip', ['-Z1', zipPath], { encoding: 'utf8' }).trim().split(/\r?\n/).sort();
  assert.deepEqual(members, [
    'n8n-lite-pack-ui-fix/',
    'n8n-lite-pack-ui-fix/README.md',
    'n8n-lite-pack-ui-fix/apply-fix.bat',
    'n8n-lite-pack-ui-fix/apply-fix.command',
    'n8n-lite-pack-ui-fix/apply-fix.ps1',
    'n8n-lite-pack-ui-fix/merge-workflow.cjs',
    'n8n-lite-pack-ui-fix/workflows/',
    'n8n-lite-pack-ui-fix/workflows/06-webhook-gemini-file.json',
    'n8n-lite-pack-ui-fix/workflows/12-knowledge-rag.json',
  ].sort());

  for (const { member, sourcePath } of [
    { member: 'README.md', sourcePath: 'README.md' },
    { member: 'apply-fix.command', sourcePath: 'apply-fix.command' },
    { member: 'apply-fix.bat', sourcePath: 'apply-fix.bat' },
    { member: 'apply-fix.ps1', sourcePath: 'apply-fix.ps1' },
    { member: 'merge-workflow.cjs', sourcePath: 'merge-workflow.cjs' },
    { member: 'workflows/06-webhook-gemini-file.json', sourcePath: 'workflows/06-webhook-gemini-file.json' },
    { member: 'workflows/12-knowledge-rag.json', sourcePath: 'workflows/12-knowledge-rag.json' },
  ]) {
    const archived = execFileSync('unzip', ['-p', zipPath, `n8n-lite-pack-ui-fix/${member}`]);
    const source = fs.readFileSync(path.join(n8nDir, 'assets/n8n-lite-pack-ui-fix', sourcePath));
    assert.deepEqual(archived, source, `${member} inside ZIP matches the build source`);
  }
});

test('packaged local UI nodes use local webhook routes without the course password gate', () => {
  const packageDir = path.join(n8nDir, 'assets/n8n-lite-pack-ui-fix/workflows');
  const expectations = [
    ['06-webhook-gemini-file.json', 'code-html-ui-06', '/webhook/ai-ui'],
    ['12-knowledge-rag.json', 'code-html-ui', '/webhook/kb-ui'],
  ];
  for (const [filename, nodeId, localRoute] of expectations) {
    const workflow = JSON.parse(fs.readFileSync(path.join(packageDir, filename), 'utf8'));
    const matches = workflow.nodes.filter((node) => node.id === nodeId);
    assert.equal(matches.length, 1);
    const code = matches[0].parameters.jsCode;
    assert.ok(code.includes(localRoute));
    assert.doesNotMatch(code, /課程專屬講義|id=["']_gate|n8n_auth/i);
  }
});

function createMockKit(tempRoot, pendingDraft = false) {
  const kitDir = path.join(tempRoot, 'n8n-starter-kit');
  const patchDir = path.join(kitDir, 'n8n-lite-pack-ui-fix');
  const sharedDir = path.join(kitDir, 'shared');
  const stateDir = path.join(tempRoot, 'state');
  const binDir = path.join(tempRoot, 'bin');
  const packageDir = path.join(n8nDir, 'assets/n8n-lite-pack-ui-fix');
  fs.mkdirSync(path.join(patchDir, 'workflows'), { recursive: true });
  fs.mkdirSync(sharedDir, { recursive: true });
  fs.mkdirSync(stateDir, { recursive: true });
  fs.mkdirSync(binDir, { recursive: true });
  fs.writeFileSync(path.join(kitDir, 'n8n-compose.yml'), 'services: {}\n');
  for (const file of ['apply-fix.command', 'merge-workflow.cjs']) {
    fs.copyFileSync(path.join(packageDir, file), path.join(patchDir, file));
  }
  for (const file of ['06-webhook-gemini-file.json', '12-knowledge-rag.json']) {
    fs.copyFileSync(path.join(packageDir, 'workflows', file), path.join(patchDir, 'workflows', file));
  }
  const dockerPath = path.join(binDir, 'docker');
  fs.copyFileSync(path.join(__dirname, 'docker-stub.cjs'), dockerPath);
  fs.chmodSync(dockerPath, 0o755);

  const id06 = TARGETS['lite-pack-06-webhook-gemini-file'];
  const id12 = TARGETS['lite-pack-12-knowledge-rag'];
  const old06 = workflow(id06.workflowId, id06.nodeId, id06.nodeName, 'old local UI #06', {
    active: true,
    credentials: { telegramApi: { id: 'student-credential-06', name: 'Student Telegram' } },
    settings: { executionOrder: 'v1', customData: 'keep-06' },
  });
  const old12 = workflow(id12.workflowId, id12.nodeId, id12.nodeName, 'old local UI #12', {
    active: false,
    settings: { executionOrder: 'v1', customData: 'keep-12' },
  });
  const published06 = structuredClone(old06);
  published06.versionId = 'published-version-06';
  published06.versionCounter = 1;
  published06.versionMetadata = { name: 'published snapshot' };
  if (pendingDraft) old06.nodes[1].parameters.keep = false;
  const unrelated = { id: 'unrelated-workflow', nodes: [{ id: 'untouched' }], active: true };
  fs.writeFileSync(path.join(stateDir, `${old06.id}.json`), JSON.stringify(old06, null, 2));
  fs.writeFileSync(path.join(stateDir, `${old06.id}.published.json`), JSON.stringify(published06, null, 2));
  fs.writeFileSync(path.join(stateDir, `${old12.id}.json`), JSON.stringify(old12, null, 2));
  fs.writeFileSync(path.join(stateDir, 'unrelated-workflow.json'), JSON.stringify(unrelated, null, 2));
  return { kitDir, patchDir, sharedDir, stateDir, binDir, old06, old12, published06, unrelated };
}

function runMockUpdater(tempRoot, failPatchImport = false, confirmation = 'YES', pendingDraft = false) {
  const fixture = createMockKit(tempRoot, pendingDraft);
  const env = {
    ...process.env,
    LITE_FIXTURE_ROOT: tempRoot,
    PATH: `${fixture.binDir}${path.delimiter}${process.env.PATH}`,
  };
  if (failPatchImport) env.PATCH_TEST_FAIL_PATCH_IMPORT_ONCE = '1';
  const result = spawnSync('bash', [path.join(fixture.patchDir, 'apply-fix.command')], {
    encoding: 'utf8',
    env,
    input: `${confirmation}\n`,
    timeout: 15000,
  });
  return { fixture, result };
}

test('Mac updater changes only the two UI nodes and restores the original publish state', (t) => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'lite-pack-ui-fix-success-'));
  t.after(() => fs.rmSync(tempRoot, { recursive: true, force: true }));
  const { fixture, result } = runMockUpdater(tempRoot);
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);

  const patched06 = JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old06.id}.json`), 'utf8'));
  const patched12 = JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old12.id}.json`), 'utf8'));
  const unrelatedAfter = JSON.parse(fs.readFileSync(path.join(fixture.stateDir, 'unrelated-workflow.json'), 'utf8'));
  const source06 = JSON.parse(fs.readFileSync(path.join(fixture.patchDir, 'workflows/06-webhook-gemini-file.json'), 'utf8'));
  const source12 = JSON.parse(fs.readFileSync(path.join(fixture.patchDir, 'workflows/12-knowledge-rag.json'), 'utf8'));
  assert.equal(patched06.nodes[0].parameters.jsCode, source06.nodes.find((node) => node.id === 'code-html-ui-06').parameters.jsCode);
  assert.equal(patched12.nodes[0].parameters.jsCode, source12.nodes.find((node) => node.id === 'code-html-ui').parameters.jsCode);
  assert.equal(patched06.active, true);
  assert.equal(patched12.active, false);
  assert.deepEqual(patched06.credentials, fixture.old06.credentials);
  assert.deepEqual(patched06.settings, fixture.old06.settings);
  assert.deepEqual(unrelatedAfter, fixture.unrelated);
  const workDirs = fs.readdirSync(fixture.sharedDir).filter((name) => name.startsWith('lite-pack-ui-fix-'));
  assert.equal(workDirs.length, 1);
  const backupDir = path.join(fixture.sharedDir, workDirs[0], 'backup');
  assert.ok(fs.existsSync(path.join(backupDir, '06-original.json')));
  assert.ok(fs.existsSync(path.join(backupDir, '12-original.json')));
  const log = fs.readFileSync(path.join(tempRoot, 'docker-log.txt'), 'utf8');
  assert.match(log, /stop\n/);
  assert.match(log, /start\n/);
  assert.match(log, new RegExp(`export-published:${fixture.old06.id}`));
  assert.match(log, new RegExp(`publish:${fixture.old06.id}`));
  assert.doesNotMatch(log, new RegExp(`publish:${fixture.old12.id}`));
});

test('Mac updater stops before import when an active workflow has unrelated unpublished edits', (t) => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'lite-pack-ui-fix-pending-draft-'));
  t.after(() => fs.rmSync(tempRoot, { recursive: true, force: true }));
  const { fixture, result } = runMockUpdater(tempRoot, false, 'YES', true);
  assert.notEqual(result.status, 0, 'pending edits outside the target UI must block the patch');
  assert.match(result.stderr, /differs from the published workflow/i);

  const after06 = JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old06.id}.json`), 'utf8'));
  assert.deepEqual(after06, fixture.old06);
  const log = fs.readFileSync(path.join(tempRoot, 'docker-log.txt'), 'utf8');
  assert.match(log, new RegExp(`export-published:${fixture.old06.id}`));
  assert.doesNotMatch(log, /stop\n|import:/);
});

test('Mac updater rolls back both workflows after an import failure', (t) => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'lite-pack-ui-fix-rollback-'));
  t.after(() => fs.rmSync(tempRoot, { recursive: true, force: true }));
  const { fixture, result } = runMockUpdater(tempRoot, true);
  assert.notEqual(result.status, 0, 'simulated import error should be reported');

  const after06 = JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old06.id}.json`), 'utf8'));
  const after12 = JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old12.id}.json`), 'utf8'));
  assert.equal(after06.nodes[0].parameters.jsCode, 'old local UI #06');
  assert.equal(after12.nodes[0].parameters.jsCode, 'old local UI #12');
  assert.equal(after06.active, true);
  assert.equal(after12.active, false);
  const log = fs.readFileSync(path.join(tempRoot, 'docker-log.txt'), 'utf8');
  assert.match(log, /import-failed-once:/);
  assert.match(log, /import:lite-pack-06-webhook-gemini-file:backup/);
  assert.match(log, /import:lite-pack-12-knowledge-rag:backup/);
  assert.match(log, /start\n/);
});

test('Mac updater cancellation leaves workflows and shared files untouched', (t) => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'lite-pack-ui-fix-cancel-'));
  t.after(() => fs.rmSync(tempRoot, { recursive: true, force: true }));
  const { fixture, result } = runMockUpdater(tempRoot, false, 'NO');
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.deepEqual(JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old06.id}.json`), 'utf8')), fixture.old06);
  assert.deepEqual(JSON.parse(fs.readFileSync(path.join(fixture.stateDir, `${fixture.old12.id}.json`), 'utf8')), fixture.old12);
  assert.deepEqual(fs.readdirSync(fixture.sharedDir), []);
  assert.equal(fs.existsSync(path.join(tempRoot, 'docker-log.txt')), false);
});
