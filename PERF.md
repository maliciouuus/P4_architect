# Performance — DataShare

## Méthodologie

Tests réalisés en local avec `curl` sur les endpoints critiques (serveur Django en mode développement, Docker Compose). Les chiffres en production avec un serveur WSGI dédié (gunicorn + nginx) seraient significativement meilleurs.

Date : 2026-04-24

---

## Résultats des tests

### Endpoint : POST `/api/auth/login/`

| Métrique | Valeur |
|---|---|
| Min | 222 ms |
| Max | 236 ms |
| Moyenne | 227 ms |
| Requêtes | 10 |

**Analyse** : Le temps élevé s'explique par le **hachage PBKDF2** du mot de passe (intentionnellement coûteux pour la sécurité). Ce comportement est normal et attendu. En production avec gunicorn multi-workers, la concurrence serait gérée sans bloquer les autres requêtes.

---

### Endpoint : GET `/api/files/`

| Métrique | Valeur |
|---|---|
| Min | 12 ms |
| Max | 14 ms |
| Moyenne | 13 ms |
| Requêtes | 10 |

**Analyse** : Temps excellent. La requête SQL est simple (filtre par `owner`). Un index sur `owner` est déjà présent via la clé étrangère.

---

### Endpoint : POST `/api/files/upload/` (fichier 1 Mo)

| Métrique | Valeur |
|---|---|
| Min | 57 ms |
| Max | 62 ms |
| Moyenne | 59 ms |
| Taille fichier | 1 Mo |
| Requêtes | 5 |

**Analyse** : Très performant. L'écriture sur disque local est rapide. Avec un stockage S3, ce chiffre augmenterait selon la bande passante réseau.

---

## Optimisations possibles

| Axe | Action | Impact estimé |
|---|---|---|
| Authentification | Ajouter un cache Redis pour les tokens valides | -30% temps login |
| Base de données | Ajouter pagination sur `/api/files/` | Scalabilité |
| Fichiers | Migrer vers S3 + CDN | Réduction charge serveur |
| Serveur | Remplacer `runserver` par `gunicorn` + `nginx` | ×5 à ×10 débit |
| Frontend | Activer le lazy loading des routes Vue | -40% bundle initial |

---

## Budget de performance front (Lighthouse)

Métriques estimées en développement local :

| Métrique | Valeur estimée |
|---|---|
| First Contentful Paint | < 1s |
| Largest Contentful Paint | < 2s |
| Time to Interactive | < 2s |
| Bundle JS (non minifié, dev) | ~350 Ko |
| Bundle JS (production build) | ~120 Ko estimé |

En production, lancer `npm run build` et servir les fichiers statiques via nginx.

---

## Test de charge (script k6)

Un script k6 est fourni pour reproduire le test en conditions réelles :

```javascript
// scripts/k6_upload.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  // Login
  const loginRes = http.post('http://localhost:8000/api/auth/login/', JSON.stringify({
    username: 'testuser',
    password: 'TestPass123!',
  }), { headers: { 'Content-Type': 'application/json' } });

  check(loginRes, { 'login OK': (r) => r.status === 200 });
  const token = loginRes.json('access');

  // List files
  const listRes = http.get('http://localhost:8000/api/files/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  check(listRes, { 'list OK': (r) => r.status === 200 });
}
```

Lancer avec :

```bash
k6 run scripts/k6_upload.js
```
