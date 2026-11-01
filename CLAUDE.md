# Site « רפי המנעולן »

## Le business
- Serrurier indépendant, nom commercial : רפי המנעולן. Basé à Netanya, se déplace en scooter.
- Zone : de Césarée (קיסריה) à Hod HaSharon (הוד השרון), plus les moshavim. Arrivée en général en ~25 min.
- Téléphone : 054-530-1389 (+972545301389). WhatsApp : https://wa.me/972545301389
- Horaires : dimanche–jeudi 24 h/24 ; vendredi 09:00–16:00 ; samedi soir (motzaei Shabbat) 19:00–00:00. Fermé pendant Shabbat.
- Services : פריצת דלתות, החלפת צילינדר, תיקון והחלפת מנעולים, פתיחת כספות, שדרוג מיגון.
- Domaine prévu : rafihamanulan.co.il (pas encore acheté). URL actuelle : https://rafi-hamanulan.onrender.com

## Technique
- Site statique en hébreu (RTL), fichiers HTML à plat à la racine (pas de sous-dossiers).
- Hébergé sur Render (static site « rafi-hamanulan »), auto-deploy à chaque push sur main.
- TOUT le site est généré par _build/build.py. Ne jamais éditer les .html à la main : modifier build.py, lancer `python3 _build/build.py` depuis la racine, vérifier, commit, push.
- Réglages (URL, téléphone, horaires, délai, message WhatsApp, code Search Console, lien avis) : section RÉGLAGES en haut de `_build/build.py`. Une seule source de vérité.
- `SITE_URL` = https://rafi-hamanulan.onrender.com tant que le domaine n'est pas relié (canonical, sitemap, schema en dépendent). Ne jamais mettre un domaine non relié.
- Images dans `img/` (webp, sans EXIF). Photos réelles fournies par Rafi le 1er nov. 2026. Ne jamais publier une photo où l'on voit l'autocollant ou le numéro d'un concurrent.
- Plan d'acquisition et textes Google Business : `docs/PLAN-CLIENTS.md`.
- Design : épuré, aéré, peu de texte, beaucoup de photos (demande de Rafi, 1er nov. 2026). Clair et moderne, style application. Police Rubik, bleu #1A56DB, vert WhatsApp #18A957. Mobile d'abord, barre fixe « appeler / WhatsApp » en bas sur mobile.

## Règles de contenu
- Jamais de faux avis, de faux chiffres ni de prix inventés.
- Ne pas affirmer « מנעולן מורשה » ou une autorisation de la police tant que ce n'est pas confirmé.
- Garder les infos (nom, téléphone, horaires, zone) identiques à la fiche Google Business.

## À faire plus tard
- [x] Photos réelles (1er nov. 2026). Manquent encore : Rafi lui-même, le scooter, un coffre-fort (la tuile « פתיחת כספות » utilise une photo libre CC0).
- Ajouter un badge « agréé » si un certificat est confirmé.
- Quand le domaine est acheté : le relier à Render, vérifier canonical/sitemap.
- Après la vérification Google Business : remplir `REVIEW_URL` dans build.py.
- Search Console : remplir `GSC_VERIFICATION` quand Rafi envoie le code, puis soumettre sitemap.xml.
