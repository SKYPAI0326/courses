import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

const here = dirname(fileURLToPath(import.meta.url));
const courseRoot = resolve(here, "../..");
const browserDir = join(here, "browser");
mkdirSync(browserDir, { recursive: true });

const baseUrl = process.env.UIUX_BASE_URL || "http://127.0.0.1:8765/courses/uiux-designer";
const cases = [
  { id: "index", url: "index.html", file: "index.html", anchor: "T01–T08" },
  { id: "b6", url: "part2/CH6-prototype-task-test.html", file: "part2/CH6-prototype-task-test.html", anchor: "T01–T08" },
  { id: "b7", url: "part2/CH7-figma-handoff-export.html", file: "part2/CH7-figma-handoff-export.html", anchor: "Photoshop" },
  { id: "b8", url: "part3/CH8-web-git-deploy.html", file: "part3/CH8-web-git-deploy.html", anchor: "VS Code官方下載" },
];
const viewports = [
  { width: 1440, height: 900 },
  { width: 820, height: 1180 },
  { width: 390, height: 844 },
];

const sha256 = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
const results = [];
let failed = false;

const browser = await chromium.launch({ channel: "chrome", headless: true });
try {
  for (const item of cases) {
    const filePath = join(courseRoot, item.file);
    for (const viewport of viewports) {
      const page = await browser.newPage({ viewport });
      const consoleErrors = [];
      const pageErrors = [];
      const badResponses = [];
      page.on("console", (message) => {
        if (message.type() === "error") consoleErrors.push(message.text());
      });
      page.on("pageerror", (error) => pageErrors.push(error.message));
      page.on("response", (browserResponse) => {
        if (browserResponse.status() >= 400) {
          badResponses.push({ status: browserResponse.status(), url: browserResponse.url() });
        }
      });

      const response = await page.goto(`${baseUrl}/${item.url}`, { waitUntil: "networkidle" });
      await page.evaluate(() => localStorage.clear());
      await page.reload({ waitUntil: "networkidle" });

      const metrics = await page.evaluate((anchor) => {
        const root = document.documentElement;
        const topbar = document.querySelector(".topbar");
        const content = document.body.innerText;
        return {
          title: document.title,
          mainCount: document.querySelectorAll("main").length,
          horizontalOverflow: root.scrollWidth > root.clientWidth,
          scrollWidth: root.scrollWidth,
          clientWidth: root.clientWidth,
          scrollHeight: root.scrollHeight,
          anchorPresent: content.includes(anchor),
          topbarPosition: topbar ? getComputedStyle(topbar).position : "not-present",
        };
      }, item.anchor);

      const passed = Boolean(response?.ok())
        && metrics.mainCount === 1
        && !metrics.horizontalOverflow
        && metrics.anchorPresent
        && badResponses.filter((item) => !item.url.endsWith("/favicon.ico")).length === 0
        && pageErrors.length === 0;
      if (!passed) failed = true;

      const screenshots = [];
      if (item.id === "b8") {
        for (const position of ["top", "middle", "bottom"]) {
          await page.evaluate((where) => {
            const max = Math.max(0, document.documentElement.scrollHeight - innerHeight);
            const y = where === "top" ? 0 : where === "middle" ? Math.floor(max / 2) : max;
            scrollTo(0, y);
          }, position);
          await page.waitForTimeout(100);
          const name = `b8-${viewport.width}-${position}.png`;
          await page.screenshot({ path: join(browserDir, name) });
          screenshots.push(name);
        }
      }

      results.push({
        id: item.id,
        file: item.file,
        sha256: sha256(filePath),
        viewport,
        httpStatus: response?.status() ?? null,
        metrics,
        consoleErrors,
        pageErrors,
        badResponses,
        screenshots,
        result: passed ? "PASS" : "FAIL",
      });
      await page.close();
    }
  }
} finally {
  await browser.close();
}

const summary = {
  generatedAt: new Date().toISOString(),
  baseUrl,
  checked: results.length,
  passed: results.filter((item) => item.result === "PASS").length,
  failed: results.filter((item) => item.result === "FAIL").length,
  limits: [
    "Local browser smoke only; no Figma, Photoshop, GitHub, Pages or human learner actions were performed.",
    "Screenshots cover B8 top, middle and bottom at 1440, 820 and 390; other pages use DOM and overflow assertions.",
  ],
  results,
};
writeFileSync(join(here, "browser-smoke.json"), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify({ checked: summary.checked, passed: summary.passed, failed: summary.failed }));
if (failed) process.exit(1);
