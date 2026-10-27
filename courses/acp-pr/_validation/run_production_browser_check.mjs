import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const baseUrl = 'http://127.0.0.1:8765/courses/acp-pr/ai-short-video-editing';
const pages = ['index', 'CH0-1', 'CH0-2', 'CH0-3', 'CH0-4', 'CH1-1', 'CH1-2', 'CH1-3', 'CH1-4'];
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'tablet', width: 820, height: 1180 },
  { name: 'desktop', width: 1440, height: 900 },
];
const screenshotPages = new Set(['index', 'CH0-3', 'CH1-3']);
const evidenceDir = path.resolve('courses/acp-pr/_validation/production-browser');
fs.mkdirSync(evidenceDir, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
});
let checked = 0;

try {
  for (const viewport of viewports) {
    for (const pageName of pages) {
      const page = await browser.newPage({ viewport });
      const response = await page.goto(`${baseUrl}/${pageName}.html`, { waitUntil: 'domcontentloaded' });
      if (!response?.ok()) throw new Error(`${pageName} ${viewport.name}: HTTP ${response?.status()}`);
      await page.waitForTimeout(250);

      const result = await page.evaluate(() => {
        const doc = document.documentElement;
        const main = document.querySelector('main#main');
        const header = document.querySelector('header');
        const heading = document.querySelector('h1');
        return {
          overflow: doc.scrollWidth - doc.clientWidth,
          mainCount: document.querySelectorAll('main#main').length,
          learnerRootCount: document.querySelectorAll('[data-learner-content-root="true"]').length,
          h1Count: document.querySelectorAll('h1').length,
          mainTop: main?.getBoundingClientRect().top ?? -1,
          headerBottom: header?.getBoundingClientRect().bottom ?? -1,
          headingVisible: Boolean(heading && heading.getBoundingClientRect().height > 0),
        };
      });

      if (result.overflow > 1) throw new Error(`${pageName} ${viewport.name}: horizontal overflow ${result.overflow}px`);
      if (result.mainCount !== 1 || result.learnerRootCount !== 1 || result.h1Count !== 1) {
        throw new Error(`${pageName} ${viewport.name}: main=${result.mainCount}, learnerRoot=${result.learnerRootCount}, h1=${result.h1Count}`);
      }
      if (result.mainTop < result.headerBottom || !result.headingVisible) {
        throw new Error(`${pageName} ${viewport.name}: header/content overlap or hidden h1`);
      }

      await page.keyboard.press('Tab');
      const focused = await page.evaluate(() => document.activeElement?.classList.contains('skip-link'));
      if (!focused) throw new Error(`${pageName} ${viewport.name}: skip link is not first focus target`);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(50);
      if ((await page.evaluate(() => location.hash)) !== '#main') throw new Error(`${pageName} ${viewport.name}: skip link did not reach #main`);

      if (screenshotPages.has(pageName)) {
        await page.screenshot({
          path: path.join(evidenceDir, `${pageName}-${viewport.name}.png`),
          fullPage: true,
        });
      }
      checked += 1;
      console.log(`PASS ${pageName} ${viewport.width}x${viewport.height}`);
      await page.close();
    }
  }
} finally {
  await browser.close();
}

console.log(`SUMMARY checked=${checked} failed=0 screenshots=9`);
