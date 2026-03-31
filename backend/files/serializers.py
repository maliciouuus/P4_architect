"""Sérialiseurs de l'application files — conversion modèles ↔ JSON."""

from rest_framework import serializers

from .models import SharedFile


class SharedFileSerializer(serializers.ModelSerializer):
    """Sérialiseur complet d'un fichier partagé, utilisé pour la liste et l'upload.

    Expose les métadonnées du fichier ainsi que l'URL de partage calculée
    dynamiquement à partir de l'hôte de la requête entrante.
    """

    # Champ calculé à la volée — non stocké en base
    share_url = serializers.SerializerMethodField()

    class Meta:
        model = SharedFile
        fields = (
            'id', 'original_name', 'size', 'content_type',
            'share_token', 'share_url', 'expires_at', 'created_at',
            'is_expired', 'is_password_protected',
        )
        # Tous les champs sont en lecture seule : l'écriture passe par la vue
        read_only_fields = fields

    def get_share_url(self, obj):
        """Construit l'URL de la page de téléchargement côté frontend.

        On pointe vers le port 5173 (Vite) et non vers l'API Django,
        pour que le destinataire arrive sur la page Vue.js.
        """
        request = self.context.get('request')
        if request:
            host = request.get_host().split(':')[0]
            return f'{request.scheme}://{host}:5173/download/{obj.share_token}'
        return f'http://localhost:5173/download/{obj.share_token}'


class FileUploadSerializer(serializers.Serializer):
    """Valide les données envoyées lors de l'upload d'un fichier.

    Trois champs sont attendus :
    - file : le fichier binaire (obligatoire)
    - password : mot de passe de protection optionnel
    - expiry_hours : durée de validité du lien en heures (1 à 720)
    """

    file = serializers.FileField()
    password = serializers.CharField(required=False, allow_blank=True, default='')
    expiry_hours = serializers.IntegerField(
        required=False,
        default=24,
        min_value=1,
        max_value=720,  # maximum 30 jours
    )


class FilePublicInfoSerializer(serializers.ModelSerializer):
    """Sérialiseur public d'un fichier partagé, sans informations sensibles.

    Utilisé sur l'endpoint GET /files/share/<token>/ accessible sans
    authentification. Il expose uniquement ce dont la page de téléchargement
    a besoin : nom, taille, état d'expiration et protection par mot de passe.
    """

    class Meta:
        model = SharedFile
        fields = (
            'original_name', 'size', 'content_type',
            'expires_at', 'is_expired', 'is_password_protected',
        )
