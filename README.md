# DataShare — Plateforme de transfert sécurisé de fichiers

Prototype MVP réalisé dans le cadre de la mission **« Pilotez le développement d'une solution informatique »** (OpenClassrooms).

---

## Présentation

DataShare permet à des utilisateurs, anonymes ou enregistrés, de transférer des fichiers via des **liens de téléchargement temporaires**, avec options de protection et de gestion pour les utilisateurs connectés.

**Cible :** freelances et petites entreprises souhaitant partager des fichiers sans dépendre de services tiers.

---

## Fonctionnalités MVP

| US | Fonctionnalité | Statut |
|----|---------------|--------|
| US01 | Upload avec compte | ✅ |
| US02 | Téléchargement via lien unique | ✅ |
| US03 | Création de compte | ✅ |
| US04 | Connexion JWT | ✅ |
| US05 | Historique des fichiers | ✅ |
| US06 | Suppression de fichier | ✅ |
| US07 | Upload anonyme | ✅ |
| US09 | Protection par mot de passe | ✅ |
| US10 | Expiration automatique (cron) | ✅ |

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | NestJS 11 (TypeScript) |
| Frontend | Vue.js 3 + Pinia + Vite |
| Base de données | PostgreSQL 16 |
| Authentification | JWT (7 jours) |
| Stockage | Système de fichiers local |
| Tests | Jest (32 tests unitaires, 78% couverture) + Playwright E2E |
| Déploiement | Docker + Docker Compose |

---

## Prérequis

- **Docker** ≥ 24 et **Docker Compose** ≥ 2.20
- **Node.js** ≥ 20 (développement local uniquement)

---

## Installation rapide (Docker)

```bash
# 1. Cloner le repository
git clone https://github.com/maliciouuus/P4_architect.git
cd P4_architect

# 2. Lancer tous les services
bash start.sh

# 3. Vérifier que tout tourne
docker compose ps
```

**Accès :**
- Frontend : http://localhost:5173
- API : http://localhost:8000/api

---

## Installation en développement local

### Base de données

```bash
docker compose up -d db
```

### Backend NestJS

```bash
cd backend-nest
npm install
npm run start:dev          # Hot-reload sur http://localhost:8000
```

### Frontend Vue.js

```bash
cd frontend
npm install
npm run dev                # http://localhost:5173
```

---

## Variables d'environnement (`backend-nest/.env`)

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `DATABASE_URL` | `postgresql://datashare:datashare@localhost:5433/datashare` | Connexion PostgreSQL |
| `JWT_SECRET` | `change_me_in_production` | Clé de signature JWT — **à changer en production** |
| `MAX_FILE_SIZE` | `1073741824` | Taille max en octets (1 Go) |
| `SHARE_LINK_EXPIRY_HOURS` | `168` | Durée de validité du lien (7 jours) |
| `UPLOAD_DIR` | `uploads` | Dossier de stockage |
| `PORT` | `8000` | Port NestJS |
| `FRONTEND_URL` | `http://localhost:5173` | URL frontend (CORS + liens de partage) |

---

## Scripts de lancement

```bash
bash start.sh       # Démarre les 3 services Docker
bash stop.sh        # Arrête proprement
bash test_unit.sh   # 32 tests unitaires + rapport couverture
bash test_e2e.sh    # 11 scénarios E2E Playwright (app doit tourner)
```

## Tests

```bash
cd backend-nest
npm test            # 32 tests unitaires
npm run test:cov    # Rapport de couverture (78% global)

# Tests E2E (nécessite bash start.sh avant)
cd ../e2e
source venv/bin/activate
pytest -v           # 11 scénarios Playwright
```

---

## Structure du projet

```
P4_architect/
├── backend-nest/          # API NestJS (TypeScript)
│   ├── src/auth/          # Authentification (JWT, bcrypt)
│   ├── src/files/         # Fichiers (upload, download, cron purge)
│   └── Dockerfile
├── frontend/              # Vue.js 3 + Pinia
│   ├── src/stores/        # État global (auth, files)
│   ├── src/views/         # Pages (Home, Login, Register, Dashboard, Upload, Download)
│   └── Dockerfile
├── docs/                  # Documentation technique PDF, OpenAPI, Postman, présentation
├── scripts/               # setup_db.sql, génération docs
├── e2e/                   # Tests Playwright (Python)
├── start.sh / stop.sh     # Scripts de lancement/arrêt
├── test_unit.sh / test_e2e.sh  # Scripts de test
├── TESTING.md / SECURITY.md / PERF.md / MAINTENANCE.md
└── docker-compose.yml
```

---

## API — Endpoints principaux

| Méthode | Route | Auth | Description |
|---------|-------|------|-------------|
| POST | `/api/auth/register` | ❌ | Créer un compte |
| POST | `/api/auth/login` | ❌ | Se connecter (JWT) |
| GET | `/api/auth/me` | ✅ | Profil utilisateur |
| GET | `/api/files` | ✅ | Historique des fichiers |
| POST | `/api/files/upload` | ✅ | Upload fichier |
| POST | `/api/files/upload/anonymous` | ❌ | Upload anonyme |
| DELETE | `/api/files/:id` | ✅ | Supprimer un fichier |
| GET | `/api/files/share/:token` | ❌ | Infos publiques |
| GET | `/api/files/download/:token` | ❌ | Télécharger |

---

## Documentation

- [Documentation technique (PDF)](docs/documentation_technique_v2.pdf)
- [Présentation investisseurs (PPTX)](docs/presentation_datashare_v2.pptx)
- [TESTING.md](TESTING.md) · [SECURITY.md](SECURITY.md) · [PERF.md](PERF.md) · [MAINTENANCE.md](MAINTENANCE.md)
