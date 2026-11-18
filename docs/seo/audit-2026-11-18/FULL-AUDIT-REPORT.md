# Audit SEO – rafihamanulan.co.il (18 nov. 2026)

**Note globale : 76 / 100.** Type : service local à domicile (serrurier, zone de service, sans vitrine).
Méthode : rendu de l'accueil (Chromium mobile), lecture des 49 pages du sitemap, en-têtes HTTP, robots/sitemap/schema. Aucune donnée Google (Search Console, GA4, CrUX) ni extension payante : **non vérifié** = positions réelles, indexation, trafic, avis, profil Google Business, backlinks. Audit seul, rien modifié.

| Catégorie | Poids | Note |
|---|---|---|
| Technique | 22 % | 88 |
| Contenu | 23 % | 62 |
| On-page | 20 % | 80 |
| Schema | 10 % | 78 |
| Performance | 10 % | 95 |
| Préparation IA | 10 % | 55 |
| Images | 5 % | 85 |

## Ce qui va bien (vérifié)
- HTTP→HTTPS et www→sans-www en 301 ; HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy en place.
- robots.txt ouvert + sitemap de 49 URL ; canonical correct sur 49/49 ; titres et descriptions uniques (0 doublon) ; 1 seul H1 par page ; `lang=he dir=rtl`.
- Mobile : LCP ≈ 0,8 s, CLS 0, 16 requêtes, ~330 Ko, pas de défilement horizontal (mesure lab Playwright, pas des données terrain).
- Schema `Locksmith` complet (téléphone, horaires, zone, fondateur, logo) + `FAQPage` + `BreadcrumbList` + `WebSite`. Toutes les images ont un attribut alt.
- Pages ville/service/guide bien structurées, hébreu, numéro et WhatsApp partout.

## Problèmes (par importance)
1. **Pages villes quasi identiques (Élevé).** 34 pages ville ≈ 840 mots chacune, ~96 % de texte commun (comparaison Netanya/Hadera). Google peut les juger « pages passerelles » et n'en indexer que quelques-unes. Chaque page est surtout le même menu de prix.
2. **Aucune preuve locale/avis sur le site (Élevé).** Pas d'avis, pas d'`aggregateRating`, pas de cas réels par ville, pas d'adresse. Pour un serrurier (secteur à arnaques), c'est le facteur de confiance n°1. Le lien d'avis existe mais aucun avis affiché (on n'en invente pas).
3. **Contenu fin sur les guides (Moyen).** 7 guides de 400–470 mots, sans auteur, sans date visible, sans schéma `Article`. Peu de chance de ranker face aux concurrents.
4. **Schema incomplet (Moyen).** `PostalAddress` sans ville ni région ; pas d'`aggregateRating`/`Review` ; pas de `Service` + `OfferCatalog` sur les pages service ; `FAQPage` n'apporte plus d'affichage enrichi dans Google (réservé santé/gouv.) – utile seulement aux IA.
5. **Préparation IA / robots (Moyen-faible).** Pas de `llms.txt` (404, optionnel, ignoré par Google), pas de Content-Signal dans robots.txt, pas de mention explicite des robots IA.
6. **Petits points techniques (Faible).** `/favicon.ico` en 404 (le favicon est en SVG) ; `/netanya` (sans .html) répond 200 en plus de `/netanya.html` (canonical protège, mais mieux vaut un 301) ; pas de CSP ; pas de `security.txt` ; 2 images sans `loading` sur chaque page.
7. **Maillage (Faible).** Menu et pied de page bons, mais les pages guides ne renvoient pas systématiquement vers la page service correspondante (à vérifier page par page).

## Local SEO (partiel)
Site cohérent avec la fiche (nom, tél., horaires). Profil Google Business, citations (Yellow Pages Israël, Midrag, Dapei Zahav…), nombre/qualité d'avis, position dans le pack local : **non vérifiés** (pas d'accès). C'est le canal n°1 pour ce métier.
