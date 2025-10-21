from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        help_text='32 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'profile_picture')

class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude password from the form

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'profile_picture', 'bio')

class CustomAuthenticationForm(forms.Form):
    """
    A simple form for rendering email and password fields for the login page.
    The actual authentication is handled by the API.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
