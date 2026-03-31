"""URLs de l'application accounts — routes d'authentification."""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import MeView, RegisterView

urlpatterns = [
    # Création de compte — accessible sans token
    path('register/', RegisterView.as_view(), name='register'),

    # Connexion — retourne un access token (1h) et un refresh token (7j)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Renouvellement du token d'accès sans re-saisir le mot de passe
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profil de l'utilisateur connecté — utilisé au chargement de l'app frontend
    path('me/', MeView.as_view(), name='me'),
]
