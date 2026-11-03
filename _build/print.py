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

# 4) Stickers scooter (vinyle extérieur) : fond noir, illustration serrure, format en largeur.
SITE_HOST = cfg["SITE_URL"].split("//")[1]
LOCK_ART = """<svg viewBox="0 0 220 220" fill="none" stroke-linecap="round" stroke-linejoin="round">
<rect x="70" y="8" width="62" height="204" rx="31" fill="#1A56DB" stroke="#3D74F0" stroke-width="3"/>
<circle cx="101" cy="62" r="17" fill="#0B0B0D" stroke="#C9D3E3" stroke-width="5"/>
<path d="M101 62H18" stroke="#C9D3E3" stroke-width="17"/><circle cx="18" cy="62" r="8.5" fill="#C9D3E3"/>
<rect x="85" y="128" width="32" height="54" rx="16" fill="#0B0B0D" stroke="#C9D3E3" stroke-width="5"/>
<circle cx="101" cy="145" r="7" fill="#C9D3E3"/><path d="M101 150v18" stroke="#C9D3E3" stroke-width="6"/>
<path d="M101 152h70" stroke="#F5A524" stroke-width="9"/><path d="M128 152v11M142 152v8" stroke="#F5A524" stroke-width="7"/>
<circle cx="190" cy="152" r="20" stroke="#F5A524" stroke-width="9" fill="#0B0B0D"/></svg>"""
SC_CSS = """body{background:#0B0B0D;color:#fff;display:grid;align-items:center}
.nm{font-weight:700;line-height:1}.act{font-weight:500;color:#C9D3E3;line-height:1.2}
.chips{display:flex;flex-wrap:wrap;gap:2mm}.chips span{border:.5mm solid #3D74F0;color:#fff;border-radius:99mm;padding:1mm 3.5mm;font-weight:500}
.phone{font-weight:700;line-height:1;direction:ltr;unicode-bidi:isolate;white-space:nowrap;text-align:right;color:#fff}
.phone b{color:#3D74F0}.bar{height:1.2mm;background:#1A56DB;border-radius:1mm}
.url{direction:ltr;unicode-bidi:isolate;font-weight:500;color:#C9D3E3;text-align:right}
.art svg{width:100%;height:auto;display:block}.q{background:#fff;border-radius:6%;padding:1.3%}.q img{width:100%;display:block}"""
def scooter(w, h, k):  # k = facteur d'échelle par rapport au 30x15
    return HEAD + BASE_CSS + SC_CSS + f"""
body{{width:{w}mm;height:{h}mm;padding:{11*k}mm {14*k}mm;grid-template-columns:1fr {78*k}mm;gap:{9*k}mm}}
.nm{{font-size:{19*k}mm}}.act{{font-size:{8*k}mm;margin:{2*k}mm 0 {4*k}mm}}.chips span{{font-size:{5.2*k}mm}}
.phone{{font-size:{24*k}mm;margin:{5*k}mm 0 {3*k}mm}}.bar{{width:{70*k}mm;margin:0 0 {3*k}mm auto}}.url{{font-size:{6.5*k}mm}}
.side{{display:flex;flex-direction:column;align-items:center;gap:{3*k}mm}}.art{{width:{70*k}mm}}.q{{width:{26*k}mm}}
</style></head><body><div><div class="nm">{NAME}</div><div class="act">מנעולן – מגיע אליכם בקטנוע</div>
<div class="chips"><span>פריצת דלתות</span><span>צילינדרים</span><span>מנעולים</span><span>כספות</span></div>
<div class="phone">{PHONE}</div><div class="bar"></div><div class="url">{SITE_HOST}</div></div>
<div class="side"><div class="art">{LOCK_ART}</div><div class="q"><img src="{QR}"></div></div></body></html>"""
ITEMS["sticker-scooter-30x15"] = ("300mm", "150mm", scooter(300, 150, 1))      # flanc / dossier du scooter

def band(w, h):  # bandeau très allongé : arrière du top case, sous les verrous
    k = h / 110
    return HEAD + BASE_CSS + SC_CSS + f"""
body{{width:{w}mm;height:{h}mm;padding:{9*k}mm {14*k}mm;grid-template-columns:{58*k}mm auto 1fr {54*k}mm;gap:{11*k}mm}}
.art{{width:{58*k}mm}}.nm{{font-size:{17*k}mm}}.act{{font-size:{6.8*k}mm;margin-top:{2.5*k}mm}}
.phone{{font-size:{27*k}mm}}.url{{font-size:{6.2*k}mm;margin-top:{3*k}mm;text-align:center}}.q{{width:{54*k}mm}}
.mid{{display:flex;flex-direction:column;align-items:center}}
</style></head><body><div class="art">{LOCK_ART}</div>
<div><div class="nm">{NAME}</div><div class="act">מנעולן · פריצת דלתות · צילינדרים</div></div>
<div class="mid"><div class="phone">{PHONE}</div><div class="url">{SITE_HOST}</div></div>
<div class="side"><div class="q"><img src="{QR}"></div></div></body></html>"""

def square(w, h):  # presque carré : côtés du top case
    k = w / 180
    return HEAD + BASE_CSS + SC_CSS + f"""
body{{width:{w}mm;height:{h}mm;padding:{12*k}mm;display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center}}
.art{{width:{58*k}mm}}.nm{{font-size:{17*k}mm}}.act{{font-size:{6.2*k}mm;margin-top:{2*k}mm}}
.phone{{font-size:{19*k}mm;text-align:center}}.bot{{display:flex;align-items:center;gap:{6*k}mm}}.q{{width:{30*k}mm}}.url{{font-size:{5.6*k}mm}}
</style></head><body><div class="art">{LOCK_ART}</div><div><div class="nm">{NAME}</div><div class="act">מנעולן · פריצת דלתות · צילינדרים</div></div>
<div class="phone">{PHONE}</div><div class="bot"><div class="url">{SITE_HOST}</div><div class="q"><img src="{QR}"></div></div></body></html>"""

ITEMS["sticker-topcase-arriere-48x11"] = ("480mm", "110mm", band(480, 110))   # arrière du top case (sous les verrous)
ITEMS["sticker-topcase-cote-18x16"] = ("180mm", "160mm", square(180, 160))    # côtés du top case (x2)

OUT = os.path.join(ROOT, "marketing"); os.makedirs(OUT, exist_ok=True)
jobs = []
for name, (w, h, html) in ITEMS.items():
    p = os.path.join(OUT, name + ".html"); open(p, "w", encoding="utf-8").write(html); jobs.append([name, w, h, p])
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const jobs=%s;
for(const [n,w,h,p] of jobs){const pg=await b.newPage({deviceScaleFactor:(parseFloat(w)>150?2.5:6),viewport:{width:Math.round(parseFloat(w)*3.78),height:Math.round(parseFloat(h)*3.78)}});
await pg.goto('file://'+p,{waitUntil:'networkidle'});await pg.evaluate(()=>document.fonts.ready);
const ok=await pg.evaluate(()=>document.fonts.check('700 12px Rubik'));if(!ok)throw new Error('Rubik non chargée: '+n);
await pg.pdf({path:p.replace('.html','.pdf'),width:w,height:h,printBackground:true});
await pg.screenshot({path:p.replace('.html','.png'),fullPage:true});console.log('ok',n);}await b.close();})().catch(e=>{console.error(e);process.exit(1)});""" % json.dumps(jobs)
r = subprocess.run(["node", "-e", js]); 
for _, _, _, p in jobs: os.remove(p)
sys.exit(r.returncode)
