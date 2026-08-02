#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';
import playwright from '/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js';

const { chromium } = playwright;
const here = path.dirname(fileURLToPath(import.meta.url));
const courseDir = path.resolve(here, '..');
const coursesDir = path.resolve(courseDir, '..');
const outDir = path.join(coursesDir, 'output', 'pdf', 'admin-ai-assistant');
const tmpDir = path.join(courseDir, 'tmp', 'pdfs', 'admin-ai-assistant');
const python = '/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const chapters = [
  { number: 1, file: 'CH1.html', title: '從 AI 工具到行政虛擬助理方案', slug: '從-AI-工具到行政虛擬助理方案' },
  { number: 2, file: 'CH2.html', title: '用 Gemini 處理會議紀錄', slug: '用-Gemini-處理會議紀錄' },
  { number: 3, file: 'CH3.html', title: 'Email、公文與行政通知撰寫', slug: 'Email-公文與行政通知撰寫' },
  { number: 4, file: 'CH4.html', title: '資料彙整與主管摘要', slug: '資料彙整與主管摘要' },
  { number: 5, file: 'CH5.html', title: '簡報製作：產出乾淨內容包', slug: '簡報製作-產出乾淨內容包' },
  { number: 6, file: 'CH6.html', title: '完整方案：把行政虛擬助理建成連結 NotebookLM 的 Gem', slug: '完整行政虛擬助理方案' },
];

const esc = (value) => value.replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const read = (file) => fs.readFileSync(path.join(courseDir, file), 'utf8');
const stylesOf = (html) => [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((match) => match[1]).join('\n');

function section(html, startPattern, endPattern, file) {
  const start = html.search(startPattern);
  const end = html.search(endPattern);
  if (start < 0 || end < 0 || end <= start) throw new Error(`無法定位正文：${file}`);
  return html.slice(start, end);
}

function answersOf(html) {
  const answers = [];
  const pattern = /<details\s+class="quiz-ans"[^>]*>([\s\S]*?)<\/details>/gi;
  for (const match of html.matchAll(pattern)) {
    const before = html.slice(0, match.index);
    const questions = [...before.matchAll(/<div\s+class="quiz-q"[^>]*>([\s\S]*?)<\/div>/gi)];
    const question = questions.at(-1)?.[1] ?? `題目 ${answers.length + 1}`;
    const answer = match[1].replace(/<summary[^>]*>[\s\S]*?<\/summary>/i, '').trim();
    answers.push({ question, answer });
  }
  return answers;
}

function cleanBody(body) {
  return body
    .replace(/<details\s+class="quiz-ans"[^>]*>[\s\S]*?<\/details>/gi, '<div class="print-answer-note">答案見本章末</div>')
    .replace(/<details(?![^>]*\bopen\b)([^>]*)>/gi, '<details open$1>')
    .replace(/<button\b[\s\S]*?<\/button>/gi, '')
    .replace(/<input\b[^>]*type=["'](?:radio|checkbox)["'][^>]*>/gi, '<span class="print-choice" aria-hidden="true">○</span>')
    .replace(/\sclass="([^"]*)\breveal\b([^"]*)"/gi, ' class="$1$2"');
}

const data = chapters.map((chapter) => {
  const html = read(chapter.file);
  const body = section(html, /<div\s+class="page-hero"[^>]*>/i, /<(?:div|nav)\s+class="nav-footer"[^>]*>/i, chapter.file);
  return { ...chapter, styles: stylesOf(html), body: cleanBody(body), answers: answersOf(html) };
});

const printCss = `
@page{size:A4;margin:16mm 16mm 18mm 18mm}
*{box-sizing:border-box!important}
html,body{background:#fff!important;color:#252422!important}
body{margin:0!important;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",Arial,sans-serif!important;font-size:10.2pt!important;line-height:1.68!important;-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
.topbar,.back-link,.nav-footer,.footer,#_gate,.skip-link,.copy-btn,.copy-row,.asset-actions,.dl-link,.toast,script,button,select{display:none!important}
.print-cover{min-height:245mm;display:flex;flex-direction:column;justify-content:center;break-after:page;padding:10mm 4mm}
.print-kicker{font-size:8.5pt;letter-spacing:.15em;color:#6f7778;margin-bottom:8mm}.print-cover h1{font-family:"Noto Serif TC","Songti TC",serif;font-size:27pt;line-height:1.3;margin:0 0 7mm;color:#252422}.print-cover h2{font-family:"Noto Serif TC","Songti TC",serif;font-size:16pt;line-height:1.45;margin:0 0 8mm;color:#527980}.print-cover p{font-size:10.5pt;color:#555b5c;line-height:1.8;margin:0 0 4mm;max-width:38em}.print-meta{margin-top:12mm;padding-top:5mm;border-top:1px solid #cfd4d4;font-size:8.5pt;color:#6f7778;line-height:1.8}
.print-source{font-size:7.4pt;color:#737979;text-align:right;border-bottom:1px solid #d7dada;padding-bottom:2.5mm;margin-bottom:6mm}
.page-hero,.lesson-section,.library-body{max-width:none!important;width:auto!important;margin-left:0!important;margin-right:0!important;padding-left:0!important;padding-right:0!important}
.page-hero{min-height:auto!important;padding-top:0!important;padding-bottom:7mm!important;margin-bottom:7mm!important;background:#fff!important;border-bottom:2px solid #3d4f52!important}.lesson-title{font-size:22pt!important;line-height:1.3!important;max-width:none!important;margin:0 0 4mm!important;color:#171817!important;break-after:avoid}.lesson-tagline,.hero-desc{font-size:10.2pt!important;line-height:1.75!important;color:#484d4d!important;max-width:none!important}.hero-eyebrow,.section-eyebrow,.outcomes-label{letter-spacing:.1em!important;color:#527980!important}
.lesson-section{padding-top:0!important;padding-bottom:0!important;margin-bottom:8mm!important;break-inside:auto}.section-heading{font-size:15pt!important;line-height:1.4!important;margin:0 0 4mm!important;color:#1d1f1e!important;break-after:avoid}.section-rule{margin:8mm 0!important;border:0!important;border-top:1px solid #d7dada!important;opacity:1!important;transform:none!important}.reveal,[class*="reveal"]{opacity:1!important;transform:none!important;visibility:visible!important;animation:none!important}
p,.body-text,li{orphans:3;widows:3}.body-text{font-size:10.2pt!important;line-height:1.72!important;color:#323534!important}h2,h3,h4{break-after:avoid}
.intro-band,.callout,.scenario-row,.tool-card,.expected-output,.practice,.prompt-card,.quiz-item,.step-block,.spec-card,.output-card{border:1px solid #c9cecd!important;background:#f6f8f7!important;color:#252422!important;box-shadow:none!important}.card-prompt,pre,.code-block,.expected-output{font-size:8.8pt!important;line-height:1.58!important;white-space:pre-wrap!important;overflow-wrap:anywhere!important;max-height:none!important;overflow:visible!important;background:#f8f7f3!important;color:#252422!important;border:1px solid #c9cecd!important;break-inside:auto!important}
table{width:100%!important;border-collapse:collapse!important;font-size:8.5pt!important;break-inside:auto}tr{break-inside:avoid}th,td{border:1px solid #aaaead!important;padding:5px 6px!important;vertical-align:top!important;background:#fff!important;color:#252422!important}a{color:#252422!important;text-decoration:none!important}img,svg,canvas{max-width:100%!important;height:auto!important;break-inside:avoid}
details{display:block!important;break-inside:auto!important}details>summary{font-weight:700!important;color:#333!important;list-style:none!important;margin-bottom:2mm;break-after:avoid}details>summary::-webkit-details-marker{display:none!important}.prompt-group{break-inside:auto!important}.prompt-cards{display:block!important}.prompt-card{break-inside:auto!important;margin-bottom:5mm!important}.print-choice{display:inline-block;margin-right:2mm;color:#666}.quiz-opt,.mini-prac-step{break-inside:avoid}.print-answer-note{font-size:8.5pt;color:#617477;margin-top:3mm}.answer-section{break-before:page}.answer-section h2,.asset-appendix h2{font-family:"Noto Serif TC","Songti TC",serif;font-size:20pt;margin:0 0 7mm}.answer-item{padding:5mm 0;border-bottom:1px solid #d7dada;break-inside:avoid}.answer-q{font-weight:700;margin-bottom:2mm}.answer-a{color:#343837}.asset-appendix{break-before:page}.library-body{padding-top:0!important}.group-header{font-size:14pt!important}
`;

function cover(title, subtitle, meta) {
  return `<section class="print-cover"><div class="print-kicker">學員版 · PRINT / NOTEBOOKLM READY</div><h1>行政 AI 虛擬助理實戰</h1><h2>${esc(title)}</h2><p>${esc(subtitle)}</p><div class="print-meta">弄一下工作室｜學員版<br>產出日期：${new Date().toISOString().slice(0, 10)}<br>${esc(meta)}</div></section>`;
}

function answerSection(chapter) {
  return `<section class="answer-section"><h2>CH${chapter.number}｜本章答案</h2>${chapter.answers.map((item, index) => `<div class="answer-item"><div class="answer-q">Q${index + 1} ${item.question}</div><div class="answer-a">${item.answer}</div></div>`).join('')}</section>`;
}

function htmlDoc(title, styles, body) {
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8"><title>${esc(title)}</title><style>${styles}\n${printCss}</style></head><body>${body}</body></html>`;
}

async function render(page, htmlPath, pdfPath, footerLabel) {
  await page.goto(`file://${htmlPath}`, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: pdfPath, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: `<div style="width:100%;font-family:Arial,sans-serif;font-size:7pt;color:#737979;padding:0 16mm 0 18mm;display:flex;justify-content:space-between"><span>${esc(footerLabel)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`, margin: { top: '0', right: '0', bottom: '0', left: '0' } });
}

function runPost(args) {
  const result = spawnSync(python, [path.join(here, 'postprocess-print-pdfs.py'), ...args], { encoding: 'utf8' });
  if (result.status !== 0) throw new Error(result.stderr || result.stdout || 'PDF 後處理失敗');
}

async function main() {
  fs.mkdirSync(outDir, { recursive: true });
  fs.mkdirSync(tmpDir, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath: chrome });
  const page = await browser.newPage({ viewport: { width: 1240, height: 1754 } });
  const outputs = [];

  for (const chapter of data) {
    const code = String(chapter.number).padStart(2, '0');
    const htmlPath = path.join(tmpDir, `ADMIN-AI-CH${code}.html`);
    const pdfPath = path.join(outDir, `ADMIN-AI-CH${code}-${chapter.slug}.pdf`);
    const body = `${cover(`CH${chapter.number}｜${chapter.title}`, '保留案例、提示詞、操作步驟與練習；答案集中於本章末尾。', `來源：admin-ai-assistant/${chapter.file}`)}<article><div class="print-source">來源：admin-ai-assistant/${chapter.file}</div>${chapter.body}</article>${answerSection(chapter)}`;
    fs.writeFileSync(htmlPath, htmlDoc(`CH${chapter.number} ${chapter.title}｜學員版`, chapter.styles, body), 'utf8');
    await render(page, htmlPath, pdfPath, `行政 AI 虛擬助理實戰｜CH${code}`);
    runPost(['document', pdfPath, `CH${chapter.number}｜${chapter.title}`, chapter.file]);
    outputs.push({ type: 'chapter', chapter: chapter.number, title: chapter.title, source: chapter.file, file: path.basename(pdfPath), answerCount: chapter.answers.length });
    console.log(`built ${pdfPath}`);
  }

  const libraryHtml = read('prompt-library.html');
  const libraryBody = cleanBody(section(libraryHtml, /<div\s+class="page-hero"[^>]*>/i, /<(?:div|nav)\s+class="nav-footer"[^>]*>/i, 'prompt-library.html'));
  const appendixHtml = path.join(tmpDir, 'ADMIN-AI-APPENDIX.html');
  const appendixPdf = path.join(tmpDir, 'ADMIN-AI-APPENDIX.pdf');
  fs.writeFileSync(appendixHtml, htmlDoc('課程資產庫附錄', stylesOf(libraryHtml), `<section class="asset-appendix"><div class="print-source">來源：admin-ai-assistant/prompt-library.html</div>${libraryBody}</section>`), 'utf8');
  await render(page, appendixHtml, appendixPdf, '行政 AI 虛擬助理實戰｜課程資產庫');
  runPost(['document', appendixPdf, '課程資產庫附錄', 'prompt-library.html']);

  const coverHtml = path.join(tmpDir, 'ADMIN-AI-FULL-COVER.html');
  const coverPdf = path.join(tmpDir, 'ADMIN-AI-FULL-COVER.pdf');
  fs.writeFileSync(coverHtml, htmlDoc('行政 AI 虛擬助理實戰｜學員版', '', cover('全課合併版', '6 章完整學習內容、章末答案與課程資產庫；可列印，也可匯入 NotebookLM 作為課程基礎資料。', '6 章｜課程資產庫附錄｜可搜尋文字')), 'utf8');
  await render(page, coverHtml, coverPdf, '行政 AI 虛擬助理實戰｜全課版');
  runPost(['document', coverPdf, '行政 AI 虛擬助理實戰｜全課版', 'course-cover']);

  const fullPdf = path.join(outDir, 'ADMIN-AI-FULL-行政AI虛擬助理實戰-學員版.pdf');
  runPost(['full', fullPdf, coverPdf, JSON.stringify(outputs.map((item) => ({ ...item, path: path.join(outDir, item.file) }))), appendixPdf]);
  outputs.push({ type: 'full', title: '行政 AI 虛擬助理實戰｜學員版', file: path.basename(fullPdf), sources: [...chapters.map((item) => item.file), 'prompt-library.html'] });
  await browser.close();

  const manifest = { course: 'admin-ai-assistant', generated: new Date().toISOString(), chapterCount: 6, sourceCount: 7, outputs };
  fs.writeFileSync(path.join(outDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  const readme = `# 行政 AI 虛擬助理實戰｜學員版 PDF\n\n產出日期：${new Date().toISOString().slice(0, 10)}\n\n## NotebookLM 建議\n\n- 分章查詢：匯入 6 份 CH 分冊，適合依課程進度建立來源。\n- 全課查詢：只匯入全課合併版，適合跨章統整與建立行政 AI 顧問。\n- 分冊與合併版內容重複，請勿同時匯入，避免 NotebookLM 重複引用。\n- 提問時指定章節與任務，例如：「依 CH3，整理行政通知提示詞的必要欄位。」\n\n## 檔案\n\n${outputs.map((item) => `- \`${item.file}\`：${item.type === 'full' ? '全課合併版（含資產庫附錄）' : `CH${item.chapter}｜${item.title}`}`).join('\n')}\n\n## 來源\n\n${chapters.map((item) => `- \`${item.file}\`：CH${item.number}｜${item.title}`).join('\n')}\n- \`prompt-library.html\`：課程資產庫附錄\n`;
  fs.writeFileSync(path.join(outDir, 'README.md'), readme, 'utf8');
  console.log(`built ${fullPdf}`);
  console.log(`built ${path.join(outDir, 'README.md')}`);
  console.log(`built ${path.join(outDir, 'manifest.json')}`);
}

main().catch((error) => { console.error(error); process.exit(1); });
