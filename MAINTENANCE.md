# Maintenance — DataShare

## Mise à jour des dépendances

### Fréquence recommandée

| Type de mise à jour | Fréquence | Risque |
|---|---|---|
| Correctifs de sécurité | Immédiatement après publication | Faible si testé |
| Mises à jour mineures | Mensuelle | Faible |
| Mises à jour majeures | Trimestrielle après évaluation | Moyen à élevé |

### Procédure backend (Python)

```bash
cd backend

# 1. Vérifier les vulnérabilités
venv/bin/pip-audit

# 2. Voir les mises à jour disponibles
venv/bin/pip list --outdated

# 3. Mettre à jour une dépendance
venv/bin/pip install --upgrade django

# 4. Figer les versions
venv/bin/pip freeze > requirements.txt

# 5. Lancer les tests
venv/bin/pytest

# 6. Rebuilder l'image Docker
docker compose build backend
```

### Procédure frontend (Node.js)

```bash
cd frontend

# 1. Voir les mises à jour disponibles
npm outdated

# 2. Mettre à jour (mineures et patches)
npm update

# 3. Mettre à jour une dépendance majeure
npm install vue@latest

# 4. Vérifier
npm run build
```

---

## Migrations de base de données

```bash
# Créer une migration après modification d'un modèle
docker compose exec backend python manage.py makemigrations

# Appliquer les migrations
docker compose exec backend python manage.py migrate

# Voir l'état des migrations
docker compose exec backend python manage.py showmigrations
```

⚠ Toujours tester les migrations sur une copie de la base avant de les appliquer en production.

---

## Sauvegardes

### Base de données

```bash
# Export
docker compose exec db pg_dump -U datashare datashare > backup_$(date +%Y%m%d).sql

# Restauration
cat backup_20260424.sql | docker compose exec -T db psql -U datashare datashare
```

### Fichiers uploadés

```bash
# Sauvegarder le volume media
docker run --rm \
  -v p4_architect_media_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/media_$(date +%Y%m%d).tar.gz /data
```

---

## Surveillance et logs

```bash
# Voir les logs en temps réel
docker compose logs -f backend

# Logs des dernières 100 lignes
docker compose logs --tail=100 backend

# État des services
docker compose ps
```

---

## Redémarrage des services

```bash
# Redémarrer un service spécifique
docker compose restart backend

# Redémarrer tous les services
docker compose restart

# Arrêt complet et redémarrage
docker compose down && docker compose up -d
```

---

## Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Rupture d'API Django 6.x | Moyen | Élevé | Tester sur branche dédiée avant maj majeure |
| Incompatibilité Vue 4 | Faible | Moyen | Rester sur Vue 3 LTS jusqu'à stabilisation |
| Saturation disque (fichiers) | Moyen | Élevé | Tâche cron de nettoyage des fichiers expirés |
| Fuite de token JWT | Faible | Élevé | Passer en httpOnly cookie en production |

---

## Nettoyage des fichiers expirés

Les fichiers expirés restent en base et sur disque jusqu'à suppression manuelle. Ajouter une commande de gestion Django pour automatiser le nettoyage :

```bash
# À créer : backend/files/management/commands/cleanup_expired.py
docker compose exec backend python manage.py cleanup_expired
```

En production, planifier via cron :

```cron
0 2 * * * docker compose exec -T backend python manage.py cleanup_expired
```
