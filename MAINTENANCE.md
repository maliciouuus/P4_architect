# Maintenance — DataShare

## Mise à jour des dépendances

### Fréquence recommandée

| Type de mise à jour | Fréquence | Risque |
|--------------------|-----------|--------|
| Correctifs de sécurité (patch) | Immédiat après publication | Faible — corrections ciblées |
| Mises à jour mineures (minor) | Mensuelle | Faible — compatibilité garantie par semver |
| Mises à jour majeures (major) | Trimestrielle après évaluation | Élevé — peut casser l'API |

### Procédure backend (NestJS)

```bash
cd backend-nest

# 1. Vérifier les vulnérabilités
npm audit

# 2. Voir les packages obsolètes
npm outdated

# 3. Mettre à jour les mises à jour mineures/patch
npm update

# 4. Mettre à jour un package majeur (ex: NestJS)
npm install @nestjs/core@latest @nestjs/common@latest

# 5. Relancer les tests pour détecter les régressions
npm test

# 6. Reconstruire l'image Docker
docker compose build backend
docker compose up -d backend
```

### Procédure frontend (Vue.js)

```bash
cd frontend

# 1. Voir les packages obsolètes
npm outdated

# 2. Mettre à jour les mises à jour mineures/patch
npm update

# 3. Mettre à jour Vue ou Vite (major)
npm install vue@latest vite@latest

# 4. Vérifier que le build fonctionne
npm run build

# 5. Tester manuellement les flows critiques (login, upload, download)
npm run dev
```

---

## Gestion de la base de données

### Migrations TypeORM

En développement, `synchronize: true` dans `app.module.ts` met à jour le schéma automatiquement. **En production**, désactiver et utiliser des migrations explicites :

```bash
# Générer une migration
npx typeorm migration:generate -d src/data-source.ts src/migrations/NomMigration

# Appliquer les migrations
npx typeorm migration:run -d src/data-source.ts

# Annuler la dernière migration
npx typeorm migration:revert -d src/data-source.ts
```

### Sauvegardes

```bash
# Sauvegarde de la base de données
docker compose exec db pg_dump -U datashare datashare > backup_$(date +%Y%m%d).sql

# Restauration
cat backup_20260505.sql | docker compose exec -T db psql -U datashare datashare

# Sauvegarde des fichiers uploadés (volume Docker)
docker run --rm -v p4_architect_uploads_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/uploads_$(date +%Y%m%d).tar.gz /data
```

---

## Surveillance et logs

```bash
# Logs en temps réel
docker compose logs -f backend

# Dernières 100 lignes
docker compose logs --tail=100 backend

# État des services
docker compose ps

# Utilisation disque des volumes
docker system df -v
```

### Purge des fichiers expirés (US10)

La purge est automatique — le `FilesCron` s'exécute toutes les 24h après le démarrage du serveur. Elle est loggée dans la console NestJS :

```
[FilesCron] Purge des fichiers expirés : 3 fichier(s) supprimé(s)
```

Pour déclencher manuellement via l'API (debug) :
```bash
# Appel interne possible si un endpoint admin est ajouté en production
curl -X POST http://localhost:8000/api/admin/purge -H "Authorization: Bearer <ADMIN_TOKEN>"
```

---

## Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|------------|
| NestJS 12 — breaking changes | Moyen | Haut | Tester sur branche dédiée avant mise à jour |
| Vue 4 — changements API | Faible | Moyen | Rester sur Vue 3 LTS jusqu'à stabilisation |
| Saturation disque (fichiers) | Moyen | Haut | Cron de purge actif + monitoring espace disque |
| JWT_SECRET exposé | Faible | Critique | Rotation du secret + variables d'env sécurisées |
| PostgreSQL major upgrade (17) | Faible | Moyen | Tester la compatibilité TypeORM avant migration |
| Vulnérabilité bcrypt | Très faible | Critique | `npm audit` hebdomadaire, alerte GitHub Dependabot |

---

## Checklist avant mise en production

- [ ] Changer `JWT_SECRET` (clé longue et aléatoire)
- [ ] Passer `synchronize: false` dans TypeORM, activer les migrations
- [ ] Configurer un reverse proxy Nginx avec HTTPS
- [ ] Remplacer `localStorage` par cookies `httpOnly`
- [ ] Activer le rate limiting sur `/api/auth/*`
- [ ] Configurer les sauvegardes automatiques (cron pg_dump)
- [ ] Mettre en place Dependabot ou Renovate pour les alertes de sécurité
- [ ] Migrer le stockage vers S3 pour la scalabilité
