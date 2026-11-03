# Kit de lancement – des clients SANS attendre Google Maps

Préparé la nuit du 1er nov. 2026. Tout est prêt à copier-coller. Rien n'a été publié ni dépensé en ton nom.

## Ce matin, dans cet ordre (environ 1 h en tout)

1. **WhatsApp Business** (10 min, gratuit) → section 2. Chaque appel manqué devient un message auquel tu réponds.
2. **Commander les imprimés** (10 min) → section 1. C'est la source n°1 des serruriers : l'autocollant sur la porte.
3. **Poster dans 5 groupes Facebook/WhatsApp de quartier** (15 min) → section 3.
4. **Écrire à 10 agences immobilières ou gestionnaires d'immeubles** (15 min) → section 4.
5. **Décider le budget Google Ads** → section 5. C'est le seul moyen d'avoir des appels de Google **dès cette semaine**, avant ta fiche Maps.
6. **Acheter le domaine** → `docs/PLAN-CLIENTS.md`, section 6.

---

## 1. Imprimés (fichiers prêts dans `marketing/`)

| Fichier | Format | Usage |
|---|---|---|
| `autocollant-porte-60x40.pdf` | 60 × 40 mm | À coller sur le cadre de porte, près du cylindre, **après chaque intervention**. |
| `carte-visite-90x50.pdf` | 90 × 50 mm, recto-verso | À laisser au client, au gardien, au commerçant. |
| `flyer-A6.pdf` | 105 × 148 mm | Boîtes aux lettres, tableaux d'affichage d'immeuble, épiceries. |
| `sticker-scooter-30x15.pdf` | 30 × 15 cm | Flanc ou dossier du scooter. |
| `sticker-topcase-arriere-48x11.pdf` | 48 × 11 cm, bandeau | Arrière du top case, sous les verrous. |
| `sticker-topcase-cote-18x16.pdf` | 18 × 16 cm | Côtés du top case (à imprimer en 2 exemplaires). |

Le **QR code** ouvre WhatsApp avec un message déjà rédigé. J'ai testé les 3 : ils mènent bien à ton numéro.

**À dire à l'imprimeur** (n'importe quelle imprimerie, ou une commande en ligne avec la recherche « הדפסת מדבקות ויניל ») :
- Autocollant : **vinyle résistant à l'eau**, coins arrondis, 500 à 1000 exemplaires.
- Carte : 350 g mat, recto-verso, 500 exemplaires.
- Flyer : 135 g, 500 à 1000 exemplaires.
- Stickers scooter : **vinyle extérieur laminé, anti-UV** (le soleil israélien décolore un vinyle non laminé en quelques mois), découpe à la forme, 2 exemplaires de chaque. Mesure ton top case et ton flanc avant : si les dimensions diffèrent, dis-les-moi, je régénère au bon format.
- Demande-lui d'**ajouter 2 mm de fond perdu** (les fichiers sont au format exact, sans marge) et de t'envoyer une épreuve avant d'imprimer.
- Prix : je ne les connais pas. Demande deux devis.

Pour modifier un texte : dis-le-moi, je change `_build/print.py` et je régénère les fichiers.

---

## 2. WhatsApp Business (gratuit)

Installe « WhatsApp Business » sur ton numéro 054-530-1389 (l'application propose de transférer ton compte actuel), puis Paramètres de l'entreprise.

**Nom :** `רפי המנעולן`  **Catégorie :** Services à domicile / Automobile & services → choisis « Services » si « Serrurier » n'existe pas.

**Description :**
```
מנעולן – מגיע אליכם בקטנוע לכל אזור השרון, מקיסריה ועד הוד השרון, בדרך כלל תוך כ-25 דקות. פריצת דלתות, החלפת צילינדר, תיקון מנעולים, פתיחת כספות ושדרוג מיגון. מחיר ברור לפני העבודה.
```
**Horaires :** dim–jeu 24 h/24 · ven 09:00–16:00 · sam 19:00–00:00. **Site :** `https://rafihamanulan.co.il`

**Message d'accueil** (outils → message d'accueil) :
```
שלום, הגעתם לרפי המנעולן 🔑
כדי שאגיע מהר: שלחו כתובת מדויקת ומה קרה (ננעלתם בחוץ / מפתח שבור / החלפת צילינדר). אם אפשר – צרפו תמונה של המנעול.
```

**Message d'absence** (hors horaires) :
```
שלום, כרגע אני מחוץ לשעות הפעילות (שבת). אחזור אליכם מיד במוצאי שבת. אפשר להשאיר כאן כתובת ותיאור קצר.
```

**Réponses rapides** (raccourci `/` dans la conversation) :
- `/בדרך` → `אני בדרך אליכם, אגיע בעוד כ-[__] דקות. 🛵`
- `/מחיר` → `אחרי שאראה את הדלת אגיד לכם מחיר ברור, ורק אחרי שתאשרו אתחיל לעבוד.`
- `/ביקורת` → le message d'avis Google de `docs/PLAN-CLIENTS.md` (quand ta fiche existera).

---

## 3. Groupes de quartier (Facebook et WhatsApp)

Cherche sur Facebook : `נתניה`, `כפר סבא`, `רעננה`, `הרצליה`, `חדרה`, `הוד השרון`, `קדימה צורן`, `עיר ימים`, `רמת פולג` + le mot `קבוצה` ou `שכנים`. Rejoins-en 5 à 10. **Lis d'abord les règles** : beaucoup n'autorisent la pub qu'un jour précis de la semaine.

**Post de présentation** (avec 2 ou 3 de tes photos) :
```
שלום לכולם 👋
אני רפי, מנעולן עצמאי באזור. מגיע בקטנוע, אז גם בפקקים אני אצלכם בדרך כלל תוך כ-25 דקות.
פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות.
מחיר ברור לפני שמתחילים, ומי שעונה לטלפון זה אני.
שמרו את המספר למקרה חירום: 054-530-1389 🔑
```

**Le meilleur moment pour agir :** quand quelqu'un demande dans un groupe « מישהו מכיר מנעולן? ». Réponds vite, en une ligne, avec ton numéro. Active les notifications sur ces groupes.

Ne poste pas le même message tous les jours : tu te ferais exclure.

---

## 4. Partenaires qui t'enverront des clients régulièrement

Chaque changement de locataire = un cylindre à changer. Chaque immeuble = des portes d'entrée, des boîtes aux lettres, des locaux techniques.

Trouve-les sur Google Maps (liens directs) :
- Agences immobilières : https://www.google.com/maps/search/תיווך+נתניה · https://www.google.com/maps/search/תיווך+כפר+סבא · https://www.google.com/maps/search/תיווך+רעננה
- Gestion d'immeubles : https://www.google.com/maps/search/חברת+ניהול+בניינים+השרון

**Message (WhatsApp ou en passant à l'agence) :**
```
שלום, אני רפי – מנעולן עצמאי באזור השרון.
אני עובד עם משרדי תיווך וחברות ניהול: החלפת צילינדר בין שוכרים, פתיחת דירות, תיקון מנעולים בבניינים.
מגיע בקטנוע תוך כ-25 דקות, מחיר ברור מראש, וחשבונית מסודרת.
אשמח לשמור אצלכם את המספר: 054-530-1389. אם יש לכם דירה שצריך להחליף בה צילינדר בקרוב – אשמח להגיע.
```
« Facture en règle » : ne la garde que si tu factures effectivement.

---

## 5. Google Ads – des appels dès cette semaine (à décider : ça coûte)

Pourquoi : la fiche Google Maps peut prendre des jours ou des semaines (vérification, avis). Une annonce payante apparaît **le jour même** en haut de Google.

**Ce que je te propose** (c'est à toi de décider) : un test de 7 jours avec un **budget fixe par jour** que tu choisis. Google ne dépasse pas, en moyenne, le budget par jour que tu fixes. Le prix d'un clic sur « מנעולן » est élevé parce que c'est une urgence : **je ne le connais pas pour ta zone**, on le mesure pendant la semaine de test avant d'augmenter.

**Création** : https://ads.google.com → « Nouvelle campagne » → objectif « Prospects » → type **Réseau de Recherche** (décoche le Réseau Display et les partenaires).

- **Zones** : ajoute une par une les villes : קיסריה, חדרה, אור עקיבא, נתניה, כפר יונה, אבן יהודה, קדימה-צורן, תל מונד, פרדסיה, כפר סבא, רעננה, הרצליה, הוד השרון. Options de zone → « **Présence** : personnes qui se trouvent dans vos zones ».
- **Langues** : hébreu + anglais.
- **Calendrier** : dim–jeu toute la journée ; ven 09:00–16:00 ; sam 19:00–23:59. Pas d'annonce pendant Shabbat.
- **Enchères** : « Maximiser les clics » avec un CPC maximum, la première semaine.
- **Composant Appel** : `054-530-1389` (l'annonce montre un bouton « appeler » sur mobile).
- **Page de destination** : `https://rafihamanulan.co.il` (ou la page de la ville).

**Mots-clés** (entre guillemets = « expression ») :
```
"מנעולן"
"מנעולן בנתניה"
"מנעולן בכפר סבא"
"מנעולן ברעננה"
"מנעולן בהרצליה"
"מנעולן בחדרה"
"מנעולן בהוד השרון"
"פורץ דלתות"
"פורץ מנעולים"
"פריצת דלת"
"פריצת פלדלת"
"החלפת צילינדר"
"מנעולן 24 שעות"
"מנעולן חירום"
"ננעלתי בחוץ"
```

**Mots-clés à exclure** (sinon tu paies pour des gens qui ne sont pas clients) :
```
קורס
לימודי
ללמוד
עבודה
דרושים
משרה
איך לפתוח
לבד
יוטיוב
סרטון
רכב
אוטו
אופנוע
סיטונאי
```
J'ai exclu « voiture » (רכב, אוטו) parce que je ne sais pas si tu ouvres des voitures. Si oui, dis-le : je l'ajoute aussi au site.

**Annonce** (Google mélange les titres et descriptions tout seul) :

Titres (30 caractères max, tous vérifiés) :
```
מנעולן קרוב אליכם
מנעולן – הגעה תוך כ-25 דק׳
פורץ דלתות ומנעולים
ננעלתם בחוץ? התקשרו עכשיו
מחיר ברור לפני העבודה
פתיחה ללא נזק ככל שניתן
ישירות מול בעל המקצוע
זמין 24 שעות בימי חול
החלפת צילינדר במקום
מנעולן בכפר סבא ורעננה
מנעולן בנתניה ובחדרה
מנעולן בהרצליה ובהוד השרון
הגעה בקטנוע, גם בפקקים
פריצת פלדלת ודלתות
רפי המנעולן
```
Descriptions (90 caractères max, vérifiées) :
```
ננעלתם בחוץ? רפי המנעולן מגיע בקטנוע תוך כ-25 דקות. מחיר ברור לפני שמתחילים.
פריצת דלתות, החלפת צילינדר, תיקון מנעולים ופתיחת כספות. לבית ולעסק.
מי שעונה לטלפון הוא מי שמגיע אליכם. בלי מוקד ובלי הפתעות במחיר.
זמין 24 שעות בימים א׳–ה׳, בשישי עד 16:00 ובמוצאי שבת עד חצות.
```

**Surveillance** : regarde chaque soir « Termes de recherche » et ajoute en exclusion tout ce qui n'est pas un client. Après 7 jours, on compare le coût total au nombre d'appels et d'interventions, puis on décide de continuer, d'ajuster ou d'arrêter.

Si tu veux que je t'aide à la créer en direct, dis-le-moi avec ton budget maximum par jour.

---

## 6. Vidéos courtes (Instagram Reels, TikTok, YouTube Shorts) – gratuit, juste toi et ton téléphone

Les vidéos de serrurier « satisfaisantes » (porte qui s'ouvre, cylindre qu'on change) font beaucoup de vues localement. Chaque vidéo = ton numéro vu par des centaines de gens du coin.

**Règles** : 15 à 30 secondes, téléphone à la verticale, jamais le visage d'un client ni son numéro de rue, toujours avec l'accord du client. Ne filme pas comment on ouvre une porte en détail (ça aiderait les cambrioleurs) : montre le résultat.

**Légende type** (à coller sous chaque vidéo, change la 1re ligne) :
```
[מה עשינו היום] 🔑
רפי המנעולן – מגיע אליכם בקטנוע בכל אזור השרון.
📞 054-530-1389
#מנעולן #מנעולןבשרון #פריצתדלתות #החלפתצילינדר #נתניה #כפרסבא #רעננה #הרצליה #חדרה #הודהשרון
```

**30 idées, une par jour** (choisis celles qui collent à ta journée) :
1. Avant / après : vieux cylindre → nouveau cylindre (gros plan).
2. « Ce que je vois le plus souvent cette semaine » en 3 plans.
3. Le scooter qui démarre + texte « en route » (sans plaque visible).
4. Un cylindre usé à côté d'un neuf : « la différence ».
5. La boîte d'un cylindre protégé qu'on ouvre (MTL, רב-בריח…).
6. « 3 erreurs quand on est enfermé dehors » (texte à l'écran, reprend le guide du site).
7. Un mortaise (מנעול רב-בריח) démonté : « voilà ce qu'il y a dans votre porte ».
8. Clé cassée extraite du cylindre (gros plan sur le morceau).
9. Porte fermée → porte ouverte (sans montrer la technique).
10. « Quand changer son cylindre ? » 5 cas, texte à l'écran.
11. Ton matériel rangé (boîtes, cylindres) : « toujours prêt ».
12. Le trajet de nuit (lumières de la ville) : « 24 h en semaine ».
13. Après une effraction : la porte réparée (accord du client).
14. Poignée cassée → poignée neuve.
15. Question d'un client + ta réponse en 15 secondes.
16 à 30 : refais les meilleures (celles qui ont eu le plus de vues), dans une autre ville.

**Astuce de lieu** : sur Instagram et TikTok, ajoute la ville en lieu (נתניה, כפר סבא…) en changeant à chaque vidéo. C'est ce qui la montre aux gens de cette ville.

---

## 7. Publications sur la fiche Google (quand elle existe) – 1 par semaine

Google montre les fiches actives en priorité. Chaque semaine : 1 photo d'une intervention + 2 lignes.
```
החלפנו היום צילינדר מוגן בדלת כניסה. מחיר ברור לפני העבודה, והגעה בקטנוע תוך כ-25 דקות.
📞 054-530-1389
```

---

## 8. Faire revenir les clients et le bouche-à-oreille (gratuit)

- **Après chaque intervention** : l'autocollant sur la porte + la carte au client + le message d'avis Google (section 2).
- **Liste de diffusion WhatsApp** (WhatsApp Business → Outils → « Listes de diffusion ») : ajoute tes clients. 3 ou 4 fois par an, pas plus, envoie un conseil utile :
```
שלום, כאן רפי המנעולן 🔑 תזכורת קטנה: אם עברתם דירה השנה או איבדתם מפתח – כדאי להחליף צילינדר. אני זמין בכל אזור השרון: 054-530-1389
```
  (Seuls les gens qui ont ton numéro dans leurs contacts reçoivent une liste de diffusion : d'où le bouton « שמרו את המספר » sur le site.)
- **Statut WhatsApp** : poste tes vidéos (section 7) en statut. Tous tes contacts les voient, gratuitement.
- **Commerçants du quartier** (épiceries, quincailleries, gardiens d'immeuble) : laisse 5 cartes. Ce sont eux qu'on interroge quand on est enfermé dehors.

---

## 9. Ce qui tourne tout seul (mis en place le 1er nov. 2026)

- **Contrôle à chaque mise à jour du site** (GitHub Actions) : liens cassés, données pour Google, textes interdits (ex. « יוצא מנתניה », numéro d'un concurrent). En cas d'erreur, la mise à jour est signalée en rouge sur GitHub.
- **Envoi automatique à Bing** (IndexNow) 3 minutes après chaque mise à jour.
- **Surveillance quotidienne** : chaque matin, toutes les pages en ligne sont testées (affichage, numéro présent, cadenas HTTPS valide encore au moins 14 jours). En cas de problème, une alerte s'ouvre dans l'onglet « Issues » du dépôt GitHub, et GitHub t'envoie un e-mail.
- **4 guides pratiques sur le site** (enfermé dehors, changer de cylindre, clé cassée, après un cambriolage) : ils attirent les recherches de gens qui ont le problème **en ce moment**.

---

## 10. Ce que je ne peux pas faire à ta place (et pourquoi)

- Publier, envoyer des messages, payer : c'est en ton nom, ça doit venir de toi.
- Créer la fiche Google Business ou le compte Google Ads : il faut ton compte Google et ta vérification.
- Les manipulations sur Render et sur le DNS du domaine : je n'ai pas d'outil pour le faire. Je te guide en 2 étapes (voir PLAN-CLIENTS.md, section 6).
