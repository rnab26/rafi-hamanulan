"""Générateur du site « רפי המנעולן ».

Lancer depuis la racine du dépôt :  python3 _build/build.py
Tout ce qui est réglable est dans la section RÉGLAGES ci-dessous (une seule source de vérité).
"""
import os, json, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du repo
OUT = os.path.join(ROOT, "public")  # SEUL dossier publié par Render (Publish Directory = public)
# Transition : tant que Render publie encore la racine (« ./ »), on recopie le site à la racine.
# Passer à False dès que Render publie « public », puis supprimer les copies à la racine.
LEGACY_ROOT_COPY = False

# ============================ RÉGLAGES ============================
# URL publique du site. Quand le domaine rafihamanulan.co.il sera acheté et relié à Render,
# remplacer UNIQUEMENT cette ligne, relancer le script, commit, push.
SITE_URL = "https://rafihamanulan.co.il"
NAME = "רפי המנעולן"
PHONE_INTL = "+972545301389"
PHONE = "054-530-1389"
WA_NUMBER = "972545301389"
WA_TEXT = "שלום רפי, אני צריך מנעולן. הכתובת שלי: "   # message pré-rempli WhatsApp
CONTENT_DATE = "2026-11-01"                         # date de dernière mise à jour du contenu (sitemap, articles) – à changer quand le contenu change
ETA_MIN = 25                                        # délai d'arrivée annoncé (minutes)
REGION = "השרון"                                    # zone affichée. Volontairement AUCUNE ville de départ (demande de Rafi, 1er nov. 2026)
# Horaires : jour (0=dimanche … 6=samedi) -> liste de créneaux (heure début, heure fin), fin 24 = minuit
HOURS = {0: [(0, 24)], 1: [(0, 24)], 2: [(0, 24)], 3: [(0, 24)], 4: [(0, 24)], 5: [(9, 16)], 6: [(19, 24)]}
HOURS_DISPLAY = [("ראשון – חמישי", "24 שעות"), ("שישי", "09:00–16:00"), ("מוצאי שבת", "19:00–00:00")]
# Code de vérification Google Search Console (balise HTML) : coller seulement la valeur content="..."
GSC_VERIFICATION = ""
# Lien « laisser un avis » de la fiche Google Business (quand elle sera vérifiée). Vide = bouton masqué.
REVIEW_URL = "https://g.page/r/CavM3AVwHYkIEBM/review"
# Clé IndexNow (Bing/Yandex) : fichier <clé>.txt publié à la racine. Ne pas changer sans republier.
# Google Ads – suivi des conversions (appel / WhatsApp). Vide = aucun script Google Ads sur le site.
# Valeurs à recopier depuis Google Ads → Objectifs → Conversions → la conversion → « Configurer la balise ».
GADS_ID = "AW-18553668064"            # ex. "AW-123456789"
GADS_LABEL_CALL = "NJHACOy_prEdEOCDio9F"    # libellé de la conversion « Clic sur appel »   (la partie après le « / » de send_to)
GADS_LABEL_WA = "S4QNCO-_prEdEOCDio9F"      # libellé de la conversion « Clic WhatsApp »
INDEXNOW_KEY = "b8684d5c82d2840ec10bbd84289ad0c2"
# ==================================================================

WA = f"https://wa.me/{WA_NUMBER}"
WA_LINK = WA + "?text=" + __import__("urllib.parse").parse.quote(WA_TEXT)
TODAY = CONTENT_DATE  # date fixe : le site régénéré un autre jour reste identique (contrôle GitHub)

I = {  # icônes trait 24x24
"door":'<path d="M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17"/><path d="M3 21h18"/><circle cx="14.5" cy="12" r="1"/>',
"tag":'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
"user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
"phone":'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
"pin":'<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
"scooter":'<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M9 17h6l3-7h-3M15 10l-2-5h-3M6 14l2-4h4"/>',
"check":'<path d="M5 12l5 5L20 7"/>',
"key":'<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2"/>',
"shield":'<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
"chat":'<path d="M4 5h16v11H8l-4 4z"/>',
"arrow":'<path d="M15 6l-6 6 6 6"/>',
}
def ic(n, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'
WA_SVG = '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'

# (slug, nom, "ב+nom", quartiers/secteurs couverts)
CITIES = [
("netanya","נתניה","בנתניה","רמת פולג, עין התכלת, קריית השרון, קריית צאנז, אגמים, נאות גנים, דורה ומרכז העיר"),
("hadera","חדרה","בחדרה","מרכז העיר, גבעת אולגה, נווה חיים והשכונות החדשות"),
("caesarea","קיסריה","בקיסריה","השכונות, הבתים הפרטיים ופארק התעשייה"),
("or-akiva","אור עקיבא","באור עקיבא","כל שכונות העיר"),
("kfar-yona","כפר יונה","בכפר יונה","השכונות הוותיקות והחדשות"),
("even-yehuda","אבן יהודה","באבן יהודה","המושבה והבתים הפרטיים"),
("kadima-zoran","קדימה-צורן","בקדימה-צורן","קדימה וצורן"),
("tel-mond","תל מונד","בתל מונד","כל היישוב"),
("pardesiya","פרדסיה","בפרדסיה","כל היישוב"),
("kfar-saba","כפר סבא","בכפר סבא","כל שכונות העיר"),
("raanana","רעננה","ברעננה","כל שכונות העיר"),
("herzliya","הרצליה","בהרצליה","הרצליה פיתוח, מרכז העיר והשכונות"),
("hod-hasharon","הוד השרון","בהוד השרון","כל שכונות העיר"),
("moshavim","מושבי השרון","במושבי השרון","אודים, יקום, מכמורת, כפר ויתקין, בית יהושע, חבצלת השרון, אביחיל ועוד"),
]
# (slug, nom, image, phrase courte, ce qui est inclus, mots-clés secondaires pour la description)
SERVICES = [
("door-opening","פריצת דלתות","door-opening","ננעלתם בחוץ? פותח את הדלת ללא נזק ככל שניתן.",
 ["דלת כניסה ופלדלת","דלתות פנים וחדרי אמבטיה","מפתח שנשבר בתוך המנעול","מפתח שנשאר בצד הפנימי"],"פורץ דלתות ופורץ מנעולים"),
("cylinder","החלפת צילינדר","cylinder","אחרי מעבר דירה, אובדן מפתחות או פריצה.",
 ["צילינדרים רגילים ומוגנים – מולטילוק, רב-בריח, מגנום ועוד","החלפה אחרי מעבר דירה","החלפה אחרי פריצה או אובדן מפתחות","מפתח אחד לכמה דלתות"],"החלפת צילינדר מולטילוק ורב-בריח"),
("lock-repair","תיקון והחלפת מנעולים","lock-repair","מנעול תקוע, ידית שבורה, דלת שלא נסגרת.",
 ["מנעולי רב-בריח","ידיות ומנגנונים","מנעולים לשערים ולתיבות דואר","כיוון דלת שנתקעת"],"תיקון מנעולים ומנעולי רב-בריח"),
("safe","פתיחת כספות","safe","קוד שנשכח או מנגנון שנתקע.",
 ["כספות עם קוד","כספות עם מפתח","החלפת קוד אחרי פתיחה"],"פריצת כספות"),
("security","שדרוג מיגון","security","בדיקת הדלת והמנעולים והמלצה במחיר ברור.",
 ["שדרוג צילינדר ומנעולים","התקנת מנעול כספת / מנעול נוסף לפלדלת","מיגון לעסקים ולמחסנים"],"שדרוג מיגון לדלת"),
]
FAQ = [
("תוך כמה זמן אתה מגיע?",f"אני עובד בקטנוע בכל אזור {REGION}, אז גם בפקקים אני מגיע בדרך כלל תוך כ-{ETA_MIN} דקות, מקיסריה ועד הוד השרון."),
("אני יודע כמה זה יעלה לפני שמתחילים?","כן. אחרי שאני רואה את הדלת או המנעול אני אומר מחיר ברור, ורק אחרי שאתם מאשרים מתחילים לעבוד."),
("הדלת תיפגע בזמן הפריצה?","ברוב המקרים אפשר לפתוח ללא נזק לדלת. אם צריך להחליף את הצילינדר אחרי הפתיחה, אני מחליף אותו באותו ביקור."),
("מתי אתה זמין?","24 שעות בימים ראשון עד חמישי, ביום שישי מ-09:00 עד 16:00, ובמוצאי שבת עד חצות."),
("מה עושים אחרי פריצה לבית?","מומלץ להחליף צילינדר כמה שיותר מהר. אני מגיע, מחליף ויכול להמליץ על שדרוג מיגון לדלת."),
]

# ------------------------------------------------------------------ CSS
CSS = r"""
@font-face{font-family:'Rubik';font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/rubik-hebrew.woff2) format('woff2');unicode-range:U+0307-0308,U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}
@font-face{font-family:'Rubik';font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/rubik-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
:root{--bg:#fff;--soft:#F5F7FB;--ink:#0E1A2B;--muted:#5B6878;--line:#E6EBF2;--blue:#1A56DB;--blue-d:#1446B4;--blue-soft:#EAF0FD;--wa:#18A957;--amber:#F5A524;--green:#16A34A;--r:20px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Rubik",Arial,sans-serif;font-size:17px;line-height:1.6;padding-bottom:84px}
a{color:var(--blue)}h1,h2,h3{line-height:1.2;margin:0;font-weight:700}p{margin:0}
img{display:block;max-width:100%;height:auto}
a:focus-visible,summary:focus-visible{outline:3px solid var(--amber);outline-offset:2px;border-radius:8px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.ic{width:22px;height:22px;flex:none}
/* header */
.hd{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700;font-size:19px}
.logo .mk{width:34px;height:34px;border-radius:10px;background:var(--blue);color:#fff;display:grid;place-items:center}
.logo .mk .ic{width:20px;height:20px}
.pill{display:inline-flex;align-items:center;gap:6px;color:var(--blue);text-decoration:none;font-weight:700;font-size:16px}
.pill span{direction:ltr}.pill .ic{width:18px;height:18px}
/* hero */
.hero{padding:20px 0 8px}
.hero .wrap{display:grid;gap:24px}
.hero-img{position:relative;border-radius:24px;overflow:hidden;aspect-ratio:4/3;background:var(--soft)}
.hero-img img{width:100%;height:100%;object-fit:cover}
.eta-badge{position:absolute;bottom:14px;inset-inline-start:14px;background:#fff;border-radius:16px;padding:10px 14px;display:flex;align-items:center;gap:10px;box-shadow:0 6px 20px rgba(14,26,43,.18)}
.eta-badge .ic{color:var(--blue)}.eta-badge b{display:block;font-size:20px;line-height:1}.eta-badge small{color:var(--muted);font-size:13px}
@media(min-width:880px){.hero{padding:56px 0 24px}.hero .wrap{grid-template-columns:1fr 1fr;align-items:center;gap:56px}.hero-img{aspect-ratio:4/5;grid-column:2;grid-row:1/3;max-height:560px}.hero-txt{grid-column:1;grid-row:1}.trust{grid-column:1;grid-row:2;align-self:start}}
.status{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;color:var(--muted)}
.dot{width:8px;height:8px;border-radius:50%;background:var(--muted)}
.status.on{color:var(--green)}.status.on .dot{background:var(--green);box-shadow:0 0 0 4px rgba(22,163,74,.16)}
.hero h1{font-size:clamp(34px,7vw,56px);letter-spacing:-.015em;margin:10px 0 12px}
.hero .sub{color:var(--muted);font-size:19px;margin:0 0 28px}
.cta{display:grid;gap:10px;max-width:440px;grid-template-columns:1fr 1fr}
.btn{display:flex;align-items:center;justify-content:center;gap:8px;min-height:54px;border-radius:14px;font-weight:700;font-size:17px;text-decoration:none;padding:0 16px}
.btn-call{background:var(--blue);color:#fff}.btn-call:hover{background:var(--blue-d)}
.btn-wa{background:var(--wa);color:#fff}
.crumb{font-size:14px;color:var(--muted);margin-bottom:14px}.crumb a{color:var(--muted);text-decoration:none}
/* trust */
.trust{display:grid;gap:14px;grid-template-columns:repeat(3,1fr);list-style:none;margin:0;padding:28px 0 0}
.trust li{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;font-size:14px;color:var(--muted);line-height:1.35}
.trust .ic{width:44px;height:44px;padding:11px;border-radius:14px;background:var(--blue-soft);color:var(--blue)}

/* sections */
.sec{padding:64px 0}.sec.alt{background:var(--soft)}
.sec h2{font-size:clamp(26px,4.6vw,36px);letter-spacing:-.01em;margin-bottom:28px}
.sec h2 small{display:block;font-size:17px;font-weight:400;color:var(--muted);margin-top:8px;letter-spacing:0}
.intro{font-size:18px;color:var(--muted);max-width:60ch;margin:-12px 0 28px}
/* services: tuiles photo */
.tiles{display:grid;gap:14px;grid-template-columns:repeat(2,1fr)}
@media(min-width:760px){.tiles{grid-template-columns:repeat(3,1fr);gap:20px}}
.tile{display:block;text-decoration:none;color:var(--ink)}
.tile img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;background:var(--soft);transition:transform .2s}
.tile:hover img{transform:scale(1.02)}
.tile h3{font-size:17px;margin-top:10px;display:flex;align-items:center;justify-content:space-between;gap:6px}
.tile h3 .ic{width:18px;height:18px;color:var(--blue)}
.gal{display:grid;gap:8px;grid-template-columns:repeat(3,1fr);list-style:none;margin:0;padding:0}
@media(min-width:760px){.gal{grid-template-columns:repeat(6,1fr);gap:12px}}
.gal img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px;background:var(--soft)}
/* étapes */
.steps{display:grid;gap:28px;grid-template-columns:1fr;list-style:none;margin:0;padding:0}
@media(min-width:760px){.steps{grid-template-columns:repeat(3,1fr)}}
.steps li{display:flex;gap:16px;align-items:flex-start}
.steps .ic{width:52px;height:52px;padding:13px;border-radius:16px;background:#fff;color:var(--blue);box-shadow:0 2px 10px rgba(14,26,43,.06)}
.steps h3{font-size:18px;margin:4px 0 2px}.steps p{color:var(--muted);font-size:15px}
/* zones */
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:0;padding:0}
.chips a{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 16px;text-decoration:none;color:var(--ink);font-size:15px}
.chips a:hover{border-color:var(--blue);color:var(--blue)}
/* faq + horaires */
.two{display:grid;gap:48px}@media(min-width:880px){.two{grid-template-columns:3fr 2fr}}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;padding:18px 0;font-weight:500;display:flex;justify-content:space-between;gap:12px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:24px;line-height:1;color:var(--blue)}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 0 18px;color:var(--muted)}
.hours div{display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid var(--line)}
.hours b{font-weight:500}.hours span{direction:ltr;color:var(--muted)}
.note{color:var(--muted);font-size:15px;margin-top:14px}
/* page service */
.incl{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.incl li{display:flex;gap:12px;align-items:center;font-size:17px}
.incl .ic{width:28px;height:28px;padding:5px;border-radius:50%;background:#E7F6EC;color:var(--green)}
/* prix */
.pgrid{display:grid;gap:16px;grid-template-columns:1fr}@media(min-width:760px){.pgrid{grid-template-columns:repeat(2,1fr)}}
.pcard{background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden}
.pcard img{width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--soft)}
.pcard.solo{max-width:560px}.pbody{padding:18px 20px}.pbody h3,.pbody h2{font-size:19px;margin:0 0 8px}
.prows{list-style:none;margin:0;padding:0}.prows li{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px dashed var(--line)}.prows li span{flex:1}
.pth{width:56px;height:56px;border-radius:12px;object-fit:cover;flex:none;background:var(--soft)}.pth.ph{display:grid;place-items:center;color:var(--blue)}.pcard .pth{width:56px;height:56px;aspect-ratio:1}
.prows li:last-child{border:0}.prows b{white-space:nowrap;color:var(--blue)}.prows b.long{white-space:normal;text-align:left;max-width:55%}
.pnote{color:var(--muted);font-size:14px;margin-top:8px}.pnotes{color:var(--muted);font-size:15px;margin:20px 0 0;padding-inline-start:20px}
/* articles */
.art{max-width:720px}.art h1{font-size:clamp(28px,6vw,40px);margin:8px 0 14px}.art .intro{margin:0 0 24px}
.art img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px;margin-bottom:12px}
.art h2{font-size:22px;margin:32px 0 10px}.art p,.art li{color:#2B3A4D}.art ul{padding-inline-start:20px;margin:0}.art li{margin-bottom:8px}
.cta-box{background:var(--soft);border-radius:20px;padding:22px;margin:36px 0 8px}.cta-box b{display:block;font-size:19px;margin-bottom:14px}
.links{list-style:none;padding:0;margin:0}.links li{border-bottom:1px solid var(--line)}.links a{display:block;padding:14px 0;text-decoration:none;color:var(--ink);font-weight:500}.links a:hover{color:var(--blue)}
/* bandeau final */
.band{text-align:center;padding:72px 0}
.band h2{font-size:clamp(28px,5vw,40px);margin-bottom:10px}
.band p{color:var(--muted);margin-bottom:28px}
.band .cta{margin:0 auto}
footer{padding:32px 0 40px;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}
footer .wrap{display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between}
footer a{color:var(--muted)}
.bar{position:fixed;bottom:0;left:0;right:0;z-index:30;display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);backdrop-filter:blur(10px);border-top:1px solid var(--line)}
.bar .btn{min-height:50px;font-size:16px}
@media(min-width:880px){.bar{display:none}body{padding-bottom:0}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

# ------------------------------------------------------------------ statut « disponible » (calculé depuis HOURS)
JS = ("<script>(function(){try{var H=" + json.dumps({str(k): v for k, v in HOURS.items()}) + ";"
      "var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Jerusalem',weekday:'short',hour:'2-digit',hour12:false});"
      "var p=f.formatToParts(new Date());var D=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];"
      "var d=D.indexOf(p.find(function(x){return x.type==='weekday'}).value),h=+p.find(function(x){return x.type==='hour'}).value%24;"
      "var on=(H[d]||[]).some(function(s){return h>=s[0]&&h<s[1]});"
      "document.querySelectorAll('.status').forEach(function(el){if(on){el.classList.add('on');el.querySelector('.t').textContent='זמין עכשיו'}"
      "else{el.querySelector('.t').textContent='מחוץ לשעות – השאירו הודעה בוואטסאפ'}})}catch(e){}})();</script>")

def img(name, alt, w, h, eager=False):
    attrs = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="img/{name}.webp" alt="{alt}" width="{w}" height="{h}" {attrs}>'

def url_of(slug):
    return SITE_URL + "/" + ("" if slug == "index" else slug + ".html")

# ------------------------------------------------------------------ données structurées
BIZ_ID = SITE_URL + "/#business"
def business(area_names):
    days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    spec = []
    for d, slots in HOURS.items():
        for a, b in slots:
            spec.append({"@type":"OpeningHoursSpecification","dayOfWeek":days[d],
                         "opens":f"{a:02d}:00","closes":"23:59" if b == 24 else f"{b:02d}:00"})
    return {"@type":"Locksmith","@id":BIZ_ID,"name":NAME,"telephone":PHONE_INTL,"url":SITE_URL+"/",
            "image":SITE_URL+"/img/og.jpg","logo":SITE_URL+"/img/logo.png",
            "address":{"@type":"PostalAddress","addressCountry":"IL"},
            "areaServed":[{"@type":"City","name":n} for n in area_names],
            "openingHoursSpecification":spec,
            "priceRange":"₪150–₪1070","contactPoint":{"@type":"ContactPoint","telephone":PHONE_INTL,"contactType":"customer service","availableLanguage":["he"]}}

def ld(objs):
    return '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@graph":objs}, ensure_ascii=False) + '</script>'

def crumbs_ld(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

def faq_ld(faq):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

# ------------------------------------------------------------------ gabarit
def gads_js():
    if not GADS_ID:
        return ""
    ev = ("document.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';"
          + (f"if(h.indexOf('tel:')===0)gtag('event','conversion',{{send_to:'{GADS_ID}/{GADS_LABEL_CALL}'}});" if GADS_LABEL_CALL else "")
          + (f"if(h.indexOf('wa.me')>-1)gtag('event','conversion',{{send_to:'{GADS_ID}/{GADS_LABEL_WA}'}});" if GADS_LABEL_WA else "")
          + "});")
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GADS_ID}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GADS_ID}');{ev}</script>")

def page(slug, title, desc, body, graph, og_img="og"):
    url = url_of(slug)
    gsc = f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">' if GSC_VERIFICATION and slug == "index" else ""
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><meta name="theme-color" content="#1A56DB">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:locale" content="he_IL"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}/img/{og_img}.jpg"><meta property="og:site_name" content="{NAME}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="img/logo.png">
<link rel="preload" href="fonts/rubik-hebrew.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">{gsc}{ld(graph)}</head><body>
<header class="hd"><div class="wrap"><a class="logo" href="index.html"><span class="mk">{ic("key")}</span>{NAME}</a><a class="pill" href="tel:{PHONE_INTL}">{ic("phone")}<span>{PHONE}</span></a></div></header>
<main>{body}</main>
<footer><div class="wrap"><span><b>{NAME}</b> · מנעולן בכל אזור {REGION}</span><span><a href="tel:{PHONE_INTL}">{PHONE}</a> · <a href="{WA}">וואטסאפ</a> · <a href="rafi-hamanulan.vcf" download>שמרו את המספר</a> · <a href="prices.html">מחירון</a> · <a href="privacy.html">פרטיות</a></span></div></footer>
<nav class="bar" aria-label="יצירת קשר"><a class="btn btn-call" href="tel:{PHONE_INTL}">{ic("phone")}התקשרו</a><a class="btn btn-wa" href="{WA_LINK}">{WA_SVG}וואטסאפ</a></nav>
{JS}{gads_js()}</body></html>'''

def cta():
    return f'<div class="cta"><a class="btn btn-call" href="tel:{PHONE_INTL}">{ic("phone")}התקשרו</a><a class="btn btn-wa" href="{WA_LINK}">{WA_SVG}וואטסאפ</a></div>'

def hero(h1, sub, photo="hero", alt="רפי המנעולן מחזיק מנעול רב-בריח", crumb=""):
    return f'''<section class="hero"><div class="wrap">
<div class="hero-img">{img(photo, alt, 900 if photo=="hero" else 800, 1125 if photo=="hero" else 600, eager=True)}<div class="eta-badge">{ic("scooter")}<div><b>~{ETA_MIN} דק׳</b><small>הגעה בקטנוע</small></div></div></div>
<div class="hero-txt">{crumb}<span class="status"><span class="dot"></span><span class="t">זמין 24/6</span></span><h1>{h1}</h1><p class="sub">{sub}</p>{cta()}</div>
<ul class="trust"><li>{ic("tag")}מחיר ברור לפני העבודה</li><li>{ic("door")}פתיחה ללא נזק ככל שניתן</li><li>{ic("user")}ישירות מול רפי, בלי מוקד</li></ul>
</div></section>'''

def services_sec(title="שירותים", sub="", exclude=None):
    t = "".join(f'<a class="tile" href="{s}.html">{img(im, n, 800, 600)}<h3>{n}{ic("arrow")}</h3></a>'
                for s, n, im, *_ in SERVICES if s != exclude)
    small = f"<small>{sub}</small>" if sub else ""
    return f'<section class="sec"><div class="wrap"><h2>{title}{small}</h2><div class="tiles">{t}</div></div></section>'

# Galerie : photos réelles de Rafi (img/g1..g6.webp). Pour en ajouter : déposer gN.webp (600x600) et ajouter une ligne.
GALLERY = [("g1","מנעול רב-בריח בדלת פלדלת"),("g2","ידית וצילינדר בדלת כניסה"),("g3","מנעול ישן בדלת עץ"),
           ("g4","מנעול רב-בריח בדלת לבנה"),("g5","מנעול בדלת פנים"),("g6","מנעול בדלת זכוכית")]
def gallery_sec():
    g = "".join(f'<li>{img(n, a, 600, 600)}</li>' for n, a in GALLERY)
    return f'<section class="sec"><div class="wrap"><h2>מהעבודה בשטח</h2><ul class="gal">{g}</ul></div></section>'

STEPS = f'''<section class="sec alt"><div class="wrap"><h2>איך זה עובד</h2><ol class="steps">
<li>{ic("chat")}<div><h3>מתקשרים או שולחים וואטסאפ</h3><p>אני עונה בעצמי.</p></div></li>
<li>{ic("scooter")}<div><h3>מגיע תוך כ-{ETA_MIN} דקות</h3><p>בקטנוע, גם בפקקים.</p></div></li>
<li>{ic("check")}<div><h3>מחיר ברור, ואז עבודה</h3><p>מתחילים רק אחרי שאישרתם.</p></div></li></ol></div></section>'''

def area_sec(title="אזורי שירות", current=None):
    chips = "".join(f'<li><a href="{s}.html">מנעולן {b}</a></li>' for s, n, b, _ in CITIES if s != current)
    return f'<section class="sec"><div class="wrap"><h2>{title}<small>מגיע אליכם – מקיסריה ועד הוד השרון.</small></h2><ul class="chips">{chips}</ul></div></section>'

def faq_sec(faq):
    q = "".join(f'<details><summary>{a}</summary><p>{b}</p></details>' for a, b in faq)
    hrs = "".join(f'<div><b>{d}</b><span>{h}</span></div>' for d, h in HOURS_DISPLAY)
    return (f'<section class="sec alt"><div class="wrap two"><div><h2>שאלות נפוצות</h2><div class="faq">{q}</div></div>'
            f'<div><h2>שעות זמינות</h2><div class="hours">{hrs}</div><p class="note">בשבת סגור. מחוץ לשעות אפשר להשאיר הודעה בוואטסאפ.</p></div></div></section>')

def band(h="ננעלתם בחוץ?", p="מתקשרים, ואני בדרך."):
    rev = f'<p class="note"><a href="{REVIEW_URL}">עבדתי אצלכם? אשמח לביקורת בגוגל</a></p>' if REVIEW_URL else ""
    save = '<p class="note"><a href="rafi-hamanulan.vcf" download>שמרו את המספר באנשי הקשר – למקרה חירום</a></p>'
    return f'<section class="band"><div class="wrap"><h2>{h}</h2><p>{p}</p>{cta()}{save}{rev}</div></section>'

def crumb_html(label):
    return f'<p class="crumb"><a href="index.html">ראשי</a> / {label}</p>'


# ------------------------------------------------------------------ guides (articles utiles, longue traîne SEO)
# Contenu factuel et général. Pas de prix, pas de promesse non vérifiée.
GUIDES = [
("guide-locked-out", "ננעלתם מחוץ לבית? מה עושים עכשיו", "g1",
 "מה לעשות כשננעלתם בחוץ: מתי להתקשר ל-100 או ל-102, מה לא לנסות לבד, ואיך מנעולן פותח את הדלת בלי לשבור.",
 [("קודם כול: יש מישהו בסכנה?", ["אם ילד קטן, אדם שזקוק לעזרה או חיית מחמד נשארו בפנים, או שהגז או הכיריים דולקים – התקשרו מיד למשטרה (100) או לכבאות והצלה (102). זה קודם לכל דבר אחר."]),
  ("מה לא לעשות", ["לא לטפס דרך חלון או מרפסת – זה מסוכן, גם בקומה נמוכה.", "לא לנסות לפתוח עם מברג, כרטיס או סיכה – ברוב הדלתות זה לא עובד, ועלול להזיק לצילינדר ולהעלות את מחיר התיקון.", "לא לשבור את הדלת או את המשקוף."]),
  ("מה כן לעשות", ["בדקו אם למישהו אחר יש מפתח: בן משפחה, שכן, בעל הדירה.", "התקשרו למנעולן ותגידו מה סוג הדלת (פלדלת, דלת עץ) ומה קרה (נטרקה, מפתח נשבר, מפתח בפנים).", "הכינו תעודה מזהה או מסמך עם הכתובת – מנעולן אחראי יבקש לוודא שאתם גרים במקום לפני שהוא פותח."]),
  ("איך זה נראה בפועל", ["ברוב המקרים אפשר לפתוח את הדלת ללא נזק. אם צריך להחליף צילינדר אחרי הפתיחה, אפשר לעשות את זה באותו ביקור.", "אצלי המחיר נאמר לפני שמתחילים, ומתחילים רק אחרי שאישרתם."])]),
("guide-cylinder", "מתי צריך להחליף צילינדר בדלת?", "cylinder",
 "חמישה מצבים שבהם כדאי להחליף צילינדר, ההבדל בין צילינדר רגיל למוגן, ומה לשאול לפני ההחלפה.",
 [("חמישה מצבים שבהם כדאי להחליף", ["עברתם דירה – אין לכם דרך לדעת לכמה אנשים יש עותק של המפתח.", "איבדתם מפתח, או שנגנב לכם תיק עם מפתחות.", "הייתה פריצה או ניסיון פריצה.", "המפתח נכנס או מסתובב בקושי.", "הצילינדר ישן ופשוט, בלי הגנה מפני פריצה."]),
  ("צילינדר רגיל או מוגן?", ["צילינדר מוגן בנוי כך שיהיה קשה יותר לפרוץ, לשבור או להעתיק את המפתח שלו. בדלת כניסה זו בדרך כלל ההמלצה.", "יש דגמים של חברות שונות, כמו מולטילוק, רב-בריח ומגנום. ההתאמה תלויה בדלת ובמנעול הקיים."]),
  ("מה לשאול לפני ההחלפה", ["איזה דגם מתאים לדלת שלי?", "כמה מפתחות מקבלים, ואיך משכפלים עוד?", "אפשר שמפתח אחד יפתח כמה דלתות?"]),
  ("כמה זמן זה לוקח?", ["החלפת צילינדר היא עבודה קצרה, ובדרך כלל נעשית באותו ביקור. המחיר תלוי בדגם – אני אומר אותו לפני שמתחילים."])]),
("guide-broken-key", "המפתח נשבר בתוך המנעול – מה עושים?", "lock-repair",
 "מפתח שנשבר בצילינדר: מה לא לעשות כדי לא להחמיר, ואיך מוציאים אותו – לפעמים בלי להחליף צילינדר.",
 [("מה לא לעשות", ["לא לדחוף את החלק השבור פנימה עם המפתח השני או עם חפץ אחר.", "לא לשים דבק, שמן או סיליקון בתוך המנעול.", "לא לנסות לסובב את הצילינדר עם פלאייר או מברג."]),
  ("מה כן לעשות", ["שמרו את החלק השני של המפתח – הוא עוזר לזהות את הדגם ולשכפל מפתח חדש.", "אם הדלת פתוחה, השאירו אותה פתוחה עד שהבעיה נפתרת.", "התקשרו למנעולן ותגידו אם הדלת נעולה או פתוחה."]),
  ("מה אפשר לעשות", ["במקרים רבים אפשר לחלץ את החלק השבור בלי להחליף את הצילינדר.", "אם הצילינדר נפגע או ישן, כדאי להחליף אותו באותו ביקור."])]),
("guide-after-burglary", "מה עושים אחרי פריצה לדירה?", "security",
 "צעד אחרי צעד אחרי פריצה: משטרה, תיעוד לביטוח, החלפת צילינדר ושדרוג המיגון של הדלת.",
 [("מיד אחרי שגיליתם", ["אל תיכנסו אם יש חשש שמישהו עדיין בפנים. התקשרו למשטרה (100).", "אל תגעו ואל תסדרו – המשטרה עשויה לבקש לבדוק את המקום."]),
  ("לביטוח", ["צלמו את הדלת, המנעול וכל נזק לפני שמתקנים.", "רשמו מה חסר, ובקשו מהמשטרה את מספר התיק או את אישור הגשת התלונה."]),
  ("לאבטח את הדלת מחדש", ["החליפו צילינדר כמה שיותר מהר – ייתכן שלפורץ יש דרך לפתוח את הקיים.", "בדקו שהמנעול והמשקוף לא נפגעו, ושהדלת ננעלת עד הסוף.", "שקלו שדרוג: צילינדר מוגן, מנעול עזר או חיזוק לדלת."]),
  ("אני יכול לעזור", ["אני מגיע, מחליף צילינדר ובודק את הדלת והמנעולים. המחיר נאמר לפני שמתחילים."])]),
]

GUIDES += [
("guide-keys-inside", "הדלת נטרקה והמפתח בפנים – מה עושים?", "g4",
 "הדלת נטרקה כשהמפתח נשאר בפנים? מה אפשר לבדוק לבד, מה לא לנסות, ואיך פותחים בלי נזק.",
 [("קודם כול", ["אם בפנים נשאר ילד, אדם שזקוק לעזרה, חיה או משהו דולק על הכיריים – התקשרו מיד למשטרה (100) או לכבאות והצלה (102)."]),
  ("מה לבדוק לבד", ["האם יש למישהו עותק של המפתח – בן משפחה, שכן, בעל הדירה.", "האם יש דלת נוספת או מרפסת נגישה בבטחה מהקרקע – בלי לטפס."]),
  ("מה לא לעשות", ["לא לנסות לפתוח עם כרטיס אשראי או מברג – בדלתות פלדה זה לא עובד ועלול לפגוע במנעול.", "לא לטפס דרך חלונות או מרפסות."]),
  ("כשמגיע מנעולן", ["בדלת שנטרקה בלי שננעלה בבריחים, לרוב אפשר לפתוח מהר וללא נזק.", "אם הדלת ננעלה עם המפתח בפנים, ייתכן שיהיה צורך להחליף צילינדר – תקבלו מחיר ברור לפני שמתחילים."])]),
("guide-stuck-lock", "מנעול רב-בריח תקוע – למה זה קורה ומה עושים", "lock-repair",
 "המפתח לא מסתובב, הדלת לא ננעלת עד הסוף או הבריחים נתקעים? הסיבות הנפוצות ומה כדאי לעשות.",
 [("סיבות נפוצות", ["הדלת שקעה מעט על הצירים והבריחים לא נכנסים בדיוק למקום.", "לכלוך או חלודה בתוך המנעול או בצילינדר.", "מפתח שחוק או צילינדר ישן.", "חלק שבור בתוך המנגנון."]),
  ("מה אפשר לבדוק לבד", ["לנסות לנעול כשהדלת לחוצה היטב אל המשקוף – אם זה עובד, כנראה צריך לכוון את הדלת.", "לנסות את המפתח השני – אם הוא עובד, המפתח הראשון שחוק."]),
  ("מה לא לעשות", ["לא להפעיל כוח על המפתח – הוא עלול להישבר בתוך הצילינדר.", "לא לשים שמן מטבח או דבק בתוך המנעול."]),
  ("הפתרון", ["לרוב מכוונים את הדלת, מנקים או מחליפים צילינדר. במקרים מסוימים מחליפים את המנגנון. המחיר נאמר לפני שמתחילים."])]),
("guide-safe-code", "שכחתם את הקוד של הכספת – מה אפשר לעשות", "safe",
 "שכחתם את הקוד או שהכספת לא נפתחת? מה לבדוק לפני שמזמינים מנעולן ואיך פותחים כספת.",
 [("מה לבדוק קודם", ["סוללות – בכספות אלקטרוניות רבות סוללה חלשה גורמת לכספת לא להיפתח גם עם הקוד הנכון.", "מפתח חירום – להרבה כספות יש מפתח עקיפה. בדקו אם הוא אצלכם.", "החוברת של הכספת – לפעמים יש בה קוד מפעל או הוראות איפוס."]),
  ("מה לא לעשות", ["לא לנסות קודים שוב ושוב – חלק מהכספות ננעלות לזמן ארוך אחרי כמה ניסיונות.", "לא לנסות לפתוח בכוח – זה עלול להרוס את הכספת ואת מה שבתוכה."]),
  ("פתיחת כספת", ["מנעולן יכול לפתוח את הכספת, ואחרי הפתיחה להגדיר קוד חדש. תתבקשו להראות שהכספת שלכם."])]),
]

def guide_body(slug, title, im, desc, sections):
    secs = "".join(f'<h2>{h}</h2>' + ("<ul>" + "".join(f"<li>{p}</li>" for p in ps) + "</ul>" if len(ps) > 1 else f"<p>{ps[0]}</p>") for h, ps in sections)
    others = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t, *_ in GUIDES if s != slug)
    return (f'<article class="sec"><div class="wrap art">{crumb_html("מדריכים")}<h1>{title}</h1><p class="intro">{desc}</p>'
            f'{img(im, title, 800, 600, eager=True)}{secs}'
            f'<div class="cta-box"><b>צריכים מנעולן עכשיו?</b>{cta()}</div>'
            f'<h2>מדריכים נוספים</h2><ul class="links">{others}</ul></div></article>' + area_sec() + band())

def guides_sec():
    li = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t, *_ in GUIDES)
    return f'<section class="sec"><div class="wrap"><h2>מדריכים קצרים</h2><ul class="links">{li}</ul></div></section>'


# ------------------------------------------------------------------ MÉTHODE DE PRIX (fournie par Raphaël le 7 nov. 2026)
# (id, titre, image, note, [(libellé, prix ₪ ou None, texte du prix)], pages de service où afficher le bloc)
NIGHT_SURCHARGE = 100   # ₪, tout jour de la semaine
PRICES = [
("fp", "פריצת דלתות", "door-opening", "",
 [("פתיחת דלת טרוקה (נטרקה ולא ננעלה)", 200, None, "t-latch"),
  ("פריצת צילינדר בפלדלת נעולה", 300, None, "t-steelcyl"),
  ("פריצה + החלפת צילינדר בפלדלת", None, "החל מ-620 ₪", "t-rav-dyn")], ["door-opening"]),
("fpc", "פריצה + החלפת צילינדר בפלדלת", "p-steel", "פריצה (300 ₪) + צילינדר חדש לבחירתכם, כולל התקנה. המחיר לפי הצילינדר:",
 [("מגנום · 5 מפתחות", 620, None, "t-magnum320"),
  ("מגנום · 5 מפתחות + כרטיס שכפול", 660, None, "t-magnum360"),
  ("רב-בריח · 5 מפתחות + כרטיס שכפול", 690, None, "t-rav390"),
  ("KEYLOCX של רב-בריח", 800, None, "t-keylocx"),
  ("לוקסיס של רב-בריח", 900, None, "t-loksis"),
  ("מולטילוק MTL600", 900, None, "t-mtl600"),
  ("מולטילוק MTL800", 1070, None, "t-mtl800")], ["door-opening", "cylinder"]),
("cyl", "החלפת צילינדר", "p-cyl", "המחיר כולל את הצילינדר וההתקנה. אפשר עם כפתור קבוע מבפנים במקום מפתח – באותו מחיר.",
 [("רב-בריח · 5 מפתחות + כרטיס שכפול", 390, None, "t-rav390"),
  ("מגנום · 5 מפתחות + כרטיס שכפול", 360, None, "t-magnum360"),
  ("מגנום · 5 מפתחות", 320, None, "t-magnum320")], ["cylinder", "security"]),
("high", "צילינדרים ברמת אבטחה גבוהה", "p-mtl", "המחיר כולל את הצילינדר וההתקנה.",
 [("מולטילוק MTL800", 770, None, "t-mtl800"), ("מולטילוק MTL600", 600, None, "t-mtl600"),
  ("לוקסיס של רב-בריח", 600, None, "t-loksis"), ("KEYLOCX של רב-בריח", 500, None, "t-keylocx")], ["cylinder", "security"]),
("mech", "פלדלת – מנגנונים ופרזול", "p-steel", "",
 [("החלפת מנגנון רב-בריח", 700, None, "t-ravmech"), ("החלפת מנגנון שריונית חוסם", 800, None, "t-shiryonit"),
  ("סט פלטות קומפלט לפלדלת – ניקל, שחור או מעוגל", 330, None, "t-plates"), ("מחזיר דלת", 450, None, None), ("התקנת מנעול כספת / מנעול נוסף לפלדלת", 550, None, "t-extralock")], ["lock-repair", "security"]),
("int", "דלתות פנים וכניסות נוספות", "p-entrance", "",
 [("החלפת צילינדר פשוט", 200, None, "t-simplecyl"), ("החלפת מנגנון", 250, None, "t-mortise"),
  ("פריצה + החלפת מנגנון", 300, None, "t-intmech"), ("פריצה + החלפת מנגנון + צילינדר", 380, None, "t-intdoor"),
  ("סט ידיות לדלת פשוטה / דלת פנים", 150, None, "t-inthandles")], ["lock-repair", "door-opening"]),
("mail", "תיבות דואר", "p-mail", "",
 [("פריצה והחלפת מנעול לתיבת דואר", 200, None, "t-mail"), ("מנעול זיז ישן בתיבות דואר מרוכזות", 300, None, "t-mailbank")], ["lock-repair"]),
("safe", "כספות", "safe", "בכספות גדולות ומיוחדות מתווספים 100 ₪ לכל שכבת פלדה – זה נקבע רק במקום, בזמן הפריצה.",
 [("התקנת כספת סטנדרטית", 350, None, "t-safe"), ("פריצת כספת סטנדרטית", 300, None, "t-safe")], ["safe"]),
("rep", "תיקונים", "p-repair", "",
 [("תיקון מנעולים ודלתות", None, "החל מ-200 ₪, לפי העבודה", None)], ["lock-repair"]),
]
import re as _re
def _pkey(r):
    l, p, t, th = r
    if p: return p
    m = _re.search(r"(\d+)", t or ""); return int(m.group(1)) if m else 0
PRICES = [(g[0], g[1], g[2], g[3], sorted(g[4], key=_pkey), g[5]) for g in PRICES]   # prix toujours en ordre croissant

PRICE_NOTES = [f"תוספת עבודת לילה: {NIGHT_SURCHARGE} ₪, בכל יום בשבוע.", "כל השירותים זמינים גם לעסקים.",
               "המחיר הסופי נאמר ומאושר לפני שמתחילים לעבוד."]

def price_txt(p, t): return t if t else f"{p} ₪"

def thumb(key, alt):
    if key:
        return f'<img class="pth" src="img/{key}.webp" alt="{alt}" width="240" height="240" loading="lazy" decoding="async">'
    return f'<i class="pth ph">{ic("key")}</i>'

def price_block(g, h="h3"):
    gid, title, im, note, rows, _ = g
    li = "".join(f'<li>{thumb(th, l)}<span>{l}</span><b{' class="long"' if t else ''}>{price_txt(p, t)}</b></li>' for l, p, t, th in rows)
    n = f'<p class="pnote">{note}</p>' if note else ""
    pic = img(im, title, 800, 600) if im else ""
    return f'<div class="pcard">{pic}<div class="pbody"><{h}>{title}</{h}><ul class="prows">{li}</ul>{n}</div></div>'

def prices_for_service(slug):
    gs = [g for g in PRICES if slug in g[5]]
    if not gs: return ""
    notes = "".join(f"<li>{x}</li>" for x in PRICE_NOTES)
    return (f'<section class="sec alt"><div class="wrap"><h2>מחירים<small><a href="prices.html">למחירון המלא</a></small></h2>'
            f'<div class="pgrid">{"".join(price_block(g) for g in gs)}</div><ul class="pnotes">{notes}</ul></div></section>')

def prices_teaser():
    keys = [("פתיחת דלת טרוקה", 200), ("פריצת צילינדר בפלדלת", 300), ("החלפת צילינדר", 320), ("פריצה + החלפת צילינדר בפלדלת", 620)]
    li = "".join(f'<li><span>{l}</span><b>{"החל מ-" if i >= 2 else ""}{p} ₪</b></li>' for i, (l, p) in enumerate(keys))
    return (f'<section class="sec"><div class="wrap"><h2>מחירים שקופים<small>בלי הפתעות – המחיר נאמר לפני העבודה.</small></h2>'
            f'<div class="pcard solo"><div class="pbody"><ul class="prows">{li}</ul><a class="btn btn-call" href="prices.html" style="margin-top:16px">למחירון המלא</a></div></div></div></section>')

# ------------------------------------------------------------------ génération
ALL = [n for _, n, _, _ in CITIES]
pages = []  # (slug, html)

# Accueil
home_faq = FAQ + [("לאילו אזורים אתה מגיע?", "קיסריה, חדרה, אור עקיבא, נתניה, כפר יונה, אבן יהודה, קדימה-צורן, תל מונד, פרדסיה, כפר סבא, רעננה, הרצליה, הוד השרון והמושבים שבדרך.")]
body = (hero("מנעולן קרוב אליכם", f"פריצת דלתות, צילינדרים, מנעולים וכספות בכל אזור {REGION}. אצלכם תוך כ-{ETA_MIN} דקות.")
        + services_sec() + prices_teaser() + STEPS + gallery_sec() + area_sec() + faq_sec(home_faq) + guides_sec() + band())
pages.append(("index", page("index",
    f"מנעולן בשרון – כפר סבא, רעננה, נתניה, הרצליה | {NAME} – {PHONE}",
    f"מנעולן בכל אזור {REGION}, מקיסריה ועד הוד השרון: פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות. הגעה בקטנוע תוך כ-{ETA_MIN} דקות, מחיר ברור לפני העבודה. {PHONE}",
    body, [business(ALL), {"@type":"WebSite","@id":SITE_URL+"/#website","url":SITE_URL+"/","name":NAME,"inLanguage":"he"}, faq_ld(home_faq)])))

# Pages villes
for s, n, b, hood in CITIES:
    faq = [(f"תוך כמה זמן מגיע מנעולן {b}?", f"בדרך כלל תוך כ-{ETA_MIN} דקות. אני מגיע בקטנוע, כך שגם בשעות העומס ההגעה {b} מהירה."),
           (f"באילו אזורים {b} אתה עובד?", f"{hood}.")] + FAQ[1:]
    intro = (f"צריכים מנעולן {b}? רפי המנעולן מגיע בקטנוע ל{hood}. "
             f"פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות – לבית ולעסק, עם מחיר ברור לפני העבודה.")
    body = (hero(f"מנעולן {b}", f"פורץ דלתות ומנעולים {b}. אצלכם תוך כ-{ETA_MIN} דקות.", crumb=crumb_html(f"מנעולן {b}"))
            + services_sec(f"שירותי מנעולן {b}", intro)
            + STEPS + faq_sec(faq) + area_sec("עוד אזורים", current=s) + band())
    pages.append((s, page(s,
        f"מנעולן {b} – הגעה תוך כ-{ETA_MIN} דק׳ | {NAME}",
        f"מנעולן {b}: פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות. {NAME} מגיע בקטנוע תוך כ-{ETA_MIN} דקות. מחיר ברור לפני העבודה. {PHONE}",
        body, [business([n]), crumbs_ld([("ראשי", SITE_URL+"/"), (f"מנעולן {b}", url_of(s))]), faq_ld(faq)])))

# Pages services
for s, n, im, t, items, kw in SERVICES:
    inc = "".join(f'<li>{ic("check")}<span>{x}</span></li>' for x in items)
    faq = FAQ[1:3] + FAQ[:1] + FAQ[3:]
    body = (hero(f"{n} – מגיע אליכם", f"{t} אצלכם תוך כ-{ETA_MIN} דקות.", photo=im, alt=n, crumb=crumb_html(n))
            + f'<section class="sec"><div class="wrap"><h2>מה כולל השירות<small>{kw} – המחיר נאמר ומאושר לפני שמתחילים.</small></h2><ul class="incl">{inc}</ul></div></section>'
            + prices_for_service(s) + services_sec("שירותים נוספים", exclude=s) + STEPS + faq_sec(faq) + area_sec() + band())
    svc = {"@type":"Service","name":n,"serviceType":n,"provider":{"@id":BIZ_ID},"areaServed":[{"@type":"City","name":c} for c in ALL],"description":t}
    pages.append((s, page(s,
        f"{n} בשרון – כפר סבא, רעננה, נתניה, הרצליה | {NAME}",
        f"{n} בכל אזור {REGION}, מקיסריה ועד הוד השרון – {t} {kw}. הגעה בקטנוע תוך כ-{ETA_MIN} דקות, מחיר ברור לפני העבודה.",
        body, [business(ALL), svc, crumbs_ld([("ראשי", SITE_URL+"/"), (n, url_of(s))]), faq_ld(faq)], og_img="og")))

for slug, title, im, desc, sections in GUIDES:
    art = {"@type":"Article","headline":title,"description":desc,"inLanguage":"he","image":f"{SITE_URL}/img/{im}.webp",
           "author":{"@id":BIZ_ID},"publisher":{"@id":BIZ_ID},"mainEntityOfPage":url_of(slug),"dateModified":TODAY}
    pages.append((slug, page(slug, f"{title} | {NAME}", desc, guide_body(slug, title, im, desc, sections),
        [business(ALL), art, crumbs_ld([("ראשי", SITE_URL+"/"), (title, url_of(slug))])])))

with open(f"{OUT}/style.css", "w") as f: f.write(CSS)
for slug, html in pages:
    with open(f"{OUT}/{slug}.html", "w") as f: f.write(html)

# Page Mehiron (prix fournis par Raphaël)
offers = [{"@type":"Offer","priceCurrency":"ILS","price":p,"itemOffered":{"@type":"Service","name":f"{g[1]} – {l}"}}
          for g in PRICES for l, p, t, th in g[4] if p]
PRICES_BODY = (hero("מחירון מנעולן", "מחירים ברורים, כולל חלקים והתקנה. המחיר הסופי נאמר לפני העבודה.", photo="p-cyl", alt="צילינדרים", crumb=crumb_html("מחירון"))
    + f'<section class="sec"><div class="wrap"><div class="pgrid">{"".join(price_block(g, "h2") for g in PRICES)}</div>'
    + '<ul class="pnotes">' + "".join(f"<li>{x}</li>" for x in PRICE_NOTES) + '</ul></div></section>' + area_sec() + band())
pages.append(("prices", page("prices", f"מחירון מנעולן – פריצת דלת, החלפת צילינדר, כספות | {NAME}",
    "מחירון רפי המנעולן: פתיחת דלת טרוקה 200 ₪, פריצת צילינדר בפלדלת 300 ₪, פריצה + החלפת צילינדר מ-620 ₪, החלפת צילינדר מ-320 ₪, כספות ומנגנונים. כולל חלקים והתקנה.",
    PRICES_BODY, [business(ALL), {"@type":"OfferCatalog","name":"מחירון","provider":{"@id":BIZ_ID},"itemListElement":offers},
                  crumbs_ld([("ראשי", SITE_URL+"/"), ("מחירון", url_of("prices"))])])))
with open(f"{OUT}/prices.html", "w") as f: f.write(pages[-1][1])

# Politique de confidentialité (le site utilise la balise Google Ads quand GADS_ID est renseigné)
PRIVACY = f"""<section class="sec"><div class="wrap art"><h1>מדיניות פרטיות</h1>
<p>האתר שייך ל{NAME}. אין באתר טפסים, ואנחנו לא אוספים שם, כתובת או פרטים אישיים דרך האתר.</p>
<h2>עוגיות ומדידה</h2><p>כדי לדעת אילו מודעות מביאות פניות, האתר משתמש בתג של Google Ads, שעשוי לשמור עוגיות בדפדפן ולספור לחיצות על כפתורי ההתקשרות והוואטסאפ. Google מעבדת את המידע לפי מדיניות הפרטיות שלה: <a href="https://policies.google.com/privacy?hl=iw">policies.google.com/privacy</a>.</p>
<p>אפשר לחסום או למחוק עוגיות בהגדרות הדפדפן, והאתר ימשיך לעבוד כרגיל.</p>
<h2>יצירת קשר</h2><p>לכל שאלה על פרטיות: <a href="tel:{PHONE_INTL}">{PHONE}</a> או בוואטסאפ.</p></div></section>"""
pages.append(("privacy", page("privacy", f"מדיניות פרטיות | {NAME}", f"מדיניות הפרטיות והעוגיות של אתר {NAME}.", PRIVACY, [business(ALL)])))
with open(f"{OUT}/privacy.html", "w") as f: f.write(pages[-1][1])

# 404
with open(f"{OUT}/404.html", "w") as f:
    f.write(page("404", f"הדף לא נמצא | {NAME}", "הדף לא נמצא.",
                 f'<section class="band"><div class="wrap"><h2>הדף לא נמצא</h2><p>אבל אני כן כאן. <a href="index.html">לדף הראשי</a></p>{cta()}</div></section>',
                 [business(ALL)]).replace('<link rel="canonical" href="' + url_of("404") + '">', '<meta name="robots" content="noindex">'))

with open(f"{OUT}/favicon.svg", "w") as f:
    f.write("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='9' fill='#1A56DB'/><circle cx='12' cy='16' r='5' fill='none' stroke='white' stroke-width='2.5'/><path d='M17 16h9M23 16v4' stroke='white' stroke-width='2.5' stroke-linecap='round'/></svg>")

with open(f"{OUT}/rafi-hamanulan.vcf", "w", encoding="utf-8") as f:
    f.write("BEGIN:VCARD\r\nVERSION:3.0\r\nN:;" + NAME + ";;;\r\nFN:" + NAME + "\r\nORG:" + NAME + "\r\nTITLE:מנעולן\r\n"
            + "TEL;TYPE=CELL,VOICE:" + PHONE_INTL + "\r\nURL:" + SITE_URL + "/\r\nNOTE:מנעולן – פריצת דלתות, צילינדרים, מנעולים וכספות\r\nEND:VCARD\r\n")
with open(f"{OUT}/{INDEXNOW_KEY}.txt", "w") as f: f.write(INDEXNOW_KEY)

urls = [url_of(s) for s, _ in pages]
with open(f"{OUT}/sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
with open(f"{OUT}/robots.txt", "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print(f"{len(pages)} pages générées dans {OUT} (SITE_URL={SITE_URL})")

if LEGACY_ROOT_COPY:
    import shutil
    for name in os.listdir(OUT):
        src, dst = os.path.join(OUT, name), os.path.join(ROOT, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    print("Copie de transition à la racine : OK (LEGACY_ROOT_COPY=True)")
