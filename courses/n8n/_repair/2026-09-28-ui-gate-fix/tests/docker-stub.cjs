#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const root = process.env.LITE_FIXTURE_ROOT;
if (!root) throw new Error('LITE_FIXTURE_ROOT is required');
const shared = path.join(root, 'n8n-starter-kit', 'shared');
const stateDir = path.join(root, 'state');
const logFile = path.join(root, 'docker-log.txt');

let args = process.argv.slice(2);
if (args.shift() !== 'compose') throw new Error('Expected docker compose');
if (args[0] === '-f') args.splice(0, 2);

function log(value) {
  fs.appendFileSync(logFile, `${value}\n`);
}

function hostPath(value) {
  const prefix = '/files/shared/';
  if (value.startsWith(prefix)) return path.join(shared, value.slice(prefix.length));
  return value;
}

function workflowFile(id) {
  return path.join(stateDir, `${id}.json`);
}

function readWorkflow(id) {
  return JSON.parse(fs.readFileSync(workflowFile(id), 'utf8'));
}

function writeWorkflow(workflow) {
  fs.writeFileSync(workflowFile(workflow.id), `${JSON.stringify(workflow, null, 2)}\n`);
}

const verb = args.shift();
if (verb === 'stop' || verb === 'start') {
  log(verb);
  process.exit(0);
}

if (verb === 'exec') {
  if (args[0] === '-T') args.shift();
  const service = args.shift();
  if (service !== 'n8n') throw new Error(`Unexpected service: ${service}`);
  if (args[0] === 'n8n' && args[1] === '--version') {
    process.stdout.write('2.37.7\n');
    process.exit(0);
  }
  if (args[0] === 'n8n' && args[1] === 'export:workflow') {
    const idArg = args.find((arg) => arg.startsWith('--id='));
    const outputArg = args.find((arg) => arg.startsWith('--output='));
    const id = idArg && idArg.slice('--id='.length);
    const output = outputArg && hostPath(outputArg.slice('--output='.length));
    if (!id || !output) throw new Error('Export requires --id and --output');
    const published = args.includes('--published');
    const source = published ? path.join(stateDir, `${id}.published.json`) : workflowFile(id);
    if (published && !fs.existsSync(source)) throw new Error(`No published fixture for ${id}`);
    const workflow = JSON.parse(fs.readFileSync(source, 'utf8'));
    fs.mkdirSync(path.dirname(output), { recursive: true });
    fs.writeFileSync(output, `${JSON.stringify(workflow, null, 2)}\n`);
    log(`export${published ? '-published' : ''}:${id}`);
    process.stdout.write('Successfully exported 1 workflow.\n');
    process.exit(0);
  }
  if (args[0] === 'node') {
    const script = hostPath(args[1]);
    const scriptArgs = args.slice(2).map(hostPath);
    const result = spawnSync(process.execPath, [script, ...scriptArgs], { stdio: 'inherit' });
    process.exit(result.status === null ? 1 : result.status);
  }
  throw new Error(`Unsupported exec command: ${args.join(' ')}`);
}

if (verb === 'run') {
  while (args.length && args[0].startsWith('-')) {
    const option = args.shift();
    if (option === '--rm' || option === '--no-deps' || option === '-T') continue;
    throw new Error(`Unexpected run option: ${option}`);
  }
  const service = args.shift();
  if (service !== 'n8n') throw new Error(`Unexpected run service: ${service}`);
  const command = args.shift();
  if (command === 'import:workflow') {
    const inputArg = args.find((arg) => arg.startsWith('--input='));
    if (!inputArg) throw new Error('Import requires --input');
    const input = hostPath(inputArg.slice('--input='.length));
    const workflow = JSON.parse(fs.readFileSync(input, 'utf8'));
    const isPatch = input.includes('/merged/');
    const failMarker = path.join(root, 'fail-once.marker');
    if (isPatch && process.env.PATCH_TEST_FAIL_PATCH_IMPORT_ONCE === '1' && !fs.existsSync(failMarker)) {
      fs.writeFileSync(failMarker, 'failed once');
      log(`import-failed-once:${workflow.id}`);
      process.stderr.write('Simulated import failure.\n');
      process.exit(41);
    }
    workflow.active = false;
    writeWorkflow(workflow);
    log(`import:${workflow.id}:${isPatch ? 'patch' : 'backup'}`);
    process.stdout.write('Successfully imported 1 workflow.\n');
    process.exit(0);
  }
  if (command === 'publish:workflow') {
    const idArg = args.find((arg) => arg.startsWith('--id='));
    const id = idArg && idArg.slice('--id='.length);
    if (!id) throw new Error('Publish requires --id');
    const workflow = readWorkflow(id);
    workflow.active = true;
    writeWorkflow(workflow);
    log(`publish:${id}`);
    process.stdout.write('Workflow published.\n');
    process.exit(0);
  }
  throw new Error(`Unsupported run command: ${command}`);
}

throw new Error(`Unsupported docker compose verb: ${verb}`);
