# Consigne à coller dans Claude in Chrome (sur ordinateur)

Préparation : ouvre Chrome sur ton ordinateur, connecté au compte Google de ta fiche Google Business. Télécharge d'abord `campagne.csv` :
https://github.com/rnab26/rafi-hamanulan/raw/main/docs/google-ads/campagne.csv
Puis ouvre Claude in Chrome et colle tout le bloc ci-dessous.

```
Tu configures Google Ads pour mon entreprise « רפי המנעולן » (serrurier, Israël). Site : https://rafihamanulan.co.il
Règles absolues :
- Ne JAMAIS activer une campagne ni fixer un budget : tout reste EN PAUSE.
- Ne JAMAIS saisir de moyen de paiement : si Google le demande, arrête-toi et demande-moi de le faire.
- Si un écran ne correspond pas à ces étapes, arrête-toi et décris-moi ce que tu vois.

Étapes :
1. Va sur https://ads.google.com. Si un assistant de campagne guidée s'ouvre, choisis « Passer en mode Expert » / « Créer un compte sans campagne ».
2. Paramètres du compte : pays Israël, fuseau horaire (GMT+02:00) Jérusalem, devise ILS. Avant de valider, montre-moi ces 3 valeurs et attends mon OK (elles sont définitives).
3. Outils → Actions groupées → Importations → importe le fichier campagne.csv que j'ai téléchargé → Aperçu → s'il n'y a pas d'erreur, Appliquer. S'il y a des erreurs, recopie-les-moi.
4. Ouvre la campagne « רפי המנעולן – חיפוש » → Paramètres :
   a. Réseaux : décoche Réseau Display et Partenaires du Réseau de Recherche.
   b. Zones : ajoute קיסריה, חדרה, אור עקיבא, נתניה, כפר יונה, אבן יהודה, קדימה-צורן, תל מונד, פרדסיה, כפר סבא, רעננה, הרצליה, הוד השרון. Options de zone : « Présence : personnes qui se trouvent dans vos zones ».
   c. Langues : hébreu et anglais.
   d. Calendrier : dimanche à jeudi toute la journée ; vendredi 09:00–16:00 ; samedi 19:00–24:00.
   e. Composants → Appel : 054-530-1389, pays Israël.
5. Objectifs → Conversions → Nouvelle action de conversion → Site Web → rafihamanulan.co.il → crée manuellement 2 conversions de catégorie « Contact » : « Clic sur appel » et « Clic WhatsApp ». Pour chacune, choisis « Configurer la balise vous-même » et recopie-moi la valeur send_to complète (format AW-XXXXXXXXX/YYYYYYY).
6. Termine par un résumé : ce qui est fait, ce qui a échoué, les 2 valeurs send_to. Rappelle que la campagne est EN PAUSE.
```

Ensuite : envoie-moi les 2 valeurs `send_to` dans la conversation Claude Code ; je les mets sur le site et je vérifie le suivi en ligne.
