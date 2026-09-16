/* npm install --no-save playwright; mdbook build; serve book at CHARTS_URL. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
(async () => {
 const browser = await chromium.launch({headless: true});
 const page = await browser.newPage({viewport: {width: 1280, height: 1000}});
 page.setDefaultTimeout(15000); page.setDefaultNavigationTimeout(15000);
 const errors = []; page.on('pageerror', e => errors.push(e.message));
 const base = process.env.CHARTS_URL || 'http://127.0.0.1:8765';
 // Verify the charts work with all external network access disabled.
 await page.route('**/*', route => (route.request().url().startsWith(base) || route.request().url().startsWith('blob:'+base) || route.request().url().startsWith('data:')) ? route.continue() : route.abort());
 const pages = ['R7/tests/static/2026-02-21', 'R7/tests/static/2026-03-21', 'R7/tests/static/2026-04-10', 'R7/tests/cold-flow/2026-04-11', 'Liquid-Rurku/tests/cold-flow', 'Liquid-Rurku/tests/static/2026_07_14'];
 let count = 0;
 for (const path of pages) {
  console.log(path);
  await page.goto(`${base}/${path}/index.html`);
  const hosts = page.locator('[data-chart]');
  for (let i=0; i<await hosts.count(); i++) {
   const host = hosts.nth(i); await host.scrollIntoViewIfNeeded();
   await host.locator('.js-plotly-plot').waitFor();
   await page.waitForFunction(el => el.dataset.loaded === 'true', await host.elementHandle());
   assert.ok(await host.locator('.scatterlayer .trace').count()); count++;
  }
 }
 assert.equal(count, 11);
 await page.goto(`${base}/R7/tests/static/2026-03-21/index.html`);
 const host = page.locator('[data-chart]').first(); await host.scrollIntoViewIfNeeded();
 await page.waitForFunction(() => document.querySelector('[data-chart]').dataset.loaded === 'true');
 const plot = host.locator('.js-plotly-plot');
 await host.locator('.legendtoggle').first().click();
 await page.waitForFunction(() => document.querySelector('.js-plotly-plot').data[0].visible === 'legendonly');
 assert.equal(await host.locator('input').first().isChecked(), false);
 await host.getByRole('button', {name:'Pokaż wszystkie linie'}).click();
 assert.equal(await host.locator('input').first().isChecked(), true);
 await host.locator('input').first().uncheck();
 assert.equal(await plot.evaluate(el=>el.data[0].visible), 'legendonly');
 await host.locator('input').first().check();
 const before = await plot.evaluate(el => el.layout.xaxis.range.slice());
 const rect = await host.locator('.nsewdrag').first().boundingBox();
 await page.mouse.move(rect.x+rect.width*.25, rect.y+rect.height*.2);
 await page.mouse.down(); await page.mouse.move(rect.x+rect.width*.65, rect.y+rect.height*.8, {steps:10}); await page.mouse.up();
 const after = await plot.evaluate(el=>el.layout.xaxis.range.slice());
 assert.ok(after[1]-after[0] < before[1]-before[0]);
 await host.getByRole('button', {name:'Resetuj widok'}).click();
 assert.deepEqual(await plot.evaluate(el=>el.layout.xaxis.range), before);
 await host.locator('[data-title="Pan"]').click();
 await page.mouse.move(rect.x+rect.width*.4, rect.y+rect.height*.5); await page.mouse.down();
 await page.mouse.move(rect.x+rect.width*.6, rect.y+rect.height*.5, {steps:10}); await page.mouse.up();
 assert.notDeepEqual(await plot.evaluate(el=>el.layout.xaxis.range), before);
 await host.getByRole('button', {name:'Resetuj widok'}).click();
 await host.getByRole('button', {name:'Powiększ / zmniejsz'}).click();
 assert.ok(await host.evaluate(el=>el.classList.contains('chart-expanded')));
 await host.getByRole('button', {name:'Powiększ / zmniejsz'}).click();
 await page.waitForFunction(() => {const p=document.querySelector('.js-plotly-plot'); return Math.abs(p._fullLayout.width-p.clientWidth)<2});
 // Hover readings, wheel zoom, PNG export, and print fallback.
 await page.mouse.move(rect.x+rect.width*.5, rect.y+rect.height*.5);
 await host.locator('.hoverlayer text').first().waitFor();
 const wheelBefore = await plot.evaluate(el=>el.layout.xaxis.range.slice());
 await page.mouse.wheel(0, -250);
 await page.waitForFunction(range => {const r=document.querySelector('.js-plotly-plot').layout.xaxis.range; return r[1]-r[0]<range[1]-range[0]}, wheelBefore);
 await host.getByRole('button', {name:'Resetuj widok'}).click();
 const [download] = await Promise.all([page.waitForEvent('download'), host.locator('[data-title^="Download plot"]').click()]); assert.ok(download.suggestedFilename().endsWith('.png'));
 await page.emulateMedia({media:'print'});
 await host.locator('.chart-fallback img').waitFor({state:'visible'});
 await page.emulateMedia({media:'screen'});
 await page.screenshot({path:'/tmp/srp-charts-desktop.png', fullPage:false});
 await page.setViewportSize({width:390,height:844});
 await page.locator('#sidebar-toggle').click();
 await host.scrollIntoViewIfNeeded();
 await page.waitForFunction(() => {const p=document.querySelector('.js-plotly-plot'); return Math.abs(p._fullLayout.width-p.clientWidth)<2});
 await page.screenshot({path:'/tmp/srp-charts-mobile.png', fullPage:false});
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth+1));
 // Missing JSON must expose the original image and a useful error.
 await page.route('**/*.plot.json', r=>r.fulfill({status:404,body:'missing'}));
 await page.reload(); await page.locator('[data-chart]').first().scrollIntoViewIfNeeded();
 await page.getByRole('status').filter({hasText:'Nie udało się wczytać'}).first().waitFor();
 assert.equal(await page.locator('.chart-fallback').first().getAttribute('open'), '');
 assert.equal(await page.locator('.chart-fallback img').first().evaluate(el=>el.complete && el.naturalWidth > 0), true);
 const noJS = await browser.newPage({javaScriptEnabled:false});
 await noJS.goto(`${base}/R7/tests/static/2026-03-21/index.html`);
 assert.equal(await noJS.locator('.chart-fallback').first().getAttribute('open'), '');
 assert.deepEqual(errors, []);
 console.log(`PASS: ${count} charts; offline, legend, keyboard controls, zoom, pan, reset, expand, mobile, failure and no-JS fallback.`);
 await browser.close();
})().catch(error=>{ console.error(error); process.exit(1); });
