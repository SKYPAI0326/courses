#!/usr/bin/env node
/**
 * v2.0 #10 workflow 本地單元測試 harness
 *
 * 模擬 n8n 的 $input.all() / $('Read 所有檔案').all() / this.helpers.httpRequest，
 * 跑 5 種 input scenarios 驗證 jsCode 在各邊界都正確。
 *
 * 跑法：node _test_workflow_10.js
 *
 * 通過判準：每個 scenario 的 inputCount === outputCount，且分類符合預期。
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── 從 workflow JSON 抽出 jsCode ──
const wfPath = path.join(__dirname, '10-folder-organize.json');
const wf = JSON.parse(fs.readFileSync(wfPath, 'utf8'));
const aiNode = wf.nodes.find(n => n.name === 'Code: AI 分類 + 命名');
const jsCode = aiNode.parameters.jsCode;

// ── Mock helpers ──
function makeReadItem(fileName, opts = {}) {
  const ext = (fileName.split('.').pop() || '').toLowerCase();
  return {
    json: {
      fileName,
      fileExtension: ext,
      mimeType: opts.mimeType || 'application/octet-stream',
      fileSize: opts.fileSize || 1024,
    },
    binary: {
      data: {
        fileName,
        fileExtension: ext,
        mimeType: opts.mimeType || 'application/octet-stream',
        fileSize: opts.fileSize || 1024,
        data: 'base64-placeholder',
      },
    },
  };
}

function makeExtractedItem(fileName, text) {
  return {
    json: { text, data: text }, // both fields for safety
    binary: { data: { fileName } },
  };
}

// ── Mock $input + $ + this.helpers ──
function makeContext({ readItems, extractedItems, mockAIResponse }) {
  return {
    items: extractedItems,
    allReadItems: readItems,
    helpers: {
      httpRequest: async () => mockAIResponse,
    },
  };
}

// ── 包成可呼叫的 async function（用 new Function 注入 mocks）──
async function runJsCode(ctx) {
  const wrappedCode = `
    return (async function () {
      const $input = { all: () => __items };
      const $ = (nodeName) => ({ all: () => __allReadItems });
      const this_helpers = __helpers;
      // 改掉 jsCode 內 this.helpers 引用
      ${jsCode.replace(/this\.helpers/g, 'this_helpers')}
    })();
  `;
  const fn = new Function('__items', '__allReadItems', '__helpers', wrappedCode);
  return await fn(ctx.items, ctx.allReadItems, ctx.helpers);
}

// ── Scenarios ──
const scenarios = [];

// Scenario 1: N=0
scenarios.push({
  name: 'N=0（空輸入）',
  ctx: makeContext({ readItems: [], extractedItems: [], mockAIResponse: null }),
  expect: (results) => {
    if (results.length !== 1) return `expected 1 placeholder item, got ${results.length}`;
    if (results[0].json._batchInfo?.inputCount !== 0) return 'inputCount should be 0';
    return null;
  },
});

// Scenario 2: N=1 PDF
scenarios.push({
  name: 'N=1（單一 PDF）',
  ctx: (() => {
    const readItems = [makeReadItem('合約_NDA.pdf')];
    const extractedItems = [makeExtractedItem('合約_NDA.pdf', '本合約由甲方與乙方簽訂...保密協議...NDA')];
    const aiResp = {
      candidates: [{
        content: {
          parts: [{
            text: '[{"category":"contracts","newName":"20260506_合約_NDA"}]',
          }],
        },
      }],
    };
    return makeContext({ readItems, extractedItems, mockAIResponse: aiResp });
  })(),
  expect: (results) => {
    if (results.length !== 1) return `expected 1 result, got ${results.length}`;
    if (results[0].json.category !== 'contracts') return 'should classify as contracts';
    return null;
  },
});

// Scenario 3: N=12 mixed (matches user's actual input set)
scenarios.push({
  name: "N=12 mixed（學員實際 input set）",
  ctx: (() => {
    const fileSpecs = [
      'AI 生產力實戰全攻略.pdf',
      '中小企業應用生成式AI實務01.pptx',
      '中小企業應用生成式AI實務02.pptx',
      '中小企業應用生成式AI實務03.pptx',
      '通用觀念_LLM.pptx',
      '01提示詞基礎.docx',
      '02提示詞進階.docx',
      '03提示詞公式.docx',
      '04提示詞角色.docx',
      '05提示詞優化.docx',
      '06提示詞JSON格式.docx',
      '虛擬會議逐字稿.docx',
    ];
    const readItems = fileSpecs.map(f => makeReadItem(f));
    // 模擬：只有 PDF 和純文字會被 Extract，其他 Bypass
    // 在 v2.0 3-way Switch 設計下，Office 不打 Extract → textMap 對它們是空的
    const extractedItems = [
      makeExtractedItem('AI 生產力實戰全攻略.pdf', '提示詞工程基礎、AI 生產力提升、實戰工具集...'),
    ];
    // Mock AI 回應：簡化成所有 chunk 都成功
    // chunk size = 5（N < 30）→ 12/5 = 3 chunks
    // chunks: [pdf, 4×pptx], [LLM-pptx, 5×docx], [docx 6+7]
    let aiCallIdx = 0;
    const chunkResponses = [
      // Chunk 0: PDF + 4 PPTX
      [
        {category:'docs', newName:'20260506_教材_AI 生產力實戰全攻略'},
        {category:'presentations', newName:'20260506_簡報_中小企業AI實務01'},
        {category:'presentations', newName:'20260506_簡報_中小企業AI實務02'},
        {category:'presentations', newName:'20260506_簡報_中小企業AI實務03'},
        {category:'presentations', newName:'20260506_簡報_通用觀念LLM'},
      ],
      // Chunk 1: 5 DOCX
      [
        {category:'docs', newName:'20260506_教材_提示詞基礎01'},
        {category:'docs', newName:'20260506_教材_提示詞進階02'},
        {category:'docs', newName:'20260506_教材_提示詞公式03'},
        {category:'docs', newName:'20260506_教材_提示詞角色04'},
        {category:'docs', newName:'20260506_教材_提示詞優化05'},
      ],
      // Chunk 2: 2 DOCX
      [
        {category:'docs', newName:'20260506_教材_提示詞JSON格式06'},
        {category:'docs', newName:'20260506_紀錄_虛擬會議逐字稿'},
      ],
    ];
    const helpers = {
      httpRequest: async () => {
        const resp = chunkResponses[aiCallIdx++];
        return {
          candidates: [{
            content: {
              parts: [{ text: JSON.stringify(resp) }],
            },
          }],
        };
      },
    };
    return { items: extractedItems, allReadItems: readItems, helpers };
  })(),
  expect: (results) => {
    if (results.length !== 12) return `expected 12 results, got ${results.length}`;
    const bi = results[0].json._batchInfo;
    if (bi.inputCount !== 12) return `inputCount should be 12, got ${bi.inputCount}`;
    if (bi.outputCount !== 12) return `outputCount should be 12, got ${bi.outputCount}`;
    if (bi.dedupCount !== 0) return `expected no dedup, got ${bi.dedupCount}`;
    // 4 個 .pptx 都該到 presentations
    const pptxResults = results.filter(r => r.json.originalName.endsWith('.pptx'));
    const pptxInPresentations = pptxResults.filter(r => r.json.category === 'presentations').length;
    if (pptxInPresentations !== 4) return `expected 4 .pptx in presentations, got ${pptxInPresentations}`;
    return null;
  },
});

// Scenario 4: AI 失敗 → per-file rule fallback
scenarios.push({
  name: "N=3（AI 失敗，rule fallback）",
  ctx: (() => {
    const readItems = [
      makeReadItem('合約_NDA.pdf'),
      makeReadItem('Q3_報價單.xlsx'),
      makeReadItem('客戶提案_簡報.pptx'),
    ];
    const extractedItems = [
      makeExtractedItem('合約_NDA.pdf', '本合約由甲方與乙方簽訂'),
    ];
    const helpers = {
      httpRequest: async () => { throw new Error('Request failed with status code 429'); },
    };
    return { items: extractedItems, allReadItems: readItems, helpers };
  })(),
  expect: (results) => {
    if (results.length !== 3) return `expected 3 results, got ${results.length}`;
    const bi = results[0].json._batchInfo;
    if (bi.aiSucceeded !== 0) return 'aiSucceeded should be 0 (all failed)';
    if (bi.ruleFallback !== 3) return `ruleFallback should be 3, got ${bi.ruleFallback}`;
    // Rule-based 應該分對：
    // 合約_NDA.pdf → contracts
    // Q3_報價單.xlsx → invoices
    // 客戶提案_簡報.pptx → presentations
    const cats = results.map(r => r.json.category);
    if (cats[0] !== 'contracts') return `合約_NDA.pdf should be contracts, got ${cats[0]}`;
    if (cats[1] !== 'invoices') return `Q3_報價單.xlsx should be invoices, got ${cats[1]}`;
    if (cats[2] !== 'presentations') return `客戶提案_簡報.pptx should be presentations, got ${cats[2]}`;
    return null;
  },
});

// Scenario 5: 命名衝突 → dedup
scenarios.push({
  name: "N=3 同名（測 dedup）",
  ctx: (() => {
    const readItems = [
      makeReadItem('合約A.pdf'),
      makeReadItem('合約B.pdf'),
      makeReadItem('合約C.pdf'),
    ];
    const extractedItems = readItems.map(r => makeExtractedItem(r.json.fileName, '合約內容'));
    const aiResp = {
      candidates: [{
        content: {
          parts: [{
            text: JSON.stringify([
              { category: 'contracts', newName: '20260506_合約' }, // AI 故意給同名測 dedup
              { category: 'contracts', newName: '20260506_合約' },
              { category: 'contracts', newName: '20260506_合約' },
            ]),
          }],
        },
      }],
    };
    return makeContext({ readItems, extractedItems, mockAIResponse: aiResp });
  })(),
  expect: (results) => {
    if (results.length !== 3) return `expected 3 results, got ${results.length}`;
    const newNames = results.map(r => r.json.newName);
    const uniqueNames = new Set(newNames);
    if (uniqueNames.size !== 3) return `expected 3 unique names, got ${uniqueNames.size}: ${newNames.join(', ')}`;
    const bi = results[0].json._batchInfo;
    if (bi.dedupCount !== 2) return `expected dedupCount=2, got ${bi.dedupCount}`;
    return null;
  },
});

// ── 跑所有 scenarios ──
(async () => {
  let pass = 0;
  let fail = 0;
  for (const s of scenarios) {
    try {
      const results = await runJsCode(s.ctx);
      const err = s.expect(results);
      if (err) {
        console.log(`❌ ${s.name}: ${err}`);
        if (process.env.VERBOSE) {
          console.log('  Result sample:', JSON.stringify(results.slice(0, 3).map(r => r.json), null, 2));
        }
        fail++;
      } else {
        console.log(`✅ ${s.name}`);
        pass++;
      }
    } catch (e) {
      console.log(`❌ ${s.name}: 例外 — ${e.message}`);
      console.log(e.stack);
      fail++;
    }
  }
  console.log(`\n=== 通過 ${pass}/${scenarios.length} ===`);
  process.exit(fail > 0 ? 1 : 0);
})();
