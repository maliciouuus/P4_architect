"""Vues de l'application accounts — inscription et profil utilisateur."""

import logging

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer

logger = logging.getLogger('accounts')


class RegisterView(generics.CreateAPIView):
    """Crée un nouveau compte utilisateur.

    POST /api/auth/register/
    Accessible sans authentification. Délègue la validation
    et la création à RegisterSerializer.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Crée l'utilisateur et logue l'événement."""
        user = serializer.save()
        logger.info('Nouvel utilisateur inscrit — username=%s', user.username)


class MeView(APIView):
    """Retourne le profil de l'utilisateur actuellement connecté.

    GET /api/auth/me/
    Authentification requise. Utilisé par le frontend pour
    initialiser le store d'authentification au chargement de l'app.
    """

    def get(self, request):
        """Sérialise et retourne les données de l'utilisateur connecté."""
        return Response(UserSerializer(request.user).data)
