from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import validate_image_file_size
from dj_rest_auth.registration.serializers import RegisterSerializer

CustomUser = get_user_model()


class CustomImageField(serializers.ImageField):
    """
    A custom ImageField that handles empty strings from multipart forms.
    If an empty string is received, it's treated as if no file was uploaded.
    """
    def to_internal_value(self, data):
        # If the incoming data is an empty string, return None.
        # This will be interpreted by DRF as "do not update this field".
        if data == '':
            return None
        return super().to_internal_value(data)


class CustomUserSerializer(serializers.ModelSerializer):
    # Use the custom image field to handle empty file inputs gracefully.
    profile_picture = CustomImageField(required=False, validators=[validate_image_file_size])
    class Meta:
        model = CustomUser
        # Expose fields that are safe and useful for API clients
        fields = ('id', 'username', 'display_name', 'email', 'profile_picture', 'bio', 'clan_tag', 'location', 'birthday', 'date_joined')
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
