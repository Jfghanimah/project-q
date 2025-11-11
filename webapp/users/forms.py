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

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude password from the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safely apply widget attributes only if the field exists in the form instance
        for field_name, config in self.get_widget_configs().items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(config.get('attrs', {}))
                if 'widget' in config:
                    self.fields[field_name].widget = config['widget']
                if 'help_text' in config:
                    self.fields[field_name].help_text = config['help_text']

    def get_widget_configs(self):
        return {
            'username': {'attrs': {'class': 'form-control'}},
            'display_name': {'attrs': {'class': 'form-control'}},
            'profile_picture': {'widget': forms.FileInput(attrs={'class': 'form-control'}), 'help_text': 'Max file size: 2MB. Image will be resized to 512x512.'},
            'bio': {'widget': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})},
            'clan_tag': {'attrs': {'class': 'form-control'}},
            'location': {'attrs': {'class': 'form-control'}},
            'birthday': {'widget': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})},
        }

    class Meta:
        model = CustomUser
        fields = ('display_name', 'username', 'profile_picture', 'bio', 'clan_tag', 'location', 'birthday')

class CustomAuthenticationForm(forms.Form):
    """
    A simple form for rendering email and password fields for the login page.
    The actual authentication is handled by the API.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
