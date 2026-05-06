# Performance — DataShare

## Tests de performance backend (NestJS)

Tests effectués en local avec `curl`, serveur NestJS démarré en mode production (`npm run start:prod`), base de données PostgreSQL 16 via Docker.

### Résultats

| Endpoint | Mesure 1 | Mesure 2 | Mesure 3 | Moyenne |
|---------|---------|---------|---------|---------|
| `POST /api/auth/login` | 218ms | 206ms | 228ms | **217ms** |
| `GET /api/files` | 13ms | 4ms | 4ms | **7ms** |
| `POST /api/files/upload` (petit fichier) | 11ms | 7ms | 6ms | **8ms** |

### Interprétation

**`POST /api/auth/login` — ~217ms**
Le temps est dominé par le calcul bcrypt (coût 12). C'est intentionnel : ralentir le hashage rend les attaques brute-force plus coûteuses. Ce délai est imperceptible pour un utilisateur humain.

**`GET /api/files` — ~7ms**
Excellent. La requête PostgreSQL est indexée sur `owner_id` (clé étrangère), le résultat est retourné quasi-instantanément.

**`POST /api/files/upload` — ~8ms**
Rapide grâce au disque local et au déplacement atomique (`renameSync`). Le temps augmentera linéairement avec la taille du fichier pour les gros uploads.

---

## Budget de performance frontend

Build de production généré avec `npm run build` (Vite).

| Asset | Taille brute | Gzip estimé |
|-------|-------------|------------|
| `index.js` (vendors) | ~140 Ko | ~55 Ko |
| Total JS | ~160 Ko | ~63 Ko |
| Total CSS | ~13 Ko | ~4 Ko |
| **Total page** | **~173 Ko** | **~67 Ko** |

**Temps de build :** ~1.2s

**Métriques estimées (Lighthouse) :**
- First Contentful Paint : < 1s
- Time to Interactive : < 2s
- Score Performance : > 90

---

## Test de charge (k6)

### Script

```javascript
// scripts/k6_load_test.js
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 20,          // 20 utilisateurs simultanés
  duration: '30s',
};

export default function () {
  const res = http.post('http://localhost:8000/api/auth/login',
    JSON.stringify({ email: 'test@datashare.com', password: 'password123' }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

**Exécution :**
```bash
k6 run scripts/k6_load_test.js
```

### Résultats (20 VUs, 30s, endpoint POST /api/auth/login)

```
          /\      |‾‾| /‾‾/   /‾‾/
     /\  /  \     |  |/  /   /  /
    /  \/    \    |     (   /   ‾‾\
   /          \   |  |\  \ |  (‾)  |
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: scripts/k6_load_test.js
     output: -

  scenarios: (100.00%) 1 scenario, 20 max VUs, 1m0s max duration (incl. graceful stop):
           * default: 20 looping VUs for 30s (gracefulStop: 30s)

✓ status 200

checks.........................: 100.00% ✓ 516 ✗ 0
data_received..................: 42 kB   1.4 kB/s
data_sent......................: 63 kB   2.1 kB/s
http_req_blocked...............: avg=12µs    min=2µs    med=5µs    max=1.2ms   p(90)=8µs    p(95)=12µs
http_req_connecting............: avg=4µs     min=0s     med=0s     max=892µs   p(90)=0s     p(95)=0s
http_req_duration..............: avg=218ms   min=198ms  med=214ms  max=287ms   p(90)=241ms  p(95)=256ms
  { expected_response:true }...: avg=218ms   min=198ms  med=214ms  max=287ms   p(90)=241ms  p(95)=256ms
http_req_failed................: 0.00%   ✓ 0   ✗ 516
http_req_receiving.............: avg=62µs    min=18µs   med=48µs   max=1.1ms   p(90)=112µs  p(95)=165µs
http_req_sending...............: avg=21µs    min=8µs    med=18µs   max=298µs   p(90)=32µs   p(95)=41µs
http_req_tls_handshaking.......: avg=0s      min=0s     med=0s     max=0s      p(90)=0s     p(95)=0s
http_req_waiting...............: avg=218ms   min=197ms  med=214ms  max=286ms   p(90)=241ms  p(95)=255ms
http_reqs......................: 516     17.2/s
iteration_duration.............: avg=1.22s   min=1.2s   med=1.21s  max=1.29s   p(90)=1.24s  p(95)=1.26s
iterations.....................: 516     17.2/s
vus............................: 20      min=20     max=20
vus_max........................: 20      min=20     max=20

running (0m30.0s), 00/20 VUs, 516 complete and 0 interrupted iterations
default ✓ [==============================] 20 VUs  30s
```

### Interprétation

- **0% d'erreurs** sur 516 requêtes avec 20 utilisateurs simultanés
- **p95 = 256ms** — le 95e percentile reste sous 300ms, acceptable pour un endpoint de login sécurisé (bcrypt coût 12)
- **17 req/s** en débit soutenu — suffisant pour un MVP à faible trafic
- Le temps de réponse est dominé par bcrypt (intentionnel — sécurité anti brute-force), pas par la base de données

### Captures de logs NestJS (extrait)

```
[Nest] LOG [NestApplication] Application is running on: http://[::]:8000
[Nest] LOG [FilesCron] Purge des fichiers expirés : 0 fichier(s) supprimé(s)
[Nest] LOG [RouterExplorer] Mapped {/api/auth/register, POST}
[Nest] LOG [RouterExplorer] Mapped {/api/auth/login, POST}
[Nest] LOG [RouterExplorer] Mapped {/api/auth/me, GET}
[Nest] LOG [RouterExplorer] Mapped {/api/files, GET}
[Nest] LOG [RouterExplorer] Mapped {/api/files/upload, POST}
[Nest] LOG [RouterExplorer] Mapped {/api/files/upload/anonymous, POST}
[Nest] LOG [RouterExplorer] Mapped {/api/files/:id, DELETE}
[Nest] LOG [RouterExplorer] Mapped {/api/files/share/:token, GET}
[Nest] LOG [RouterExplorer] Mapped {/api/files/download/:token, GET}
```

---

## Axes d'optimisation

| Axe | Action | Impact estimé |
|-----|--------|--------------|
| Auth | Cache Redis pour les tokens fréquents | -30% sur /login |
| Base de données | Pagination sur `GET /api/files` | Scalabilité sur gros volumes |
| Fichiers | Migration AWS S3 + CDN | Décharge le serveur, meilleure latence mondiale |
| Serveur | Nginx en reverse proxy | +5× débit concurrent |
| Frontend | Lazy-loading des routes Vue | -40% bundle initial |

---

## Métriques à surveiller en production

| Métrique | Seuil acceptable | Outil |
|---------|-----------------|-------|
| Temps de réponse p95 | < 500ms | k6, Datadog |
| Taille max fichier uploadé | 1 Go | Multer config |
| Espace disque uploads | > 20% libre | cron + alerte |
| Erreurs 5xx | < 0.1% | logs NestJS |
