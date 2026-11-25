// Rend _build/og/card.html en public/img/og-rafi.jpg (1200x630, image d'aperçu des liens). Lancer : node _build/og/render.js
// Nécessite playwright (ou playwright-core) et son Chromium.
let pw; try { pw = require('playwright'); } catch (e) { pw = require('playwright-core'); }
const path = require('path');
(async () => {
  const b = await pw.chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });   // CHROME_PATH : Chromium déjà installé (ex. ms-playwright\chromium-1148\chrome-win\chrome.exe)
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'card.html').replace(/\\/g, '/'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForLoadState('networkidle');
  await p.screenshot({ path: path.join(__dirname, '../../public/img/og-rafi.jpg'), type: 'jpeg', quality: 86 });
  await b.close();
})();
