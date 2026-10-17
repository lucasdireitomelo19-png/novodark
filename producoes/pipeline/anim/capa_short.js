// Capas verticais de Shorts (1080x1920 JPG), para teste A/B.
// Uso: node capa_short.js <pasta_do_video>   (lê <pasta>/capas.json)
// capas.json: [{"nome": "capa_a", "cena": "escolta", "p": {...}, "t": 3, "l1": "13 OBJETOS", "l2": "ATRÁS DO CAÇA", "tag": "FAB · 1986"}]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const pasta = path.resolve(process.argv[2]);
const lista = JSON.parse(fs.readFileSync(path.join(pasta, 'capas.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await pg.goto('file://' + path.join(__dirname, 'anim.html')); await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate(() => Promise.all([...document.fonts].map(f => f.load())));
  await pg.evaluate(() => window.tamanho(1080, 1920));
  for (const th of lista) {
    await pg.evaluate((th) => {
      window.desenhar(th.cena, th.t ?? 4, 8, th.p || {});
      const c = document.getElementById('c').getContext('2d');
      const g = c.createLinearGradient(0, 0, 0, 760); g.addColorStop(0, 'rgba(0,0,0,.9)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(0, 0, 1080, 760);
      c.textAlign = 'center'; c.textBaseline = 'alphabetic'; c.shadowColor = 'rgba(0,0,0,.95)'; c.shadowBlur = 30;
      const caber = (txt, tam) => { c.font = `${tam}px MX`; while (c.measureText(txt).width > 980 && tam > 60) { tam -= 4; c.font = `${tam}px MX`; } };
      caber(th.l1, 150); c.fillStyle = '#fff'; c.fillText(th.l1, 540, 380);
      caber(th.l2, 150); c.fillStyle = '#e0262b'; c.fillText(th.l2, 540, 540);
      c.shadowBlur = 0; c.font = '44px MX'; c.fillStyle = '#ffb347'; c.letterSpacing = '6px'; c.fillText(th.tag, 540, 640);
    }, th);
    await pg.locator('#c').screenshot({ path: path.join(pasta, `${th.nome}.jpg`), type: 'jpeg', quality: 92 });
  }
  await b.close(); })();
