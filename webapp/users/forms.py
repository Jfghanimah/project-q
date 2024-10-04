from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'profile_picture', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude password from the form

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'profile_picture')
