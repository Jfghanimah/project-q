from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
# The user viewset will handle user-related API actions like follow/unfollow
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # Template-based views (for web frontend)
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/followers/', views.followers_page, name='followers_page'),
    path('profile/<str:username>/following/', views.following_page, name='following_page'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # API endpoints for user actions
    path('api/', include(router.urls)),

    # Add dj-rest-auth URLs for login, logout, registration, etc.
    path('api/auth/', include('dj_rest_auth.urls')),
    # Override the default registration view with our custom one that logs the user in
    path('api/auth/registration/', views.CustomRegisterView.as_view(), name='rest_register'),

    # Password Reset flow - using Django's built-in views which work with templates
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
