"""Configuration de l'application accounts pour Django."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Déclare l'application accounts auprès de Django.

    Cette app gère tout ce qui touche aux utilisateurs :
    inscription, connexion JWT et récupération du profil.
    Elle s'appuie sur le modèle User intégré à Django
    plutôt que de définir un modèle personnalisé,
    ce qui simplifie la gestion des droits et de l'admin.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
