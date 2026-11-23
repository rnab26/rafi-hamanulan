"""Générateur du site « רפי המנעולן ».

Lancer depuis la racine du dépôt :  python3 _build/build.py
Tout ce qui est réglable est dans la section RÉGLAGES ci-dessous (une seule source de vérité).
"""
import os, json, datetime, builtins
def open(file, mode="r", *a, **k):  # UTF-8 + fins de ligne "\n" partout (sinon un build sous Windows diffère du dépôt)
    if "b" not in mode:
        k.setdefault("encoding", "utf-8"); k.setdefault("newline", "\n")
    return builtins.open(file, mode, *a, **k)
ROOT =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du repo
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
CONTENT_DATE = "2026-11-19"                       # date de dernière mise à jour du contenu (sitemap, articles) – à changer quand le contenu change
ETA_MIN = 25                                        # délai d'arrivée annoncé (minutes)
# Majoration selon l'heure de l'appel (fournie par Raphaël le 7 nov. 2026) : (heure début, heure fin, ₪). Jamais plus de 150 ₪.
NIGHT_TIERS = [(20, 22, 50), (22, 24, 100), (0, 8, 150)]   # pas de supplément de 08:00 à 20:00 (Rafi, 18 nov.)
NIGHT_MAX = 150
def _hh(h): return "00:00" if h == 24 else f"{h:02d}:00"
NIGHT_TXT = " · ".join(f"{_hh(a)}–{_hh(b)}: +{v} ₪" for a, b, v in NIGHT_TIERS)
REGION = "השרון"                                    # zone affichée. Volontairement AUCUNE ville de départ (demande de Rafi, 1er nov. 2026)
# Horaires : jour (0=dimanche … 6=samedi) -> liste de créneaux (heure début, heure fin), fin 24 = minuit
HOURS = {0: [(0, 24)], 1: [(0, 24)], 2: [(0, 24)], 3: [(0, 24)], 4: [(0, 24)], 5: [(9, 16)], 6: [(19, 24)]}
HOURS_DISPLAY = [("ראשון – חמישי", "24 שעות"), ("שישי", "09:00–16:00"), ("מוצאי שבת", "19:00–00:00")]
# Code de vérification Google Search Console (balise HTML) : coller seulement la valeur content="..."
GSC_VERIFICATION = ""
# Lien « laisser un avis » de la fiche Google Business (quand elle sera vérifiée). Vide = bouton masqué.
REVIEW_URL = "https://g.page/r/CavM3AVwHYkIEBM/review"
MIDRAG_URL = "https://www.midrag.co.il/SpCard/Sp/99543?areaId=10&serviceId=340&sortByCategory=333&isGeneric=true"   # fiche Midrag de Rafi (inscrit depuis 2–3 ans), lien fourni le 18 nov.
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
# icônes Tabler Icons (licence MIT, tabler.io) pour les badges du héros
"shekel":'<path d="M6 18v-12h4a4 4 0 0 1 4 4v4"/><path d="M18 6v12h-4a4 4 0 0 1-4-4v-4"/>',
"unlock":'<path d="M3 13a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-10a2 2 0 0 1-2-2z"/><path d="M9 16a1 1 0 1 0 2 0a1 1 0 0 0-2 0"/><path d="M13 11v-4a4 4 0 1 1 8 0v4"/>',
"hand":'<path d="M19.5 12.572l-7.5 7.428l-7.5-7.428a5 5 0 1 1 7.5-6.566a5 5 0 1 1 7.5 6.572"/><path d="M12 6l-3.293 3.293a1 1 0 0 0 0 1.414l.543 .543c.69 .69 1.81 .69 2.5 0l1-1a3.182 3.182 0 0 1 4.5 0l2.25 2.25"/><path d="M12.5 15.5l2 2"/><path d="M15 13l2 2"/>',
}
# Moto : Material Symbols « two_wheeler » (Google, licence Apache 2.0), choisie par Rafi le 18 nov. ; retournée pour rouler vers la gauche (RTL)
MOPED_SVG = '<svg class="ic sc" viewBox="0 -960 960 960" fill="currentColor" aria-hidden="true"><path transform="matrix(-1 0 0 1 960 0)" d="M157-200q-65 0-111-45.5T0-357q0-66 45.5-111.5T156-514l-47-36H25q-11 0-18-7t-7-18q0-11 7-18t18-7h156l99 60 149-56q5-2 10.5-3t10.5-1h129l-78-100h-59q-13 0-21.5-8.5T412-730q0-13 8.5-21.5T442-760h60q14 0 26.5 6t20.5 17l68 88 107-53q8-4 15 .5t7 12.5v65q0 6-4.5 10.5T731-609h-83l85 110q17-7 34-10.5t35-3.5q66 0 112 45.5T960-356q0 66-46 111t-112 45q-65 0-110.5-45.5T646-356q0-30 10-57t30-49l-35-45-137 209q-5 6-11 10t-14 4h-82q-5 0-10.5-2t-10.5-6l-72-65q0 66-45.5 111.5T157-200Zm0-60q41 0 69-28.5t28-68.5q0-40-28-68.5T157-454q-40 0-68.5 28T60-357q0 41 28.5 69t68.5 28Zm645 0q41 0 69.5-28t28.5-68q0-41-28.5-69.5T802-454q-40 0-68 28.5T706-356q0 40 28 68t68 28Z"/></svg>'
# Logo (option B, confirmée par Rafi le 18 nov.) : cadenas bleu + « ר » de Rafi. Une seule source : en-tête, favicon, logo.png
LOGO_SVG = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><linearGradient id="lgg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B82F6"/><stop offset="1" stop-color="#1446B4"/></linearGradient></defs>'
            '<path d="M19 28v-8a13 13 0 0 1 26 0v8" fill="none" stroke="#0E1A2B" stroke-width="6" stroke-linecap="round"/><rect x="8" y="25" width="48" height="36" rx="11" fill="url(#lgg)"/>'
            '<path d="M22 36h12a7 7 0 0 1 7 7v10" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
def ic(n, cls="ic"):
    if n == "moped": return MOPED_SVG
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'
WA_SVG = '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'

# (slug, nom, "ב+nom", quartiers/secteurs couverts)
CITIES = [
("netanya","נתניה","בנתניה","רמת פולג, עין התכלת, קריית השרון, קריית צאנז, אגמים, נאות גנים, דורה ומרכז העיר"),
("hadera","חדרה","בחדרה","מרכז העיר, גבעת אולגה, נווה חיים והשכונות החדשות"),
("givat-olga","גבעת אולגה","בגבעת אולגה","כל השכונה, עד חוף הים"),
("caesarea","קיסריה","בקיסריה","השכונות, הבתים הפרטיים ופארק התעשייה"),
("or-akiva","אור עקיבא","באור עקיבא","כל שכונות העיר"),
("jisr-az-zarqa","ג'סר א-זרקא","בג'סר א-זרקא","כל שכונות היישוב"),
("binyamina","בנימינה-גבעת עדה","בבנימינה-גבעת עדה","בנימינה וגבעת עדה"),
("pardes-hanna","פרדס חנה-כרכור","בפרדס חנה-כרכור","פרדס חנה, כרכור והשכונות החדשות"),
("kfar-yona","כפר יונה","בכפר יונה","השכונות הוותיקות והחדשות"),
("even-yehuda","אבן יהודה","באבן יהודה","המושבה והבתים הפרטיים"),
("kadima-zoran","קדימה-צורן","בקדימה-צורן","קדימה וצורן"),
("tel-mond","תל מונד","בתל מונד","כל היישוב"),
("tayibe","טייבה","בטייבה","כל שכונות העיר"),
("tira","טירה","בטירה","כל שכונות העיר"),
("qalansawe","קלנסווה","בקלנסווה","כל שכונות העיר"),
("pardesiya","פרדסיה","בפרדסיה","כל היישוב"),
("kfar-saba","כפר סבא","בכפר סבא","כל שכונות העיר"),
("raanana","רעננה","ברעננה","כל שכונות העיר"),
("herzliya","הרצליה","בהרצליה","הרצליה פיתוח, מרכז העיר והשכונות"),
("hod-hasharon","הוד השרון","בהוד השרון","כל שכונות העיר"),
("kochav-yair","כוכב יאיר-צור יגאל","בכוכב יאיר-צור יגאל","כוכב יאיר וצור יגאל"),
("ramat-hasharon","רמת השרון","ברמת השרון","כל שכונות העיר"),
("emek-hefer","עמק חפר","בעמק חפר","יישובי המועצה האזורית עמק חפר"),
("michmoret","מכמורת","במכמורת","כל המושב"),
("kfar-vitkin","כפר ויתקין","בכפר ויתקין","כל המושב"),
("kfar-haim","כפר חיים","בכפר חיים","כל המושב"),
("kfar-yedidya","כפר ידידיה","בכפר ידידיה","כל המושב"),
("beit-yitzhak","בית יצחק","בבית יצחק","בית יצחק-שער חפר"),
("udim","אודים","באודים","כל המושב"),
("kfar-netter","כפר נטר","בכפר נטר","כל המושב"),
("tel-yitzhak","תל יצחק","בתל יצחק","כל המושב"),
("bnei-zion","בני ציון","בבני ציון","כל המושב"),
("yakum","יקום","ביקום","כל הקיבוץ"),
("moshavim","מושבי השרון","במושבי השרון","אודים, יקום, מכמורת, כפר ויתקין, בית יהושע, חבצלת השרון, אביחיל ועוד"),
]
# slug: (à propos de la ville, conseil serrurerie propre au type d'habitat). Pas de chiffres ni de cas inventés.
SALT = "ליד הים האוויר המלוח והחול מאיצים חלודה בצילינדרים ובמנעולי השער – אם המפתח מתחיל להיתקע או להסתובב קשה, כדאי להחליף לפני שהוא נשבר בפנים."
PRIV = "בבית פרטי יש בדרך כלל כמה מנעולים – דלת ראשית, דלת שירות, שער, מחסן ותיבת דואר – וכדאי לבדוק את כולם בבת אחת ולהתאים צילינדר איכותי לכל דלת חיצונית."
BLD = "בבניינים עם דלתות פלדלת ישנות ומנעולים שחוקים, החלפת צילינדר לאיכותי היא השדרוג הזול ביותר לאבטחה, ואפשר לעשות אותה בלי להחליף את הדלת."
CITY_TEXT = {
"netanya": ("נתניה היא עיר חוף גדולה: מגדלי מגורים לאורך הים ובעיר ימים, בניינים ותיקים במרכז, ושכונות של בתים פרטיים כמו קריית השרון ורמת פולג.", SALT + " " + BLD),
"hadera": ("חדרה משלבת מרכז עיר ותיק עם בניינים בני עשרות שנים, ושכונות חדשות יותר עם בנייה חדשה ובתים פרטיים.", BLD),
"givat-olga": ("גבעת אולגה היא שכונה על חוף הים של חדרה, עם בניינים ובתים צמודי קרקע לא רחוק מהמים.", SALT),
"caesarea": ("בקיסריה רוב הבתים פרטיים, לא מעט וילות עם שער, גדר ודלתות כניסה כבדות, ובנוסף פארק תעשייה עם עסקים.", SALT + " " + PRIV),
"or-akiva": ("אור עקיבא היא עיר קטנה שבה בניינים ותיקים עומדים לצד שכונות של בתים פרטיים.", BLD),
"jisr-az-zarqa": ("ג'סר א-זרקא הוא יישוב על חוף הים עם בתים צמודי קרקע ובניינים קטנים קרוב לשפת הים.", SALT),
"binyamina": ("בנימינה היא מושבה ותיקה בנוף של כרמים ויקבים, וגבעת עדה שכנה לה – בעיקר בתים פרטיים עם חצר ושער.", PRIV),
"pardes-hanna": ("פרדס חנה-כרכור היא מועצה גדולה שהתפתחה מפרדסים: שכונות רבות של בתים פרטיים, ולצדן בנייה חדשה בבניינים.", PRIV),
"kfar-yona": ("כפר יונה היא עיר שרונית שבה בניינים ותיקים בשכונות מרכזיות לצד שכונות חדשות ובתים פרטיים.", BLD),
"even-yehuda": ("אבן יהודה היא מושבה ותיקה עם הרבה בתים פרטיים בשכונות שקטות, חצרות ושערים.", PRIV),
"kadima-zoran": ("קדימה-צורן מורכבת משני יישובים סמוכים עם בתים פרטיים רבים וגם בנייה חדשה בבניינים.", PRIV),
"tel-mond": ("תל מונד היא יישוב ותיק בשרון עם בתים פרטיים רבים וחצרות, וכמה שכונות חדשות.", PRIV),
"tayibe": ("בטייבה יש בתים פרטיים לצד בניינים, ובבית עם כמה כניסות ויחידות יש גם יותר מנעולים לשמור עליהם.", PRIV + " " + BLD),
"tira": ("טירה היא עיר גדולה במשולש עם בתים פרטיים ובניינים בכמה שכונות.", PRIV),
"qalansawe": ("קלנסווה היא עיר במשולש עם בתים פרטיים, בניינים ומסחר לאורך הרחובות הראשיים.", PRIV + " " + BLD),
"pardesiya": ("פרדסיה היא יישוב קטן עם בתים פרטיים וחצרות, כמעט בלי בניינים גבוהים.", PRIV),
"kfar-saba": ("כפר סבא היא עיר גדולה עם בניינים מכל התקופות – ממרכז העיר הוותיק ועד שכונות חדשות – ושכונות של בתים פרטיים.", BLD + " " + PRIV),
"raanana": ("ברעננה בתים פרטיים רבים עם חצר, לצד מגדלים ובניינים חדשים במרכז העיר ובאזור התעשייה.", PRIV),
"herzliya": ("הרצליה כוללת את הרצליה פיתוח עם וילות ושערים, מרכז עיר עם בניינים ותיקים, ושכונות קרובות לים והמרינה.", SALT + " " + PRIV),
"hod-hasharon": ("הוד השרון היא עיר שרונית עם שכונות רבות של בתים פרטיים ובניינים חדשים יחסית.", PRIV + " " + BLD),
"kochav-yair": ("כוכב יאיר-צור יגאל הוא יישוב קהילתי של בתים פרטיים רחבים עם חצר ושער, בקצה השרון הדרומי.", PRIV),
"ramat-hasharon": ("רמת השרון היא עיר ירוקה סמוכה לתל אביב, עם הרבה בתים פרטיים ושכונות שקטות ובניינים חדשים בכמה מרכזים.", PRIV),
"emek-hefer": ("עמק חפר היא מועצה אזורית של מושבים וקיבוצים ויישובים קהילתיים: בתים פרטיים, חצרות, מחסנים ומבני משק.", PRIV),
"michmoret": ("מכמורת היא מושב על חוף הים עם בתים פרטיים וחצרות והרבה מחסנים ומבני משק.", SALT + " " + PRIV),
"kfar-vitkin": ("כפר ויתקין הוא מושב ותיק בשרון הצפוני, לא רחוק מהים, עם בתים פרטיים וחצרות.", PRIV),
"kfar-haim": ("כפר חיים הוא מושב בעמק חפר, עם בתים פרטיים בחצרות גדולות ומבני משק.", PRIV),
"kfar-yedidya": ("כפר ידידיה הוא מושב קטן בעמק חפר, בתים פרטיים וחצרות עם מחסנים ושערים.", PRIV),
"beit-yitzhak": ("בית יצחק-שער חפר הוא יישוב בעמק חפר, עם בתים פרטיים וחצרות.", PRIV),
"udim": ("אודים הוא מושב קטן בעמק חפר, ובו בעיקר בתים פרטיים וחצרות, ומבני משק לצדם.", PRIV),
"kfar-netter": ("כפר נטר הוא מושב קטן בעמק חפר, עם בתים פרטיים, חצרות ושערים.", PRIV),
"tel-yitzhak": ("תל יצחק הוא מושב בעמק חפר, קרוב לחוף, עם בתים פרטיים וחצרות.", SALT + " " + PRIV),
"bnei-zion": ("בני ציון הוא מושב בעמק חפר עם בתים פרטיים וחצרות רחבות.", PRIV),
"yakum": ("יקום הוא קיבוץ בשרון הדרומי שהתרחב גם לשכונות של בתים פרטיים, ויש בו מבני משק ועסקים.", PRIV),
"moshavim": ("מושבי השרון – מושבים וקיבוצים קטנים עם בתים פרטיים, חצרות, שערים ומחסנים, לעיתים רחוקים מהכביש הראשי.", PRIV),
}
# Localités proches (texte unique par page ville + maillage interne ; 19 nov. 2026, audit SEO). Toutes dans la zone de Rafi.
NEARBY = {
"netanya": ["even-yehuda", "kfar-yona", "udim", "beit-yitzhak", "kfar-netter"],
"hadera": ["givat-olga", "pardes-hanna", "or-akiva", "caesarea", "emek-hefer"],
"givat-olga": ["hadera", "michmoret", "caesarea"],
"caesarea": ["or-akiva", "jisr-az-zarqa", "binyamina", "hadera"],
"or-akiva": ["caesarea", "hadera", "binyamina"],
"jisr-az-zarqa": ["caesarea", "binyamina", "or-akiva"],
"binyamina": ["pardes-hanna", "caesarea", "or-akiva"],
"pardes-hanna": ["binyamina", "hadera", "caesarea"],
"kfar-yona": ["netanya", "beit-yitzhak", "pardesiya", "emek-hefer"],
"even-yehuda": ["netanya", "kadima-zoran", "tel-mond", "kfar-netter"],
"kadima-zoran": ["even-yehuda", "tel-mond", "netanya"],
"tel-mond": ["kadima-zoran", "even-yehuda", "pardesiya", "tayibe"],
"tayibe": ["qalansawe", "tira", "tel-mond"],
"tira": ["tayibe", "kfar-saba", "kochav-yair"],
"qalansawe": ["tayibe", "kfar-yona", "tel-mond"],
"pardesiya": ["tel-mond", "kfar-yona", "netanya"],
"kfar-saba": ["raanana", "hod-hasharon", "kochav-yair", "tira"],
"raanana": ["kfar-saba", "herzliya", "hod-hasharon"],
"herzliya": ["raanana", "ramat-hasharon", "yakum", "bnei-zion"],
"hod-hasharon": ["kfar-saba", "raanana", "ramat-hasharon"],
"kochav-yair": ["kfar-saba", "tira", "hod-hasharon"],
"ramat-hasharon": ["herzliya", "hod-hasharon", "raanana"],
"emek-hefer": ["kfar-vitkin", "kfar-haim", "kfar-yedidya", "beit-yitzhak", "michmoret"],
"michmoret": ["kfar-vitkin", "givat-olga", "emek-hefer"],
"kfar-vitkin": ["michmoret", "kfar-haim", "emek-hefer"],
"kfar-haim": ["kfar-vitkin", "kfar-yedidya", "emek-hefer"],
"kfar-yedidya": ["kfar-haim", "beit-yitzhak", "emek-hefer"],
"beit-yitzhak": ["netanya", "kfar-yona", "kfar-yedidya", "emek-hefer"],
"udim": ["netanya", "kfar-netter", "tel-yitzhak", "yakum"],
"kfar-netter": ["netanya", "even-yehuda", "udim"],
"tel-yitzhak": ["udim", "bnei-zion", "yakum"],
"bnei-zion": ["tel-yitzhak", "herzliya", "raanana"],
"yakum": ["herzliya", "udim", "tel-yitzhak"],
"moshavim": ["emek-hefer", "udim", "yakum", "michmoret", "kfar-vitkin"],
}
def nearby_html(slug):
    names = {c[0]: c[1] for c in CITIES}
    links = [f'ל<a href="{s}.html">{names[s]}</a>' for s in NEARBY.get(slug, []) if s in names and s != slug]
    if not links: return ""
    txt = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " ו" + links[-1]
    return f"<p>באותו אזור אני מגיע גם {txt} – באותה מהירות ובאותם מחירים.</p>"
# (slug, nom, image, phrase courte, ce qui est inclus, mots-clés secondaires pour la description)
SERVICES = [
("door-opening","פריצת דלתות","door-opening","ננעלתם בחוץ? פותח את הדלת בלי לגרום נזק, ברוב המקרים.",
 ["דלת כניסה ופלדלת","דלתות פנים וחדרי אמבטיה","מפתח שנשבר בתוך המנעול","מפתח שנשאר בפנים"],"פורץ דלתות ופורץ מנעולים"),
("cylinder","החלפת צילינדר","cylinder","אחרי מעבר דירה, אובדן מפתחות או פריצה.",
 ["צילינדרים איכותיים וברמת אבטחה גבוהה – מולטילוק, רב-בריח, מגנום ועוד","החלפה אחרי מעבר דירה","החלפה אחרי פריצה או אובדן מפתחות","מפתח אחד לכמה דלתות"],"החלפת צילינדר מולטילוק ורב-בריח"),
("lock-repair","תיקון והחלפת מנעולים","lock-repair","מנעול תקוע, ידית שבורה, דלת שלא נסגרת.",
 ["מנעולי רב-בריח","ידיות ומנגנונים","מנעולים לשערים ולתיבות דואר","כיוון דלת שנתקעת"],"תיקון מנעולים ומנעולי רב-בריח"),
("safe","פתיחת כספות","safe","קוד שנשכח או מנגנון שנתקע.",
 ["כספות עם קוד","כספות עם מפתח","החלפת קוד אחרי פתיחה"],"פריצת כספות"),
("security","שדרוג מיגון","security","בודק את הדלת והמנעולים וממליץ על פתרון – במחיר ברור.",
 ["שדרוג צילינדר ומנעולים","התקנת מנעול כספת / מנעול נוסף לפלדלת","מיגון לעסקים ולמחסנים"],"שדרוג מיגון לדלת"),
]
FAQ = [
("תוך כמה זמן אתה מגיע?",f"אני עובד בקטנוע בכל אזור {REGION}, אז גם בפקקים אני מגיע בדרך כלל תוך כ-{ETA_MIN} דקות, מקיסריה ועד רמת השרון."),
("אדע כמה זה עולה לפני שמתחילים?","כן. אחרי שאני רואה את הדלת או המנעול אני אומר לכם מחיר ברור, ומתחילים לעבוד רק אחרי שאישרתם."),
("הדלת תיפגע בזמן הפריצה?","ברוב המקרים אפשר לפתוח בלי לגרום נזק לדלת. אם צריך להחליף את הצילינדר אחרי הפתיחה, אני מחליף אותו באותו ביקור."),
("מתי אתה זמין?","24 שעות בימים ראשון עד חמישי, ביום שישי מ-09:00 עד 16:00, ובמוצאי שבת עד חצות."),
("מה עושים אחרי פריצה לבית?","מומלץ להחליף צילינדר כמה שיותר מהר. אני מגיע, מחליף ויכול להמליץ על שדרוג מיגון לדלת."),
]

HERO_SVG = open(os.path.join(ROOT, "_build/hero.svg"), encoding="utf-8").read()

# ------------------------------------------------------------------ CSS
CSS = r"""
@font-face{font-family:'Rubik';font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/rubik-hebrew.woff2) format('woff2');unicode-range:U+0307-0308,U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}
@font-face{font-family:'Rubik';font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/rubik-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
:root{--bg:#fff;--soft:#F5F5F7;--ink:#1D1D1F;--muted:#6E6E73;--line:#E5E5EA;--blue:#0071E3;--blue-d:#0062C4;--blue-soft:#E8F1FC;--wa:#1FAF5A;--amber:#F5A524;--green:#16A34A;--r:20px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Rubik",system-ui,Arial,sans-serif;font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased;letter-spacing:-.01em;padding-bottom:84px}
a{color:var(--blue)}h1,h2,h3{line-height:1.2;margin:0;font-weight:700}p{margin:0}
img{display:block;max-width:100%;height:auto}
a:focus-visible,summary:focus-visible{outline:3px solid var(--amber);outline-offset:2px;border-radius:8px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.ic{width:22px;height:22px;flex:none}
/* header */
.hd{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700;font-size:19px}
.logo .mk{width:38px;height:38px;display:block}.logo .mk svg{width:38px;height:38px;display:block}.logo em{font-style:normal;color:var(--blue)}
.logo .mk .ic{width:20px;height:20px}
.pill{display:inline-flex;align-items:center;gap:6px;color:var(--blue);text-decoration:none;font-weight:700;font-size:16px}
.pill span{direction:ltr}.pill .ic{width:18px;height:18px}
.hd .wrap{gap:10px}.hd .logo{margin-inline-end:auto}
@media(max-width:430px){.pill span{display:none}.pill{width:40px;height:40px;justify-content:center;border-radius:12px;background:var(--blue-soft)}.logo{font-size:18px}}
.nav summary{list-style:none;width:42px;height:40px;border-radius:12px;background:var(--ink);display:flex;flex-direction:column;justify-content:center;align-items:center;gap:4px;cursor:pointer}.nav summary::-webkit-details-marker{display:none}
.nav summary i{display:block;width:18px;height:2px;border-radius:2px;background:#fff;transition:transform .2s,opacity .2s}
.nav[open] summary i:nth-child(1){transform:translateY(6px) rotate(45deg)}.nav[open] summary i:nth-child(2){opacity:0}.nav[open] summary i:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
.navp{position:fixed;top:60px;inset-inline:0;height:calc(100vh - 60px);height:calc(100dvh - 60px);background:#fff;overflow-y:auto;padding:16px 20px 120px;border-top:1px solid var(--line);z-index:30}
@media(min-width:760px){.navp{inset-inline:auto 24px;left:24px;right:auto;height:auto;width:380px;max-height:calc(100vh - 80px);border:1px solid var(--line);border-radius:20px;box-shadow:0 20px 50px rgba(14,26,43,.18)}}
.navp .nbig{display:flex;align-items:center;gap:12px;padding:12px;margin-bottom:8px;border-radius:14px;background:var(--blue-soft);color:var(--ink);font-weight:700;font-size:17px;text-decoration:none}
.navp .nbig .ic{width:36px;height:36px;padding:7px;border-radius:10px;background:var(--blue);color:#fff}
.navp p{margin:18px 0 6px;color:var(--muted);font-size:13px;font-weight:700}
.navp ul{list-style:none;margin:0;padding:0}.navp li a{display:flex;align-items:center;gap:12px;padding:8px 0;color:var(--ink);text-decoration:none;font-size:16px;border-bottom:1px solid var(--line)}
.navp li img{width:44px;height:44px;border-radius:10px;object-fit:cover;flex:none}.navp .cta{margin-top:20px}
.svc{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:12px}@media(min-width:760px){.svc{grid-template-columns:repeat(5,1fr)}}
.svc a{display:block;text-decoration:none;color:var(--ink);font-weight:700;font-size:15px}.svc img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:14px;margin-bottom:6px}
.gds{list-style:none;margin:0;padding:0}.gds a{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink);font-weight:500}
.gds img{width:64px;height:64px;border-radius:12px;object-fit:cover;flex:none}.gds span{flex:1}.gds .ic{width:18px;height:18px;color:var(--blue)}
/* hero */
.hero{padding:20px 0 8px}
.hero .wrap{display:grid;gap:24px}
.hero-img{position:relative;border-radius:24px;overflow:hidden;aspect-ratio:4/3;background:var(--soft)}
.hero-img>img,.hero-img>svg{width:100%;height:100%;object-fit:cover;display:block}
.pro{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--line);border-radius:22px;padding:12px 14px;box-shadow:0 6px 20px rgba(14,26,43,.08);max-width:460px}
.pro>img{width:92px;height:92px;border-radius:50%;object-fit:cover;flex:none;border:3px solid #fff;box-shadow:0 0 0 3px var(--blue)}
.who{flex:1;min-width:0}.who b{display:block;font-size:20px}.who small{display:block;color:var(--muted);font-size:14px}
.eta-badge{flex:none;display:flex;flex-direction:column;align-items:center;gap:2px;background:var(--blue-soft);border-radius:16px;padding:8px 12px;text-align:center}
.eta-badge .sc{width:44px;height:44px;color:var(--blue)}.eta-badge b{display:block;font-size:19px;line-height:1.1}.eta-badge small{color:var(--muted);font-size:12px}
@media(min-width:880px){.hero{padding:48px 0 16px}.hero .wrap{grid-template-columns:1.2fr .8fr;align-items:center;gap:20px 56px}.hero-txt{grid-column:1;grid-row:1/3}.pro{grid-column:2;grid-row:1;flex-direction:column;text-align:center;padding:24px;max-width:none}.pro>img{width:170px;height:170px}.trust{grid-column:2;grid-row:2;align-self:start}}
.status{display:inline-flex;align-items:center;gap:10px;font-size:16px;font-weight:700;color:var(--muted);background:var(--soft);border-radius:999px;padding:8px 16px 8px 14px}
.dot{position:relative;width:12px;height:12px;border-radius:50%;background:var(--muted);flex:none}
.status.on{color:#11803A;background:#E7F6EC}.status.on .dot{background:var(--green)}
.status.on .dot::after{content:"";position:absolute;inset:0;border-radius:50%;background:var(--green);animation:ping 1.6s cubic-bezier(0,0,.2,1) infinite}
@keyframes ping{0%{transform:scale(1);opacity:.75}80%,100%{transform:scale(2.6);opacity:0}}
.status.off{color:#9A5B00;background:#FFF4E0}.status.off .dot{background:var(--amber)}
.hero h1{font-size:clamp(32px,7vw,56px);letter-spacing:-.015em;margin:10px 0 12px}
.hero .sub{color:var(--muted);font-size:18px;margin:0 0 22px}
.cta{display:grid;gap:10px;max-width:440px;grid-template-columns:1fr 1fr}
.btn{display:flex;align-items:center;justify-content:center;gap:8px;min-height:54px;border-radius:14px;font-weight:700;font-size:17px;text-decoration:none;padding:0 16px}
.btn-call{background:var(--blue);color:#fff}.btn-call:hover{background:var(--blue-d)}
.btn-wa{background:var(--wa);color:#fff}
.crumb{font-size:14px;color:var(--muted);margin-bottom:14px}.crumb a{color:var(--muted);text-decoration:none}
/* trust */
.trust{display:grid;gap:10px;grid-template-columns:repeat(3,1fr);list-style:none;margin:0;padding:0}
.trust li{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px 6px 14px;box-shadow:0 6px 18px rgba(14,26,43,.07);line-height:1.25}
.trust .ic{width:56px;height:56px;padding:13px;border-radius:18px;color:#fff;margin-bottom:6px;stroke-width:2;background:linear-gradient(135deg,#4F8BFF,#1A56DB);box-shadow:0 8px 16px rgba(26,86,219,.30)}
.trust li:nth-child(1) .ic{background:linear-gradient(135deg,#34D399,#15803D);box-shadow:0 8px 16px rgba(21,128,61,.30)}
.trust li:nth-child(3) .ic{background:linear-gradient(135deg,#475569,#0E1A2B);box-shadow:0 8px 16px rgba(14,26,43,.30)}
.trust b{font-size:15px;color:var(--ink)}.trust small{font-size:13px;color:var(--muted)}
.cats{display:flex;gap:12px;overflow-x:auto;list-style:none;margin:0 -20px 20px;padding:4px 20px 8px;scrollbar-width:none}.cats::-webkit-scrollbar{display:none}
.cats a{flex:none;width:86px;display:flex;flex-direction:column;align-items:center;gap:6px;text-decoration:none;color:var(--ink);font-size:13px;font-weight:600;text-align:center;line-height:1.2}
.cats img{width:70px;height:70px;border-radius:20px;object-fit:cover;box-shadow:0 4px 12px rgba(14,26,43,.12);border:2px solid #fff}
#prix{padding-top:36px}.sec h2.sh,.sec h1.sh{font-size:clamp(26px,4.6vw,36px);letter-spacing:-.01em;margin-bottom:18px}.sec h1.sh small{display:block;font-size:17px;font-weight:400;color:var(--muted);margin-top:8px}
.accs{display:grid;gap:10px}
.acc{background:#fff;border:1px solid var(--line);border-radius:18px;scroll-margin-top:76px;box-shadow:0 2px 10px rgba(14,26,43,.04)}
a.acc{display:block;color:inherit;text-decoration:none;background:#fff}a.acc .accl{display:flex;align-items:center;gap:14px;padding:10px 12px}a.acc .accl>span{flex:1}a.acc b{display:block;font-size:18px}a.acc small{color:var(--green);font-weight:700;font-size:14px}a.acc i{width:34px;height:34px;border-radius:50%;background:var(--blue-soft);flex:none;position:relative}a.acc i::after{content:"";position:absolute;inset:0;margin:auto;width:9px;height:9px;border-right:2.5px solid var(--blue);border-bottom:2.5px solid var(--blue);transform:translateX(2px) rotate(-45deg)}a.acc img{width:64px;height:64px;border-radius:14px;object-fit:cover;flex:none}
.acc summary{list-style:none;display:flex;align-items:center;gap:14px;padding:10px 12px;cursor:pointer}.acc summary::-webkit-details-marker{display:none}
.acc summary img{width:64px;height:64px;border-radius:14px;object-fit:cover;flex:none;cursor:pointer}
.acc summary span{flex:1}.acc summary b{display:block;font-size:18px}.acc summary small{color:var(--green);font-weight:700;font-size:14px}
.acc summary i{width:34px;height:34px;border-radius:50%;background:var(--blue-soft);flex:none;position:relative}
.acc summary i::after{content:"";position:absolute;inset:0;margin:auto;width:9px;height:9px;border-right:2.5px solid var(--blue);border-bottom:2.5px solid var(--blue);transform:translateY(-2px) rotate(45deg);transition:transform .2s}
.acc[open] summary i::after{transform:translateY(2px) rotate(-135deg)}
.acc[open]{border:2px solid var(--blue);box-shadow:0 10px 28px rgba(26,86,219,.16);margin:10px 0 22px;overflow:hidden}
.acc[open] summary{background:var(--blue-soft);border-bottom:1px solid #C9D8F8;margin-bottom:6px}
.accx{display:block;width:100%;border:0;border-top:1px solid var(--line);background:var(--soft);color:var(--blue);font:inherit;font-weight:700;padding:12px;cursor:pointer}.acc .prows{padding:0 16px 8px}.acc .pnote{padding:0 16px 14px}


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
.steps .sc{height:auto;padding:12px 8px}.steps .ic{width:52px;height:52px;padding:13px;border-radius:16px;background:#fff;color:var(--blue);box-shadow:0 2px 10px rgba(14,26,43,.06)}
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
.prows{list-style:none;margin:0;padding:0}.prows li{border-bottom:1px dashed var(--line)}.prows label{display:flex;align-items:center;gap:12px;padding:10px 0;cursor:pointer}.prows li span{flex:1}
.pick{appearance:none;-webkit-appearance:none;width:24px;height:24px;border:2px solid #B8C4D4;border-radius:7px;flex:none;display:grid;place-items:center;margin:0;background:#fff}
.pick:checked{background:var(--wa);border-color:var(--wa)}.pick:checked::after{content:"✓";color:#fff;font-weight:700;font-size:15px}
.prows li.psub{border:0;margin:18px 0 6px;padding:10px 14px;font-weight:700;font-size:16px;color:#fff;background:var(--blue);border-radius:12px}.prows li.psub:first-child{margin-top:4px}
.prows b s{display:block;color:#DC2626;font-weight:500;font-size:.8em;text-align:center;text-decoration-thickness:2px}.prows b:has(s){text-align:center;color:var(--green)}
.prows li:has(.pick:checked){background:#F0FAF3;border-radius:10px}
.pick:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.nightb{background:#0E1A2B;color:#fff;border-radius:16px;padding:10px 12px;margin-bottom:14px}
.nightb .nt{font-size:14px;color:#C9D3E1;margin-bottom:8px}.nightb .nt b{color:#fff;font-size:15px}
.nightb .nrow{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.nightb .nrow span{background:rgba(255,255,255,.09);border-radius:10px;padding:5px 4px;text-align:center;font-size:12.5px;color:#C9D3E1}
.nightb .nrow b{display:block;color:#FFD166;font-size:16px}.nightb small{display:block;margin-top:7px;font-size:13px;color:#7EE2A8;font-weight:500}
.pickhint{background:#E7F6EC;color:#11803A;border-radius:14px;padding:12px 16px;font-weight:500;margin-bottom:18px}
/* panier WhatsApp */
.selbar{position:fixed;left:12px;right:12px;bottom:calc(76px + env(safe-area-inset-bottom));z-index:31;background:var(--ink);color:#fff;border-radius:18px;padding:12px 14px;display:none;align-items:center;gap:12px;box-shadow:0 10px 30px rgba(14,26,43,.3)}
.selbar.show{display:flex}.selbar .si{flex:1;font-size:14px;line-height:1.3}.selbar .si b{font-size:16px;display:block}
.selbar .btn{min-height:46px;padding:0 14px;font-size:15px;white-space:nowrap}.selbar .x{background:none;border:0;color:#9FB0C6;font-size:22px;padding:4px 6px;cursor:pointer}
@media(min-width:880px){.selbar{left:auto;right:24px;bottom:24px;max-width:460px}}
/* aperçu photos */
main img{cursor:zoom-in}main a img{cursor:pointer}.lb{position:fixed;inset:0;z-index:50;background:rgba(8,14,24,.9);display:none;align-items:center;justify-content:center;padding:20px;flex-direction:column;gap:12px}
.lb.show{display:flex}.lb img{max-width:min(92vw,900px);max-height:78vh;min-width:min(80vw,420px);object-fit:contain;border-radius:14px;background:#fff}
.lb p{color:#fff;margin:0;text-align:center;font-weight:500}.lb button{position:absolute;top:14px;left:14px;background:#fff;border:0;border-radius:50%;width:44px;height:44px;font-size:22px;cursor:pointer}
.pth{width:56px;height:56px;border-radius:12px;object-fit:cover;flex:none;background:var(--soft)}.pth.ph{display:grid;place-items:center;color:var(--blue)}.pcard .pth{width:56px;height:56px;aspect-ratio:1}
.prows li:last-child{border:0}.prows b{white-space:nowrap;color:var(--blue)}.prows b.long{white-space:normal;text-align:left;max-width:55%}
.pnote{color:var(--muted);font-size:14px;margin-top:8px}.pnotes{color:var(--muted);font-size:15px;margin:20px 0 0;padding-inline-start:20px}
/* articles */
.art{max-width:720px}.art h1{font-size:clamp(28px,6vw,40px);margin:8px 0 14px}.art .intro{margin:0 0 24px}.art .meta{color:#6E6E73;font-size:14px;margin:-6px 0 14px}.art .rel{margin:28px 0 0;font-weight:500}
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
.bar .btn{min-height:50px;font-size:16px}.bar{transition:transform .25s}.bar.hid{transform:translateY(110%)}body.barhid .selbar{bottom:calc(12px + env(safe-area-inset-bottom))}
@media(min-width:880px){.bar{display:none}body{padding-bottom:0}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
/* ---- Style Apple (Rafi, 18 nov.) : police système, gris Apple, pilules, en-tête translucide, listes iOS ---- */
h1,h2,h3{letter-spacing:-.025em;font-weight:700}
.hd{background:rgba(255,255,255,.72);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);border-bottom:.5px solid rgba(0,0,0,.12)}
.btn{border-radius:980px;font-weight:600;min-height:52px;transition:filter .15s,transform .1s}.btn:active{transform:scale(.98)}.btn:hover{filter:brightness(1.06)}
.hero{background:linear-gradient(180deg,#fff,#F5F5F7)}.hero h1{font-weight:700;letter-spacing:-.03em}
.pro{border:0;border-radius:22px;box-shadow:0 4px 24px rgba(0,0,0,.06)}.pro>img{box-shadow:0 0 0 3px #fff,0 0 0 5px var(--blue)}
.eta-badge{background:#F5F5F7}
.status{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.trust li{border:0;box-shadow:0 4px 24px rgba(0,0,0,.06);border-radius:22px}
.trust .ic{border-radius:14px;box-shadow:none}
#prix{background:#F5F5F7}
.accs{gap:12px}.acc{border:0;border-radius:18px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.acc summary i{background:#F5F5F7}.acc summary i::after{border-color:#86868B}
.acc[open]{border:0;box-shadow:0 8px 30px rgba(0,0,0,.10);margin:6px 0 18px}
.acc[open] summary{background:#fff;border-bottom:.5px solid var(--line)}.acc[open] summary i{background:var(--blue)}.acc[open] summary i::after{border-color:#fff}
.prows li{border-bottom:.5px solid var(--line)}.prows li.psub{border-radius:10px;font-weight:600;letter-spacing:0}
.prows b{font-weight:600}.pth{border-radius:10px}
.accx{background:#fff;font-weight:600}
.nightb{background:#1D1D1F;border-radius:18px}.nightb .nrow span{border-radius:12px}
.pickhint,.pnotes{border-radius:14px}
.chips a{border:0;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.faq details{border-bottom:.5px solid var(--line)}
.navp{background:rgba(255,255,255,.96);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px)}.navp .nbig{background:#F5F5F7}.navp .nbig .ic{border-radius:9px}
.nav summary{background:#1D1D1F;border-radius:980px}
.bar{background:rgba(255,255,255,.8);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);border-top:.5px solid rgba(0,0,0,.12)}
.selbar{border-radius:22px}
.svc img,.gds img{border-radius:14px}
footer{background:#F5F5F7;border-top:0;font-size:12px}
"""

# ------------------------------------------------------------------ statut « disponible » (calculé depuis HOURS)
JS = ("<script>(function(){try{var H=" + json.dumps({str(k): v for k, v in HOURS.items()}) + ";"
      "var f=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Jerusalem',weekday:'short',hour:'2-digit',hour12:false});"
      "var p=f.formatToParts(new Date());var D=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];"
      "var d=D.indexOf(p.find(function(x){return x.type==='weekday'}).value),h=+p.find(function(x){return x.type==='hour'}).value%24;"
      "var on=(H[d]||[]).some(function(s){return h>=s[0]&&h<s[1]});"
      "document.querySelectorAll('.status').forEach(function(el){if(on){el.classList.add('on');el.querySelector('.t').textContent='זמין עכשיו – עונה מיד'}"
      "else{el.classList.add('off');el.querySelector('.t').textContent='מחוץ לשעות – השאירו הודעה בוואטסאפ'}})}catch(e){}})();</script>")


UI_JS = ("<div class=\"selbar\" id=\"selbar\" role=\"region\" aria-label=\"הבחירה שלי\"><button class=\"x\" id=\"selclr\" aria-label=\"ניקוי\">×</button>"
  "<div class=\"si\"><b id=\"selc\"></b><span id=\"selt\"></span></div><a class=\"btn btn-wa\" id=\"selgo\" href=\"#\">" + WA_SVG + "שלחו בוואטסאפ</a></div>"
  "<div class=\"lb\" id=\"lb\" role=\"dialog\" aria-modal=\"true\" aria-label=\"תמונה\"><button id=\"lbx\" aria-label=\"סגירה\">×</button><img id=\"lbi\" alt=\"\"><p id=\"lbp\"></p></div>"
  "<script>(function(){var W='" + f"https://wa.me/{WA_NUMBER}" + "',bar=document.getElementById('selbar');"
  "function upd(){var c=[].slice.call(document.querySelectorAll('.pick:checked'));if(!c.length){bar.classList.remove('show');return}"
  "var NT=" + json.dumps(NIGHT_TIERS) + ",hr=+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Jerusalem',hour:'2-digit',hour12:false}).format(new Date())%24,ns=0;"
  "NT.forEach(function(t){if(hr>=t[0]&&hr<t[1])ns=t[2]});ns=Math.min(ns," + str(NIGHT_MAX) + ");"
  "var sum=0,fix=true,lines=c.map(function(x){var p=+x.dataset.p;if(p)sum+=p;else fix=false;return '• '+x.dataset.l+' ('+x.dataset.t+')'});"
  "document.getElementById('selc').textContent=c.length+(c.length>1?' שירותים נבחרו':' שירות נבחר');"
  "if(ns){lines.push('• תוספת לפי שעת הקריאה (+'+ns+' ₪)');sum+=ns}"
  "document.getElementById('selt').textContent=sum?('לפי המחירון: '+(fix?'':'החל מ-')+sum+' ₪'+(ns?' (כולל תוספת שעה '+ns+' ₪)':'')):'';"
  "var msg='שלום רפי, אני צריך:\\n'+lines.join('\\n')+'\\n\\nהכתובת שלי: ';"
  "document.getElementById('selgo').href=W+'?text='+encodeURIComponent(msg);bar.classList.add('show')}"
  "document.addEventListener('change',function(e){if(e.target.classList&&e.target.classList.contains('pick'))upd()});"
  "document.getElementById('selclr').onclick=function(){document.querySelectorAll('.pick:checked').forEach(function(x){x.checked=false});upd()};"
  "var lb=document.getElementById('lb'),lbi=document.getElementById('lbi'),lbp=document.getElementById('lbp');"
  "document.addEventListener('click',function(e){var t=e.target;if(t.tagName==='IMG'&&t.closest('main')&&!t.closest('a')&&!t.closest('summary')){e.preventDefault();lbi.src=t.currentSrc||t.src;lbi.alt=t.alt;lbp.textContent=t.alt;lb.classList.add('show')}"
  "else if(t===lb||t.id==='lbx'||t===lbi){lb.classList.remove('show')}});"
  "document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.accx');if(b){var d=b.closest('details');d.open=false;d.scrollIntoView({block:'nearest'})}});document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.navp a');if(a){var n=document.querySelector('.nav');if(n)n.open=false}});document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('show')});upd();try{var hh=location.hash&&document.querySelector(location.hash);if(hh&&hh.tagName=='DETAILS'){hh.open=true;hh.scrollIntoView()}}catch(x){}"
  "var hc=document.querySelector('.hero .cta'),fb=document.querySelector('.bar');if(hc&&fb&&'IntersectionObserver' in window){"
  "new IntersectionObserver(function(en){var v=en[0].isIntersecting;fb.classList.toggle('hid',v);document.body.classList.toggle('barhid',v)}).observe(hc)}})();</script>")

def img(name, alt, w, h, eager=False):
    attrs = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="img/{name}.webp" alt="{alt}" width="{w}" height="{h}" {attrs}>'

def url_of(slug):
    return SITE_URL + "/" + ("" if slug == "index" else slug + ".html")

# ------------------------------------------------------------------ données structurées
BIZ_ID = SITE_URL + "/#business"
def _price_range():   # calculée depuis PRICES (une seule source de vérité)
    ps = [r[1] for g in PRICES for r in g[4] if r[0] != "#" and r[1]]
    return f"₪{min(ps)}–₪{max(ps)}"

def business(area_names):
    PRICE_RANGE = _price_range()
    days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    spec = []
    for d, slots in HOURS.items():
        for a, b in slots:
            spec.append({"@type":"OpeningHoursSpecification","dayOfWeek":days[d],
                         "opens":f"{a:02d}:00","closes":"23:59" if b == 24 else f"{b:02d}:00"})
    return {"@type":"Locksmith","@id":BIZ_ID,"name":NAME,"telephone":PHONE_INTL,"url":SITE_URL+"/",
            "image":SITE_URL+"/img/og.jpg","founder":{"@type":"Person","name":"רפי","image":SITE_URL+"/img/rafi.webp"},"logo":SITE_URL+"/img/logo.png",
            "address":{"@type":"PostalAddress","addressRegion":REGION,"addressCountry":"IL"},
            "areaServed":[{"@type":"City","name":n} for n in area_names],
            "openingHoursSpecification":spec,
            "priceRange":PRICE_RANGE,"sameAs":([REVIEW_URL.rsplit("/review",1)[0]] if REVIEW_URL else []) + ([MIDRAG_URL] if MIDRAG_URL else []),"contactPoint":{"@type":"ContactPoint","telephone":PHONE_INTL,"contactType":"customer service","availableLanguage":["he"]}}

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

def nav_menu(body):   # menu classique (☰) : renvoie aux sections de la page si elles existent, sinon à l'accueil
    h = lambda a: ("" if f'id="{a}"' in body else "index.html") + "#" + a
    sv = "".join(f'<li><a href="{s}.html"><img src="img/{im}.webp" alt="" width="44" height="44" loading="lazy">{n}</a></li>' for s, n, im, *_ in SERVICES)
    gd = "".join(f'<li><a href="{s}.html"><img src="img/{im}.webp" alt="" width="44" height="44" loading="lazy">{t}</a></li>' for s, t, im, *_ in GUIDES)
    return (f'<details class="nav"><summary aria-label="תפריט"><i></i><i></i><i></i></summary><div class="navp">'
            f'<a class="nbig" href="{h("prix")}">{ic("tag")}מחירים – כל השירותים</a>'
            f'<a class="nbig" href="{h("faq")}">{ic("chat")}שאלות נפוצות ושעות</a>'
            f'<a class="nbig" href="{h("areas")}">{ic("pin")}אזורי שירות</a>'
            f'<p>שירותים</p><ul>{sv}</ul><p>מדריכים</p><ul>{gd}</ul>{cta()}</div></details>')

CSS_V = __import__("hashlib").sha1(CSS.encode()).hexdigest()[:8]
def page(slug, title, desc, body, graph, og_img="og"):
    url = url_of(slug)
    gsc = f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">' if GSC_VERIFICATION and slug == "index" else ""
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><meta name="theme-color" content="#1A56DB">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:locale" content="he_IL"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}/img/{og_img}.jpg"><meta property="og:site_name" content="{NAME}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="32x32"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="img/logo.png">
<link rel="preload" href="fonts/rubik-hebrew.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css?v={CSS_V}">{gsc}{ld(graph)}</head><body>
<header class="hd"><div class="wrap"><a class="logo" href="index.html"><span class="mk">{LOGO_SVG}</span><span>רפי <em>המנעולן</em></span></a><a class="pill" href="tel:{PHONE_INTL}">{ic("phone")}<span>{PHONE}</span></a>{nav_menu(body)}</div></header>
<main>{body}</main>
<footer><div class="wrap"><span><b>{NAME}</b> · מנעולן בכל אזור {REGION}</span><span><a href="tel:{PHONE_INTL}">{PHONE}</a> · <a href="{WA}">וואטסאפ</a> · <a href="rafi-hamanulan.vcf" download>שמרו את המספר</a> · <a href="prices.html">מחירון</a> · <a href="privacy.html">פרטיות</a></span></div></footer>
<nav class="bar" aria-label="יצירת קשר"><a class="btn btn-call" href="tel:{PHONE_INTL}">{ic("phone")}התקשרו</a><a class="btn btn-wa" href="{WA_LINK}">{WA_SVG}וואטסאפ</a></nav>
{JS}{UI_JS}{gads_js()}</body></html>'''

def cta():
    return f'<div class="cta"><a class="btn btn-call" href="tel:{PHONE_INTL}">{ic("phone")}התקשרו</a><a class="btn btn-wa" href="{WA_LINK}">{WA_SVG}וואטסאפ</a></div>'

def hero(h1, sub, photo="hero", alt="רפי המנעולן מחזיק מנעול רב-בריח", crumb=""):
    return f'''<section class="hero"><div class="wrap">
<div class="hero-txt">{crumb}<span class="status"><span class="dot"></span><span class="t">זמין 24 שעות בימים א׳–ה׳</span></span><h1>{h1}</h1><p class="sub">{sub}</p>{cta()}</div>
<div class="pro"><img src="img/rafi.webp" alt="רפי – המנעולן" width="480" height="480" fetchpriority="high"><div class="who"><b>רפי</b><small>מגיע אליכם בעצמו</small></div><div class="eta-badge">{ic("moped")}<div><b>~{ETA_MIN} דק׳</b><small>בקטנוע</small></div></div></div>
<ul class="trust"><li>{ic("shekel")}<b>מחיר ברור</b><small>לפני העבודה</small></li><li>{ic("unlock")}<b>פתיחה בלי נזק</b><small>ברוב המקרים</small></li><li>{ic("hand")}<b>ישירות מול רפי</b><small>בלי מוקד</small></li></ul>
</div></section>'''

# Galerie : photos réelles de Rafi (img/g1..g6.webp). Pour en ajouter : déposer gN.webp (600x600) et ajouter une ligne.
GALLERY = [("g1","מנעול רב-בריח בדלת פלדלת"),("g2","ידית וצילינדר בדלת כניסה"),("g3","מנעול ישן בדלת עץ"),
           ("g4","מנעול רב-בריח בדלת לבנה"),("g5","מנעול בדלת פנים"),("g6","מנעול בדלת זכוכית")]
def gallery_sec():
    g = "".join(f'<li>{img(n, a, 600, 600)}</li>' for n, a in GALLERY)
    return f'<section class="sec"><div class="wrap"><h2>מהעבודה בשטח</h2><ul class="gal">{g}</ul></div></section>'


def area_sec(title="אזורי שירות", current=None):
    chips = "".join(f'<li><a href="{s}.html">מנעולן {b}</a></li>' for s, n, b, _ in CITIES if s != current)
    return f'<section class="sec" id="areas"><div class="wrap"><h2>{title}<small>מגיע אליכם – מקיסריה ועד רמת השרון.</small></h2><ul class="chips">{chips}</ul></div></section>'

def faq_sec(faq):
    q = "".join(f'<details><summary>{a}</summary><p>{b}</p></details>' for a, b in faq)
    hrs = "".join(f'<div><b>{d}</b><span>{h}</span></div>' for d, h in HOURS_DISPLAY)
    return (f'<section class="sec alt" id="faq"><div class="wrap two"><div><h2>שאלות נפוצות</h2><div class="faq">{q}</div></div>'
            f'<div><h2>שעות זמינות</h2><div class="hours">{hrs}</div><p class="note">בשבת סגור. מחוץ לשעות אפשר להשאיר הודעה בוואטסאפ.</p></div></div></section>')

def band(h="ננעלתם בחוץ?", p="מתקשרים, ואני בדרך."):
    rev = f'<p class="note"><a href="{REVIEW_URL}">עבדתי אצלכם? אשמח שתשאירו ביקורת בגוגל</a></p>' if REVIEW_URL else ""
    mid = f'<p class="note"><a href="{MIDRAG_URL.replace("&", "&amp;")}" rel="noopener" target="_blank">ההמלצות עליי במדרג</a></p>' if MIDRAG_URL else ""
    save = '<p class="note"><a href="rafi-hamanulan.vcf" download>שמרו את המספר באנשי הקשר – למקרה חירום</a></p>'
    return f'<section class="band"><div class="wrap"><h2>{h}</h2><p>{p}</p>{cta()}{save}{mid}{rev}</div></section>'

def crumb_html(label):
    return f'<p class="crumb"><a href="index.html">ראשי</a> / {label}</p>'


# ------------------------------------------------------------------ guides (articles utiles, longue traîne SEO)
# Contenu factuel et général. Pas de prix, pas de promesse non vérifiée.
GUIDES = [
("guide-locked-out", "ננעלתם מחוץ לבית? מה עושים עכשיו", "g1",
 "ננעלתם בחוץ? מתי להתקשר ל-100 או ל-102, מה לא כדאי לנסות לבד, ואיך מנעולן פותח את הדלת בלי לשבור אותה.",
 [("קודם כול: יש מישהו בסכנה?", ["אם ילד קטן, אדם שזקוק לעזרה או חיית מחמד נשארו בפנים, או שהגז או הכיריים דולקים – התקשרו מיד למשטרה (100) או לכבאות והצלה (102). זה קודם לכל דבר אחר."]),
  ("מה לא לעשות", ["לא לטפס דרך חלון או מרפסת – זה מסוכן, גם בקומה נמוכה.", "לא לנסות לפתוח עם מברג, כרטיס או סיכה – ברוב הדלתות זה לא עובד, ועלול להזיק לצילינדר ולהעלות את מחיר התיקון.", "לא לשבור את הדלת או את המשקוף."]),
  ("מה כן לעשות", ["בדקו אם למישהו אחר יש מפתח: בן משפחה, שכן, בעל הדירה.", "התקשרו למנעולן וספרו לו איזו דלת יש לכם (פלדלת, דלת עץ) ומה קרה (נטרקה, מפתח נשבר, מפתח נשאר בפנים).", "הכינו תעודה מזהה או מסמך עם הכתובת – מנעולן אחראי יבקש לוודא שאתם גרים במקום לפני שהוא פותח."]),
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
  ("מה כן לעשות", ["שמרו את החלק השני של המפתח – הוא עוזר לזהות את הדגם ולשכפל מפתח חדש.", "אם הדלת פתוחה, השאירו אותה פתוחה עד שהבעיה נפתרת.", "התקשרו למנעולן וספרו לו אם הדלת נעולה או פתוחה."]),
  ("מה אפשר לעשות", ["במקרים רבים אפשר לחלץ את החלק השבור בלי להחליף את הצילינדר.", "אם הצילינדר נפגע או ישן, כדאי להחליף אותו באותו ביקור."])]),
("guide-after-burglary", "מה עושים אחרי פריצה לדירה?", "security",
 "מה עושים שלב אחרי שלב: משטרה, תיעוד לביטוח, החלפת צילינדר ושדרוג המיגון של הדלת.",
 [("מיד אחרי שגיליתם", ["אל תיכנסו אם יש חשש שמישהו עדיין בפנים. התקשרו למשטרה (100).", "אל תגעו ואל תסדרו – המשטרה עשויה לבקש לבדוק את המקום."]),
  ("לביטוח", ["צלמו את הדלת, המנעול וכל נזק לפני שמתקנים.", "רשמו מה חסר, ובקשו מהמשטרה את מספר התיק או את אישור הגשת התלונה."]),
  ("לאבטח את הדלת מחדש", ["החליפו צילינדר כמה שיותר מהר – ייתכן שלפורץ יש דרך לפתוח את הקיים.", "בדקו שהמנעול והמשקוף לא נפגעו, ושהדלת ננעלת עד הסוף.", "שקלו שדרוג: צילינדר מוגן, מנעול עזר או חיזוק לדלת."]),
  ("אני יכול לעזור", ["אני מגיע, מחליף צילינדר ובודק את הדלת והמנעולים. המחיר נאמר לפני שמתחילים."])]),
]

GUIDES += [
("guide-keys-inside", "הדלת נטרקה והמפתח בפנים – מה עושים?", "g4",
 "הדלת נטרקה כשהמפתח נשאר בפנים? מה אפשר לבדוק לבד, מה לא לנסות, ואיך פותחים בלי נזק.",
 [("קודם כול", ["אם בפנים נשאר ילד, אדם שזקוק לעזרה, חיה או משהו דולק על הכיריים – התקשרו מיד למשטרה (100) או לכבאות והצלה (102)."]),
  ("מה לבדוק לבד", ["האם יש למישהו עותק של המפתח – בן משפחה, שכן, בעל הדירה.", "האם יש דלת נוספת או מרפסת שאפשר להגיע אליה בבטחה מהקרקע – בלי לטפס."]),
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
 [("מה לבדוק קודם", ["סוללות – בהרבה כספות אלקטרוניות, כשהסוללה חלשה הכספת לא נפתחת גם עם הקוד הנכון.", "מפתח חירום – להרבה כספות יש מפתח שפותח גם בלי קוד. בדקו אם הוא אצלכם.", "החוברת של הכספת – לפעמים יש בה קוד מפעל או הוראות איפוס."]),
  ("מה לא לעשות", ["לא לנסות קודים שוב ושוב – חלק מהכספות ננעלות לזמן ארוך אחרי כמה ניסיונות.", "לא לנסות לפתוח בכוח – זה עלול להרוס את הכספת ואת מה שבתוכה."]),
  ("פתיחת כספת", ["מנעולן יכול לפתוח את הכספת ולהגדיר אחר כך קוד חדש. תתבקשו להראות שהכספת שלכם."])]),
]

# Sections ajoutées le 19 nov. 2026 (audit SEO : guides trop courts). (position dans la liste d'origine, section) ; 99 = à la fin.
GUIDE_EXTRA = {
"guide-locked-out": [
 (99, ("כמה זמן זה לוקח?", ["דלת שרק נטרקה ולא ננעלה בבריחים נפתחת בדרך כלל מהר, ולרוב בלי שום נזק.", "דלת שננעלה עם המפתח דורשת יותר עבודה, ולפעמים צריך להחליף צילינדר. כשאתם מתקשרים, ספרו אם נעלתם במפתח או שהדלת רק נטרקה – כך אפשר להגיד לכם מראש למה לצפות."])),
 (99, ("איך בוחרים מנעולן אמין", ["בקשו מחיר כבר בטלפון, ושאלו מה הוא כולל: הגעה, עבודה וחלקים.", "מנעולן אמין יבקש לוודא שאתם גרים בבית לפני שהוא פותח – זה לטובתכם.", "היזהרו ממחיר נמוך במיוחד בטלפון שמתנפח כשהמנעולן כבר ליד הדלת.", "עדיף לדבר ישירות עם המנעולן שיגיע, ולא עם מוקד שמעביר את הקריאה הלאה."])),
 (99, ("איך לא להינעל שוב", ["השאירו מפתח רזרבי אצל מישהו קרוב שאתם סומכים עליו.", "אל תחביאו מפתח מתחת לשטיח או בעציץ ליד הדלת – זה המקום הראשון שפורץ בודק.", "שמרו את המספר של מנעולן באנשי הקשר, כדי לא לחפש ברגע של לחץ."]))],
"guide-cylinder": [
 (3, ("איך יודעים איזה צילינדר יש לכם", ["שם היצרן מופיע בדרך כלל על חזית הצילינדר או על המפתח.", "בפלדלתות נפוץ צילינדר בפרופיל אירופאי – אפשר להחליף אותו בלי להחליף את המנעול או את הדלת.", "האורך חשוב: הצילינדר צריך להתאים לעובי הדלת. צילינדר שבולט החוצה מהדלת קל יותר לשבירה."])),
 (3, ("כרטיס שכפול", ["לצילינדרים מוגנים רבים יש כרטיס שכפול. בלי הכרטיס אי אפשר לשכפל מפתח, כך שמי שהחזיק את המפתח לרגע לא יכול להעתיק אותו.", "שמרו את הכרטיס במקום בטוח – לא יחד עם המפתחות."])),
 (3, ("תחזוקה פשוטה", ["פעם בשנה בערך כדאי לשמן את הצילינדר בתרסיס ייעודי למנעולים – לא בשמן מטבח.", "אם המפתח מתחיל להיתקע, אל תחכו שהוא יישבר בפנים."]))],
"guide-broken-key": [
 (0, ("למה מפתח נשבר?", ["מפתח ישן ושחוק, שנחלש עם השנים.", "צילינדר תקוע או מלוכלך, שמכריח לסובב בכוח.", "מפתח משוכפל שלא שוכפל במדויק.", "סיבוב המפתח כשהדלת לא סגורה עד הסוף, והבריחים לוחצים על המשקוף."])),
 (99, ("איך מונעים את הפעם הבאה", ["אם המפתח נכנס או מסתובב בקושי – לטפל בזה מיד, לפני שהוא נשבר.", "כשהמפתח מתחיל להישחק, לשכפל מפתח חדש מהמפתח המקורי – לא מעותק של עותק.", "לא לתלות צרור כבד על המפתח כשהוא בתוך המנעול – המשקל מעקם אותו עם הזמן."]))],
"guide-after-burglary": [
 (3, ("איך פורצים נכנסים בדרך כלל", ["דרך דלת עם צילינדר ישן ופשוט, שאפשר לשבור או לפתוח בקלות.", "דרך דלת שרק נטרקה ולא ננעלה בבריחים.", "דרך חלון או מרפסת, בעיקר בקומות נמוכות ובבתים פרטיים."])),
 (3, ("רשימת בדיקה לדלת", ["הצילינדר הוחלף, ויש לכם את כל המפתחות החדשים.", "המשקוף והצירים שלמים, והדלת לא שקעה.", "כל הבריחים נכנסים עד הסוף כשנועלים.", "אם יש מצלמה או אזעקה – בדקו שהן עובדות."]))],
"guide-keys-inside": [
 (1, ("למה זה קורה?", ["רוב הדלתות ננעלות בלשונית ברגע שהן נטרקות – רוח או טריקה חזקה מספיקות.", "יציאה של רגע – לזרוק זבל, לאסוף חבילה – בלי לקחת את המפתחות."])),
 (99, ("מפתח תקוע בצד הפנימי", ["אם המפתח נשאר בתוך הצילינדר מבפנים, בהרבה צילינדרים אי אפשר להכניס מפתח מבחוץ – גם אם יש לכם עותק.", "יש צילינדרים עם פונקציית חירום, שמאפשרים לפתוח מבחוץ גם כשמפתח נמצא בצד הפנימי. כדאי לשקול כזה כשמחליפים צילינדר."])),
 (99, ("איך מונעים את הפעם הבאה", ["השאירו עותק של המפתח אצל שכן או בן משפחה.", "התרגלו לנעול מבחוץ עם המפתח – כך המפתח תמיד ביד.", "אל תשאירו את המפתח תקוע בצילינדר מבפנים."]))],
"guide-stuck-lock": [
 (0, ("איך עובד מנעול רב-בריח", ["בפלדלת יש מנגנון רב-בריח: סיבוב אחד של המפתח מזיז כמה בריחים בבת אחת – לצד, ולפעמים גם למעלה ולמטה.", "כדי שהבריחים ייכנסו חלק, הדלת צריכה להיות מיושרת מול המשקוף. כשהיא שוקעת אפילו קצת, הבריחים מתחילים להיתקע."])),
 (3, ("מתי לקרוא למנעולן ולא לחכות", ["כשהמפתח מסתובב רק עם הרבה כוח.", "כשהבריחים לא יוצאים עד הסוף – הדלת לא באמת נעולה.", "כשמשהו בתוך המנגנון מקרקש או נשמע שבור."])),
 (99, ("תחזוקה שמונעת תקיעות", ["לשמן את הבריחים ואת הצילינדר בערך פעם בשנה בחומר סיכה ייעודי.", "לשים לב אם הדלת מתחילה לגרד ברצפה או במשקוף – זה סימן שהצירים צריכים כיוון.", "ליד הים כדאי לבדוק לעיתים קרובות יותר, כי המלח מאיץ חלודה."]))],
"guide-safe-code": [
 (0, ("איזו כספת יש לכם?", ["כספת אלקטרונית עם לוח מקשים וסוללות – הנפוצה בבתים.", "כספת מכנית עם חוגה מסתובבת או עם מפתח בלבד.", "כספת קטנה לבית או למלון, בדרך כלל עם מפתח חירום."])),
 (99, ("אחרי שהכספת נפתחה", ["החליפו סוללות והגדירו קוד חדש שתזכרו – אבל לא תאריך לידה או 1234.", "רשמו את הקוד במקום בטוח מחוץ לכספת.", "שמרו את מפתח החירום במקום אחר – לא בתוך הכספת עצמה."]))],
}
def _merge_sections(sections, extra):
    out, n = list(sections), len(sections)
    for pos, sec in reversed(sorted(((min(p, n), s) for p, s in extra), key=lambda x: x[0])):
        out.insert(pos, sec)
    return out
GUIDES = [(sl, t, im, d, _merge_sections(sec, GUIDE_EXTRA.get(sl, []))) for sl, t, im, d, sec in GUIDES]
GUIDES_PUBLISHED = "2026-11-18"
# Page service liée à chaque guide (lien dans le texte)
GUIDE_SERVICE = {"guide-locked-out":"door-opening","guide-keys-inside":"door-opening","guide-cylinder":"cylinder","guide-broken-key":"lock-repair",
                 "guide-stuck-lock":"lock-repair","guide-after-burglary":"security","guide-safe-code":"safe"}
HE_MONTHS = ["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"]
REGION_B = "ב" + (REGION[1:] if REGION.startswith("ה") else REGION)  # « בשרון » (ב + השרון)
def _fit160(*variants):  # meta description : première variante de 160 caractères ou moins (Google coupe au-delà)
    return next((v for v in variants if len(v) <= 160), variants[-1])
def he_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} ב{HE_MONTHS[m-1]} {y}"

# Illustrations dessinées pour chaque guide (sources _build/ill/*.svg, rendu : node _build/ill/render.js) au lieu des photos réutilisées
GUIDES = [(sl, t, "ill-" + sl[len("guide-"):], d, sec) for sl, t, _im, d, sec in GUIDES]

def guide_body(slug, title, im, desc, sections):
    secs = "".join(f'<h2>{h}</h2>' + ("<ul>" + "".join(f"<li>{p}</li>" for p in ps) + "</ul>" if len(ps) > 1 else f"<p>{ps[0]}</p>") for h, ps in sections)
    others = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t, *_ in GUIDES if s != slug)
    svc = GUIDE_SERVICE.get(slug)
    rel = (f'<p class="rel">השירות הקשור: <a href="{svc}.html">{next(n for s, n, *_ in SERVICES if s == svc)}</a> – מחירים, מה כולל השירות ושאלות נפוצות.</p>'
           if svc else "")
    return (f'<article class="sec"><div class="wrap art">{crumb_html("מדריכים")}<h1>{title}</h1>'
            f'<p class="meta">מאת רפי המנעולן · עודכן ב-<time datetime="{TODAY}">{he_date(TODAY)}</time></p><p class="intro">{desc}</p>'
            f'{img(im, title, 800, 600, eager=True)}{secs}{rel}'
            f'<div class="cta-box"><b>צריכים מנעולן עכשיו?</b>{cta()}</div>'
            f'<h2>מדריכים נוספים</h2><ul class="links">{others}</ul></div></article>' + area_sec() + band())


# ------------------------------------------------------------------ MÉTHODE DE PRIX (fournie par Raphaël le 7 nov. 2026)
# (id, titre, image, note, [(libellé, prix ₪ ou None, texte du prix)], pages de service où afficher le bloc)
PRICES = [
# Rangée : (libellé, prix ₪, texte de prix ou None, vignette[, ancien prix barré]) ; ("#", "titre") = sous-titre
("fp", "פריצת דלתות", "p-open", "פריצה + צילינדר חדש לבחירתכם, כולל התקנה. המחיר תלוי בצילינדר.",
 [("#", "דלת טרוקה"),
  ("פתיחת דלת טרוקה (נטרקה ולא ננעלה)", 200, None, "t-latch"),
  ("#", "פריצה + החלפת צילינדר בפלדלת"),
  ("מגנום · 5 מפתחות", 630, None, "t-magnum320"),
  ("מגנום · 5 מפתחות + כרטיס שכפול", 660, None, "t-magnum360"),
  ("רב-בריח · 5 מפתחות + כרטיס שכפול", 690, None, "t-rav390"),
  ("KEYLOCX של רב-בריח", 800, None, "t-keylocx"),
  ("לוקסיס של רב-בריח", 900, None, "t-loksis"),
  ("מולטילוק MTL600", 900, None, "t-mtl600"),
  ("מולטילוק MTL800", 1070, None, "t-mtl800")], ["door-opening", "cylinder"]),
("cyl", "החלפת צילינדר בפלדלת", "p-cyl", "המחיר כולל את הצילינדר וההתקנה. אפשר גם עם כפתור פנימי במקום מפתח – באותו מחיר.",
 [("#", "צילינדרים איכותיים"),
  ("רב-בריח · 5 מפתחות + כרטיס שכפול", 390, None, "t-rav390"),
  ("מגנום · 5 מפתחות + כרטיס שכפול", 360, None, "t-magnum360"),
  ("מגנום · 5 מפתחות", 330, None, "t-magnum320"),
  ("#", "צילינדרים ברמת אבטחה גבוהה"),
  ("KEYLOCX של רב-בריח", 500, None, "t-keylocx"), ("לוקסיס של רב-בריח", 600, None, "t-loksis"),
  ("מולטילוק MTL600", 600, None, "t-mtl600"), ("מולטילוק MTL800", 770, None, "t-mtl800")], ["cylinder", "security"]),
("mech", "פלדלת – מנגנונים ופרזול", "p-steel", "",
 [("החלפת מנגנון רב-בריח", 700, None, "t-ravmech"), ("החלפת מנגנון שריונית חוסם", 800, None, "t-shiryonit"),
  ("סט פלטות קומפלט לפלדלת – ניקל, שחור או מעוגל", 330, None, "t-plates"), ("מחזיר דלת", 450, None, None), ("התקנת מנעול כספת / מנעול נוסף לפלדלת", 550, None, "t-extralock")], ["lock-repair", "security"]),
("int", "דלתות פנים ושערי כניסה", "p-intmech", "",
 [("#", "דלתות פנים – החלפה"),
  ("סט ידיות לדלת פשוטה / דלת פנים", 150, None, "t-inthandles"),
  ("החלפת צילינדר פשוט + 3 מפתחות", 240, None, "t-simplecyl"), ("החלפת מנגנון", 250, None, "t-intlock.svg"),
  ("החלפת מנגנון + צילינדר", 430, None, "t-intdoor", 500),
  ("#", "דלתות פנים – פריצה + החלפה"),
  ("פריצה + החלפת מנגנון (ללא צילינדר)", 300, None, "t-intmech", 350), ("פריצה + החלפת מנגנון + צילינדר", 470, None, "t-intdoor", 550),
  ("#", "שער כניסה חיצוני – החלפה"),
  ("החלפת מנגנון שער כניסה", 250, None, "p-entrance"),
  ("החלפת מנגנון + צילינדר בשער כניסה", 430, None, "p-entrance", 500),
  ("#", "שער כניסה חיצוני – פריצה + החלפה"),
  ("פריצה + החלפת מנגנון + צילינדר בשער כניסה", 470, None, "p-entrance", 550)], ["lock-repair", "door-opening"]),
("safe", "כספות ותיבות דואר", "safe", "בכספות גדולות ומיוחדות מתווספים 100 ₪ לכל שכבת פלדה – זה נקבע רק במקום, בזמן הפריצה.",
 [("#", "כספות"),
  ("התקנת כספת סטנדרטית", 350, None, "t-safe"), ("פריצת כספת סטנדרטית", 300, None, "t-safe"),
  ("#", "תיבות דואר"),
  ("פריצה והחלפת מנעול לתיבת דואר", 200, None, "t-mail"), ("החלפת מנעול זיז ישן בתיבות דואר מרוכזות", 300, None, "t-mailbank")], ["safe", "lock-repair"]),
("rep", "תיקונים", "p-repair", "",
 [("תיקון מנעולים ודלתות", None, "החל מ-200 ₪, לפי העבודה", None)], ["lock-repair"]),
]
import re as _re
def _pkey(r):
    l, p, t = r[0], r[1], r[2]
    if p: return p
    m = _re.search(r"(\d+)", t or ""); return int(m.group(1)) if m else 0
def _sort_rows(rows):   # prix en ordre croissant à l'intérieur de chaque sous-titre
    out, seg = [], []
    for r in rows:
        if r[0] == "#": out += sorted(seg, key=_pkey) + [r]; seg = []
        else: seg.append(r)
    return out + sorted(seg, key=_pkey)
PRICES = [(g[0], g[1], g[2], g[3], _sort_rows(g[4]), g[5]) for g in PRICES]

PRICE_NOTES = [f"תוספת לפי שעת הקריאה: {NIGHT_TXT}. בין 08:00 ל-20:00 – בלי תוספת. אותו דבר בכל ימות השבוע, כולל שישי ומוצאי שבת.", "כל השירותים זמינים גם לעסקים.",
               "המחיר הסופי נאמר ומאושר לפני שמתחילים לעבוד."]

def price_txt(p, t): return t if t else f"{p} ₪"

def thumb(key, alt):
    if key:
        return f'<img class="pth" src="img/{key if key.endswith(".svg") else key + ".webp"}" alt="{alt}" width="240" height="240" loading="lazy" decoding="async">'
    return f'<i class="pth ph">{ic("key")}</i>'

def _h2(h): return "00" if h == 24 else f"{h:02d}"
NIGHT_BANNER = ('<div class="nightb"><div class="nt">🌙 <b>תוספת לילה</b> – מתווספת למחיר לפי שעת הקריאה</div><div class="nrow">'
    + "".join(f'<span><bdi dir="ltr">{_hh(a)}–{_hh(b)}</bdi><b><bdi dir="ltr">+{v} ₪</bdi></b></span>' for a, b, v in NIGHT_TIERS)
    + '</div><small>מ-08:00 עד 20:00 – בלי תוספת</small></div>')

def _from(rows):
    ps = [_pkey(r) for r in rows if r[0] != "#"]
    return min(ps) if ps else 0

def acc_block(g, open_=False):   # une catégorie = un menu déroulant (photo + titre + « dès X ₪ »)
    gid, title, im, note, rows, _ = g
    def row(r):
        if r[0] == "#": return f'<li class="psub">{r[1]}</li>'
        l, p, t, th = r[:4]; was = r[4] if len(r) > 4 else None
        old = f'<s>{was} ₪</s>' if was else ""
        return (f'<li><label><input type="checkbox" class="pick" data-l="{title} – {l}" data-p="{p or ''}" data-t="{price_txt(p, t)}">'
                f'{thumb(th, l)}<span>{l}</span><b{' class="long"' if t else ''}>{old}{price_txt(p, t)}</b></label></li>')
    n = f'<p class="pnote">{note}</p>' if note else ""
    return (f'<details class="acc" id="p-{gid}"{" open" if open_ else ""}><summary><img src="img/{im}.webp" alt="{title}" width="64" height="64" loading="lazy" decoding="async">'
            f'<span><b>{title}</b><small>החל מ-{_from(rows)} ₪</small></span><i aria-hidden="true"></i></summary>'
            f'<ul class="prows">{"".join(row(r) for r in rows)}</ul>{n}<button type="button" class="accx">סגירה ▲</button></details>')

def acc_link(g):   # pages villes : même carte que le menu fermé, mais renvoie au מחירון (évite 34 copies du même texte)
    gid, title, im, _, rows, _ = g
    return (f'<a class="acc" href="prices.html#p-{gid}"><span class="accl"><img src="img/{im}.webp" alt="{title}" width="64" height="64" loading="lazy" decoding="async">'
            f'<span><b>{title}</b><small>החל מ-{_from(rows)} ₪</small></span><i aria-hidden="true"></i></span></a>')

def prices_all(title="השירותים והמחירים", small="לוחצים על שירות כדי לראות את כל המחירים, מסמנים ושולחים לי בוואטסאפ.", open_ids=(), h="h2", alt=False, link=False):
    notes = "".join(f"<li>{x}</li>" for x in PRICE_NOTES[1:])
    return (f'<section class="sec{" alt" if alt else ""}" id="prix"><div class="wrap"><{h} class="sh">{title}<small>{small}</small></{h}>{NIGHT_BANNER}'
            f'<div class="accs">{"".join(acc_link(g) if link else acc_block(g, g[0] in open_ids) for g in PRICES)}</div><ul class="pnotes">{notes}</ul></div></section>')

def more_sec():   # liens internes (SEO) vers les pages de service et les guides, avec vignettes
    sv = "".join(f'<li><a href="{s}.html"><img src="img/{im}.webp" alt="" width="120" height="90" loading="lazy" decoding="async"><span>{n}</span></a></li>' for s, n, im, *_ in SERVICES)
    gd = "".join(f'<li><a href="{s}.html"><img src="img/{im}.webp" alt="" width="64" height="64" loading="lazy" decoding="async"><span>{t}</span>{ic("arrow")}</a></li>' for s, t, im, *_ in GUIDES)
    return (f'<section class="sec" id="info"><div class="wrap"><h2>שירותים<small>כל מה שצריך לדעת על כל שירות.</small></h2><ul class="svc">{sv}</ul>'
            f'<h2 style="margin-top:40px">מדריכים קצרים<small>מה עושים כשזה קורה.</small></h2><ul class="gds">{gd}</ul></div></section>')

# ------------------------------------------------------------------ génération
ALL = [n for _, n, _, _ in CITIES]
pages = []  # (slug, html)

# Accueil
home_faq = FAQ + [("לאילו אזורים אתה מגיע?", ", ".join(c[1] for c in CITIES if c[0] != "moshavim") + " והמושבים שבדרך.")]
body = (hero("מנעולן קרוב אליכם", f"פריצת דלתות, צילינדרים, מנעולים וכספות בכל אזור {REGION}. אצלכם תוך כ-{ETA_MIN} דקות.")
        + prices_all() + gallery_sec() + faq_sec(home_faq) + area_sec() + more_sec() + band())
pages.append(("index", page("index",
    f"מנעולן בשרון – כפר סבא, רעננה, נתניה, הרצליה | {NAME} – {PHONE}",
    f"מנעולן {REGION_B}, מקיסריה ועד רמת השרון: פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות. הגעה בקטנוע תוך כ-{ETA_MIN} דקות, מחיר ברור לפני העבודה. {PHONE}",
    body, [business(ALL), {"@type":"WebSite","@id":SITE_URL+"/#website","url":SITE_URL+"/","name":NAME,"inLanguage":"he"}, faq_ld(home_faq)])))

# Pages villes
for s, n, b, hood in CITIES:
    faq = [(f"תוך כמה זמן מגיע מנעולן {b}?", f"בדרך כלל תוך כ-{ETA_MIN} דקות. אני מגיע בקטנוע, כך שגם בשעות העומס אני מגיע ל{n} מהר."),
           (f"לאילו אזורים {b} אתה מגיע?", f"{hood}."),
           (f"מה כדאי לדעת על מנעולים {b}?", CITY_TEXT[s][1])] + FAQ[1:]
    intro = (f"צריכים מנעולן {b}? רפי המנעולן מגיע בקטנוע לכל מקום {b}" + ("." if hood.startswith("כל") else f": {hood}.") + " "
             f"פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות – לבית ולעסק, עם מחיר ברור לפני העבודה.")
    body = (hero(f"מנעולן {b}", f"פורץ דלתות ומנעולים {b}. אצלכם תוך כ-{ETA_MIN} דקות.", crumb=crumb_html(f"מנעולן {b}"))
            + f'<section class="sec"><div class="wrap"><h2>מנעולן {b}</h2><p>{CITY_TEXT[s][0]} {intro}</p>{nearby_html(s)}</div></section>'
            + prices_all(f"שירותי מנעולן {b}", "לוחצים על שירות כדי לראות את כל המחירים, מסמנים ושולחים לי בוואטסאפ.", link=True)
            + faq_sec(faq) + area_sec("עוד אזורים", current=s) + band())
    pages.append((s, page(s,
        f"מנעולן {b} – הגעה תוך כ-{ETA_MIN} דק׳ | {NAME}",
        f"מנעולן {b}: פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות. {NAME} מגיע בקטנוע תוך כ-{ETA_MIN} דקות. מחיר ברור לפני העבודה. {PHONE}",
        body, [business([n]), crumbs_ld([("ראשי", SITE_URL+"/"), (f"מנעולן {b}", url_of(s))]), faq_ld(faq)])))

# Pages services
for s, n, im, t, items, kw in SERVICES:
    inc = "".join(f'<li>{ic("check")}<span>{x}</span></li>' for x in items)
    faq = FAQ[1:3] + FAQ[:1] + FAQ[3:]
    body = (hero(f"{n} – מגיע אליכם", f"{t} אצלכם תוך כ-{ETA_MIN} דקות.", photo=im, alt=n, crumb=crumb_html(n))
            + prices_all("מחירים", "סמנו מה אתם צריכים ושלחו לי בוואטסאפ. שאר השירותים – באותו עמוד, למטה.", [g[0] for g in PRICES if s in g[5]][:1])
            + f'<section class="sec alt"><div class="wrap"><h2>מה כולל השירות<small>{kw} – המחיר נקבע ומאושר מראש.</small></h2><ul class="incl">{inc}</ul></div></section>'
            + faq_sec(faq) + area_sec() + more_sec() + band())
    svc = {"@type":"Service","name":n,"serviceType":n,"provider":{"@id":BIZ_ID},"areaServed":[{"@type":"City","name":c} for c in ALL],"description":t}
    pages.append((s, page(s,
        f"{n} בשרון – כפר סבא, רעננה, נתניה, הרצליה | {NAME}",
        _fit160(f"{n} בכל אזור {REGION}, מקיסריה ועד רמת השרון – {t} {kw}. הגעה בקטנוע תוך כ-{ETA_MIN} דקות, מחיר ברור לפני העבודה.",
                f"{n} {REGION_B}, מקיסריה ועד רמת השרון – {t} הגעה בקטנוע תוך כ-{ETA_MIN} דקות, מחיר ברור לפני העבודה.",
                f"{n} {REGION_B} – {t} הגעה בקטנוע תוך כ-{ETA_MIN} דקות, מחיר ברור לפני העבודה."),
        body, [business(ALL), svc, crumbs_ld([("ראשי", SITE_URL+"/"), (n, url_of(s))]), faq_ld(faq)], og_img="og")))

for slug, title, im, desc, sections in GUIDES:
    art = {"@type":"Article","headline":title,"description":desc,"inLanguage":"he","image":f"{SITE_URL}/img/{im}.webp",
           "author":{"@type":"Person","name":"רפי","url":SITE_URL+"/","worksFor":{"@id":BIZ_ID}},"publisher":{"@id":BIZ_ID},
           "mainEntityOfPage":url_of(slug),"datePublished":GUIDES_PUBLISHED,"dateModified":TODAY}
    pages.append((slug, page(slug, f"{title} | {NAME}", desc, guide_body(slug, title, im, desc, sections),
        [business(ALL), art, crumbs_ld([("ראשי", SITE_URL+"/"), (title, url_of(slug))])])))

with open(f"{OUT}/style.css", "w") as f: f.write(CSS)
for slug, html in pages:
    with open(f"{OUT}/{slug}.html", "w") as f: f.write(html)

NIGHT_CARD = ('<div class="pcard solo" style="margin-top:24px"><div class="pbody"><h2>תוספת לפי שעת הקריאה</h2><ul class="prows">'
    + '<li><label><span>08:00–20:00</span><b>בלי תוספת</b></label></li>'
    + "".join(f'<li><label><span>{_hh(a)}–{_hh(b)}</span><b>+{v} ₪</b></label></li>' for a, b, v in NIGHT_TIERS)
    + f'</ul><p class="pnote">התוספת לא עולה על {NIGHT_MAX} ₪, והיא זהה בכל ימות השבוע – כולל שישי ומוצאי שבת. כשבוחרים שירותים, היא מחושבת אוטומטית לפי השעה.</p></div></div>')
# Page Mehiron (prix fournis par Raphaël)
offers = [{"@type":"Offer","priceCurrency":"ILS","price":p,"itemOffered":{"@type":"Service","name":f"{g[1]} – {l}"}}
          for g in PRICES for r in g[4] if r[0] != "#" and r[1] for l, p in [r[:2]]]
PRICES_BODY = (hero("מחירון מנעולן", "מחירים ברורים, כולל חלקים והתקנה. המחיר הסופי נאמר לפני העבודה.", photo="p-cyl", alt="צילינדרים", crumb=crumb_html("מחירון"))
    + prices_all("כל המחירים", "לוחצים על שירות כדי לפתוח.") + f'<section class="sec" style="padding-top:0"><div class="wrap">{NIGHT_CARD}</div></section>' + area_sec() + band())
pages.append(("prices", page("prices", f"מחירון מנעולן – פריצת דלת, החלפת צילינדר, כספות | {NAME}",
    "מחירון רפי המנעולן: פתיחת דלת טרוקה 200 ₪, פריצה + החלפת צילינדר מ-630 ₪, החלפת צילינדר מ-330 ₪, כספות ומנגנונים. כולל חלקים והתקנה.",
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
                 f'<section class="band"><div class="wrap"><h1>הדף לא נמצא</h1><p>אבל אני כן כאן. <a href="index.html">לדף הראשי</a></p>{cta()}</div></section>',
                 [business(ALL)]).replace('<link rel="canonical" href="' + url_of("404") + '">', '<meta name="robots" content="noindex">'))

with open(f"{OUT}/favicon.svg", "w") as f:
    f.write(LOGO_SVG.replace(' aria-hidden="true"', ""))

with open(f"{OUT}/rafi-hamanulan.vcf", "w", encoding="utf-8") as f:
    f.write("BEGIN:VCARD\r\nVERSION:3.0\r\nN:;" + NAME + ";;;\r\nFN:" + NAME + "\r\nORG:" + NAME + "\r\nTITLE:מנעולן\r\n"
            + "TEL;TYPE=CELL,VOICE:" + PHONE_INTL + "\r\nURL:" + SITE_URL + "/\r\nNOTE:מנעולן – פריצת דלתות, צילינדרים, מנעולים וכספות\r\nEND:VCARD\r\n")
with open(f"{OUT}/{INDEXNOW_KEY}.txt", "w") as f: f.write(INDEXNOW_KEY)

urls = [url_of(s) for s, _ in pages]
with open(f"{OUT}/sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
# llms.txt : fiche en texte simple pour les assistants IA (standard llmstxt.org) — mêmes réglages que le site
_llms = [f"# {NAME}", "", f"> מנעולן עצמאי בכל אזור {REGION}, מקיסריה ועד רמת השרון. מגיע בקטנוע, בדרך כלל תוך כ-{ETA_MIN} דקות. מחיר ברור לפני העבודה.", "",
         f"- טלפון: {PHONE} ({PHONE_INTL})", f"- וואטסאפ: {WA}", f"- אתר: {SITE_URL}/",
         "- שעות: " + "; ".join(f"{d} {h}" for d, h in HOURS_DISPLAY) + ". בשבת סגור.",
         f"- תוספת לילה: {NIGHT_TXT}. בין 08:00 ל-20:00 בלי תוספת.", "", "## שירותים ומחירים (כולל חלקים והתקנה)"]
for g in PRICES:
    _llms.append(f"### {g[1]}")
    _sub = ""
    for r in g[4]:
        if r[0] == "#": _sub = r[1]; continue
        _llms.append(f"- {(_sub + ' – ') if _sub else ''}{r[0]}: {price_txt(r[1], r[2])}")
_llms += ["", "## אזורי שירות", ", ".join(c[1] for c in CITIES), "", "## דפים"]
_llms += [f"- [מחירון]({url_of('prices')})"] + [f"- [{n}]({url_of(sl)})" for sl, n, *_ in SERVICES] + [f"- [{t}]({url_of(sl)})" for sl, t, *_ in GUIDES]
with open(f"{OUT}/llms.txt", "w", encoding="utf-8") as f: f.write("\n".join(_llms) + "\n")

with open(f"{OUT}/robots.txt", "w") as f:
    # Content-Signal (contentsignals.org) : autorise moteurs de recherche, réponses IA et entraînement (le but est d'être trouvé partout)
    f.write(f"User-agent: *\nContent-Signal: search=yes, ai-input=yes, ai-train=yes\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
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
