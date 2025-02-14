from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    # followers/following lists
    path('profile/<str:username>/followers/', views.followers_page, name='followers_page'),
    path('profile/<str:username>/following/', views.following_page, name='following_page'),
    # api endpoints for following/unfollowing actions:
    path('api/follow/<str:username>/', views.api_follow_user, name='api_follow_user'),
    path('api/unfollow/<str:username>/', views.api_unfollow_user, name='api_unfollow_user'),
]
