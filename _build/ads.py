"""Génère la campagne Google Ads (Réseau de Recherche) prête à importer.
Usage : python3 _build/ads.py  -> docs/google-ads/campagne.csv (format Google Ads Editor) + campagne-lisible.md
Mêmes réglages que build.py (villes, services, téléphone, délai) : une seule source de vérité.
La campagne est créée EN PAUSE : rien n'est dépensé avant que Raphaël l'active."""
import os, csv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "_build/build.py"), encoding="utf-8").read().split("# ------------------------------------------------------------------ CSS")[0]
cfg = {"__file__": os.path.join(ROOT, "_build/build.py")}; exec(src, cfg)
SITE, ETA, NAME = cfg["SITE_URL"], cfg["ETA_MIN"], cfg["NAME"]

CAMPAIGN = "רפי המנעולן – חיפוש"
BUDGET_PLACEHOLDER = 50   # ₪/jour – VALEUR D'ATTENTE, à fixer par Raphaël avant d'activer
NEGATIVES = ["קורס", "לימודי", "ללמוד", "עבודה", "דרושים", "משרה", "איך לפתוח", "לבד", "יוטיוב", "סרטון",
             "רכב", "אוטו", "אופנוע", "סיטונאי", "חינם", "מכירה", "יד 2", "טוטוריאל"]

COMMON_H = [f"הגעה תוך כ-{ETA} דק׳", "מחיר ברור לפני העבודה", "פתיחה ללא נזק ככל שניתן", "ישירות מול בעל המקצוע",
            "זמין 24 שעות בימי חול", "הגעה בקטנוע, גם בפקקים", NAME]
COMMON_D = [f"ננעלתם בחוץ? {NAME} מגיע בקטנוע תוך כ-{ETA} דקות. מחיר ברור לפני שמתחילים.",
            "פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות. לבית ולעסק.",
            "מי שעונה לטלפון הוא מי שמגיע אליכם. בלי מוקד ובלי הפתעות במחיר.",
            "זמין 24 שעות בימים א׳–ה׳, בשישי עד 16:00 ובמוצאי שבת עד חצות."]

def group(name, url, keywords, own_h, path1="מנעולן", path2=""):
    return {"name": name, "url": url, "kw": keywords, "h": own_h + COMMON_H, "p1": path1, "p2": path2}

GROUPS = [
    group("מנעולן – כללי", SITE + "/", ["מנעולן", "מנעולן 24 שעות", "מנעולן חירום", "מנעולן קרוב", "מנעולן באזור השרון", "מנעולן בשרון"],
          ["מנעולן קרוב אליכם", "מנעולן – התקשרו עכשיו", "ננעלתם בחוץ? התקשרו עכשיו", "מנעולן בשרון"]),
    group("פריצת דלתות", SITE + "/door-opening.html",
          ["פריצת דלת", "פריצת דלתות", "פורץ דלתות", "פורץ מנעולים", "ננעלתי בחוץ", "פתיחת דלת", "פריצת פלדלת", "ננעלתי מחוץ לבית"],
          ["פורץ דלתות ומנעולים", "ננעלתם בחוץ? התקשרו עכשיו", "פריצת פלדלת ודלתות", "פתיחת דלת ללא נזק"], "פריצת-דלתות"),
    group("החלפת צילינדר", SITE + "/cylinder.html",
          ["החלפת צילינדר", "צילינדר לדלת", "החלפת מנעול", "צילינדר מוגן", "החלפת צילינדר אחרי פריצה"],
          ["החלפת צילינדר במקום", "צילינדר מוגן לדלת", "אחרי מעבר דירה? החליפו", "החלפת מנעולים"], "צילינדר"),
    group("פתיחת כספות", SITE + "/safe.html", ["פתיחת כספת", "פורץ כספות", "פריצת כספת", "שכחתי קוד כספת"],
          ["פתיחת כספות", "שכחתם את הקוד?", "פריצת כספת"], "כספות"),
]
for slug, n, b, _ in cfg["CITIES"]:
    if slug == "moshavim": continue
    GROUPS.append(group(f"עיר – {n}", f"{SITE}/{slug}.html",
        [f"מנעולן {b}", f"מנעולן {n}", f"פורץ דלתות {b}", f"פריצת דלת {b}", f"מנעולן 24 שעות {b}"],
        [f"מנעולן {b}", f"פורץ דלתות {b}", f"מנעולן {b} – 24 שעות"], "מנעולן", n.replace(" ", "-")))

def fit(lst, n, mx):
    out, seen = [], set()
    for x in lst:
        if len(x) <= mx and x not in seen: out.append(x); seen.add(x)
    return out[:n]

H_COLS = [f"Headline {i}" for i in range(1, 16)]; D_COLS = [f"Description {i}" for i in range(1, 5)]
COLS = ["Campaign", "Campaign Type", "Networks", "Budget", "Budget type", "Bid Strategy Type", "Campaign Status", "EU political ads", "Ad type",
        "Ad Group", "Ad Group Status", "Keyword", "Criterion Type", *H_COLS, *D_COLS, "Final URL", "Path 1", "Path 2", "Status"]
rows = [{"Campaign": CAMPAIGN, "Campaign Type": "Search", "Networks": "Google search", "Budget": BUDGET_PLACEHOLDER,
         "Budget type": "Daily", "Bid Strategy Type": "Maximize clicks", "Campaign Status": "Paused", "EU political ads": "No"}]
# Les mots-clés à exclure ne passent pas par l'import web (valeurs refusées, essai du 3 nov. 2026) :
# ils sont listés dans campagne-lisible.md et s'ajoutent à la main (Mots-clés → Mots-clés à exclure).
problems = []
for g in GROUPS:
    rows.append({"Campaign": CAMPAIGN, "Ad Group": g["name"], "Ad Group Status": "Enabled"})
    for kw in g["kw"]:
        rows.append({"Campaign": CAMPAIGN, "Ad Group": g["name"], "Keyword": kw, "Criterion Type": "Phrase"})
    hs, ds = fit(g["h"], 15, 30), fit(COMMON_D, 4, 90)
    if len(hs) < 3: problems.append(f"{g['name']}: seulement {len(hs)} titres")
    for p in (g["p1"], g["p2"]):
        if len(p) > 15: problems.append(f"{g['name']}: chemin trop long « {p} »")
    ad = {"Campaign": CAMPAIGN, "Ad Group": g["name"], "Ad type": "Responsive search ad", "Final URL": g["url"], "Path 1": g["p1"], "Path 2": g["p2"], "Status": "Enabled"}
    ad.update({H_COLS[i]: h for i, h in enumerate(hs)}); ad.update({D_COLS[i]: d for i, d in enumerate(ds)})
    rows.append(ad)
if problems: raise SystemExit("PROBLÈMES : " + "; ".join(problems))

OUT = os.path.join(ROOT, "docs/google-ads"); os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "campagne.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT, "campagne-lisible.md"), "w", encoding="utf-8") as f:
    f.write(f"# Campagne « {CAMPAIGN} » (générée par `_build/ads.py`)\n\nStatut à l'import : **EN PAUSE**. Budget d'attente : {BUDGET_PLACEHOLDER} ₪/jour (à fixer avant d'activer).\n\n")
    f.write("## Mots-clés exclus (toute la campagne)\n" + " · ".join(NEGATIVES) + "\n\n")
    for g in GROUPS:
        f.write(f"## {g['name']}\nPage : {g['url']}\n\nMots-clés : " + " · ".join(f'"{k}"' for k in g["kw"]) + "\n\nTitres : " + " | ".join(fit(g["h"], 15, 30)) + "\n\n")
    f.write("## Descriptions (toutes les annonces)\n" + "\n".join(f"- {d}" for d in COMMON_D) + "\n")
print(f"{len(GROUPS)} groupes d'annonces, {sum(len(g['kw']) for g in GROUPS)} mots-clés, {len(NEGATIVES)} exclusions -> docs/google-ads/")
