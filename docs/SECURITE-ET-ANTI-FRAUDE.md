# Protection du site, du référencement et du budget Google Ads (3 nov. 2026)

## Ce qui protège déjà le site (vérifié)
- **Site statique** (pas de base de données, pas de formulaire, pas de compte) : il n'y a presque rien à pirater sur le site lui-même.
- **Anti-DDoS** : Render sert le site derrière le réseau Cloudflare (en-tête `server: cloudflare`). Une attaque par saturation est absorbée en amont.
- **En-têtes de sécurité** ajoutés le 3 nov. via l'API Render : HSTS (HTTPS obligatoire), X-Frame-Options (le site ne peut pas être affiché dans un autre site pour piéger les visiteurs), Referrer-Policy, Permissions-Policy.
- **Surveillance toutes les heures** (GitHub Actions) : pages en ligne, numéro présent, certificat HTTPS, **DNS non détourné** (serveurs Cloudflare, www vers Render), en-têtes de sécurité, balise Google Ads présente, fichiers internes non publics. Alerte = issue GitHub = e-mail.
- **Police Rubik hébergée sur le site** : plus d'appel à Google Fonts (affichage plus rapide, moins de dépendances).

## Le vrai risque : la prise de contrôle d'un compte
Un concurrent ne peut pas « faire sauter » un site statique, mais quelqu'un qui obtient le mot de passe d'un de tes comptes peut tout changer. À faire **une fois** (validation en 2 étapes, avec une application ou une clé, pas de SMS si possible) :
- [ ] Compte Google refamanoulan@gmail.com (fiche Google, Google Ads, Search Console) : https://myaccount.google.com/signinoptions/twosv
- [ ] Compte Google habituel, s'il est différent
- [ ] GitHub : https://github.com/settings/security
- [ ] Render : https://dashboard.render.com/u/settings#security
- [ ] Cloudflare : https://dash.cloudflare.com/profile/authentication
- [ ] LiveDNS (registraire du domaine) : activer la double authentification et le **verrouillage du domaine** (DomainLock) s'il est proposé — empêche un transfert du domaine sans ton accord. Coût éventuel à vérifier.

## Référencement : ce qu'un concurrent peut tenter, et la parade
- **Liens toxiques vers ton site** (« negative SEO ») : Google les ignore en général d'après sa documentation ; on surveille dans Search Console → Liens. Rien à faire tant qu'aucune action manuelle n'apparaît.
- **Faux avis négatifs sur la fiche Google** : répondre calmement à chacun, signaler ceux qui sont faux (fiche → avis → ⋮ → Signaler). Le meilleur rempart : beaucoup de vrais avis (message WhatsApp dans PLAN-CLIENTS.md).
- **« Suggérer une modification » sur ta fiche** (changer ton numéro, marquer « fermé ») : Google t'envoie un e-mail ; vérifier la fiche chaque semaine, refuser toute modification qui n'est pas de toi.
- **Copie de ton contenu** : sans conséquence notable ; ton site est la source (dates, Search Console).

## Google Ads : clics frauduleux et budget
- **Google filtre lui-même les clics invalides** (robots, clics répétés) et ne les facture pas ; quand un clic invalide passe, il est recrédité. On le vérifie avec les colonnes « Clics incorrects ».
- **Le plafond absolu** : le budget par jour. Même en cas d'attaque, Google ne dépasse pas en moyenne ton budget journalier (jusqu'à 2× un jour donné, compensé sur le mois).
- **Déjà réglé** : Réseau de Recherche uniquement (pas de Display ni partenaires, où la fraude est la plus forte), zones en « Présence » (seulement les gens physiquement dans tes villes), calendrier, mots-clés en « expression exacte » (= phrase match dans l'interface anglaise), 18 exclusions.
- **À régler** (consigne Claude in Chrome ci-dessous) : couper « AI Max » / requête large / extension d'URL (qui dépensent sur des recherches qu'on n'a pas choisies), plafond de coût par clic, colonnes de clics incorrects.
- **Outils payants anti-fraude** (ClickCease, Lunio…) : inutiles à ce stade pour un petit budget ; à reconsidérer seulement si le taux de clics incorrects dépasse ~10-15 % plusieurs semaines.
- **Exclusion d'adresses IP** : si tu connais l'IP d'un concurrent qui clique (rare), Paramètres → Exclusions d'adresses IP.

## État vérifié le 3 nov. 2026 (par Claude in Chrome)
- AI Max OFF, extension d'URL finale OFF, requête large OFF, composants automatiques OFF, réseaux = Recherche uniquement.
- Accès au compte : un seul utilisateur (refamanoulan@gmail.com, Admin).
- Limite de CPC : non posée (Google exige un montant) – décision de Raphaël, après la semaine de test.
- Colonnes « clics incorrects » : indisponibles tant que la campagne n'a pas diffusé – à ajouter après activation.
- Bing Webmaster et validation en 2 étapes : à faire par Raphaël (l'agent refuse de créer des comptes ou de toucher la sécurité).

## Consigne à coller dans Claude in Chrome (Google Ads + Bing)
```
Règles : ne rien activer, ne fixer aucun budget, ne rien payer, ne rien supprimer. Pour le reste, avance sans me demander et résume à la fin.
1. Google Ads, campagne « רפי המנעולן – חיפוש » → Paramètres :
   a. Si « AI Max pour le Réseau de Recherche » est activé : désactive-le.
   b. Si « Requête large » (broad match) au niveau campagne est activé : désactive-le.
   c. « Extension d'URL finale » / « Final URL expansion » : désactive.
   d. Ressources automatiques (« Automatically created assets ») : désactive.
   e. Réseaux : vérifie que Display et Partenaires sont décochés.
2. Stratégie d'enchères « Maximiser les clics » : coche « Définir une limite de CPC maximale » et laisse le champ VIDE ; dis-moi seulement si Google l'exige.
3. Campagnes → colonnes → ajoute « Clics incorrects » et « Taux de clics incorrects », enregistre la vue.
4. Outils → Accès et sécurité : liste-moi les utilisateurs ayant accès au compte.
5. Bing Webmaster Tools : va sur https://www.bing.com/webmasters, connecte-toi avec le compte Google refamanoulan@gmail.com, choisis « Importer depuis Google Search Console », sélectionne rafihamanulan.co.il, valide.
Résume : fait / pas fait / problème.
```
