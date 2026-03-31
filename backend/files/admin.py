"""Enregistrement des modèles de l'app files dans l'interface d'administration Django."""

from django.contrib import admin

from .models import SharedFile


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les fichiers partagés.

    Permet de consulter et gérer les fichiers uploadés directement
    depuis l'interface Django Admin (/admin/).
    """

    # Colonnes affichées dans la liste
    list_display = ('original_name', 'owner', 'size', 'expires_at', 'is_expired', 'created_at')

    # Filtres disponibles dans la barre latérale
    list_filter = ('owner',)

    # Champ de recherche par nom de fichier ou propriétaire
    search_fields = ('original_name', 'owner__username')

    # Champs en lecture seule — on ne modifie pas les tokens ni les dates auto
    readonly_fields = ('id', 'share_token', 'created_at', 'is_expired', 'is_password_protected')
