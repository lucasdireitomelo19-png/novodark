// Exporta cada <section class="s"> do carrossel como PNG 1080x1350 (renderiza em 2x e reduz).
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
(async () => {
  const out = path.join(__dirname, '..');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ deviceScaleFactor: 2, viewport: { width: 1080, height: 1350 } });
  await pg.goto('file://' + path.join(__dirname, 'carrossel.html'));
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(400);
  const slides = await pg.locator('section.s').all();
  for (let i = 0; i < slides.length; i++) {
    const f = path.join(out, String(i + 1).padStart(2, '0') + '.png');
    await slides[i].screenshot({ path: f });
    execFileSync('convert', [f, '-filter', 'Lanczos', '-resize', '1080x1350!', f]);
  }
  await b.close(); console.log(slides.length + ' slides');
})();
