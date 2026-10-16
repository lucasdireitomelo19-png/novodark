// Renderiza cenas do anim.html em MP4 (1920x1080, 30 fps).
// Uso: node render_anim.js jobs.json   (jobs: [{saida, cena, dur, p}])
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

(async () => {
  const k = +(process.argv[3] || 0), n = +(process.argv[4] || 1);
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).filter((_, i) => i % n === k);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'anim.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.fonts].map(f => f.load())));
  for (const j of jobs) {
    if (fs.existsSync(j.saida) && fs.existsSync(j.saida + '.key') && fs.readFileSync(j.saida + '.key', 'utf8') === JSON.stringify(j)) continue;
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-i', '-',
      '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', j.saida]);
    const n = Math.round(j.dur * 30);
    for (let i = 0; i < n; i++) {
      const b64 = await page.evaluate(([c, t, d, p]) => { window.desenhar(c, t, d, p);
        return document.getElementById('c').toDataURL('image/jpeg', 0.92).split(',')[1]; }, [j.cena, i / 30, j.dur, j.p || {}]);
      if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    fs.writeFileSync(j.saida + '.key', JSON.stringify(j));
    console.log('ok', path.basename(j.saida), j.dur + 's');
  }
  await browser.close();
})();
