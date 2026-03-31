"""Vues de l'application accounts — inscription et profil utilisateur."""

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Crée un nouveau compte utilisateur.

    POST /api/auth/register/
    Accessible sans authentification. Délègue la validation
    et la création à RegisterSerializer.
    """

    serializer_class = RegisterSerializer
    # On autorise tout le monde — c'est la page d'inscription
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    """Retourne le profil de l'utilisateur actuellement connecté.

    GET /api/auth/me/
    Authentification requise. Utilisé par le frontend pour
    initialiser le store d'authentification au chargement de l'app.
    """

    def get(self, request):
        """Sérialise et retourne les données de l'utilisateur connecté."""
        return Response(UserSerializer(request.user).data)
