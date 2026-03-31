# Plan de tests — DataShare

## Résumé

| Indicateur | Valeur |
|---|---|
| Tests totaux | 30 |
| Tests passants | 30 ✅ |
| Tests échoués | 0 |
| Couverture globale | 99% |
| Seuil cible | 70% |

---

## Plan de tests

| Fonctionnalité | Type | Cas testés | Critère d'acceptation |
|---|---|---|---|
| Inscription | Unitaire | Succès, mot de passe faible, doublon, mots de passe différents | HTTP 201 si valide, 400 sinon |
| Connexion | Unitaire | Succès, mauvais mot de passe, utilisateur inconnu | HTTP 200 + tokens si valide, 401 sinon |
| Profil `/me/` | Unitaire | Authentifié, non authentifié | HTTP 200 avec données, 401 sinon |
| Liste fichiers | Unitaire | Vide, isolation par utilisateur | Seuls les fichiers de l'utilisateur retournés |
| Upload fichier | Unitaire | Succès, trop grand, pas de fichier, token généré | HTTP 201 si valide, 400/413 sinon |
| Suppression | Unitaire | Propre fichier, fichier d'autrui | 204 si propriétaire, 404 sinon |
| Téléchargement | Unitaire | Valide, expiré, token invalide, sans auth | 200 si valide, 410 si expiré, 404 si inconnu |
| Infos publiques | Unitaire | Valide, expiré, introuvable | Données publiques retournées sans auth |
| Modèle `SharedFile` | Unitaire | `is_expired` vrai/faux, `__str__` | Comportement conforme |

---

## Lancer les tests

```bash
cd backend
venv/bin/pytest
```

Pour la couverture seule :

```bash
venv/bin/pytest --cov=accounts --cov=files --cov-report=html:htmlcov
# Rapport HTML : backend/htmlcov/index.html
```

---

## Rapport de couverture

```
Name                               Stmts   Miss  Cover
------------------------------------------------------
accounts/serializers.py               21      0   100%
accounts/views.py                     10      0   100%
accounts/urls.py                       4      0   100%
files/models.py                       28      1    96%
files/serializers.py                  21      0   100%
files/views.py                        48      0   100%
files/urls.py                          3      0   100%
------------------------------------------------------
TOTAL                                348      1    99%
```

La seule ligne non couverte est une branche défensive dans `SharedFile.save()` (cas `expires_at` déjà défini à la création).

---

## Tests d'intégration et E2E

Les tests pytest couvrent les appels HTTP de bout en bout via `APIClient` (Django REST Framework), ce qui constitue des tests d'intégration réels contre une base SQLite en mémoire.

Des tests E2E complémentaires (navigateur) peuvent être ajoutés avec **Playwright** ou **Cypress** pour couvrir les flux UI.

---

## Exécution dans Docker

```bash
docker compose exec backend pytest
```
