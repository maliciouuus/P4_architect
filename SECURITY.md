# Sécurité — DataShare

## Authentification

- **JWT** (JSON Web Tokens) via `djangorestframework-simplejwt`
- Access token : durée de vie **1 heure**
- Refresh token : durée de vie **7 jours**, rotation activée
- Tokens stockés en `localStorage` côté client (acceptable pour un prototype)
- Le refresh est automatiquement tenté par l'intercepteur Axios si le token est expiré

## Gestion des accès

- Tous les endpoints `/api/files/` requièrent un token JWT valide sauf :
  - `GET /api/files/share/<token>/` — infos publiques (pas de données sensibles)
  - `GET /api/files/download/<token>/` — téléchargement public via lien opaque
- Isolation stricte : un utilisateur ne peut voir/supprimer que ses propres fichiers (filtrage par `owner=request.user`)
- Les tokens de partage sont des **UUID v4** (128 bits d'entropie), non devinables

## Sécurisation des fichiers

- Les fichiers sont stockés dans `MEDIA_ROOT` avec un chemin `uploads/<user_id>/<uuid>_<filename>`
- En production : le serveur web (nginx) devrait servir les fichiers statiques, pas Django
- Limite de taille : **50 Mo** par fichier (validée côté serveur et côté client)
- Expiration automatique : les liens expirent après 24h par défaut (configurable)

## Mots de passe

- Hachage via **PBKDF2 + SHA-256** (défaut Django)
- Validateurs actifs : longueur minimale, mots courants, similarité avec le nom d'utilisateur, numérique seul

## CORS

- Origines autorisées configurées explicitement (pas de wildcard `*`)
- En développement : `http://localhost:5173` uniquement

## En-têtes de sécurité

Django active par défaut :
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- Protection CSRF (pas applicable pour une API JWT pure)

## Scan de sécurité des dépendances

Outil utilisé : **pip-audit**

```bash
venv/bin/pip-audit
```

### Résultats (2026-04-24)

| Package | Version | CVE | Correction | Décision |
|---|---|---|---|---|
| pip | 21.3.1 | PYSEC-2023-228, CVE-2025-8869, CVE-2026-1703 | 26.0 | Accepté — pip est un outil de build, non exposé en prod |
| setuptools | 59.6.0 | PYSEC-2022-43012, PYSEC-2025-49, CVE-2024-6345 | 78.1.1 | Accepté — outil de build uniquement, non exposé |

**Aucune vulnérabilité dans les dépendances applicatives** (Django, DRF, simplejwt, psycopg2, Pillow, corsheaders).

Les vulnérabilités détectées concernent uniquement `pip` et `setuptools` du système hôte, qui ne sont pas présents dans l'image Docker de production.

### Vérification dans le container

```bash
docker compose exec backend pip-audit
```

## Points d'amélioration pour la production

- [ ] Passer les tokens en `httpOnly cookies` pour éviter le vol par XSS
- [ ] Activer HTTPS (certificat TLS via Let's Encrypt)
- [ ] Rate limiting sur les endpoints d'authentification (ex. `django-ratelimit`)
- [ ] Configurer `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`
- [ ] Stocker les fichiers sur S3 ou équivalent (pas le disque local)
- [ ] Scanner les fichiers uploadés avec un antivirus (ex. ClamAV)
