// Structural and visual checks for docs/index.html.
//
//   set NODE_PATH to a folder containing playwright, and PREVIEW_CHROMIUM to a
//   Chromium executable. Optional: SHOTS_DIR for screenshots (default: none).
//   node scripts/check_site.cjs
const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');

(async () => {
  const root = path.resolve(__dirname, '..');
  const shots = process.env.SHOTS_DIR || '';
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.PREVIEW_CHROMIUM, headless: true });
  const failures = [];
  const check = (ok, msg) => { if (!ok) failures.push(msg); console.log((ok ? 'ok    ' : 'FAIL  ') + msg); };
  try {
    for (const vp of [{ name: 'desktop', width: 1300, height: 1000 }, { name: 'mobile', width: 390, height: 844 }]) {
      const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
      const errors = [];
      page.on('pageerror', e => errors.push(String(e)));
      await page.goto(process.env.SITE_URL || pathToFileURL(path.join(root, 'docs/index.html')).href);
      await page.waitForLoadState('load');
      await page.waitForTimeout(1500);

      const info = await page.evaluate(() => {
        const sections = [...document.querySelectorAll('section.level1')];
        const imgs = [...document.querySelectorAll('main img')];
        const nav = document.querySelector('nav.sitebar');
        return {
          sections: sections.length,
          imgs: imgs.length,
          broken: imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')),
          noAlt: imgs.filter(i => !(i.getAttribute('alt') || '').trim()).length,
          navHome: !!(nav && nav.querySelector('a[href]')),
          kofi: document.querySelectorAll('a[href="https://ko-fi.com/s/9e3a539eb0"]').length,
          tables: document.querySelectorAll('main table').length,
          wrapped: document.querySelectorAll('.table-scroll table').length,
          footnoteRefs: document.querySelectorAll('a.footnote-ref').length,
          footnoteLists: document.querySelectorAll('aside.footnotes').length,
          overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
          strips: document.querySelectorAll('.aud').length,
          visibleStrips: [...document.querySelectorAll('.aud')].filter(s => s.style.display !== 'none').length,
          introReady: !!document.querySelector('#aud-intro.ready'),
          hasManifest: typeof AUDIO !== 'undefined' && AUDIO !== null,
        };
      });
      check(errors.length === 0, `${vp.name}: no page errors ${errors.join('; ')}`);
      check(info.sections >= 18, `${vp.name}: ${info.sections} top-level sections`);
      check(info.imgs === 21 && info.broken.length === 0, `${vp.name}: ${info.imgs} figures, none broken ${info.broken.join(',')}`);
      check(info.noAlt === 0, `${vp.name}: every figure has alt text`);
      const cover = await page.evaluate(() => { const i = document.querySelector('.mast-cover'); return i ? { ok: i.complete && i.naturalWidth > 0, alt: !!(i.alt || '').trim() } : null; });
      check(cover && cover.ok && cover.alt, `${vp.name}: cover image loads and has alt text`);
      check(info.navHome, `${vp.name}: site header has a link home`);
      check(info.kofi >= 3, `${vp.name}: Ko-fi link in header, masthead and footer (${info.kofi})`);
      check(info.tables === info.wrapped && info.tables > 0, `${vp.name}: ${info.tables} tables, all in scroll regions`);
      check(info.footnoteRefs > 50 && info.footnoteLists >= 12, `${vp.name}: ${info.footnoteRefs} footnote refs in ${info.footnoteLists} lists`);
      check(!info.overflowX, `${vp.name}: no horizontal page overflow`);
      if (info.hasManifest) {
        check(info.strips >= 15, `${vp.name}: ${info.strips} player strips`);
        check(info.introReady && info.visibleStrips === info.strips, `${vp.name}: player revealed after audio answered`);
      } else {
        console.log(`note  ${vp.name}: no audio manifest embedded (reading copy only)`);
      }
      if (shots) {
        await page.screenshot({ path: path.join(shots, `site-${vp.name}-top.png`) });
        for (const [key, sel] of [['ch6', '#chapter-6\\.-a-measured-case'], ['ch7', '#chapter-7\\.-the-cascade-that-made-things-worse'], ['ch10', '#chapter-10\\.-between-prediction-and-action']]) {
          const el = await page.$(sel);
          if (el) {
            await el.scrollIntoViewIfNeeded();
            await page.waitForTimeout(300);
            await page.screenshot({ path: path.join(shots, `site-${vp.name}-${key}.png`) });
          }
        }
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
  console.log(failures.length ? `\n${failures.length} check(s) failed` : '\nall checks passed');
  process.exit(failures.length ? 1 : 0);
})();
