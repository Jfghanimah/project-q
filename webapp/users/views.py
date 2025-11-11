from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import exception_handler
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.jwt_auth import JWTCookieAuthentication

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from .models import GameList, Rating, CustomUser, UserFollower, Activity, Notification
from .serializers import CustomUserSerializer


def custom_exception_handler(exc, context):
    """
    Custom API exception handler.
    Returns a consistent, more informative error structure.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If DRF handled the exception, we'll reformat its response
    if response is not None:
        custom_response = {
            'error_type': exc.__class__.__name__,
            'status_code': response.status_code,
            'detail': response.data
        }
        response.data = custom_response
    # If DRF can't handle the exception, we return None.
    # This allows Django's default error handling to take over and show the debug page.

    return response


class CustomRegisterView(RegisterView):
    """
    Custom registration view to automatically log the user in
    and set the auth cookie upon successful registration.
    """
    def perform_create(self, serializer):
        # Create the user as normal
        user = super().perform_create(serializer)
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # Manually create JWT tokens
        access_token, refresh_token = jwt_encode(user)

        # Use the CustomUserSerializer to get the user data for the response
        data = CustomUserSerializer(user, context=self.get_serializer_context()).data
        data['access'] = str(access_token)
        data['refresh'] = str(refresh_token)

        # Create the final response object
        response = Response(data, status=status.HTTP_201_CREATED)

        # Set the JWT cookies on the response
        from dj_rest_auth.app_settings import api_settings
        response.set_cookie(api_settings.JWT_AUTH_COOKIE, access_token, httponly=True)
        response.set_cookie(api_settings.JWT_AUTH_REFRESH_COOKIE, refresh_token, httponly=True)

        return response


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing user profiles and handling user actions like following.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'  # Use username instead of pk for lookups

    def update(self, request, *args, **kwargs):
        """
        Custom update method to detect if any changes were actually made.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Serialize the original data to compare against later
        original_serializer = self.get_serializer(instance)
        original_data = original_serializer.data

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Refresh the instance from the DB to get the final state
        instance.refresh_from_db()
        updated_serializer = self.get_serializer(instance)

        # Compare the data before and after the update
        if original_data == updated_serializer.data:
            return Response({"detail": "No changes were made to the profile."}, status=status.HTTP_200_OK)

        return Response(updated_serializer.data)


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
    # This is a more explicit and reliable way to get the followers
    follower_ids = UserFollower.objects.filter(user=profile_user).values_list('follower_id', flat=True)
    followers = CustomUser.objects.filter(id__in=follower_ids)

    # Create a list of tuples: (follower_user, is_followed_by_request_user)
    followers_with_status = []
    if request.user.is_authenticated:
        # Get a set of IDs for users the request.user is following, for efficient lookup
        following_ids = set(request.user.following.values_list('user_id', flat=True))
        for follower in followers:
            is_followed = follower.id in following_ids
            followers_with_status.append((follower, is_followed))
    else:
        for follower in followers:
            followers_with_status.append((follower, False))

    context = {
        'profile_user': profile_user,
        'followers_with_status': followers_with_status,
    }
    return render(request, 'followers.html', context)


def following_page(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    # Get all users that the profile_user is following
    # This is a more explicit and reliable way to get the users being followed
    following_ids_subquery = UserFollower.objects.filter(follower=profile_user).values_list('user_id', flat=True)
    following = CustomUser.objects.filter(id__in=following_ids_subquery)

    # Create a list of tuples: (followed_user, is_followed_by_request_user)
    following_with_status = []
    if request.user.is_authenticated:
        # Get a set of IDs for users the request.user is following, for efficient lookup
        following_ids = set(request.user.following.values_list('user_id', flat=True))
        for followed_user in following:
            is_followed = followed_user.id in following_ids
            following_with_status.append((followed_user, is_followed))
    else:
        for followed_user in following:
            following_with_status.append((followed_user, False))

    context = {
        'profile_user': profile_user,
        'following_with_status': following_with_status,
    }
    return render(request, 'following.html', context)
