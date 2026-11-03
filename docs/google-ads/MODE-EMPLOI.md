# Google Ads – mode d'emploi (préparé le 3 nov. 2026)

Tout est prêt. La campagne s'importe **en pause** : elle ne dépensera rien tant que tu ne l'actives pas toi-même.

- `campagne.csv` : la campagne complète, à importer en un seul fichier (17 groupes d'annonces : général, ouverture de porte, cylindre, coffres, plus un groupe par ville avec sa propre page).
- `campagne-lisible.md` : la même chose, lisible, pour vérifier les textes.
- Pour modifier quelque chose (mot-clé, titre, ville) : dis-le-moi, je change `_build/ads.py` et je régénère.

## 1. Créer le compte (10 min, une seule fois)
1. Va sur https://ads.google.com et connecte-toi avec le même compte Google que ta fiche Google Business.
2. Quand Google propose de créer une campagne guidée, cherche le lien **« Passer en mode Expert »** (ou « Créer un compte sans campagne »). Sinon, Google crée une campagne automatique qu'on ne contrôle pas.
3. **Pays : Israël. Fuseau horaire : Jérusalem. Devise : ILS (₪).** Ces 3 choix sont **définitifs**, vérifie-les.
4. Moyen de paiement : Google le demande pour activer. Rien n'est prélevé tant que la campagne est en pause.

## 2. Importer la campagne (2 min)
1. Dans Google Ads : **Outils** (clé à molette) → **Actions groupées** → **Importations**.
2. **+** → choisis le fichier `campagne.csv` (télécharge-le depuis GitHub : `docs/google-ads/campagne.csv` → bouton « Download raw file »).
3. **Aperçu** → vérifie qu'il n'y a pas d'erreur → **Appliquer**.
4. Le format est celui de Google Ads Editor. Je ne l'ai pas testé sur ton compte : si Google refuse une colonne, envoie-moi une capture et je corrige le fichier.

## 3. Les 5 réglages à faire à la main dans la campagne (5 min)
Ouvre la campagne « רפי המנעולן – חיפוש » → **Paramètres** :
1. **Réseaux** : décoche « Réseau Display » et « Partenaires du Réseau de Recherche ».
2. **Zones** : ajoute une par une : קיסריה, חדרה, אור עקיבא, נתניה, כפר יונה, אבן יהודה, קדימה-צורן, תל מונד, פרדסיה, כפר סבא, רעננה, הרצליה, הוד השרון. Dans « Options de zone », choisis **Présence : personnes qui se trouvent dans vos zones**.
3. **Langues** : hébreu et anglais.
4. **Calendrier de diffusion** : dimanche → jeudi toute la journée ; vendredi 09:00–16:00 ; samedi 19:00–24:00.
5. **Composants → Appel** : ajoute `054-530-1389`. Un bouton « appeler » apparaîtra sous l'annonce sur mobile.

## 4. Compter les appels venus de la pub (5 min) – sans ça on paie à l'aveugle
1. **Objectifs** → **Conversions** → **+ Nouvelle action de conversion** → **Site Web** → saisis `rafihamanulan.co.il`.
2. Crée **manuellement** 2 conversions de type **« Contact »** :
   - nom : `Clic sur appel`
   - nom : `Clic WhatsApp`
3. Pour chacune, choisis « Configurer la balise vous-même ». Google affiche un code avec `send_to: 'AW-XXXXXXXXX/YYYYYYY'`.
4. **Envoie-moi ces 2 lignes `send_to`** (ce ne sont pas des secrets : elles sont visibles dans le code de n'importe quel site). Je les ajoute au site (`GADS_ID`, `GADS_LABEL_CALL`, `GADS_LABEL_WA` dans `_build/build.py`). Le suivi est déjà programmé et testé : chaque clic sur « התקשרו » ou « וואטסאפ » sera compté.
5. Les appels passés directement depuis le bouton de l'annonce sont comptés tout seuls par Google.

## 5. Activer (quand TU le décides)
1. Fixe ton **budget par jour** : Campagne → Paramètres → Budget. La valeur de 50 ₪ dans le fichier est une valeur d'attente, pas une recommandation : c'est toi qui choisis.
2. Passe la campagne de « En pause » à **« Activée »**.
3. Les 7 premiers jours, chaque soir : **Mots-clés → Termes de recherche**. Tout ce qui n'est pas un client (cours, emploi, voiture…) → **Ajouter comme mot-clé à exclure**. Ou envoie-moi une capture, je te dis quoi exclure.
4. Après une semaine : on compare le coût total au nombre d'appels et de chantiers, puis on décide : continuer, ajuster ou arrêter.

## À vérifier (non vérifié)
- Le prix d'un clic sur « מנעולן » dans ta zone : inconnu, on le mesure pendant la semaine de test.
- Vie privée : la balise Google Ads dépose des cookies. La loi israélienne sur la vie privée (amendement 13) peut demander une mention sur le site. À vérifier avant d'activer la balise ; je peux ajouter une courte page « מדיניות פרטיות » si tu veux.
