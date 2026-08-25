const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const courseDir = path.resolve(__dirname, '..');
const assetsDir = path.join(courseDir, 'assets');
const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const publicAssetBase = 'https://skypai0326.github.io/courses/courses/simple-ai/assets/';
const publicEnvironmentContract = 'https://skypai0326.github.io/courses/_outlines/simple-ai.environment.md';
const mode = process.argv[2] || 'handbook';
const draft = process.argv.includes('--draft');

function assertAuthorizedBrowserEnvironment() {
  if (process.env.CODEX_SANDBOX === 'seatbelt') {
    throw new Error([
      'PDF rendering blocked: Chrome cannot start inside the Codex seatbelt sandbox.',
      'Run: ./simple-ai/_tools/build-deliverables-authorized.sh all',
      'The authorized host process is required for macOS Mach-port access.',
    ].join('\n'));
  }
}

const chapters = [
  ['CH1-1.html', '第一章｜選對工具，設定你的 AI 助理', '你是一位在家製作手工皂的老闆，每次開新對話都要重講自己的行業與語氣。本章完成一份能反覆貼上的 AI 助理設定。', [1, 2, 3, 5, 8, 11]],
  ['CH1-2.html', '第二章｜把會議變成摘要與待辦', '你剛結束一場包裝改版會議，原始對話裡混著數量、交期與誰要負責。本章把完整逐字稿整理成可追蹤的三欄待辦。', [2, 5, 8]],
  ['CH1-3.html', '第三章｜拍照萃取資料，再寫成可寄 Email', '供應商傳來一張報價單，你必須先把數字整理正確，再決定用什麼語氣回信。本章的完成物是一張核對過的表格與一封可寄 Email。', [1, 2, 3, 6, 10]],
  ['CH1-4.html', '第四章｜資安紅線與發佈檢查', '一段讀起來很順的 AI 草稿，可能同時藏著個資、無依據數字與不符合自家語氣的承諾。本章練習在送出前把問題攔下。', [1, 2, 3, 4, 5]],
  ['CH2-1.html', '第五章｜建立 NotebookLM 品牌知識庫', '咖啡館老闆不需要「一般咖啡館」的答案，而要 AI 先讀自家官網、菜單與評論，再把草稿帶回來源查核。本章完成一份能回指來源的品牌摘要與雙向查核貼文。', [3, 5, 6]],
  ['CH2-2.html', '第六章｜從三個角度選出品牌定位', '品牌摘要已完成，下一步不是請 AI 決定答案，而是比較功能、情感、對立三種角度，留下老闆真的做得到的一句定位。', [1, 2, 3, 5, 8]],
  ['CH2-3.html', '第七章｜建立一週社群內容產線', '你已經有品牌定位，現在要把它變成一週七則貼文骨架、A/B 標題與一支 30 秒短影音腳本，同時保持每則內容像同一家店。', [1, 2, 3, 5, 6]],
  ['CH2-4.html', '第八章｜FAQ、檢查清單與結訓行動', '客人反覆詢問停車、訂位與寵物規則。本章一次建立 15 則 FAQ，再用事實、個資與品牌語氣三關完成發佈前修正。', [1, 2, 3, 4, 8, 14]],
];

const workflows = [
  ['WF-01', '新產品上市', '產品規格、價格、上市日', 'ChatGPT → 人工核對 → Gemini', '定位句、貼文、Email、短影音腳本', '價格與日期逐項對照原資料', '配額不足時先做定位與 Email，其餘隔日完成'],
  ['WF-02', '週末社群內容備稿', '本週事件、主打品、常見問題', 'MK-01 → MK-02 → 發佈三問', '七則骨架與兩組標題', '每則只說一件事且符合品牌定位', '先完成三則最重要貼文'],
  ['WF-03', '客戶訪談變行銷素材', '逐字稿與受訪同意範圍', 'EF-01 → NotebookLM → MK-03', '重點摘要、客戶原話、短影音腳本', '引言不得超出同意範圍', '無法上傳音檔時貼文字逐字稿'],
  ['WF-04', '收到客訴緊急處理', '客訴原文、訂單事實、可補救範圍', 'EF-05 → EF-04 → 人工核准', '問題摘要與可寄回覆', '不承諾做不到的退款或期限', '先用中性短版回覆已收到'],
  ['WF-05', '決定要不要接新案子', '需求、預算、時程、現有工作量', 'EF-05 → TK-01 → 決策表', '接案／婉拒理由與回信', '四項限制都有真實資料', '資料不足先列待確認問題'],
  ['WF-06', '年度或季度盤整', '訂單摘要、客戶回饋、重大事件', 'NotebookLM → Gemini', '趨勢、問題、下季三項行動', '每個結論能指回來源', '只先上傳一季的去識別資料'],
  ['WF-07', '競品快速偵察', '三個公開競品頁面與觀察日期', '人工蒐集 → NotebookLM → TK-02', '差異表與定位調整建議', '不把推測寫成競品事實', '無法匯入網頁時貼公開文字摘錄'],
  ['WF-08', '長文一稿多用', '一篇已核准長文', 'MK-04 → MK-02 → MK-03', '貼文、標題、短影音腳本', '核心主張與原文一致', '先轉一種格式，確認後再擴寫'],
  ['WF-09', '每週 Email 電子報', '本週消息、單一 CTA、截止日', 'MK-01 → EF-04 → 發佈三問', '主旨 A/B 與完整 Email', 'CTA、日期與連結正確', '連結不確定時先存草稿不寄送'],
  ['WF-10', '年度報告給合作方', '季度資料、里程碑、風險與下步', 'NotebookLM → Gemini → NotebookLM 查核', '有來源的年度摘要與合作提案', '數字與里程碑逐項可追', '資料太多時按季度分批加入'],
];

const completeFaqOutput = `<div class="complete-example"><p class="body-text"><strong>示範政策卡（AI 只能依這張卡回答）</strong>：店內無專屬車位；民生公園地下停車場步行 4 分鐘。平日現場候位；4 人以上可提前一日 IG 私訊。提供低咖啡因手沖與無咖啡因洋甘菊茶。Wifi 名稱為「松山咖啡」，密碼保留為 [密碼]。店內飲品不外送；咖啡豆可至線上商店下單。</p><p class="body-text"><strong>完整預期輸出：5 題 × 3 語氣 = 15 則</strong></p><div class="code-block">
【問題 1：附近有沒有停車位？】
A. 簡潔精準：店內無專屬車位；民生公園地下停車場步行約 4 分鐘，建議先預留停車時間。
B. 溫暖親切：我們沒有專屬車位，最近的是民生公園地下停車場，走過來約 4 分鐘喔。
C. 輕鬆活潑：車子先去民生公園地下停車場休息，走 4 分鐘就到我們店啦。

【問題 2：可以訂位嗎？】
A. 簡潔精準：平日採現場候位；4 人以上可提前一日透過 IG 私訊，我們會依座位狀況回覆。
B. 溫暖親切：平日直接來就可以；如果是 4 人以上，前一天 IG 私訊我們，會幫你看看座位。
C. 輕鬆活潑：一兩個人直接來，4 人以上先私訊喊一聲，我們幫桌子做好心理準備。

【問題 3：有低咖啡因或無咖啡因選項嗎？】
A. 簡潔精準：店內提供低咖啡因手沖；無咖啡因飲品可選洋甘菊茶，品項以現場菜單為準。
B. 溫暖親切：想少一點咖啡因，可以選低咖啡因手沖；完全不喝咖啡因，也有洋甘菊茶。
C. 輕鬆活潑：今天想早點睡？選低咖啡因手沖；想完全放過咖啡因，就交給洋甘菊茶。

【問題 4：Wifi 密碼是什麼？】
A. 簡潔精準：Wifi 名稱為「松山咖啡」，密碼是 [密碼]；連線異常請洽櫃台。
B. 溫暖親切：連「松山咖啡」，密碼是 [密碼]。連不上跟我們說，會幫你確認。
C. 輕鬆活潑：Wifi 找「松山咖啡」，密碼 [密碼]；連不上別跟手機吵，來找我們。

【問題 5：可以外送嗎？】
A. 簡潔精準：目前店內飲品不提供外送；咖啡豆可由線上商店下單寄送。
B. 溫暖親切：飲品目前沒有外送，不過咖啡豆可以在線上商店下單，我們會幫你寄出。
C. 輕鬆活潑：拿鐵還沒學會自己出門，但咖啡豆可以從線上商店搭宅配去找你。
</div><p class="body-text"><strong>判讀與修復</strong>：十五則只能使用政策卡資訊。若 AI 自行增加停車優惠、訂位保證、外送平台或療效，直接刪除並回覆：「只根據政策卡重寫，沒有寫到的服務請回答目前未提供。」</p></div>`;

function replaceIncompleteFaq(html) {
  const replaced = html.replace(/<p class="body-text" style="margin-top:28px[\s\S]*?<div class="copy-row"><\/div>/, completeFaqOutput);
  if (replaced === html) throw new Error('Incomplete FAQ example was not replaced');
  return replaced;
}

function extractAll(source, re) {
  return [...source.matchAll(re)].map((match) => match[1]).join('\n');
}

function extractCuratedMain(source, selectedIndexes) {
  const match = source.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  if (!match) throw new Error('Missing <main>');
  const main = match[1];
  const firstSection = main.search(/<section\b[^>]*class="[^"]*lesson-section/i);
  if (firstSection < 0) throw new Error('Missing lesson sections');
  const sections = main.match(/<section\b[^>]*class="[^"]*lesson-section[^"]*"[^>]*>[\s\S]*?<\/section>/gi) || [];
  const missing = selectedIndexes.filter((index) => !sections[index]);
  if (missing.length) throw new Error(`Missing section indexes: ${missing.join(', ')}`);
  return selectedIndexes.map((index) => sections[index]).join('\n')
    .replace(/<a\b[^>]*class="[^"]*back-link[^"]*"[^>]*>[\s\S]*?<\/a>/gi, '')
    .replace(/<div\b[^>]*class="[^"]*nav-footer[^"]*"[^>]*>[\s\S]*?<\/div>\s*$/gi, '')
    .replace(/<button\b[^>]*>[\s\S]*?<\/button>/gi, '')
    .replace(/<details(?![^>]*\bopen\b)([^>]*)>/gi, '<details open$1>')
    .replace(/\sclass="([^"]*)\breveal\b([^"]*)"/gi, ' class="$1$2"');
}

function handbookHtml() {
  const pageSources = chapters.map(([file]) => fs.readFileSync(path.join(courseDir, file), 'utf8'));
  const inheritedStyles = pageSources
    .map((source) => extractAll(source, /<style[^>]*>([\s\S]*?)<\/style>/gi))
    .join('\n')
    .replace(/box-shadow\s*:[^;}{]+;?/gi, '');
  const chapterBodies = chapters.map(([file, title, situation, selectedIndexes], index) => {
    let body = extractCuratedMain(pageSources[index], selectedIndexes);
    body = body.replace('NotebookLM 只有網頁版，把 <code>notebooklm.google.com</code> 加入手機主畫面當 App 用就好。', 'NotebookLM／Gemini Notebook 的手機入口依裝置與地區而異；若未看到官方 App，改用手機瀏覽器開官方 Notebook 頁面即可。');
    body = body.replace(/\sloading="lazy"/g, '');
    body = body.replace(/href="assets\//g, `href="${publicAssetBase}`);
    body = body.replace(/href="\.\.\/\.\/_outlines\/simple-ai\.environment\.md"/g, `href="${publicEnvironmentContract}"`);
    if (file === 'CH2-4.html') body = replaceIncompleteFaq(body);
    return `
<article class="print-chapter" data-source="${file}">
  <header class="print-chapter-cover">
    <div class="print-kicker">${String(index + 1).padStart(2, '0')} / 08</div>
    <h1>${title}</h1>
    <p>${situation}</p>
  </header>
  ${body}
</article>`;
  }).join('\n');

  const workflowBodies = workflows.map(([code, title, input, pathText, artifact, check, fallback]) => `<article class="workflow-card"><div class="workflow-code">${code}</div><h2>${title}</h2><dl><dt>起始素材</dt><dd>${input}</dd><dt>工具順序</dt><dd>${pathText}</dd><dt>完成物</dt><dd>${artifact}</dd><dt>人工檢查</dt><dd>${check}</dd><dt>免費備援</dt><dd>${fallback}</dd></dl></article>`).join('\n');
  const printCss = `
@page{size:A4;margin:8mm 9mm 10mm}
*{box-sizing:border-box!important}
html,body{background:#fff!important;color:#252421!important}
body{margin:0!important;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif!important;font-size:8.45pt!important;line-height:1.48!important;-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
#_gate,.topbar,.progress-strip,.skip-link,.back-link,.nav-footer,.footer,.copy-btn,.copy-row,button,script{display:none!important}
.print-book-cover{height:260mm;display:flex;flex-direction:column;justify-content:center;break-after:page;border-top:4mm solid #5a7a5a;padding:18mm 12mm}
.print-book-cover h1{font-family:"Shippori Mincho","Noto Serif TC",serif;font-size:29pt!important;line-height:1.32!important;max-width:15ch;margin:0 0 10mm!important}
.print-book-cover p{font-size:11pt!important;line-height:1.8!important;max-width:35em;color:#555!important}
.print-book-meta{margin-top:18mm;font-size:8.5pt;color:#777;line-height:1.8}
.print-contents{break-after:page;padding:12mm 4mm}
.print-contents h2{font-size:22pt!important;margin:0 0 10mm!important}
.print-contents ol{columns:2;column-gap:12mm;padding-left:6mm}
.print-contents li{break-inside:avoid;margin:0 0 5mm;line-height:1.6}
.print-chapter{break-before:page}
.print-chapter-cover{break-after:avoid;display:block;border-left:3mm solid #5a7a5a;padding:5mm 6mm;margin-bottom:7mm;background:#f4f3ef}
.print-chapter-cover h1{font-family:"Shippori Mincho","Noto Serif TC",serif;font-size:21pt!important;line-height:1.35!important;max-width:none;margin:2mm 0 3mm!important}
.print-chapter-cover p{font-size:8.5pt!important;line-height:1.65!important;color:#666!important;max-width:none;margin:0!important}
.print-kicker{font-size:8pt;letter-spacing:.18em;color:#5a7a5a;text-transform:uppercase}
.page-hero,.lesson-hero{min-height:auto!important;padding:0 0 6mm!important;margin:0 0 7mm!important;max-width:none!important;background:#fff!important;border-bottom:1px solid #aaa!important}
.lesson-body,.tool-wrap,main{max-width:none!important;width:auto!important;padding:0!important;margin:0!important}
.lesson-title{font-size:19pt!important;line-height:1.3!important;margin:0 0 4mm!important;max-width:none!important}
.lesson-tagline{font-size:9pt!important;line-height:1.65!important;max-width:none!important}
.outcomes{padding:4mm!important;margin:5mm 0!important;break-inside:avoid;background:#f4f3ef!important;border:1px solid #ccc!important}
.lesson-section{padding:0!important;margin:0 0 4mm!important;max-width:none!important;break-inside:auto!important;opacity:1!important;transform:none!important}
.section-heading{font-size:13.5pt!important;line-height:1.38!important;margin:0 0 3mm!important;break-after:avoid!important}
.section-eyebrow{font-size:7.5pt!important;margin-top:3mm!important;break-after:avoid!important}
p,.body-text,li{font-size:8.45pt!important;line-height:1.48!important;orphans:3;widows:3}
.print-chapter[data-source="CH2-1.html"] p,.print-chapter[data-source="CH2-1.html"] .body-text,.print-chapter[data-source="CH2-1.html"] li{font-size:8.2pt!important;line-height:1.42!important}
.print-chapter[data-source="CH2-1.html"] pre,.print-chapter[data-source="CH2-1.html"] .code-block{font-size:7.2pt!important;line-height:1.4!important}
h2,h3,h4{break-after:avoid!important}
.tool-card,.concept-card,.callout,.quiz-item,.scenario-row,.step-block,.output-row,.challenge-card,.verify-card,.intro-band{break-inside:avoid!important}
.repair-table{break-inside:avoid!important}
.tool-grid,.concept-grid,.scenario-grid,.steps-wrap,.material-block,.output-fold,details{break-inside:auto!important}
details{display:block!important}
details>summary{list-style:none!important;font-weight:700!important}
details>summary::-webkit-details-marker{display:none!important}
pre,.code-block,.ai-prompt,.fill-template{font-size:7.55pt!important;line-height:1.5!important;white-space:pre-wrap!important;overflow-wrap:anywhere!important;background:#f1f0ec!important;color:#171717!important;border:1px solid #ccc!important;padding:3mm!important;break-inside:auto!important}
table{width:100%!important;border-collapse:collapse!important;font-size:7.6pt!important;break-inside:auto!important}
tr{break-inside:avoid!important}th,td{border:1px solid #bbb!important;padding:1.5mm!important;vertical-align:top!important;background:#fff!important;color:#222!important}
a{color:inherit!important;text-decoration:none!important}
.workflow-appendix{break-before:page}
.workflow-title{break-after:avoid;border-left:3mm solid #b5703a;padding:5mm 6mm;margin-bottom:7mm;background:#f7f2ed}
.workflow-title h1{font-size:21pt!important;line-height:1.35!important;margin:2mm 0 3mm!important}
.workflow-intro{font-size:9pt!important;line-height:1.7!important;color:#555!important;max-width:none;margin:0!important}
.workflow-grid{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.workflow-card{break-inside:avoid!important;border:1px solid #bbb;padding:4mm;background:#faf9f6}
.workflow-code{font-size:7.5pt;letter-spacing:.12em;color:#5a7a5a;font-weight:700}
.workflow-card h2{font-size:13pt!important;margin:1.5mm 0 3mm!important}
.workflow-card dl{margin:0;display:grid;grid-template-columns:18mm 1fr;gap:1.5mm 2mm;font-size:8.2pt;line-height:1.5}
.workflow-card dt{font-weight:700;color:#555}.workflow-card dd{margin:0}
`;

  return `<!doctype html>
<html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>創業 AI 實戰手冊｜弄一下工作室</title><style>${inheritedStyles}\n${printCss}</style></head>
<body>
<section class="print-book-cover"><div class="print-kicker">完整學員手冊</div><h1>創業 AI 實戰手冊</h1><p>手機免費版的三小時入門體驗。從會議、拍照與 Email，到品牌知識庫、社群內容與 FAQ，把每天重複的小事變成可以反覆使用的工作路徑。</p><div class="print-book-meta">弄一下工作室<br>版本：2026-08-25<br>工具：ChatGPT・Gemini・NotebookLM</div></section>
<section class="print-contents"><h2>手冊目錄</h2><ol>${chapters.map(([, title]) => `<li>${title}</li>`).join('')}<li>附錄｜十條工作流應用路徑</li></ol><p>使用方式：第一次照章節順序完成；第二次直接翻到你眼前的任務。每章都附起始素材、完整 Prompt、預期輸出、檢查與卡關修復。</p><p>課前先看<a href="${publicEnvironmentContract}">環境契約與課前檢查表</a>；課程結訓先保存一條工作流路徑，再選課後延伸。</p></section>
${chapterBodies}
<section class="workflow-appendix"><header class="workflow-title"><div class="print-kicker">Appendix</div><h1>十條工作流應用路徑</h1><p class="workflow-intro">每條路徑都從你已完成的章節產物出發。不要一次跑完十條；先選現在最常重複的一件事，完成、檢查、存成自己的版本。</p></header><div class="workflow-grid">${workflowBodies}</div></section>
</body></html>`;
}

function pageCount(pdfPath) {
  const output = execFileSync('pdfinfo', [pdfPath], { encoding: 'utf8' });
  const match = output.match(/^Pages:\s+(\d+)/m);
  if (!match) throw new Error('Unable to read PDF page count');
  return Number(match[1]);
}

const quickPromptCodes = [
  ['EF-08', 'AI 助理設定', '設定一次，之後每次對話先貼上同一份背景。', '手機備忘錄中的個人化 AI 助理設定與「已設定，請開始」確認回覆。'],
  ['EF-01', '會議 → 摘要與待辦', '把錄音轉文字或逐字稿整理成可追蹤的會議產物。', '逐字稿、五點摘要與「誰／做什麼／何時前」待辦清單。'],
  ['EF-02', '拍照 → 結構化資料與 Email', '先讀清楚報價單，再產出可核對的回信草稿。', '欄位表格、模糊處標記與 150 字內確認 Email。'],
  ['EF-04', '棘手 Email 三種語氣', '漲價、婉拒或催款時，先比較立場再選語氣。', '正式保守、溫和堅定、友善清楚三版信件。'],
  ['NB-01', '萃取品牌聲音', '讓 NotebookLM 只根據來源整理品牌語氣，不自行推測。', '五個形容詞、三個句型、避用詞、開場方式與來源引用。'],
  ['TK-02', '品牌定位一句話', '先補齊模糊資料，再比較功能／情感／對立三個角度。', '三句 30 字內定位候選與人工選定的一句版本。'],
  ['MK-01', '一週七則社群貼文', '用同一份品牌定位建立一週內容節奏。', '七則貼文：開頭、150 字內內文、CTA、5–8 個 Hashtag。'],
  ['MK-02', '標題 A/B 測試', '同一篇內文先產不同吸引角度，再由人決定測哪兩個。', '10 個 20 字內標題，含客群類型標註。'],
  ['MK-03', '30 秒短影音腳本', '把一個主題拆成 5–7 秒一鏡、最後三秒 CTA。', '約 80–100 字逐鏡腳本與可執行的拍攝畫面。'],
  ['CS-01', 'FAQ 回覆庫', '同一組五個問題，批次產出三種使用情境的回覆。', '5 題 × 正式／親切／幽默三版，共 15 則 FAQ。'],
];

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function stripTags(value) {
  return value.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').trim();
}

function promptLibraryEntry(source, code) {
  const article = (source.match(/<article\b[\s\S]*?<\/article>/gi) || [])
    .find((block) => new RegExp(`<div class="pcard-code">\\s*${escapeRegExp(code)}\\s*</div>`).test(block));
  if (!article) throw new Error(`Prompt library entry not found: ${code}`);
  const title = stripTags(article.match(/<div class="pcard-title">([\s\S]*?)<\/div>/)?.[1] || '');
  const use = stripTags(article.match(/<p class="pcard-use">([\s\S]*?)<\/p>/)?.[1] || '');
  const prompt = article.match(/<pre class="(?:fill-template|prompt-pre)">([\s\S]*?)<\/pre>/)?.[1];
  if (!prompt) throw new Error(`Prompt text not found: ${code}`);
  return { title, use, prompt };
}

function quickReferenceHtml() {
  const source = fs.readFileSync(path.join(courseDir, 'prompt-library.html'), 'utf8');
  const entries = quickPromptCodes.map(([code, shortTitle, use, artifact]) => {
    const canonical = promptLibraryEntry(source, code);
    return { code, title: shortTitle || canonical.title, use: use || canonical.use, prompt: canonical.prompt, artifact };
  });
  const front = entries.slice(0, 5);
  const back = entries.slice(5);
  const card = ({ code, title, use, prompt, artifact }) => `<article class="quick-card"><header><span class="quick-code">${code}</span><h2>${title}</h2></header><p class="quick-use">${use}</p><pre class="quick-prompt">${prompt}</pre><p class="quick-artifact"><strong>完成物：</strong>${artifact}</p></article>`;
  const page = (label, subtitle, list) => `<section class="quick-page"><header class="quick-head"><div class="quick-kicker">創業 AI 實戰｜10 則 Prompt 精選</div><h1>${label}</h1><p>${subtitle}</p></header><div class="quick-grid">${list.map(card).join('')}</div><footer class="quick-footer"><div><strong>三條紅線：</strong>不貼個資／不把猜測當事實／不讓 AI 代替最後核對。</div><div><strong>發佈三問：</strong>來源在哪裡？數字對嗎？這句話我真的承諾得起嗎？</div></footer></section>`;
  const css = `
@page{size:A4;margin:7mm 8mm 8mm}
*{box-sizing:border-box!important}
html,body{margin:0!important;background:#fff!important;color:#252421!important}
body{font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif!important;font-size:7.1pt!important;line-height:1.28!important;-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
.quick-page{height:282mm;break-after:page;position:relative;padding:0 0 10mm}
.quick-page:last-child{break-after:auto}
.quick-head{border-top:2.5mm solid #5a7a5a;background:#f4f3ef;padding:4mm 5mm 3mm;margin-bottom:4mm}
.quick-kicker{color:#5a7a5a;font-size:7pt;letter-spacing:.12em;font-weight:700}
.quick-head h1{font-family:"Shippori Mincho","Noto Serif TC",serif;font-size:18pt!important;line-height:1.25!important;margin:1mm 0!important}
.quick-head p{color:#555;font-size:7.5pt!important;margin:0!important}
.quick-grid{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm 4mm;align-items:start}
.quick-card{border:1px solid #aaa;background:#faf9f6;padding:2.8mm;break-inside:avoid}
.quick-card header{display:flex;align-items:baseline;gap:2mm;border-bottom:1px solid #d3d0ca;padding-bottom:1mm;margin-bottom:1.5mm}
.quick-code{color:#5a7a5a;font-size:7pt;letter-spacing:.1em;font-weight:700;white-space:nowrap}
.quick-card h2{font-size:9.4pt!important;line-height:1.3!important;margin:0!important}
.quick-use{font-size:7pt!important;color:#555;margin:0 0 1.5mm!important;line-height:1.35!important}
.quick-prompt{font-family:"SFMono-Regular","Menlo","Noto Sans Mono",monospace;font-size:6.65pt!important;line-height:1.24!important;white-space:pre-wrap!important;overflow-wrap:anywhere!important;background:#efeee9!important;border-left:1.5mm solid #b5703a;padding:2mm!important;margin:0!important;color:#171717!important}
.quick-artifact{font-size:6.9pt!important;line-height:1.3!important;margin:1.5mm 0 0!important;color:#444}
.quick-footer{position:absolute;left:0;right:0;bottom:0;border-top:1px solid #aaa;padding-top:2mm;font-size:6.7pt;line-height:1.35;color:#444;display:flex;justify-content:space-between;gap:8mm}
.quick-footer>div{flex:1}
.quick-page:nth-child(2) .quick-head{padding-top:3mm;padding-bottom:2mm;margin-bottom:3mm}
.quick-page:nth-child(2) .quick-grid{gap:2.5mm 3mm}
.quick-page:nth-child(2) .quick-card{padding:2mm}
.quick-page:nth-child(2) .quick-prompt{font-size:6.1pt!important;line-height:1.13!important;padding:1.6mm!important}
.quick-page:nth-child(2) .quick-use,.quick-page:nth-child(2) .quick-artifact{font-size:6.45pt!important;line-height:1.2!important}
`;
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>創業 AI 實戰｜10 則 Prompt 精選</title><style>${css}</style></head><body>${page('正面｜效率與品牌資料', 'EF-08、EF-01、EF-02、EF-04、NB-01｜每則保留用途、可直接複製 Prompt 與完成物。', front)}${page('背面｜定位、內容與客服', 'TK-02、MK-01、MK-02、MK-03、CS-01｜先產候選，再由你做最後判斷。', back)}</body></html>`;
}

async function renderPdf({ htmlName, pdfName, pageContract, label }) {
  assertAuthorizedBrowserEnvironment();
  fs.mkdirSync(assetsDir, { recursive: true });
  const htmlPath = path.join(courseDir, htmlName);
  const pdfPath = path.join(assetsDir, pdfName);
  fs.writeFileSync(htmlPath, (htmlName === 'handbook.html' ? handbookHtml() : quickReferenceHtml()).replace(/[ \t]+$/gm, ''));
  if (!fs.existsSync(chromePath)) throw new Error(`Google Chrome not found: ${chromePath}`);
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  const page = await browser.newPage({ viewport: { width: 1240, height: 1754 } });
  await page.goto(`file://${htmlPath}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: htmlName === 'handbook.html',
    headerTemplate: '<div></div>',
    footerTemplate: htmlName === 'handbook.html' ? '<div style="width:100%;font-size:7px;color:#777;padding:0 12mm;text-align:right"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' : '<div></div>',
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  await browser.close();
  const pages = pageCount(pdfPath);
  console.log(`${label}: ${pdfPath}\\nPages: ${pages}`);
  if (!draft && !pageContract(pages)) throw new Error(`${label} page contract failed: ${pages}`);
}

async function renderHandbook() {
  await renderPdf({ htmlName: 'handbook.html', pdfName: '創業-AI-實戰手冊.pdf', pageContract: (pages) => pages >= 55 && pages <= 65, label: 'Handbook' });
}

async function renderQuickReference() {
  await renderPdf({ htmlName: 'quick-reference.html', pdfName: '創業-AI-實戰-10則Prompt精選.pdf', pageContract: (pages) => pages === 2, label: 'Quick reference' });
}

if (!['handbook', 'quick-reference', 'all'].includes(mode)) {
  console.error('Usage: node build-deliverables.js handbook|quick-reference|all [--draft]');
  process.exit(2);
}

(async () => {
  if (mode === 'handbook') await renderHandbook();
  if (mode === 'quick-reference') await renderQuickReference();
  if (mode === 'all') {
    await renderHandbook();
    await renderQuickReference();
  }
})().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
