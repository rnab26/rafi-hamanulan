import os, json
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du repo
PHONE_INTL="+972545301389"; PHONE="054-530-1389"; WA="https://wa.me/972545301389"
DOMAIN="https://rafihamanulan.co.il"
I={ # stroke icons 24x24
"door":'<path d="M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17"/><path d="M3 21h18"/><circle cx="14.5" cy="12" r="1"/>',
"cyl":'<rect x="4" y="7" width="16" height="10" rx="5"/><circle cx="9" cy="12" r="2"/><path d="M11 12h6"/>',
"lock":'<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><path d="M12 14v3"/>',
"safe":'<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="12" cy="12" r="4"/><path d="M12 8v1M12 15v1M8 12h1M15 12h1M6 20v1M18 20v1"/>',
"shield":'<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
"clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
"tag":'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
"user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
"phone":'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
"pin":'<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
"scooter":'<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M9 17h6l3-7h-3M15 10l-2-5h-3M6 14l2-4h4"/>',
"check":'<path d="M5 12l5 5L20 7"/>',
"key":'<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2"/>',
}
def ic(n,cls="ic"): return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'
WA_SVG='<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
CITIES=[("netanya","נתניה","בנתניה","כל השכונות – רמת פולג, עין התכלת, קריית השרון, קריית צאנז, אגמים ומרכז העיר"),
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
("moshavim","מושבי השרון","במושבי השרון","אודים, יקום, מכמורת, כפר ויתקין, בית יהושע, חבצלת השרון, אביחיל ועוד")]
SERVICES=[("door-opening","פריצת דלתות","door","ננעלתם בחוץ? פתיחת הדלת ללא נזק ככל שניתן.",["דלת כניסה ופלדלת","דלתות פנים וחדרי אמבטיה","מפתח שנשבר בתוך המנעול","מפתח שנשאר בצד הפנימי"]),
("cylinder","החלפת צילינדר","cyl","אחרי מעבר דירה, אובדן מפתחות או פריצה.",["צילינדרים רגילים ומוגנים","החלפה אחרי מעבר דירה","החלפה אחרי פריצה או אובדן מפתחות","מפתח אחד לכמה דלתות"]),
("lock-repair","תיקון והחלפת מנעולים","lock","מנעול שנתקע, ידית שנשברה, דלת שלא נסגרת.",["מנעולי רב-בריח","ידיות ומנגנונים","מנעולים לשערים ולתיבות דואר","כיוון דלת שנתקעת"]),
("safe","פתיחת כספות","safe","קוד שנשכח או מנגנון שנתקע.",["כספות עם קוד","כספות עם מפתח","החלפת קוד אחרי פתיחה"]),
("security","שדרוג מיגון","shield","בדיקת הדלת והמנעולים והמלצה במחיר ברור.",["שדרוג צילינדר ומנעולים","מנעולי עזר","מיגון לעסקים ולמחסנים"])]
FAQ=[("תוך כמה זמן אתה מגיע?","אני יוצא מנתניה בקטנוע, אז גם בפקקים אני מגיע בדרך כלל תוך כ-25 דקות לכל מקום באזור, מקיסריה ועד הוד השרון."),
("אני יודע כמה זה יעלה לפני שמתחילים?","כן. אחרי שאני רואה את הדלת או המנעול אני אומר מחיר ברור, ורק אחרי שאתם מאשרים מתחילים לעבוד."),
("הדלת תיפגע בזמן הפריצה?","ברוב המקרים אפשר לפתוח ללא נזק לדלת. אם צריך להחליף את הצילינדר אחרי הפתיחה, אני מחליף אותו באותו ביקור."),
("מתי אתה זמין?","24 שעות בימים ראשון עד חמישי, ביום שישי מ-09:00 עד 16:00, ובמוצאי שבת עד חצות."),
("לאילו אזורים אתה מגיע?","נתניה, חדרה, קיסריה, אור עקיבא, כפר יונה, אבן יהודה, קדימה-צורן, תל מונד, פרדסיה, כפר סבא, רעננה, הרצליה, הוד השרון והמושבים שבדרך."),
("מה עושים אחרי פריצה לבית?","מומלץ להחליף צילינדר כמה שיותר מהר. אני מגיע, מחליף ויכול להמליץ על שדרוג מיגון לדלת.")]
CSS=r"""
:root{--bg:#FFFFFF;--soft:#F3F6FB;--ink:#0E1A2B;--muted:#5B6878;--line:#E3E9F1;--blue:#1A56DB;--blue-d:#1446B4;--blue-soft:#E8EFFD;--wa:#18A957;--amber:#F5A524;--green:#16A34A;--r:18px;--shadow:0 1px 2px rgba(14,26,43,.06),0 8px 24px rgba(14,26,43,.06)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Rubik",Arial,sans-serif;font-size:17px;line-height:1.6;padding-bottom:88px}
a{color:var(--blue)}h1,h2,h3{line-height:1.2;margin:0}
a:focus-visible,summary:focus-visible{outline:3px solid var(--amber);outline-offset:2px;border-radius:8px}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.ic{width:22px;height:22px;flex:none}
/* header */
.hd{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700;font-size:20px}
.logo .mk{width:38px;height:38px;border-radius:12px;background:var(--blue);color:#fff;display:grid;place-items:center}
.logo .mk .ic{width:22px;height:22px}
.pill{display:inline-flex;align-items:center;gap:8px;background:var(--blue-soft);color:var(--blue-d);text-decoration:none;font-weight:700;padding:9px 14px;border-radius:999px;font-size:16px}
.pill span{direction:ltr}
/* hero */
.hero{background:linear-gradient(180deg,var(--soft),#fff);padding:28px 0 36px}
.hero .wrap{display:grid;gap:28px}
@media(min-width:900px){.hero .wrap{grid-template-columns:1.15fr .85fr;align-items:center;padding-top:28px;padding-bottom:28px}}
.status{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:14px;font-weight:500;color:var(--muted)}
.dot{width:9px;height:9px;border-radius:50%;background:var(--muted)}
.status.on .dot{background:var(--green);box-shadow:0 0 0 4px rgba(22,163,74,.18)}
.status.on{color:var(--green)}
.hero h1{font-size:clamp(32px,6.4vw,52px);font-weight:700;letter-spacing:-.01em;margin:16px 0 12px}
.hero .sub{color:var(--muted);font-size:18px;margin:0 0 22px;max-width:44ch}
.cta{display:grid;gap:10px;max-width:460px}
@media(min-width:520px){.cta{grid-template-columns:1fr 1fr}}
.btn{display:flex;align-items:center;justify-content:center;gap:10px;min-height:56px;border-radius:14px;font-weight:700;font-size:18px;text-decoration:none;padding:0 18px}
.btn-call{background:var(--blue);color:#fff;box-shadow:0 6px 18px rgba(26,86,219,.28)}
.btn-call:hover{background:var(--blue-d)}
.btn-wa{background:#fff;color:var(--wa);border:2px solid var(--wa)}
.trust{display:flex;flex-wrap:wrap;gap:8px 18px;margin:20px 0 0;padding:0;list-style:none;color:var(--muted);font-size:15px}
.trust li{display:flex;align-items:center;gap:6px}.trust .ic{width:18px;height:18px;color:var(--green)}
/* eta card */
.eta{background:#fff;border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:20px;max-width:420px;width:100%;justify-self:center}
.eta-top{display:flex;align-items:center;gap:12px}
.av{width:48px;height:48px;border-radius:50%;background:var(--blue-soft);color:var(--blue);display:grid;place-items:center;font-weight:700;font-size:20px}
.eta-top b{display:block;font-size:17px}.eta-top small{color:var(--muted);font-size:14px}
.eta-time{margin-inline-start:auto;text-align:center;background:var(--blue);color:#fff;border-radius:14px;padding:6px 12px;line-height:1.1}
.eta-time strong{display:block;font-size:22px;direction:ltr}.eta-time span{font-size:12px}
.map{margin:16px 0 14px;height:130px;border-radius:16px;background:var(--soft);position:relative;overflow:hidden}
.map svg{position:absolute;inset:0;width:100%;height:100%}
.eta-steps{display:flex;justify-content:space-between;font-size:13px;color:var(--muted)}
.eta-steps span{display:flex;align-items:center;gap:6px}.eta-steps .ic{width:16px;height:16px;color:var(--blue)}
/* sections */
.sec{padding:52px 0}.sec.alt{background:var(--soft)}
.sec h2{font-size:clamp(26px,4.5vw,34px);font-weight:700;margin-bottom:8px}
.sec .lede{color:var(--muted);margin:0 0 26px;max-width:56ch}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.card{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px;text-decoration:none;color:var(--ink);transition:border-color .15s,box-shadow .15s}
a.card:hover{border-color:var(--blue);box-shadow:var(--shadow)}
.card .bub{width:46px;height:46px;border-radius:14px;background:var(--blue-soft);color:var(--blue);display:grid;place-items:center;margin-bottom:14px}
.card .bub .ic{width:24px;height:24px}
.card h3{font-size:19px;margin-bottom:4px}
@media(max-width:600px){.card{display:grid;grid-template-columns:46px 1fr;column-gap:14px;align-items:center;padding:16px}.card .bub{margin:0;grid-row:span 2}.card h3{margin:0}.grid{gap:10px}.step{padding:16px}}.card p{margin:0;color:var(--muted);font-size:15px}
.steps{display:grid;gap:14px;counter-reset:s;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.step{background:#fff;border-radius:var(--r);padding:20px;border:1px solid var(--line)}
.step::before{counter-increment:s;content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;margin-bottom:12px}
.step h3{font-size:18px;margin-bottom:4px}.step p{margin:0;color:var(--muted);font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:0;padding:0}
.chips a{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;text-decoration:none;color:var(--ink);font-size:15px}
.chips a:hover{border-color:var(--blue);color:var(--blue)}.chips .ic{width:16px;height:16px;color:var(--blue)}
.faq{max-width:760px}
.faq details{background:#fff;border:1px solid var(--line);border-radius:14px;margin-bottom:10px}
.faq summary{cursor:pointer;list-style:none;padding:16px 18px;font-weight:500;display:flex;justify-content:space-between;gap:12px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:22px;line-height:1;color:var(--blue)}
.faq details[open] summary::after{content:"–"}
.faq details p{margin:0;padding:0 18px 16px;color:var(--muted)}
.hours{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:6px 18px;max-width:440px}
.hours div{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--line)}
.hours div:last-child{border:0}.hours b{font-weight:500}.hours span{direction:ltr;color:var(--muted)}
.two{display:grid;gap:28px}@media(min-width:860px){.two{grid-template-columns:1fr 1fr}}
.incl{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.incl li{display:flex;gap:10px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px}
.incl .ic{color:var(--green)}
.band{background:var(--blue);color:#fff;border-radius:24px;padding:30px 24px;display:grid;gap:18px;align-items:center}
@media(min-width:760px){.band{grid-template-columns:1fr auto}}
.band h2{color:#fff;margin:0}.band p{margin:6px 0 0;opacity:.85}
.band .btn{background:#fff;color:var(--blue)}
.crumb{font-size:14px;color:var(--muted);margin:0}.crumb a{color:var(--muted)}
footer{padding:30px 0 40px;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}
footer .wrap{display:grid;gap:6px}
.bar{position:fixed;bottom:0;left:0;right:0;z-index:30;display:grid;grid-template-columns:1.4fr 1fr;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);backdrop-filter:blur(10px);border-top:1px solid var(--line)}
.bar .btn{min-height:52px;font-size:17px}
@media(min-width:900px){.bar{display:none}body{padding-bottom:0}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""
JS=r"""<script>(function(){try{var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Jerusalem',weekday:'short',hour:'2-digit',hour12:false});var p=f.formatToParts(new Date());var d=p.find(function(x){return x.type==='weekday'}).value,h=+p.find(function(x){return x.type==='hour'}).value;var on=(['Sun','Mon','Tue','Wed','Thu'].indexOf(d)>-1)||(d==='Fri'&&h>=9&&h<16)||(d==='Sat'&&h>=19);document.querySelectorAll('.status').forEach(function(el){if(on){el.classList.add('on');el.querySelector('.t').textContent='זמין עכשיו – אפשר להתקשר'}else{el.querySelector('.t').textContent='כרגע שבת – אפשר להשאיר הודעה בוואטסאפ'}})}catch(e){}})();</script>"""
MAP='''<svg viewBox="0 0 360 130" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g stroke="#DCE4EF" stroke-width="10" fill="none" stroke-linecap="round"><path d="M-10 30H380"/><path d="M-10 95H380"/><path d="M80 -10V140"/><path d="M250 -10V140"/></g><path d="M300 108 C 250 108, 250 40, 190 40 S 110 70, 62 34" fill="none" stroke="#1A56DB" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 9"/><circle cx="300" cy="108" r="8" fill="#1A56DB"/><circle cx="300" cy="108" r="14" fill="#1A56DB" opacity=".15"/><g transform="translate(50 12)"><path d="M12 30s-10-8.5-10-16a10 10 0 0 1 20 0c0 7.5-10 16-10 16z" fill="#F5A524"/><circle cx="12" cy="14" r="4" fill="#fff"/></g></svg>'''
def eta(where="אליכם"):
    return f'''<div class="eta" role="img" aria-label="הגעה משוערת כ-25 דקות"><div class="eta-top"><div class="av">ר</div><div><b>רפי המנעולן</b><small>יוצא אליכם בקטנוע</small></div><div class="eta-time"><strong>25</strong><span>דק׳ בערך</span></div></div><div class="map">{MAP}</div><div class="eta-steps"><span>{ic("scooter")}נתניה</span><span>{ic("pin")}{where}</span></div></div>'''
def schema(area,faq=True):
    d=[{"@context":"https://schema.org","@type":"Locksmith","name":"רפי המנעולן","telephone":PHONE_INTL,"url":DOMAIN,"areaServed":area,
    "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Sunday","Monday","Tuesday","Wednesday","Thursday"],"opens":"00:00","closes":"23:59"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Friday","opens":"09:00","closes":"16:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"19:00","closes":"23:59"}]}]
    if faq: d.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
def page(slug,title,desc,body,area):
    url=DOMAIN+"/"+("" if slug=="index" else slug+".html")
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><meta name="theme-color" content="#1A56DB">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:locale" content="he_IL"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%231A56DB'/%3E%3Ccircle cx='12' cy='16' r='5' fill='none' stroke='white' stroke-width='2.5'/%3E%3Cpath d='M17 16h9M23 16v4' stroke='white' stroke-width='2.5' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">{schema(area)}</head><body>
<header class="hd"><div class="wrap"><a class="logo" href="index.html"><span class="mk">{ic("key")}</span>רפי המנעולן</a><a class="pill" href="tel:{PHONE_INTL}">{ic("phone")}<span>{PHONE}</span></a></div></header>
<main>{body}</main>
<footer><div class="wrap"><b style="color:var(--ink)">רפי המנעולן</b><span>מנעולן באזור השרון – מקיסריה ועד הוד השרון. יוצא מנתניה.</span><span>טלפון: <a href="tel:{PHONE_INTL}">{PHONE}</a> · <a href="{WA}">וואטסאפ</a></span></div></footer>
<nav class="bar" aria-label="יצירת קשר"><a class="btn btn-call" href="tel:{PHONE_INTL}">{ic("phone")}התקשרו עכשיו</a><a class="btn btn-wa" href="{WA}">{WA_SVG}וואטסאפ</a></nav>
{JS}</body></html>'''
def hero(h1,sub,where="אליכם",crumb=""):
    return f'''<section class="hero"><div class="wrap"><div>{crumb}<span class="status"><span class="dot"></span><span class="t">זמין 24 שעות בימי חול ובמוצאי שבת</span></span>
<h1>{h1}</h1><p class="sub">{sub}</p>
<div class="cta"><a class="btn btn-call" href="tel:{PHONE_INTL}">{ic("phone")}התקשרו עכשיו</a><a class="btn btn-wa" href="{WA}">{WA_SVG}שלחו וואטסאפ</a></div>
<ul class="trust"><li>{ic("check")}מחיר ברור לפני העבודה</li><li>{ic("check")}פתיחה ללא נזק ככל שניתן</li><li>{ic("check")}מדברים ישירות איתי</li></ul></div>{eta(where)}</div></section>'''
def services_sec(title="השירותים שלי",lede="כל מה שקשור לדלתות, מנעולים וכספות – לבית ולעסק."):
    cards="".join(f'<a class="card" href="{s}.html"><span class="bub">{ic(i)}</span><h3>{n}</h3><p>{t}</p></a>' for s,n,i,t,_ in SERVICES)
    return f'<section class="sec"><div class="wrap"><h2>{title}</h2><p class="lede">{lede}</p><div class="grid">{cards}</div></div></section>'
STEPS=f'''<section class="sec alt"><div class="wrap"><h2>איך זה עובד</h2><p class="lede">שלושה צעדים, בלי מוקד ובלי המתנה על הקו.</p><div class="steps">
<div class="step"><h3>מתקשרים או שולחים וואטסאפ</h3><p>מספרים לי מה קרה ואיפה אתם. אני עונה בעצמי.</p></div>
<div class="step"><h3>אני מגיע תוך כ-25 דקות</h3><p>בקטנוע, כך שגם בפקקים ההגעה מהירה.</p></div>
<div class="step"><h3>מחיר ברור, ואז עבודה</h3><p>אתם מאשרים את המחיר לפני שמתחילים, ואני פותר את הבעיה.</p></div></div></div></section>'''
WHY=f'''<section class="sec"><div class="wrap"><h2>למה להתקשר אליי</h2><p class="lede">מנעולן עצמאי, לא מוקד שמעביר את הפנייה הלאה.</p><div class="grid">
<div class="card"><span class="bub">{ic("scooter")}</span><h3>הגעה בקטנוע</h3><p>בדרך כלל תוך כ-25 דקות לכל מקום באזור, גם בשעות העומס.</p></div>
<div class="card"><span class="bub">{ic("tag")}</span><h3>מחיר ידוע מראש</h3><p>בלי הפתעות בסוף העבודה. המחיר נאמר ומאושר לפני שמתחילים.</p></div>
<div class="card"><span class="bub">{ic("user")}</span><h3>ישירות מול בעל המקצוע</h3><p>מי שעונה לטלפון הוא מי שמגיע אליכם.</p></div>
<div class="card"><span class="bub">{ic("clock")}</span><h3>זמין גם בלילה</h3><p>24 שעות בימי חול, ביום שישי עד 16:00 ובמוצאי שבת.</p></div></div></div></section>'''
def area_sec(title="אזורי שירות"):
    chips="".join(f'<li><a href="{s}.html">{ic("pin")}מנעולן {b}</a></li>' for s,n,b,_ in CITIES)
    return f'<section class="sec alt"><div class="wrap"><h2>{title}</h2><p class="lede">יוצא מנתניה לכל אזור השרון – מקיסריה בצפון ועד הוד השרון בדרום.</p><ul class="chips">{chips}</ul></div></section>'
def faq_sec():
    q="".join(f'<details><summary>{a}</summary><p>{b}</p></details>' for a,b in FAQ)
    hrs='<div class="hours"><div><b>ראשון – חמישי</b><span>24 שעות</span></div><div><b>שישי</b><span>09:00–16:00</span></div><div><b>מוצאי שבת</b><span>19:00–00:00</span></div></div>'
    return f'<section class="sec"><div class="wrap two"><div><h2>שאלות נפוצות</h2><p class="lede">התשובות לשאלות שהכי שואלים אותי בטלפון.</p><div class="faq">{q}</div></div><div><h2>שעות זמינות</h2><p class="lede">מחוץ לשעות האלה אפשר להשאיר הודעה בוואטסאפ.</p>{hrs}</div></div></section>'
BAND=f'<section class="sec"><div class="wrap"><div class="band"><div><h2>ננעלתם בחוץ? אל תחכו.</h2><p>מתקשרים, ואני בדרך.</p></div><a class="btn" href="tel:{PHONE_INTL}">{ic("phone")}{PHONE}</a></div></div></section>'
ALL=[n for _,n,_,_ in CITIES]
open(f"{OUT}/style.css","w").write(CSS)
home=hero("מנעולן בנתניה והשרון, אצלכם תוך כ-25 דקות","פריצת דלתות, החלפת צילינדרים, תיקון מנעולים ופתיחת כספות. מקיסריה ועד הוד השרון.")+services_sec()+STEPS+WHY+area_sec()+faq_sec()+BAND
open(f"{OUT}/index.html","w").write(page("index","רפי המנעולן | מנעולן בנתניה והשרון – הגעה תוך כ-25 דקות","מנעולן מנתניה לכל השרון, מקיסריה ועד הוד השרון. פריצת דלתות, החלפת צילינדרים, תיקון מנעולים ופתיחת כספות. מחיר ברור לפני העבודה.",home,ALL))
for s,n,b,hood in CITIES:
    cr=f'<p class="crumb"><a href="index.html">ראשי</a> / מנעולן {b}</p><br>'
    body=hero(f"מנעולן {b}, אצלכם תוך כ-25 דקות",f"רפי המנעולן מגיע {b} בקטנוע. שירות ב{hood}.",n if s!="netanya" else "אליכם",cr)+services_sec(f"שירותי מנעולנות {b}",f"פריצת דלתות, צילינדרים, מנעולים וכספות {b} – לבית ולעסק.")+STEPS+WHY+faq_sec()+area_sec("עוד אזורים שאני מגיע אליהם")+BAND
    open(f"{OUT}/{s}.html","w").write(page(s,f"מנעולן {b} | רפי המנעולן – הגעה תוך כ-25 דקות",f"מנעולן {b}: פריצת דלתות, החלפת צילינדרים, תיקון מנעולים ופתיחת כספות. רפי המנעולן מגיע בקטנוע, מחיר ברור לפני העבודה.",body,[n]))
for s,n,i,t,items in SERVICES:
    cr=f'<p class="crumb"><a href="index.html">ראשי</a> / {n}</p><br>'
    inc="".join(f'<li>{ic("check")}<span>{x}</span></li>' for x in items)
    body=hero(f"{n} בנתניה והשרון",f"{t} מגיע בקטנוע מקיסריה ועד הוד השרון, בדרך כלל תוך כ-25 דקות.","אליכם",cr)+f'<section class="sec"><div class="wrap two"><div><h2>מה כולל השירות</h2><p class="lede">המחיר נאמר ומאושר לפני שמתחילים לעבוד.</p><ul class="incl">{inc}</ul></div><div><h2>שירותים נוספים</h2><p class="lede">גם את זה אפשר לסגור באותו ביקור.</p><div class="grid">'+"".join(f'<a class="card" href="{s2}.html"><span class="bub">{ic(i2)}</span><h3>{n2}</h3></a>' for s2,n2,i2,_,_ in SERVICES if s2!=s)+'</div></div></div></section>'+STEPS+faq_sec()+area_sec()+BAND
    open(f"{OUT}/{s}.html","w").write(page(s,f"{n} בנתניה והשרון | רפי המנעולן",f"{n} בנתניה והשרון – {t} הגעה בקטנוע תוך כ-25 דקות, מחיר ברור לפני העבודה.",body,ALL))
urls=[""]+[f"{s}.html" for s,*_ in CITIES]+[f"{s}.html" for s,*_ in SERVICES]
open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{DOMAIN}/{u}</loc></url>" for u in urls)+"</urlset>")
open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("Site généré dans",OUT)
