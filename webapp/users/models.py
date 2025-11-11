from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.files import File
#from games.models import Game
from PIL import Image
import os
from io import BytesIO


def validate_image_file_size(value):
    if value.size > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("The maximum file size that can be uploaded is 2MB.")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        if not username:
            raise ValueError('The Username field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=32, unique=True)
    display_name = models.CharField(max_length=32, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, validators=[validate_image_file_size])
    bio = models.CharField(max_length=128, blank=True, null=True)
    clan_tag = models.CharField(max_length=5, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_premium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # For admin access
    is_active = models.BooleanField(default=True)  # For account activation
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required when creating superusers

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Keep track of the original profile picture to see if it has changed.
        if self.pk:
            original_instance = CustomUser.objects.get(pk=self.pk)
            if original_instance.profile_picture != self.profile_picture:
                is_new_picture = True
            else:
                is_new_picture = False
        else:
            is_new_picture = True

        # If the user is being created and display_name is not set, default it to username
        if not self.pk and not self.display_name:
            self.display_name = self.username

        # Only process the image if it's a new upload.
        if self.profile_picture and is_new_picture:
            # Open the uploaded image
            img = Image.open(self.profile_picture)

            # Resize the image if it's too large
            max_size = (512, 512)
            if img.height > max_size[1] or img.width > max_size[0]:
                img.thumbnail(max_size)

            # Save the processed image back to a memory buffer
            output = BytesIO()
            # Convert to RGB to ensure it can be saved as JPEG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(output, format='JPEG', quality=85)
            output.seek(0)

            # Replace the original image with the processed one
            filename = os.path.basename(self.profile_picture.name)
            self.profile_picture = File(output, name=filename)

        super().save(*args, **kwargs)

class UserFollower(models.Model):
    user = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"

    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    object_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"


# Game Related Models
class GameList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    games = models.ManyToManyField('games.Game', related_name='game_lists')

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    rating_value = models.IntegerField()
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username}'s rating for {self.game.title}"