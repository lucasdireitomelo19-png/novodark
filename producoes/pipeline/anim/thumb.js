// Thumbnails A/B do vídeo das máscaras de chumbo (1920x1080 -> JPG 1280x720 com ffmpeg).
// Uso: node thumb.js <pasta_do_video>
const { chromium } = require('playwright'); const path = require('path');
const pasta = path.resolve(process.argv[2]);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('file://' + path.join(__dirname, 'anim.html')); await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate(() => Promise.all([...document.fonts].map(f => f.load())));
  for (const [nome, cena, l1, l2, sub] of [
    ['thumb_a', 'mascara', 'NUNCA', 'RESOLVIDO', 'O caso das máscaras de chumbo'],
    ['thumb_b', 'morro', 'AGUARDAR', 'SINAL', 'Encontrados mortos com máscaras de chumbo'],
  ]) {
    await pg.evaluate(([cena, l1, l2, sub]) => {
      if (cena === 'mascara') { window.desenhar('mascara', 4, 8, {}); fundo('#0b0d10', '#020203');
        const lg = ctx.createRadialGradient(1350, 540, 50, 1350, 540, 800); lg.addColorStop(0, 'rgba(150,160,180,.35)'); lg.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = lg; ctx.fillRect(0, 0, 1920, 1080);
        lente(1600, 640, 1.25, -0.12, 1.2, 0); vinheta(0.7); }
      else window.desenhar('morro', 5, 8, { luz: 1, corpos: 1, vel: 0, zoom: 0.12 });
      const c = document.getElementById('c').getContext('2d');
      const g = c.createLinearGradient(0, 0, 1150, 0); g.addColorStop(0, 'rgba(0,0,0,.92)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(0, 0, 1150, 1080);
      c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.shadowColor = 'rgba(0,0,0,.9)'; c.shadowBlur = 30;
      c.font = '190px MX'; c.fillStyle = '#fff'; c.fillText(l1, 80, 430);
      c.font = '190px MX'; c.fillStyle = '#e0262b'; c.fillText(l2, 80, 630);
      c.shadowBlur = 0; c.font = '54px MM'; c.fillStyle = 'rgba(255,255,255,.92)'; c.fillText(sub, 88, 750);
      c.fillStyle = '#e0262b'; c.fillRect(88, 790, 160, 8);
      c.font = '40px MX'; c.fillStyle = '#ffb347'; c.fillText('NITERÓI · 1966', 88, 870);
    }, [cena, l1, l2, sub]);
    await pg.locator('#c').screenshot({ path: path.join(pasta, `${nome}.png`) });
  }
  await b.close(); })();
