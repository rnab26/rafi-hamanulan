"""Contrôles automatiques du site généré (utilisé en local et par GitHub Actions).
Usage : python3 _build/check.py            -> vérifie le dossier public/
        python3 _build/check.py --live     -> vérifie le site en ligne (toutes les URL du sitemap)
Sort avec le code 1 et la liste des problèmes s'il y en a."""
import os, re, sys, json, glob, ssl, socket, datetime, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
src = open(os.path.join(ROOT, "_build/build.py"), encoding="utf-8").read().split("# ==================================================================")[0]
cfg = {"__file__": os.path.join(ROOT, "_build/build.py")}; exec(src, cfg)
SITE = cfg["SITE_URL"]
# Phrases interdites (règles de contenu du CLAUDE.md)
FORBIDDEN = {"יוצא מנתניה": "Netanya présentée comme point de départ", "052-3931553": "numéro d'un concurrent",
             "מנעולן מורשה": "agrément non confirmé", "מורשה משטרה": "agrément non confirmé"}
problems = []

def check_local():
    files = glob.glob(os.path.join(PUB, "*.html"))
    if len(files) < 20: problems.append(f"seulement {len(files)} pages HTML dans public/")
    for f in files:
        t = open(f, encoding="utf-8").read(); n = os.path.basename(f)
        for h in set(re.findall(r'(?:href|src)="([^":#?]+\.(?:html|webp|css|svg|png|jpg|vcf))"', t)):
            if not os.path.exists(os.path.join(PUB, h)): problems.append(f"{n}: lien cassé vers {h}")
        for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try: json.loads(j)
            except Exception as e: problems.append(f"{n}: JSON-LD invalide ({e})")
        if n != "404.html" and t.count("<h1>") != 1: problems.append(f"{n}: {t.count('<h1>')} titres h1 (attendu 1)")
        if n != "404.html" and f'href="{SITE}/' not in t: problems.append(f"{n}: canonical ne pointe pas vers {SITE}")
        for k, why in FORBIDDEN.items():
            if k in t: problems.append(f"{n}: texte interdit « {k} » ({why})")
    if "rafihamanulan.co.il" in open(os.path.join(PUB, "sitemap.xml")).read() and "rafihamanulan.co.il" not in SITE:
        problems.append("sitemap pointe vers un domaine non relié")

def check_live():
    urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(PUB, "sitemap.xml")).read())
    for u in urls:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "site-monitor"}), timeout=30) as r:
                body = r.read().decode("utf-8", "ignore")
                if r.status != 200: problems.append(f"{u}: HTTP {r.status}")
                elif cfg["PHONE"] not in body: problems.append(f"{u}: numéro de téléphone absent de la page")
        except Exception as e: problems.append(f"{u}: inaccessible ({e})")
    host = SITE.split("//")[1].split("/")[0]
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=20) as s, ctx.wrap_socket(s, server_hostname=host) as ss:
            exp = datetime.datetime.strptime(ss.getpeercert()["notAfter"], "%b %d %H:%M:%S %Y %Z")
            days = (exp - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)).days
            if days < 14: problems.append(f"certificat HTTPS de {host} expire dans {days} jours")
    except Exception as e: problems.append(f"HTTPS {host}: {e}")

check_live() if "--live" in sys.argv else check_local()
if problems:
    print("PROBLÈMES :"); [print(" -", p) for p in problems]; sys.exit(1)
print("OK –", "site en ligne" if "--live" in sys.argv else "public/", "sans problème")
