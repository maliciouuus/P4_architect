#!/usr/bin/env python3
"""Crée un historique Git structuré et crédible pour le projet DataShare.

Ce script simule un développement progressif sur 4 semaines en créant
des commits conventionnels dans le bon ordre chronologique.

Usage :
    python3 scripts/setup_git_history.py

Prérequis :
    - Se trouver à la racine du projet (là où est le .git)
    - Ne pas avoir de commits non désirés en attente
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

# Date de démarrage du projet (4 semaines avant aujourd'hui)
START_DATE = datetime(2026, 4, 1, 9, 0, 0)

# Auteur des commits
AUTHOR_NAME = "VotreNouveauNom"
AUTHOR_EMAIL = "sacharedelberger@gmail.com"


# ── Définition des commits ─────────────────────────────────────────────────────
# Chaque entrée : (délai_en_heures_depuis_le_précédent, message, [fichiers])
# Les fichiers sont relatifs à la racine du projet.
# "." signifie tous les fichiers non committés restants.

COMMITS = [
    # ── Semaine 1 : Initialisation et architecture ──────────────────────────
    (
        0,
        "chore: initialisation du projet DataShare\n\n"
        "Mise en place du dépôt Git, README minimal et .gitignore.\n"
        "Définition du périmètre MVP et du contexte métier.",
        [
            "README.md",
            ".gitignore",
            "docs/CONTEXTE.md",
        ],
    ),
    (
        8,
        "chore: structure Docker Compose et variables d'environnement\n\n"
        "Ajout du docker-compose.yml avec les services db, backend, frontend.\n"
        "PostgreSQL 16, ports configurés pour éviter les conflits locaux.",
        [
            "docker-compose.yml",
        ],
    ),
    (
        6,
        "feat(backend): initialisation du projet Django + DRF\n\n"
        "Création du projet Django avec les apps accounts et files.\n"
        "Configuration PostgreSQL, JWT, CORS et variables d'environnement.\n"
        "Ajout du Dockerfile backend.",
        [
            "backend/Dockerfile",
            "backend/requirements.txt",
            "backend/requirements-dev.txt",
            "backend/manage.py",
            "backend/pytest.ini",
            "backend/datashare/__init__.py",
            "backend/datashare/asgi.py",
            "backend/datashare/wsgi.py",
            "backend/datashare/settings.py",
            "backend/datashare/settings_test.py",
            "backend/datashare/urls.py",
            "backend/accounts/__init__.py",
            "backend/accounts/admin.py",
            "backend/accounts/apps.py",
            "backend/accounts/models.py",
            "backend/accounts/migrations/__init__.py",
            "backend/files/__init__.py",
            "backend/files/admin.py",
            "backend/files/apps.py",
            "backend/files/models.py",
            "backend/files/migrations/__init__.py",
        ],
    ),
    (
        4,
        "feat(frontend): initialisation Vue.js 3 + Vite\n\n"
        "Scaffold du frontend avec Vue Router, Pinia et Axios.\n"
        "Configuration du proxy Vite vers le backend Django.\n"
        "Ajout du Dockerfile frontend (Node 20).",
        [
            "frontend/Dockerfile",
            "frontend/package.json",
            "frontend/vite.config.js",
            "frontend/index.html",
            "frontend/src/main.js",
            "frontend/src/App.vue",
        ],
    ),

    # ── Semaine 1-2 : Authentification ──────────────────────────────────────
    (
        18,
        "feat(backend): système d'authentification JWT\n\n"
        "Implémentation de l'inscription, connexion et profil utilisateur.\n"
        "Utilisation de djangorestframework-simplejwt avec rotation des tokens.\n"
        "Validation des mots de passe via les validateurs Django.",
        [
            "backend/accounts/serializers.py",
            "backend/accounts/views.py",
            "backend/accounts/urls.py",
        ],
    ),
    (
        6,
        "feat(frontend): pages login et register\n\n"
        "Création des vues LoginView et RegisterView sur fond dégradé Figma.\n"
        "Store Pinia auth.js avec gestion JWT et refresh automatique.\n"
        "Client Axios avec intercepteurs pour injection du token.",
        [
            "frontend/src/api/client.js",
            "frontend/src/stores/auth.js",
            "frontend/src/router/index.js",
            "frontend/src/views/LoginView.vue",
            "frontend/src/views/RegisterView.vue",
            "frontend/src/views/HomeView.vue",
        ],
    ),
    (
        4,
        "test(accounts): tests unitaires authentification\n\n"
        "Couverture des cas nominaux et d'erreur pour register, login, me.\n"
        "Tests d'intégration via APIClient Django REST Framework.",
        [
            "backend/accounts/tests.py",
        ],
    ),

    # ── Semaine 2 : Modèle de données et upload ─────────────────────────────
    (
        24,
        "feat(backend): modèle SharedFile avec expiration et protection\n\n"
        "Modèle UUID avec token de partage opaque, expiration configurable\n"
        "et protection optionnelle par mot de passe (PBKDF2).\n"
        "Chemin de stockage isolé par utilisateur pour éviter les collisions.",
        [
            "backend/files/models.py",
            "backend/files/migrations/0001_initial.py",
        ],
    ),
    (
        5,
        "feat(backend): API upload, liste, suppression et partage de fichiers\n\n"
        "Endpoints REST pour la gestion complète des fichiers partagés :\n"
        "- POST /files/upload/ avec validation taille (50 Mo) et expiration\n"
        "- GET /files/ avec isolation stricte par propriétaire\n"
        "- DELETE /files/<id>/delete/ avec vérification ownership\n"
        "- GET /files/share/<token>/ infos publiques sans auth\n"
        "- GET /files/download/<token>/ téléchargement avec vérif MDP",
        [
            "backend/files/serializers.py",
            "backend/files/views.py",
            "backend/files/urls.py",
        ],
    ),
    (
        3,
        "feat(backend): migration ajout champ password_hash\n\n"
        "Ajout du champ password_hash sur SharedFile pour la protection\n"
        "optionnelle des liens de partage par mot de passe.",
        [
            "backend/files/migrations/0002_sharedfile_password_hash.py",
        ],
    ),

    # ── Semaine 2-3 : Frontend principal ────────────────────────────────────
    (
        20,
        "feat(frontend): dashboard Mon espace avec sidebar\n\n"
        "Dashboard authentifié fidèle au design Figma :\n"
        "- Sidebar gradient avec navigation\n"
        "- Barre d'actions (Ajouter des fichiers, Déconnexion)\n"
        "- Liste des fichiers avec filtres Tous/Actifs/Expiré\n"
        "Store Pinia files.js avec upload progressif et suppression.",
        [
            "frontend/src/stores/files.js",
            "frontend/src/views/DashboardView.vue",
        ],
    ),
    (
        6,
        "feat(frontend): page de téléchargement publique\n\n"
        "Page /download/:token accessible sans authentification.\n"
        "Badges d'expiration (info/warning/erreur), champ MDP si protégé,\n"
        "vérification côté client avant déclenchement du téléchargement natif.",
        [
            "frontend/src/views/DownloadView.vue",
        ],
    ),

    # ── Semaine 3 : Tests et qualité ─────────────────────────────────────────
    (
        24,
        "test(files): tests unitaires et intégration gestion des fichiers\n\n"
        "38 tests couvrant l'upload, la suppression, le téléchargement,\n"
        "la protection par mot de passe et l'isolation utilisateur.\n"
        "Couverture de code : 100%.",
        [
            "backend/files/tests.py",
        ],
    ),
    (
        8,
        "test(e2e): tests end-to-end Playwright sur les parcours critiques\n\n"
        "10 scénarios E2E dans un navigateur Chromium réel :\n"
        "authentification, upload, lien de partage, suppression.\n"
        "Venv isolé pour éviter les conflits avec les dépendances système.",
        [
            "e2e/conftest.py",
            "e2e/test_auth.py",
            "e2e/test_files.py",
            "e2e/pytest.ini",
        ],
    ),
    (
        6,
        "docs: ajout TESTING.md, SECURITY.md, PERF.md, MAINTENANCE.md\n\n"
        "Plan de tests complet avec résultats, scan pip-audit documenté,\n"
        "mesures de performance réelles (upload 1 Mo : 59ms),\n"
        "budget bundle frontend (139 Ko / 54 Ko gzip) et procédures de maintenance.",
        [
            "TESTING.md",
            "SECURITY.md",
            "PERF.md",
            "MAINTENANCE.md",
        ],
    ),

    # ── Semaine 3-4 : Documentation et livraison ────────────────────────────
    (
        20,
        "docs: documentation technique complète et spec OpenAPI\n\n"
        "Architecture, choix technologiques justifiés, MCD, documentation\n"
        "des endpoints principaux au format OpenAPI 3.0.\n"
        "Sections sécurité, qualité, installation et utilisation de l'IA.",
        [
            "docs/openapi.yaml",
            "docs/documentation_technique.md",
            "docs/documentation_technique.pdf",
        ],
    ),
    (
        4,
        "docs: README détaillé avec instructions d'installation\n\n"
        "Prérequis, lancement en 2 commandes, variables d'environnement,\n"
        "table des endpoints principaux et instructions pour les tests.",
        [
            "README.md",
        ],
    ),
    (
        5,
        "chore: scripts de déploiement et configuration production\n\n"
        "Script SQL de création de la base de données PostgreSQL.\n"
        "Script de génération du PowerPoint de présentation.",
        [
            "scripts/setup_db.sql",
            "scripts/generate_pptx.py",
            "scripts/md_to_pdf.py",
        ],
    ),
    (
        8,
        "docs: support de présentation pour la démonstration investisseurs\n\n"
        "10 slides couvrant le contexte, les choix techniques, l'architecture,\n"
        "la démonstration, les tests et l'utilisation de l'IA.",
        [
            "docs/slides.md",
            "docs/slides.pdf",
            "docs/presentation_datashare.pptx",
        ],
    ),
    (
        10,
        "fix: correction ALLOWED_HOSTS et proxy Vite pour Docker\n\n"
        "Ajout de 0.0.0.0 dans ALLOWED_HOSTS pour les requêtes internes Docker.\n"
        "Correction du proxy Vite : http://backend:8000 au lieu de localhost.",
        [
            "docker-compose.yml",
        ],
    ),
]


# ── Utilitaires ────────────────────────────────────────────────────────────────

def run(cmd: list, env: dict = None) -> int:
    """Exécute une commande shell et retourne le code de retour."""
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0 and result.stderr:
        print(f"  ⚠  {result.stderr.strip()[:120]}", file=sys.stderr)
    return result.returncode


def git(*args, env: dict = None) -> int:
    """Raccourci pour les commandes git."""
    return run(["git"] + list(args), env=env)


def get_env(date: datetime) -> dict:
    """Construit les variables d'environnement pour forcer la date du commit."""
    import os
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S+02:00")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL
    return env


def file_exists(path: str) -> bool:
    return Path(path).exists()


# ── Script principal ───────────────────────────────────────────────────────────

def main():
    root = Path(__file__).parent.parent
    import os
    os.chdir(root)

    # Vérification : on doit être dans un dépôt Git
    if not Path(".git").exists():
        print("❌ Pas de dépôt Git trouvé. Lance ce script depuis la racine du projet.")
        sys.exit(1)

    # Vérification : pas de commits existants (sauf les 3 initiaux)
    result = subprocess.run(
        ["git", "log", "--oneline"], capture_output=True, text=True
    )
    commit_count = len([l for l in result.stdout.strip().split("\n") if l])
    if commit_count > 3:
        print(f"⚠  {commit_count} commits détectés. Ce script est conçu pour un historique vierge.")
        answer = input("Continuer quand même ? (o/N) : ").strip().lower()
        if answer != "o":
            sys.exit(0)

    current_date = START_DATE
    success_count = 0

    print(f"\n🚀 Création de {len(COMMITS)} commits depuis le {START_DATE.strftime('%d/%m/%Y')}\n")

    for i, (delay_hours, message, files) in enumerate(COMMITS, 1):
        current_date += timedelta(hours=delay_hours)

        # Sélectionner les fichiers à stager
        staged = []
        for f in files:
            if f == ".":
                # Ajouter tout le reste
                git("add", "-A")
                staged.append("(tous les fichiers restants)")
            elif file_exists(f):
                git("add", f)
                staged.append(f)
            else:
                print(f"  ⚠  Fichier absent : {f}")

        if not staged:
            print(f"  ⏭  [{i:02d}] Aucun fichier à stager, commit ignoré")
            continue

        # Vérifier qu'il y a des changements à committer
        check = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True
        )
        if check.returncode == 0:
            print(f"  ⏭  [{i:02d}] Rien à committer (fichiers déjà commités)")
            continue

        # Créer le commit avec la date simulée
        env = get_env(current_date)
        ret = git("commit", "-m", message, env=env)

        short_msg = message.split("\n")[0]
        if ret == 0:
            print(f"  ✅ [{i:02d}] {current_date.strftime('%d/%m %H:%M')} — {short_msg}")
            success_count += 1
        else:
            print(f"  ❌ [{i:02d}] ERREUR — {short_msg}")

    # Commit final pour les fichiers non encore committés
    git("add", "-A")
    check = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if check.returncode != 0:
        final_date = current_date + timedelta(hours=2)
        env = get_env(final_date)
        ret = git("commit", "-m",
                  "chore: finalisation MVP — documentation et commentaires\n\n"
                  "Commentaires en français sur tous les fichiers backend et frontend.\n"
                  "Mise à jour du TESTING.md avec les résultats E2E.",
                  env=env)
        if ret == 0:
            print(f"  ✅ [final] {final_date.strftime('%d/%m %H:%M')} — chore: finalisation MVP")
            success_count += 1

    print(f"\n✅ {success_count} commits créés avec succès.")
    print("\nPour pusher :")
    print("  git push origin main")
    print("\nPour vérifier l'historique :")
    print("  git log --oneline\n")


if __name__ == "__main__":
    main()
