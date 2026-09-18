const fs = require('fs');
const path = require('path');
const { chromium } = require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const COURSE_ROOT = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(COURSE_ROOT, '..', '..');
const OUTPUT_DIR = path.join(COURSE_ROOT, 'output', 'pdf');
const TMP_DIR = path.join(COURSE_ROOT, 'tmp', 'pdfs');
const LAYOUT_CSS = path.join(COURSE_ROOT, 'assets', 'layout-redesign.css');

const LESSONS = [
  { file: 'CH1-1.html', code: 'CH1-1', title: '第一次與 LLM 對話：把日常問題說清楚', sections: ['lesson-start', 'lesson-concept', 'lesson-example-bank', 'lesson-demo', 'lesson-practice', 'lesson-check'] },
  { file: 'CH2-1.html', code: 'CH2-1', title: '日常溝通：讓 AI 幫你寫 Email、LINE／短訊息與自我介紹', sections: ['lesson-start', 'lesson-concept', 'lesson-demo', 'lesson-practice', 'lesson-check'] },
  { file: 'CH3-1.html', code: 'CH3-1', title: '摘要、抽取、條列：用 NotebookLM 把長文變成可用重點', sections: ['lesson-start', 'lesson-concept', 'lesson-demo', 'lesson-practice', 'lesson-check', 'lesson-assets'] },
  { file: 'CH4-1.html', code: 'CH4-1', title: '30 個生活化提示詞：把 LLM 套到自己的情境', sections: ['lesson-start', 'lesson-concept', 'lesson-demo', 'lesson-practice', 'lesson-check'] },
];

function read(relativePath) {
  return fs.readFileSync(path.join(COURSE_ROOT, relativePath), 'utf8');
}

function extractMain(source) {
  const match = source.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  if (!match) throw new Error('Missing <main> in source page');
  return match[1];
}

function extractStyles(source) {
  return [...source.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((match) => match[1]).join('\n');
}

function extractHero(main) {
  const start = main.search(/<div\b[^>]*class=["'][^"']*page-hero/i);
  const end = main.search(/<nav\b[^>]*class=["'][^"']*lesson-quicknav/i);
  if (start < 0 || end < 0 || end <= start) return '';
  return main.slice(start, end);
}

function extractSection(main, id) {
  const escaped = id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = main.match(new RegExp(`<section\\b[^>]*\\bid=["']${escaped}["'][^>]*>[\\s\\S]*?<\\/section>`, 'i'));
  if (!match) throw new Error(`Missing section #${id}`);
  return match[0];
}

function cleanMarkup(markup) {
  return markup
    .replace(/<nav\b[\s\S]*?<\/nav>/gi, '')
    .replace(/<script\b[\s\S]*?<\/script>/gi, '')
    .replace(/<details(?![^>]*\bopen\b)([^>]*)>/gi, '<details open$1>')
    .replace(/<a\b[^>]*href=["'][^"']*["'][^>]*>([\s\S]*?)<\/a>/gi, '$1')
    .replace(/\s(?:onclick|onchange|oninput)=["'][^"']*["']/gi, '')
    .trim();
}

function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function titleFrom(source, fallback) {
  return (source.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i) || [null, fallback])[1]
    .replace(/<[^>]+>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function assetAppendix() {
  const groups = [
    {
      title: '核心工作表',
      files: [
        'assets/worksheets/unit1-practice-sheet.md',
        'assets/templates/unit2-communication-scenarios.md',
        'assets/worksheets/unit3-notebooklm-reading-pack.md',
        'assets/worksheets/unit4-lifestyle-application-card.md',
        'assets/worksheets/course-capstone-handoff.md',
      ],
    },
    {
      title: '生活化提示詞庫與共同素材',
      files: [
        'assets/prompts/unit4-lifestyle-prompts.md',
        'assets/datasets/unit4-air-conditioner-comparison.md',
      ],
    },
    {
      title: '離線備援',
      files: [
        'assets/fallback/text-llm-minimum-start.md',
        'assets/fallback/unit1-dialogue-simulator.md',
        'assets/fallback/unit3-notebooklm-text-fallback.md',
      ],
    },
    {
      title: 'NotebookLM 來源索引與示範來源',
      files: [
        'assets/sources/README.md',
        'assets/sources/news-community-fridge.txt',
        'assets/sources/news-workshop-transcript.txt',
        'assets/sources/news-market-stall.txt',
        'assets/sources/news-library-books.txt',
        'assets/sources/news-repair-cafe.txt',
        'assets/sources/notice-tax-filing.txt',
        'assets/sources/notice-labor-insurance.txt',
        'assets/sources/notice-health-insurance.txt',
        'assets/sources/book-excerpt-learning-notes.txt',
      ],
    },
  ];

  return `<section class="appendix">
    <div class="section-eyebrow">附錄｜離線材料</div>
    <h2 class="section-heading">工作表、提示詞與來源全部附在這裡</h2>
    <p class="body-text">完整離線版把課堂會用到的材料一併收進 PDF。需要實際操作時，仍建議先用網頁上的可下載原檔；本附錄適合離線閱讀、查找欄位與對照示範。</p>
    ${groups.map((group) => `<section class="asset-group">
      <h3>${group.title}</h3>
      ${group.files.map((file) => `<article class="asset-sheet">
        <h4>${file}</h4>
        <pre class="asset-text">${escapeHtml(read(file))}</pre>
      </article>`).join('\n')}
    </section>`).join('\n')}
  </section>`;
}

function courseMap() {
  return `<section class="print-map">
    <div class="section-eyebrow">閱讀順序</div>
    <h2 class="section-heading">四個單元，從提問到可重做的交付物</h2>
    <p class="body-text">每個單元都先看完成物，再用一個具體案例跟做，最後留下可保存的紀錄。第 3 單元固定使用 NotebookLM；其餘單元採 LLM 通用方法，不指定聊天平台。</p>
    <table class="map-table"><thead><tr><th>單元</th><th>核心任務</th><th>帶走的完成物</th></tr></thead><tbody>
      <tr><td>CH1-1｜3 小時</td><td>五欄提示詞、五題日常對話、一次單一變因修改</td><td>LLM 實務紀錄</td></tr>
      <tr><td>CH2-1｜3 小時</td><td>Email、LINE／短訊息、自我介紹的讀者與語氣改寫</td><td>日常文書包</td></tr>
      <tr><td>CH3-1｜3 小時</td><td>NotebookLM 來源、摘要、抽取、條列與引用回查</td><td>來源閱讀包</td></tr>
      <tr><td>CH4-1｜3 小時</td><td>從 30 張生活卡選一張，填入自己的條件並修訂</td><td>生活應用卡</td></tr>
      <tr><td>課後整合｜20–30 分鐘</td><td>把背景、任務、資料、條件、格式與版本紀錄放在一起</td><td>可交接的整合工作表</td></tr>
    </tbody></table>
  </section>`;
}

function blankLine(label, height = '13mm') {
  return `<div class="write-line-label">${label}</div><div class="write-area" style="min-height:${height}"></div>`;
}

function classroomWorksheet(code) {
  if (code === 'CH1-1') {
    return `<section class="print-worksheet">
      <div class="worksheet-kicker">課堂填寫｜CH1-1</div>
      <h3>五題對話紀錄與一次修改</h3>
      <p>每題留下「原始輸入／回答重點／你怎麼判斷」。修改時只改一個主要條件，保留前後版本。</p>
      <table class="write-table"><thead><tr><th>題目</th><th>本次輸入與必要條件</th><th>回答重點／判斷</th><th>修改一項</th></tr></thead><tbody>
        ${['自我介紹', '明天台北天氣', '晚餐規劃', 'ETF 白話解釋', '通知整理'].map((label, index) => `<tr><td>${index + 1}. ${label}</td><td></td><td></td><td></td></tr>`).join('')}
      </tbody></table>
      <div class="worksheet-footer">完成線：五題都有回答；至少一題有原版、修改指令、修正版；能指出一個仍需人工確認的地方。</div>
    </section>`;
  }
  if (code === 'CH2-1') {
    return `<section class="print-worksheet">
      <div class="worksheet-kicker">課堂填寫｜CH2-1</div>
      <h3>同一件事，換一位讀者</h3>
      <p>三類成品共用同一組事實；只改讀者、場合、語氣或長度。不要為了讓文字好看而新增資料。</p>
      <table class="write-table"><thead><tr><th>完成物</th><th>讀者／場合</th><th>必要事實與限制</th><th>我的版本與修改</th></tr></thead><tbody>
        <tr><td>Email</td><td></td><td></td><td></td></tr>
        <tr><td>LINE／短訊息</td><td></td><td></td><td></td></tr>
        <tr><td>自我介紹 1</td><td></td><td></td><td></td></tr>
        <tr><td>自我介紹 2</td><td></td><td></td><td></td></tr>
        <tr><td>自我介紹 3</td><td></td><td></td><td></td></tr>
      </tbody></table>
      <div class="worksheet-footer">完成線：1 封 Email、1 則訊息、3 版自我介紹；至少兩份保留前後版本，且三版事實一致。</div>
    </section>`;
  }
  if (code === 'CH3-1') {
    return `<section class="print-worksheet">
      <div class="worksheet-kicker">課堂填寫｜CH3-1</div>
      <h3>NotebookLM 閱讀包紀錄</h3>
      <p>每次回答都要能回到來源。先記錄來源名稱，再留下輸出目的與引用核對結果。</p>
      <table class="write-table"><thead><tr><th>任務</th><th>來源名稱</th><th>我要保留的欄位／格式</th><th>引用回查結果</th></tr></thead><tbody>
        <tr><td>新聞摘要</td><td></td><td>一句／200 字／500 字</td><td></td></tr>
        <tr><td>公告白話化</td><td></td><td>影響誰、期限／條件、下一步</td><td></td></tr>
        <tr><td>書籍行動筆記</td><td></td><td>5 個重點、3 個行動</td><td></td></tr>
      </tbody></table>
      <div class="worksheet-footer">完成線：三類產出都有來源；至少點開一個引用回看原文；若用離線備援，標記「待重跑」。</div>
    </section>`;
  }
  return `<section class="print-worksheet">
    <div class="worksheet-kicker">課堂填寫｜CH4-1</div>
    <h3>把一張提示詞卡改成自己的條件</h3>
    <p>選一個主卡即可。保留第一版，只修改一個主要條件，最後把待確認資訊標出來。</p>
    <table class="field-table"><tbody>
      <tr><th>主卡與目標</th><td></td></tr>
      <tr><th>時間／預算</th><td></td></tr>
      <tr><th>偏好／限制</th><td></td></tr>
      <tr><th>輸出格式</th><td></td></tr>
      <tr><th>本輪只改的變因</th><td></td></tr>
    </tbody></table>
    ${blankLine('第一版結果中，我看見的條件：', '22mm')}
    ${blankLine('修正版與待確認事項：', '22mm')}
    <div class="worksheet-footer">完成線：一張主卡、四段式提示詞、第一版、一次修訂、修正版與完成檢核。</div>
  </section>`;
}

function promptThemeGrid() {
  const groups = [
    ['旅遊', ['行程規劃', '景點推薦', '預算試算', '交通安排', '餐廳挑選', '行李打包']],
    ['購物', ['商品比較', '規格分析', '評價彙整', '議價話術', '退貨應對', '購買時機建議']],
    ['學習', ['讀書計畫', '知識解釋', '考試準備', '教材推薦', '進度追蹤', '學習瓶頸排解']],
    ['健康', ['飲食建議', '運動規劃', '症狀說明', '藥品說明', '就醫準備', '健檢報告解讀']],
    ['家庭', ['菜單規劃', '節慶安排', '家事管理', '親子活動', '家庭旅遊', '年節禮品選購']],
  ];
  return `<div class="theme-grid">${groups.map(([name, items]) => `<div class="theme-group"><strong>${name}</strong><ol>${items.map((item) => `<li>${item}</li>`).join('')}</ol></div>`).join('')}</div>`;
}

const FULL_CSS = `
@page{size:A4;margin:15mm 14mm 17mm}
*{box-sizing:border-box}
html,body{background:#fff!important;color:#202020!important}
body{margin:0!important;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",Arial,sans-serif!important;font-size:10.6pt!important;line-height:1.65!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.topbar,.progress-strip,.skip-link,#_gate,.lesson-quicknav,.nav-footer,.footer,script{display:none!important}
main,.page-hero,.lesson-section{max-width:none!important;width:auto!important;margin:0!important}
.print-cover{min-height:245mm;display:flex;flex-direction:column;justify-content:center;break-after:page;padding:18mm 7mm}
.print-kicker{font-size:9pt;letter-spacing:.16em;color:#555;margin-bottom:9mm}
.print-cover h1{font-family:"Noto Serif TC","Songti TC",serif;font-size:29pt;line-height:1.25;margin:0 0 8mm;max-width:17ch;color:#111}
.print-cover p{font-size:12pt;line-height:1.8;color:#444;max-width:38em;margin:0}
.print-meta{margin-top:18mm;font-size:9pt;color:#666;line-height:1.9}
.print-map{break-after:page;padding:3mm 1mm}
.print-map h2,.appendix>.section-heading{font-family:"Noto Serif TC","Songti TC",serif;font-size:19pt;line-height:1.35;margin:0 0 5mm;color:#111}
.section-eyebrow{font-size:8.2pt!important;letter-spacing:.14em!important;color:#666!important;margin:0 0 3mm!important}
.body-text{font-size:10.3pt!important;line-height:1.75!important;color:#303030!important;margin:0 0 4mm!important}
.map-table,table{width:100%!important;border-collapse:collapse!important;font-size:9.1pt!important;margin:5mm 0!important}
th,td{border:1px solid #a9a9a9!important;padding:5px 6px!important;vertical-align:top!important;line-height:1.55!important;color:#202020!important;background:#fff!important}
th{font-weight:700!important;background:#f1f1f1!important}
.full-lesson{break-before:page}
.full-lesson.first{break-before:auto}
.source-ribbon{font-size:8pt;color:#666;border-bottom:1px solid #777;padding-bottom:3mm;margin-bottom:6mm;text-align:right}
.page-hero{padding:0 0 8mm!important;margin:0 0 8mm!important;border-bottom:2px solid #222!important;min-height:auto!important}
.lesson-title{font-family:"Noto Serif TC","Songti TC",serif!important;font-size:23pt!important;line-height:1.3!important;color:#111!important;max-width:none!important;margin:0 0 4mm!important}
.lesson-tagline{font-size:10.5pt!important;color:#444!important;line-height:1.7!important;margin:0 0 5mm!important}
.outcomes{display:block!important;padding:4mm!important;border:1px solid #aaa!important;border-left:3px solid #444!important;margin:5mm 0 0!important;background:#fafafa!important;break-inside:avoid}
.outcomes-label{font-size:8pt!important;color:#333!important;letter-spacing:.12em!important;margin-bottom:2mm!important}
.outcome-item{font-size:9.3pt!important;color:#333!important;line-height:1.6!important;margin:1mm 0!important}
.lesson-start{border:1px solid #aaa!important;border-left:3px solid #444!important;padding:4mm!important;margin-top:5mm!important;background:#fafafa!important;break-inside:avoid}
.lesson-start-label{font-size:8pt!important;font-weight:700!important;letter-spacing:.12em!important;color:#333!important;display:block!important}
.lesson-start strong{display:block!important;font-size:10.5pt!important;margin:1mm 0!important}
.lesson-start-copy{display:block!important;font-size:9.3pt!important;color:#444!important}
.lesson-section{padding:0!important;margin:0 0 7mm!important;break-inside:auto}
.section-heading{font-family:"Noto Serif TC","Songti TC",serif!important;font-size:16.5pt!important;line-height:1.35!important;color:#111!important;margin:0 0 4mm!important;break-after:avoid!important}
.section-rule{border:0!important;border-top:1px solid #bbb!important;margin:7mm 0!important}
.intro-band,.callout,.tool-card,.ts-item,.quiz-item,.completion-line{border:1px solid #b8b8b8!important;border-left:3px solid #666!important;background:#fafafa!important;box-shadow:none!important;border-radius:0!important;padding:4mm!important;break-inside:avoid!important}
.intro-band{margin:0 0 4mm!important}.intro-label{font-size:8pt!important;letter-spacing:.1em!important;color:#333!important;margin-bottom:1mm!important}.intro-text,.callout-body,.tool-summary,.tool-list-item,.ts-a{font-size:9.6pt!important;line-height:1.65!important;color:#333!important}
.tool-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:4mm!important;margin:4mm 0!important}.tool-card{padding:4mm!important}.tool-name{font-family:"Noto Serif TC","Songti TC",serif!important;font-size:11pt!important;color:#111!important}.tool-tag{font-size:8pt!important;color:#444!important;border:1px solid #999!important;border-radius:0!important;padding:1px 5px!important}.tool-list{gap:1mm!important}
.steps-wrap{margin:4mm 0!important}.step-block{display:flex!important;gap:4mm!important;padding:4mm 0!important;border-bottom:1px solid #c5c5c5!important;break-inside:avoid!important}.step-circle{width:25px!important;height:25px!important;border-radius:50%!important;background:#eee!important;border:1px solid #888!important;font-size:9pt!important;color:#111!important}.step-heading{font-size:10.5pt!important;color:#111!important;margin-bottom:1mm!important}.step-body{font-size:9.5pt!important;color:#333!important;line-height:1.65!important}
.code-block,pre{white-space:pre-wrap!important;overflow-wrap:anywhere!important;word-break:break-word!important}.code-block{background:#f3f3f3!important;color:#111!important;border:1px solid #999!important;border-radius:0!important;padding:4mm!important;font-size:8.8pt!important;line-height:1.55!important;margin:4mm 0!important;break-inside:avoid!important}.dialog-box,.expected-output{font-size:9pt!important;line-height:1.55!important;background:#fff!important;border:1px solid #aaa!important;padding:3mm!important;break-inside:avoid!important}
.scenario-grid{margin:4mm 0!important;border:1px solid #999!important;border-radius:0!important;break-inside:auto!important}.scenario-row{display:grid!important;grid-template-columns:34mm 1fr!important;border-bottom:1px solid #bbb!important;break-inside:avoid!important}.scenario-task{padding:3mm!important;background:#f1f1f1!important;border-right:1px solid #bbb!important;font-size:8.9pt!important;color:#111!important}.scenario-pick{padding:3mm!important;font-size:9pt!important;color:#222!important;line-height:1.6!important}
table{break-inside:auto!important}tr{break-inside:avoid!important}p,li{orphans:3;widows:3}.quiz-ans{display:block!important;background:#fafafa!important;border:1px solid #aaa!important;padding:3mm!important}.quiz-ans summary{font-weight:700!important}.quiz-ans>div{font-size:9pt!important;line-height:1.6!important}.quiz-opt{background:#fff!important;border:1px solid #bbb!important;border-radius:0!important;font-size:9pt!important;padding:2mm!important}.quiz-opt input{display:none!important}.quiz-opt::before{content:"□ ";color:#555}
.appendix{break-before:page}.asset-group{break-before:page}.asset-group h3{font-family:"Noto Serif TC","Songti TC",serif;font-size:16pt;color:#111;margin:0 0 4mm}.asset-sheet{break-inside:auto;margin:0 0 8mm}.asset-sheet h4{font-size:10.5pt;color:#111;border-bottom:1px solid #aaa;padding-bottom:2mm;margin:0 0 3mm;break-after:avoid}.asset-text{font-family:"SFMono-Regular","Menlo","Noto Sans Mono",monospace;font-size:8.2pt!important;line-height:1.5!important;white-space:pre-wrap!important;background:#fafafa!important;border:1px solid #aaa!important;padding:4mm!important;color:#111!important}
a{color:#222!important;text-decoration:none!important}
`;

const BRIEF_CSS = `
@page{size:A4;margin:12mm 11mm 16mm}
*{box-sizing:border-box}
html,body{background:#fff!important;color:#171717!important}
body{margin:0!important;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",Arial,sans-serif!important;font-size:10.2pt!important;line-height:1.58!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.topbar,.progress-strip,.skip-link,#_gate,.lesson-quicknav,.nav-footer,.footer,script{display:none!important}
main,.page-hero,.lesson-section{max-width:none!important;width:auto!important;margin:0!important}
.print-cover{min-height:245mm;display:flex;flex-direction:column;justify-content:center;break-after:page;padding:15mm 5mm}.print-kicker{font-size:8.5pt;letter-spacing:.15em;color:#555;margin-bottom:8mm}.print-cover h1{font-family:"Noto Serif TC","Songti TC",serif;font-size:27pt;line-height:1.25;max-width:17ch;margin:0 0 7mm;color:#111}.print-cover p{font-size:11pt;color:#444;line-height:1.75;margin:0}.print-meta{margin-top:16mm;font-size:8.5pt;color:#666;line-height:1.8}
.print-map{break-after:page;padding:2mm 0}.print-map h2{font-family:"Noto Serif TC","Songti TC",serif;font-size:18pt;line-height:1.35;margin:0 0 4mm}.section-eyebrow{font-size:8pt!important;letter-spacing:.13em!important;color:#666!important;margin-bottom:2mm!important}.body-text{font-size:9.9pt!important;line-height:1.65!important;color:#222!important;margin:0 0 3mm!important}.map-table,table{width:100%!important;border-collapse:collapse!important;font-size:8.6pt!important;margin:4mm 0!important}th,td{border:1px solid #999!important;padding:4px 5px!important;vertical-align:top!important;line-height:1.45!important;color:#111!important;background:#fff!important}th{background:#eee!important}
.brief-lesson{break-before:page}.brief-lesson.first{break-before:auto}.brief-label{font-size:8pt;color:#555;border-bottom:1px solid #777;padding-bottom:2.5mm;margin-bottom:4mm;text-align:right}.brief-lesson .page-hero{padding:0 0 5mm!important;margin:0 0 5mm!important;border-bottom:2px solid #222!important;min-height:auto!important}.brief-lesson .lesson-title{font-family:"Noto Serif TC","Songti TC",serif!important;font-size:20pt!important;line-height:1.28!important;color:#111!important;max-width:none!important;margin:0 0 3mm!important}.brief-lesson .lesson-tagline{font-size:9.7pt!important;line-height:1.6!important;color:#333!important;margin:0 0 3mm!important}.brief-lesson .outcomes{display:block!important;padding:3mm!important;border:1px solid #999!important;border-left:3px solid #333!important;background:#fafafa!important;margin:3mm 0 0!important;break-inside:avoid}.brief-lesson .outcomes-label{font-size:7.8pt!important;letter-spacing:.1em!important;color:#222!important}.brief-lesson .outcome-item{font-size:8.8pt!important;line-height:1.5!important;margin:1mm 0!important}.brief-lesson .lesson-start{border:1px solid #999!important;border-left:3px solid #333!important;padding:3mm!important;background:#fafafa!important;margin-top:3mm!important;break-inside:avoid}.brief-lesson .lesson-start-label{font-size:7.8pt!important;display:block!important;font-weight:700!important}.brief-lesson .lesson-start strong{font-size:9.7pt!important;display:block!important;margin:1mm 0!important}.brief-lesson .lesson-start-copy{font-size:8.8pt!important;display:block!important}
.brief-lesson .lesson-section{padding:0!important;margin:0 0 5mm!important}.brief-lesson .section-heading{font-family:"Noto Serif TC","Songti TC",serif!important;font-size:14.5pt!important;line-height:1.32!important;color:#111!important;margin:0 0 3mm!important;break-after:avoid!important}.brief-lesson .intro-band,.brief-lesson .callout,.brief-lesson .tool-card,.brief-lesson .completion-line{border:1px solid #aaa!important;border-left:3px solid #555!important;background:#fafafa!important;border-radius:0!important;box-shadow:none!important;padding:3mm!important;break-inside:avoid!important}.brief-lesson .intro-band{margin:0 0 3mm!important}.brief-lesson .intro-label{font-size:7.8pt!important;letter-spacing:.08em!important;color:#222!important;margin-bottom:1mm!important}.brief-lesson .intro-text,.brief-lesson .callout-body,.brief-lesson .tool-summary,.brief-lesson .tool-list-item{font-size:8.9pt!important;line-height:1.55!important;color:#222!important}.brief-lesson .tool-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:3mm!important;margin:3mm 0!important}.brief-lesson .tool-name{font-family:"Noto Serif TC","Songti TC",serif!important;font-size:10pt!important}.brief-lesson .tool-tag{font-size:7.5pt!important;border:1px solid #999!important;border-radius:0!important;color:#333!important}.brief-lesson .steps-wrap{margin:3mm 0!important}.brief-lesson .step-block{display:flex!important;gap:3mm!important;padding:3mm 0!important;border-bottom:1px solid #c5c5c5!important;break-inside:avoid!important}.brief-lesson .step-circle{width:22px!important;height:22px!important;background:#eee!important;border:1px solid #888!important;font-size:8.5pt!important}.brief-lesson .step-heading{font-size:9.7pt!important;color:#111!important;margin-bottom:1mm!important}.brief-lesson .step-body{font-size:8.8pt!important;line-height:1.55!important;color:#222!important}.brief-lesson .code-block,pre{white-space:pre-wrap!important;overflow-wrap:anywhere!important;word-break:break-word!important}.brief-lesson .code-block{background:#f4f4f4!important;color:#111!important;border:1px solid #999!important;border-radius:0!important;padding:3mm!important;font-size:8.1pt!important;line-height:1.45!important;margin:3mm 0!important;break-inside:avoid!important}.brief-lesson .scenario-grid{margin:3mm 0!important;border:1px solid #999!important;border-radius:0!important}.brief-lesson .scenario-row{display:grid!important;grid-template-columns:31mm 1fr!important;border-bottom:1px solid #bbb!important;break-inside:avoid!important}.brief-lesson .scenario-task{padding:2.5mm!important;background:#eee!important;border-right:1px solid #bbb!important;font-size:8.2pt!important;color:#111!important}.brief-lesson .scenario-pick{padding:2.5mm!important;font-size:8.4pt!important;line-height:1.5!important;color:#222!important}.brief-lesson table{break-inside:auto!important}.brief-lesson tr{break-inside:avoid!important}.brief-lesson .quiz-item,.brief-lesson .quiz-ans{font-size:8.6pt!important}.brief-lesson .quiz-opts{gap:1mm!important}.brief-lesson .quiz-opt{border:1px solid #bbb!important;border-radius:0!important;padding:1.5mm!important;font-size:8.3pt!important}.brief-lesson .quiz-opt input{display:none!important}.brief-lesson .quiz-opt::before{content:"□ ";color:#555}.brief-lesson .quiz-ans{display:block!important;background:#fafafa!important;border:1px solid #aaa!important;padding:2.5mm!important}.brief-lesson .quiz-ans summary{font-weight:700!important}.brief-lesson .quiz-ans>div{font-size:8.4pt!important;line-height:1.5!important}
.print-worksheet{break-before:page;border-top:2px solid #222;padding-top:5mm;margin:5mm 0 0}.worksheet-kicker{font-size:7.8pt;letter-spacing:.12em;color:#555;margin-bottom:2mm}.print-worksheet h3{font-family:"Noto Serif TC","Songti TC",serif;font-size:15pt;line-height:1.35;margin:0 0 3mm}.print-worksheet p{font-size:9pt;line-height:1.6;margin:0 0 3mm}.write-table{font-size:8.1pt!important}.write-table th,.write-table td{padding:3mm 3mm!important}.write-table tbody td{height:25mm;vertical-align:top}.worksheet-footer{border-top:1px solid #777;margin-top:4mm;padding-top:3mm;font-size:8.8pt;line-height:1.55}.field-table th{width:31mm}.field-table tbody td{height:14mm}.write-line-label{font-weight:700;font-size:8.8pt;margin-top:4mm}.write-area{border-bottom:1px solid #777;background:repeating-linear-gradient(to bottom,transparent 0,transparent 9mm,#bbb 9.2mm,#bbb 9.5mm)}.theme-grid{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:4mm 0}.theme-group{border:1px solid #999;padding:3mm;break-inside:avoid}.theme-group strong{font-family:"Noto Serif TC","Songti TC",serif;font-size:10pt}.theme-group ol{margin:2mm 0 0 5mm;padding:0;font-size:8.5pt;line-height:1.5}.theme-group li{margin:0}
a{color:#111!important;text-decoration:none!important}
`;

function fullDocument(overview, lessons, styles) {
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>AI 入門即戰力｜完整離線講義</title><style>${styles}\n${FULL_CSS}</style></head><body class="pdf-document">
  <section class="print-cover"><div class="print-kicker">FULL OFFLINE HANDOUT</div><h1>AI 入門即戰力：零基礎的 AI 入門應用</h1><p>12 小時基礎實務課程完整離線講義。保留四個單元的教學正文、完整示範、操作步驟、判斷標準、修復路徑與課程材料。</p><div class="print-meta">版本：2026-09-16<br>內容來源：ai-beginner-practical 課程網頁與課程資產<br>使用方式：可搜尋閱讀；需要實際操作時，請搭配課程提供的原始 Markdown 資產。</div></section>
  ${courseMap()}
  <article class="full-overview">${overview}</article>
  ${lessons.join('\n')}
  ${assetAppendix()}
  </body></html>`;
}

function briefDocument(lessons, styles) {
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>AI 入門即戰力｜課堂印刷簡易版</title><style>${styles}\n${BRIEF_CSS}</style></head><body class="pdf-document">
  <section class="print-cover"><div class="print-kicker">CLASSROOM PRINT HANDOUT</div><h1>AI 入門即戰力：課堂翻閱版</h1><p>四個單元的必做案例、操作提示、判斷標準與填寫頁。適合 A4 黑白雙面列印，課堂中邊聽邊翻閱、記錄與核對。</p><div class="print-meta">版本：2026-09-16<br>印刷原則：A4｜黑白可讀｜重要區塊避免跨頁<br>建議：每位學員一份，從 CH1-1 開始使用。</div></section>
  <section class="print-map"><div class="section-eyebrow">課堂地圖</div><h2>今天要留下四份可以重做的完成物</h2><table class="map-table"><thead><tr><th>單元</th><th>課堂必做</th><th>完成物</th></tr></thead><tbody><tr><td>CH1-1</td><td>五題對話＋一次修改</td><td>LLM 實務紀錄</td></tr><tr><td>CH2-1</td><td>Email、訊息、三版自我介紹</td><td>日常文書包</td></tr><tr><td>CH3-1</td><td>NotebookLM 三類閱讀任務＋引用回查</td><td>來源閱讀包</td></tr><tr><td>CH4-1</td><td>選一張生活卡＋一次條件修訂</td><td>生活應用卡</td></tr></tbody></table><p class="body-text">每次都保留第一版與修正版。只改一個主要條件，才能看懂結果為什麼改變。</p></section>
  ${lessons.map((lesson, index) => lesson).join('\n')}
  </body></html>`;
}

async function renderPdf(browser, htmlPath, pdfPath, headerText) {
  const page = await browser.newPage({ viewport: { width: 1240, height: 1754 }, deviceScaleFactor: 1 });
  await page.goto(`file://${htmlPath}`, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: `<div style="width:100%;font-size:7pt;color:#777;padding:0 14mm;text-align:left;">${headerText}</div>`,
    footerTemplate: '<div style="width:100%;font-size:7pt;color:#777;padding:0 14mm;text-align:right;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  await page.close();
}

async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  fs.mkdirSync(TMP_DIR, { recursive: true });

  const sourcePages = LESSONS.map((lesson) => ({ ...lesson, html: read(lesson.file) }));
  const sourceStyles = [
    fs.readFileSync(LAYOUT_CSS, 'utf8'),
    ...sourcePages.map((page) => extractStyles(page.html)),
    extractStyles(read('module1.html')),
  ].join('\n');

  const overview = cleanMarkup(extractMain(read('module1.html')));
  const fullLessons = sourcePages.map((lesson, index) => `<article class="full-lesson ${index === 0 ? 'first' : ''}"><div class="source-ribbon">${lesson.code}｜完整教學正文</div>${cleanMarkup(extractMain(lesson.html))}</article>`);

  const briefLessons = sourcePages.map((lesson, index) => {
    const main = extractMain(lesson.html);
    const hero = cleanMarkup(extractHero(main));
    const sections = lesson.sections.map((id) => cleanMarkup(extractSection(main, id))).join('\n');
    const worksheet = classroomWorksheet(lesson.code);
    const extra = lesson.code === 'CH4-1' ? `<section class="print-worksheet"><div class="worksheet-kicker">課堂速查｜CH4-1</div><h3>30 張生活化提示詞主題</h3><p>選一張主卡即可；這裡列出主題，完整四段式提示詞仍收在完整版附錄與網頁資產。</p>${promptThemeGrid()}</section>` : '';
    return `<article class="brief-lesson ${index === 0 ? 'first' : ''}"><div class="brief-label">${lesson.code}｜課堂翻閱版</div>${hero}${sections}${worksheet}${extra}</article>`;
  });

  const fullHtml = fullDocument(overview, fullLessons, sourceStyles);
  const briefHtml = briefDocument(briefLessons, sourceStyles);
  const fullHtmlPath = path.join(TMP_DIR, 'ai-beginner-practical-full-offline-handout.html');
  const briefHtmlPath = path.join(TMP_DIR, 'ai-beginner-practical-classroom-print-handout.html');
  const fullPdfPath = path.join(OUTPUT_DIR, 'ai-beginner-practical-full-offline-handout.pdf');
  const briefPdfPath = path.join(OUTPUT_DIR, 'ai-beginner-practical-classroom-print-handout.pdf');
  fs.writeFileSync(fullHtmlPath, fullHtml, 'utf8');
  fs.writeFileSync(briefHtmlPath, briefHtml, 'utf8');

  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  try {
    await renderPdf(browser, fullHtmlPath, fullPdfPath, 'AI 入門即戰力｜完整離線講義');
    await renderPdf(browser, briefHtmlPath, briefPdfPath, 'AI 入門即戰力｜課堂翻閱版');
  } finally {
    await browser.close();
  }

  console.log(fullPdfPath);
  console.log(briefPdfPath);
  console.log(`source lessons=${sourcePages.length}, appendix assets=${sourceStyles ? 'included' : 'missing'}`);
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
