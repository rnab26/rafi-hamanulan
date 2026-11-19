# Consigne : brancher Google Search Console sur Claude (session LOCALE sur le PC de Rafi)

Pourquoi en local : l'outil (`mcp-server-gsc`, npm, licence MIT) a besoin d'un fichier de clé Google sur la machine qui le fait tourner. Une session cloud ne peut pas le garder de façon sûre ; le PC de Rafi, si.

À coller dans une session Claude Code locale (appli de bureau → Claude Code → nouvelle session dans « claude-taches »), Chrome connecté au compte refamanoulan@gmail.com :

---

Branche Google Search Console sur Claude Code, sur ce PC, pour le site rafihamanulan.co.il. Utilise Chrome (compte refamanoulan@gmail.com déjà connecté) pour les étapes web. Montre-moi un récapitulatif avant chaque étape qui crée quelque chose. Ne dépense rien : tout doit rester dans l'offre gratuite de Google Cloud (pas de carte bancaire, pas d'essai payant).

1. Google Cloud Console (https://console.cloud.google.com/) : crée un projet nommé « rafi-search-console ».
2. Active l'API « Google Search Console API » dans ce projet (APIs & Services → Library).
3. APIs & Services → Credentials → Create credentials → Service account, nom « claude-gsc », aucun rôle de projet. Puis Keys → Add key → JSON. Enregistre le fichier dans `%USERPROFILE%\.secrets\gsc-rafi.json` (crée le dossier). Ce fichier est un secret : ne le mets dans aucun dépôt git, ne l'affiche pas, ne le colle nulle part.
4. Search Console (https://search.google.com/search-console), propriété « rafihamanulan.co.il » (type Domaine) → Paramètres → Utilisateurs et autorisations → Ajouter un utilisateur : l'e-mail du compte de service (…@rafi-search-console.iam.gserviceaccount.com), autorisation « Restreint » (lecture seule suffit).
5. Ajoute l'outil à Claude Code pour mon utilisateur :
   `claude mcp add gsc --scope user -e GOOGLE_APPLICATION_CREDENTIALS=%USERPROFILE%\.secrets\gsc-rafi.json -- npx -y mcp-server-gsc`
6. Test : relance Claude Code, puis appelle l'outil `search_analytics` avec `siteUrl` = `sc-domain:rafihamanulan.co.il`, les 28 derniers jours, dimensions `query`. Dis-moi s'il répond (même avec peu ou pas de données : le site est récent, c'est normal).
7. Écris le résultat (réussi ou l'erreur exacte) dans le fil du projet rnab26/rafi-hamanulan : ajoute une ligne datée dans CLAUDE.md, section « À faire plus tard », sans jamais y mettre le contenu de la clé.
