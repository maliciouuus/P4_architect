"""Tests unitaires et d'intégration pour l'application files.

Couvre tous les cas nominaux et d'erreur pour :
- La liste des fichiers (isolation par utilisateur)
- L'upload (taille, mot de passe, expiration personnalisée)
- La suppression (contrôle propriétaire)
- Le téléchargement (expiration, mot de passe, token invalide)
- Les infos publiques (endpoint sans auth)
- Le modèle SharedFile (is_expired, is_password_protected, hachage)

Base de données : SQLite en mémoire via settings_test.py.
Les fichiers sont écrits dans /tmp/datashare_test_media/.
"""

import io

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import SharedFile


@pytest.fixture
def client():
    """Client HTTP de test non authentifié."""
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPass123!',
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='OtherPass123!',
    )


@pytest.fixture
def auth_client(client, user):
    response = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'TestPass123!',
    }, format='json')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
    return client


def make_shared_file(owner, name='test.txt', content=b'Test content',
                     expired=False, password=''):
    sf = SharedFile(
        owner=owner,
        original_name=name,
        size=len(content),
        content_type='text/plain',
        expires_at=(
            timezone.now() - timezone.timedelta(hours=1)
            if expired
            else timezone.now() + timezone.timedelta(hours=24)
        ),
    )
    sf.set_password(password)
    sf.file.save(name, io.BytesIO(content))
    sf.save()
    return sf


@pytest.fixture
def shared_file(db, user):
    return make_shared_file(user)


@pytest.fixture
def expired_file(db, user):
    return make_shared_file(user, name='expired.txt', expired=True)


@pytest.fixture
def protected_file(db, user):
    return make_shared_file(user, name='protected.txt', password='secret123')


# ── List ──────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFileList:
    def test_list_requires_auth(self, client):
        response = client.get('/api/files/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_empty(self, auth_client):
        response = auth_client.get('/api/files/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_list_only_own_files(self, auth_client, shared_file, other_user, db):
        make_shared_file(other_user, name='other.txt')
        response = auth_client.get('/api/files/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['original_name'] == 'test.txt'

    def test_list_exposes_password_protected_flag(self, auth_client, protected_file):
        response = auth_client.get('/api/files/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['is_password_protected'] is True


# ── Upload ────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFileUpload:
    def test_upload_requires_auth(self, client):
        f = io.BytesIO(b'hello')
        f.name = 'test.txt'
        response = client.post('/api/files/upload/', {'file': f}, format='multipart')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_upload_success(self, auth_client):
        f = io.BytesIO(b'hello world')
        f.name = 'test.txt'
        response = auth_client.post('/api/files/upload/', {'file': f}, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['original_name'] == 'test.txt'
        assert 'share_url' in response.data
        assert response.data['is_expired'] is False
        assert response.data['is_password_protected'] is False

    def test_upload_with_password(self, auth_client):
        f = io.BytesIO(b'secret content')
        f.name = 'secret.txt'
        response = auth_client.post(
            '/api/files/upload/',
            {'file': f, 'password': 'mypassword'},
            format='multipart',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['is_password_protected'] is True

    def test_upload_custom_expiry(self, auth_client):
        f = io.BytesIO(b'content')
        f.name = 'file.txt'
        response = auth_client.post(
            '/api/files/upload/',
            {'file': f, 'expiry_hours': 72},
            format='multipart',
        )
        assert response.status_code == status.HTTP_201_CREATED
        token = response.data['share_token']
        sf = SharedFile.objects.get(share_token=token)
        delta = sf.expires_at - timezone.now()
        assert 71 < delta.total_seconds() / 3600 <= 72

    def test_upload_too_large(self, auth_client, settings):
        settings.MAX_FILE_SIZE = 10
        f = io.BytesIO(b'x' * 11)
        f.name = 'large.txt'
        response = auth_client.post('/api/files/upload/', {'file': f}, format='multipart')
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_upload_no_file(self, auth_client):
        response = auth_client.post('/api/files/upload/', {}, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ── Delete ────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFileDelete:
    def test_delete_requires_auth(self, client, shared_file):
        response = client.delete(f'/api/files/{shared_file.id}/delete/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_own_file(self, auth_client, shared_file):
        response = auth_client.delete(f'/api/files/{shared_file.id}/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not SharedFile.objects.filter(id=shared_file.id).exists()

    def test_cannot_delete_other_user_file(self, auth_client, other_user, db):
        other = make_shared_file(other_user, name='other.txt')
        response = auth_client.delete(f'/api/files/{other.id}/delete/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert SharedFile.objects.filter(id=other.id).exists()


# ── Download ──────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFileDownload:
    def test_download_valid_no_auth(self, client, shared_file):
        response = client.get(f'/api/files/download/{shared_file.share_token}/')
        assert response.status_code == status.HTTP_200_OK

    def test_download_expired(self, client, expired_file):
        response = client.get(f'/api/files/download/{expired_file.share_token}/')
        assert response.status_code == status.HTTP_410_GONE

    def test_download_invalid_token(self, client):
        response = client.get('/api/files/download/00000000-0000-0000-0000-000000000000/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_download_protected_no_password(self, client, protected_file):
        response = client.get(f'/api/files/download/{protected_file.share_token}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_download_protected_wrong_password(self, client, protected_file):
        response = client.get(
            f'/api/files/download/{protected_file.share_token}/?password=wrong'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_download_protected_correct_password(self, client, protected_file):
        response = client.get(
            f'/api/files/download/{protected_file.share_token}/?password=secret123'
        )
        assert response.status_code == status.HTTP_200_OK


# ── Public info ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFilePublicInfo:
    def test_public_info_valid(self, client, shared_file):
        response = client.get(f'/api/files/share/{shared_file.share_token}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['original_name'] == 'test.txt'
        assert response.data['is_expired'] is False
        assert response.data['is_password_protected'] is False

    def test_public_info_protected(self, client, protected_file):
        response = client.get(f'/api/files/share/{protected_file.share_token}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_password_protected'] is True

    def test_public_info_expired(self, client, expired_file):
        response = client.get(f'/api/files/share/{expired_file.share_token}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_expired'] is True

    def test_public_info_not_found(self, client):
        response = client.get('/api/files/share/00000000-0000-0000-0000-000000000000/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ── Model ─────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestSharedFileModel:
    def test_is_expired_false(self, shared_file):
        assert shared_file.is_expired is False

    def test_is_expired_true(self, expired_file):
        assert expired_file.is_expired is True

    def test_password_check_correct(self, protected_file):
        assert protected_file.check_password('secret123') is True

    def test_password_check_wrong(self, protected_file):
        assert protected_file.check_password('wrong') is False

    def test_no_password_not_protected(self, shared_file):
        assert shared_file.is_password_protected is False

    def test_str_representation(self, shared_file, user):
        assert 'test.txt' in str(shared_file)
        assert user.username in str(shared_file)
