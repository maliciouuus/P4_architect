"""Modèles de l'application files — gestion des fichiers partagés."""

import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def user_upload_path(instance, filename):
    """Génère un chemin de stockage unique pour chaque fichier uploadé.

    Le chemin est de la forme uploads/<id_utilisateur>/<uuid>_<nom_fichier>
    afin d'éviter les collisions même si deux utilisateurs uploadent un
    fichier portant le même nom.
    """
    return f'uploads/{instance.owner.id}/{uuid.uuid4()}_{filename}'


class SharedFile(models.Model):
    """Représente un fichier uploadé par un utilisateur et partageable via un lien."""

    # Identifiant interne en UUID — on évite les IDs séquentiels prévisibles
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Propriétaire du fichier — si l'utilisateur est supprimé, ses fichiers le sont aussi
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    # Nom original conservé pour proposer le bon nom lors du téléchargement
    original_name = models.CharField(max_length=255)

    # Fichier physique sur le disque
    file = models.FileField(upload_to=user_upload_path)

    # Taille en octets, stockée pour affichage sans lire le fichier
    size = models.PositiveBigIntegerField()

    # Type MIME utilisé dans l'en-tête Content-Type lors du téléchargement
    content_type = models.CharField(max_length=100)

    # Token opaque inclus dans le lien de partage — UUID v4, non devinable
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Date d'expiration du lien de partage
    expires_at = models.DateTimeField()

    # Date d'upload, remplie automatiquement à la création
    created_at = models.DateTimeField(auto_now_add=True)

    # Hash du mot de passe optionnel (PBKDF2) — vide si le fichier n'est pas protégé
    password_hash = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        # Les fichiers les plus récents apparaissent en premier dans la liste
        ordering = ['-created_at']

    @property
    def is_expired(self):
        """Retourne True si la date d'expiration est dépassée."""
        return timezone.now() > self.expires_at

    @property
    def is_password_protected(self):
        """Retourne True si le fichier est protégé par un mot de passe."""
        return bool(self.password_hash)

    def set_password(self, raw_password):
        """Hache et stocke le mot de passe. Si vide, retire la protection."""
        self.password_hash = make_password(raw_password) if raw_password else ''

    def check_password(self, raw_password):
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f'{self.original_name} ({self.owner.username})'
