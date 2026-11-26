// Test permanent (26 nov. 2026) : alertes ntfy du site = titre clair + page + origine du visiteur, priorité 5.
// Lancer depuis la racine : node _build/test_source.js (aussi dans .github/workflows/site.yml)
const fs = require('fs');
const h = fs.readFileSync('public/index.html', 'utf8');
const m = h.match(/var S=\(function\(\)\{[\s\S]*?\}\)\(\);try\{var s0=[\s\S]*?catch\(e\)\{\}/);
if (!m) { console.log('SNIPPET ABSENT'); process.exit(1); }
const nt = h.includes("priority=5&title='+encodeURIComponent(m)") && h.includes("'\\nVenu par : '+S")
  && h.includes("nt('📞 Client : clic sur « Appeler »')") && h.includes("nt('💬 Client : clic sur WhatsApp')");
console.log('message titre+page+source :', nt);
if (!nt) { console.log('TESTS KO'); process.exit(1); }
function run(search, ref, store) {
  const location = { search, hostname: 'rafihamanulan.co.il' }; const document = { referrer: ref };
  const sessionStorage = { d: store || {}, getItem(k) { return this.d[k] || null; }, setItem(k, v) { this.d[k] = v; } };
  return eval(m[0] + ';S');
}
const cases = [
  ['?gclid=abc', 'https://www.google.com/', 'pub Google Ads'],
  ['', 'https://www.google.co.il/', 'Google gratuit (recherche ou Maps)'],
  ['?utm_source=gbp', '', 'fiche Google'],
  ['', 'https://www.b144.co.il/x', 'autre site : www.b144.co.il'],
  ['', '', 'direct ou lien partagé'],
  ['', 'https://rafihamanulan.co.il/netanya.html', 'direct ou lien partagé'],
];
let ok = true;
for (const [s, r, e] of cases) { const g = run(s, r); if (g !== e) { ok = false; console.log('ECHEC', s, r, '=>', g); } }
const st = {}; run('?gclid=1', 'https://www.google.com/', st);
const g2 = run('', 'https://rafihamanulan.co.il/a.html', st);
if (g2 !== 'pub Google Ads') { ok = false; console.log('ECHEC mémoire', g2); }
console.log(ok ? 'TESTS OK (' + (cases.length + 1) + ')' : 'TESTS KO');
if (!ok) process.exit(1);
