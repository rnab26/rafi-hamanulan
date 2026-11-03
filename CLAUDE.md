# Site « רפי המנעולן »

## Le business
- Serrurier indépendant, nom commercial : רפי המנעולן. Basé à Netanya, se déplace en scooter.
- Zone : de Césarée (קיסריה) à Hod HaSharon (הוד השרון), plus les moshavim. Arrivée en général en ~25 min.
- Téléphone : 054-530-1389 (+972545301389). WhatsApp : https://wa.me/972545301389
- Horaires : dimanche–jeudi 24 h/24 ; vendredi 09:00–16:00 ; samedi soir (motzaei Shabbat) 19:00–00:00. Fermé pendant Shabbat.
- Services : פריצת דלתות, החלפת צילינדר, תיקון והחלפת מנעולים, פתיחת כספות, שדרוג מיגון.
- Domaine : rafihamanulan.co.il, acheté le 1er nov. 2026 chez LiveDNS (compte de Raphael Nabet). DNS chez Cloudflare (compte de Raphael, serveurs candy/seth.ns.cloudflare.com ; 2 CNAME @ et www → rafi-hamanulan.onrender.com, proxy « DNS only »). Relié à Render, HTTPS Let's Encrypt OK le 1er nov. 2026 vers 07:10. Site : https://rafihamanulan.co.il (l'ancienne adresse onrender.com marche toujours).

## Technique
- Site statique en hébreu (RTL), fichiers HTML à plat dans `public/` (pas de sous-dossiers).
- Hébergé sur Render (static site « rafi-hamanulan »), auto-deploy à chaque push sur main.
- TOUT le site est généré par _build/build.py dans `public/`. Ne jamais éditer les .html à la main : modifier build.py, lancer `python3 _build/build.py` puis `python3 _build/check.py` depuis la racine, commit, push.
- `public/` = seul dossier publié par Render (Publish Directory = `public`, confirmé le 3 nov. 2026). Rien d'autre (CLAUDE.md, docs/, _build/, marketing/) ne doit être en ligne. `LEGACY_ROOT_COPY=False` (copie à la racine supprimée le 3 nov.).
- Automatismes GitHub Actions : `.github/workflows/site.yml` (contrôle à chaque push + IndexNow après mise en ligne), `surveillance.yml` (chaque jour : `check.py --live`, ouvre une issue si problème).
- `CONTENT_DATE` dans build.py : date de mise à jour du contenu (sitemap/articles), fixe pour que le contrôle « régénérer = identique » passe.
- Réglages (URL, téléphone, horaires, délai, message WhatsApp, code Search Console, lien avis) : section RÉGLAGES en haut de `_build/build.py`. Une seule source de vérité.
- `SITE_URL` = https://rafihamanulan.co.il depuis le 1er nov. 2026 (canonical, sitemap, schema en dépendent). Garder le proxy Cloudflare en « DNS only » (sinon le certificat Render peut casser).
- Images dans `public/img/` (webp, sans EXIF). Photos réelles fournies par Rafi le 1er nov. 2026 (confirmées comme les siennes, usage officiel). Ne jamais publier une photo où l'on voit l'autocollant ou le numéro d'un concurrent.
- Guides (articles) : liste `GUIDES` dans build.py, pages `guide-*.html`. Contenu factuel, pas de prix.
- Plan d'acquisition et textes Google Business : `docs/PLAN-CLIENTS.md`. Kit de lancement (WhatsApp Business, groupes, partenaires, Google Ads prêt) : `docs/KIT-LANCEMENT.md`.
- Imprimés (autocollant 60x40, carte 90x50, flyer A6, QR WhatsApp) : `python3 _build/print.py` → `marketing/` (nécessite `pip install qrcode` et Playwright). Mêmes réglages que build.py.
- IndexNow (Bing) : clé `INDEXNOW_KEY` dans build.py, fichier `<clé>.txt` à la racine ; après une grosse mise à jour, soumettre les URL du sitemap à https://api.indexnow.org/indexnow.
- Design : épuré, aéré, peu de texte, beaucoup de photos (demande de Rafi, 1er nov. 2026). Clair et moderne, style application. Police Rubik, bleu #1A56DB, vert WhatsApp #18A957. Mobile d'abord, barre fixe « appeler / WhatsApp » en bas sur mobile.

## Règles de contenu
- Ne JAMAIS présenter Netanya comme point de départ (« יוצא מנתניה ») : chaque client doit sentir que Rafi est dans sa ville (demande du 1er nov. 2026). Netanya n'apparaît que comme une ville parmi d'autres.
- Jamais de faux avis, de faux chiffres ni de prix inventés.
- Ne pas affirmer « מנעולן מורשה » ou une autorisation de la police tant que ce n'est pas confirmé.
- Garder les infos (nom, téléphone, horaires, zone) identiques à la fiche Google Business.

## À faire plus tard
- [x] Photos réelles (1er nov. 2026). Manquent encore : Rafi lui-même, le scooter, un coffre-fort (la tuile « פתיחת כספות » utilise une photo libre CC0).
- Ajouter un badge « agréé » si un certificat est confirmé.
- [x] Domaine relié et SITE_URL basculé (1er nov. 2026).
- Après la vérification Google Business : remplir `REVIEW_URL` dans build.py.
- Search Console : remplir `GSC_VERIFICATION` quand Rafi envoie le code, puis soumettre sitemap.xml.
