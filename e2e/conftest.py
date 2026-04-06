"""Configuration des tests E2E Playwright pour DataShare.

Ces tests simulent un utilisateur réel dans un navigateur Chromium.
L'application doit tourner sur http://localhost:5173 avant de les lancer :

    docker compose up -d
    e2e/venv/bin/pytest e2e/
"""

import uuid
import pytest


# Identifiants uniques par session pour éviter les conflits en base
_uid = uuid.uuid4().hex[:8]
TEST_EMAIL = f"e2e_{_uid}@test.com"
TEST_PASSWORD = "E2ePass123!"
TEST_USERNAME = f"e2e_{_uid}"


@pytest.fixture(scope="session")
def credentials():
    """Identifiants de test partagés entre tous les tests de la session."""
    return {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "username": TEST_USERNAME,
    }
