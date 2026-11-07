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
- Automatismes GitHub Actions : `.github/workflows/site.yml` (contrôle à chaque push + IndexNow après mise en ligne), `surveillance.yml` (TOUTES LES HEURES : `check.py --live` = pages, numéro, HTTPS, DNS non détourné, en-têtes de sécurité, balise Google Ads, fichiers internes en 404 ; ouvre une issue si problème).
- Sécurité : en-têtes HSTS / X-Frame-Options / Referrer-Policy / Permissions-Policy + cache images posés via l'API Render (pas dans le dépôt). Police Rubik auto-hébergée (`public/fonts/`). Détail et checklist comptes : `docs/SECURITE-ET-ANTI-FRAUDE.md`.
- Tests locaux avec Playwright : bloquer googletagmanager/doubleclick (sinon de vraies visites sont envoyées au compte Google Ads).
- `CONTENT_DATE` dans build.py : date de mise à jour du contenu (sitemap/articles), fixe pour que le contrôle « régénérer = identique » passe.
- Réglages (URL, téléphone, horaires, délai, message WhatsApp, code Search Console, lien avis) : section RÉGLAGES en haut de `_build/build.py`. Une seule source de vérité.
- `SITE_URL` = https://rafihamanulan.co.il depuis le 1er nov. 2026 (canonical, sitemap, schema en dépendent). Garder le proxy Cloudflare en « DNS only » (sinon le certificat Render peut casser).
- Images dans `public/img/` (webp, sans EXIF). Photos réelles fournies par Rafi le 1er nov. 2026 (confirmées comme les siennes, usage officiel). Ne jamais publier une photo où l'on voit l'autocollant ou le numéro d'un concurrent.
- Prix : liste `PRICES` dans build.py = tarifs fournis par Raphaël le 7 nov. 2026 (page `prices.html`, blocs prix sur chaque page service, aperçu sur l'accueil, OfferCatalog). Ne jamais modifier un prix sans qu'il le donne. Orthographe laissée à Claude par Rafi (7 nov.) : « הדכנה » → « התקנה », « פלתות » = « פלטות » (סט פלטות קומפלט : ניקל, שחור, מעוגל – photos 7 nov.), « Keyloks » = KEYLOCX de רב-בריח (photo 7 nov.), « מגנום 5 מפתחות 320 ₪ » = sans carte de copie. Prix toujours triés en ordre croissant (tri automatique dans build.py). Catégorie « פריצה + החלפת צילינדר בפלדלת » = 300 ₪ + prix du cylindre, dès 620 ₪. Pas de photo de boîte aux lettres.
- Guides (articles) : liste `GUIDES` dans build.py, pages `guide-*.html`. Contenu factuel, pas de prix.
- Plan d'acquisition et textes Google Business : `docs/PLAN-CLIENTS.md`. Kit de lancement (WhatsApp Business, groupes, partenaires, Google Ads prêt) : `docs/KIT-LANCEMENT.md`.
- Imprimés (autocollant 60x40, carte 90x50, flyer A6, QR WhatsApp) : `python3 _build/print.py` → `marketing/` (nécessite `pip install qrcode` et Playwright). Mêmes réglages que build.py.
- Google Ads : campagne générée par `python3 _build/ads.py` → `docs/google-ads/campagne.csv` (format Google Ads Editor, importée EN PAUSE) + `MODE-EMPLOI.md`. Compte Google Ads AW-18553668064 (créé le 3 nov. via Claude in Chrome, compte Google de la fiche GBP refamanoulan@gmail.com). Campagne importée EN PAUSE ; 70 mots-clés (« מנעולן », service+ville, פורץ מנעולים, החלפת צילינדר) refusés par la règle Google « Local services » : exception demandée le 3 nov. (pas de champ justification), 88 mots-clés au total ; statut au 6 nov. : aucun refus visible (tout « Campaign is paused », 32 en « Low search volume ») — le vrai verdict n'apparaîtra qu'à l'activation ; Policy manager (7 nov.) : pub politique UE = fait, source du financement = fait, infos organisation = vérifiées, Dun & Bradstreet = en examen (3-5 jours ouvrés), « Confirm your affiliation » (pièce d'identité probable) = bloqué jusqu'à la fin de l'examen (Admin → Policy → Account → Advertiser Verification) ; budget actuel dans le compte : 25 ₪/jour ; Pardesiya non reconnue comme zone ; ciblage langue supprimé par Google (sept. 2026). Conversions « Clic sur appel » et « Clic WhatsApp » branchées sur le site (GADS_* dans build.py, testé). Page `privacy.html` (cookies Google Ads) liée au pied de page. Budget et activation : décision de Raphaël uniquement.
- IndexNow (Bing) : clé `INDEXNOW_KEY` dans build.py, fichier `<clé>.txt` à la racine ; après une grosse mise à jour, soumettre les URL du sitemap à https://api.indexnow.org/indexnow.
- Design : épuré, aéré, peu de texte, beaucoup de photos (demande de Rafi, 1er nov. 2026). Clair et moderne, style application. Police Rubik, bleu #1A56DB, vert WhatsApp #18A957. Mobile d'abord, barre fixe « appeler / WhatsApp » en bas sur mobile.

## Accès API (secrets de l'environnement, 3 nov. 2026)
- Render : secret réseau Bearer sur `api.render.com` (clé « claude-env »), vérifié OK le 3 nov. Service `srv-dbj7en142hec73c7ntc0` (publishPath public, autoDeploy yes, 2 domaines vérifiés). Les clés ne sont jamais visibles : le proxy les ajoute.
- Cloudflare : secret réseau Bearer sur `api.cloudflare.com` (token « claude », Zone DNS Edit, All zones, sans expiration), vérifié OK le 3 nov. Zone rafihamanulan.co.il = `5c83406223612057357ae7ed46edbee6` : 2 CNAME (@, www → rafi-hamanulan.onrender.com, DNS only) + TXT google-site-verification (ne pas supprimer).
- Ces secrets valent pour l'environnement « Full access » : utilisables sur tout autre projet de Raphaël lancé dans cet environnement.

## Routines actives
- `trig_019PUnWAXoMwXvsMBGrF4maU` : chaque jour (dim–ven 09:13 Jérusalem), cherche dans Gmail r.nabet26@gmail.com les e-mails Google Ads (vérification annonceur) + check.py --live. À SUPPRIMER quand la vérification annonceur est terminée. Les e-mails Ads arrivent sur refamanoulan@gmail.com : il faut un transfert vers r.nabet26 pour que la routine les voie.
- Stickers scooter : posés sur le top case par Rafi (7 nov.).

## Règles de contenu
- Ne JAMAIS présenter Netanya comme point de départ (« יוצא מנתניה ») : chaque client doit sentir que Rafi est dans sa ville (demande du 1er nov. 2026). Netanya n'apparaît que comme une ville parmi d'autres.
- Jamais de faux avis, de faux chiffres ni de prix inventés.
- Ne pas affirmer « מנעולן מורשה » ou une autorisation de la police tant que ce n'est pas confirmé.
- Garder les infos (nom, téléphone, horaires, zone) identiques à la fiche Google Business.

## À faire plus tard
- [x] Photos réelles (1er nov. 2026). Coffre-fort réel fourni le 7 nov. (img/safe.webp, t-safe). Boîte aux lettres (étiquette de nom recadrée hors champ), plaques ניקל/שחור/מעוגל et portail fournis le 7 nov. Porte blindée (p-steel) fournie le 7 nov. ; photo du verrou additionnel (t-extralock) = image type catalogue fabricant envoyée par Rafi. Manquent encore : Rafi lui-même, le scooter, ferme-porte.
- Ajouter un badge « agréé » si un certificat est confirmé.
- [x] Domaine relié et SITE_URL basculé (1er nov. 2026).
- [x] Fiche Google Business VÉRIFIÉE (5 nov. 2026). Lien d'avis `REVIEW_URL` = https://g.page/r/CavM3AVwHYkIEBM/review (sur le site + QR `marketing/qr-avis-google.png`). Ne jamais cliquer « Finish ad set-up » sur la fiche (crée une campagne Smart).
- [x] Search Console : propriété « Domaine » rafihamanulan.co.il validée le 3 nov. 2026 via Cloudflare (enregistrement TXT google-site-verification dans Cloudflare — NE PAS SUPPRIMER). `GSC_VERIFICATION` dans build.py inutile, laisser vide. Sitemap à soumettre : sitemap.xml.
