const { chromium } = require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const baseUrl = 'http://127.0.0.1:8765/courses/office-ai';
const outputDir = path.join(__dirname, 'evidence');
fs.mkdirSync(outputDir, { recursive: true });

const units = [
  { id: 'CH1-2', url: 'ch1/CH1-2.html', mid: '免費帳號的 50 筆來源怎麼分' },
  { id: 'CH6-1', url: 'ch6/CH6-1.html', mid: '確認後才寫入' },
  { id: 'CH6-3', url: 'ch6/CH6-3.html', mid: '從學習助教移植到工作助理' },
];
const viewports = [
  { width: 1440, height: 900 },
  { width: 390, height: 844 },
  { width: 430, height: 932 },
];

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  const results = [];
  let failed = false;
  try {
    for (const viewport of viewports) {
      const context = await browser.newContext({ viewport });
      for (const unit of units) {
        const page = await context.newPage();
        await page.goto(`${baseUrl}/${unit.url}`, { waitUntil: 'networkidle' });
        if (await page.locator('#_gate').isVisible()) {
          await page.locator('#_gate-input').fill('officeai2026');
          await page.locator('#_gate-btn').click();
        }
        await page.waitForTimeout(100);
        const top = await page.evaluate(() => {
          const root = document.documentElement;
          const body = document.querySelector('.lesson-body');
          const nav = document.querySelector('.lesson-nav');
          return {
            title: document.querySelector('.lesson-title')?.textContent.trim(),
            gate: getComputedStyle(document.querySelector('#_gate')).display,
            sticky: getComputedStyle(document.querySelector('.topbar')).position,
            viewport: { width: innerWidth, height: innerHeight },
            globalOverflow: root.scrollWidth > root.clientWidth,
            root: { scrollWidth: root.scrollWidth, clientWidth: root.clientWidth },
            bodyWidth: body?.getBoundingClientRect().width,
            navWithinViewport: nav ? nav.getBoundingClientRect().right <= innerWidth + 1 : false,
            sections: document.querySelectorAll('.lesson-section').length,
            tables: [...document.querySelectorAll('.prose table')].map((el) => ({ scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, display: getComputedStyle(el).display })),
            pres: [...document.querySelectorAll('.prose pre')].map((el) => ({ scrollWidth: el.scrollWidth, clientWidth: el.clientWidth })),
          };
        });
        const label = `${unit.id}-${viewport.width}`;
        await page.screenshot({ path: path.join(outputDir, `${label}-top.png`), fullPage: false });
        await page.getByText(unit.mid, { exact: true }).scrollIntoViewIfNeeded();
        await page.screenshot({ path: path.join(outputDir, `${label}-mid.png`), fullPage: false });
        await page.locator('.lesson-nav').scrollIntoViewIfNeeded();
        await page.screenshot({ path: path.join(outputDir, `${label}-bottom.png`), fullPage: false });

        let scrollState = null;
        if (viewport.width === 1440) {
          await page.evaluate(() => window.scrollTo(0, Math.round(document.documentElement.scrollHeight * 0.4)));
          await page.waitForTimeout(350);
          const savedAt = await page.evaluate(() => window.scrollY);
          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(100);
          const restoredAt = await page.evaluate(() => window.scrollY);
          await page.evaluate(() => {
            localStorage.removeItem(`progress:${location.pathname}`);
            window.scrollTo(0, 0);
          });
          await page.waitForTimeout(350);
          await page.goto(`${baseUrl}/${unit.url}?smoke=cleared`, { waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(100);
          const clearedAt = await page.evaluate(() => window.scrollY);
          scrollState = { savedAt, restoredAt, clearedAt };
        }

        const pass = top.gate === 'none' && top.sticky === 'sticky' && !top.globalOverflow && top.navWithinViewport && top.sections > 0 && (!scrollState || (scrollState.restoredAt > 0 && scrollState.clearedAt === 0));
        results.push({ unit: unit.id, viewport, pass, top, scrollState });
        if (!pass) failed = true;
        await page.close();
      }
      await context.close();
    }
  } finally {
    await browser.close();
  }
  const report = { generatedAt: new Date().toISOString(), failed, results };
  fs.writeFileSync(path.join(outputDir, 'viewport-smoke.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = failed ? 1 : 0;
})();
