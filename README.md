# DataShare — Plateforme de transfert sécurisé de fichiers

Prototype MVP réalisé dans le cadre de la mission **« Pilotez le développement d'une solution informatique »** (OpenClassrooms).

---

## Présentation

**DataShare** permet aux freelances et petites entreprises d'envoyer des fichiers simplement et de générer des **liens de téléchargement à durée limitée**, sans dépendance à des services tiers.

### Fonctionnalités MVP

- Création de compte et connexion (JWT)
- Upload de fichiers (max 50 Mo)
- Génération d'un lien de téléchargement unique avec expiration configurable
- Historique des fichiers envoyés
- Suppression manuelle d'un fichier
- Page de téléchargement publique avec affichage de l'état du lien (valide / expiré)

---

## Stack technique

| Composant | Technologie |
|---|---|
| Back-end | Django 5.2 + Django REST Framework |
| Authentification | JWT (djangorestframework-simplejwt) |
| Front-end | Vue.js 3 + Vite + Pinia |
| Base de données | PostgreSQL 16 |
| Stockage fichiers | Disque local (`/media/`) |
| Containerisation | Docker + Docker Compose |

---

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/) ≥ 2.18

---

## Installation et lancement

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd P4_architect

# 2. Lancer tous les services
docker compose up -d

# 3. Vérifier que tout tourne
docker compose ps
```

L'application est disponible sur :
- **Frontend** : http://localhost:5173
- **API** : http://localhost:8000/api/
- **Admin Django** : http://localhost:8000/admin/

Les migrations sont appliquées automatiquement au démarrage.

---

## Variables d'environnement

Le fichier `docker-compose.yml` contient des valeurs par défaut pour le développement. En production, surcharger via un fichier `.env` :

| Variable | Description | Défaut |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clé secrète Django | `dev-secret-key-change-in-production` |
| `DEBUG` | Mode debug | `True` |
| `DB_NAME` | Nom de la base | `datashare` |
| `DB_USER` | Utilisateur BDD | `datashare` |
| `DB_PASSWORD` | Mot de passe BDD | `datashare` |
| `DB_HOST` | Hôte BDD | `db` |
| `CORS_ALLOWED_ORIGINS` | Origines autorisées | `http://localhost:5173` |
| `SHARE_LINK_EXPIRY_HOURS` | Durée de validité des liens (heures) | `24` |

---

## Créer un compte administrateur

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## Structure du projet

```
P4_architect/
├── backend/                  # Django + DRF
│   ├── accounts/             # App authentification
│   ├── files/                # App gestion fichiers
│   ├── datashare/            # Settings, URLs
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Vue.js 3
│   ├── src/
│   │   ├── views/            # Pages (Home, Login, Register, Dashboard, Download)
│   │   ├── stores/           # Pinia (auth, files)
│   │   ├── api/              # Client Axios
│   │   └── router/           # Vue Router
│   └── Dockerfile
├── docs/                     # Documentation
├── docker-compose.yml
└── README.md
```

---

## Lancer les tests

```bash
cd backend
venv/bin/pytest
```

Rapport de couverture HTML généré dans `backend/htmlcov/index.html`.

Résultats actuels : **30 tests, 99% de couverture**.

---

## API — Endpoints principaux

| Méthode | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/auth/register/` | Créer un compte | Non |
| POST | `/api/auth/login/` | Connexion (JWT) | Non |
| POST | `/api/auth/token/refresh/` | Rafraîchir le token | Non |
| GET | `/api/auth/me/` | Profil utilisateur | Oui |
| GET | `/api/files/` | Liste de mes fichiers | Oui |
| POST | `/api/files/upload/` | Uploader un fichier | Oui |
| DELETE | `/api/files/<id>/delete/` | Supprimer un fichier | Oui |
| GET | `/api/files/share/<token>/` | Infos publiques du fichier | Non |
| GET | `/api/files/download/<token>/` | Télécharger un fichier | Non |

La spec OpenAPI complète est disponible dans [`docs/openapi.yaml`](docs/openapi.yaml).

---

## Qualité et maintenance

| Fichier | Contenu |
|---|---|
| [`TESTING.md`](TESTING.md) | Plan de tests, résultats, coverage |
| [`SECURITY.md`](SECURITY.md) | Scan de sécurité, décisions |
| [`PERF.md`](PERF.md) | Tests de performance, métriques |
| [`MAINTENANCE.md`](MAINTENANCE.md) | Procédures de mise à jour |

---

## Arrêter les services

```bash
docker compose down          # Arrêter sans supprimer les données
docker compose down -v       # Arrêter et supprimer les volumes (⚠ supprime les fichiers)
```
