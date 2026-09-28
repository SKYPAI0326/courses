#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const TARGETS = Object.freeze({
  'lite-pack-06-webhook-gemini-file': Object.freeze({
    workflowId: 'lite-pack-06-webhook-gemini-file',
    nodeId: 'code-html-ui-06',
    nodeName: 'Code: 組 HTML (ai-ui)',
  }),
  'lite-pack-12-knowledge-rag': Object.freeze({
    workflowId: 'lite-pack-12-knowledge-rag',
    nodeId: 'code-html-ui',
    nodeName: 'Code: 組 HTML (kb-ui)',
  }),
});

function assertWorkflow(workflow, label) {
  if (!workflow || typeof workflow !== 'object' || Array.isArray(workflow)) {
    throw new Error(`${label} must be one workflow JSON object`);
  }
  if (typeof workflow.id !== 'string' || !TARGETS[workflow.id]) {
    throw new Error(`${label} workflow ID is not allowlisted`);
  }
  if (!Array.isArray(workflow.nodes)) {
    throw new Error(`${label} workflow has no nodes array`);
  }
  return TARGETS[workflow.id];
}

function getTargetNode(workflow, target, label) {
  const byId = workflow.nodes.filter((node) => node && node.id === target.nodeId);
  const byName = workflow.nodes.filter((node) => node && node.name === target.nodeName);
  if (byId.length !== 1 || byName.length !== 1 || byId[0] !== byName[0]) {
    throw new Error(`${label} must contain exactly one target node with the approved ID and name`);
  }
  const node = byId[0];
  if (node.type !== 'n8n-nodes-base.code') {
    throw new Error(`${label} target node identity mismatch: expected a Code node`);
  }
  if (!node.parameters || typeof node.parameters !== 'object' || Array.isArray(node.parameters)) {
    throw new Error(`${label} target node has no parameters object`);
  }
  return node;
}

function mergeWorkflow(current, corrected) {
  const currentTarget = assertWorkflow(current, 'Current');
  const correctedTarget = assertWorkflow(corrected, 'Patch');
  if (current.id !== corrected.id) {
    throw new Error(`Workflow ID mismatch: ${current.id} !== ${corrected.id}`);
  }
  if (currentTarget !== correctedTarget) {
    throw new Error('Workflow target mismatch');
  }

  const currentNode = getTargetNode(current, currentTarget, 'Current');
  const correctedNode = getTargetNode(corrected, correctedTarget, 'Patch');
  if (typeof correctedNode.parameters.jsCode !== 'string' || correctedNode.parameters.jsCode.trim() === '') {
    throw new Error('Patch UI Code node must contain non-empty JavaScript');
  }

  const merged = JSON.parse(JSON.stringify(current));
  const mergedNode = getTargetNode(merged, currentTarget, 'Merged');
  mergedNode.parameters.jsCode = correctedNode.parameters.jsCode;
  return merged;
}

function sortKeysDeep(value) {
  if (Array.isArray(value)) return value.map(sortKeysDeep);
  if (!value || typeof value !== 'object') return value;
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, sortKeysDeep(value[key])]));
}

function publishedComparable(workflow, target) {
  const copy = JSON.parse(JSON.stringify(workflow));
  for (const key of ['active', 'createdAt', 'updatedAt', 'versionId', 'versionCounter', 'triggerCount', 'versionMetadata']) {
    delete copy[key];
  }
  getTargetNode(copy, target, 'Workflow version');
  return sortKeysDeep(copy);
}

function assertPublishedMatchesDraft(draft, published) {
  const draftTarget = assertWorkflow(draft, 'Draft');
  const publishedTarget = assertWorkflow(published, 'Published');
  if (draft.id !== published.id || draftTarget !== publishedTarget) {
    throw new Error('Draft and published workflow IDs do not match');
  }
  const draftComparable = publishedComparable(draft, draftTarget);
  const publishedComparableValue = publishedComparable(published, publishedTarget);
  if (JSON.stringify(draftComparable) !== JSON.stringify(publishedComparableValue)) {
    throw new Error('Draft differs from the published workflow. Publish or resolve the existing edits in n8n first, then rerun; nothing was imported.');
  }
  return true;
}

function verifyWorkflow(current, corrected) {
  const currentTarget = assertWorkflow(current, 'Current');
  const correctedTarget = assertWorkflow(corrected, 'Patch');
  if (current.id !== corrected.id || currentTarget !== correctedTarget) {
    throw new Error('Workflow ID mismatch during verification');
  }
  const currentNode = getTargetNode(current, currentTarget, 'Current');
  const correctedNode = getTargetNode(corrected, correctedTarget, 'Patch');
  if (typeof currentNode.parameters.jsCode !== 'string' || currentNode.parameters.jsCode !== correctedNode.parameters.jsCode) {
    throw new Error(`Verification failed: ${current.id} UI code does not match the patch`);
  }
  return true;
}

function activeState(workflow) {
  const target = assertWorkflow(workflow, 'Current');
  getTargetNode(workflow, target, 'Current');
  if (typeof workflow.active !== 'boolean') {
    throw new Error(`Cannot safely preserve publish state for ${workflow.id}: exported active field is missing`);
  }
  return workflow.active;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJsonAtomic(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temp = `${file}.tmp-${process.pid}`;
  fs.writeFileSync(temp, `${JSON.stringify(data, null, 2)}\n`, { encoding: 'utf8', mode: 0o600 });
  fs.renameSync(temp, file);
}

function main(argv) {
  if (argv[0] === '--active' && argv.length === 2) {
    process.stdout.write(`${activeState(readJson(argv[1]))}\n`);
    return;
  }
  if (argv[0] === '--verify' && argv.length === 3) {
    verifyWorkflow(readJson(argv[1]), readJson(argv[2]));
    process.stdout.write('Verified target UI code.\n');
    return;
  }
  if (argv[0] === '--assert-published' && argv.length === 3) {
    assertPublishedMatchesDraft(readJson(argv[1]), readJson(argv[2]));
    process.stdout.write('Draft matches published workflow outside the target UI code.\n');
    return;
  }
  if (argv.length !== 3) {
    throw new Error('Usage: merge-workflow.cjs <current.json> <patch.json> <output.json> | --active <workflow.json> | --verify <current.json> <patch.json> | --assert-published <draft.json> <published.json>');
  }
  const merged = mergeWorkflow(readJson(argv[0]), readJson(argv[1]));
  writeJsonAtomic(argv[2], merged);
  process.stdout.write(`Merged only the approved UI Code node for ${merged.id}.\n`);
}

if (require.main === module) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`Patch stopped safely: ${error.message}\n`);
    process.exitCode = 1;
  }
}

module.exports = { TARGETS, mergeWorkflow, verifyWorkflow, activeState, assertPublishedMatchesDraft };
