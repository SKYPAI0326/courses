const fs = require('fs');
const path = require('path');
const { chromium } = require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const root = path.resolve(__dirname, '..');
const repo = path.resolve(root, '..');
const outDir = path.join(repo, 'output', 'pdf');
const lessons = [
  'CH0.html',
  'CH1-1.html',
  'CH1-2.html',
  'CH1-3.html',
  'CH1-4.html',
  'CH2-1.html',
];

const outHtml = path.join(outDir, 'gemini-notebooklm-workshop-print.html');
const outPdf = path.join(outDir, 'gemini-notebooklm-workshop-handout-print.pdf');

function between(source, startRe, endRe) {
  const start = source.search(startRe);
  if (start < 0) return '';
  const openEnd = source.indexOf('>', start);
  const end = source.search(endRe);
  if (openEnd < 0 || end < 0 || end <= openEnd) return '';
  return source.slice(openEnd + 1, end);
}

function extractStyles(source) {
  return [...source.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => m[1]).join('\n');
}

function cleanMain(main) {
  return main
    .replace(/<a href="index\.html" class="back-link">[\s\S]*?<\/a>/g, '')
    .replace(/<div class="nav-footer">[\s\S]*?<\/div>\s*$/g, '')
    .replace(/<details(?![^>]*\bopen\b)([^>]*)>/g, '<details open$1>')
    .replace(/\sclass="([^"]*)\breveal\b([^"]*)"/g, ' class="$1$2"')
    .replace(/\sclass="([^"]*)\bin\b([^"]*)"/g, ' class="$1$2"');
}

const styleParts = [];
const lessonParts = lessons.map((file, index) => {
  const fullPath = path.join(root, file);
  const html = fs.readFileSync(fullPath, 'utf8');
  const title = (html.match(/<title>([\s\S]*?)<\/title>/i) || [null, file])[1]
    .replace(/\s*｜[\s\S]*$/, '')
    .trim();
  styleParts.push(extractStyles(html));
  const main = cleanMain(between(html, /<main\b[^>]*>/i, /<\/main>/i));
  return `<article class="print-lesson${index === 0 ? ' first' : ''}" data-source="${file}">
<div class="print-source">${file}</div>
${main}
</article>`;
});

const printCss = `
@page{size:A4;margin:14mm 13mm 16mm}
*{box-sizing:border-box!important}
html,body{background:#fff!important;color:#222!important}
body{margin:0!important;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",Arial,sans-serif!important;font-size:10.4pt!important;line-height:1.58!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.topbar,.progress-strip,.skip-link,#_gate,.nav-footer,.footer,.back-link,script{display:none!important}
.print-cover{min-height:238mm;display:flex;flex-direction:column;justify-content:center;border-bottom:0;break-after:page}
.print-kicker{font-size:9pt;letter-spacing:.16em;text-transform:uppercase;color:#666;margin-bottom:10mm}
.print-cover h1{font-family:"Noto Serif TC","Songti TC",serif;font-size:28pt;line-height:1.25;margin:0 0 8mm;color:#222;max-width:18ch}
.print-cover p{font-size:11pt;color:#555;line-height:1.8;margin:0;max-width:36em}
.print-meta{margin-top:18mm;font-size:8.5pt;color:#777;line-height:1.8}
.print-lesson{break-before:page}
.print-lesson.first{break-before:auto}
.print-source{font-size:7.6pt;color:#777;text-align:right;border-bottom:1px solid #ddd;padding-bottom:3mm;margin-bottom:7mm}
main,.page-hero,.lesson-section,.nav-footer,.footer{max-width:none!important;width:auto!important}
.page-hero{min-height:auto!important;padding:0 0 8mm!important;margin:0 0 8mm!important;background:#fff!important;border-bottom:2px solid #222!important}
.hero-eyebrow,.section-eyebrow,.outcomes-label{letter-spacing:.12em!important;color:#666!important}
.lesson-title{font-size:22pt!important;line-height:1.25!important;max-width:none!important;margin:0 0 5mm!important;color:#111!important}
.lesson-tagline{font-size:10.2pt!important;line-height:1.75!important;color:#444!important;max-width:none!important}
.outcomes{margin-top:7mm!important;padding:5mm!important;border:1px solid #ccc!important;background:#fafafa!important;break-inside:avoid}
.lesson-section{padding:0!important;margin:0 0 8mm!important;break-inside:auto}
.section-heading{font-size:15pt!important;line-height:1.35!important;margin:0 0 4mm!important;color:#111!important;break-after:avoid}
.section-rule{margin:8mm 0!important;border:0!important;border-top:1px solid #d7d7d7!important;opacity:1!important}
p,.body-text,li{orphans:3;widows:3}
.body-text{font-size:10.2pt!important;line-height:1.72!important;color:#333!important}
.intro-band,.callout,.demo-takeaway,.verify-card,.quiz-item,.concept-card,.scenario-card,.tool-card,.pitfall-block,.expected-output{border:1px solid #ccc!important;background:#fafafa!important;box-shadow:none!important;break-inside:avoid}
.dialog-box,.expected-output{font-size:9.2pt!important;line-height:1.58!important;white-space:pre-wrap!important;overflow-wrap:anywhere!important;background:#fff!important}
.dialog-label,.expected-label,.intro-label,.callout-icon{color:#333!important}
table{width:100%!important;border-collapse:collapse!important;font-size:8.6pt!important;break-inside:auto}
tr{break-inside:avoid}
th,td{border:1px solid #bbb!important;padding:5px 6px!important;vertical-align:top!important;background:#fff!important;color:#222!important}
pre,code{white-space:pre-wrap!important;overflow-wrap:anywhere!important}
a{color:#222!important;text-decoration:none!important}
details{display:block!important}
details>summary{font-weight:700!important;color:#333!important;list-style:none!important;margin-bottom:2mm}
details>summary::-webkit-details-marker{display:none!important}
input[type="radio"],input[type="checkbox"]{accent-color:#555!important}
.quiz-opt{break-inside:avoid;background:#fff!important;border-color:#ccc!important}
.step-block,.asset-row,.verify-item,.pitfall-row{break-inside:avoid}
`;

const html = `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>Gemini × NotebookLM 跨部門 AI 工作坊｜印刷版講義</title>
<style>
${styleParts.join('\n')}
${printCss}
</style>
</head>
<body>
<section class="print-cover">
  <div class="print-kicker">Printable Handout</div>
  <h1>Gemini × NotebookLM 跨部門 AI 工作坊</h1>
  <p>印刷版講義。互動區塊與檢核答案已展開，版面改為 A4 列印樣式，方便雙面列印與課堂紙本使用。</p>
  <div class="print-meta">來源：gemini-notebooklm-workshop<br>產出：${new Date().toISOString().slice(0, 10)}<br>範圍：${lessons.join(' / ')}</div>
</section>
${lessonParts.join('\n')}
</body>
</html>`;

async function main() {
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(outHtml, html);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1240, height: 1754 } });
  await page.goto(`file://${outHtml}`, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: outPdf,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:7pt;color:#777;padding:0 13mm;text-align:right;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  await browser.close();

  console.log(outHtml);
  console.log(outPdf);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
