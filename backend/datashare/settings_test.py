from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Désactiver la limite de taille pour les tests
MAX_FILE_SIZE = 52_428_800
SHARE_LINK_EXPIRY_HOURS = 24
MEDIA_ROOT = '/tmp/datashare_test_media'
