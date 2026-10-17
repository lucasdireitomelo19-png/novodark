// Renderiza logo e capa do canal em PNG (Chromium do Playwright).
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ deviceScaleFactor: 1 }); const url = f => 'file://' + path.join(__dirname, f);
  await pg.setViewportSize({ width: 800, height: 800 }); await pg.goto(url('logo.html'));
  await pg.locator('#logo').screenshot({ path: path.join(__dirname, 'logo_inquerito_sombrio_800x800.png') });
  await pg.goto(url('logo.html') + '?transp=1'); await pg.locator('#logo').screenshot({ path: path.join(__dirname, 'lupa_transparente.png'), omitBackground: true });
  if (require('fs').existsSync(path.join(__dirname, 'capa.html'))) {
    await pg.setViewportSize({ width: 2560, height: 1440 });
    for (const [h, nome] of [['', 'capa_inquerito_sombrio_2560x1440.png'], ['?guias=1', 'capa_guias.png']]) {
      await pg.goto(url('capa.html' + h)); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
      await pg.locator('#capa').screenshot({ path: path.join(__dirname, nome) }); }
  }
  await b.close(); })();
