from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import GameList, Rating, CustomUser, UserFollower


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
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
        'followers_list': followers_list,
        'following_list': following_list,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, username):
    # Ensure that only the owner can edit their profile
    if request.user.username != username:
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def followers_page(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    # "Followers" are those who follow profile_user.
    followers_relations = profile_user.followers.select_related('follower')
    followers = []
    for relation in followers_relations:
        follower_user = relation.follower
        is_following = False
        if request.user.is_authenticated:
            is_following = UserFollower.objects.filter(
                user=follower_user, follower=request.user).exists()
        followers.append({
            'user': follower_user,
            'is_following': is_following,
        })
    context = {
        'profile_user': profile_user,
        'followers': followers,
    }
    return render(request, 'followers.html', context)


def following_page(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    # "Following" are those whom profile_user is following.
    following_relations = profile_user.following.select_related('user')
    following = []
    for relation in following_relations:
        following_user = relation.user
        is_following = False
        if request.user.is_authenticated:
            is_following = UserFollower.objects.filter(
                user=following_user, follower=request.user).exists()
        following.append({
            'user': following_user,
            'is_following': is_following,
        })
    context = {
        'profile_user': profile_user,
        'following': following,
    }
    return render(request, 'following.html', context)


@login_required
@require_POST
def api_follow_user(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if target_user == request.user:
        return JsonResponse({'error': "You cannot follow yourself."}, status=400)

    # Check if already following
    if UserFollower.objects.filter(user=target_user, follower=request.user).exists():
        return JsonResponse({'message': f"You are already following {target_user.username}."})

    UserFollower.objects.create(user=target_user, follower=request.user)
    follower_count = UserFollower.objects.filter(user=target_user).count()
    return JsonResponse({'message': f"You are now following {target_user.username}.", 'follower_count': follower_count})


@login_required
@require_POST
def api_unfollow_user(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    follow_relation = UserFollower.objects.filter(
        user=target_user, follower=request.user).first()
    if follow_relation:
        follow_relation.delete()
        follower_count = UserFollower.objects.filter(user=target_user).count()
        return JsonResponse({'message': f"You have unfollowed {target_user.username}.", 'follower_count': follower_count})
    else:
        return JsonResponse({'message': f"You are not following {target_user.username}."})
