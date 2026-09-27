// Run with NODE_PATH pointing at an installation of playwright.
const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
(async () => {
  const root = path.resolve(__dirname, '..');
  const out = path.join(root, '.research/preview-qa');
  fs.mkdirSync(out, {recursive:true});
  const browser = await chromium.launch({executablePath:process.env.PREVIEW_CHROMIUM, headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1440,height:1000}, deviceScaleFactor:1});
    const errors=[]; page.on('pageerror', e => errors.push(String(e)));
    await page.emulateMedia({reducedMotion:'reduce'});
    const url = pathToFileURL(path.join(root,'tutorial/decision-models.html')).href;
    await page.goto(url);
    await page.waitForFunction(() => document.querySelectorAll('[data-rendered="true"]').length === 5, {timeout:45000});
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({path:path.join(out,'desktop.png')});
    const figures = page.locator('.diagram-panel');
    for(let i=0;i<5;i++) await figures.nth(i).screenshot({path:path.join(out,`figure-${i+1}.png`)});
    await page.locator('math[display=block]').first().screenshot({path:path.join(out,'equation.png')});
    await page.locator('.table-scroll').first().screenshot({path:path.join(out,'table.png')});
    await page.locator('div.sourceCode').first().screenshot({path:path.join(out,'code.png')});
    const inspect = () => ({figures:document.querySelectorAll('.diagram-canvas svg').length,
      errors:document.querySelectorAll('.diagram-error').length,
      math:document.querySelectorAll('math').length,
      overflow:document.documentElement.scrollWidth > window.innerWidth,
      diagramWidths:[...document.querySelectorAll('.diagram-canvas')].map(n=>({content:n.scrollWidth,available:n.clientWidth})),
      nestedCode:document.querySelectorAll('pre.mermaid > code').length,
      brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.hash.slice(1)).filter(id=>!document.getElementById(decodeURIComponent(id)))});
    const desktop=await page.evaluate(inspect);
    await page.locator('.rail a').first().click();
    await page.waitForFunction(() => location.hash.length > 1);
    const navigation=await page.evaluate(()=>location.hash.length>1);
    await page.setViewportSize({width:390,height:844});
    await page.goto(url);
    await page.waitForFunction(() => document.querySelectorAll('[data-rendered="true"]').length === 5);
    await page.screenshot({path:path.join(out,'mobile.png')});
    const mobile=await page.evaluate(inspect);
    await page.locator('.diagram-panel').first().screenshot({path:path.join(out,'mobile-figure.png')});
    await page.emulateMedia({reducedMotion:'reduce'});
    const reducedMotion=await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior==='auto');
    await page.route('https://cdn.jsdelivr.net/**', route=>route.abort());
    await page.reload();
    await page.waitForFunction(()=>[...document.querySelectorAll('.diagram-canvas')].every(n=>n.textContent.includes('Connect to the internet')));
    const offline=await page.locator('.diagram-panel details[open]').count()===5;
    const report={desktop,mobile,navigation,reducedMotion,offlineSourceFallback:offline,pageErrors:errors};
    fs.writeFileSync(path.join(out,'render-check.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify(report,null,2));
    if(errors.length || desktop.overflow || mobile.overflow || desktop.errors || mobile.errors || desktop.diagramWidths.some(n=>n.content>n.available) || desktop.brokenAnchors.length || !offline || !navigation || !reducedMotion) process.exitCode=1;
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
