"""Supports imprimés (autocollant de porte, carte de visite, flyer A6).
Lancer depuis la racine : python3 _build/print.py   (nécessite qrcode + playwright)
Sorties : marketing/*.pdf (à envoyer à l'imprimeur) et marketing/*.png (aperçu).
Les réglages (téléphone, WhatsApp, délai) viennent de build.py : une seule source de vérité."""
import os, sys, io, base64, importlib.util, subprocess, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# On importe les réglages de build.py sans régénérer le site
src = open(os.path.join(ROOT, "_build/build.py"), encoding="utf-8").read().split("# ==================================================================")[0]
cfg = {"__file__": os.path.join(ROOT, "_build/build.py")}; exec(src, cfg)
import urllib.parse, qrcode
WA_LINK = f"https://wa.me/{cfg['WA_NUMBER']}?text=" + urllib.parse.quote(cfg["WA_TEXT"])
def qr_data_uri(data):
    q = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M); q.add_data(data); q.make(fit=True)
    b = io.BytesIO(); q.make_image(fill_color="#0E1A2B", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
def img_uri(path):
    return "data:image/webp;base64," + base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode()
QR = qr_data_uri(WA_LINK)
KEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2"/></svg>'
NAME, PHONE, ETA = cfg["NAME"], cfg["PHONE"], cfg["ETA_MIN"]
BASE_CSS = """@page{margin:0}*{box-sizing:border-box;margin:0;padding:0}body{font-family:Rubik,sans-serif;direction:rtl;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.ph{direction:ltr;unicode-bidi:isolate;font-weight:700;letter-spacing:.01em;white-space:nowrap;text-align:right}.tm{direction:ltr;unicode-bidi:isolate;white-space:nowrap}.mk{background:#1A56DB;color:#fff;border-radius:22%;display:grid;place-items:center}.mk svg{width:62%;height:62%}"""
HEAD = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=block" rel="stylesheet"><style>'

ITEMS = {}
# 1) Autocollant de porte 60x40 mm (à coller près du cylindre après chaque intervention)
ITEMS["autocollant-porte-60x40"] = ("60mm", "40mm", HEAD + BASE_CSS + """
body{width:60mm;height:40mm;background:#1A56DB;color:#fff;padding:3.2mm;display:grid;grid-template-columns:1fr 15mm;gap:2mm;align-items:center}
.t{font-size:3.4mm;font-weight:500;opacity:.9}.n{font-size:4.8mm;font-weight:700;margin:.6mm 0 1mm}.p{font-size:4.9mm}.s{font-size:2.5mm;opacity:.9;margin-top:1mm;line-height:1.35}
.q{background:#fff;border-radius:2mm;padding:1mm;text-align:center}.q img{width:100%;display:block}.q span{color:#1A56DB;font-size:1.9mm;font-weight:700;display:block;margin-top:.3mm}
</style></head><body><div><div class="t">ננעלתם בחוץ?</div><div class="n">""" + NAME + """</div><div class="p ph">""" + PHONE + """</div>
<div class="s">24 שעות בימי חול ובמוצ״ש<br>מגיע תוך כ-""" + str(ETA) + """ דקות</div></div><div class="q"><img src=\"""" + QR + """\"><span>וואטסאפ</span></div></body></html>""")

# 2) Carte de visite 90x50 mm (format israélien), recto + verso dans le même PDF
ITEMS["carte-visite-90x50"] = ("90mm", "50mm", HEAD + BASE_CSS + """
.pg{width:90mm;height:50mm;page-break-after:always;overflow:hidden;position:relative}
.f{background:#fff;padding:6mm;display:flex;flex-direction:column;justify-content:space-between;border:0}
.top{display:flex;align-items:center;gap:3mm}.top .mk{width:11mm;height:11mm}.top b{font-size:6mm;display:block}.top small{font-size:3mm;color:#5B6878}
.f .p{font-size:7.5mm;color:#1A56DB}.f .s{font-size:2.9mm;color:#5B6878;line-height:1.5}
.b{background:#1A56DB;color:#fff;padding:5mm 6mm;display:grid;grid-template-columns:1fr 22mm;gap:4mm;align-items:center}
.b ul{list-style:none;font-size:3.1mm;line-height:1.75}.b li::before{content:"✓ ";font-weight:700}
.b .q{background:#fff;border-radius:2.5mm;padding:1.2mm;text-align:center}.b .q img{width:100%;display:block}.b .q span{color:#1A56DB;font-size:2.2mm;font-weight:700}
</style></head><body><div class="pg f"><div class="top"><div class="mk">""" + KEY + """</div><div><b>""" + NAME + """</b><small>מנעולן – מגיע אליכם בקטנוע</small></div></div>
<div><div class="p ph">""" + PHONE + """</div><div class="s">זמין 24 שעות בימים א׳–ה׳ · שישי <span class="tm">09:00–16:00</span> · מוצ״ש עד חצות</div></div></div>
<div class="pg b"><ul><li>פריצת דלתות ופלדלתות</li><li>החלפת צילינדרים</li><li>תיקון והחלפת מנעולים</li><li>פתיחת כספות</li><li>שדרוג מיגון</li></ul>
<div class="q"><img src=\"""" + QR + """\"><span>שלחו וואטסאפ</span></div></div></body></html>""")

# 3) Flyer A6 105x148 mm pour boîtes aux lettres / tableaux d'immeuble
ITEMS["flyer-A6"] = ("105mm", "148mm", HEAD + BASE_CSS + """
body{width:105mm;height:148mm;display:flex;flex-direction:column;background:#fff}
.ph-img{height:56mm;background:#ddd center/cover no-repeat;position:relative}
.badge{position:absolute;bottom:4mm;right:5mm;background:#fff;border-radius:3mm;padding:2mm 3mm;font-size:3.2mm;color:#5B6878}.badge b{display:block;font-size:5.5mm;color:#0E1A2B}
.c{padding:6mm 7mm 5mm;flex:1;display:flex;flex-direction:column;justify-content:space-between}
h1{font-size:8.6mm;line-height:1.15;margin-bottom:2.5mm}.sub{font-size:3.6mm;color:#5B6878;margin-bottom:4mm}
ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 3mm;font-size:3.4mm;margin-bottom:5mm}li::before{content:"✓ ";color:#16A34A;font-weight:700}
.bot{display:grid;grid-template-columns:1fr 24mm;gap:4mm;align-items:center;background:#1A56DB;color:#fff;border-radius:4mm;padding:4mm}
.bot .p{font-size:7.4mm}.bot small{font-size:2.8mm;opacity:.9;display:block;margin-top:.5mm}
.q{background:#fff;border-radius:2.5mm;padding:1.2mm;text-align:center}.q img{width:100%;display:block}.q span{color:#1A56DB;font-size:2.3mm;font-weight:700}
</style></head><body><div class="ph-img" style="background-image:url('""" + img_uri("public/img/g1.webp") + """')"><div class="badge"><b>~""" + str(ETA) + """ דק׳</b>הגעה בקטנוע</div></div>
<div class="c"><h1>ננעלתם בחוץ?<br>מנעולן קרוב אליכם.</h1><p class="sub">""" + NAME + """ – מחיר ברור לפני העבודה, ישירות מול בעל המקצוע.</p>
<ul><li>פריצת דלתות</li><li>החלפת צילינדר</li><li>תיקון מנעולים</li><li>פתיחת כספות</li><li>שדרוג מיגון</li><li>לבית ולעסק</li></ul>
<div class="bot"><div><div class="p ph">""" + PHONE + """</div><small>24 שעות בימי חול · שישי עד <span class="tm">16:00</span> · מוצ״ש עד חצות</small></div><div class="q"><img src=\"""" + QR + """\"><span>וואטסאפ</span></div></div></div></body></html>""")

OUT = os.path.join(ROOT, "marketing"); os.makedirs(OUT, exist_ok=True)
jobs = []
for name, (w, h, html) in ITEMS.items():
    p = os.path.join(OUT, name + ".html"); open(p, "w", encoding="utf-8").write(html); jobs.append([name, w, h, p])
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const jobs=%s;
for(const [n,w,h,p] of jobs){const pg=await b.newPage({deviceScaleFactor:6,viewport:{width:Math.round(parseFloat(w)*3.78),height:Math.round(parseFloat(h)*3.78)}});
await pg.goto('file://'+p,{waitUntil:'networkidle'});await pg.evaluate(()=>document.fonts.ready);
const ok=await pg.evaluate(()=>document.fonts.check('700 12px Rubik'));if(!ok)throw new Error('Rubik non chargée: '+n);
await pg.pdf({path:p.replace('.html','.pdf'),width:w,height:h,printBackground:true});
await pg.screenshot({path:p.replace('.html','.png'),fullPage:true});console.log('ok',n);}await b.close();})().catch(e=>{console.error(e);process.exit(1)});""" % json.dumps(jobs)
r = subprocess.run(["node", "-e", js]); 
for _, _, _, p in jobs: os.remove(p)
sys.exit(r.returncode)
