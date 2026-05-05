# Plan de tests — DataShare

## Résumé

| Indicateur | Valeur |
|---|---|
| Tests unitaires + intégration | 38 ✅ |
| Tests E2E (Playwright) | 10 ✅ |
| Tests échoués | 0 |
| Couverture de code | 99% |
| Seuil cible | 70% |

---

## Plan de tests

### Tests unitaires et d'intégration (pytest)

| Fonctionnalité | Type | Cas testés | Critère d'acceptation |
|---|---|---|---|
| Inscription | Unitaire | Succès, mot de passe faible, doublon, mots de passe différents | HTTP 201 si valide, 400 sinon |
| Connexion | Unitaire | Succès, mauvais mot de passe, utilisateur inconnu | HTTP 200 + tokens si valide, 401 sinon |
| Profil `/me/` | Unitaire | Authentifié, non authentifié | HTTP 200 avec données, 401 sinon |
| Liste fichiers | Unitaire | Vide, isolation par utilisateur, flag protégé | Seuls les fichiers du propriétaire retournés |
| Upload fichier | Unitaire | Succès, trop grand, sans fichier, avec MDP, expiration custom | HTTP 201 si valide, 400/413 sinon |
| Suppression | Unitaire | Propre fichier, fichier d'autrui | 204 si propriétaire, 404 sinon |
| Téléchargement | Unitaire | Valide, expiré, token invalide, MDP correct/incorrect | 200 si valide, 403/410/404 sinon |
| Infos publiques | Unitaire | Valide, expiré, protégé, introuvable | Données publiques sans auth |
| Modèle `SharedFile` | Unitaire | `is_expired`, `is_password_protected`, hachage, `__str__` | Comportement conforme |

### Tests E2E — Playwright (navigateur Chromium réel)

| Scénario | Parcours testé | Critère d'acceptation |
|---|---|---|
| Page d'accueil | Affichage tagline + icône | Éléments visibles |
| Inscription | Remplissage formulaire → redirection dashboard | URL `/dashboard` atteinte |
| Connexion réussie | Login valide → dashboard | Dashboard affiché |
| Mauvais mot de passe | Login invalide → message d'erreur | Message "Identifiants incorrects" visible |
| Déconnexion | Clic déconnexion → retour login | URL `/login` atteinte |
| Redirection non-auth | Accès `/dashboard` sans token | Redirection vers `/login` |
| Upload fichier | Sélection fichier → téléverser → lien généré | URL `/download/` présente dans le lien |
| Lien de partage | Navigation vers lien → page téléchargement | "Télécharger un fichier" visible |
| Fichier dans la liste | Après upload → fichier dans `.file-row` | Au moins 1 ligne visible |
| Suppression | Clic supprimer → confirmer → fichier retiré | Comptage -1 après suppression |

---

## Lancer les tests

### Tests unitaires et d'intégration

```bash
cd backend
venv/bin/pytest
```

Rapport de couverture HTML généré dans `backend/htmlcov/index.html`.

### Tests E2E

```bash
# Prérequis : application lancée
docker compose up -d

# Lancer les tests E2E
e2e/venv/bin/pytest e2e/ --browser chromium -v --base-url http://localhost:5173
```

---

## Rapport de couverture (backend)

```
Name                               Stmts   Miss  Cover
------------------------------------------------------
accounts/serializers.py               21      0   100%
accounts/views.py                     14      0   100%
files/models.py                       33      0   100%
files/serializers.py                  23      0   100%
files/views.py                        64      0   100%
------------------------------------------------------
TOTAL                                395      1    99%
```

---

## Exécution dans Docker

```bash
docker compose exec backend pytest
```
