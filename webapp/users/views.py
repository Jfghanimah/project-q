from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import GameList, Rating, CustomUser

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
    # Fetch the user by username
    profile_user = get_object_or_404(CustomUser, username=username)
    # Get the ratings and game lists
    ratings = Rating.objects.filter(user=profile_user)
    user_games = [rating.game for rating in ratings]
    game_lists = GameList.objects.filter(user=profile_user)
    
    # Determine if the logged-in user is viewing their own profile
    is_owner = request.user.is_authenticated and (profile_user.pk == request.user.pk)
    
    context = {
        'profile_user': profile_user,
        'user_games': user_games,
        'game_lists': game_lists,
        'is_owner': is_owner,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request, username):
    # Ensure that only the owner can edit their profile
    if request.user.username != username:
        return redirect('profile', username=request.user.username)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
