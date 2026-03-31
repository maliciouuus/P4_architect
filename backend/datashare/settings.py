"""Configuration principale du projet Django DataShare.

Les valeurs sensibles (clé secrète, mot de passe BDD) sont lues
depuis les variables d'environnement pour ne jamais être committées.
Le fichier docker-compose.yml fournit ces variables en développement.
En production, les surcharger avec des vraies valeurs sécurisées.
"""

from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète Django — ne jamais la committer en production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-in-production')

# En production : passer DEBUG=False et définir ALLOWED_HOSTS correctement
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Librairies tierces
    'rest_framework',       # API REST
    'corsheaders',          # Gestion des origines croisées (CORS)
    # Applications métier
    'accounts',             # Inscription, connexion, profil
    'files',                # Upload, partage, téléchargement
]

MIDDLEWARE = [
    # CorsMiddleware doit être en premier pour traiter les preflight requests
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datashare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'datashare.wsgi.application'

# Base de données PostgreSQL — connexion configurée via variables d'environnement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'datashare'),
        'USER': os.environ.get('DB_USER', 'datashare'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'datashare'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Règles de validation des mots de passe utilisateur
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Fichiers uploadés stockés localement — à migrer vers S3 en production
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de Django REST Framework — JWT par défaut sur tous les endpoints
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Durées de vie des tokens JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),    # Token court pour limiter l'exposition
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh plus long pour le confort
    'ROTATE_REFRESH_TOKENS': True,                   # Nouveau refresh à chaque renouvellement
}

# Origines autorisées à appeler l'API (frontend Vue.js en dev)
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
).split(',')

# Limite d'upload : 50 Mo — vérifiée côté serveur (le client vérifie aussi)
FILE_UPLOAD_MAX_MEMORY_SIZE = 52_428_800
DATA_UPLOAD_MAX_MEMORY_SIZE = 52_428_800
MAX_FILE_SIZE = 52_428_800

# Durée de validité par défaut des liens de partage (en heures)
SHARE_LINK_EXPIRY_HOURS = int(os.environ.get('SHARE_LINK_EXPIRY_HOURS', 24))
