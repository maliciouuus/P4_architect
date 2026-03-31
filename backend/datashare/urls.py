"""Configuration des URLs principales du projet DataShare.

Ce fichier est le point d'entrée du routage Django. Il délègue :
- /api/auth/ → app accounts (inscription, connexion, profil)
- /api/files/ → app files (upload, liste, téléchargement, partage)
- /media/ → fichiers uploadés servis en développement

En production, les fichiers /media/ doivent être servis par nginx
et non par Django (performance et sécurité).
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    # Interface d'administration Django — utile pour la gestion manuelle en dev
    path('admin/', admin.site.urls),

    # Routes d'authentification : register, login, refresh, me
    path('api/auth/', include('accounts.urls')),

    # Routes de gestion des fichiers : upload, liste, suppression, partage
    path('api/files/', include('files.urls')),

# En développement uniquement : Django sert lui-même les fichiers uploadés
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
