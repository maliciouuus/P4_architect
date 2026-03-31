"""Tests unitaires et d'intégration pour l'application accounts.

Couvre les cas nominaux et d'erreur pour :
- L'inscription (RegisterView)
- La connexion JWT (TokenObtainPairView)
- La récupération du profil (MeView)

Les tests utilisent une base SQLite en mémoire (settings_test.py)
pour être rapides et isolés, sans dépendance à PostgreSQL.
"""

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Client HTTP de test — simule les requêtes du frontend."""
    return APIClient()


@pytest.fixture
def user(db):
    """Crée un utilisateur de test en base — disponible dans tous les tests qui en ont besoin."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPass123!',
    )


@pytest.fixture
def auth_client(client, user):
    """Client HTTP déjà authentifié — le token JWT est injecté dans les headers."""
    response = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'TestPass123!',
    }, format='json')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
    return client


@pytest.mark.django_db
class TestRegister:
    def test_register_success(self, client):
        response = client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'
        assert User.objects.filter(username='newuser').exists()

    def test_register_password_mismatch(self, client):
        response = client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'StrongPass123!',
            'password2': 'DifferentPass!',
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_username(self, client, user):
        response = client.post('/api/auth/register/', {
            'username': 'testuser',
            'email': 'other@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, client):
        response = client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '123',
            'password2': '123',
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, client, user):
        response = client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPass123!',
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_wrong_password(self, client, user):
        response = client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrong',
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_unknown_user(self, client):
        response = client.post('/api/auth/login/', {
            'username': 'nobody',
            'password': 'anything',
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMe:
    def test_me_authenticated(self, auth_client, user):
        response = auth_client.get('/api/auth/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'

    def test_me_unauthenticated(self, client):
        response = client.get('/api/auth/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
