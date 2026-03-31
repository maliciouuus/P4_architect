"""Configuration de l'application files pour Django."""

from django.apps import AppConfig


class FilesConfig(AppConfig):
    """Déclare l'application files auprès de Django.

    Django utilise cette classe pour initialiser l'app au démarrage.
    Le champ default_auto_field définit le type de clé primaire
    utilisé par défaut pour les modèles qui n'en spécifient pas une.
    Ici on utilise BigAutoField (entier 64 bits) mais notre modèle
    SharedFile surcharge cela avec un UUID.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files'
