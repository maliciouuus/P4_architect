from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Désactiver la limite de taille pour les tests
MAX_FILE_SIZE = 1_073_741_824
SHARE_LINK_EXPIRY_HOURS = 168
MEDIA_ROOT = '/tmp/datashare_test_media'
