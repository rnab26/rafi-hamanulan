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
    # Fichiers internes qui ne doivent JAMAIS être en ligne (Publish Directory = public)
    for priv in ["CLAUDE.md", "docs/KIT-LANCEMENT.md", "docs/PLAN-CLIENTS.md", "_build/build.py", "public/index.html"]:
        try:
            urllib.request.urlopen(urllib.request.Request(f"{SITE}/{priv}", headers={"User-Agent": "site-monitor"}), timeout=20)
            problems.append(f"{SITE}/{priv} est accessible publiquement (vérifier Publish Directory = public sur Render, puis « Clear build cache & deploy »)")
        except urllib.error.HTTPError as e:
            if e.code != 404: problems.append(f"{SITE}/{priv}: HTTP {e.code} inattendu")
        except Exception as e: problems.append(f"{SITE}/{priv}: {e}")
    # Intégrité DNS (détourne-t-on le domaine ?) via le résolveur public de Google
    host0 = SITE.split("//")[1].split("/")[0]
    def dns(name, typ):
        with urllib.request.urlopen(f"https://dns.google/resolve?name={name}&type={typ}", timeout=20) as r:
            return [a["data"].rstrip(".").lower() for a in json.load(r).get("Answer", [])]
    try:
        ns = dns(host0, "NS")
        if not ns or not all(n.endswith(".ns.cloudflare.com") for n in ns):
            problems.append(f"DNS : serveurs de noms inattendus {ns} (attendu *.ns.cloudflare.com) – possible détournement du domaine")
        www = dns("www." + host0, "CNAME")
        if www and www != ["rafi-hamanulan.onrender.com"]:
            problems.append(f"DNS : www pointe vers {www} au lieu de Render")
    except Exception as e: problems.append(f"DNS : vérification impossible ({e})")
    # En-têtes de sécurité et balise Google Ads sur l'accueil
    try:
        with urllib.request.urlopen(urllib.request.Request(SITE + "/", headers={"User-Agent": "site-monitor"}), timeout=30) as r:
            hdr = {k.lower(): v for k, v in r.headers.items()}; home = r.read().decode("utf-8", "ignore")
        for h in ["strict-transport-security", "x-frame-options", "referrer-policy"]:
            if h not in hdr: problems.append(f"en-tête de sécurité manquant : {h}")
        if cfg.get("GADS_ID") and cfg["GADS_ID"] not in home: problems.append("balise Google Ads absente de l'accueil (conversions non comptées)")
    except Exception as e: problems.append(f"accueil : {e}")
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
