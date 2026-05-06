# Sécurité — DataShare

## Scan de sécurité des dépendances

### Commande exécutée

```bash
cd backend-nest
npm audit
```

### Résultat (Mai 2026)

```
found 0 vulnerabilities
```

**Aucune vulnérabilité détectée** dans les dépendances de production NestJS.

### Analyse

| Dépendance | Version | Statut |
|-----------|---------|--------|
| @nestjs/core | 11.x | ✅ Aucune CVE connue |
| @nestjs/jwt | 11.x | ✅ Aucune CVE connue |
| passport-jwt | 4.x | ✅ Aucune CVE connue |
| bcrypt | 6.x | ✅ Aucune CVE connue |
| typeorm | 0.3.x | ✅ Aucune CVE connue |
| pg (PostgreSQL driver) | 8.x | ✅ Aucune CVE connue |
| class-validator | 0.15.x | ✅ Aucune CVE connue |
| multer | 2.x | ✅ Aucune CVE connue |

---

## Authentification JWT

**Décisions prises :**

- Tokens signés HMAC-SHA256 avec clé secrète en variable d'environnement (jamais en dur dans le code)
- Durée de vie : **7 jours** — adapté à un prototype pour le confort utilisateur
- Stockage côté client : `localStorage` — acceptable pour un MVP, à remplacer par cookies `httpOnly` en production
- Validation à chaque requête via `passport-jwt` + `JwtAuthGuard`
- Le payload JWT contient uniquement `{ sub: userId, email }` — données minimales

**Risque identifié :** `localStorage` est accessible par JavaScript (vulnérable aux XSS). En production, utiliser des cookies `httpOnly; Secure; SameSite=Strict`.

---

## Hashage des mots de passe

- Bibliothèque : **bcrypt** avec coût **12**
- Les mots de passe utilisateurs et les mots de passe de fichiers sont hashés de la même façon
- Aucun mot de passe n'est jamais retourné dans les réponses API
- En cas de mauvais identifiants, le message d'erreur est identique qu'il s'agisse de l'email ou du mot de passe — évite l'énumération des comptes

---

## Contrôle d'accès

**Isolation stricte des données :**
- `GET /api/files` filtre par `ownerId = req.user.id` — un utilisateur ne voit jamais les fichiers d'un autre
- `DELETE /api/files/:id` cherche `{ id, ownerId }` — retourne 404 (pas 403) si l'id ne correspond pas au propriétaire, pour ne pas révéler l'existence du fichier

**Tokens de partage :**
- UUID v4 (128 bits d'entropie) — probabilité de collision ou de devinette négligeable
- Liens publics accessibles sans authentification — intentionnel (partage avec des destinataires sans compte)

---

## Validation des entrées

- **`class-validator`** sur tous les DTOs : `@IsEmail`, `@MinLength`, `@IsInt`, `@Max`
- **`ValidationPipe` global** avec `whitelist: true` — les champs non déclarés sont ignorés silencieusement
- Vérifications serveur (en plus du client) :
  - Taille max fichier : 1 Go
  - Extensions interdites : `.exe`, `.bat`, `.cmd`, `.sh`, `.ps1`, `.msi`, `.com`
  - Durée expiration : 1 à 168 heures
  - Mot de passe fichier : minimum 6 caractères

---

## CORS

- Origines autorisées : liste blanche explicite (`FRONTEND_URL` env var)
- Aucun wildcard `*`
- `credentials: true` pour les headers d'autorisation

---

## Sécurité des fichiers stockés

- Chemin : `uploads/<userId>/<uuid>_<originalName>` — non devinable, non accessible directement par URL
- Fichiers temporaires Multer dans `/tmp/` — déplacés ou supprimés immédiatement après traitement
- Streaming : `fs.createReadStream().pipe(res)` — le fichier n'est jamais chargé entièrement en mémoire (important pour les gros fichiers)

---

## Améliorations pour la production

| Amélioration | Priorité | Raison |
|-------------|---------|--------|
| Cookies `httpOnly` à la place de localStorage | Haute | Protection XSS |
| HTTPS (TLS/Let's Encrypt) | Haute | Chiffrement en transit |
| Rate limiting sur `/api/auth/*` | Haute | Protection brute-force |
| Scan antivirus des fichiers uploadés (ClamAV) | Moyenne | Malware upload |
| Migration vers AWS S3 | Moyenne | Fichiers non exposés via disque local |
| Rotation JWT + refresh token court | Basse | Révocation des sessions |
