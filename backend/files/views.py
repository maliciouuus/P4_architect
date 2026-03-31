"""Vues de l'application files — endpoints de l'API REST pour les fichiers."""

from django.conf import settings
from django.http import FileResponse, Http404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SharedFile
from .serializers import (
    FilePublicInfoSerializer,
    FileUploadSerializer,
    SharedFileSerializer,
)


class FileListView(generics.ListAPIView):
    """Retourne la liste des fichiers appartenant à l'utilisateur connecté.

    GET /api/files/
    Authentification requise. Seuls les fichiers dont l'utilisateur
    est propriétaire sont retournés — jamais ceux des autres.
    """

    serializer_class = SharedFileSerializer

    def get_queryset(self):
        """Filtre les fichiers par propriétaire pour garantir l'isolation."""
        return SharedFile.objects.filter(owner=self.request.user)


class FileUploadView(APIView):
    """Gère l'upload d'un nouveau fichier.

    POST /api/files/upload/
    Authentification requise. Accepte un fichier multipart avec un
    mot de passe optionnel et une durée d'expiration en heures.
    """

    # On accepte les deux formats de formulaire multipart habituels
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """Valide, stocke le fichier et retourne ses métadonnées avec le lien de partage."""
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded = serializer.validated_data['file']
        raw_password = serializer.validated_data.get('password', '')
        expiry_hours = serializer.validated_data.get(
            'expiry_hours', settings.SHARE_LINK_EXPIRY_HOURS
        )

        # Vérification de la taille côté serveur — le client vérifie aussi,
        # mais on ne fait jamais confiance au seul contrôle frontend
        if uploaded.size > settings.MAX_FILE_SIZE:
            return Response(
                {'detail': 'Le fichier dépasse la taille maximale autorisée (50 Mo).'},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        expires_at = timezone.now() + timezone.timedelta(hours=expiry_hours)

        # On construit l'objet sans le sauvegarder pour pouvoir hacher
        # le mot de passe avant le premier accès à la base
        shared_file = SharedFile(
            owner=request.user,
            original_name=uploaded.name,
            size=uploaded.size,
            content_type=uploaded.content_type or 'application/octet-stream',
            expires_at=expires_at,
        )
        shared_file.set_password(raw_password)
        shared_file.file = uploaded
        shared_file.save()

        return Response(
            SharedFileSerializer(shared_file, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class FileDeleteView(generics.DestroyAPIView):
    """Supprime un fichier appartenant à l'utilisateur connecté.

    DELETE /api/files/<id>/delete/
    Authentification requise. Si l'identifiant correspond à un fichier
    d'un autre utilisateur, on retourne 404 plutôt que 403 pour ne pas
    révéler l'existence du fichier.
    """

    serializer_class = SharedFileSerializer

    def get_queryset(self):
        """Restreint la suppression aux fichiers du propriétaire connecté."""
        return SharedFile.objects.filter(owner=self.request.user)


class FilePublicInfoView(APIView):
    """Retourne les informations publiques d'un fichier partagé.

    GET /api/files/share/<token>/
    Accessible sans authentification. Utilisé par la page de téléchargement
    Vue.js pour afficher le nom, la taille et l'état du lien avant de
    déclencher le téléchargement réel.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        """Recherche le fichier par son token de partage et retourne ses infos publiques."""
        try:
            shared_file = SharedFile.objects.get(share_token=token)
        except SharedFile.DoesNotExist:
            raise Http404
        return Response(FilePublicInfoSerializer(shared_file).data)


class FileDownloadView(APIView):
    """Déclenche le téléchargement d'un fichier via son lien de partage.

    GET /api/files/download/<token>/
    Accessible sans authentification. Vérifie l'expiration et,
    si le fichier est protégé, valide le mot de passe passé en query param.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        """Vérifie le token, l'expiration et le mot de passe, puis sert le fichier."""
        try:
            shared_file = SharedFile.objects.get(share_token=token)
        except SharedFile.DoesNotExist:
            raise Http404

        # HTTP 410 Gone indique que la ressource a existé mais n'est plus disponible
        if shared_file.is_expired:
            return Response(
                {'detail': 'Ce lien de téléchargement a expiré.'},
                status=status.HTTP_410_GONE,
            )

        # Si le fichier est protégé, on vérifie le mot de passe avant de servir
        if shared_file.is_password_protected:
            password = request.query_params.get('password', '')
            if not shared_file.check_password(password):
                return Response(
                    {'detail': 'Mot de passe incorrect.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        # FileResponse streame le fichier sans le charger entièrement en mémoire
        return FileResponse(
            shared_file.file.open('rb'),
            content_type=shared_file.content_type,
            as_attachment=True,
            filename=shared_file.original_name,
        )
