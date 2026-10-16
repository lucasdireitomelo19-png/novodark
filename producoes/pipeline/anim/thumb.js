// Thumbnails A/B (1920x1080 PNG; depois converta para JPG 1280x720 com ffmpeg).
// Uso: node thumb.js <pasta_do_video>   (lê <pasta>/thumbs.json)
// thumbs.json: [{"nome": "thumb_a", "cena": "mascara", "p": {...}, "l1": "NUNCA", "l2": "RESOLVIDO", "sub": "...", "tag": "NITERÓI · 1966"}]
// cena "mascara_lado" desenha a máscara de chumbo à direita (thumb do vídeo 01).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const pasta = path.resolve(process.argv[2]);
const lista = JSON.parse(fs.readFileSync(path.join(pasta, 'thumbs.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('file://' + path.join(__dirname, 'anim.html')); await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate(() => Promise.all([...document.fonts].map(f => f.load())));
  for (const th of lista) {
    await pg.evaluate((th) => {
      if (th.cena === 'mascara_lado') { window.desenhar('mascara', 4, 8, {}); fundo('#0b0d10', '#020203');
        const lg = ctx.createRadialGradient(1350, 540, 50, 1350, 540, 800); lg.addColorStop(0, 'rgba(150,160,180,.35)'); lg.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = lg; ctx.fillRect(0, 0, 1920, 1080);
        lente(1600, 640, 1.25, -0.12, 1.2, 0); vinheta(0.7); }
      else window.desenhar(th.cena, th.t ?? 5, 8, th.p || {});
      const c = document.getElementById('c').getContext('2d');
      const g = c.createLinearGradient(0, 0, 1150, 0); g.addColorStop(0, 'rgba(0,0,0,.92)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(0, 0, 1150, 1080);
      c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.shadowColor = 'rgba(0,0,0,.9)'; c.shadowBlur = 30;
      const caber = (txt, tam) => { c.font = `${tam}px MX`; while (c.measureText(txt).width > 1100 && tam > 60) { tam -= 6; c.font = `${tam}px MX`; } };
      caber(th.l1, 190); c.fillStyle = '#fff'; c.fillText(th.l1, 80, 430);
      caber(th.l2, 190); c.fillStyle = '#e0262b'; c.fillText(th.l2, 80, 630);
      c.shadowBlur = 0; c.font = '54px MM'; c.fillStyle = 'rgba(255,255,255,.92)'; c.fillText(th.sub, 88, 750);
      c.fillStyle = '#e0262b'; c.fillRect(88, 790, 160, 8);
      c.font = '40px MX'; c.fillStyle = '#ffb347'; c.fillText(th.tag, 88, 870);
    }, th);
    await pg.locator('#c').screenshot({ path: path.join(pasta, `${th.nome}.png`) });
  }
  await b.close(); })();
