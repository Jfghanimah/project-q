from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Public profiles: always accessed via /profile/<username>/
    path('profile/<str:username>/', views.profile, name='profile'),
    # Edit profile (only accessible for the owner)
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
]
