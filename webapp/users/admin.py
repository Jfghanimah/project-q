from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GameList, Rating, UserFollower, Notification, Activity
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'profile_picture')}), # remove? "password'
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'profile_picture', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GameList)
admin.site.register(Rating)
admin.site.register(UserFollower)
admin.site.register(Notification)
admin.site.register(Activity)