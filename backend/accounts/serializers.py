"""Sérialiseurs de l'application accounts — inscription et profil utilisateur."""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """Valide et crée un nouveau compte utilisateur.

    Deux champs de mot de passe sont demandés pour confirmer
    que l'utilisateur n'a pas fait de faute de frappe.
    """

    # write_only=True : le mot de passe n'est jamais renvoyé dans les réponses
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],  # règles Django : longueur, complexité, etc.
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        """Vérifie que les deux mots de passe saisis sont identiques."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Les mots de passe ne correspondent pas.'}
            )
        return data

    def create(self, validated_data):
        """Crée l'utilisateur en retirant password2 qui ne doit pas être stocké."""
        validated_data.pop('password2')
        # create_user hache automatiquement le mot de passe avant la sauvegarde
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur léger du profil utilisateur, utilisé sur l'endpoint /me/.

    On n'expose que les champs non sensibles — pas le mot de passe.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
