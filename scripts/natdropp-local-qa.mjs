import { createRequire } from 'node:module';
import { mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const require = createRequire('file:///C:/Users/jonat/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright@1.61.1/node_modules/playwright/package.json');
const { chromium } = require('playwright');

const root = resolve('.');
const preview = pathToFileURL(resolve(root, 'dist/natdropp-preview.html')).href;
const outDir = resolve(root, 'dist/qa-final');
await mkdir(outDir, { recursive: true });

const viewports = [
  { name: '390', width: 390, height: 844 },
  { name: '768', width: 768, height: 1024 },
  { name: '1440', width: 1440, height: 960 },
];

const browser = await chromium.launch({ headless: true });
const results = [];

for (const viewport of viewports) {
  const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height } });
  const consoleMessages = [];
  page.on('console', (message) => {
    if (['error', 'warning'].includes(message.type())) {
      consoleMessages.push({ type: message.type(), text: message.text() });
    }
  });
  page.on('pageerror', (error) => {
    consoleMessages.push({ type: 'pageerror', text: error.message });
  });

  await page.goto(`${preview}?qa=${Date.now()}-${viewport.name}`, { waitUntil: 'load' });
  await page.fill('[data-preview-gate-input]', 'natdrop4321');
  await page.click('[data-preview-gate-form] button');
  await page.waitForSelector('#nd-formula-home', { state: 'visible' });
  await page.evaluate(() => {
    document.documentElement.style.scrollBehavior = 'auto';
    document.body.style.scrollBehavior = 'auto';
  });
  await page.waitForTimeout(250);
  await page.screenshot({ path: resolve(outDir, `hero-${viewport.name}.png`), fullPage: false });

  await page.evaluate(() => {
    const formula = document.querySelector('#nd-formula');
    if (formula) {
      const top = formula.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: Math.max(0, top), left: 0, behavior: 'instant' });
    }
  });
  await page.waitForTimeout(350);
  await page.screenshot({ path: resolve(outDir, `formula-${viewport.name}.png`), fullPage: false });

  await page.evaluate(() => {
    const multiuse = document.querySelector('.nd-multiuse');
    if (multiuse) {
      const top = multiuse.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: Math.max(0, top), left: 0, behavior: 'instant' });
    }
  });
  await page.waitForTimeout(250);
  await page.screenshot({ path: resolve(outDir, `multiuse-${viewport.name}.png`), fullPage: false });

  await page.evaluate(() => {
    const final = document.querySelector('.nd-final');
    if (final) {
      const top = final.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: Math.max(0, top), left: 0, behavior: 'instant' });
    }
  });
  await page.waitForTimeout(250);
  await page.screenshot({ path: resolve(outDir, `final-${viewport.name}.png`), fullPage: false });

  const checks = await page.evaluate(() => {
    const root = document.querySelector('#nd-formula-home');
    const rootRect = root ? root.getBoundingClientRect() : null;
    const brokenImages = Array.from(document.images)
      .filter((image) => image.complete && image.naturalWidth === 0)
      .map((image) => image.currentSrc || image.src || image.alt || 'unknown');
    const longTextNodes = Array.from(document.querySelectorAll('#nd-formula-home .nd-btn, #nd-formula-home summary, #nd-formula-home .nd-use-tags span, #nd-formula-home .nd-specs li'))
      .map((element) => {
        const rect = element.getBoundingClientRect();
        return {
          text: element.textContent.trim().slice(0, 90),
          overflow: Math.max(0, rect.width - window.innerWidth),
          height: rect.height,
        };
      })
      .filter((item) => item.overflow > 1);
    return {
      hasRoot: Boolean(root),
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth,
      overflowX: document.documentElement.scrollWidth - window.innerWidth,
      rootWidth: rootRect ? rootRect.width : 0,
      brokenImages,
      detailsCount: document.querySelectorAll('#nd-formula-home details').length,
      useTagCount: document.querySelectorAll('#nd-formula-home .nd-use-tags span').length,
      stepCount: document.querySelectorAll('#nd-formula-home [data-nd-steps] article').length,
      longTextNodes,
      visibleOldBotanicalSrcs: Array.from(document.querySelectorAll('#nd-formula-home img, #nd-formula-home [style]'))
        .map((node) => node.getAttribute('src') || node.getAttribute('style') || '')
        .filter((value) => value.includes('nd-leaf-') || value.includes('nd-lavender-')),
    };
  });

  results.push({ viewport: viewport.name, consoleMessages, checks });
  await page.close();
}

await browser.close();
console.log(JSON.stringify({ outDir, results }, null, 2));
