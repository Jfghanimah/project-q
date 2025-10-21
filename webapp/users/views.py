from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from .models import GameList, Rating, CustomUser, UserFollower, Activity, Notification
from .serializers import CustomUserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing user profiles and handling user actions like following.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'  # Use username instead of pk for lookups

    @action(detail=True, methods=['post', 'delete'], url_path='follow')
    def follow_unfollow(self, request, username):
        target_user = self.get_object()
        if target_user == request.user:
            return Response({'error': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            # Follow action
            _, created = UserFollower.objects.get_or_create(user=target_user, follower=request.user)
            if not created:
                return Response({'message': f"You are already following {target_user.username}."}, status=status.HTTP_200_OK)
            follower_count = UserFollower.objects.filter(user=target_user).count()
            return Response({'message': f"You are now following {target_user.username}.", 'follower_count': follower_count}, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            # Unfollow action
            follow_relation = UserFollower.objects.filter(user=target_user, follower=request.user).first()
            if follow_relation:
                follow_relation.delete()
                follower_count = UserFollower.objects.filter(user=target_user).count()
                return Response({'message': f"You have unfollowed {target_user.username}.", 'follower_count': follower_count}, status=status.HTTP_200_OK)
            else:
                return Response({'error': f"You are not following {target_user.username}."}, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    # This view just renders the login page. The actual login is handled by the API.
    # If a user is already logged in, redirect them from the login page.
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    # If a user is already logged in, redirect them from the register page.
    if request.user.is_authenticated:
        return redirect('home')

    # The view's only job is to render the page with the form.
    # The actual registration is handled by the API via JavaScript.
    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    ratings = Rating.objects.filter(user=profile_user)
    user_games = [rating.game for rating in ratings]
    game_lists = GameList.objects.filter(user=profile_user)

    is_owner = request.user.is_authenticated and (profile_user.pk == request.user.pk)
    is_following = False
    if request.user.is_authenticated and not is_owner:
        is_following = UserFollower.objects.filter(
            user=profile_user, follower=request.user).exists()

    # Correctly fetch followers and following:
    followers_list = profile_user.followers.all()  # People following this user
    following_list = profile_user.following.all()    # People this user is following

    context = {
        'profile_user': profile_user,
        'user_games': user_games,
        'game_lists': game_lists,
        'is_owner': is_owner,
        'is_following': is_following,
        'ratings': ratings,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, username):
    # Ensure that only the owner can edit their profile
    profile_user = get_object_or_404(CustomUser, username=username)
    if profile_user != request.user:
        return redirect('profile', username=profile_user.username)

    # The view's only job is to render the page with the form populated with user data.
    # The actual update is handled by the API via JavaScript.
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def followers_page(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    # Get all users that follow the profile_user
    followers = CustomUser.objects.filter(following__user=profile_user)

    # Check which of these followers the current logged-in user is also following
    following_by_request_user = set()
    if request.user.is_authenticated:
        following_by_request_user = set(
            UserFollower.objects.filter(follower=request.user, user__in=followers)
            .values_list('user_id', flat=True)
        )

    context = {
        'profile_user': profile_user,
        'followers': followers,
        'following_by_request_user': following_by_request_user,
    }
    return render(request, 'followers.html', context)


def following_page(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    # Get all users that the profile_user is following
    following = CustomUser.objects.filter(followers__follower=profile_user)

    # Check which of these users the current logged-in user is also following
    following_by_request_user = set()
    if request.user.is_authenticated:
        following_by_request_user = set(
            UserFollower.objects.filter(follower=request.user, user__in=following)
            .values_list('user_id', flat=True)
        )
    context = {
        'profile_user': profile_user,
        'following': following,
        'following_by_request_user': following_by_request_user,
    }
    return render(request, 'following.html', context)
