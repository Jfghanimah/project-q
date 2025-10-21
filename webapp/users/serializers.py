from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from dj_rest_auth.registration.serializers import RegisterSerializer

CustomUser = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, used for retrieving and updating user info.
    """
    class Meta:
        model = CustomUser
        # Expose fields that are safe and useful for API clients
        fields = ('id', 'username', 'email', 'profile_picture', 'bio', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer to enforce username and email uniqueness.
    """
    username = serializers.CharField(
        max_length=32,
        # Add a validator to ensure the username is unique
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        # Add a validator to ensure the email is unique
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
