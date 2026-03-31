"""URLs de l'application files — routes de gestion des fichiers partagés."""

from django.urls import path

from .views import (
    FileDeleteView,
    FileDownloadView,
    FileListView,
    FilePublicInfoView,
    FileUploadView,
)

urlpatterns = [
    # Liste des fichiers de l'utilisateur connecté
    path('', FileListView.as_view(), name='file-list'),

    # Upload d'un nouveau fichier avec expiration et mot de passe optionnels
    path('upload/', FileUploadView.as_view(), name='file-upload'),

    # Suppression d'un fichier (propriétaire uniquement)
    path('<uuid:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),

    # Infos publiques d'un fichier — utilisé par la page de téléchargement
    path('share/<uuid:token>/', FilePublicInfoView.as_view(), name='file-public-info'),

    # Téléchargement effectif via le token de partage
    path('download/<uuid:token>/', FileDownloadView.as_view(), name='file-download'),
]
