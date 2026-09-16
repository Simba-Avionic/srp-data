const {chromium} = require('playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const base = process.env.CHARTS_URL || 'http://127.0.0.1:8765';
  for (const width of [1280, 390]) {
    await page.setViewportSize({width, height: 950});
    await page.goto(`${base}/R7/tests/launch/2025-05-31/index.html`);
    const frame = page.frameLocator('iframe');
    await frame.locator('.js-plotly-plot').nth(7).waitFor();
    assert.equal(await frame.locator('.js-plotly-plot').count(), 8);
    const plots = frame.locator('.js-plotly-plot');
    assert.equal(await frame.locator('.flight-phases').count(), 8);
    for (let i = 0; i < 8; i++) {
      assert.equal(await frame.locator('input[type=checkbox]').nth(i).isChecked(), true);
      assert.ok(await plots.nth(i).evaluate(plot => plot.layout.shapes.length > 0));
      const phases = frame.locator('.flight-phases').nth(i);
      assert.equal(await phases.isVisible(), true);
      assert.ok((await phases.innerText()).includes('THRUST'));
      assert.ok(await phases.locator('li').evaluateAll(items => items.every((item, i) => {
        const a = item.getBoundingClientRect();
        return items.slice(i+1).every(other => {const b=other.getBoundingClientRect(); return a.right<=b.left || b.right<=a.left || a.bottom<=b.top || b.bottom<=a.top;});
      })));
    }
    for (let i = 0; i < 8; i++) {
      const geometry = await plots.nth(i).evaluate(plot => ({
        width: plot.clientWidth, svg: plot._fullLayout.width,
        annotations: plot.layout.annotations.length,
        xTitle: plot.layout.xaxis.title.text, yTitle: plot.layout.yaxis.title.text,
        legend: plot.querySelector('.legend').getBoundingClientRect().toJSON(),
        area: plot.querySelector('.nsewdrag').getBoundingClientRect().toJSON(),
      }));
      assert.ok(Math.abs(geometry.width - geometry.svg) < 2);
      assert.equal(geometry.annotations, 0);
      assert.equal(geometry.xTitle, 'Czas [s]');
      assert.ok(geometry.yTitle);
      assert.ok(geometry.legend.top >= geometry.area.bottom);
    }
    await frame.locator('summary').click();
    assert.ok(await frame.locator('tbody tr').count() > 5);
    assert.ok(await frame.locator('tbody').innerText().then(text => text.includes('ev_liftoff') && text.includes('Faza:')));
    await frame.locator('summary').click();
    const first = plots.first();
    await frame.locator('input[type=checkbox]').first().check();
    assert.ok(await first.evaluate(plot => plot.layout.shapes.length > 0));
    assert.equal(await first.evaluate(plot => plot.layout.annotations.length), 0);
    await frame.locator('input[type=checkbox]').first().uncheck();
    assert.equal(await first.evaluate(plot => plot.layout.shapes.length), 0);
    assert.equal(await frame.locator('.flight-phases').first().isVisible(), false);
    await frame.locator('input[type=checkbox]').first().check();
    assert.equal(await frame.locator('.flight-phases').first().isVisible(), true);
    await first.locator('.legendtoggle').click();
    await first.evaluate(plot => new Promise(resolve => {
      if (plot.data[0].visible === 'legendonly') resolve();
      else plot.once('plotly_restyle', resolve);
    }));
    assert.equal(await first.evaluate(plot => plot.data[0].visible), 'legendonly');
    await frame.getByRole('button', {name: 'Resetuj widok'}).first().click();
    assert.equal(await first.evaluate(plot => plot.layout.xaxis.autorange), true);
    await first.locator('.legendtoggle').click();
    await first.locator('.scatterlayer .trace').waitFor({state: 'visible'});
    await page.locator('iframe').scrollIntoViewIfNeeded();
    await page.screenshot({path:`/tmp/launch-${width}.png`});
    const framePage = page.frames().find(f => f.url().includes('fl004_plots'));
    assert.ok(await framePage.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
  }
  // The downloadable standalone report must also respond to viewport changes.
  await page.goto(`${base}/R7/tests/launch/2025-05-31/fl004_plots_09142026_190818.html`);
  await page.locator('.js-plotly-plot').nth(7).waitFor();
  await page.setViewportSize({width: 800, height: 950});
  await page.waitForFunction(() => [...document.querySelectorAll('.js-plotly-plot')].every(p => Math.abs(p._fullLayout.width-p.clientWidth)<2));
  assert.deepEqual(errors, []);
  console.log('PASS: 8 launch plots; desktop/mobile iframe, standalone resize, readable legends, event table/toggles, trace legend and reset.');
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
